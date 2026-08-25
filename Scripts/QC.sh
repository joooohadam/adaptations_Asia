#!/bin/bash
##### CREDITS ---------------------------------------------------------------------------
#Johanne Adam Doucet
#25/03/2023
#PhD, year 1 
#####------------------------------------------------------------------------------------

##### DESCRIPTION -----------------------------------------------------------------------
#Written to apply Quality controls checks to .vcf files.
#####------------------------------------------------------------------------------------

#####LOADING DIRECTORY-------------------------------------------------------------------
cd /path/to/working/directory/
#####------------------------------------------------------------------------------------

##### LOOPING THROUGH SAMPLES -----------------------------------------------------------
for i in {1..22}
do
 echo "Processing $i"

### NO POSITION -------------------------------------------------------------------------
 echo "Chromosome $i :Removing no positions $i"
 awk -F'\t' '{if($1 ~ /^#/ || $2 != ".") print}' input_file.$i.vcf > step1_$i.vcf
 grep -v '#' step1_$i.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------

### INDELS ------------------------------------------------------------------------------
 echo "Chromosome $i :Removing indels $i"
 vcftools --vcf step1_$i.vcf --remove-indels --recode --out step2_$i
 grep -v '#' step2_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------

### CALL RATE ---------------------------------------------------------------------------
 echo "Chromosome $i :Removing call rate <90% $i"
 vcftools --vcf step2_$i.recode.vcf --max-missing 0.9 --recode --out step3_$i
 grep -v '#' step3_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------

### DUPLICATES --------------------------------------------------------------------------
 echo "Chromosome $i :Removing duplicates rsid and positions $i"
 #Generate file with chr:position rsid
 grep -v '#' step3_$i.recode.vcf | awk '{print $1 ":" $2 "\t" $3}' > positions_$i.txt
 #Identify duplicate rsid 
 awk '{print $2}' positions_$i.txt | uniq -d > rsid_dupli_$i.txt
 #create file with duplicate positions (rsid)
 cat rsid_dupli_$i.txt | while read rsid
 do
  grep "$rsid" positions_$i.txt | awk '{print $1}' >> pos_dup_$i.dup
 done
 #add duplicate positions 
 awk '{print $1}' positions_$i.txt | uniq -d >> pos_dup_$i.dup
 vcftools --vcf step3_$i.recode.vcf --exclude-positions  pos_dup_$i.dup --recode --out step4_$i
 grep -v '#' step4_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------

### MONOMORPHIC SNPs---------------------------------------------------------------------
 echo "Chromosome $i :Removing monomorphic SNPs $i"
 vcftools --vcf step4_$i.recode.vcf --min-alleles 2 --max-alleles 2 --maf 0.0001 --recode --out step5_$i
 grep -v '#' step5_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------
 
#### HWE EQUI ---------------------------------------------------------------------------
 echo "Chromosome $i :Removing SNPs at HWE $i" 
 vcftools --vcf step5_$i.recode.vcf --hwe 0.00001 --recode --out step6_$i
 grep -v '#' step6_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------

### MINOR ALLELE FREQUENCIES ------------------------------------------------------------
 echo "Chromosome $i : Removing SNPs with MAF < 5%" 
 vcftools --vcf step6_$i.recode.vcf --maf 0.05 --recode --out final_output_$i
 grep -v '#' final_output_$i.recode.vcf | wc -l >> recap.$i.txt
###--------------------------------------------------------------------------------------
done

####CLEANING UP--------------------------------------------------------------------------
#removing log files 
rm *.log 
#combining recap files into one 
for i in {1..22}
do 
 cat recap.$i.txt >> recap_final.txt
done 
#removing individual recaps 
rm recap.*.txt
#removing position files 
rm positions_*.txt
###THE END 

