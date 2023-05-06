#!/usr/bin/perl -w
my(@bandwidth,@latency,@size,@time);
my($total_samples) = 0;
my($rawdata_file) = "";
sub max {
my($x,$y) = @_;
if($x > $y) {
return $x;
}else{
return $y;
}
}
sub f_sum {
my($x,$y) = @_;
my($b,$l,$s,$t) = 0;
my($sum);
$sum = 0;
for($k=0; $k < $total_samples; $k++){
$b = $bandwidth[$k];
$l = $latency[$k];
$s = $size[$k];
$t = $time[$k];
$sum += (log($s*max(1.0/($b*$x),1.0e-4*$l)+ $y*$l)-log($t))**2
}
return sqrt($sum/$total_samples);
}
sub f_max {
my($x,$y) = @_;
my($b,$l,$s,$t) = 0;
my($max);
$max = 0;
for($k=0; $k < $total_samples; $k++){
$b = $bandwidth[$k];
$l = $latency[$k];
$s = $size[$k];
$t = $time[$k];
$max = max((log($s*max(1.0/($b*$x),1.0e-4*$l)+ $y*$l)-log($t))**2,$max);
}
return sqrt($max);
}
sub findMinimum () {
my($max_iteration) = 1e5;
my($min_precision) = 1e-10;
my($minX) = 1e-10;
my($maxX) = 2;
my($minY) = 1e-10;
my($maxY) = 20;
my($candidateX) = 0;
my($candidateY) = 0;
my($minimumBEFORE) = +1e20;
my($minimumAFTER) = +1e20;
my($sampleX,$sampleY)=(10,10);
my($diffX) = 0;
my($diffY) = 0;
my($progressCounter) = 1;
for($i=0;$i<$max_iteration;$i++){
print STDERR $i.": X in [$minX,$maxX] , Y in [$minY,$maxY], min $minimumAFTER , candidates are X $candidateX , Y $candidateY \n";
$minimumBEFORE = $minimumAFTER;
$diffX = ($maxX - $minX)/$sampleX;
$diffY = ($maxY - $minY)/$sampleY;
my($progress)=0;
for($itX = $minX; $itX <= $maxX; $itX += $diffX){
for($itY = $minY; $itY <= $maxY; $itY += $diffY){
$temp = f_max($itX, $itY);
if($temp < $minimumAFTER){
$minimumAFTER = $temp;
$candidateX = $itX;
$candidateY = $itY;
}
$progress++;
if((($sampleX*$sampleY)/$progress)%10 == 0){
if($progressCounter++ == 60){
print STDOUT "\n";
$|++;
$progressCounter = 1;
}else{
print STDOUT ".";
$|++;
}
}
}
}
print STDERR "\n";
print STDERR "Found $candidateX, $candidateY! min=".$minimumAFTER."\n";
if( abs($minimumAFTER - $minimumBEFORE) <= $min_precision){
print STDERR "Found minimum because ".abs($minimumAFTER - $minimumBEFORE)." <= ".$min_precision."\n";
print STDOUT "\nCadidates are X=$candidateX and Y=$candidateY\n";
print STDERR "Bailling out, have a nice day\n";
return $minimumAFTER;
}
$minX = $candidateX - $diffX;
$maxX = $candidateX + $diffX;
$minY = $candidateY - $diffY;
$maxY = $candidateY + $diffY;
}
return $minimumAFTER;
}
if($
print "Usage:\n";
print "logbased-regression.pl <inputfile>\n\n";
exit 1;
}else {
$rawdata_file = $ARGV[0];
print STDOUT "Relax this may take some time\n";
}
open (INPUTFILE, "< ".$rawdata_file) || die "Could not open file \"".$rawdata_file."\" !";
while(<INPUTFILE>){
@values = split(/\s+/, $_);
if(scalar(@values) != 5){
print STDERR "Wrong input file, lines must follow the convetion:\n";
print STDERR "Bandwidth Latency Size Model Time\n";
print STDERR "Error, near line $total_samples:\n";
print STDERR "\t$_\n";
exit 1;
}
push @bandwidth, $values[0];
push @latency, $values[1];
push @size, $values[2];
push @time, $values[4];
$total_samples++;
}
close(INPUTFILE);
print STDERR "Value of bandwidth[0] is ".$bandwidth[0]." and total samples is ".$total_samples."\n";
print STDERR "Value of latency[0] is ".$latency[0]." and total samples is ".$total_samples."\n";
print STDERR "Value of size[0] is ".$size[0]." and total samples is ".$total_samples."\n";
print STDERR "Value of time[0] is ".$time[0]." and total samples is ".$total_samples."\n";
print STDERR "The sum for 1 and 1 is ".f_max(1,1)."\n";
print STDERR "The sum for 1 and 10 is ".f_max(1,10)."\n";
$min = findMinimum();
print STDOUT "The min is approximatelly: ".$min."\n";
