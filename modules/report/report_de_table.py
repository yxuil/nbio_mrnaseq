#!/usr/bin/env python
__author__ = 'liu'

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform, output_notebook
from bokeh.embed import components

import pandas as pd

def table_to_grid(table_fn, width = 800, height = 280):
    grid = []
    for fn in table_fn:
        data = pd.read_table(fn)
        data.columns=["Gene"] + list( data.columns[1:])
        source = ColumnDataSource(data)
        columns = [ TableColumn(field= a, title= a) for a in data.columns ]
        data_table = DataTable(source=source, columns=columns, width=width, height=height)
        grid.append(data_table)
    return grid

def table_to_html(table_fn, width = 800, height = 280):
    grid = table_to_grid(table_fn, width, height)
    script, divs = components(grid)
    return(script, divs)

if __name__ == "__main__":
    """take a list of txt file in tabular format and turn into slickgrid HTML.
    """
    import os, sys
    from glob import glob

    if len(sys.argv) > 1:
        fn_list = sys.argv[1:]
    else:  #find txt file in current folder
        fn_list = glob("./*.txt")

    # crate the clickgrid scripts
    source = table_to_html(fn_list)
    html = source[0]
    html +=  "<p>\n".join(source[1])

    print(html)