# Cell2Editing
A novel method for RNA edting investigation using scRNA-seq
	This is a tutorial about using scRNA-seq to detect RNA editing events of different cell types. By integrating the aligned reads of cells in the same cell type, we can obtain a pseudo Bulk RNA-seq. And then we used RED-ML to detect RNA editing sites in pseudo Bulk RNA-seq data of different cell types.
	Before running the program it is recommended to use samtools to split the reads aligned to the forward and aligned to the reserve strand.
	samtools view -b -f 16
	samtools view -b -F 16
	• Software installed
	Firstly, we need install several software and add those to your PATH environment variable after installing them.
	Samtools (https://github.com/samtools/samtools/releases/)
	RED-ML (https://github.com/BGIHENG/RED-ML)
	Python (https://www.python.org/downloads/)
	Perl (https://www.perl.org/)
	Picard (https://github.com/broadinstitute/picard)
	• Program running
	Download Split_bacorde_v2.pl, duplicate.v2.py, Cell2editing.sh.
	According to the tutorial of RED-ML download appropriate reference genome, dbSNP138,  simpleRepeat and Alu.
	
	sh Cell2editing.sh ProB.primary.sort.bam PB48h_3_ProB_barcode.list CB:Z: ProB 01.RNA_editing genome.fasta All_20180418.GRCh38p7.vcf.gz simpleRepeat.merge.bed hg38.alu.bed Split_bacorde_v2.pl duplicate.v2.py
	
	Argument	Summary
	1	The file path of bam
	2	The file path of barcode list of cell type
	3	The pattern of barcode tag in bam file
	4	The name of cell type
	5	The output path
	6	The file path of reference genome
	7	The file path of SNP database
	8	The file path of simpleRepeat.merge.bed
	9	The file path of Alu.bed
	10	The file path of Split_bacorde_v2.pl
	11	The file path of duplicate.v2.py

