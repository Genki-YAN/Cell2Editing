# Cell2Editing
A novel method for RNA edting investigation using scRNA-seq
	This is a tutorial about using scRNA-seq to detect RNA editing events of different cell types. By integrating the aligned reads of cells in the same cell type, we can obtain a pseudo Bulk RNA-seq. And then we used RED-ML to detect RNA editing sites in pseudo Bulk RNA-seq data of different cell types.
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
	
	run Cell2editing.sh
	
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

