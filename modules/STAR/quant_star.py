__author__ = 'liu'

rule star_exp_matrix:
    input: lambda wc: ["tmp/star_alignment_pass2/{s}_ReadsPerGene.out.tab".format(s=sample, f=wc.feature) for sample in \
                       config["treatments"][wc.exp] + config["treatments"][wc.ctrl] ]
    output: "tmp/star_alignment_readcounts/"
    log: "tmp/shell_log/{exp}_vs_{ctrl}.{feature}_cntMat.log"
    params:
        mem = "1G",
        header_str = lambda wildcards: "\t".join([""] + config["treatments"][wildcards.exp] + config["treatments"][wildcards.ctrl])
    message: "\n    Merging reads count for {wildcards.exp}_vs_{wildcards.ctrl}.{wildcards.feature} data matrix"
    shell: """
             {RSEM}/rsem-generate-data-matrix {input} > {output}
             sed -i '1s/.*/{params.header_str}/' {output}
             """


