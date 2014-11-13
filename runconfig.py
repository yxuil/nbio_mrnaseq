#!/mnt/grl/software/epd/bin/python

from ConfigParser import SafeConfigParser
import os

class run_options:
    '''The class with mRNAseq run options'''
    def __init__(self, filename):
        parser = self.read_runconfig(filename)
        self.parse_options(parser)        
    
    def read_runconfig(self, filename):
        parser = SafeConfigParser()
        parser.optionxform=str
        parser.read(filename)
        return parser
    
    def parse_options(self, parser):
        # [runInfo]
        self.projName=parser.get('runInfo', 'projName')
        self.projDetail = parser.get('runInfo', 'projDetail')
        self.projType = parser.get('runInfo', 'projType')
        self.PI = parser.get('runInfo', 'PI')
        self.projID = parser.get('runInfo', 'projID')
        self.projPI = parser.get('runInfo', 'projPI')
        self.email = parser.get('runInfo', 'email')
        self.thread = parser.get('runInfo', 'thread') if parser.has_option('runInfo', 'thread') else 1
        self.max_mem = parser.get('runInfo', 'max_mem') if parser.has_option('runInfo', 'max_mem') else '2G'
        self.queue = parser.get('runInfo', 'queue') if parser.has_option('runInfo', 'queue') else "brchigh.q"
        self.IGV_genome = parser.get('runInfo', 'IGV_genome')
        
        # [delivery]
        self.workflow = parser.get('delivery', 'workflow')
        self.feature = parser.get('delivery', 'feature') if parser.has_option('delivery', 'feature') else "genes"
        self.measurement = parser.get('delivery', 'measurement')
        
        # [dataPath]
        self.refPath = parser.get('dataPath', 'refPath')
        self.outputPath = parser.get('dataPath', 'outputPath')
        self.deliveryPath= parser.get('dataPath', 'deliveryPath')
        
        # [toolInfo]
        self.samtools = parser.get('toolInfo', 'samtools')
        self.bedtools = parser.get('toolInfo', 'bedtools')
        self.htseq = parser.get('toolInfo', 'htseq')
        self.rsem = parser.get('toolInfo', 'rsem')
        self.star = parser.get('toolInfo', 'star')
        self.bowtie = parser.get('toolInfo', 'bowtie')
        
        # [sampleInfo]
        treatment_list = map(str.strip, parser.get('sampleInfo', 'treatments').split(','))
        self.fdr=parser.get('sampleInfo', 'fdr')
        # samples
        self.treatments = {}
        self.samples = []
        self.samplePath = {}
        for trt in treatment_list:
            self.treatments[trt] = map(str.strip, parser.get('sampleInfo', trt).split(','))
            # sample path
            for sample in self.treatments[trt]:
                self.samples.append(sample)
                self.samplePath[sample] = []
                p=[a.strip() for a in parser.get('dataPath', sample).split(';') if a.strip() != '']
                for reads_path in p:
                    self.samplePath[sample].append((map(str.strip,reads_path.split(','))))
        
        # somparisons
        self.comparisons = []
        compList = map(str.strip, parser.get('sampleInfo', 'comparisons').split(','))
        for compareson in compList:
            self.comparisons.append(map(str.strip, compareson.split('-')))
            
        # inferred path
        self.aln_path = os.path.join(self.outputPath, 'alignment')   
        self.dge_paths = [self.get_dge_path(a,b) for a, b in self.comparisons]
        
    def get_dge_path(self, treatment1, treatment2):
        return os.path.join(self.outputPath, "DGE_{}_vs_{}".format(treatment1, treatment2))

            
