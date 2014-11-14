import sys, os, shutil

configfile:
    "run_config.json"

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
data_dir = config["data_dir"]
ref_dir = config["ref_dir"]
GTF = ref_dir + "./annotation/genes_chr_only.gtf"

expGrp_lst =  [ str.strip(comp.split("-")[0]) for comp in config["comparisons"]]
ctrlGrp_lst = [ str.strip(comp.split("-")[1]) for comp in config["comparisons"]]
    
##### target #####
# run all the rules by default
rule all:
    input: ["diff_expr/{}_vs_{}.{}_DE_table.txt".format(exp,ctrl,feature)  \
            for exp, ctrl in zip(expGrp_lst, ctrlGrp_lst) \
            for feature in ['genes','isoforms'] ]

# use all conditions in one conparison
rule one_compare: 
    input: ["diff_expr/all.{}_DE_table.txt".format(feature) for feature in ['genes','isoforms'] ]
    
##### deliver #####
rule deliver:
    input: ""
    output: "{PI}/projects/{rt}/all.genes_DE.txt"
    message:
        "Copy / move results to delivery folder"
    shell:
        """
        cp
        mv
        ln -s
        """


##### remove #####
rule remove:
    shell: "rm -r rsem_alignment/ trimmed_fq/ DE_gene.txt gene_reads_counts.matrix *snakejob*"
    
##### TRIMMING #####
#rule trim_r1:
    #input: lambda wildcards: config["samples"][wildcards.sample]  #glob("../data/run*.{sample}_*_L*_R1.fastq.gz")
    #output: "trimmed_fq/{sample}_R1.trimmed.fq"
    #threads: 1
    #shell: "echo input is {input}"
        #"{CUTADAPT} -m 16 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -o {output} {input}" 

#rule trim_r2:
    #input: lambda wc: glob("../data/run*.{wc.sample}_*_L*_R2.fastq.gz".format(wc=wc))
    #output: "trimmed_fq/{sample}_R2.trimmed.fq"
    #threads: 1
    #shell: "{CUTADAPT} -m 16 -a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT \
            #-o {output} {input}"

rule trim_single:
    input: data_dir+"./{prefix, .*_R1.*}"
    output: "trimmed_fq/{prefix}.fastq"
    threads: 8
    message:
        "Trim sequencing adaptor from single end reads of sample: {wildcards.prefix}"
    shell: "{SKEWER} -x AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC "
             "-y AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
             "-k 15 -o trimmed_fq/{wildcards.prefix} -t {threads} {input}"
    
rule trim_pair:
    input: data_dir+"./{prefix}_R1{sufix}", data_dir+"./{prefix}_R2{sufix}"
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

def getR1trimmedName(wc):
    R1_fn = [ r for r in config['samples'][wc.sample] if "R1" in r ]
    basename = map(lambda x: x.replace("_R1","@@").replace("R1","@@").split("@@")[0], R1_fn)
    trimmedName = ["trimmed_fq/" + b  + "-pair1.fastq" for b in basename]
    return trimmedName

def getR2trimmedName(wc):
    trimmedName = map(lambda x: x.replace("pair1","pair2"), getR1trimmedName(wc))
    return trimmedName

def getSingleTrimmedName(wc):
    trimmedName = map(lambda x: x.replace("-pair1", ""), getR1trimmedName(wc))
    return trimmedName
    
ruleorder:
    rsem_paired > rsem_single
rule rsem_single:
    input: 
        ref = RSEM_IDX, 
        read  = lambda wc: [ "trimmed_fq/{}.fastq".format(r) for r in config['samples'][wc.sample]  if "R1" in r]
    output: 
        "rsem_alignment/{sample}.genes.results",
        "rsem_alignment/{sample}.isoforms.results",
        "rsem_alignment/{sample}.transcript.sorted.bam",
        "rsem_alignment/{sample}.genome.sorted.bam"
    threads: 8
    params:
        ref= ref_dir + "./RSEMIndex/genome"
    message: "estimate expression from sample {wildcards.sample} RNAseq single-end reads"
    run:
        read_lst = ",".join(input.read)
        print(read_lst)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam "
            "--bowtie-path {BOWTIE} --fragment-length-mean 250 --fragment-length-sd 50 "
            "{read_lst} {params.ref} rsem_alignment/{wildcards.sample}")   
                     
rule rsem_paired:
    input: 
        ref = RSEM_IDX, 
        R1 = lambda wc: [ "trimmed_fq/{s}-pair1.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ] ,
        R2 = lambda wc: [ "trimmed_fq/{s}-pair2.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ]
    output: "rsem_alignment/{sample}.genes.results", 
            "rsem_alignment/{sample}.isoforms.results", 
            "rsem_alignment/{sample}.transcript.sorted.bam",
            "rsem_alignment/{sample}.genome.sorted.bam"
    threads: 8
    params:
        ref= ref_dir + "./RSEMIndex/genome"
    message: "Estimate expression from sample {wildcards.sample} RNAseq paired-end reads"
    run:
        read1_lst = ",".join(input.R1)
        read2_lst = ",".join(input.R2)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam --bowtie-path {BOWTIE} "\
              "--paired-end {read1_lst} {read2_lst} {params.ref} rsem_alignment/{wildcards.sample}")
    
###### DE genes ######
rule gene_matrix:
    input: lambda wc: ["rsem_alignment/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       sorted(config["treatments"][wc.exp]) + sorted(config["treatments"][wc.ctrl]) ]
    output: "counts/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    message: "Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + sorted(config["treatments"][wildcards.exp]) + sorted(config["treatments"][wildcards.ctrl]))
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}")
        
rule ebseq:
    input: "counts/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    output: "diff_expr/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_table.txt"
    message: "Differential expression analysis between treatment groups with ebseq"
    run:
        conditions=','.join(map(str, (map(len, [config["treatments"][wildcards.exp], config["treatments"][wildcards.ctrl]]))))
        shell("{RSEM}/rsem-run-ebseq {input} {conditions} {output}")

rule de_fdr:
    input: "diff_expr/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_table.txt"
    output: "diff_expr/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_DE_table.txt"
    params: 
        pval = config["FDR"]
    message:
        "Filter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"

#### rules for comparing all groups together
rule gene_matrix_all:
    input: lambda wc: ["rsem_alignment/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ] ]
    output: "counts/all.{feature, [a-zA-Z]+}.counts.matrix"
    message: "Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ])
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}") 
        
rule ebseq_all:
    input: "counts/all.{feature, [a-zA-Z]+}.counts.matrix"
    output: "diff_expr/all.{feature, [a-zA-Z]+}_table.txt"
    params:
        conditions=','.join(map(str, (map(len, config["treatments"].values()))))
    message: "Differential expression analysis among all treatment groups with ebseq"
    shell: "{RSEM}/rsem-run-ebseq {input} {params.conditions} {output}"    

rule de_fdr_all:
    input: "diff_expr/all.{feature, [a-zA-Z]+}_table.txt"
    output: "diff_expr/all.{feature, [a-zA-Z]+}_DE_table.txt"
    params: 
        pval = config["FDR"]
    message:
        "Filter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"