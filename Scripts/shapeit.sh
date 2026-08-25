#!/bin/bash

##### CREDITS ---------------------------------------------------------------------------
#Johanne Adam Doucet
#07/04/2023
#PhD, year 1 
#####------------------------------------------------------------------------------------

##### DESCRIPTION -----------------------------------------------------------------------
#Example of command lines for running shapeit and preparation of strand.exclude files
#####------------------------------------------------------------------------------------

#generate exclude files
shapeit -check --input-vcf /input_file.chrom.recode.vcf -M genetic_map.chrom.txt --input-ref 20230407_1KGP_III.chrom.haps 20230407_1KGP_III.chrom.legend 20230407_1KGP_III.chrom.sample --output-log ARRAY_alignment_chrom

#phasing data
shapeit --input-vcf input_file.chrom.recode.vcf \ -M genetic_map.chrom.txt \ --input-ref 20230407_1KGP_III.chrom.haps 20230407_1KGP_III.chrom.legend 20230407_1KGP_III.chrom.sample \ --exclude-snp alignement.chrom.snp.strand.exclude \ -T 30 \-O 20230407_hg38_QC_annoREF_strandfix.1.phased.vcf 


