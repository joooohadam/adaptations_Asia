####REFANC pipeline 

#### Johanne ADAM 
#### 03/02/2023
#### PhD 1

#### IMPORT DEPENDANCIES ----------------------------------------------------------------
import pandas as pd 
import numpy as np 
####-------------------------------------------------------------------------------------

####BASES FONCTION IMPLEMENTATION -------------------------------------------------------
#function to handle the 'AA=x" in the column info 
infocol_dict={"AA=a":"A", "AA=c":"C", "AA=g":"G", "AA=t":"T", "AA=A":"A", "AA=C":"C", "AA=G":"G", "AA=T":"T"}
def dealwithinfo(info_base):
    if info_base in infocol_dict:
        return(infocol_dict[info_base])

#function to return associated base 
bases_dict = {"A":"T", "T":"A", "C":"G", "G":"C"}
def invbase(base_name):
    if base_name in bases_dict:
        return(bases_dict[base_name])

#function to swap genotypes when ALT or REF = inv ANC
geno_to_swap = {"0|0":"1/1", "0|1" : "1/0", "1|0":"0/1", "1|1": "0/0"}
def swap_geno(geno_in):
    if geno_in in geno_to_swap:
        return(geno_to_swap[geno_in])
#change / to | if working with already phased data

#function to change | to / when ALT or REF = ANC 
geno_to_fix = {'0|0' : '0/0', '0|1':'0/1', '1|0':'1/0', '1|1':'1/1'}
def fix_geno(geno_in):
    if geno_in in geno_to_fix:
        return(geno_to_fix[geno_in])
#data used in the paper had been phased previously. I undid the phase because I redid it
#later on in the pipeline. Remove it if not needed

####-------------------------------------------------------------------------------------


#### VARIABLES---------------------------------------------------------------------------
#file infos not changing per chromosome
LOCATION_in = '/path/to/input/directory/'
LOCATION_out='/path/to/output/directory/'
ARRAY = '_ARRAY'
DATE_in = 'date'
DATE_out = 'date'
END_in = '_file_suffix.'
END_out = '_file_suffix_oriented.'
FORMAT_in = '.vcf.gz'
FORMAT_out='.vcf'
FILENAME_metrics = LOCATION_out+DATE_out+ARRAY+'metrics_all.csv'
HEADER_metrics = ("chr", "skipped A/T C/G", "not skipped", "no ANC info", "ANC info", "REF=ANC", "REF=invANC", "ALT=ANC", "ALT=invANC", "overflow")

#looping through the chromosomes from 22 to 1
for j in range(22,0,-1):
    print ("Chromosome treated :", str(j))
    #filenames changing per chromosomes 
    FILENAME_in = LOCATION_in + DATE_in + ARRAY + END_in + str(j) + FORMAT_in
    FILENAME_out = LOCATION_out + DATE_out + ARRAY + END_out + str(j) + FORMAT_out
    #####------------------------------------------------------------------------------------

    ####COMPTEURS---------------------------------------------------------------------------
    #metrics resetting at each chromosome loop
    skippedATCG=0 
    not_skipped=0
    no_anc_info=0 
    anc_info=0
    ref_equal_anc=0 
    ref_equal_inv_anc=0 
    alt_equal_anc=0
    alt_equal_inv_anc=0
    not_treated=0 
    compteur=0
    #i counts the lines of the file 
    #k counts the columns of the file 
    #j counts the chromosomes 
    ####-------------------------------------------------------------------------------------

    ##### IMPORT FILES ----------------------------------------------------------------------
    ARRAY_in = pd.read_csv(FILENAME_in, sep='\t', skiprows=74, low_memory=False, header=None)
    ARRAY_out=pd.DataFrame()
    metrics_out=pd.DataFrame()
    #looping through the lines of the file 
    for i in range(0,len(ARRAY_in)):
        compteur += 1 
        #CONDITION 1 : if the polymorphism is A/T or C/G -> do not copy the line to the file and continue 
        if ((l[3] in bases_dict) and (l[4] == invbase(l[3]))):
            skippedATCG+=1
            continue
        #CONDITION 2 : the polymorphism is not A/T or C/G 
        else:
            not_skipped +=1
            #CONDITION 3 : the INFO field does not contain ancestral allele information (AA=N, AA=. or AA=-)
            if (l[7] not in infocol_dict):
                #ARRAY_out=ARRAY_out.append(l[], ignore_index=True)
                no_anc_info += 1
            #CONDITION 4 : the INFO field does contain ancestral allele information 
            else:
                anc_info +=1
                #CONDITION 5 : if REF = ANC -> do not swap 
                if (l[3] == dealwithinfo(l[7])):
                    for k in range(9, len(ARRAY_in.columns)):
                        l[k]=fix_geno(l[k])
                    ARRAY_out = ARRAY_out.append(l[], ignore_index=True)
                    ref_equal_anc += 1
                #CONDITION 6 : if REF = invANC -> do not swap 
                elif (l[3] == invbase(dealwithinfo(l[7]))):
                    for k in range(9, len(ARRAY_in.columns)):
                        l[k]=fix_geno(l[k])
                    ARRAY_out=ARRAY_out.append(l[], ignore_index=True)
                    ref_equal_inv_anc += 1 
                #CONDITION 7 : if ALT = ANC -> swap genotypes 
                elif ((l[4]) == dealwithinfo(l[7])):
                    ARRAY_in.iloc[1,3], ARRAY_in.iloc[1,4] = ARRAY_in.iloc[1,4], ARRAY_in.iloc[1,3]
                    for k in range(9, len(ARRAY_in.columns)):
                        l[k]=swap_geno(l[k])
                    ARRAY_out=ARRAY_out.append(l[], ignore_index = True)
                    alt_equal_anc +=1
                #CONDITION 8 : if ALT = invANC -> swap genotypes 
                elif ((l[4]) == invbase(dealwithinfo(l[7]))):
                    ARRAY_in.iloc[1,3], ARRAY_in.iloc[1,4] = ARRAY_in.iloc[1,4], ARRAY_in.iloc[1,3]
                    for k in range(9, len(ARRAY_in.columns)):
                        l[k]=swap_geno(l[k])
                    ARRAY_out=ARRAY_out.append(l[], ignore_index = True)
                    alt_equal_inv_anc +=1
                #CONDITION 9 : if none of the previous conditions filled, do not copy.  
                else:
                    not_treated +=1
    #checking all the lines from ARRAY_in were treated 
    if(skippedATCG+no_anc_info+ref_equal_anc+ref_equal_inv_anc+alt_equal_anc+alt_equal_inv_anc+not_treated == compteur):
        print("All lines treated")
    else:
        print('Something went wrong')
    #checking CONDITIONS 5,6,7 and 8 were copied to new file ARRAY_out 
    if(ref_equal_anc+ref_equal_inv_anc+alt_equal_anc+alt_equal_inv_anc == len(ARRAY_out)):
        print("ARRAY_out complete with the right number of lines")
    else:
        print("some lines were not transfered on ARRAY_out")
    #checking the non-treated lines correspond to CONDITIONS 1,3 and 9
    if(skippedATCG+no_anc_info+not_treated==(len(ARRAY_in)-len(ARRAY_out))):
        print("the lines discared correspond to A/T C/G and lines with no ANC info")
    else:
        print('something went wrong')
    #exporting the file 
    print('exporting file for chromosome'+str(j))
    ARRAY_out.to_csv(FILENAME_out, sep = '\t', header = None, index = False, float_format='%.0f')
    print("chromosome " + str(j))
    print(skippedATCG, no_anc_info, anc_info, ref_equal_anc, ref_equal_inv_anc, alt_equal_anc, alt_equal_inv_anc, not_treated)
