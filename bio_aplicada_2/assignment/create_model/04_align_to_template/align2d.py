from modeller import *

log.verbose()

env = environ()
aln = alignment(env)

mdl = model(env, file='2w96', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='2w96', atom_files='2w96.pdb')
aln.append(file='CCND2.ali', align_codes='CCND2')
aln.align2d()
aln.write(file='CCND2-2w96.ali', alignment_format='PIR')
aln.write(file='CCND2-2w96.pap', alignment_format='PAP')
