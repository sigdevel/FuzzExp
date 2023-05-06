#!/usr/bin/perl -w
BEGIN {
if ($0 =~ /\//) {
(my $searchpath) = ($0 =~ /(.+)\/[^\/]+/);
push @INC, $searchpath;
}
}
use strict;
use Getopt::Long;
use requestlog qw(parseRequestLog);
my $path;
sub printEntry (%) {
my %record=@_;
print "[" . $record{"timestamp"}  . "] ". $record{"method"} . " " .  $record{"handle"} . " => " . $record{"duration"} . " ms, statuscode= " . $record{"statuscode"} . "\n" ;
}
foreach my $logfile (@ARGV) {
parseRequestLog($logfile,undef, \&printEntry);
}
