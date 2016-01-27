# Developemnt Guide

### Folder organization
.
├── rnaseq.sm   <= main pipeline file
├── run_rnaseq_sge.sh       <- bash wrapper submit jobs to SGE
├── run_rnaseq.sh           <- bash wrapper run jobs locolly
├── deliver.sh              <- delivery script
├── config                  <= configuration files, and to manipulate
│   ├── ini2json.py         <- make JSON file from INI format
│   ├── run_config.cfg      <- example configure file
│   ├── run_config.json     <- example configure in JSON
│   └── toolsinfo           <- config paths of softwares used
└── modules                 <=
│   ├── utilities.sm  <- helper functions
│   ├── preprocess          <= Trim and filter reads
│   │   ├── trim_report.py
│   │   └── trim.sm
│   ├── STAR                <= Align to genome
│   │   ├── align_star_report.py
│   │   ├── align_star.sm
│   │   ├── quant_star.py
│   │   └── star_junc_merge.py
│   ├── RSEM                <= Quantitate; align to mRNA (option)
│   │   ├── prepare_reference.sm
│   │   └── quant_rsem.sm
│   ├── quant_featurecounts.sm <- reads count (not completed)
│   ├── EBseq               <= EBseq : need report hook 
│   │   ├── DE_analysis_ebseq.sm
│   │   ├── DE_ebseq_report.py <- need update to current report hook
│   │   └── format_rsem_results.py
│   ├── EdgeR               <= EdgeR : currently implemented
│   │   ├── DE_analysis_edger.sm
│   │   ├── DE_edger_report.py
│   │   ├── report_edger.py
│   │   └── script_edger.py
│   ├── goseq               <= goseq: need both config hook and report hook
│   │   ├── goseq.py
│   │   ├── goseq.sm
│   │   ├── make_de_gene_list.py
│   │   └── report_goseq.py
│   ├── report              <= report module
│   │   ├── CSS             <= CSS file used in html pages
│   │   │   ├── bokeh-0.9.2.min.css
│   │   │   ├── bootstrap.min.css
│   │   │   ├── dashboard.css
│   │   │   └── jquery-ui.css
│   │   ├── degust.py       <= degust html maker (not in use)
│   │   ├── JS              <= javascript file used in html
│   │   │   ├── bokeh-0.9.2.min.js
│   │   │   ├── bootstrap.min.js
│   │   │   ├── custom.js
│   │   │   ├── jquery-2.1.3.min.js
│   │   │   ├── jquery.min.js
│   │   │   └── jquery-ui.js
│   │   ├── report_de_table.py 
│   │   ├── report.py
│   │   ├── report.sm
│   │   ├── software_version.py
│   │   ├── templates       <= html templates
│   │   │   ├── alignment_QC.html
│   │   │   ├── alignment_stat.html
│   │   │   ├── base.html
│   │   │   ├── diffexpr.html
│   │   │   ├── expression.html
│   │   │   ├── genesets.html
│   │   │   ├── project.html
│   │   │   ├── readsdata.html
│   │   │   ├── redirect.html
│   │   │   ├── report.html
│   │   │   ├── report_template.html
│   │   │   ├── versions.html
│   │   │   └── workflow.html
│   │   └── workflow.png
│   ├── rsemQC      <- QC use STAR transcriptome alignment (not in use)
│   │   ├── alignment_distribution.py
│   │   ├── gene_coverage.py
│   │   ├── insert_size.py
│   │   └── transcript_satuation.py
│   ├── RSeQC       <- QC package
│   │   ├── RSeQC_report.py
│   │   └── RSeQC.sm

