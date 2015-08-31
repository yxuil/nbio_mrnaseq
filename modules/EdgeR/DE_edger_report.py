#!/usr/bin/env python
import imp

# from utilities.py import table_to_grid, table_to_html

def edger_report(config, output):
    """
    :param config: run configuration file that contains group, sample information
    :param output: output prefix for saving file
    :return:
    """
    header = "Comparison,Condition1,Condition2,Total Expressed Genes,DE Genes".split(',')
    table_content  = []

    # gene table file list
    file_list = []
    for cmp in config["comparisons"]:
        condition1, condition2 = map(lambda x: str(x).strip(), cmp.split(":")) # split cmp and strip whitespace
        fn = "diff_expr/{}_vs_{}.gene.diffexpr.txt".format(condition1, condition2)
        file_list.append(fn)
        with open(fn) as f_in:
            line_count = sum(1 for _ in f_in)  # _ is a throwaway variable
        total_gene = line_count - 1            # remove the header line

        fn = "diff_expr/{}_vs_{}.gene.onlyDE.txt".format(condition1, condition2)
        with open(fn) as f_in:
            line_count = sum(1 for _ in f_in)
        de_gene = line_count - 1
        table_content.append([cmp, config["treatments"][condition1], config["treatments"][condition2], total_gene, de_gene])
    
    # write DE summary table
    table_df = pd.DataFrame([i[1:] for i in table_content], columns=header[1:], index=[i[0] for i in table_content ])
    table_df.index.name = header[0]
    table_df.to_csv(output + ".txt", sep="\t", index=False)
    
    # write gene table
    grid_js, gt_divs = table_to_html(file_list)
    with open(output + ".html", 'w') as f_out:
        f_out.write(table_df.to_html(classes="brc", escape=False))
        for comp, gt_div in zip (config["comparisons"], gt_divs):
            f_out.write('\n<div id="genetable">\n<p>Gene table for comparison between {} </p>\n{}\n</div>\n'.format(comp, gt_div))

        f_out.write(grid_js + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: {} <run_config> <output_prefix>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    edger_report(config, sys.argv[2])
