#!/mnt/grl/software/epd/bin/python
'''
format DGE results
'''
import pandas as pd
import matplotlib.pyplot as plt
from runconfig import run_options

runconfig_fn = sys.argv[1]
opt = run_options(runconfig_fn)

def update_csv(opt):
    '''
    update csv file: add mean expression; log2 FC; 
    add addition csv file according to the cretira
    '''
    csv_fn = 'DE_{feature}_{measurement}.csv'.format(feature=opt.measured_feature, measurement=opt.measurement)
    
tpm = pd.read_csv('DE_genes_tpm.csv', index_col=[0])
tpm['control'] = tpm.ix[:, 1:4].mean(axis = 1)
tpm['affected'] = tpm.ix[:, 4:7].mean(axis = 1)
tpm.FC = 1/tpm.FC
cols = ['transcript_id(s)', '10862', '10931', '10955', 'control',  
        '10706', '10875', '11304', 'affected', 'Probability', 'FC' ]
tpm = tpm[cols]


# <codecell>

# read gene_id <-> gene_name mapping from the GTF file and add to the table
f_in = open( "/mnt/grl/genomes/Felis_catus/ENSEMBL_felis_catus_6.2.74/annotation/genes_chr_only.gtf", 'r')
genenames = {}
for line in f_in:
    fields = line.strip().split('\t')
    anno = fields[-1]
    anno = anno.replace('"', '').replace("'", "")
    anno = map(str.strip, anno.split(';'))
    anno = map(str.split, anno)
    anno = dict([i for i in anno if i != []])
    if anno['gene_id'] not in genenames :
        if 'gene_name' in anno : genenames[anno['gene_id']] = anno['gene_name']
        else: genenames[anno['gene_id']] = ''
gnames = pd.Series(genenames, name='gene_name')
gnames.index.name='gene_id'
tpm['gene_name'] = gnames
tpm[:3]

# <codecell>


fig=pyplot.figure(figsize=(18,6))
ax = fig.add_subplot(131)
tpm.Probability.hist(bins = 100)
ax.set_xlabel("DE Probablity")
ax.set_ylabel("Frequency")
ax.set_title("Probability Distribution")

ax = fig.add_subplot(132)
line = ax.scatter(x = (tpm.control+0.5), y = (tpm.affected +0.5), alpha = 0.1, linewidths=0, s = 4)
ax.set_xscale('log')
ax.set_xlabel('Control')
ax.set_xlim(0.4, 100000)
ax.set_ylim(0.4, 100000)
ax.set_ylabel('Affected')
ax.set_yscale('log')
ax.set_title("scatter plot")

ax = fig.add_subplot(133)
line = ax.scatter(x = log2(tpm.FC), y = -log10(1-tpm.Probability), alpha = 0.1, linewidths=0, s=4)
ax.set_ylim(-0.01, 2.2)
ax.set_ylabel('-log10(1-probability)')
ax.set_xlabel('log2FC')
ax.set_title("Volcano plot")
fig.savefig('plots.png')

# <codecell>

tpm.to_csv('gene_expression.csv', float_format='%.2f')

# <codecell>

genes_up = tpm[ (tpm.Probability >=0.95) & (log2(tpm.FC) >= 1)]
print len(genes_up)
genes_up.to_csv('genes_overexpressed.csv', float_format='%.2f')

# <codecell>

genes_down = tpm[ (tpm.Probability >=0.95) & (log2(tpm.FC) <= -1)]
print len(genes_down)
genes_down.to_csv('genes_underexpressed.csv', float_format='%.2f')

# <codecell>

genes_significant = tpm[ (tpm.Probability >=0.95)]
print len(genes_significant)
genes_significant.to_csv('genes_differentialExpressed.csv',  float_format='%.2f')

# <codecell>

!mkdir -p /mnt/grl/agar/users/Duncan/projects/rt223
!cp *.csv /mnt/grl/agar/users/Duncan/projects/rt223
!mkdir -p /mnt/grl/agar/users/Duncan/projects/rt223/alignment
!cp ../rsem_alignment/*/*.genome.sorted.bam* /mnt/grl/agar/users/Duncan/projects/rt223/alignment
!cp /mnt/grl/genomes/Felis_catus/ENSEMBL_felis_catus_6.2.74/genome.fa* /mnt/grl/agar/users/Duncan/projects/rt223/alignment
# open and save IGV session in IGV

# <codecell>

pwd

# <codecell>


