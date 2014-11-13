#!/mnt/grl/software/epd/bin/python

from glob import glob
import os
sub_cmd="qsub -V -cwd -j y -b y -q {queue} -N {job} -o {log} -l vf={mem} {options} "
script_dir = os.path.dirname(os.path.realpath(__file__))

def make_aln_script(opt):
    rsem_cmd_tmplt = '"{rsem}/rsem-calculate-expression -p {thread} --output-genome-bam --bowtie-path {bowtie} {reads_string} {ref} {sampleName}; touch .alignment_done"\n'
    
    alignment_cmd = '\n## ==== Align reads with RSEM ==== ##\n'
    # create folders
    log_path = os.path.join(opt.outputPath, 'log')
    aln_path = os.path.join(opt.outputPath, 'rsem_alignment')
    
    for pth in [log_path, aln_path]:
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = pth)
    # check if RSEM reference exists
    rsemIndexPath = os.path.join(opt.refPath, "RSEMIndex", "genome")
    rsemIndexFiles = set(['genome.2.ebwt', 'genome.chrlist', 'genome.rev.2.ebwt', 
                          'genome.1.ebwt', 'genome.3.ebwt', 'genome.idx.fa', 'genome.seq', 
                          'genome.rev.1.ebwt', 'genome.transcripts.fa', 'genome.ti', 
                          'genome.grp', 'genome.4.ebwt'])
    fileInRSEMIndexPath = map(os.path.basename, glob(rsemIndexPath + "*"))
    hold_option = ""
    if not rsemIndexFiles.issubset(set(fileInRSEMIndexPath)):
        # RSEMIndex does not exist, let create it
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = rsemIndexPath)
        
        # prepare genome
        alignment_cmd += sub_cmd.format(queue = opt.queue,
             job   = 'rsemIdx' ,
             log   = os.path.join(log_path, 'rsem_indexing.log' ),
             mem   = "4G",
             options = hold_option)
        alignment_cmd += '"{rsem}/rsem-prepare-reference --gtf {gtf} --bowtie-path {bowtie} {genome} {indexPfx}"\n'.format\
            (rsem = opt.rsem,
             gtf = os.path.join(opt.refPath, "annotation", "genes_chr_only.gtf"),
             bowtie = opt.bowtie,
             genome = os.path.join(opt.refPath, "genome.fa"),
             indexPfx = os.path.join(opt.refPath, "RSEMIndex", "genome") )
        # hold alignment until Indexing finishes
        hold_option = '-hold_jid rsemIdx'
        
        # rsem_generate_ngvector
        alignment_cmd += sub_cmd.format(queue = opt.queue,
                     job   = 'rsemNgvector' ,
                     log   = os.path.join(log_path, 'rsem_generate_ngvector.log' ),
                     mem   = "4G",
                     options = hold_option)        
        alignment_cmd += ' "{rsem}/rsem-generate-ngvector {ref_transcripts_fa} {ngvector}"\n'.format\
            (rsem = opt.rsem,
             ref_transcripts_fa = os.path.join(opt.refPath, "RSEMIndex", "genome.transcripts.fa"),
             ngvector = os.path.join(opt.refPath, "RSEMIndex", "genome.transcripts")  )
    
    # alignment
    for sampleName, readPaths in opt.samplePath.items():
        # create alignment output directory if not exist
        aln_dir = os.path.join(aln_path, sampleName)
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = aln_dir)
        alignment_cmd += "cd {}\n".format(aln_dir)
        
        # unzip reads
        # make reads string
        reads_str = ''
        read1_str, read2_str = '', ''
        if hold_option == "":
            # no holding yet, make one
            hold_option = '-hold_jid '
        else:
            # prepare for additional holding option
            hold_option +=','
        for files in readPaths:
            if '.gz' in files[0]:
                    basename=os.path.basename(files[0])
                    fastaName=os.path.join(aln_dir, basename.replace(".gz", ""))
                    job_id = "unzip_{}".format(os.path.basename(fastaName))
                    alignment_cmd += sub_cmd.format(job= job_id, queue = opt.queue,
                                            log=os.path.join(aln_dir, job_id + ".log"),
                                            mem = "4G", options=' ')
                    #x = '"zcat {read} > {fas}" \n'.format(read=files[1], fas= fastaName)
                    #alignment_cmd += x
                    alignment_cmd += '"zcat {read} > {fas}" \n'.format(read=files[0], fas= fastaName)
                    hold_option += (job_id+',')
                    read1_str += (fastaName+ ',')
            if len(files) == 2:
                if '.gz' in files[1]:
                    basename=os.path.basename(files[1])
                    fastaName=os.path.join(aln_dir, basename.replace(".gz", ""))
                    job_id = "unzip_{}".format(os.path.basename(fastaName))
                    alignment_cmd += sub_cmd.format(job= job_id, queue = opt.queue,\
                                            log=os.path.join(log_path, job_id + ".log"),\
                                            mem="4G",
                                            options=' ') 
                    alignment_cmd += '"zcat {read} > {fas}" \n'.format(read=files[1], fas= fastaName)
                    hold_option += (job_id+',')
                    read2_str += (fastaName+ ',')
        paired=''
        if read2_str != '': # paired end
            paired="--paired-end"
    
        reads_str=' '.join([paired, read1_str.rstrip(','), read2_str.rstrip(',')])
        hold_option = hold_option.rstrip(',')
            

        # alignment command
        alignment_cmd += sub_cmd.format(queue = opt.queue,
                            job   = 'aln_%s' % (sampleName,),
                            log   = os.path.join(log_path, 'aln_%s.log' % (sampleName,)),
                            mem = opt.max_mem,
                            options = hold_option + " -m abe -M liu@biotech.wisc.edu ")
        alignment_cmd += rsem_cmd_tmplt.format(thread = opt.thread,
                            bowtie = opt.bowtie,
                            rsem = opt.rsem,
                            reads_string = reads_str,
                            ref = rsemIndexPath,
                            sampleName = sampleName)
        
    return alignment_cmd

def get_reads_string(readPaths):
    # make reads string
    reads_str = ''
    read1_str, read2_str = '', ''
    for files in readPaths:
        read1_str += (files[0] + ',')
        if len(files) == 2:
            read2_str += (files[1] + ',')

    paired=''
    if read2_str != '': # paired end
        paired="--paired-end"

    reads_str=' '.join([paired, read1_str.rstrip(','), read2_str.rstrip(',')])
    
    return reads_str
    

def make_dge_script(opt):
    
    rsem_mat_cmd = ' "{rsem}/rsem-generate-data-matrix {result_list} > {counts_file}"\n'
    
    # rsem-find-DE is decaptated in rsem-1.2.7 replaced by rsem-run-ebseq and rsem-control-fdr
    #rsem_dge_cmd = ' "{rsem}/rsem-find-DE {counts_file} {num} {FDR_rate} {output}"\n'
    
    rsem_isoforms_ebseq = ' "{rsem}/rsem-run-ebseq --ngvector {ngvector} {counts_file} {trt1_no},{trt2_no} {isoform_DE_results}"\n'
    rsem_gene_ebseq = ' "{rsem}/rsem-run-ebseq {counts_file} {trt1_no},{trt2_no} {gene_DE_results}"\n'
    
    log_path = os.path.join(opt.outputPath, 'log')
    aln_path = os.path.join(opt.outputPath, 'rsem_alignment')
    
    dge_cmd = '\n## ==== Differential gene expression analysis ==== ##\n'
    # walk through comparisons need to make
    for comparison in opt.comparisons:
        if len(comparison) == 2:
            trt1, trt2 = comparison
        else:
            print "ERROR: need two treatments for differential gene expression analysis."
            print "ERROR: treatments {} specified.".format(" - ".join(comparison))
            continue
        
        # create the output directory
        dirname = "DGE_{}_vs_{}".format(trt1, trt2)
        opath = os.path.join(opt.outputPath, dirname)
        dge_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = opath)
        dge_cmd += "cd {}\n".format(opath)
        
        # setup the matrix file
        for feature in ['genes', 'isoforms']:
            # make a list of samples
            result_list = []
            samples=sorted(opt.treatments[trt1]) + sorted(opt.treatments[trt2])
            for sample in samples:
                result = "rsem_alignment/{s}/{s}.{ftr}.results".format(s=sample, ftr=feature)
                result_list.append(os.path.join(opt.outputPath, result))
            # the output file 
            matrix_fn = os.path.join(opath, "{}.counts.matrix".format(feature))
            
            # hold for alignment jobs
            hold_option = '-hold_jid '
            for sample in samples:
                hold_option += 'aln_%s,' % (sample,)
            hold_option = hold_option.rstrip(',')
            matrix_jid = "{}_cnt_{}_vs_{}".format(feature, trt1, trt2)
            dge_cmd += sub_cmd.format(queue = opt.queue,
                            job   = matrix_jid,
                            log   = os.path.join(log_path, '%s.log' % (matrix_jid,)),
                            mem = "4G",
                            options = hold_option)
            dge_cmd += ' "{rsem}/rsem-generate-data-matrix {s_list} > {output}"\n'.format(
                        rsem=opt.rsem, s_list=' '.join(result_list), output=matrix_fn)
            
            # collect parameters for the DGE calculation
            
            dge_fn = os.path.join(opath, "DE_{}_{}_vs_{}.list".format(feature, trt1, trt2))
            ebseq_jid = "{}_eb_{}_vs_{}".format(feature, trt1, trt2)

            if feature == "genes":
                dge_cmd += sub_cmd.format(queue = opt.queue,
                            job   = ebseq_jid,
                            log   = os.path.join(log_path, '%s.log' % (ebseq_jid,)),
                            mem = '4G',
                            options = '-hold_jid %s' % (matrix_jid,))
                dge_cmd += ' "{rsem}/rsem-run-ebseq {counts_file} {trt1_no},{trt2_no} {output}"\n'.format\
                    (rsem=opt.rsem,
                     counts_file = matrix_fn,
                     trt1_no = len(opt.treatments[trt1]),
                     trt2_no = len(opt.treatments[trt2]),
                     output = dge_fn
                     )
            elif feature == "isoforms":
                dge_cmd += sub_cmd.format(queue = opt.queue,
                            job   = ebseq_jid,
                            log   = os.path.join(log_path, '%s.log' % (ebseq_jid,)),
                            mem = '4G',
                            options = '-hold_jid %s,%s' % (matrix_jid,"rsemNgvector"))
                dge_cmd += ' "{rsem}/rsem-run-ebseq --ngvector {ngvector} {counts_file} {trt1_no},{trt2_no} {output}"\n'.format\
                    (rsem=opt.rsem,
                     ngvector = os.path.join(opt.refPath, "RSEMIndex", "genome.transcripts.ngvec") ,
                     counts_file = matrix_fn,
                     trt1_no = len(opt.treatments[trt1]),
                     trt2_no = len(opt.treatments[trt2]),
                     output = dge_fn
                     )
            
    return dge_cmd


def make_exp_table(opt):
    """
    Create expression table from the each sample's expression and the differential expression list
    """
    
    merge_exp_cmd = os.path.join(script_dir, 'merge_expression_table.py') + " {dge_path} {out_path} {num}\n"
    log_path = os.path.join(opt.outputPath, 'log')    
    exp_tbl_cmds = '\n## ==== Generate expression summary table ==== ##\n'
    for p in opt.dge_paths:
        # comparison pair:
        comp = p.split("DGE_")[-1]
        trt1, trt1 = comp.split('_vs_')
        
        # hold for EBseq jobs
        hold_option = '-hold_jid '
        for feature in ['genes', 'isoforms']:
            hold_option += "{f}_eb_{c},".format(f = feature, c = comp )
        hold_option = hold_option.rstrip(',')
        exp_tbl_jid = "exp_tbl_{}".format(comp)
        
        # SGE submission command        
        # add qsub portion
        exp_tbl_cmds += sub_cmd.format(queue = opt.queue,
                            job   = exp_tbl_jid,
                            log   = os.path.join(log_path, '%s.log' % (exp_tbl_jid,)),
                            mem='2G',
                            options = hold_option)
        # add merge_exp_table script portion
        exp_tbl_cmds += merge_exp_cmd.format(dge_path = p, out_path = p, num = len(opt.treatments[trt1]) )
    return exp_tbl_cmds


def make_delivery(opt):
    delivery_cmd = '\n## ==== Making delivery ==== ##\n'
    
    # copy alignment bam files
    alignment_delivery_folder = os.path.join(opt.deliveryPath, 'alignment', 'bam')
    delivery_cmd += 'if [ ! -d "{dest}" ]; then mkdir -p {dest}; fi\n'.format(dest=alignment_delivery_folder)

    aln_path = os.path.join(opt.outputPath, 'rsem_alignment')
    delivery_cmd += "cd {p}\n".format(p = aln_path)
    delivery_cmd += "for i in *; do echo 'copying $i alignment ...'; cp $i/$i.genome.sorted.bam* {p}; done\n".format(p = alignment_delivery_folder)
    delivery_cmd += "cd -\n"
    
    # create IGV seassion files
    for comparison in opt.comparisons:
        if len(comparison) == 2:
            trt1, trt2 = comparison
        else:
            print("ERROR in comparison pair!")
        delivery_cmd += "{cmd} {genome} {sample_list} {output_script_name}\n".format(\
            cmd = os.path.join(script_dir, "create_igv_session.py"),
            genome = opt.IGV_genome,
            sample_list = ','.join(opt.treatments[trt1]+opt.treatments[trt2]),
            output_script_name = os.path.join(opt.deliveryPath, 'alignment', "IGV-%s_vs_%s.xml" % (trt1, trt2))
            )
    
    # copy expression files
    for comparison in opt.comparisons:
        if len(comparison) == 2:
            trt1, trt2 = comparison
        else:
            print("ERROR in comparison pair!")
        # source file = project output + DGE_folder + csv file
        src_file = os.path.join(opt.outputPath, "DGE_{t1}_vs_{t2}".format(t1=trt1, t2=trt2),
                    "DE_{ftr}_{msr}.csv".format(ftr=opt.feature, msr = opt.measurement))
        # dest file = delivery folder + DE_of_comparison.csv
        dest_file = os.path.join(opt.deliveryPath, "DE_{ftr}_{msr}_{t1}_vs_{t2}.csv".format(\
            ftr=opt.feature, msr = opt.measurement,t1=trt1, t2=trt2))
        
        delivery_cmd += "cp {src} {dest}\n".format(src=src_file, dest=dest_file)
        
    # create plots for probability and scatter plot
    
    return delivery_cmd

def rsem_path(opt, script_fn):
    # make bash script for mRNAseq run
    f_out = open(script_fn, 'w')
    f_out.write(make_aln_script(opt) + '\n')
    f_out.write(make_dge_script(opt) + '\n')
    f_out.write(make_exp_table(opt) + '\n')
    #f_out.write(make_delivery(opt) + '\n')
    f_out.close() 
    
    # make delivery script
    f_out = open(script_fn.replace("_run.sh", "_deliver.sh"), 'w')
    f_out.write(make_delivery(opt))
    f_out.close()
