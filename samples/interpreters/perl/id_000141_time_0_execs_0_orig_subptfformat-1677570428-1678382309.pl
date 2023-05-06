#! /usr/bin/perl
push(@INC,split(/:/,$ENV{"PATH"}));
do 'bldperlconst';
do 'bldperlfunc';
do 'bldperllog';
$rc=$SUCCESS;
$COMMAND=$0; $COMMAND =~ s
&logset("-c $COMMAND +l");
%SIG=('HUP','Abort','INT','Abort','QUIT','Abort',
'TERM','Abort','ABRT','Abort');
(defined $ENV{'DEBUG'}) && &log("-b","entering (@ARGV)");
($subsystem,$ptfgroupfile,$ifreqfile,$coreqfile,$prereqfile,$aparfile)=@ARGV;
chop ($globalpath=`ksh bldglobalpath`);
&Getdata($ifreqfile,*ifreqs) || &log("-x","unable to get ifreq data");
&Getdata($coreqfile,*coreqs) || &log("-x","unable to get coreq data");
&Getdata($prereqfile,*prereqs) || &log("-x","unable to get prereq data");
$familycode = 0;
open (APARFILE,"<$aparfile") ||
&log("-x","unable to get APAR data from $aparfile ($!)");
while ($aparline=<APARFILE>) {
chop $aparline;
($defect,$apar,$release,$family) = split(/\|/,$aparline);
($family) = split('@', $family);
if ( $family eq undef ) {
&log("-e","unable to determine family for defect $defect in aparfile $aparfile");
}
if ($families{$family} eq undef) {
$familycode = $familycode +1;
$families{$family} = $familycode;
}
$fcode = $families{$family};
$dnum = $defect . $SEP . $fcode;
$defectapars{$dnum} = $apar;
}
open (PTFGROUPS,"<$ptfgroupfile") ||
&log("-x","unable to get group data from $ptfgroupfile ($!)");
while ($groupline=<PTFGROUPS>) {
chop $groupline;
($ptfid,$file,$directdefects,$indirectdefects) = split(/\|/,$groupline);
$files{$ptfid} .= $file . $SEP;
@directdefects = split($SEP,$directdefects);
@indirectdefects = split($SEP,$indirectdefects);
$ptfids{$ptfid} = $DEFINED;
foreach $dtoken ((@directdefects,@indirectdefects)) {
$fcode = 0;
($release,$defect) = split(/\./,$dtoken);
if ($releaseFamily{$release} eq undef) {
chop($family=`ksh bldgetfamily $release`);
($family) = split('@', $family);
if ( $family eq undef ) {
&log("-e","unable to determine family for release $release");
}
elsif ($families{$family} eq undef) {
&log("-e","family $family was not found for any defect in aparfile $aparfile.");
}
else {
$releaseFamily{$release} = $families{$family};
$fcode = $releaseFamily{$release};
}
}
else {
$fcode = $releaseFamily{$release};
}
$dnum = $defect . $SEP . $fcode;
if ($defectapars{$dnum} ne "") {
$apars{$file} .= $defectapars{$dnum} . $SEP;
}
else {
if (! $already_error{$dnum}) {
&log("-e", "null APAR for defect $defect (defect used)");
$already_error{$dnum}=1;
}
$apars{$file} .= $defect . $SEP;
}
}
chop $apars{$file};
}
foreach $ptf (sort keys %ptfids) {
foreach $file (sort split(/$SEP/,$files{$ptf})) {
$formatline = $ptf . $PSEP;
$formatline .= &Uniquesort($SEP,$apars{$file}) . $PSEP;
$ofile = $file;
if ($file =~ m/liblpp.a$/) {
$file =~ s
}
$formatline .= $file . $PSEP . $subsystem . $PSEP;
$formatline .= $ifreqs{$ofile} . $PSEP;
$formatline .= $coreqs{$ofile} . $PSEP;
$formatline .= $prereqs{$ofile} . $PSEP;
$formatline .= "\n";
$formatline =~ s/$SEP/ /g;
$formatline =~ s
print $formatline;
if ( $! != 0 ) {
&log("-x","write error ($!)");
}
}
}
(defined $ENV{'DEBUG'}) && &log("-b","exiting");
&logset("-r");
exit $rc;
sub Abort {
&logset("-r");
exit $FATAL;
}
