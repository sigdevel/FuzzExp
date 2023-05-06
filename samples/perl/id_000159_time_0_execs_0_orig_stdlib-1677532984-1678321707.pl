my $PLX_INTERPRET_BUILTINS = 1;
my %func = ();
my @builtins = qw(uc lc shift push pop);
my $debug = 0;
sub expand {
my ($val, $x, $o) = '';
my $line = shift;
print "EXPAND:$line" if $debug;
$o = $line;
for $x (keys %func) {
$o =~ s/$x/&{$func{$x}}/ge;
}
if ($PLX_INTERPRET_BUILTINS) {
for $x (@builtins) {
$o =~ s/($x\([^\)]+?\))/eval $1/ge;
}
}
if ($o ne $line) {
$o = expand($o);
}
return $o;
}
while (($k,$v) = each %{*{'::'}} ) {
local *g = $v;
if( defined $v && defined *g{CODE}) {
$func{$k} = $v;
}
}
while(<DATA>) {
print expand($_);
}
1;
