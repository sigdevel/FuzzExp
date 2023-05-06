#!/usr/bin/perl -w
=pod
@temp = ("while", "for", "if", "elif");
foreach $item (@ARGV) {
if (grep {$_ eq $item} @temp) {
print "-----------------\n";
}
print $item;
print "\n";
}
=pod2
$string = "welcome to runoob site.";
while (1) {
$string =~ m/(\w+)/;
}
print "数组：$a[0]\n";
print "数组：$a[1]\n";
print "数组：$a[2]\n";
print "数组：$a[3]\n";
print "匹配前的字符串: $`\n";
print "匹配的字符串: $&\n";
print "匹配后的字符串: $'\n"
=cut
=pod
$a = "(dqwdfq)";
if ($a =~ m/^\(/) {
$a =~ s/^\(//g;
$a =~ s/\)$//g;
}
print "$a\n"
=cut
$l = "AAAABcBBfbB";
if ($l =~ m/^A((A[^AB]*)(?1)?(B[^AB]*))B$/) {
print "=========\n";
}
@a = (1,2,3);
$r =  @a;
print $r,"\n";
=pod
@variables = ("a","b");
@arrays = ();
$line = "a= b";
sub addDollar {
foreach $arg (@_) {
foreach $var (@variables) {
$arg =~ s/ $var/ \$$var/g;
$arg =~ s/\t$var/\t\$$var/g;
$arg =~ s/\($var/\(\$$var/g;
$arg =~ s/\[$var/\[\$$var/g;
$arg =~ s/\.$var/\.\$$var/g;
$arg =~ s/\*$var/\*\$$var/g;
$arg =~ s/^$var/\$$var/;
}
foreach $var (@arrays) {
if ($arg =~ /$var\[/) {
$arg =~ s/ $var/ \$$var/g;
$arg =~ s/\t$var/\t\$$var/g;
$arg =~ s/\($var/\(\$$var/g;
$arg =~ s/\[$var/\[\$$var/g;
$arg =~ s/\.$var/\.\$$var/g;
$arg =~ s/\*$var/\*\$$var/g;
$arg =~ s/^$var/\$$var/;
} else {
$arg =~ s/ $var/ \@$var/g;
$arg =~ s/\t$var/\t\@$var/g;
$arg =~ s/\($var/\(\@$var/g;
$arg =~ s/\[$var/\[\@$var/g;
$arg =~ s/\.$var/\.\@$var/g;
$arg =~ s/^$var/\@$var/;
}
}
$arg =~ s/\$?i\$?f/if/g;
$arg =~ s/\$?w\$?h\$?i\$?l\$?e/while/g;
$arg =~ s/\$?p\$?r\$?i\$?n\$?t/print/g;
}
}
addDollar($line);
print $line, "\n";
=cut
@a = (2,3);
if ($a[0] == 2) {
print "----\n";
}
elsif ($a[1] == 3) {
print "++++\n";
}
else {
print "[[[[\n";
}
