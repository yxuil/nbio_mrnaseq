#!/mnt/grl/software/epd/bin/python
from runconfig import run_options
from mRNAseq_deseq import deseq_path
from mRNAseq_rsem import rsem_path
from subprocess import call

import os, sys

sub_cmd="qsub -V -cwd -j y -b y -q {queue} -N {job} -o {log} {options} -m abe -M {email}"

USAGE = "Usage: {} run_config_file [script_output]".format(sys.argv[0])
if len(sys.argv) < 2:
    print USAGE
    exit()
else:
    runconfig_fn = sys.argv[1]
    opt = run_options(runconfig_fn)
    #script_fn = "run_{}_mRNAseq.sh".format(opt.projID) if len(sys.argv) == 2 else sys.argv[2]
    
    base_dir = os.path.dirname(runconfig_fn)
    base_fn  = os.path.basename(runconfig_fn)
    
    script_fn = os.path.join(base_dir, base_fn.rstrip('.txt').rstrip("_config") + "_run.sh")
    
    if opt.workflow == "deseq":
        deseq_path(opt, script_fn)
    elif opt.workflow == "rsem":
        rsem_path(opt, script_fn)
    elif opt.workflow == "trinity":
        pass
    else:
        print 'workflow "{}" does not exist. Only "rsem" "deseq" and "guided" are valid workflow option'.format(opt.workflow)
        print USAGE