# Introduction
mRNAseq pipeline is implemented in snakemake
[http://bitbucket.org/snakemake/snakemake/wiki/Documentation], which links
serveral open source programs to analysis mRNAseq data (illumina sequence). The
pipeline performs read alignment, expression estimation, differential expression
analysis, and report the results in a summary HTML page.

## Why snakemake
snakemake has a few desirable advantages. 
. relatively simple
. valid python statement is valid snakemake statement too
. makefile like job dependency
. job recovery after failure

Python statements are used extensively in the pipeline files (ext. with .sm).
But snakemake can be easy to use even without python. It is designed to work
like GNU make. Just as in make, it defines 'build' target (rule: 
There are obvious drawbacks of snakemake, especially on SGE, which snakemake has
larger than normal minimal memory footprint, and may hang for long time if a
program fails on the SGE. Newer version of snakemake has better communication
machenisms on the cluster, which could help with the latter issue. 

One particular issue snakemake has is that RSEM does not play will with
snakemake. When managed by snakemake, rsem-calculate-expression script will
throw an error after all tasks have been completed. This causes the pipeline 
to stop before complete all the jobs, and need to be restarted.

## Pipeline modules
There are following modules in the current pipeline:
- preprocess
  this module trims reads for adapter sequence. Currently `skewer` is implemented
for both paired end and single end sequence reads. Recent version of `cutadpt`
can handle paired reads properly. It would be possible to implement it too.
- alignment
  This module aligns reads to the genome (if STAR is choosed), or transcriptome
(if RSEM is choosed as aligner).
- quantification
  RSEM is used to quantify the gene/isoform expression. The results are in TPM,
FPKM, and expected counts. RSEM is chosen for its outstanding performance, and
(initally) the integration of EBseq. TPM is a better representation of
expression value, which just start to get traction in the community. There are
questions regarding using expected counts for downstream differential expression
analysis though. STAR generate gene counts in recent build; both featurecounts 
and HTseq-count should be relatively easy to implement, if this becomes a real
concern. [UPDATE: EdgeR manual indicated that although raw counts is preferred,
it can work with RSEM expected counts]
- differential expression 
  Both EBseq and EdgeR are implemented and will work with RSEM quantification.
However EBseq's reporting script has not updated to be integrated as a part of
the final reporting procedure yet.
- QC and report
  RseQC is implemented to examine the alignment, gene coverage, exon junction
saturation, etc. It was intended to have a few custom build scripts to replace
some of RseQC function for better QC and speed. But not all of them are
finished, and currently none of those scripts are really used yet.
  Report are in the form of HTML files. Each above modules will generate summary
table / text for their own part, and report.py will collect and assemble them
into one report. 

# Use mRNAseq pipeline
wiki page: http://wiki.biotech.wisc.edu/wiki/index.php/mRNAseq_pipeline

# Developemnt Guide
snakemake document: http://bitbucket.org/snakemake/snakemake/wiki/Documentation
rnaseq.sm is the main snakemake file. It `include`s other snakemake or python
files by default or according to run configuration file:
    include: "path/to/other/snakefile"

rnaseq.sm always includes 'toolsinfo' and 'untilities.sm', the former specifies
paths to each program used in the pipeline and the latter contains several
helper functions that are useful. One of those helper function is
`isPairedReads`, which takes a sample name and determines if sequencing files
are paired end. 

A better implementation of `isPairedReads` would allow a regex being passed to
help determining the pairings.

Each program is wrapped in a snakemake file, and resides in its own subfolder in
the modules directory, along with other scripts / files associated with it. The
module snakemake file is `include`d in the main snakemake file rnaseq.sm with 
relative path to it. snakemake provides



### Folder organization
```
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

```