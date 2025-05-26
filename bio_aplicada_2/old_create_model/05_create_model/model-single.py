from modeller import *
from modeller.automodel import *
#from modeller import soap_protein_od

log.verbose()

env = environ()
a = automodel(env, alnfile='CCND2-2cr4.ali',
              knowns='2cr4', sequence='CCND2',
              assess_methods=(assess.DOPE,
                              #soap_protein_od.Scorer(),
                              assess.GA341))
a.starting_model = 1
a.ending_model = 5

a.make()
