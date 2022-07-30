#!/bin/bash
#Author------Yan
#Data------20220328
#Function------RNA editing was detected in different cell types

if [ $# == 0 ]; then
        echo "Parameter error"
        echo "Eleven Parameter needed!!! Type --help or help for details "
        exit 1;
elif [[ $1 == *help ]] ; then
        echo "Parameter"
        echo "The first parameter is the file path of bam. The second parameter is the barcode list. The third parameter is the pattern of barcode pattern in bam file. The fourth parameter is the name of cell type. The fifth parameter is the path of output. The sixth parameter is the reference genome. The seventh parameter is the SNP database. The eighth parameter is the simpleRepeat.merge.bed file. The ninth parameter is the alu.bed file. The tenth parameter is the file path of Split_bacorde_v2.pl. The eleventh parameter is the file path of duplicate.v2.py"
        exit 1;
elif [ $# == 11 ] ; then
        bamfile=$1
        barcodelist=$2
        barcodepattern=$3
        celltype=$4
        outpath=$5
        refseq=$6
        refvcf=$7
        Repeat=$8
        alu=$9
	split=$10
	duplicate=$11
#       echo ${bamfile} ${barcodelist} ${barcodepattern} ${celltype}
        cd ${outpath} &&
        mkdir ${celltype} &&
        cd ${celltype} &&
        echo ==========Cell2bam start at : `date` ========== &&
        echo "Spliting bam file------------------------------" &&
        perl /hwfssz5/ST_SUPERCELLS/P21H10200N0163/wuyan/Software/Cell2bam/Split_bacorde_v2.pl -f1 ${barcodelist} -f2 ${bamfile} -f3 $barcodepattern -out1 ${celltype}.bam &&
        mv sorted.bam ${celltype}.sort.bam &&
        mv sorted.bam.bai ${celltype}.sort.bam.bai &&
        echo "index bam file AND get chromosome---------------" &&
#       samtools index ${celltype}.sort.bam &&
        samtools idxstats ${celltype}.sort.bam|awk '{print $1}'|sed 's/*//g'|sed '/^[[:blank:]]*$/d' >  chromosome.txt &&
        echo "Marker duplicate, it will take long time!!!-----" &&
        for j in $(cat chromosome.txt|awk '{print $1}'); do  echo /hwfssz1/ST_SUPERCELLS/Reference/software/miniconda3_py3.9/bin/python /hwfssz5/ST_SUPERCELLS/P21H10200N0163/wuyan/Software/Cell2bam/duplicate.v2.py ${celltype}.sort.bam ${celltype}.marked_duplicates.${j}.bam ${j} >> run.sh ; echo ${celltype}.marked_duplicates.${j}.bam >> merge.path ;done &&
        sh run.sh &&
        echo "merge bam----------------------------------------" &&
        samtools merge -b merge.path ${celltype}.marked_duplicates.bam &&
        picard SortSam -I ${celltype}.marked_duplicates.bam -O ${celltype}.marked_duplicates.sort.bam -SORT_ORDER coordinate &&
        echo "RNA editing--------------------------------------" &&
        red_ML.pl --rnabam ${celltype}.marked_duplicates.sort.bam --reference $refseq --dbsnp $refvcf --simpleRepeat $Repeat --alu $alu --outdir . &&
	echo ==========end at : `date` ========== 

fi

