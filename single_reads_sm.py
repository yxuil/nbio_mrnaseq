
##### TRIMMING #####
rule trim_single:
    input: data_dir+"/{prefix, .*_R1.*}"
    output: "trimmed_fq/{prefix}.fastq"
    threads: 8
    message:
        "\n    Trim sequencing adaptor from single end reads of sample: {wildcards.prefix}"
    shell: "{SKEWER} -x AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC "
             "-y AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT "
             "-k 15 -o trimmed_fq/{wildcards.prefix} -t {threads} {input}"


##### STAR alginment #####
##### RSEM quantification #####
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
    message: "\n    estimate expression from sample {wildcards.sample} RNAseq single-end reads"
    run:
        read_lst = ",".join(input.read)
        print(read_lst)
        shell("{RSEM}/rsem-calculate-expression -p {threads} --output-genome-bam "
            "--bowtie-path {BOWTIE} --fragment-length-mean 250 --fragment-length-sd 50 "
            "{read_lst} {params.ref} rsem_estimate/{wildcards.sample}")
