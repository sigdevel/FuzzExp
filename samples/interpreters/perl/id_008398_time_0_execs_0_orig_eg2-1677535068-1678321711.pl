#!/usr/bin/perl -w
open time, "date|" || die "cannot pipe from date: $!\n";
close time;
die "time: nonzero exit of $?" if $?;
open F, "find / -atime +90 -size +1000 -print|" or die "fork: $!";
while (<F>) {
chomp;
printf "%s size %dK last accessed on %s\n",
$_, (1023 + -s $_)/1024, -A $_;
}
