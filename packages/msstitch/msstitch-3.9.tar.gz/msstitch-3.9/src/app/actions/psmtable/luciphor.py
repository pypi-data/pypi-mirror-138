import sys
import re
from os import environ
from Bio import SeqIO
from string import Template

#from create_modfile import get_msgfmods, categorize_mod, parse_cmd_mod, modpos, NON_BLOCKING_MODS

from app.dataformats import mzidtsv as dm
from app.dataformats.defaultmods import defaultmods

def get_msgf_seq_mass(mass):
    return '{}{}'.format('+' if mass > 0 else '', round(mass, 3))


def get_luci_mod(pos, aa, mass):
    if pos == 'N-term':
        residue = '['
    elif pos == 'C-term':
        residue = ']'
    else:
        residue = aa
    return '{} {}'.format(residue, mass)


def populate_mod(msgfmod, aa):
    return {'mass': float(msgfmod[0]), 'aa': aa, 'name': msgfmod[4],
            'pos': msgfmod[3], 'var': msgfmod[2] == 'opt'}


def parse_input_mods(input_mods):
    defaultmods = {x.split(',')[0]: x for x in defaultmods.strip().split('\n') 
            if x.strip()[0] != '#'}
    mods, fixmods = [], {}

    for passedmod in input_mods:
        msgfmod = passedmod.split(',')
        stdmod = passedmod.split(':')
        if len(msgfmod) == 5:
            for aa in msgfmod[1]:
                mod = populate_mod(msgfmod, aa)
        else:
            defmod = defaultmods[stdmod[0]]
            aas = stdmod[1] if len(stdmod) == 2 else defmod['aa']
            for aa in aas:
                populate_mod(defmod, aa)
        mods.append(mod)
        if not mod['var']:
            # pos included here for the mod can be */N-term
            mp = f"{mod['aa']}_{mod['pos']}"
            if mp not in fixmods:
                fixmods[mp] = []
            fixmods[mp].append(mod)
    # Change masses for MSGF in case you have a variable and fixed mod on the same
    # amino acid (e.g. Acetyl and TMT, but not GG and TMT)
    for mod in mods:
        mp = f"{mod['aa']}_{mod['pos']}"
        if mp in fixmods:
            nonblocked = dm.NON_BLOCKING_MODS[mod['name']] if mod['name'] in dm.NON_BLOCKING_MODS else []
            blocked = sum(x['mass'] for x in fixmods[mp] if x['name'] not in nonblocked)
            mod['masschange'] = round(-(blocked - mod['mass']), 5)
        else:
            mod['masschange'] = mod['mass']

    return mods


def get_ptm_mass(ptmnames, ):
    ptms_mass = []
    for cmdptm in ptmnames:
        for ptm in parse_cmd_mod(cmdptm, msgfmods):
            # FIXME OPTIONAL competition for multi-residue/line spec, how to know which 
            # modifications can compete?
            ptm = ptm.split(',')
            realmodmass = ptm[0]
            if modpos(ptm) in fixedmods:
                fixmass = sum([float(x[0]) for x in fixedmods[modpos(ptm)]])
                ptm[0] = str(round(-(fixmass - float(ptm[0])), 5))
                print(realmodmass, ptm)
            ptms_mass.append(add_mods_translationtable(ptm, massconversion_msgf))
            for residue in ptm[1]:
                luciptm = get_luci_mod([ptm[0], residue, *ptm[2:]])
                ## TODO
                ## Now we add e.g. -187 if acetyl mod competes with fixed TMT
                ## That does not work, but the below line also doesnt work, which
                ## Puts the actual +42 mass in the luciphor config
                ## Total mass of residue is in the luci input K+42 = 170
                ## Luciphor ignores fixed mod containing residues I think
                #luciptm = get_luci_mod([realmodmass, residue, *ptm[2:]])
                if luciptm not in target_mods:
                    target_mods.append(luciptm)
                    decoy_mods.add(ptm[0])
        # Neutral loss only for phospho (and possibly glycosylation), add more if we need
        nlosses, decoy_nloss = [], []
        if ptm[4] == 'Phospho':
            nlosses.append('sty -H3PO4 -97.97690')
            decoy_nloss.append('X -H3PO4 -97.07690')
    return ptms_mass

###############
# FIXME we can also incorporate create_modfile for MSGF

def create_luciphor_input(psms, template, fixedmods, varmods, ptms, psmfields,
        lucheader, ms2tol, ms2toltype, mzmlpath, lucialgo, maxcharge, maxlen,
        minpsms, threads):
    """Writes the following files:
        - luciphor_config_input - the config file
        - luciphor_psm_input - the PSMs with PTM in luciphor format
        - ptm_psms - the PSMs for adding luciphor to afterwards

    Fixed mods, var mods, ptms - {'mass': float, 'aa': str,  'name': str, 'pos': str}
    """
    massconversion_msgf = {}
    target_mods, decoy_mods, lucifixed, lucivar = [], set(), [], []

    # Prep fixed mods for luciphor template
    for mod in fixedmods:
        massconversion_msgf[get_msgf_seq_mass(mod['masschange'])] = mod['masschange']
        lucimod = get_luci_mod(mod['pos'], mod['aa'], mod['masschange'])
        if lucimod not in lucifixed:
            lucifixed.append(lucimod)
    # Var mods too, and add to mass list to filter PSMs on later (all var mods must be annotated on sequence input)
    varmods_mass = []
    for mod in varmods:
        msgf_mass = get_msgf_seq_mass(mod['masschange'])
        massconversion_msgf[msgf_mass] = mod['masschange']
        varmods_mass.append(msgf_mass)
        lucimod = get_luci_mod(mod['pos'], mod['aa'], mod['masschange'])
        if lucimod not in lucivar:
            lucivar.append(lucimod)

    # Get PTMs from cmd line and prep for template
    ptms_mass = set()
    nlosses, decoy_nloss = set(), set()
    phos_nloss = '-H3PO4 -97.97690'
    for ptm in ptms:
        luciptm = get_luci_mod(ptm['pos'], ptm['aa'], ptm['masschange'])
        if luciptm not in target_mods:
            target_mods.append(luciptm)
            decoy_mods.add(ptm['masschange'])
        msgf_modmass = get_msgf_seq_mass(ptm['masschange'])
        massconversion_msgf[msgf_modmass] = ptm['masschange']
        ptms_mass.add(msgf_modmass)
        # Neutral loss only for phospho (and possibly glycosylation), add more if we need
        if ptm['name'] == 'Phospho':
            nlosses.add(f"{ptm['aa']} {phos_nloss}")
            decoy_nloss.add(f'X {phos_nloss}')

    # Create the config file contents
    with open(template) as fp:
        lucitemplate = Template(fp.read())
    lt_render = lucitemplate.substitute(mzml_path=mzml_path, algo=lucialgo, maxcharge=maxcharge,
            maxpeplen=maxlen, minpsms=minpsms, outfile='luciphor.out', 
            ms2tol=ms2tol,
            ms2toltype=ms2toltype,
            dmasses=decoy_mods,
            neutralloss=nlosses,
            decoy_nloss=decoy_nloss,
            thread=threads
            )
    for tmod in lucifixed:
        lt_render = f'{lt_render}\nFIXED_MOD = {tmod}'
    for tmod in lucivar:
        lt_render = f'{lt_render}\nVAR_MOD = {tmod}'
    for tmod in target_mods:
        lt_render = f'{lt_render}\nVAR_MOD = {tmod}'
    for tmod in nlosses:
        lt_render = f'{lt_render}\nNL = {tmod}'
    for tmod in decoy_nloss:
        lt_render = f'{lt_render}\nDECOY_NL = {tmod}'
    for tmod in decoy_mods:
        lt_render = f'{lt_render}\nDECOY_MASS = {tmod}'
    yield lt_render

    # TODO
    # How to handle competing mods? I have yet to find a use-case but theoretically
    # a fixed/PTM competition may occur (not Acetyl/TMT since Ac is not labile like Phos)
    # Probably replace double notation (tmt - (tmt - mod)), eg 229-187 in PSM table with 
    # the actual PTM mass (42)? But luciphor ignores PTMs on residues with a fixed mod anyway

    # Create the Lucxor PSM input table
    for psm in psms:
        outpsm = {lucfield[ix]: psm[psmfield] for ix, psmfield in psmfields}
        ptm_in_seq = False
        sites = []
        pep, start = '', 0
        seq = psm[dm.HEADER_PEPTIDE]
        # TODO below mod notation is MSGF+ dependent, may need changing
        for mod in re.finditer('[\+\-0-9]+.[\+\-.0-9]+', seq):
            modtxt = mod.group()
            if modtxt.count('+') + modtxt.count('-') > 1:
                # multi mod on single residue
                multimods = re.findall('[\+\-][0-9.]+', modtxt)
            else:
                multimods = [modtxt]
            modmass = sum([massconversion_msgf[x] for x in multimods])
            if set(multimods).intersection(ptms_mass):
                ptm_in_seq = True
                # IF fixed + target -> use the target mass from the msgfmods file
                # target + target -> 
            pep += seq[start:mod.start()]
            if not set(multimods).intersection([*ptms_mass, *varmods_mass]):
                # Do not annotate fixed mods
                start = mod.end()
                continue
            if len(pep) == 0:
                aamass = modmass
            else:
                aamass = round(dm.AA_WEIGHTS_MONO[pep[-1]] + modmass, 5)
            sites.append([len(pep)- 1, aamass])
            start = mod.end()
        if not ptm_in_seq:
            # only output PSMs with PTM for luciphor
            continue
        if start != mod.endpos:
            pep += seq[start:]
        if sites[0][0] == -1: sites[0][0] = -100
        # TODO add C-terminal mods (rare)?
        outpsm.update({
            'peptide': pep,
            'modSites': ','.join(['{}={}'.format(x[0], x[1]) for x in sites])})
        yield outpsm


def parse_luciphor_output(luciptms, luciscores, outpsms, tdb, minscore_high, ptmmods):
    modresidues, ptmmasses = {}, {}
    for mod in ptmmods:
        modresidues[mod['name']] = []
        # FIXME mass is not float?
        totalmass = mod['mass'] if mod['aa'] == '*' else dm.AA_WEIGHTS_MONO[mod['aa']] + mod['mass']
        ptmmasses[round(totalmass, 0)] = modname
        
    # Now go through scores, luciphor and PSM table
#    with open('all_scores.debug') as scorefp, open('luciphor.out') as fp, open('psms') as psms, open(outfile, 'w') as wfp:
#        outheader = psmheader + PTMFIELDS

    scorepep = {'specId': False}
    lucptms = {}
    for lucptm in luciptms:
        out = {}
        specid = lucptm['specId']
        ptm = {
            TOPFLR: lucptm['globalFLR'],
            TOPSCORE: lucptm['pep1score'],
            OTHERPTMS: 'NA',
            }
        # match the modified residues and group:
        barepep, start = '', 0
        modpep = lucptm['predictedPep1']
        for x in re.finditer('([A-Z]){0,1}\[([0-9]+)\]', modpep):
            if x.group(1) is not None: # check if residue (or protein N-term)
                barepep += modpep[start:x.start()+1]
            else:
                barepep += modpep[start:x.start()]
            start = x.end()
            modresidues[ptmmasses[int(x.group(2))]].append((x.group(1), len(barepep)))

        # modresidues = { ptmname: [('S', 13), ('S', 22), ...], ...}
        barepep += modpep[start:]
        ptm.update({'barepep': barepep, 'modres': modresidues})
        ptm[TOPPTM] = ';'.join(['{}:{}'.format(name, ','.join(['{}{}'.format(x[0], x[1]) for x in resmods])) for 
                name, resmods in modresidues.items() if len(resmods)])

        # Get other highscoring permutations from all_scores file
        extrapeps = []
        if scorepep['specId'] == specid:
            lucptm['likeScoredPep'] = re.sub(r'([A-Z])\[[0-9]+\]', lambda x: x.group(1).lower(), lucptm['predictedPep1'])
            if scorepep['curPermutation'] != lucptm['likeScoredPep'] and float(scorepep['score']) > minscore_high:
                extrapeps.append('{}:{}'.format(','.join(['{}{}'.format(x.group().upper(), x.start() + 1)
                            for x in re.finditer('[a-z]', scorepep['curPermutation'])]),
                            scorepep['score']))
        for scorepep in luciscores:
            if int(scorepep['isDecoy']):
                continue
            if scorepep['specId'] != specid:
                break
            lucptm['likeScoredPep'] = re.sub(r'([A-Z])\[[0-9]+\]', lambda x: x.group(1).lower(), lucptm['predictedPep1'])
            if scorepep['curPermutation'] != lucptm['likeScoredPep'] and float(scorepep['score']) > minscore_high:
                extrapeps.append('{}:{}'.format(','.join(['{}{}'.format(x.group().upper(), x.start() + 1)
                        for x in re.finditer('[a-z]', scorepep['curPermutation'])]),
                        scorepep['score']))
            if len(extrapeps):
                ptm[OTHERPTMS] = ';'.join(extrapeps)
        lucptms[specid] = ptm

    # Now output to its PSM table
    for psm in outpsms:
        spfile = os.path.splitext(psm[dm.HEADER_SPECFILE])[0]
        luc_psmid = f'{spfile}.{psm[dm.HEADER_SCANNR]}.{psm[dm.HEADER_SCANNR]}.{dm.HEADER_CHARGE}'
        if luc_psmid in lucptms:
            ptm = lucptms[luc_psmid]
            # Get protein site location of mod
            if dm.HEADER_MASTER_PROT in psm:
                proteins = psm[dm.HEADER_MASTER_PROT].split(';')
                proteins = {p: tdb[p].seq.find(ptm['barepep']) for p in proteins}
                proteins_loc = {p: [] for p, peploc in proteins.items() if peploc > -1}
                for p, peploc in proteins.items():
                    for ptmname, ptmlocs in ptm['modres'].items():
                        if ptmname not in ptms:
                            continue
                        protptms = []
                        for res_loc in ptmlocs:
                            protptms.append('{}{}'.format(res_loc[0], res_loc[1] + peploc))
                            proteins_loc[p].append('{}_{}'.format(ptmname, ','.join(protptms)))
                psm[dm.HEADER_MASTER_PROT] = ';'.join(['{}:{}'.format(p, ':'.join(ptmloc)) for p, ptmloc in proteins_loc.items()])
            outpsm = {k: v for k,v in psm.items()}
            outpsm.update(ptm)
            outpsm[SE_PEPTIDE] = outpsm.pop(PEPTIDE)
            outpsm[PEPTIDE] = '{}_{}'.format(ptm['barepep'], ptm[TOPPTM])
            yield outpsm
