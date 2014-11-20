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
    _pipeline_dir + "/toolsinfo"

# copy run_config.json to workdir
#shutil.copyfile(cwd + "/run_config.json" , config["workdir"] + "/run_config.json")
                
##### CONFIG #####
SAMPLES = config["samples"].keys()
w_dir =  config["workdir"]
delivery = config["delivery"]
data_dir = config["data_dir"]
ref_dir = config["ref_dir"]
GTF = ref_dir + "./annotation/genes_chr_only.gtf"

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
    
##### TRIMMING #####
rule trim_single:
    input: data_dir+"/{prefix, .*_R1.*}"
    output: "trimmed_fq/{prefix}.fastq"
    threads: 8
    message:
        "Trim sequencing adaptor from single end reads of sample: {wildcards.prefix}"
    shell: "{SKEWER} -x AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC "
             "-y AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
             "-k 15 -o trimmed_fq/{wildcards.prefix} -t {threads} {input}"
    
rule trim_pair:
    input: data_dir+"/{prefix}_R1{sufix}", data_dir+"./{prefix}_R2{sufix}"
    output: "trimmed_fq/{prefix}_RR{sufix}-pair1.fastq","trimmed_fq/{prefix}_RR{sufix}-pair2.fastq"
    threads: 8
    message:
        "Trim sequencing adaptor from paired end reads of sample: {wildcards.prefix}_R*{wildcards.sufix}"
    shell: "{SKEWER} -x AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC "
             "-y AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
             "-k 15 -o trimmed_fq/{wildcards.prefix}_RR{wildcards.sufix} -t {threads} {input}"

##### INDEX #####
RSEM_IDX= [ref_dir + "./RSEMIndex/genome.{i}.ebwt".format(i=i) for i in range(1,5)] +  [ref_dir + "./RSEMIndex/genome.rev.{i}.ebwt".format(i=i) for i in [1,2]]

def clean_GTF(gtf_fn, output_fn):
    valid_gtf_records = {}
    trx_id_lst = []
    dup_gtf_records = {}

    with open(gtf_fn, 'r') as gtf_in:
        for line in gtf_in:
            fields = line.strip().split('\t')

            if len(fields[0]) > 5: continue # skip non 'chrXX' lines
            trx_id = fields[-1].split(";")[1].split('"')[1] # gene_id "NM_032291"; transcript_id "NM_032291"; 
            if trx_id not in valid_gtf_records: # make a new trx entry if it is not exist yet
                valid_gtf_records[trx_id] = {'transcript_id': trx_id, 
                                             'chr': fields[0],
                                             'strand': fields[6],
                                             'GTF': []}
                trx_id_lst.append(trx_id) # for late use to keep the GTF records in the same order

            if valid_gtf_records[trx_id]['chr'] != fields[0] or valid_gtf_records[trx_id]['strand'] != fields[6]:
                # same trx_id on other chromosome
                if trx_id not in dup_gtf_records:
                    dup_gtf_records[trx_id] = {'transcript_id': trx_id, 
                                             'chr': fields[0],
                                             'strand': fields[6],
                                             'GTF': []}
                dup_gtf_records[trx_id]['GTF'].append(line)
            else:
                valid_gtf_records[trx_id]['GTF'].append(line)

    with open(output_fn, 'w') as gtf_out:
        for trx_id in trx_id_lst:
            gtf_out.writelines(valid_gtf_records[trx_id]['GTF'])
    with open("/tmp/dup.gtf", 'w') as dup_out:
        for trx_id in trx_id_lst:
            if trx_id in dup_gtf_records:
                dup_out.writelines(dup_gtf_records[trx_id]['GTF'])


rule link_ref:
    input: ref_dir + "./genome.fa"
    output: ref_dir + "./RSEMIndex/genome.fa"
    shell: "ln -sf {input} {output}\n touch {output}"
    
rule rsem_index:
    input:  ref_dir + "./RSEMIndex/genome.fa", ref_dir + "./annotation/genes.gtf"
    output: RSEM_IDX
    params:
        ref = ref_dir + "./RSEMIndex/genome"
    message: "make RSEM index with reference sequence and gene annotation"
    run:
        clean_GTF(input[1], 'gene_cleaned.gtf')
        shell("{RSEM}/rsem-prepare-reference --gtf gene_cleaned.gtf --bowtie --bowtie-path {BOWTIE} {input[0]} {params.ref}")

##### ALIGN #####

    
ruleorder:
    rsem_paired > rsem_single
rule rsem_single:
    input: 
        ref = RSEM_IDX, 
        read  = lambda wc: [ "trimmed_fq/{}.fastq".format(r) for r in config['samples'][wc.sample]  if "R1" in r]
    output: 
        "rsem_estimate/{sample}.genes.results",
        "rsem_estimate/{sample}.isoforms.results",
        "rsem_estimate/{sample}.transcript.sorted.bam",
        "rsem_estimate/{sample}.genome.sorted.bam"
    threads: 8
    params:
        ref= ref_dir + "./RSEMIndex/genome"
    message: "estimate expression from sample {wildcards.sample} RNAseq single-end reads"
    run:
        read_lst = ",".join(input.read)
        print(read_lst)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam "
            "--bowtie-path {BOWTIE} --fragment-length-mean 250 --fragment-length-sd 50 "
            "{read_lst} {params.ref} rsem_estimate/{wildcards.sample}")   
                     
rule rsem_paired:
    input: 
        ref = RSEM_IDX, 
        R1 = lambda wc: [ "trimmed_fq/{s}-pair1.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ] ,
        R2 = lambda wc: [ "trimmed_fq/{s}-pair2.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ]
    output: "rsem_estimate/{sample}.genes.results", 
            "rsem_estimate/{sample}.isoforms.results", 
            "rsem_estimate/{sample}.transcript.sorted.bam",
            "rsem_estimate/{sample}.genome.sorted.bam"
    threads: 8
    params:
        ref= ref_dir + "./RSEMIndex/genome"
    message: "Estimate expression from sample {wildcards.sample} RNAseq paired-end reads"
    run:
        read1_lst = ",".join(input.R1)
        read2_lst = ",".join(input.R2)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam --bowtie-path {BOWTIE} "\
              "--paired-end {read1_lst} {read2_lst} {params.ref} rsem_estimate/{wildcards.sample}")
    
###### DE genes ######
rule gene_matrix:
    input: lambda wc: ["rsem_estimate/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       sorted(config["treatments"][wc.exp]) + sorted(config["treatments"][wc.ctrl]) ]
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    message: "Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + sorted(config["treatments"][wildcards.exp]) + sorted(config["treatments"][wildcards.ctrl]))
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}")
        
rule ebseq:
    input: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_FCstat.txt"
    message: "Differential expression analysis between treatment groups with ebseq"
    run:
        conditions=','.join(map(str, (map(len, [config["treatments"][wildcards.exp], config["treatments"][wildcards.ctrl]]))))
        shell("{RSEM}/rsem-run-ebseq {input} {conditions} {output}")

rule de_fdr:
    input: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_FCstat.txt"
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_DE_FCstat.txt"
    params: 
        pval = config["FDR"]
    message:
        "Filter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"

rule expression_table:
    input: cfg_fn, "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}{de, _|_DE_}FCstat.txt" 
    output: "diff_expr/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}{de, _|_DE_}table.txt"
    #message: "Make gene table from expression results (rsem) and fold change result (EBseq)"
    shell: "{_pipeline_dir}/format_rsem_results.py {input} > {output}"
        
#### rules for comparing all groups together
rule gene_matrix_all:
    input: lambda wc: ["rsem_estimate/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ] ]
    output: "expression/all.{feature, [a-zA-Z]+}.counts.matrix"
    message: "Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ])
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}") 
        
rule ebseq_all:
    input: "expression/all.{feature, [a-zA-Z]+}.counts.matrix"
    output: "expression/all.{feature, [a-zA-Z]+}_FCstat.txt"
    params:
        conditions=','.join(map(str, (map(len, config["treatments"].values()))))
    message: "Differential expression analysis among all treatment groups with ebseq"
    shell: "{RSEM}/rsem-run-ebseq {input} {params.conditions} {output}"    

rule de_fdr_all:
    input: "expression/all.{feature, [a-zA-Z]+}_FCstat.txt"
    output: "expression/all.{feature, [a-zA-Z]+}_DE_FCstat.txt"
    params: 
        pval = config["FDR"]
    message:
        "Filter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"