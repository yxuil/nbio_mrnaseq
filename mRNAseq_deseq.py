#!/mnt/grl/software/epd/bin/python


import os, sys
sub_cmd="qsub -V -cwd -j y -b y -q {queue} -N {job} -o {log} -l vf={mem} {options} "
email = "-m abe -M {email}"

def make_star_script(opt):
    star_aln_cmd = '"{star}/STAR --genomeDir {star_ref} --readFilesIn {reads_string} --runThreadN {thread} --outSAMunmapped Within {gunzip}"\n'
    alignment_cmd = ''
    # create folders
    temp_aln_path = os.path.join(opt.outputPath, 'star_alignment')
    aln_path = os.path.join(opt.outputPath, 'alignment')
    
    
    for pth in [temp_aln_path, aln_path]:
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = pth)
        
    # alignment
    for sampleName, readPaths in opt.samplePath.items():
        # create alignment output directory if not exist
        temp_sample_aln_dir = os.path.join(temp_aln_path, sampleName)
        sample_aln_path = os.path.join(aln_path, sampleName)
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = temp_sample_aln_dir)
        alignment_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = sample_aln_path)
        alignment_cmd += 'cd {}\n'.format(temp_sample_aln_dir)
        
        gunzip_option = ""
        readfile_str = ""
        for readlist in readPaths:
            readfile_str = ' '.join(readlist)
            for readfile in readlist:
                if readfile.strip().endswith('.gz'):
                    gunzip_option = "--readFilesCommand zcat"        
        
                    gunzip_option = ""
                    readfile_str = ""
                    for readlist in readPaths:
                        readfile_str = ' '.join(readlist)
                        for readfile in readlist:
                            if readfile.strip().endswith('.gz'):
                                gunzip_option = "--readFilesCommand zcat"        

        # make reads string
        reads_str = ''
        read1_str, read2_str = '', ''
        hold_option = '-hold_jid '
        for readLists in readPaths:
            if '.gz' in readLists[0]: # need to uncompress the reads file
                gunzip_option = "--readFilesCommand zcat"
            
            # add the Read1 file to the list
            read1_str += (readLists[0] + ',')
            
            # add the Read2 file to the file
            if len(readLists) == 2:
                # ** assuming the pair should be in the same format **
                #if '.gz' in readLists[1]: gunzip_option = "--readFilesCommand zcat"
                read2_str += (readLists[1] + ',')
    
        # Does STAR work with single or paired reads inplicitly?
        reads_str=' '.join([read1_str.rstrip(','), read2_str.rstrip(',')])
        
        # alignment command
        option = ''
        alignment_cmd += sub_cmd.format(queue = opt.queue,
                            job   = 'aln_%s' % (sampleName,),
                            log   = os.path.join(sample_aln_path, 'aln_%s.log' % (sampleName,)),
                            #email = opt.email,
                            mem = opt.max_mem,
                            options = option)
        
        alignment_cmd += star_aln_cmd.format(star = opt.star,
                            star_ref = os.path.join(opt.refPath , "STARIndex"),
                            reads_string = reads_str,
                            thread = opt.thread,
                            gunzip = gunzip_option)
        
        
        # exit the folder
        alignment_cmd += "cd ..\n"
    return alignment_cmd

def make_bam_script(opt):
    samtools_cmd = '"{samtools}/samtools view -bS {sam} | samtools sort -m 4000000000 - {sorted_bam}"\n'
    script_cmd = ''
    
    # input sam file path
    temp_aln_path = os.path.join(opt.outputPath, 'star_alignment')
    
    # output bam file path
    aln_path = os.path.join(opt.outputPath, 'alignment')    
    script_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = aln_path)
        
    # convert, sort, index bam files
    for sampleName in opt.samples:
        
        temp_sample_aln_dir = os.path.join(temp_aln_path, sampleName)
        
        # create alignment output directory if not exist
        sample_aln_path = os.path.join(aln_path, sampleName)
        script_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = sample_aln_path)
        
        # covert to sorted bam and index the bam
        hold_option = '-hold_jid aln_{}'.format(sampleName)
        script_cmd += sub_cmd.format(queue = opt.queue,
                                    job   = 's2bam_%s' % (sampleName,),
                                    log   = os.path.join(sample_aln_path, 'aln_%s.log' % (sampleName,)),
                                    #email = opt.email,
                                    mem = "4G",
                                    options = hold_option)      
        script_cmd += samtools_cmd.format(samtools = opt.samtools,
                                     sam = os.path.join(temp_sample_aln_dir, "Aligned.out.sam"),
                                     sorted_bam = os.path.join(sample_aln_path, "sorted") )
        
        # index sorted bam file
        hold_option = '-hold_jid aln_{}'.format(sampleName)
        script_cmd += sub_cmd.format(queue = opt.queue,
                                    job   = 'index_%s' % (sampleName,),
                                    log   = os.path.join(sample_aln_path, 's2bam_%s.log' % (sampleName,)),
                                    #email = opt.email,
                                    mem = "4G",
                                    options = hold_option)     
        script_cmd += "{samtools}/samtools index {bam} \n".format(samtools = opt.samtools,
                                bam = os.path.join(sample_aln_path, "sorted.bam") )    
    
    return script_cmd


def make_count_script(opt):
    count_cmd = '"{htseq} -s no -a 10 {sam} {gtf} > {count}"\n'
    script_cmd = ''
    
    # imput sam file path
    temp_aln_path = os.path.join(opt.outputPath, 'star_alignment')
    
    # coutput count file folder
    cnt_path = os.path.join(opt.outputPath, 'raw_count')
        
    # count
    for sampleName in opt.samples:
        # imput sam file
        sam_fn = os.path.join(temp_aln_path, sampleName, "Aligned.out.sam")
        
        # create  output directory if not exist
        sample_cnt_path = os.path.join(cnt_path, sampleName)
        script_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = sample_cnt_path)
        
        hold_option = '-hold_jid aln_{}'.format(sampleName)
        script_cmd += sub_cmd.format(queue = opt.queue,
                            job   = 'cnt_%s' % (sampleName,),
                            log   = os.path.join(sample_cnt_path, 'cnt_%s.log' % (sampleName,)),
                            #email = opt.email,
                            mem = "4G",
                            options = hold_option)
        if os.path.exists(os.path.join( opt.refPath, "annotation", "genes_cleaned.gtf")):
            preferred_gtf = os.path.join( opt.refPath, "annotation", "genes_cleaned.gtf")
        elif os.path.exists(os.path.join( opt.refPath, "annotation", "genes.gtf")):
            preferred_gtf = os.path.join( opt.refPath, "annotation", "genes.gtf")
        else: # FIX this
            preferred_gtf = os.path.join( opt.refPath, "annotation", "*.gtf")
        script_cmd += count_cmd.format( htseq = opt.htseq,
                            sam = sam_fn,
                            gtf = preferred_gtf,
                            count = os.path.join(sample_cnt_path, 'count.txt'))

    return script_cmd    


def make_deseq_script(opt):   
    deseq_cmd = ''
    for sampleName in opt.samples:
        # input count file
        cnt_fn = os.path.join(opt.outputPath, 'raw_count', sampleName, 'count.txt')
        
        # output folder
        dge_path = os.path.join(opt.outputPath, 'DGE', sampleName)
        deseq_cmd += 'if [ ! -d "${path}" ]; then mkdir -p {path}; fi\n'.format(path = dge_path)
        

def deseq_path(opt, script_fn):
    script = ''
    script += make_star_script(opt)
    
    #return script
    f_out = open(script_fn, 'w')
    #f_out.write( make_star_script(opt) )
    #f_out.write( make_bam_script(opt) )
    f_out.write( make_count_script(opt) )
    f_out.close()
    
    call_cmd = (sub_cmd+email).format(queue = opt.queue, job = os.path.basename(script_fn), 
                             log = os.path.join(opt.outputPath, script_fn+'.log'),
                             options = '',
                             mem = "2G",
                             email = opt.email)
    call_cmd = call_cmd.split(" ") + ['sh', script_fn]
    
    print ' '.join(call_cmd)
    
    