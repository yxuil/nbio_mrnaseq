#!/usr/bin/env python
import pandas as pd
import json, sys

def make_exp_table(exp_path, samples, feature):
    '''
    given sample list (samples), and disired features ('genes', 'isoforms'), collect the
    specified measurement ("expected_count", "TPM" or "FPKM"
    '''
    exp_table = { "expected_count": pd.DataFrame(), "TPM": pd.DataFrame(), "FPKM": pd.DataFrame() }
    for sample in samples:
        exp_fn = "{p}/{s}_{f}_table.txt".format(p=exp_path, s=sample, f=feature)
        print("reading", exp_fn)
        m = pd.read_table(exp_fn, index_col=[0])
        for measure in exp_table.keys():
            exp_table[measure][sample] = m[measure]

    for measure in exp_table.keys():
        o_fn = "{}/{}_{}_table.txt".format(exp_path, feature, measure.replace("expected_",""))
        print("saving", o_fn)
        exp_table[measure].to_csv(o_fn, sep="\t")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: {} <run_config> <feature>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))

    # nake none duplicate sample list
    duplicates=set()
    samples = [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] \
                  if not (s in duplicates or duplicates.add(s))]
    make_exp_table(config.get("workdir", ".") + "/expression", samples, sys.argv[2])