#!/usr/bin/perl -w
$emin = 1;
$smodel = "m16";
$Ttag = "T003_T030";
$isort = 2;
$file_stations = "/home/carltape/gmt/stations/seismic/Matlab_output/STATIONS_CALIFORNIA_TOMO_INNER_gmt";
if (not -f ${file_stations}) {die("check if file_stations ${file_stations} exist or not\n")}
open(IN,"${file_stations}"); @stalines = <IN>; close(IN); $nrec = @stalines;
$edir = "/home/carltape/results/SOURCES/EID_STATION_LISTS";
$file_eid_sub = "/home/carltape/results/EID_LISTS/eids_simulation";
if (not -f ${file_eid_sub}) {die("check if ${file_eid_sub} exist or not\n")}
if($isort == 1) {$sortlab = "dist"} else {$sortlab = "az"}
print "\n $nrec \n";
if (0==1) {
for ($ik = 1; $ik <= $nrec; $ik = $ik+1) {
($stalon,$stalat,$station,$network,undef,undef) = split(" ",$stalines[$ik-1]);
print "$ik out of $nrec : station $station.$network\n";
}
die("TESTING: listing only the stations\n");
}
$imin = 1; $imax = $nrec;
for ($ik = $imin; $ik <= $imax; $ik = $ik+1) {
@pdcat = "/home/carltape/bin/pdcat -r"; $k = 1;
($stalon,$stalat,$station,$network,undef,undef) = split(" ",$stalines[$ik-1]);
print "$ik out of $nrec : station $station.$network\n";
$event_sort = "${edir}/EIDS_by_${sortlab}_from_${station}.${network}";
if (not -f "${event_sort}") {die("check if event_sort ${event_sort} exist or not\n")}
open(IN,"${event_sort}"); @elines = <IN>; close(IN); $nevent = @elines;
print "$nevent events in the list \n";
$ofile = "${station}_${network}_${Ttag}_${smodel}_ALL.pdf";
if (-f $ofile) {
print "--> $ofile already exists\n";
} else {
for ($j = 1; $j <= $nevent; $j = $j+1) {
($eid,$elon,$elat,undef,undef,undef,undef,undef) = split(" ",$elines[$j-1]);
($nmatch,undef,undef) = split(" ",`grep $eid ${file_eid_sub} | wc`);
if ($nmatch == 1) {
@files = glob("${eid}_${Ttag}_${station}_${network}_${smodel}*pdf");
$numf = @files;
if ($numf == 0) {
} elsif ($numf == 1) {
$pdffile = $files[0]; chomp($pdffile);
$pdcat[$k] = $pdffile; $k = $k+1;
} else {
print "$eid\n";
die("more than one pdf file exists\n");
}
}
}
if ($k > $emin+1) {
print "output file is $ofile\n";
$pdcat[$k] = "./$ofile";
print "@pdcat\n";
`@pdcat`;
`sleep 5s`;
} else {
print "--> Fewer than $emin events out of $nevent for this station\n";
}
}
}
