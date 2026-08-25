#!/bin/bash
##### CREDITS ---------------------------------------------------------------------------
#Johanne Adam Doucet
#no date
#PhD, year 1 
#####------------------------------------------------------------------------------------

##### DESCRIPTION -----------------------------------------------------------------------
#This script prepares .vcf files for the REFANC_pipeline.py script. It uses samtools 
#-fill-aa to add reference or ancestral allele information in the INFO column of the 
#file. 
#####------------------------------------------------------------------------------------


ARRAY=name_of_array
DATEin=date_input_file
DATEout=date_output_file
cd /path/to/your/file/$ARRAY/
####LOOP
for i in {1..22}
do 
###BGZIP
 bgzip -c final_output_$i.recode.vcf > $DATEout_$ARRAY_hg38_QC.$i.vcf.gz
###FILL-AA
 conda activate samtools 
 zcat $DATEout_$ARRAY_hg38_QC.$i.vcf.gz | fill-aa -a /path/to/reference/or/ancestral/genome/Homo_sapiens.GRCh38.dna.chromosome.$i.fa.gz > $DATEout_$ARRAY_hg38_QC_annoREF.$i.vcf
done 
