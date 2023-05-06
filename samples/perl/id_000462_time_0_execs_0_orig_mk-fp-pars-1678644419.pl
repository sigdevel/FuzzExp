#!/usr/bin/perl
@dtypes=('Byte(uchar)','Short(int16)','Float(float32)','Short(int16)','Float/(float32)','Short/(int16)','UShort/(uint16)','Long/(int32)');
$finname=shift;
$inname=qx(basename $finname);
chomp($inname);
open IN,$finname or die "Couldn't find $finname !";
$br=read(IN,$hdr,1024);
close IN;
if($br != 1024){die "jacked!!!";}
$endi = "undefined";
my ($ncol, $nrow, $nsecs, $pixtype, $mxst, $myst, $mzst, $mx, $my, $mz,
$dx,$dy,$dz,$alpha,$beta,$gamma,$colax,$rowax,$secax,$min,$max,$mean,
$nspg, $next, $dvid, $nblank, $ntst, $blank, $numints, $numfloats, $sub,
$zfac, $min2, $max2, $min3, $max3, $min4, $max4, $imtype, $lensnum,
$n1, $n2, $v1, $v2, $min5, $max5, $ntimes, $imgseq, $xtilt, $ytilt, $ztilt,
$nwaves, $wv1, $wv2, $wv3, $wv4, $wv5, $z0, $x0, $y0, $ntitles,
$t1, $t2, $t3, $t4, $t5, $t6, $t7, $t8, $t9, $t10) = unpack (
"l>l>l>l>l>l>l>l>l>l>f>f>f>f>f>f>l>l>l>f>f>f>l>l>s>s>l>A24s>s>s>s>f>f>f>f>f>f>s>s>s>s>s>s>f>f>s>s>f>f>f>s>s>s>s>s>s>f>f>f>l>A80A80A80A80A80A80A80A80A80A80",$hdr);
if($pixtype >=0 && $pixtype<7) {$endi="ieee-be";}
else {
my ($ncol, $nrow, $nsecs, $pixtype, $mxst, $myst, $mzst, $mx, $my, $mz,
$dx,$dy,$dz,$alpha,$beta,$gamma,$colax,$rowax,$secax,$min,$max,$mean,
$nspg, $next, $dvid, $nblank, $ntst, $blank, $numints, $numfloats, $sub,
$zfac, $min2, $max2, $min3, $max3, $min4, $max4, $imtype, $lensnum,
$n1, $n2, $v1, $v2, $min5, $max5, $ntimes, $imgseq, $xtilt, $ytilt, $ztilt,
$nwaves, $wv1, $wv2, $wv3, $wv4, $wv5, $z0, $x0, $y0, $ntitles,
$t1, $t2, $t3, $t4, $t5, $t6, $t7, $t8, $t9, $t10) = unpack (
"l<l<l<l<l<l<l<l<l<l<f<f<f<f<f<f<l<l<l<f<f<f<l<l<s<s<l<A24s<s<s<s<f<f<f<f<f<f<s<s<s<s<s<s<f<f<s<s<f<f<f<s<s<s<s<s<s<f<f<f<l<A80A80A80A80A80A80A80A80A80A80",$hdr);
if($pixtype >=0 && $pixtype<7) {$endi="ieee-le";}
else {die ("failed: pixtype is $pixtype, and endian is $endi")};
}
print "Read success: pixtype is $dtypes[$pixtype], endian is $endi\n";
$IMF=$finname;
$PGF=$IMF.'.pol';
$OPF=$IMF.'.pts';
$NZS=($nsecs/$nwaves)-1;
$w1=0+($nwaves>1);
$w2=0+($nwaves>2);
$w3=0+($nwaves>3);
$w4=0+($nwaves>4);
open PARS,">$IMF.pars";
print PARS <<EOF
FP Parameter Format 1.0
ImageFile $IMF
ProcMode 1
Method 1
PolygonFile $PGF
gap 1
SubRegion
Z 0 $NZS 1
T 0 0 1
W 0 $w1 $w2 $w3 $w4
PeakFinding
nstd 8.000000
auto_dec 1
dec_nstd .300000
min_pts 1500
max_pts 2000
min_pt_sep 4.000000
pt_center_method 0
search_range 2 2
box_size 5 5
RegionGrowing
nstd 2.000000
half_max 0 0.500000
xyz_range 315 233 28
valley 0
min_pixels_to_accept_pt 1
mask_file null
out_mask null
Pt_Output $OPF
EOF
