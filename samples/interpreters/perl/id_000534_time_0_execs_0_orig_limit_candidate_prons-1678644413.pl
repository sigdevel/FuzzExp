#!/usr/bin/env perl
if (@ARGV != 1 && @ARGV != 2) {
die "Usage: limit_candidate_prons.pl rule_hierarchy [candidate_prons] > limited_candidate_prons";
}
$hierarchy = shift @ARGV;
open(H, "<$hierarchy") || die "Opening rule hierarchy $hierarchy";
while(<H>) {
chop;
m:.+;.+: || die "Bad rule-hierarchy line $_";
$hierarchy{$_} = 1;
}
sub process_word;
undef $cur_word;
@cur_lines = ();
while(<>) {
chop;
m:^([^;]+);: || die "Unexpected input: $_";
$word = $1;
if (!defined $cur_word || $word eq $cur_word) {
if (!defined $cur_word) { $cur_word = $word; }
push @cur_lines, $_;
} else {
process_word(@cur_lines);
$cur_word = $word;
@cur_lines = ( $_ );
}
}
process_word(@cur_lines);
sub process_word {
my %pair2rule_list;
my @cur_lines = @_;
foreach my $line (@cur_lines) {
my ($word, $pron, $baseword, $basepron, $rulename, $destress, $rule_score) = split(";", $line);
my $key = $baseword.";".$basepron;
if (defined $pair2rule_list{$key}) {
push @{$pair2rule_list{$key}}, $line;
} else {
$pair2rule_list{$key} = [ $line ];
}
}
while ( my ($key, $value) = each(%pair2rule_list) ) {
my @lines = @$value;
my @stress, @rules;
for (my $n = 0; $n < @lines; $n++) {
my $line = $lines[$n];
my ($word, $pron, $baseword, $basepron, $rulename, $destress, $rule_score) = split(";", $line);
$stress[$n] = $destress;
$rules[$n] = $rulename;
}
for (my $m = 0; $m < @lines; $m++) {
my $ok = 1;
for (my $n = 0; $n < @lines; $n++) {
if ($m != $n && $stress[$m] eq $stress[$n]) {
if (defined $hierarchy{$rules[$n].";".$rules[$m]}) {
$ok = 0;
last;
}
}
}
if ($ok != 0) {
print $lines[$m] . "\n";
}
}
}
}
