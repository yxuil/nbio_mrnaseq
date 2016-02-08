__author__ = 'liu'

import pandas as pd
import sys

if len(sys.argv) <=2:
    print("{} <output> <input> [<input2> ...]".format(sys.argv[0]))
table_out = pd.DataFrame()
for fn in sys.argv[2:]:
    sample_name = os.path.basename(fn).replace("_ReadsPerGene.out.tab", "")
    table_in = pd.read_table(fn, index_col=0, header = None, skiprows=skip)

    table_out[sample_name] = table_in[1]
table_out.index.name = "gene"
table_out.to_csv(sys.argv[1], sep = '\t')