#!/usr/bin/perl -w
my @list = sort {$a <=> $b} @ARGV;
$size = @list;
print "$list[($size-1)/2]\n";
