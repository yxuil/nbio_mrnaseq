#!/usr/bin/env python
__author__ = "Xiaoyu Liu"
__email__ = "liux@nbio.info"
__copyright__ = "Copyright (C) 2016 Xiaoyu Liu"
__status__ = "development"
__license__ = "Public Domain"
__version__ = "0.2b"

import os
import begin

import sys

edgeR = """
# read in exp data
rawdata <- read.delim("{INPUT}", check.names=FALSE, stringsAsFactors=FALSE)

library('edgeR')
library('Cairo')
library('RColorBrewer')
# put the data into a DGEList object
y <- DGEList(counts=rawdata[,2:ncol(rawdata)], genes=rawdata[,1])

# skipped annotation part
# filter duplicated entries (None)
o <- order(rowSums(y$counts), decreasing=TRUE)
y <- y[o,]

d <- duplicated(y$genes)
y <- y[!d,]

# filter lowly expressed genes
keep <- rowSums(cpm(y)>1) >= 3
y <- y[keep,]

# calculate library size
# normalization
y <- calcNormFactors(y)
# setup design matrix
# Treatments (conditions to be compared)
treatments <- factor(c({treatments}))

if (is.null(c({pairs}))) {{
    # no paired
    design <- model.matrix(~treatments)
}} else {{
    # paired samples
    pairs <- factor(c({pairs}))
    data.frame(Sample=colnames(y),pairs,treatments)
    design <- model.matrix(~pairs + treatments)
}}

# MDS
cols <- brewer.pal(8, "Set1")
colcode <- cols[as.numeric(treatments)]
CairoPNG("{prefix}.MDS.png")
plotMDS(y,
        pch = as.numeric(treatments),
        col = colcode,
        labels = colnames(y))
dev.off()


rownames(design) <- colnames(y)
# DE analysis
y <- estimateGLMCommonDisp(y, design, verbose=TRUE)
y <- estimateGLMTrendedDisp(y, design)
y <- estimateGLMTagwiseDisp(y, design)
fit <- glmFit(y, design)
lrt <- glmLRT(fit)
# top genes
de_table=topTags(lrt, n=Inf, sort.by="PValue")
#        de_table = format(de_table, digit = 3)
write.table(de_table, file="{prefix}.diffexpr.txt", sep = '\t', row.names=FALSE,na='')
# num of de genes summary
de <- decideTestsDGE(lrt)
de_stat = summary(de)
cat(c("{prefix}", de_stat[1:3], "\n"), file="{prefix}.deSummary.txt", sep = '\t', append=FALSE)

# plot log Fold Change vs Count per Million
CairoPNG("{prefix}.FC-CPM.png")
detags <- rownames(y)[as.logical(de)]
plotSmear(lrt, de.tags=detags)
abline(h=c(-1, 1), col="blue")
dev.off()

# plot boxplots of counts and cpm
CairoPNG("{prefix}.Boxplot.png", width = 960, height = 480)
boxplot(log2(y$counts + 1), las=2, col=colcode, main="Counts")
boxplot(log2(cpm(y) + 1), las=2, col=colcode, main = "CPM")
dev.off()
"""

@begin.start
def run(treatments=None, prefix=None, pairs="", *count_table):
    rscript = edgeR.format(INPUT=' '.join(count_table),
                               prefix=prefix,
                               treatments=treatments ,
                               pairs = pairs)
    with open(prefix + "_edger.R", 'w') as rscript_out:
            rscript_out.write(rscript)