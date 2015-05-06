#!/usr/bin/env python

from glob import glob
from jinja2 import Template
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

    trim_html = open("trimmed_fq/trim_stat.html").read()
    bam_qc_html = open("QC_graphs/qc_table.html").read()
    alignment_html = open("alignments/alignment_stat.html").read()
    de_html  = open("diff_expr/de_report.html").read()

    t = Template(open(os.path.join(os.path.abspath(sys.path[0]), "report.html")).read())
    html_str =  t.render(locals())
    return html_str


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: {} <run_config>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    print "Generating report..."
    r = generate_report(config)
    with open(os.path.join(config["workdir"], "report.html"), 'w') as html_out:
        html_out.write(r)

    print "Report Finished"