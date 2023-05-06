#!/usr/bin/env perl
local $/;
$text = <>;
my %max_width = ();
my @alignments = ();
my $less_than_tab = 3;
my $line_start = qr{
[ ]{0,$less_than_tab}
}mx;
my $table_row = qr{
[^\n]*?\|[^\n]*?\n
}mx;
my $first_row = qr{
$line_start
\S+.*?\|.*?\n
}mx;
my $table_rows = qr{
(?:\n?$table_row)
}mx;
my $table_caption = qr{
$line_start
\[.*?\][ \t]*\n
}mx;
my $table_divider = qr{
$line_start
[\|\-\+\:\.][ \-\+\|\:\.]*?\|[ \-\+\|\:\.]*
}mx;
my $whole_table = qr{
($table_caption)?
($first_row
($table_row)*?)?
$table_divider
$table_rows+
\n?[^\n]*?\|[^\n]*?
($table_caption)?
}mx;
$text =~ s{
^($whole_table)
(\n|\Z)
}{
my $table = $1 . "\n";
my $table_original = $table;
$result = "";
@alignments = ();
%max_width = ();
$table =~ s/^$line_start\[\s*(.*?)\s*\](\[\s*(.*?)\s*\])?[ \t]*$//m;
$table =~ s/\n$line_start\[\s*(.*?)\s*\][ \t]*\n/\n/s;
$table = "\n" . $table;
$table =~ s/\n($table_divider)\n($table_rows+)//s;
my $alignment_string = $1;
my $body = $2;
my $header = $table;
while ($alignment_string =~ /\|?\s*(.+?)\s*(\||\Z)/gs) {
my $cell = $1;
if ($cell =~ /\:$/) {
if ($cell =~ /^\:/) {
push(@alignments,"center");
} else {
push(@alignments,"right");
}
} else {
if ($cell =~ /^\:/) {
push(@alignments,"left");
} else {
if (($cell =~ /^\./) || ($cell =~ /\.$/)) {
push(@alignments,"char");
} else {
push(@alignments,"");
}
}
}
}
$table = $header . "\n" . $body;
foreach my $line (split(/\n/, $table)) {
my $count = 0;
while ($line =~ /(\|?\s*[^\|]+?\s*(\|+|\Z))/gs) {
my $cell = $1;
my $ending = $2;
if ($ending =~ /\|\|/) {
$count += (length($ending));
next;
}
setWidth($count, $cell);
$count++
}
}
foreach my $line (split(/\n/, $table)) {
my $count = 0;
while ($line =~ /(\|?\s*[^\|]+?\s*(\|+|\Z))/gs) {
my $cell = $1;
my $ending = $2;
if ($ending =~ /\|\|/) {
setWidth($count, $cell);
$count += (length($ending));
next;
}
$count++
}
}
$table_original =~ s{
\n($table_divider)\n
}{
my $divider = $1;
my $count = 0;
$divider =~ s{
(\|?)\s*([^\|]+?)\s*(\|+|\Z)
}{
my $opening = $1;
my $cell = $2;
my $ending = $3;
my $result = "";
my $goal_length = $max_width{$count} -3;
if ($count == 0) {
if ($opening eq ""){
$goal_length++;
} else {
$goal_length--;
}
}
if ($cell =~ /^\:/) {
$goal_length--;
$result = ":";
}
if ($cell =~ /[\:\+]$/) {
$goal_length--;
}
for (my $i=0;$i < $goal_length;$i++){
$result.="-";
}
if ($cell =~ /\:$/) {
$result .=":";
}
if ($cell =~ /\+$/) {
$result .="+";
}
$count++;
$opening . "$result" . $ending;
}xsge;
"\n$divider\n";
}sxe;
$table_original =~ s{
(.*)
}{
$line = $1;
my $result = "";
my $count = 0;
if (($line =~ /^\[/) && ($line !~ /\|/)){
$result .= $line;
} else {
while ($line =~ /(\|?)\s*([^\|]+?)\s*(\|+|\Z)/gs) {
my $opening = $1;
my $cell = $2;
my $ending = $3;
my $lead = 0;
my $pad_lead = 0;
my $pad_trail = 0;
my $len = length($2);
if ($count > 0) {
$pad_lead = 1;
} elsif (length($opening) > 0) {
$pad_lead = 1;
}
if (length($ending) > 0) {
$pad_trail = 1;
}
my $width = 0;
if ($ending =~ /\|/) {
$width = maxWidth($count,length($ending));
} else {
$width = maxWidth($count, 1);
}
if ($alignments[$count] =~ /^(left)?$/) {
$lead = $len + $pad_lead;
$trail = $width - $lead  - length($opening);
}
if ($alignments[$count] =~ /^right$/) {
if ($count == 0) {
if ($opening eq "") {
$opening = "|";
$pad_lead = 1;
$width++;
}
}
$trail = $pad_trail+length($ending);
$lead = $width - $trail - length($opening);
}
if ($alignments[$count] =~ /^center$/) {
if ($count == 0) {
if ($opening eq "") {
$opening = "|";
$pad_lead = 1;
$width++;
}
}
my $pad_total =  $width - $len;
$pad_lead = int($pad_total/2)+1;
$pad_trail = $pad_total - $pad_lead;
$trail = $pad_trail+length($ending);
$lead = $width - $trail - length($opening);
}
$result .= $opening . sprintf("%*s", $lead, $cell) . sprintf("%*s", $trail, $ending);
if ($ending =~ /\|\|/) {
$count += (length($ending));
} else {
$count++;
}
}
}
$result;
}xmge;
$table_original;
}xsge;
print $text;
sub maxWidth {
my ($start_col, $cols) = @_;
my $total = 0;
for (my $i = $start_col;$i < ($start_col + $cols);$i++) {
$total += $max_width{$i};
}
return $total;
}
sub setWidth {
my ($start_col, $cell) = @_;
$cell =~ /(\|?)\s*([^\|]+?)\s*(\|+|\Z)/;
my $opening = 	$1;
my $contents =	$2;
my $closing =	$3;
my $padding =	0;
$padding++ if (length($opening) > 0);
$padding++ if ($start_col > 0);
$padding++ if (length($closing) > 0);
$contents =~ s/&\s*(.*?)\s*$/$1/;
my $cell_length = length($contents) + $padding + length($opening)  + length($closing);
if ($closing =~ /\|\|/) {
my @current_max = ();
my $cols = length($closing);
my $current_total = 0;
for (my $i = $start_col;$i < ($start_col + $cols);$i++) {
$current_total += $max_width{$i};
}
if ($current_total < $cell_length) {
my %columns = ();
for (my $i = $start_col; $i < ($start_col + $cols);$i++) {
$max_width{$i} = int($max_width{$i} * ($cell_length/$current_total));
$columns{$i} = $max_width{$i};
}
$current_total = 0;
for (my $i = $start_col;$i < ($start_col + $cols);$i++) {
$current_total += $max_width{$i};
}
my $missing = $cell_length - $current_total;
foreach my $a_col (sort { $max_width{$b} <=> $max_width{$a} }keys %columns) {
if ($missing > 0) {
$max_width{$a_col}++;
$missing--;
}
}
}
} else {
if ($max_width{$start_col}< $cell_length) {
$max_width{$start_col} = $cell_length;
}
}
}
