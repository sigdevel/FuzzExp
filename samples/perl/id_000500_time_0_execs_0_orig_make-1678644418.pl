my %regex = (
extname  => qr/^[A-Z][A-Za-z0-9_]+$/,
exturl   => qr/^http.+$/,
function => qr/^(.+) ([a-z][a-z0-9_]*) \((.*)\)$/i,
token    => qr/^([A-Z][A-Z0-9_x]*)\s+((?:0x)?[0-9A-Fa-f]+(u(ll)?)?|[A-Z][A-Z0-9_]*)$/,
type     => qr/^typedef\s+(.+)$/,
exact    => qr/.*;$/,
);
sub prefixname($)
{
my $name = $_[0];
$name =~ s/^(.*?)gl/__$1glew/;
return $name;
}
sub prefix_varname($)
{
my $name = $_[0];
$name =~ s/^(.*?)GL(X*?)EW/__$1GL$2EW/;
return $name;
}
sub make_exact($)
{
my $exact = $_[0];
$exact =~ s/(; |{)/$1\n/g;
return $exact;
}
sub make_separator($)
{
my $extname = $_[0];
my $l = length $extname;
my $s = (71 - $l)/2;
print "/* ";
my $j = 3;
for (my $i = 0; $i < $s; $i++)
{
print "-";
$j++;
}
print " $_[0] ";
$j += $l + 2;
while ($j < 76)
{
print "-";
$j++;
}
print " */\n\n";
}
sub parse_ext($)
{
my $filename = shift;
my %functions = ();
my %tokens = ();
my @reuse = ();
my @types = ();
my @exacts = ();
my $extname = "";
my $exturl = "";
my $extstring = "";
open EXT, "<$filename" or return;
$extname   = readline(*EXT);
$exturl    = readline(*EXT);
$extstring = readline(*EXT);
@reuse     = split(" ", readline(*EXT));
chomp($extname);
chomp($exturl);
chomp($extstring);
while(<EXT>)
{
chomp;
if (s/^\s+//)
{
if (/$regex{exact}/)
{
push @exacts, $_;
}
elsif (/$regex{type}/)
{
push @types, $_;
}
elsif (/$regex{token}/)
{
my ($name, $value) = ($1, $2);
$tokens{$name} = $value;
}
elsif (/$regex{function}/)
{
my ($return, $name, $parms) = ($1, $2, $3);
$functions{$name} = {
rtype => $return,
parms => $parms,
};
} else {
print STDERR "'$_' matched no regex.\n";
}
}
}
close EXT;
return ($extname, $exturl, $extstring, \@reuse, \@types, \%tokens, \%functions, \@exacts);
}
sub output_tokens($$)
{
my ($tbl, $fnc) = @_;
if (keys %{$tbl})
{
local $, = "\n";
print "\n";
print map { &{$fnc}($_, $tbl->{$_}) } sort {
if (${$tbl}{$a} eq ${$tbl}{$b}) {
$a cmp $b
} else {
if (${$tbl}{$a} =~ /_/) {
if (${$tbl}{$b} =~ /_/) {
$a cmp $b
} else {
-1
}
} else {
if (${$tbl}{$b} =~ /_/) {
1
} else {
if (hex ${$tbl}{$a} eq hex ${$tbl}{$b}) {
$a cmp $b
} else {
hex ${$tbl}{$a} <=> hex ${$tbl}{$b}
}
}
}
}
} keys %{$tbl};
print "\n";
} else {
print STDERR "no keys in table!\n";
}
}
sub output_types($$)
{
my ($tbl, $fnc) = @_;
if (scalar @{$tbl})
{
local $, = "\n";
print "\n";
print map { &{$fnc}($_) } sort @{$tbl};
print "\n";
}
}
sub output_decls($$)
{
my ($tbl, $fnc) = @_;
if (keys %{$tbl})
{
local $, = "\n";
print "\n";
print map { &{$fnc}($_, $tbl->{$_}) } sort keys %{$tbl};
print "\n";
}
}
sub output_exacts($$)
{
my ($tbl, $fnc) = @_;
if (scalar @{$tbl})
{
local $, = "\n";
print "\n";
print map { &{$fnc}($_) } sort @{$tbl};
print "\n";
}
}
sub output_reuse($$)
{
my ($tbl, $fnc) = @_;
if (scalar @{$tbl})
{
local $, = "\n";
print "\n";
print map { &{$fnc}($_) } sort @{$tbl};
print "\n";
}
}
