#!/usr/bin/perl -w
if (@ARGV < 7) {die("Usage: plot_win_stats.pl Tmin/Tmax eid name meas_file sta_file eid_text cmtall_psmeca\n")}
($Ts,$eid,$name,$meas_file,$sta_file,$eid_text,$cmtall_psmeca) = @ARGV;
if (not -f $meas_file) {die("\n check if $meas_file exists\n")}
if (not -f $sta_file) {die("\n check if $sta_file exists\n")}
if (not -f $eid_text) {die("\n check if $eid_text exists\n")}
if (not -f $cmtall_psmeca) {die("\n check if $cmtall_psmeca exists\n")}
($Tmin,$Tmax) = split("/",$Ts);
$sTper = sprintf("T = %i - %i s",$Tmin,$Tmax);
$fontno = 1;
$psfile = "$name.ps";
$jpgfile = "$name.jpg";
$xmin = -122; $xmax = -114; $ymin = 32; $ymax = 37;
$R = "-R$xmin/$xmax/$ymin/$ymax ";
$xtick = 1; $ytick = 1;
$B = "-Ba${xtick}:.\"  \":WEsN";
$coast_info = "-W0.5 -Dh -A100";
$wid = 3.5;
$J = "-JM$wid";
$origin = "-X3.5 -Y7.5";
$cshfile = "plot_win_stats.csh";
print "\nWriting to $cshfile ...\n";
open(CSH,">$cshfile");
print CSH "gmtset MEASURE_UNIT inch TICK_LENGTH 5p BASEMAP_TYPE plain PAPER_MEDIA letter ANNOT_FONT_SIZE = 10p LABEL_FONT_SIZE = 12p PLOT_DEGREE_FORMAT D\n";
print CSH "psbasemap $R $J $B $origin -K -V -P > $psfile\n";
print CSH "pscoast $R $J $coast_info -S150/200/255 -W2 -G200/255/150 -N1/1p -N2/0.5p -O -K -V >> $psfile\n";
$ifault = 1;
if($ifault==1) {
$dir_fault = "/home/carltape/gmt/faults";
$fault_file = "${dir_fault}/jennings_more.xy";
$fault_infoK = "-m -W0.5p,0/0/0";
print CSH "psxy $fault_file $R $J $fault_infoK -O -K -V >> $psfile\n";
}
print CSH "awk \'{print \$4,\$3,0,4,B,C}\' ${sta_file} | psxy $J $R -m -Si0.15 -W2 -G200/200/200 -N -O -K -V >>$psfile\n";
open(IN,"${eid_text}"); @mapstrings = <IN>; close(IN);
$nstrings = @mapstrings;
$x1 = $xmin - 6*$xtick;
for ($i = 0; $i < $nstrings; $i++) {
$y1 = $ymax - $i*$ytick*0.6;
$line = $mapstrings[$i]; chomp($line);
print CSH "pstext $R $J $B -N -K -O -V >> $psfile <<EOF\n $x1 $y1 12 0 $fontno LM $line\nEOF\n";
}
$cmtfont = 10;
$cmt_scale = 0.4;
$cmtinfo    = "-N -Sm${cmt_scale}/$cmtfont -L0.5p/0/0/0 -G255/0/0";
$cmtinfo_dc = "-N -Sd${cmt_scale}/$cmtfont -L0.5p/0/0/0 -G255/0/0";
@psmeca_line = `grep $eid ${cmtall_psmeca}`; chomp(@psmeca_line);
print "\n -- @psmeca_line -- \n";
print CSH "psmeca $R $J $cmtinfo -O -K -V >>$psfile<<EOF\n @psmeca_line \nEOF\n";
($nwin,undef,undef,undef) = split(" ",`wc $meas_file`);
print "\n -- $nwin total windows -- \n";
$y1 = $ymax - ($nstrings+2.5)*$ytick/2;
print CSH "pstext $R $J $B -N -K -O -V >> $psfile <<EOF\n $x1 $y1 14 0 $fontno LM $nwin windows picked for period range $sTper\nEOF\n";
$file0 = "${eid}_cc_dT_dA_dTsigma_dAsigma";
`awk '{print \$15,\$16,\$19,\$20,\$15/\$19,\$16/\$20}' $meas_file > $file0`;
($min1,$max1,$min2,$max2,$min3,$max3,$min4,$max4,$min5,$max5,$min6,$max6) = split(" ",`minmax -C $file0`);
$st1 = sprintf("min/max = %.2f / %.2f",$min1,$max1);
$st2 = sprintf("min/max = %.2f / %.2f",$min2,$max2);
$st3 = sprintf("min/max = %.2f / %.2f",$min3,$max3);
$st4 = sprintf("min/max = %.2f / %.2f",$min4,$max4);
$st5 = sprintf("min/max = %.2f / %.2f",$min5,$max5);
$st6 = sprintf("min/max = %.2f / %.2f",$min6,$max6);
$widhist = 2.75; $heighthist = 1.4;
$Nbin = 20;
$max_DT = 8; $min_DT = -$max_DT;
$max_DA = 2.5; $min_DA = -$max_DA;
$max_sigma_DT = 2.5; $min_sigma_DT = 0;
$max_sigma_DA = $max_sigma_DT; $min_sigma_DA = $min_sigma_DT ;
$max_DTerr = $max_DT; $min_DTerr = -$max_DTerr;
$max_DAerr = $max_DA; $min_DAerr = -$max_DAerr;
if($Tmin == 2 || $Tmin == 3) {
$max_DT = 5; $min_DT = -$max_DT;
$max_DA = 1.5; $min_DA = -$max_DA;
$max_sigma_DT = 2.0; $min_sigma_DT = 0;
$max_sigma_DA = $max_sigma_DT; $min_sigma_DA = $min_sigma_DT ;
$max_DTerr = 10; $min_DTerr = -$max_DTerr;
$max_DAerr = 4; $min_DAerr = -$max_DAerr;
}
$DT_bin = ($max_DT - $min_DT)/$Nbin;
$DA_bin = ($max_DA - $min_DA)/$Nbin;
$DT_sigma_bin = ($max_sigma_DT - $min_sigma_DT)/$Nbin;
$DA_sigma_bin = ($max_sigma_DA - $min_sigma_DA)/$Nbin;
$DTerr_bin = ($max_DTerr - $min_DTerr)/$Nbin;
$DAerr_bin = ($max_DAerr - $min_DAerr)/$Nbin;
$X0 = -2.25; $Y0 = -2.1;
$dX = $widhist+1; $dY = $heighthist+0.75;
@ohistX = ($X0, $X0+$dX, $X0, $X0+$dX, $X0, $X0+$dX);
@ohistY = ($Y0, $Y0, $Y0-$dY, $Y0-$dY, $Y0-2*$dY, $Y0-2*$dY);
$origin_hist1 = "-Xa$ohistX[0] -Ya$ohistY[0]";
$origin_hist2 = "-Xa$ohistX[1] -Ya$ohistY[1]";
$origin_hist3 = "-Xa$ohistX[2] -Ya$ohistY[2]";
$origin_hist4 = "-Xa$ohistX[3] -Ya$ohistY[3]";
$origin_hist5 = "-Xa$ohistX[4] -Ya$ohistY[4]";
$origin_hist6 = "-Xa$ohistX[5] -Ya$ohistY[5]";
$max_count = 50; $count_tick = 10;
$Rhist1 = "-R$min_DT/$max_DT/0/$max_count";
$Rhist2 = "-R$min_DA/$max_DA/0/$max_count";
$Rhist3 = "-R$min_sigma_DA/$max_sigma_DA/0/$max_count";
$Rhist4 = "-R$min_sigma_DA/$max_sigma_DA/0/$max_count";
$Rhist5 = "-R$min_DTerr/$max_DTerr/0/$max_count";
$Rhist6 = "-R$min_DAerr/$max_DAerr/0/$max_count";
$Jhist = "-JX${widhist}i/${heighthist}";
$sty = "Percent  (N = $nwin)";
$Bhist1 = "-Ba4f1:\"dT (s)  ($st1)\":/a${count_tick}:\"$sty\":WeSn";
$Bhist2 = "-Ba1f0.25:\"dlnA  ($st2)\":/a${count_tick}:\"$sty\":WeSn";
$Bhist3 = "-Ba0.5f0.1:\"sigma-dT (s)  ($st3)\":/a${count_tick}:\"$sty\":WeSn";
$Bhist4 = "-Ba0.5f0.1:\"sigma-dlnA  ($st4)\":/a${count_tick}:\"$sty\":WeSn";
$Bhist5 = "-Ba4f1:\"dT / sigma-dT  ($st5)\":/a${count_tick}:\"$sty\":WeSn";
$Bhist6 = "-Ba1f0.25:\"dlnA / sigma-dlnA  ($st6)\":/a${count_tick}:\"$sty\":WeSn";
$hist_info = "-W5 -G0/255/255 -L0.5p,0/0/0 -Z1";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist1 $Rhist1 -T0 -W${DT_bin} -K -O -V $origin_hist1 >> $psfile\n";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist2 $Rhist2 -T1 -W${DA_bin} -K -O -V $origin_hist2 >> $psfile\n";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist3 $Rhist3 -T2 -W${DT_sigma_bin} -K -O -V $origin_hist3 >> $psfile\n";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist4 $Rhist4 -T3 -W${DA_sigma_bin} -K -O -V $origin_hist4 >> $psfile\n";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist5 $Rhist5 -T4 -W${DTerr_bin} -K -O -V $origin_hist5 >> $psfile\n";
print CSH "pshistogram $file0 $hist_info $Jhist $Bhist6 $Rhist6 -T5 -W${DAerr_bin} -K -O -V $origin_hist6 >> $psfile\n";
print CSH "psxy -W1.5p,0/0/0 $Jhist $Rhist1 -K -O -V $origin_hist1 >>$psfile<<EOF\n0 0\n0 $max_count\nEOF\n";
print CSH "psxy -W1.5p,0/0/0 $Jhist $Rhist2 -K -O -V $origin_hist2 >>$psfile<<EOF\n0 0\n0 $max_count\nEOF\n";
print CSH "psxy -W1.5p,0/0/0 $Jhist $Rhist5 -K -O -V $origin_hist5 >>$psfile<<EOF\n0 0\n0 $max_count\nEOF\n";
print CSH "psxy -W1.5p,0/0/0 $Jhist $Rhist6 -K -O -V $origin_hist6 >>$psfile<<EOF\n0 0\n0 $max_count\nEOF\n";
print CSH "psxy $J $R -N -O -X15 -V >>$psfile<<EOF\n 0 0\nEOF\n";
print CSH "ps2pdf $psfile\n";
print CSH "rm $psfile\n";
close(CSH);
system("csh -f $cshfile");
