import sys, os, shutil

cfg_fn = "run_config.json"

configfile:
    cfg_fn

workdir:
    config["workdir"]
    
# include software/program information
# HACK: to get current Snakefile directory
_pipeline_dir = os.path.abspath(sys.path[0])
include: 
    _pipeline_dir + "/toolsinfo",
    _pipeline_dir + "/paired_reads_sm.py",
    _pipeline_dir + "/DE_analysis_sm.py"

# copy run_config.json to workdir
#shutil.copyfile(cwd + "/run_config.json" , config["workdir"] + "/run_config.json")
                
##### CONFIG #####
SAMPLES = config["samples"].keys()
w_dir =  config["workdir"]
delivery = config["delivery"]
data_dir = config["data_dir"]
ref_dir = config["ref_dir"]
GTF = ref_dir + "./annotation/genes_chr_only.gtf"=

expGrp_lst =  [ str.strip(comp.split("-")[0]) for comp in config["comparisons"]]
ctrlGrp_lst = [ str.strip(comp.split("-")[1]) for comp in config["comparisons"]]
    
##### target #####
# run all the rules by default
rule all:
    input: ["diff_expr/{}_vs_{}.{}_{}table.txt".format(exp,ctrl,feature, de)  \
            for exp, ctrl in zip(expGrp_lst, ctrlGrp_lst) \
            for feature in ['genes','isoforms'] ] \
            for de in ['', 'DE_']

# use all conditions in one conparison
rule one_compare: 
    input: ["diff_expr/all.{}_DE_table.txt".format(feature) for feature in ['genes','isoforms'] ]
    # input: "expression/all.genes.counts.matrix","expression/all.isoforms.counts.matrix"

##### deliver #####
rule deliver:
    input: ["diff_expr/{}_vs_{}.{}_{}table.txt".format(exp,ctrl,feature, de)  \
            for exp, ctrl in zip(expGrp_lst, ctrlGrp_lst) \
            for feature in ['genes','isoforms'] ] \
            for de in ['', 'DE_']
    output: ["{}/diff_expr/{}_vs_{}.{}_{}table.txt".format(delivery, exp,ctrl,feature, de)  \
            for exp, ctrl in zip(expGrp_lst, ctrlGrp_lst) \
            for feature in ['genes','isoforms'] ] \
            for de in ['', 'DE_']
    message:
        "Copy / move results to delivery folder"
    shell:
        """
        mkdir snakejob.log
        mv snakejob.* snakejob.log
        mkdir -p {delivery}
        mkdir {delivery}/alignment
        for bam in rsem_estimate/*.genome.sorted.bam; do 
           mv ${{bam}} {delivery}/alignment; 
           ln -s {delivery}/alignment/${{bam}} ${{bam}};
           mv ${{bam}}.bai {delivery}/alignment; 
           ln -s {delivery}/alignment/${{bam}}.bai ${{bam}}.bai;  
        done
        cp -r diff_expr/ {delivery}
        cp -r expression/ {delivery}
        """


##### remove #####
rule remove:
    shell: "rm -r rsem_estimate/ trimmed_fq/ DE_gene.txt gene_reads_counts.matrix *snakejob*"





#### RNAseQC
# rule qc:
#     input: "qc/bam_list.txt"
#     output: "qc/report.html"
#     params: rrna=config["rRNA_fa"],
#             ref =config["ref_fa"],
#             gtf =config["gtf"],
#             o_dir = "qc",
#             single = ""
#     shell: "java -jar {RNASEQC} -BWArRNA {params.rrna} " \
#            "-r {params.ref} -s {input} -singleEnd -t hg38_gene.gtf -o {o_dir}"
#
# rule bamlist:
#     input: "alignment/*/*.bam"
#     output: "qc/bam_list.txt"
#     shell: "{_pipeline}/qc.py bamlist {input}"