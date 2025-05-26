
import re
import urllib.request
import os


query = 'CCND2' # <-- ESC
idthres = 25
evalthres = 0

print(f'[+] Searching templates for {query}')

with open(f"../{query}/{query}_profile.prf", 'r') as archivo_in: # <-- ESC
	contenido = archivo_in.read().splitlines()

pdbs = []

print(f'\t[++] the following templates have been found {query}')

for element in contenido:
	if not element.startswith("#") | element.startswith("    1"):
		columns = re.split('[ ]+', element)
		columns2 = ("\t").join(columns[1:13])
		print(columns2)

		identity = int(columns[11].split('.')[0])

		evalue = float(columns[12])

		if  evalue == evalthres and identity >= idthres:
			pdbs.append(columns[2])

print("\n\t\tColumn 11th shows the percentage of identity and the 12th column the e-value of the alignment")
print(f"\t\tAn identity value above approximately 25% indicates a potential template. A threshold of {idthres} will be used")
print(f"\t\tThe closer the E-value to 0, the better is the alignment. A threshold of {evalthres} will be used")

print('\n[+] Saving identifiers')

if len(pdbs) == 0:
	print('\t[++] No suitable templates have been found')

else:
	pdbfilename = f"../{query}/{query}_pdbfiles.txt"
	with open(f"{pdbfilename}", 'w') as archivo_out:
		for pdb in pdbs:
			pdb_code = pdb[0:-1]
			chain = pdb[-1]
			archivo_out.write(f'{pdb_code} {chain}\n')

	print(f'\t[++] File {pdbfilename} has been created with the following sequences')
	print(f'\t\t {pdbs}')


	print(f'[+] Downloading templates for {query}')

	with open(f"{pdbfilename}", 'r') as archivo_in:
		contenido = archivo_in.read().splitlines()

	outputfolderpdbs = f"../{query}/{query}_templates"

	if not os.path.exists(f'{outputfolderpdbs}'):
		os.makedirs(outputfolderpdbs)

	for element in contenido:
	    pdb_with_chain = element.split(" ")
	    pdb = pdb_with_chain[0]

	    url = "http://files.rcsb.org/download/" + pdb + ".pdb"
	    file = f"{outputfolderpdbs}/" + pdb + ".pdb"
	    urllib.request.urlretrieve(url, file)
	    print("Downloading structure", pdb)

	    with open(file, 'r') as pdb_file:
	        molecule = pdb_file.read().splitlines()
	        print(molecule[1])
