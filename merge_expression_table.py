#!/mnt/grl/software/epd/bin/python
import pandas as pd
import sys, os
import argparse
from runconfig import run_options
from numpy import log2


def merge_exp(dge_path, output_path, condition1_num):
    '''
    dge_path <- directory that contains the DE_genes... and DE_isoforms... result
    output_path <- where to save the results
    '''
    
    
    # create output folder
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    # folder name without the path
    folder_name = os.path.basename(dge_path.rstrip('/'))
    
    # get the names of conditions from the folder name
    condition1, condition2 = folder_name.lstrip("DGE_").split("_vs_")
    for feature in ['genes', 'isoforms']:
        # get the DE result file name in the DGE folder
        dge_file = os.path.join(dge_path, folder_name.replace(\
            "DGE_", "DE_{}_".format(feature)) + ".list")
        
        
        # get the expression file from the header line in the matrix file
        matrix_file = os.path.join(dge_path, "{}.counts.matrix".format(feature))
        f_in = open(matrix_file, 'r')
        header_line = f_in.readline()
        f_in.close()
        
        exp_files = header_line.strip().split()
        exp_files = [e.strip('"') for e in exp_files]
        sampleName = [a.split('/')[-2] for a in exp_files]
        
        exp = {}
        # add expression value
        num_of_samples = 0
        for sn, ef in zip(sampleName, exp_files ):
            t = pd.read_table(ef, index_col=[0])
            if exp == {}:
                # init dataframe with gene_id and transcript_id(s)
                exp['count'] = pd.DataFrame(t.ix[:,0])
                exp['tpm'] = pd.DataFrame(t.ix[:,0])
                exp['fpkm'] = pd.DataFrame(t.ix[:,0])
            # add expression column of each sample
            exp['fpkm'][sn] = t.FPKM
            exp['tpm'][sn] = t.TPM
            exp['count'][sn] = t.expected_count.astype(int)
            
            # add the mean expression of condition 1
            num_of_samples += 1
            if num_of_samples == condition1_num:
                exp['fpkm'][condition1] = exp['fpkm'].ix[:, -condition1_num:].mean(axis = 1)
                exp['tpm'][condition1]   = exp['tpm'].ix[:, -condition1_num:].mean(axis = 1)
                exp['count'][condition1] = exp['count'].ix[:, -condition1_num:].mean(axis = 1)
        # add the mean expression of condition 2
        exp['fpkm'][condition2] = exp['fpkm'].ix[:, -(num_of_samples-condition1_num):].mean(axis = 1)
        exp['tpm'][condition2]   = exp['tpm'].ix[:, -(num_of_samples-condition1_num):].mean(axis = 1)
        exp['count'][condition2] = exp['count'].ix[:, -(num_of_samples-condition1_num):].mean(axis = 1)
                
        # add diexp['tpm'][sn] = tfferential expression
        t = pd.read_table(dge_file, sep="\t", index_col = [0])
        for measure in ['fpkm', 'tpm', 'count']:
            exp[measure]['Mean'] = (exp[measure][condition1] + exp[measure][condition2] ) / 2
            #exp[measure]['p_NoChange'] = t.PPEE
            #exp[measure]['p_DiffExp'] = t.PPDE
            #exp[measure]['est_FC'] = t.PostFC
            exp[measure]['logFC'] = log2(t.PostFC)
            exp[measure]['Fold Change'] = t.PostFC
            exp[measure]['Relative FC'] = t.PostFC
            exp[measure].ix[exp[measure]['Fold Change']<1, 'Relative FC'] = -1 /exp[measure]['Fold Change']
            exp[measure]['Probability'] = t.PPDE
            exp[measure]['*FDR'] = 1 - t.PPDE
            
            output_file = os.path.join(output_path, "DE_{f}_{m}.csv".format(
                                                     f=feature, m=measure))
            exp[measure].to_csv(output_file, float_format='%.2f')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("DGE_path", help = "Directory that holds the DGE result of EBseq")
    parser.add_argument("output", help = "Output path")
    parser.add_argument("n", help = "Number of samples in condition 1", type=int)
    args = parser.parse_args()    
    merge_exp(args.DGE_path, args.output, args.n)
