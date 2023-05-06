#!/usr/bin/perl
print "Enter an IP Address: ";
$_ = <STDIN>;
chomp($_);
$converteddecimal = ip2dec($_);
$convertedip = dec2ip($converteddecimal);
print "\nIP address: $_\n";
print "Decimal: $converteddecimal\n";
sub dec2ip ($) {
join '.', unpack 'C4', pack 'N', shift;
}
sub ip2dec ($) {
unpack N => pack CCCC => split /\./ => shift;
}
