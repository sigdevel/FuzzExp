#!/usr/bin/perl
$mask = pack("CCCC", $ARGV[0], $ARGV[1], $ARGV[2], $ARGV[3]);
$bits += unpack("%32b*", $mask);
print "$bits\n";
