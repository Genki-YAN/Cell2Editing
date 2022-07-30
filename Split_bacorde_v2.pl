#!/usr/bin/perl -w
use Getopt::Long ;
my ($file1,$file2,$file3,$out1);
GetOptions (
        "f1:s" => \$file1,
        "f2:s" => \$file2,
	"f3:s" => \$file3,
        "out1:s" => \$out1
);
if (!$file1|!$file2) {
        die <<USAGE;
==================================================================================
Description: merge the file1 and file2
Usage:       perl $0 [options]
Options:
                * -f1   file 1(barcode)
                * -f2   file 2(bam)
		* -f3	pattern
                * -out1  new bam
E.g.:
            perl $0 -f1 file1.txt -f2 file2.txt -f3 CB:Z: -out1 result.bam
==================================================================================
USAGE
}

`samtools view -H $file2 > header.txt`;

###1.get hash
my %hash;
open FILE,$file1 or die "Can't open the $file1 !";
while($_ = <FILE>){
	chomp($_);
	$hash{$_} = 1;      	
}
close FILE;
while(my ($key, $val) = each(%hash)) { print "$key => $val\n" }

###2.split
open(IN,"samtools view $file2|") or die "Can't open the $file2 !";
open OUT1, ">$out1.1" or die $!;
	while(<IN>){
		chomp($_);
		#@info = split /\t/,$_;
		if ($_ =~ /$file3/){
			$_ =~ /$file3(\S+)/;
			$barcode = $1;
		
			if(exists $hash{$barcode}) {
				print OUT1 "$_\n";
				#print  "$_\n";
				if(!exists $hash2{$barcode}){
                        		$hash2{$barcode}=1;
                		}
			}
		}
}
close OUT1;
close IN;
$length = keys %hash2;
print "$length\n";

`cat header.txt > $out1`;
`cat $out1.1 >> $out1`;
`rm $out1.1`;
`samtools sort $out1 -o sorted.bam`;
`samtools index sorted.bam`;
