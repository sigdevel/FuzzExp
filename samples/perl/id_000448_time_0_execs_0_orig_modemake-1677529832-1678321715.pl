#!/usr/bin/env perl
die "Input two POSCAR-type files\n" if @ARGV != 2 ;
$p1 = $ARGV[0] ;
$p2 = $ARGV[1] ;
open P1 , $p1 or die "$p1 not found in this directory\n" ;
while (<P1>){$file .= $_ ;}
@p1 = split /\n/ , $file ;
$n1 = @p1 ;
close P1 ;
open P2 , $p2 or die "$p2 not found in this directory\n" ;
$file = undef ;
while (<P2>){$file .= $_ ;}
@p2 = split /\n/ , $file ;
$n2 = @p2 ;
close P2 ;
die "The two files are not of the same length\n" if $n1 != $n2 ;
for ($i=1; $i<5; $i++){
$line = $p1[$i] ; chomp($line) ; $line=~s/^\s+//g ; @line=split /\s+/,$line ;
if($i == 1){$latt = $line[0] ;}
if($i == 2){@ax[0..2] = @line[0..2] ;}
if($i == 3){@ay[0..2] = @line[0..2] ;}
if($i == 4){@az[0..2] = @line[0..2] ;}
}
if ($p1[5] =~ /\d+/) {
$lineno = 5;
$vasp5=0;
}else{
$lineno = 6;
$vasp5=1;
}
@elements = split /\s+/ , $p1[$lineno] ;
$nel = @elements ;
$line = $p1[$lineno] ; chomp($line) ; $line=~s/^\s+//g ; @line=split /\s+/,$line ;
@not[0..$nel-1] = @line[0..$nel-1] ;
while ($not[$k] != undef){
$natoms+=$not[$k++] ;
}
if ($p1[7] =~ /Selective/){
$selectiveDynamics=1;
}else{
$selectiveDynamics=0;
}
$sh = 7 + $vasp5+$selectiveDynamics ;
for ($i=0; $i<$natoms; $i++){
$j = $i+$sh ;
$l1 = $p1[$j] ; chomp($l1) ; $l1=~s/^\s+//g ;
@l1=split /\s+/,$l1 ;
$l2 = $p2[$j] ; chomp($l2) ; $l2=~s/^\s+//g ; @l2=split /\s+/,$l2 ;
$dx = $l1[0]-$l2[0] ; while ($dx > 0.5){$dx -= 1.0 ;} while ($dx < -0.5){$dx += 1.0 ;}
$dy = $l1[1]-$l2[1] ; while ($dy > 0.5){$dy -= 1.0 ;} while ($dy < -0.5){$dy += 1.0 ;}
$dz = $l1[2]-$l2[2] ; while ($dz > 0.5){$dz -= 1.0 ;} while ($dz < -0.5){$dz += 1.0 ;}
$w[$i][0] = ($dx*$ax[0]+$dy*$ay[0]+$dz*$az[0])*$latt ;
$w[$i][1] = ($dx*$ax[1]+$dy*$ay[1]+$dz*$az[1])*$latt ;
$w[$i][2] = ($dx*$ax[2]+$dy*$ay[2]+$dz*$az[2])*$latt ;
}
for ($i=0; $i<$natoms; $i++){
for ($j=0; $j<3; $j++){
$sum += $w[$i][$j] * $w[$i][$j] ;
}
}
$sum = sqrt($sum) ;
open MOD , ">MODECAR" ;
for ($i=0; $i<$natoms; $i++){
for ($j=0; $j<3; $j++){
$w[$i][$j] = $w[$i][$j]/$sum ;
}
printf MOD "%20.10E %20.10E %20.10E \n",$w[$i][0],$w[$i][1],$w[$i][2] ;
}
close(MOD) ;
