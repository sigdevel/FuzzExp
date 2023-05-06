#!/usr/bin/perl -w
%allsections = ();
%allsectionslist = ();
%secnames = (
"input" => "0",
"required" => "0",
"additional" => "0",
"advanced" => "0",
"output" => "0",
"unknown" => "0"
);
%secnumber = (
"input" => "1",
"required" => "2",
"additional" => "3",
"advanced" => "4",
"output" => "5",
"unknown" => "0"
);
sub numerically { $allsections{$b} <=> $allsections{$a} }
sub numericallyb { $secnames{$b} <=> $secnames{$a} }
chdir( "$ENV{HOME}/local/share/EMBOSS/acd/");
opendir (ACD,".");
while ($acdfile = readdir(ACD)) {
if ($acdfile !~ /(.*).acd$/) {
next;
}
if ($acdfile =~ /^[.]/) {
next;
}
open (ACDFILE, $acdfile) || die "Cannot open $acdfile";
$sections = "";
$secnum = 0;
$secname = "unknown";
while ($acdline = <ACDFILE>) {
if ($acdline =~ /^\s*section:\s+(\S+)/) {
if (defined($secnames{$1})) {
$secname = $1;
$calc=0;
if ($secnumber{$secname} <= $secnum) {
print "$acdfile: section $secname out of order $secnumber{$secname} <= $secnum\n";
}
}
}
if ($acdline =~ /\$[\(]/) {
$calc++;
}
if ($acdline =~ /^\s*endsection:\s+(\S+)/) {
if ($1 eq $secname) {
$secnames{$1}++;
$secnum = $secnumber{$secname};
if ($sections ne "") {$sections .= ";"}
$sections .= $1;
if ($calc) {
$sections .= "+";
}
}
}
}
close ACDFILE;
$allsections{$sections}++;
$allsectionslist{$sections} .= "$acdfile\n";
}
foreach $x (sort numericallyb keys (%secnames)) {
printf "%4d %s\n", $secnames{$x}, $x;
}
print "=============\n";
foreach $x (sort numerically keys (%allsections)) {
printf "%4d %s\n", $allsections{$x}, $x;
print "$allsectionslist{$x}";
}
