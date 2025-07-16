
#%%Clean everything
for i in list(globals().keys()):
    if not i.startswith('_'):
        exec('del ' + i)

#%%Imports
import pandas as pd
from rdkit import Chem
import os
from rdkit.Chem import AllChem, SDWriter
import numpy as np
from pathlib import Path

#%%Initial variables
parent = Path(__file__).resolve().parent
os.chdir(parent)
print(f'Working on: \n {os.getcwd()}')

#%% Load the datasets
# path = 'C:/Users/Martina/Documents/Endocrine_disruptors/DockingYazara/Docking_mycotoxins/Seleccion_micotoxinas/'
# os.chdir(path)

file = "ProtoADME_filtered_reduced_50.csv"
df = pd.read_csv (file, sep=';')

#%% Create sdf
# Define the output SDF file
output_sdf_file = f"{file}.sdf"

# Initialize the SDF writer
writer = SDWriter(output_sdf_file)

# Loop through the DataFrame and convert SMILES to RDKit molecules
for index, row in df.iterrows():
    smiles = row['SMILES']
    
    # Convert SMILES to an RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    
    if mol:
        # Add explicit hydrogens
        mol = Chem.AddHs(mol)
        
        # Optionally add metadata (e.g., molecule name)
        # mol.SetProp("cid",name)
        mol.SetProp('_Name', row['Name'])  # Set the molecule identifier(important for SDF)

        
        # Add 3D coordinates (optional, for visualization)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        
        # Write the molecule to the SDF file
        writer.write(mol)
    else:
        print(f"Failed to parse SMILES: {smiles}")

# Close the writer
writer.close()

print(f"SDF file with hydrogens saved to: {output_sdf_file}")


# %%

#%% One smile

# Define the output SDF file
output_sdf_file = "Saquinarvir.sdf"

# Initialize the SDF writer
writer = SDWriter(output_sdf_file)

# Loop through the DataFrame and convert SMILES to RDKit molecules

smiles =  "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1C[C@H]([C@H](CC3=CC=CC=C3)NC(=O)[C@H](CC(=O)N)NC(=O)C4=NC5=CC=CC=C5C=C4)O"
name = "Saquinarvir"  # Use 'Name' if present, otherwise create a default name

# Convert SMILES to an RDKit molecule
mol = Chem.MolFromSmiles(smiles)

# Add explicit hydrogens
mol = Chem.AddHs(mol)

# Optionally add metadata (e.g., molecule name)
# mol.SetProp("cid",name)

# Add 3D coordinates (optional, for visualization)
AllChem.EmbedMolecule(mol, randomSeed=42)

# Write the molecule to the SDF file
writer.write(mol)

# Close the writer
writer.close()

print(f"SDF file with hydrogens saved to: {output_sdf_file}")



#%% Convert dataframe tino subframes