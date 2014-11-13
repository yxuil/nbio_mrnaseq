if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log; fi
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment; fi
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R4" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R4; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R4
qsub -V -cwd -j y -b y -q brchigh.q -N aln_R4 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_R4.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.R4_CTTGTA_L003_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.R4_CTTGTA_L003_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V23" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V23; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V23
qsub -V -cwd -j y -b y -q brchigh.q -N aln_V23 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_V23.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.V23_GTGAAA_L005_R1.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V23_GTGAAA_L007_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.V23_GTGAAA_L005_R2.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V23_GTGAAA_L007_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C20" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C20; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C20
qsub -V -cwd -j y -b y -q brchigh.q -N aln_C20 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_C20.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.C20_GTGAAA_L002_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.C20_GTGAAA_L002_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R15" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R15; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R15
qsub -V -cwd -j y -b y -q brchigh.q -N aln_R15 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_R15.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.R15_GCCAAT_L003_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.R15_GCCAAT_L003_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R2" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R2; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R2
qsub -V -cwd -j y -b y -q brchigh.q -N aln_R2 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_R2.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.R2_GTGAAA_L003_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.R2_GTGAAA_L003_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R10" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R10; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/R10
qsub -V -cwd -j y -b y -q brchigh.q -N aln_R10 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_R10.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.R10_ACAGTG_L003_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.R10_ACAGTG_L003_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V6" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V6; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V6
qsub -V -cwd -j y -b y -q brchigh.q -N aln_V6 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_V6.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.V6_CTTGTA_L005_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.V6_CTTGTA_L005_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L14" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L14; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L14
qsub -V -cwd -j y -b y -q brchigh.q -N aln_L14 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_L14.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.L14_GCCAAT_L004_R1.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.L14_GCCAAT_L006_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.L14_GCCAAT_L004_R2.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.L14_GCCAAT_L006_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L15" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L15; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L15
qsub -V -cwd -j y -b y -q brchigh.q -N aln_L15 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_L15.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.L15_ACAGTG_L004_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.L15_ACAGTG_L004_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V3" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V3; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V3
qsub -V -cwd -j y -b y -q brchigh.q -N aln_V3 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_V3.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.V3_ACAGTG_L005_R1.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V3_ACAGTG_L006_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.V3_ACAGTG_L005_R2.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V3_ACAGTG_L006_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L12" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L12; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L12
qsub -V -cwd -j y -b y -q brchigh.q -N aln_L12 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_L12.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.L12_CTTGTA_L004_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.L12_CTTGTA_L004_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B20" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B20; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B20
qsub -V -cwd -j y -b y -q brchigh.q -N aln_B20 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_B20.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.B20_GCCAAT_L001_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.B20_GCCAAT_L001_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B4" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B4; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B4
qsub -V -cwd -j y -b y -q brchigh.q -N aln_B4 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_B4.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.B4_GTGAAA_L001_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.B4_GTGAAA_L001_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L5" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L5; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/L5
qsub -V -cwd -j y -b y -q brchigh.q -N aln_L5 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_L5.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.L5_GTGAAA_L004_R1.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.L5_GTGAAA_L006_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.L5_GTGAAA_L004_R2.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.L5_GTGAAA_L006_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V5" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V5; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/V5
qsub -V -cwd -j y -b y -q brchigh.q -N aln_V5 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_V5.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.V5_GCCAAT_L005_R1.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V5_GCCAAT_L007_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.V5_GCCAAT_L005_R2.fastq.gz,/mnt/grl/agar/users/AndersonRoz/run363/run363.V5_GCCAAT_L007_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B10" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B10; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B10
qsub -V -cwd -j y -b y -q brchigh.q -N aln_B10 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_B10.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.B10_ACAGTG_L001_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.B10_ACAGTG_L001_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B3" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B3; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/B3
qsub -V -cwd -j y -b y -q brchigh.q -N aln_B3 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_B3.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.B3_CTTGTA_L001_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.B3_CTTGTA_L001_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C11" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C11; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C11
qsub -V -cwd -j y -b y -q brchigh.q -N aln_C11 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_C11.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.C11_CTTGTA_L002_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.C11_CTTGTA_L002_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C17" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C17; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C17
qsub -V -cwd -j y -b y -q brchigh.q -N aln_C17 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_C17.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.C17_GCCAAT_L002_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.C17_GCCAAT_L002_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
if [ ! -d "$/mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C14" ]; then mkdir -p /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C14; fi
cd /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/star_alignment/C14
qsub -V -cwd -j y -b y -q brchigh.q -N aln_C14 -o /mnt/grl/brc/data/anderson_rozalyn/rt195/mRNAseq_mm10_deseq/log/aln_C14.log  "/mnt/grl/sofrware/star//STAR --genomeDir /mnt/grl/genomes/Mus_musculus/UCSC_mm10/STARIndex --readFilesIn /mnt/grl/agar/users/AndersonRoz/run323/run323.C14_ACAGTG_L002_R1.fastq.gz /mnt/grl/agar/users/AndersonRoz/run323/run323.C14_ACAGTG_L002_R2.fastq.gz --runThreadN 8 --outSAMunmapped Within --readFilesCommand zcat"
cd ..
