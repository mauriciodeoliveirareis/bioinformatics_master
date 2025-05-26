# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 18:54:30 2025

@author: Eva
"""


############################### CLEAN EVERYTHING #############################
for i in list(globals().keys()):
    if not i.startswith('_'):
        exec('del ' + i)
##############################################################################
#################################### IMPORTS #################################
import os
from pathlib import Path
import pandas as pd
##############################################################################

################################ INITIAL VARIABLES ###########################
parent = Path(__file__).resolve().parent
os.chdir(parent)
print(f'Working on: \n {os.getcwd()}')
##############################################################################

################################### FUNCTIONS ################################

def translate(start):
    
    initial_protein = ''
    
    for nt in range(start,len(CDS_sequence_upper),3):
        codon = CDS_sequence_upper[nt:nt+3]
        if len(codon) == 3:
            
            aa = codon_table_dict['Abbreviation (1 Letter)'][codon]
            initial_protein = initial_protein + aa
        else:
            continue
    
    return initial_protein

##############################################################################

# two ways to use system separators:

codon_table = pd.read_excel('..' + os.path.sep + 'Codon_aa_table.xlsx')

# codon_table2 = pd.read_excel(os.path.join('..','..','RECURSOS','Codon_aa_table.xlsx'))

codon_table_dict = codon_table.set_index('Codon').to_dict('dict')

# Read only fasta contents into CSD_sequence without headers
CDS_sequence = ''
with open('./ccdn2.fasta', 'r') as file:
    for line in file:
        if not line.startswith('>'):  # Skip header lines
            CDS_sequence += line.strip()  # Remove whitespace and concatenate

# Uncomment the next line to not read read from a file 
# CDS_sequence = 'ATGGAGCTGCTGTGCCACGAGGTGGACCCGGTCCGCAGGGCCGTGCGGGACCGCAACCTGCTCCGAGACGACCGCGTCCTGCAGAACCTGCTCACCATCGAGGAGCGCTACCTTCCGCAGTGCTCCTACTTCAAGTGCGTGCAGAAGGACATCCAACCCTACATGCGCAGAATGGTGGCCACCTGGATGCTGGAGGTCTGTGAGGAACAGAAGTGCGAAGAAGAGGTCTTCCCTCTGGCCATGAATTACCTGGACCGTTTCTTGGCTGGGGTCCCGACTCCGAAGTCCCATCTGCAACTCCTGGGTGCTGTCTGCATGTTCCTGGCCTCCAAACTCAAAGAGACCAGCCCGCTGACCGCGGAGAAGCTGTGCATTTACACCGACAACTCCATCAAGCCTCAGGAGCTGCTGGAGTGGGAACTGGTGGTGCTGGGGAAGTTGAAGTGGAACCTGGCAGCTGTCACTCCTCATGACTTCATTGAGCACATCTTGCGCAAGCTGCCCCAGCAGCGGGAGAAGCTGTCTCTGATCCGCAAGCATGCTCAGACCTTCATTGCTCTGTGTGCCACCGACTTTAAGTTTGCCATGTACCCACCGTCGATGATCGCAACTGGAAGTGTGGGAGCAGCCATCTGTGGGCTCCAGCAGGATGAGGAAGTGAGCTCGCTCACTTGTGATGCCCTGACTGAGCTGCTGGCTAAGATCACCAACACAGACGTGGATTGTCTCAAAGCTTGCCAGGAGCAGATTGAGGCGGTGCTCCTCAATAGCCTGCAGCAGTACCGTCAGGACCAACGTGACGGATCCAAGTCGGAGGATGAACTGGACCAAGCCAGCACCCCTACAGACGTGCGGGATATCGACCTGTGA'

CDS_sequence_upper = CDS_sequence.upper()

# translate protein frames 0, 1 and 2, select longest one (that has more amino acids before a stop *)
longest_protein_sequence = ""
for i in range(3):
    protein = translate(i)
    print(f"Protein frame {i+1} (raw): {protein}")
    stop_codon_index = protein.find('*')
    if stop_codon_index != -1:
        current_protein = protein[:stop_codon_index]
    else:
        current_protein = protein
    
    if len(current_protein) > len(longest_protein_sequence):
        longest_protein_sequence = current_protein

print(f'\\nLongest protein sequence before stop codon: {longest_protein_sequence}')
print(f'Length: {len(longest_protein_sequence)} amino acids')
ali = ">P1;CCND2\nsequence:CCND2::::::::\n" + longest_protein_sequence + "*\n"
with open('./create_model/CCND2/CCND2.ali', 'w') as file:
    file.write(ali)