###### DE genes ######
rule gene_matrix:
    input: lambda wc: ["rsem_estimate/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       sorted(config["treatments"][wc.exp]) + sorted(config["treatments"][wc.ctrl]) ]
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    message: "\n    Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + sorted(config["treatments"][wildcards.exp]) + sorted(config["treatments"][wildcards.ctrl]))
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}")
        
rule ebseq:
    input: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}.counts.matrix"
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_w_FCstat.txt"
    message: "\n    Differential expression analysis between treatment groups with ebseq"
    run:
        conditions=','.join(map(str, (map(len, [config["treatments"][wildcards.exp], config["treatments"][wildcards.ctrl]]))))
        shell("{RSEM}/rsem-run-ebseq {input} {conditions} {output}")

rule de_fdr:
    input: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_w_FCstat.txt"
    output: "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}_DE_w_FCstat.txt"
    params: 
        pval = config["FDR"]
    message:
        "Filter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"

rule expression_table:
    input: cfg_fn, "expression/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}{de, _|_DE_}w_FCstat.txt"
    output: "diff_expr/{exp}_vs_{ctrl}.{feature, [a-zA-Z]+}{de, _|_DE_}table.txt"
    #message: "\n    Make gene table from expression results (rsem) and fold change result (EBseq)"
    shell: "{_pipeline_dir}/format_rsem_results.py {input} > {output}"
        
#### rules for comparing all groups together
rule gene_matrix_all:
    input: lambda wc: ["rsem_estimate/{s}.{f}.results".format(s=sample, f=wc.feature) for sample in \
                       [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ] ]
    output: "expression/all.{feature, [a-zA-Z]+}.counts.matrix"
    message: "\n    Merging reads count for genes / isoforms data matrix"
    run:
        header_str = "\t".join([""] + [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ])
        shell("{RSEM}/rsem-generate-data-matrix {input} > {output}")
        shell("sed -i '1s/.*/{header_str}/' {output}") 
        
rule ebseq_all:
    input: "expression/all.{feature, [a-zA-Z]+}.counts.matrix"
    output: "expression/all.{feature, [a-zA-Z]+}_w_FCstat.txt"
    params:
        conditions=','.join(map(str, (map(len, config["treatments"].values()))))
    message: "\n    Differential expression analysis among all treatment groups with ebseq"
    shell: "{RSEM}/rsem-run-ebseq {input} {params.conditions} {output}"    

rule de_fdr_all:
    input: "expression/all.{feature, [a-zA-Z]+}_w_FCstat.txt"
    output: "expression/all.{feature, [a-zA-Z]+}_DE_w_FCstat.txt"
    params: 
        pval = config["FDR"]
    message:
            "\nFilter for differentially expressed genes by FDR"
    shell: "{RSEM}/rsem-control-fdr {input} {params.pval} {output}"

rule expression_table_all:
    input: cfg_fn, "expression/all.{feature, [a-zA-Z]+}{de, _|_DE_}w_FCstat.txt"
    output: "diff_expr/all.{feature, [a-zA-Z]+}{de, _|_DE_}table.txt"
    shell: "{_pipeline_dir}/format_rsem_results.py {input} > {output}"
