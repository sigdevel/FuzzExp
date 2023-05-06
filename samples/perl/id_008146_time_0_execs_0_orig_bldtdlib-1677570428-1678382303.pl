sub BLDTDinterfaceinit {
($release) = @_; $rc=$SUCCESS;
local($rc);
$workpath=`ksh bldreleasepath $release`; chop $workpath;
dbmopen(targetfd,"$workpath/bldtd/targetfd",0750) ||
&log("$lvar -x","$workpath/bldtd/targetfd open error ($!)");
(&Opendecodeddefects($release) == $SUCCESS) ||
&log("$lvar -x","cannot access decoded defects");
return $rc;
}
sub BLDTDbuild {
local($release,$makelist,$defectlist,$updatelist,$bldenvlist,$changelist)=@_;
local(%sourcefd,%targetfd,$path,@newtarget,@alldepend,@newdepend,$rc);
local($makeline,$target,$dependency,$built,$udfile);
local($benvfile,$defect,$file,%zbuiltfiles,$rc,%benvlistplus);
local ($changefile,%changefiles,$changeline,$changedefect,$changes);
$rc=$SUCCESS;
chop($workpath=`ksh bldreleasepath $release`);
$path="$workpath/bldtd";
`rm -fr $path`; mkdir($path,0750);
dbmopen(sourcefd,"$path/sourcefd",0750) ||
&log("$lvar -x","$path/sourcefd open error ($!)");
dbmopen(targetfd,"$path/targetfd",0750) ||
&log("$lvar -x","$path/targetfd open error ($!)");
if (defined $ENV{'BLDBASERELEASE'})
{ $baserel = $ENV{'BLDBASERELEASE'}; }
else {
$baserel = "bos";
$baserel .= &bldhostsfile_perl("get_afs_base",$FALSE,"HOSTSFILE_BLDNODE");
chop $baserel;
if ( $baserel eq "bos" ) {
&log("$lvar -x",
"bldhostsfile_perl(get_afs_base,$FALSE,HOSTSFILE_BLDNODE) failed");
}
}
open (MAKELIST,"<$makelist") ||
&log("$lvar -x","makelist ($makelist) open error ($!)");
while ($makeline = <MAKELIST>) {
chop $makeline;
($target,$dependency,$built) = split(/ /,$makeline,3);
next if ($target eq $dependency);
if ($target eq "" || $dependency eq "") {
&log("$lvar -e","missing token in make line $. ($makeline)");
next;
}
if (defined $built && $built ne "" && $built ne "NEW") {
&log("$lvar -e","illegal type in make line $. ($makeline)");
next;
}
if ($release eq $baserel) {
if ($dependency =~ m
&log("$lvar -w",
"unexpected /bldenv dependency in make line $. ($makeline)");
}
}
if ($dependency =~ m
&log("$lvar -w",
"unexpected host dependency in make line $. ($makeline)");
}
$target=&Encodepath($target); $dependency=&Encodepath($dependency);
$alldepend[$target] .= $dependency . $SEP;
if (defined $built && $built eq "NEW") {
$newtarget[$dependency] .= $target . $SEP;
$newdepend[$target] .= $dependency . $SEP;
}
}
open (UPDATELIST,$updatelist) ||
&log("$lvar -x","updatelist ($updatelist) open error ($!)");
while ($udfile = <UPDATELIST>) {
chop $udfile;
$udlist{$udfile}=$DEFINED;
if ( $! != 0 ) {
&log("$lvar -x","updatelist ($updatelist) write error ($!)");
}
}
open (BLDENVLIST,$bldenvlist) ||
&log("$lvar -x","bldenvlist ($bldenvlist) open error ($!)");
while ($benvfile = <BLDENVLIST>) {
chop $benvfile;
$benvlist{$benvfile}=$DEFINED;
if ( $! != 0 ) {
&log("$lvar -x","bldenvlist ($bldenvlist) write error ($!)");
}
}
open (CHANGELIST,$changelist) ||
&log("$lvar -x","changelist ($changelist) open error ($!)");
while ($changeline = <CHANGELIST>) {
chop $changeline;
($changedefect,$changefile) = split(/\|/,$changeline);
(defined $changefiles{$changedefect}) ?
($changefiles{$changedefect} .= $changefile . $SEP) :
($changefiles{$changedefect} = $changefile . $SEP);
if ($newtarget[&Encodepath($changefile)] eq undef) {
if ($changefile !~ m/TOOLS/) {
&log("$lvar -w","$changefile missing NEW makelist entry");
}
}
}
(defined $ENV{'BLDOPTLIBS'}) &&
&OptimizeLibDeps($release,*newtarget,*newdepend,*alldepend,
*benvlist,*benvlistplus);
(&Openenvnames($release) == $SUCCESS) ||
&log("$lvar -x","cannot access other bldenv names");
(&Opendecodeddefects($release) == $SUCCESS) ||
&log("$lvar -x","cannot access decoded defects");
&log("$lvar -b","processing defect list");
open (DEFECTLIST,$defectlist) ||
&log("$lvar -x","defectlist ($defectlist) open error ($!)");
while ($defect = <DEFECTLIST>) {
chop $defect;
(defined $ENV{'DEBUG'}) && &log("$lvar -b","processing defect $defect");
chop ($changes=$changefiles{&Defectnumber($defect)});
foreach $file (split(/$SEP/,$changes)) {
undef $hastarget; reset 'z';
&Getbuiltlist ($file,*newtarget,*zbuiltfiles);
foreach $bfile (keys %zbuiltfiles) {
if ($udlist{$bfile} || $benvlist{$bfile}) {
&Appendlist(*targetfd,$bfile,
&Encodedefect($defect),$SEP);
$hastarget=1;
}	}
&Appendlist(*sourcefd,$file,$defect,$SEP) if ($hastarget);
}	}
&log("$lvar -b","saving new update dependents");
&Savedependents ($release,*udlist,"NEW",*newdepend);
&log("$lvar -b","saving new bldenv dependents");
&Savedependents ($release,*benvlist,"NEW",*newdepend);
&log("$lvar -b","saving all update dependents");
&Savedependents ($release,*udlist,"ALL",*alldepend);
&log("$lvar -b","saving all bldenv dependents");
&Savedependents ($release,*benvlistplus,"ALL",*alldepend);
foreach (keys %benvlist) {
print "$_\n";
}
&log("$lvar -b","saving bldenv names");
&Savebldenvnames ($release,*benvlistplus);
dbmclose(sourcefd); dbmclose(targetfd);
return $rc;
}
sub Getbuiltlist {
local($file,*newtarget,*builtfiles) = @_;
local($tfile);
push(@stack,(&Encodepath($file)));
while (($tfile=pop(@stack)) ne undef) {
next if ($builtfiles[$tfile] ne undef);
$builtfiles{&Decodepath($tfile)} = $DEFINED;
next if ($newtarget[$tfile] eq undef);
push(@stack,(split(/$SEP/,$newtarget[$tfile])));
if ($
&log ("$lvar -x","probably circular dependency with $file");
}
}
}
sub Appendlist {
local(*list,$key,$value,$sep) = @_;
local($listvalue,$exist); $exist=$FALSE;
foreach $listvalue (split(/$sep/,$list{$key}))
{ if ($listvalue eq $value) { $exist=$TRUE; } }
if ($exist==$FALSE) {
(defined $list{$key}) ?
($list{$key} .= $value . $sep) :
($list{$key} = $value . $sep);
if ( $! != 0 ) {
&log("$lvar -x","Appendlist write error ($!)");
}
}
}
sub Savedependents {
local($release,*filelist,$typeflag,*depends) = @_;
local($fileprefix,$file,%ydependentlist,$dfile,$workpath,$rc);
chop($workpath=`ksh bldreleasepath $release`);
$rc=$SUCCESS;
$fileprefix = $typeflag eq "NEW" ? "newdepend" : "alldepend";
foreach $file (keys %filelist) {
reset 'y';
&Finddependents ($file,$typeflag,*depends,*ydependentlist);
$file =~ s
$file =~ s
open (OUTFILE,">$workpath/bldtd/$fileprefix.$file") ||
&log("$lvar -x",
"unable to open $workpath/bldtd/$fileprefix.$file ($!)");
foreach $dfile (keys %ydependentlist) {
print OUTFILE "$dfile\n" ||
&log("$lvar -x",
"$workpath/bldtd/$fileprefix.$file output error ($!)");
}
close (OUTFILE);
}
return $rc;
}
sub BLDTDgettargetdefects {
local($release,$file) = @_; $rc=$SUCCESS;
local(%targetfd,$value,$rc);
$workpath=`ksh bldreleasepath $release`; chop $workpath;
dbmopen(targetfd,"$workpath/bldtd/targetfd",0750) ||
&log("$lvar -x","$workpath/bldtd/targetfd open error ($!)");
(&Opendecodeddefects($release) == $SUCCESS) ||
&log("$lvar -x","cannot access decoded defects");
&BLDTD2gettargetdefects($file,*value); print "$value\n";
dbmclose (targetfd);
return $rc;
}
sub BLDTD2gettargetdefects {
local($file,*value) = @_;
@dcodes=split(/$SEP/,$targetfd{$file});
grep($_=&Decodedefect($_),@dcodes);
$value=join($SEP,@dcodes);
}
sub BLDTDgetsrcdefects {
local($release) = @_;
local($workpath,$file,%sourcefd,$fdvalue,$rc);
$rc=$SUCCESS;
$workpath=`ksh bldreleasepath $release`; chop $workpath;
dbmopen(sourcefd,"$workpath/bldtd/sourcefd",0750) ||
&log("$lvar -x","$workpath/bldtd/sourcefd open error ($!)");
foreach $file (keys %sourcefd)
{ chop($fdvalue=$sourcefd{$file}); print "$file|$fdvalue\n"; }
dbmclose (sourcefd);
return $rc;
}
sub Finddependents {
local($file,$typeflag,*depends,*tdependentlist) = @_;
local (%tdslist,$dependent,@list,$listitem,$release,$workpath);
&Getterminaldepends ($file,*depends,*tdslist);
foreach $dependent (keys %tdslist) {
if ($typeflag eq "ALL" &&
($release=&Otherbuildenv($dependent)) ne undef) {
$workpath=`ksh bldreleasepath $release`; chop $workpath;
&BLDTDgetdependentslist
($workpath,$dependent,$typeflag,*list);
while (($listitem=pop(@list)) ne undef) {
chop ($listitem);
$tdependentlist{$listitem}=$DEFINED;
}
}
else { $tdependentlist{$dependent}=$DEFINED; }
}
}
sub Getterminaldepends {
local($file,*depends,*tdslist) = @_;
local(@dependents,$tfile);
$tfile=&Encodepath($file);
push(@stack,($tfile));
while (($tfile=pop(@stack)) ne undef) {
$file=&Decodepath($tfile);
next if ($tdslist{$file} ne undef);
if ($depends[$tfile] eq undef) {
$tdslist{$file}=$DEFINED;
}
else {
@dependents=(split(/$SEP/,$depends[$tfile]));
push(@stack,(@dependents));
if ($
&log ("$lvar -x","probably circular dependency ($file)");
}
}
}
}
sub BLDTDgetdependents {
local($release,$file,$typeflag) = @_;
local(@dependentlist,$rc);
$workpath=`ksh bldreleasepath $release`; chop $workpath;
$rc=&BLDTDgetdependentslist ($workpath,$file,$typeflag,*dependentlist);
print @dependentlist;
return $rc;
}
sub BLDTDgetdependentslist {
local($workpath,$file,$typeflag,*dependentlist) = @_;
local($fileprefix,$rc); $rc=$SUCCESS;
$fileprefix = $typeflag eq "NEW" ? "newdepend" : "alldepend";
$file =~ s
open (FILELIST,"<$workpath/bldtd/$fileprefix.$file") || return $FAILURE;
while (<FILELIST>) {
push(@dependentlist,($_));
}
close (FILELIST);
return $SUCCESS;
}
sub Openenvnames {
local($release) = @_;
local($rc); $rc=$SUCCESS;
chop($workpath=`ksh bldglobalpath`);
dbmopen(bldenvnames,"$workpath/bldenvnames",0750) ||
&log("$lvar -e","$workpath/bldenvnames open error ($!)");
return $rc;
}
sub Savebldenvnames {
local($release,*bldenvlist) = @_;
foreach (keys %bldenvlist) {
s
$bldenvnames{$_}=$release;
if ( $! != 0 ) {
&log("$lvar -x","Savebldenvnames ($workpath/bldenvnames) write error ($!)");
}
}
dbmclose (bldenvnames);
}
sub Otherbuildenv {
local($file) = @_;
return $bldenvnames{$file};
}
sub Opendecodeddefects {
local($release) = @_;
local($workpath,$rc); $rc=$SUCCESS;
$workpath=`ksh bldreleasepath $release`; chop $workpath;
dbmopen(decodeddefects,"$workpath/bldtd/decodeddefects",0750) ||
&log("$lvar -e","$workpath/bldtd/decodeddefects open error ($!)");
return $rc;
}
sub Encodedefect {
local($defect) = @_;
if ($encodeddefects{$defect} eq undef) {
$encodeddefects{$defect} = ++$curdefcode;
$decodeddefects{$curdefcode} = $defect;
if ( $! != 0 ) {
&log("$lvar -x","Encodedefect ($workpath/bldtd/decodeddefects) write error ($!)");
}
}
return ($encodeddefects{$defect});
}
sub Decodedefect {
local($code) = @_;
if (($code ne undef) && ($decodeddefects{$code} eq undef)) {
&log("-e","unable to decode bldtd defect code $code");
}
return ($decodeddefects{$code});
}
