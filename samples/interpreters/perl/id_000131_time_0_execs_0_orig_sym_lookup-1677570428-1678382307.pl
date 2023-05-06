#! /usr/bin/perl
$noteview = shift(ARGV);
$formatted_noteview = shift(ARGV);
$usermemos = shift(ARGV);
$error = shift(ARGV);
$dummy_symp = "START_SYMPTOM\nDUMMY SYMPTOM\nSTOP_SYMPTOM\n";
$dummy_symp =~ s/(\n)/"\376".ord($1)."\377"/eg;
&create_note_array;
&create_assoc_arrays;
&print_arrays($formatted_noteview,*symp_ary,$dummy_symp);
&print_arrays($usermemos,*memo_ary,"");
sub create_note_array{
local(@buffer);
open noteview || die "Could not open $noteview\n";
@buffer = <noteview>;
$i = -1;
for (0..$
if ($buffer[$_] =~ /^.*\|.*\|.*\|\d{2}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2}\|.*\|.*\|.*\|.*\|.*$/){
$i++;
$note_ary[$i] = $buffer[$_];
}
else{
$note_ary[$i] .= $buffer[$_];
}
}
undef @buffer;
}
sub create_assoc_arrays{
local($defect,$note,$symptom,$memo);
local($saint,$blessed_symp,$blessed_note);
local($infidel_override_symp,$infidel_override_memo);
open (ERROR,">$error") ||  die "Could not open $error\n";
foreach (@note_ary){
$/ = "";
$* = 1;
local(@ary) = split(/\|/,$_,9);
print ERROR "$defect\n"
if (($defect ne "") && ($defect ne $ary[0]) &&
($symp_ary{$defect} =~ /^$/));
if ($defect ne $ary[0]) {
$blessed_symp = 0;
$blessed_note = 0;
if ($defect ne "" && $infidel_override_symp == 1) {
print STDERR "$defect: attempt to override ";
print STDERR "mustfix attached symptom ignored\n";
}
if ($defect ne "" && $infidel_override_note == 1) {
print STDERR "$defect: attempt to override ";
print STDERR "mustfix attached memo ignored\n";
}
$infidel_override_symp = 0;
$infidel_override_note = 0;
}
$defect = $ary[0];
$note = $ary[8];
$login = $ary[4];
if ($login =~ m/^mustfix.*/) {
$saint = 1;
}
else {
$saint = 0;
}
$note =~ s/(\n)/"\376".ord($1)."\377"/eg;
if ($note =~ /^.*[(\376\d+\377)][(\376\d+\377)\s]*[Ss][tT][aA][rR][tT]_[sS][yY][mM][pP][tT][oO][mM].*[sS][tT][oO][pP]_[sS][yY][mM][pP][tT][oO][mM].*$|^[(\376\d+\377)\s]*[Ss][tT][aA][rR][tT]_[sS][yY][mM][pP][tT][oO][mM].*[sS][tT][oO][pP]_[sS][yY][mM][pP][tT][oO][mM].*$/){
if (($blessed_symp != 1) || ($saint == 1)) {
if ($saint == 1) {
$blessed_symp = 1;
$infidel_override_symp = 0;
}
$symptom = $note;
$symptom =~ s/^.*([Ss][tT][aA][rR][tT]_[sS][yY][mM][pP][tT][oO][mM].*[sS][tT][oO][pP]_[sS][yY][mM][pP][tT][oO][mM]).*$/$1/;
$symp_ary{$defect} = $symptom;
}
elsif (($blessed_symp == 1) && (saint != 1)) {
$infidel_override_symp = 1;
}
}
else{
$symp_ary{$defect} = ''
unless defined $symp_ary{$defect};
}
if ($note =~ /^.*[(\376\d+\377)][(\376\d+\377)\s]*[Ss][tT][aA][rR][tT]_[mM][eE][mM][oO].*[(\376\d+\377)\s]*[sS][tT][oO][pP]_[mM][eE][mM][oO].*$|^[(\376\d+\377)\s]*[Ss][tT][aA][rR][tT]_[mM][eE][mM][oO].*[(\376\d+\377)\s]*[sS][tT][oO][pP]_[mM][eE][mM][oO].*$/){
if (($blessed_note != 1) || ($saint == 1)) {
if ($saint == 1) {
$blessed_note = 1;
$infidel_override_note = 0;
}
$memo = $note;
$memo =~ s/^.*([Ss][tT][aA][rR][tT]_[mM][eE][mM][oO].*[sS][tT][oO][pP]_[mM][eE][mM][oO]).*$/$1/;
$memo_ary{$defect} = $memo;
}
elsif (($blessed_note == 1) && (saint != 1)) {
$infidel_override_note = 1;
}
}
else{
$memo_ary{$defect} = ''
unless defined $memo_ary{$defect};
}
}
print ERROR "$defect\n"
if ($symp_ary{$defect} =~ /^$/);
if ($defect ne "" && $infidel_override_symp == 1) {
print STDERR "$defect: attempt to override ";
print STDERR "mustfix attached symptom ignored\n";
}
if ($defect ne "" && $infidel_override_note == 1) {
print STDERR "$defect: attempt to override ";
print STDERR "mustfix attached memo ignored\n";
}
}
sub getfile_array{
local($file,*file_ary) = @_;
local($defect,$note);
if (-s $file){
open(INPUT,"<$file") || die "Could not open $file\n";
while (<INPUT>){
chop;
($defect,$note) = split(/\|/,$_,2);
if ( ! ($defect =~ /.*:.*/) )
{
$defect .= ":" . $ENV{'DEFAULT_CMVCFAMILY'};
}
$file_ary{$defect} = $note;
}
}
}
sub print_arrays{
local($file,*assc_ary,$dummy_symp) = @_;
local(%file_ary);
$/ = "\n";
$* = 0;
&getfile_array($file,*file_ary);
open (OUTPUT,">$file") ||
die "Could not open $file\n";
foreach (keys %assc_ary){
if ($assc_ary{$_} =~ /^$/){
if ((defined $ENV{'AREABLD'}) && ($dummy_symp ne "")) {
$file_ary{$_} = $dummy_symp;
} else {
next;
}
}
else{
$file_ary{$_} = $assc_ary{$_};
}
}
while (($defect,$note) = each %file_ary){
print OUTPUT "$defect|$note\n";
}
}
