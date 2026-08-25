#!/bin/bash

##### CREDITS ---------------------------------------------------------------------------
#Johanne Adam Doucet
#08/11/2023
#PhD, year 1 
#####------------------------------------------------------------------------------------

##### DESCRIPTION -----------------------------------------------------------------------
#This script prepares contains examples of selscan runs and normalization.
#Note: data has to be stored into folders with the population name on it. Selscans maps 
#used in the script have been generated using selscan_genetic_maps.
#####------------------------------------------------------------------------------------

#run selscan
path/to/selscan --vcf /path/to/input/pop/file.$pop.$chrom.vcf --map /path/to/map.$chrom.map --out /path/to/output/folder/name_ihs.$pop.$chrom


# Combine the contents of prefix_all.txt and number_ind.txt side by side
#prefix contains all pop prefix, number_ind contains the size of normalization bin
paste "/path/to/prefix_all.txt" "/path/to/bin/size/number_ind.txt" | while read -r pop num_bins
do
    # Check if num_bins has a value
    if [ -n "$num_bins" ]; then
        # Run selscan norm
        /path/to/selscan/norm --ihs --files ${pop_dir}${pop}/input_file.${pop}.*.ihs.out --bins "$num_bins" --log ${pop_dir}${pop}/output_file.${pop}.log
        echo "Found $num_bins bins for $pop"
    else
        echo "Error: Number of bins not found for population $pop in number_ind.txt"
    fi
done

