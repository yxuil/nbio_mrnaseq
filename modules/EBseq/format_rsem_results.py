#!/mnt/grl/software/epd/bin/python
'''
format DGE results
'''
__author__ = "Xiaoyu Liu"
__email__ = "liux@nbio.info"
__copyright__ = "Copyright (C) 2016 Xiaoyu Liu"
__status__ = "development"
__license__ = "Public Domain"
__version__ = "0.2b"

import os, sys, json
import pandas as pd

def save_gene_table(config_fn, fc_file):
    config = json.loads(open(config_fn, 'r').read())
    exp, ctrl = os.path.basename(fc_file).split(".")[0].split("_vs_")
    feature   = os.path.basename(fc_file).split(".")[1].split("_")[0]
    w_dir = config['workdir']
    tpm = None
    for s in config["treatments"][exp]+config["treatments"][ctrl]:
        exp_fn = "{d}/expression/{s}_{f}_table.txt".format(d=w_dir, s=s, f=feature)
        df = pd.read_table(exp_fn, index_col = [0])
        if tpm is None: # get the first samples expression value
            tpm = df[["TPM"]]
            tpm.columns = [s]
            continue
        # add the TPM value to the table
        tpm[s] = df[["TPM"]]
    # avg expresion, fold change, and p_value
    df = pd.read_table(fc_file, index_col=[0])
    tpm=tpm.ix[df.index]
    
    # add average expression to the table
    tpm["avg"] = tpm.mean(axis=1)
    
    tpm['p-value'] = 1-df.PPDE
    tpm['Fold Change'] = df.RealFC.apply(lambda x: x if x >= 1 else -1/x ) # change fc <1 to negative number
    
    tpm.to_csv(sys.stdout, sep="\t", float_format='%.2f')

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        save_gene_table(sys.argv[1], sys.argv[2])
    else:
        print("Usage: {} config_file fold_change_file".format(argv[0]))
