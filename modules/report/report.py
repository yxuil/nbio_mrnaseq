#!/usr/bin/env python

from glob import glob
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

import pandas as pd
import os, sys, json
import re, time

def generate_report(config):
    outputDir= config.get("workdir", "")
    PIname = config.get("piname", "")
    description = config.get("project", "")
    sample_num = len(config.get("samples", ""))
    organism = config.get("organism", "")
    ref = config.get("ref_base", "")
    report_time = time.asctime()

    trim_html = open("trimmed_fq/trim_stat.html").read() \
        if os.path.isfile("trimmed_fq/trim_stat.html") \
        else "Reads trim report is not available."
    bam_qc_html = open("QC_graphs/qc_table.html").read() \
        if os.path.isfile("QC_graphs/qc_table.html") \
        else "mRNAseq Alignment quality report is not available."
    alignment_html = open("alignments/alignment_stat.html").read()\
        if os.path.isfile("alignments/alignment_stat.html") \
        else "Alignment report is not available."
    expr_html  = open("expression/exp_report.html").read()\
        if os.path.isfile("expression/exp_report.html") \
        else "Expression tables are not available"
    de_html  = open("diff_expr/de_report.html").read()\
        if os.path.isfile("diff_expr/de_report.html") \
        else "Differential expression report is not available"
    geneset_html  = open("pathway/pathway_report.html").read()\
        if os.path.isfile("pathway/pathway_report.html") \
        else "Pathway analysis was not ordered. Pathway report is not available "
    #_html  = open("").read()\
    #    if os.path.isfile \
    #    else ""

    env = Environment()
    template_path = os.path.abspath(sys.path[0])
    env.loader = FileSystemLoader(template_path)

    pages = "workflow project readsdata alignment_stat alignment_QC expression diffexpr genesets versions".split()


    for html in pages:
        print("writing {}.html".format(html))
        t = env.get_template(html + ".html") #Template(open(os.path.join(template_path, html + ".html")).read())
        html_str =  t.render(locals())
        with open(os.path.join(config["workdir"], "report/{}.html".format(html)), 'w') as html_out:
            html_out.write(html_str.encode('utf-8'))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: {} <run_config>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    print("Generating report...")
    r = generate_report(config)

    print("Report Finished")