""" obselete
"""

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
    message: "\n    Make RSEM index with reference sequence and gene annotation"
    run:
        clean_GTF(input[1], 'gene_cleaned.gtf')
        shell("{RSEM}/rsem-prepare-reference --gtf gene_cleaned.gtf --bowtie --bowtie-path {BOWTIE} {input[0]} {params.ref}")

