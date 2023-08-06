DECOY_PREFIX = 'decoy_'

HEADER_SPECFILE = '#SpecFile'
HEADER_SCANNR = 'ScanNum'
HEADER_SPECSCANID = 'SpecID'
HEADER_CHARGE = 'Charge'
HEADER_PEPTIDE = 'Peptide'
HEADER_PROTEIN = 'Protein'
HEADER_GENE = 'Gene ID'
HEADER_SYMBOL = 'Gene Name'
HEADER_DESCRIPTION = 'Description'
HEADER_PRECURSOR_MZ = 'Precursor'
HEADER_PRECURSOR_QUANT = 'MS1 area'
HEADER_PREC_PURITY = 'Precursor ion fraction'
HEADER_PRECURSOR_FWHM = 'FWHM'
HEADER_MASTER_PROT = 'Master protein(s)'
HEADER_PG_CONTENT = 'Protein group(s) content'
HEADER_PG_AMOUNT_PROTEIN_HITS = 'Amount of matching proteins in group(s)'
HEADER_PG = [HEADER_MASTER_PROT, HEADER_PG_CONTENT,
             HEADER_PG_AMOUNT_PROTEIN_HITS]
HEADER_SVMSCORE = 'percolator svm-score'
HEADER_MISSED_CLEAVAGE = 'missed_cleavage'
HEADER_PSMQ = 'PSM q-value'
HEADER_PSM_PEP = 'PSM PEP'
HEADER_PEPTIDE_Q = 'peptide q-value'
HEADER_PEPTIDE_PEP = 'peptide PEP'
HEADER_TARGETDECOY = 'TD'
HEADER_MSGFSCORE = 'MSGFScore'
HEADER_EVALUE = 'EValue'
HEADER_SETNAME = 'Biological set'
HEADER_RETENTION_TIME = 'Retention time(min)'
HEADER_INJECTION_TIME = 'Ion injection time(ms)'
HEADER_ION_MOB = 'Ion mobility(Vs/cm2)'
MOREDATA_HEADER = [HEADER_RETENTION_TIME, HEADER_INJECTION_TIME, HEADER_ION_MOB]
PERCO_HEADER = [HEADER_SVMSCORE, HEADER_PSMQ, HEADER_PSM_PEP, HEADER_PEPTIDE_PEP, HEADER_PEPTIDE_Q, HEADER_TARGETDECOY]

AA_WEIGHTS_MONO = { # From ExPASY
        'A': 71.03711,
        'R': 156.10111,
        'N': 114.04293,
        'D': 115.02694,
        'C': 103.00919,
        'E': 129.04259,
        'Q': 128.05858,
        'G': 57.02146,
        'H': 137.05891,
        'I': 113.08406,
        'L': 113.08406,
        'K': 128.09496,
        'M': 131.04049,
        'F': 147.06841,
        'P': 97.05276,
        'S': 87.03203,
        'T': 101.04768,
        'W': 186.07931,
        'Y': 163.06333,
        'V': 99.06841,
        'U': 150.953636,
        'O': 237.147727,
        }

NON_BLOCKING_MODS = {
        'GG': ['TMTpro', 'TMT6plex', 'iTRAQ8plex', 'iTRAQ4plex'],
        }
