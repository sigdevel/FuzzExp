#!/usr/bin/perl -w
if (@ARGV != 2) {
die
}
open my $file1, '<', $ARGV[0] or die "Can't open $ARGV[0]: $!";
while ($word = <$file1>) {
chomp $word;
$dic_word{$word} = "in A";
}
close $file1;
open my $file2, '<', $ARGV[1] or die "Can't open $ARGV[1]: $!";
while ($word = <$file2>) {
chomp $word;
$dic_word{$word} = "in B";
}
close $file2;
foreach $word (sort keys %dic_word) {
if ($dic_word{$word} eq "in A" && $dic_word{$word} ne "in B") {
print "$word\n";
}
}
