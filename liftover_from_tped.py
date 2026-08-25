###LiftOver from tped file

###Johanne Adam 
###20221129
####PhD, year 1


####import dependancies 
import pandas as pd 

#import liftover file with the new positions 
pos_df = pd.read_csv('path/to/new/build/positions.bed',sep='\t', names=["Chromosome", "Start", "End", "rsID"])
#creating dictionnary 
pos_dict = dict(zip(pos_df.iloc[:,3], pos_df.iloc[:,2]))

#create variables in the loop 
replaced_pos_loop=0
deleted_pos_loop=0
replaced_pos_tot = 0
deleted_pos_tot = 0

#names and directories of files to open
file_begin_in = 'path/to/input/file'
file_end_in = '_ARRAY.tped'
file_begin_out = '/path/to/output/file'
file_end_out = '_ARRAY.tped'

#looping through all of the chromosomes 
for j in range(17,16,-1):
    print(j)
    #change filename according to chromosome number
    filename_in = file_begin_in + str(j) + file_end_in
    filename_out = file_begin_out + str(j) + file_end_out
    #open file with chromosome j 
    ARRAY_in = pd.read_csv(filename_in,  sep=' ', low_memory=False, header=None)
    #create empty dataframe to store the new positions 
    ARRAY_out=pd.DataFrame()
    #create a loop for replacing the old position with new position
    for i in range(0, len(ARRAY_in)):
        if ARRAY_in.iloc[i, 1] in pos_dict:
            ARRAY_in.iloc[i, 3] = pos_dict[ARRAY_in.iloc[i, 1]]
            ARRAY_out=ARRAY_out.append(ARRAY_in.iloc[i,], ignore_index=True)
            replaced_pos_loop += 1
        else:
            deleted_pos_loop += 1
            continue 
    deleted_pos_tot = deleted_pos_tot + deleted_pos_loop
    replaced_pos_tot = replaced_pos_tot + deleted_pos_loop
    ARRAY_out.to_csv(filename_out, sep=' ', header=False)

print(deleted_pos_tot)
print(replaced_pos_tot)
