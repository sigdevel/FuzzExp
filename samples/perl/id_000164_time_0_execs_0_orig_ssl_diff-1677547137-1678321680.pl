#!/usr/bin/perl
($pat, $xs, $h) = @ARGV;
open XS, $xs or die "Cant open .xs `$xs' ($!)\n";
foreach $_ (<XS>) {
next unless ($name) = /^($pat.*?)\(/o;
$xs{$name} = 1;
}
close XS;
open H, $h or die "Cant open .h `$h' ($!)\n";
foreach $_ (<H>) {
next unless ($name) = /($pat.*?)\(/o;
print "$name\n" unless $xs{$name};
}
close H;
__END__
