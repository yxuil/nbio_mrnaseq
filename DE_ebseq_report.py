#!/usr/bin/env python

import pandas as pd
import os, sys, json

def ebseq_report(config, output):
    """
    :param config: run configuration file that contains group, sample information
    :param output: output prefix for saving file
    :return:
    """
    header = "Comparison,Condition1,Condition2,Total Expressed Genes,DE Genes".split(',')
    table_content  = []

    for cmp in config["comparisons"]:
        condition1, condition2 = map(lambda x: str(x).strip(), cmp.split("-")) # split cmp and strip whitespace
        fn = "diff_expr/{}_vs_{}.genes_table.txt".format(condition1, condition2)
        with open(fn) as f_in:
            line_count = sum(1 for _ in f_in)  # _ is a throwaway variable
        total_gene = line_count - 1            # remove the header line

        fn = "diff_expr/{}_vs_{}.genes_DE_table.txt".format(condition1, condition2)
        with open(fn) as f_in:
            line_count = sum(1 for _ in f_in)
        de_gene = line_count - 1
        table_content.append([cmp, config["treatments"][condition1], config["treatments"][condition2], total_gene, de_gene])

    table_df = pd.DataFrame([i[1:] for i in table_content], columns=header[1:], index=[i[0] for i in table_content ])
    table_df.index.name = header[0]
    table_df.to_csv(output + ".txt", sep="\t", index=False)
    with open(output + ".html", 'w') as f_out:
        f_out.write(table_df.to_html(classes="brc", escape=False))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: {} <run_config> <output_prefix>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    ebseq_report(config, sys.argv[2])