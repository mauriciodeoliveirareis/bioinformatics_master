#Clean everything
for i in list(globals().keys()):
    if not i.startswith('_'):
        exec('del ' + i)

#Imports
import pandas as pd
from rdkit import Chem
import os
from rdkit.Chem import AllChem, SDWriter
import numpy as np
from pathlib import Path
#Initial variables
parent = Path(__file__).resolve().parent
os.chdir(parent)
print(f'Working on: \n {os.getcwd()}')

df = pd.read_excel("./protoadme_data_base_screening_out.xlsx", sheet_name="Summary")

filtered_df = df[
    (df["Druglikeness score"].isin(["7/8", "8/8"])) &
    (df["Bioavailability30"] == "Positive") &
    (df["Caco-2 permeability: cm/s"] > -6) &
    (df["Blood-brain barrier"].str.lower() == "bbb-") &
    (df["Plasma-protein binding: %"] < 0.7)
]
print(f"Filtered {len(df)} rows to {len(filtered_df)} rows based on the criteria. It wil be saved on ./filtered_screening_protoadme.csv")
filtered_df.to_csv("filtered_screening_protoadme.csv", index=False, sep=';')

