#!/usr/bin/env python
__author__ = "Xiaoyu Liu"
__email__ = "liux@nbio.info"
__copyright__ = "Copyright (C) 2016 Xiaoyu Liu"
__status__ = "development"
__license__ = "Public Domain"
__version__ = "0.1"

from jinja2 import Template
import os
import pandas as pd
import begin

import sys
sys.path.append("..")


def report_txt(goseq_inputs, output = None):
    file_list = list(goseq_inputs)
#        summarize how many pathways are enriched

    table_content = []
    for fn in file_list:
        comp, pa_table = os.path.basename(fn).split('.')[:2]
        comp     = comp.replace('_vs_', ' vs. ')
        pa_table = pa_table.replace('_', ' ')

        # count number of pathways been enriched
        num_pa = open(fn).read().count('\n') - 1

        # make table
        row = [comp, pa_table, num_pa]
        table_content.append(row)

    # write DE summary table
    table_df = pd.DataFrame(table_content, columns=["Comparison", "Pathways", "Enriched"])
    if output:
        table_df.to_csv(output, sep="\t", index=False)
    else:
        return table_df

def report_xls(goseq_inputs, output):
    file_list = list(goseq_inputs)

    # get all txt files in one excel file
    xls_writer = pd.ExcelWriter(output, engine="xlsxwriter")
    pd.read_table(output.txt).to_excel(xls_writer, index=False, sheet_name='Summary')

    workbook = xls_writer.book
    # Add a format. Light red fill with dark red text.
    over_fmt = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    # Add a format. Green fill with dark green text.
    under_fmt = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})
    float_fmt = workbook.add_format({'num_format': '0.000'})

    for fn in file_list:
        comp, pa_table = os.path.basename(fn).replace("_", " ").split('.')[:2]
        sh_name = comp[:25] + ' ' + pa_table.replace("GO Biological Process", "GO BP")\
                                        .replace("GO Cellular Component", "GO CC")\
                                        .replace("GO Molecular Function", "GO MF")\
                                        .replace("KEGG pathway","KEGG")

        df = pd.read_table(fn)
        number_rows = len(df.index)
        df.to_excel(xls_writer, startrow=1, index=False, sheet_name=sh_name)

        # format cells
        worksheet = xls_writer.sheets[sh_name]
        worksheet.set_header(comp + ' ' + pa_table )
        worksheet.set_column('A:A', 12)
        worksheet.set_column('F:F', 40)
        worksheet.set_column('G:G', 100)
        worksheet.set_column('D:E', 12, float_fmt)

        worksheet.conditional_format("D3:D{}".format(number_rows +1),
                                     {'type': 'cell',
                                         'criteria': '<',
                                         'value': 0.05,
                                         'format': over_fmt})
        worksheet.conditional_format("E3:E{}".format(number_rows +1),
                                     {'type': 'cell',
                                         'criteria': '<',
                                         'value': 0.05,
                                         'format': under_fmt})
    xls_writer.save()

def report_html(goseq_inputs, output):
    html_template = Template("""
<div onchange="displayTable(null);">
    <select id="tableSelect" class="form-control">
		<option>Select a table</option>
		{% for exp, ctrl, pa, tbl in exp_ctrl_tbl %}
		<option value="tab-{{ loop.index }}">{{ exp }} vs. {{ ctrl }} {{ pa }}</option>
		{% endfor %}
	</select>
</div>
<hr/>
<div class='grid'>
    {% for exp, ctrl, pa, tbl in exp_ctrl_tbl %}
    <div id='tab-{{ loop.index }}' style="display:none"><h2>{{ exp }} vs. {{ ctrl }} {{ pa }}</h2>
	    {{ tbl }}
	    <hr/>
	</div>
    {% endfor %}
</div>


    <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.css" type="text/css" />
    <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.2.min.js"></script>

    {{ grid_js }}

    """)
    file_list = list(goseq_inputs)
    table_df = report_txt(goseq_inputs)
    # add links to the gene table
    table_df['Enriched'] = '<a href="#tab-' + (table_df.index + 1).map(str) + '">' + table_df['Enriched'].map(str) +'</a>'
    table_df = table_df.set_index(["Comparison", "Pathways"])
    # make html table
    summary_html = table_df.to_html(classes="table table-bordered table-hover", escape=False, index=True)

    grid_js, pa_divs = table_to_html(file_list)
    # The tabbed interface is templated from http://www.w3.org/Style/Examples/007/target.en.html#tab1

    exp_lst_rep = [ i for i in expGrp_lst for rep in range(len(PA_TABLES))] # repeat exp for # of pa_tables
    ctrl_lst_rep = [ i for i in ctrlGrp_lst for rep in range(len(PA_TABLES))] # same for ctrl
    pa_tbl_rep = [ i for rep in range(len(expGrp_lst)) for i in PA_TABLES]   # and for pa_tables

    pa_html = html_template.render(exp_ctrl_tbl=zip(exp_lst_rep, ctrl_lst_rep, pa_tbl_rep, pa_divs),
                                    grid_js=grid_js,
                                    exp_ctrl = zip(expGrp_lst, ctrlGrp_lst),
                                    pa_table=  PA_TABLES )
    with open(output, 'w') as f_out:
        #write out summary table
        f_out.write("""
        <div class="table-responsive">
        {}
        </div>
        {}
        """.format(summary_html, pa_html) )


@begin.start
def run(html='default', txt='default', xls='default', config_file="run_config.json", *tables):
    write_html, write_txt, write_xls = False, False, False
    if html=='default' and txt=='default' and xls=='default': # none output option is define, then output all
        write_html, write_txt, write_xls = True, True, True
        html = "pathway/pathway_report.html"
        txt  = "pathway/pathway_report.txt"
        xls  = "pathway/GeneSetEnrichment.xlsx"
    else:
        if html != 'default':
            write_html = True
        if txt  != 'default':
            write_txt  = True
        if xls  != 'default':
            write_xls  = True

    if write_html:
        report_html(tables, html)
    if write_txt:
        report_txt(tables, txt)
    if write_xls:
        report_xls(tables, xls)