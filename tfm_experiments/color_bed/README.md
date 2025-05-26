# Experiment in generating a .color.bed
- color_bed.py was coped from: https://github.com/alexpan00/SQANTI_colors/  

- ./data was taken sample files were taken from https://github.com/ConesaLab/SQANTI3/tree/master/example/SQANTI3_QC_output  

- Steps are run on run_all.sh

- TODO convert bed to big bed https://genome.ucsc.edu/goldenpath/help/bigBed.html

# Big bed files
- Put in a separate data folder a copy of bed file and the genome assembly
- I assumed that the bed file is genome assembly hg38 (saw on https://github.com/ConesaLab/SQANTI3/blob/master/example/SQANTI3_QC_output/UHR_chr22.qc_params.txt)
- Invoked to create a big bed file `/Users/mauriciodeoliveirareis/code/gen_browser/macOSX.arm64/bedToBigBed ./data_bb/UHR_chr22_corrected.bed ./data_bb/hg38.chrom.sizes ./data_bb/UHR_chr22_corrected.bb`

# Next steps
1. Idenfity what should I change (possibly not the big bed file as it's alreay bynary), change the bedToBigBed script to colour it or accept a coloured big bed? Clone bedToBigBed script?
2. 
