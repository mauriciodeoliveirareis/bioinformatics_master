from modeller import *

log.verbose()
env = Environ() # <-- ESC
aln = Alignment(env) # <-- ESC



query = 'CCND2' # <-- ESC
with open(f"../{query}/{query}_pdbfiles.txt", 'r') as archivo_in: # <-- ESC
	contenido = archivo_in.read().splitlines()
print(f'[+] Compare alignments for {query} templates')

print(contenido) # <-- ESC

list_tuples = []
for ids in contenido:
    list_idchain = [ids.split(' ')[0] , ids.split(' ')[1]]
    tuple_idchain = tuple(list_idchain)
    list_tuples.append(tuple_idchain)
print(list_tuples)
#
for (pdb, chain) in tuple(list_tuples):
    m = Model(env, file = f'../{query}/{query}_templates/{pdb}', model_segment = ('FIRST:'+chain, 'LAST:'+chain)) # <-- ESC
    aln.append_model(m, atom_files = pdb, align_codes = pdb+chain)

aln.malign()
aln.malign3d(fit=False) # fit=False for TRANSFER_XYZ to work properly
aln.compare_structures()
aln.id_table(matrix_file=f'../{query}/{query}family.mat')
env.dendrogram(matrix_file=f'../{query}/{query}family.mat', cluster_cut=-1.0)
