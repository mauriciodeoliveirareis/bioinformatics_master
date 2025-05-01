#!/bin/bash
# convets a gtf file to genepred file
/Users/mauriciodeoliveirareis/code/gen_browser/macOSX.arm64/gtfToGenePred ./data/UHR_chr22_corrected.gtf ./data/UHR_chr22_corrected.genepred -genePredExt -allErrors -ignoreGroupsWithoutExons
# converts a genepred file to bed file
/Users/mauriciodeoliveirareis/code/gen_browser/macOSX.arm64/genePredToBed ./data/UHR_chr22_corrected.genepred ./data/UHR_chr22_corrected.bed
# colors the bed file
python3 color_bed.py