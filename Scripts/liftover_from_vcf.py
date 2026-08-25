###LiftOver from vcf file

###Johanne Adam 
###20230104
####PhD, year 1


####import dependancies 
import pandas as pd 

#import liftover file with the new poisitions 
pos_df = pd.read_csv('/path/to/new/build/positions.bed', sep='\t', names=["Chromosome", "Start", "End", "rsID"])
#create dictionnary 
pos_dict=dict(zip(pos_df.iloc[:,3], pos_df.iloc[:,2]))

#create variables in the loop
replaced_pos_loop=0
deleted_pos_loop=0
replaced_pos_tot = 0
deleted_pos_tot = 0

#name and directories of the files to open 
file_begin_hg37 = '/path/to/input/file'
file_end_hg37 = '_ARRAY.vcf'
file_begin_hg38 = '/path/to/outputput/file'
file_end_hg38 = '_ARRAY_hg38.vcf'

#looping through all of the chromosomes 
for j in range(1, 0,-1):
    print(j)
    #change filename according to chromosome number
    filename_hg37 = file_begin_hg37 + str(j) + file_end_hg37
    filename_hg38 = file_begin_hg38 + str(j) + file_end_hg38
    #open file with chromosome j 
    ARRAY_hg37_per_chrom = pd.read_csv(filename_hg37,  sep='\t',skiprows=72, low_memory=False)
    #create empty dataframe to store the new positions 
    ARRAY_hg38_per_chrom=pd.DataFrame()
    #create a loop for replacing the old position with new position
    for i in range(0, len(ARRAY_hg37_per_chrom)):
        if ARRAY_hg37_per_chrom.iloc[i, 2] in pos_dict:
            ARRAY_hg37_per_chrom.iloc[i, 1] = pos_dict[ARRAY_hg37_per_chrom.iloc[i, 2]]
            ARRAY_hg38_per_chrom=ARRAY_hg38_per_chrom.append(ARRAY_hg37_per_chrom.iloc[i,], ignore_index=True)
            replaced_pos_loop += 1
        else:
            deleted_pos_loop += 1
            continue 
    deleted_pos_tot = deleted_pos_tot + deleted_pos_loop
    replaced_pos_tot = replaced_pos_tot + deleted_pos_loop
    ARRAY_hg38_per_chrom.to_csv(filename_hg38, sep='\t')

print(deleted_pos_tot)
print(replaced_pos_tot)
