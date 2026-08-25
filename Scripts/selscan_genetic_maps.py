import pandas as pd

def formatNumber(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

pops = ['AKI', 'AKZ', 'HKS', 'KAZ', 'KIB', 'SHO', 'TAB', 'TUB', 'TUR', 'UZB', 'BOU', 'CST', 'CJO', 'CSA', 'CKC', 'CTA', 'CPN', 'CMR', 'CBR', 'CRE', 'LKM', 'LMT', 'LPO', 'LPR','LTA']

for p in pops:
    for k in range(22, 0, -1):
        # Import genetic map file
        ref_file = pd.read_csv('/path/to/genetic/map/genetic_map_LD_uniq.' + str(k) + '.txt',
                               sep=' ', names=["physical", "CM/MB", "genetic"])
        # Create a dictionary with physical position as key and genetic position as value
        pos_dict = dict(zip(ref_file["physical"], ref_file["genetic"]))
        recomb_dict = dict(zip(ref_file["physical"], ref_file["CM/MB"]))

        prevLine = None  # Initialize prevLine

        # Open input and output files
        file_in = open('/path/to/input/file' + str(p) + '/' + str(p) + '.' + str(k) + '.map', 'r')
        file_out = open('/path/to/output/file' + str(p) + '/' + str(p) + '_genetic_pos.' + str(k) + '.map', 'w')

        found = 0
        calculated = 0
        not_found = 0
        for line in file_in:
            l = line.split()
            if int(l[3]) in pos_dict:
                l[2] = pos_dict[int(l[3])]
                l[2] = str(l[2])
                print('\t'.join(l), file=file_out)
                found += 1
                # storing prev_line if it exists in dictionary
                prevLine = l
            elif prevLine and float(prevLine[3]) in recomb_dict:
                l[2] = float(prevLine[2]) + ((float(prevLine[3]) - float(l[3])) / 100000) * recomb_dict[
                    formatNumber(float(prevLine[3]))]
                l[2] = str(l[2])
                print('\t'.join(l), file=file_out)
                calculated += 1
            else:
                print('\t'.join(l), file=file_out)
                not_found += 1
        file_in.close()
        file_out.close()
        print(k, found, calculated, not_found)
