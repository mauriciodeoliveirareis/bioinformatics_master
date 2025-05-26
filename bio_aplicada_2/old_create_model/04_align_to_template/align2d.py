from modeller import *

log.verbose()

env = environ()
aln = alignment(env)

mdl = model(env, file='2cr4', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='2cr4', atom_files='2cr4.pdb')
aln.append(file='CCND2.ali', align_codes='CCND2')
aln.align2d()
aln.write(file='CCND2-2cr4.ali', alignment_format='PIR')
aln.write(file='CCND2-2cr4.pap', alignment_format='PAP')
