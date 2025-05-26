# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 06:57:16 2025

@author: Eva + Lauri
"""



############################### CLEAN EVERYTHING #############################
for i in list(globals().keys()):
    if not i.startswith('_'):
        exec('del ' + i)
##############################################################################
#################################### IMPORTS #################################
import os
from pathlib import Path
import MDAnalysis as mda
import prolif as plf
import pandas as pd

import matplotlib.pyplot as plt


##############################################################################

################################ INITIAL VARIABLES ###########################
parent = Path(__file__).resolve().parent
os.chdir(parent)
print(f'Working on: \n {os.getcwd()}')

##############################################################################
#%%
def translate_df(df):
    df_trans = df.T
    
    df_trans_reseteado = df_trans.reset_index()
    
    noninter = df_trans_reseteado.query('ligand != protein') 
    
    new_col_ordered = []

    for idx, row in noninter.iterrows():
        
        residues = [row['ligand'], row['protein']]
        
        residues.sort()
        
        residues.append(row['interaction'])
        
        new_col_ordered.append(('-').join(residues))
        
    
    noninter['ordered_residues'] = new_col_ordered
    
    noninter_unique = noninter.drop_duplicates(subset = ['ordered_residues'])
    
    return noninter_unique


#%%

if __name__ == '__main__': # it is essential if all the script is executed

    

    path_input_pdbs = './input'
    
    path_results = 'results2' 

    pdb = 'CCND2.B99990002_ChimeraHs.pdb'
    
    print(f'[+] Analysing interactions for file {pdb}')
    u = mda.Universe(path_input_pdbs + os.path.sep +pdb, guess_bonds=False,  vdwradii={"H": 1.05, "O": 1.48})
    
    
#%%
    # prot = u.atoms.select_atoms("protein and not resid 255")B99990002_
    prot = u.atoms.select_atoms("protein and not resid 255")

    #B99990003
    # prot = u.atoms.select_atoms("protein and not resid 8 and not resid 166") #B99990003
    # prot = u.atoms.select_atoms("protein and not resid 8 and not resid 2755") #B99990003
    
    print(f'\t\t A total of {len(prot)} atoms has been selected')
#%%
    fp = plf.Fingerprint()
    
    fp.run(u.trajectory[::10], prot, prot, progress=True)
 
   
    df = fp.to_dataframe()
    print(df)

    outputfilename = pdb[:-4]
    df.to_csv(path_results + os.path.sep + f'{outputfilename}_interactions.csv', sep = ';')
    print(f"\t[++] Saved table: {outputfilename}_interactions.csv")
    
    reordered_df = translate_df(df)
    reordered_df.to_csv(path_results + os.path.sep + f'{outputfilename}_ordered_interactions.csv', sep = ';')
    print(f"\t[++] Saved table: {outputfilename}_ordered_interactions.csv")
    
    types_interaction = set(reordered_df['interaction'])

    for interaction_type in types_interaction:
        df_interaction_specific = reordered_df[reordered_df['interaction'] == interaction_type]
        output_csv_name = f'{outputfilename}_ordered_interactions_{interaction_type}.csv'
        df_interaction_specific.to_csv(path_results + os.path.sep + output_csv_name, sep = ';')
        print(f"\t[++] Saved table: {output_csv_name}")
  
    dict_interactions = dict()
    
    for type_int in types_interaction:
        
        dict_interactions[type_int] = reordered_df[reordered_df['interaction'] == type_int].shape[0]
        
        
    df_interactions = pd.DataFrame.from_dict(dict_interactions, orient='index')
    
    df_interactions.reset_index(inplace = True)
    
    df_interactions.columns = ['Type', 'Count']
    
    
    
    plt.bar(df_interactions['Type'], df_interactions['Count'])
    plt.title(f'Interactions {outputfilename}')
    plt.xlabel('Types')
    plt.ylabel('count')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()

    out_file = f"{outputfilename}_interactions.png"
    plt.savefig(path_results + os.path.sep + out_file)

    print(f"\t[++] Saved plot: {outputfilename}_interactions.png")

    output_csv_name = f'{outputfilename}_df_iteractions_summary.csv'
    df_interactions.to_csv(path_results + os.path.sep + output_csv_name, sep = ';')
    print(f"\t[++] Saved summary table: {output_csv_name}")


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
