
##### TRIMMING #####

rule trim_pair:
    input: data_dir+"/{prefix}_R1{sufix}", data_dir+"./{prefix}_R2{sufix}"
    output: "trimmed_fq/{prefix}_RR{sufix}-pair1.fastq","trimmed_fq/{prefix}_RR{sufix}-pair2.fastq"
    threads: 8
    message:
        "\n    Trim sequencing adaptor from paired end reads of sample: {wildcards.prefix}_R*{wildcards.sufix}"
    shell: "{SKEWER} -x AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -y AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
           "-k 15 -l 25 -q 20 -t {threads} -o trimmed_fq/{wildcards.prefix}_RR{wildcards.sufix} {input}"

##### STAR ALIGNMENT #####
def get_ref():
    if 'ref_dir' in config:
        return os.path.join(['ref_dir'], 'genome.fa')
    elif 'ref_fa' in config:
        return config['ref_fa']
    else:
        return "ref/genome.fa"

rule star_prep:
    input: get_ref()
    output: "ref/genome.fa"
    params:
        ref_dir = config['ref_dir'],
        ref_gtf = "",
        ref_fa  = ""
    message: "\n    # Create STAR reference genome index"
    shell: ""

rule star_align:
    input:
        ref="ref/genome.fa",
        R1 = lambda wc: [ "trimmed_fq/{s}-pair1.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ] ,
        R2 = lambda wc: [ "trimmed_fq/{s}-pair2.fastq".format(s=r.replace("R1", "RR")) for r in config['samples'][wc.sample] if "R1" in r ]
    output:
        "star_align/{sample}/Aligned_.bam"
    message: "\n    Align sample {sample} reads to reference with STAR"
    shell: "{STAR} "

##### RSEM quantification #####

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
    message: "\n    Estimate expression from sample {wildcards.sample} RNAseq paired-end reads"
    run:
        read1_lst = ",".join(input.R1)
        read2_lst = ",".join(input.R2)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam --bowtie-path {BOWTIE} "\
              "--paired-end {read1_lst} {read2_lst} {params.ref} rsem_estimate/{wildcards.sample}")

