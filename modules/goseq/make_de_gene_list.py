#!/usr/bin/env python
__author__ = "Xiaoyu Liu"
__email__ = "liux@nbio.info"
__copyright__ = "Copyright (C) 2016 Xiaoyu Liu"
__status__ = "development"
__license__ = "Public Domain"
__version__ = "0.1"

import pandas as pd
import sys, os

def genetable_to_DElist(filename, p_col = "p-value", p_value = 0.05):
    '''

    :param filename: genetable filename
    :param p_col: name of the column that contains p values
    :param p_value: p value threshold for differential expression cutoff
    :return: DE list in dataframe
    '''

    gt = pd.read_table(filename, index_col = 0)
    gt.columns.name = "genename"
    de = gt["p-value"] < p_value
    gt["diffexpr"] = de.map(lambda x: 1 if x else 0)

    return gt[["diffexpr"]]

if __name__ == "__main__":
    USAGE = "{} [filename]\n".format(
        os.path.basename(sys.argv[0]))
    ops = sys.argv[1:]

    if len(ops) < 1:  # no cli options
        print(USAGE)
    else:
        if os.path.isfile(ops[0]):
            delist = genetable_to_DElist(ops[0])
            print(delist.to_csv(sep="\t")) # output to consoe





