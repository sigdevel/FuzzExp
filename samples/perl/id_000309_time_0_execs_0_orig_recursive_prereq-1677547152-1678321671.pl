#!/usr/bin/perl -w
$debug = 0;
$recursive = 0;
$year = 1900 + (localtime(time))[5];
$url_base = "http://www.handbook.unsw.edu.au/";
$url_ugrad = "$url_base/undergraduate/courses/$year";
$url_pgrad = "$url_base/postgraduate/courses/$year";
sub prereq {
my ($course) = @_;
print STDERR "prereq($course) $url_ugrad/$course.html $url_pgrad/$course.html\n" if $debug;
open my $f, '-|', "wget -q -O- $url_ugrad/$course.html $url_pgrad/$course.html" or die;
my (@prereqs, $line);
while ($line = <$f>) {
next if $line !~ /pre.?(requisite)?(.?:|\s+[A-Z]{4}\d{4})/i;
$line = uc $line;
$line =~ s/<[^>]*>/ /g;
$line =~ s/EXCLU.*/ /i;
my @courses = $line =~ /([A-Z]{4}\d{4})/g;
push @prereqs, @courses;
}
print STDERR "prereq($course) -> @prereqs\n" if $debug;
foreach my $course (@prereqs) {
prereq($course) if !$prereqs{$course}++ && $recursive;
}
close $f;
}
foreach $arg (@ARGV)
{
if ($arg eq "-r") {
$recursive = 1;
next;
}
else {
prereq($arg);
}
}
print "$_\n" foreach sort keys %prereqs;
