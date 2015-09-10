"""Usage: goseq.py [-g genome] [-i id_type] [-o output_prefix] [-t temp_dir] <FILE>...

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  FILE        required input file(s) contain the gene DE call list.
              It must be tab delimited two column file: first column is gene name; the second is DE calls.
              Use 1, yes, true for DE genes; 0, no, false, of empty for non DE genes.

Options:
  -h --help
  -g <genome> --genome <genome>     genome name (goseq supported) [default: hg19]
  -i <id_type> --id <id_type>       ID type of the gene identifier [default: geneSymbol]
  -p <p> --pvalue <p>               FDR value for reporting the pathway [default: 0.25]
  -o <DIR> --output <DIR>           output prefix [default: goseq_result]
  -t <temp> --temp <temp>           temporary directory [default: ./temp]

"""
from docopt import docopt
import pandas as pd
import rpy2

PA_TABLES = ['KEGG_pathway', 'GO_Biological_Process', 'GO_Molecular_Function','GO_Cellular_Component']

GOSEQ = """
sig_threshold = {sig}
library(goseq)
library(GO.db)
library(KEGG.db)

# all_genes = read.table("diff_expr/{comparison}.gene.diffexpr.txt", header=TRUE, sep='\\t', row.names=1)
# de_genes = read.table("diff_expr/{comparison}.gene.onlyDE.txt", header=TRUE, sep='\\t', row.names=1)
genes = read.table({de_file}, header=FALSE, sep='\\t', row.names=1)
genes = as.integer(genes)
# genes = as.integer( row.names(all_genes) %in% row.names(de_genes))
# names(genes)=row.names(all_genes)

# crate pwf table
pwf=nullp(genes,"{genome}","{ID_type}", plot.fit=FALSE)

# GO analysis
GO = goseq(pwf,"{genome}","{ID_type}")

# adjust pvalue
GO$over_represented_FDR = p.adjust(GO$over_represented_pvalue, method="BH")
GO$under_represented_FDR = p.adjust(GO$under_represented_pvalue, method="BH")

GO.sig=GO[GO$over_represented_FDR < sig_threshold | GO$under_represented_FDR < sig_threshold, ]
GO.sig$defination <- sapply(GO.sig$category, function(x) Definition(GOTERM[[x]]) )

GO.sig$over_represented_pvalue <- NULL
GO.sig$under_represented_pvalue <- NULL

o_ <- GO.sig[, c(1,3,2,6,7,4,8,5)]
colnames(o_) = c("GO ID", "Total Genes", "DE Genes", "Over Rep. FDR", "Under Rep. FDR", "Pathway", "Description", "ontology")

# output
write.table(o_[o_$ontology == "BP",], "{prefix}.GO_Biological_Process.txt", sep='\\t', quote=F)
write.table(o_[o_$ontology == "MF",], "{prefix}.GO_Molecular_Function.txt", sep='\\t', quote=F)
write.table(o_[o_$ontology == "CC",], "{prefix}.GO_Cellular_Component.txt", sep='\\t', quote=F)

# KEGG analysis
KEGG = goseq(pwf, "{genome}","{ID_type}", test.cats="KEGG")
KEGG$over_represented_FDR = p.adjust(KEGG$over_represented_pvalue, method="BH")
KEGG$under_represented_FDR = p.adjust(KEGG$under_represented_pvalue, method="BH")

# Get pathway names for significant patways
KEGG.sig = KEGG[KEGG$over_represented_FDR < sig_threshold | KEGG$under_represented_FDR < sig_threshold,]
KEGG.sig$over_represented_pvalue <- NULL
KEGG.sig$under_represented_pvalue <- NULL

pathway = stack(mget(KEGG.sig$category, KEGGPATHID2NAME))

KEGG.sig$pathway = pathway$values
colnames(KEGG.sig) = c("KEGG ID", "Total Genes", "DE Genes", "Over Rep. FDR", "Under Rep. FDR", "Pathway Description")
write.table(KEGG.sig, '{prefix}.KEGG_pathway.txt', sep='\t', quote=F)

"""


if __name__ == '__main__':
    args = docopt(__doc__)

    print args

    exit(0)
    gs_genome = args['--genome']
    gs_id     = args["--id"]
    prefix    = args['--output']
    SIG_P     = args['--pvalue']
    for f in args['<FILE>']:
        rscript = GOSEQ.format(de_file = f,
                        prefix=prefix,
                        sig = SIG_P,
                        genome = gs_genome,
                        ID_type = gs_id)
        with open(f + ".goseq.R", 'w') as rscript_out:
            rscript_out.write(rscript)
    #shell("Rscript {params.prefix}.goseq.R")

    xls_writer = pd.ExcelWriter(output.xls, engine="xlsxwriter")
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
