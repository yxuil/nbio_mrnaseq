#!/mnt/grl/software/epd-7.3-2/bin/python
from jinja2 import Template
import sys

xml_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Session genome="{{ genome }}">
    <Resources>
      {% for sample in samples %}
        <Resource path="./bam/{{ sample }}.genome.sorted.bam"/>
      {% endfor %}
    </Resources>
    
    {% for sample in samples %}
    <Panel height="{{ panel_height }}" name="panel_{{ sample }}" width="{{ panel_width }}">
        <Track altColor="0,0,178" autoScale="true" color="175,175,175" colorScale="ContinuousColorScale;0.0;52.0;255,255,255;175,175,175" 
        displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" 
        id="./bam/{{ sample }}.genome.sorted.bam_coverage" 
        name="{{ sample }} Coverage" showDataRange="true" visible="true">
            <DataRange baseline="0.0" drawBaseline="true" flipAxis="false" maximum="100.0" minimum="0.0" type="LINEAR"/>
        </Track>
        <Track altColor="0,0,178" color="0,0,178" colorOption="READ_STRAND" displayMode="EXPANDED" 
        featureVisibilityWindow="-1" fontSize="10" 
        id="./bam/{{ sample }}.genome.sorted.bam" 
        name="{{ sample }} alignment" showDataRange="true" sortByTag="" visible="true"/>
    </Panel>
    {% endfor %}
    
    {% if annotation !="" %}
    <Panel height="98" name="FeaturePanel" width="{{ panel_width }}">
        <Track altColor="0,0,178" color="0,0,178" displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" id="Reference sequence" name="Reference sequence" showDataRange="true" sortable="false" visible="true"/>
        <Track altColor="0,0,178" color="0,0,178" displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" height="45" id="{{ annotation }}" name="annotation" renderer="GENE_TRACK" showDataRange="true" sortable="false" visible="true" windowFunction="count"/>
    </Panel>
    {% endif %}
    
    
    <PanelLayout dividerFractions="{{ divider_frac }}"/>
</Session>
'''
def make_IGV_session(genome, samples, output_filename, annotation = ""):
    
    var = {'samples': samples,
           'genome': genome,
           "panel_height": 800/len(samples),
           "panel_width": 1000,
           "divider_frac": ','.join(map(str, frange(0.02, 0.9, 0.88 / len(samples)))),
           "annotation": annotation
           }


    xml = Template(xml_template).render(var)
    f_out = open(output_filename, 'w')
    f_out.write(xml)
    f_out.close()

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump
    
if __name__ == '__main__':
    USAGE = "Usage: {} genome sample1[,sample2,...] bam1[,bam2,...] output_filename".format(sys.argv[0])
    if len(sys.argv) < 5:
        print USAGE
        exit()
    else:
        make_IGV_session(sys.argv[1], sys.argv[2].split(','), sys.argv[3].split(','), sys.argv[4])
        
if False:
    from glob import glob
    print "Usage {} option_file".format(sys.argv[0])
    ori_path = sys.argv[2]
    dest_path = sys.argv[3]
    for p in glob(ori_path + "/DGE_*"):
        pass
        
    

