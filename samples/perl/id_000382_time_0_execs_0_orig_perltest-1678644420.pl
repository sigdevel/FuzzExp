#! /usr/bin/env perl
sub pchars {
my($t) = "";
if ($utf8)
{
@p = unpack('U*', $_[0]);
foreach $c (@p)
{
if ($c >= 32 && $c < 127) { $t .= chr $c; }
else { $t .= sprintf("\\x{%02x}", $c);
}
}
}
else
{
foreach $c (split(//, $_[0]))
{
if (ord $c >= 32 && ord $c < 127) { $t .= $c; }
else { $t .= sprintf("\\x%02x", ord $c); }
}
}
$t;
}
if (@ARGV > 0)
{
open(INFILE, "<$ARGV[0]") || die "Failed to open $ARGV[0]\n";
$infile = "INFILE";
}
else { $infile = "STDIN"; }
if (@ARGV > 1)
{
open(OUTFILE, ">$ARGV[1]") || die "Failed to open $ARGV[1]\n";
$outfile = "OUTFILE";
}
else { $outfile = "STDOUT"; }
printf($outfile "Perl $] Regular Expressions\n\n");
NEXT_RE:
for (;;)
{
printf "  re> " if $infile eq "STDIN";
last if ! ($_ = <$infile>);
printf $outfile "$_" if $infile ne "STDIN";
next if ($_ =~ /^\s*$/ || $_ =~ /^< forbid/);
$pattern = $_;
while ($pattern !~ /^\s*(.).*\1/s)
{
printf "    > " if $infile eq "STDIN";
last if ! ($_ = <$infile>);
printf $outfile "$_" if $infile ne "STDIN";
$pattern .= $_;
}
chomp($pattern);
$pattern =~ s/\s+$//;
$showrest = ($pattern =~ s/\+(?=[a-zA-Z]*$)//);
$pattern =~ s/\+(?=[a-zA-Z]*$)//;
$utf8 = $pattern =~ s/8(?=[a-zA-Z]*$)//;
$pattern =~ s/J(?=[a-zA-Z]*$)//;
$pattern =~ s/K(?=[a-zA-Z]*$)//;
$pattern =~ s/W(?=[a-zA-Z]*$)/u/;
$pattern =~ s/S(?=[a-zA-Z]*$)//g;
$pattern =~ s/[YO](?=[a-zA-Z]*$)//;
eval "\$_ =~ ${pattern}";
if ($@)
{
printf $outfile "Error: $@";
if ($infile != "STDIN")
{
for (;;)
{
last if ! ($_ = <$infile>);
last if $_ =~ /^\s*$/;
}
}
next NEXT_RE;
}
$cmd = ($pattern =~ /g[a-z]*$/)? "while" : "if";
$pattern = "/(?
for (;;)
{
printf "data> " if $infile eq "STDIN";
last NEXT_RE if ! ($_ = <$infile>);
chomp;
printf $outfile "$_\n" if $infile ne "STDIN";
s/\s+$//;
s/^\s+//;
s/\\Y//g;
last if ($_ eq "");
$x = eval "\"$_\"";
@subs = ();
$pushes = "push \@subs,\$&;" .
"push \@subs,\$1;" .
"push \@subs,\$2;" .
"push \@subs,\$3;" .
"push \@subs,\$4;" .
"push \@subs,\$5;" .
"push \@subs,\$6;" .
"push \@subs,\$7;" .
"push \@subs,\$8;" .
"push \@subs,\$9;" .
"push \@subs,\$10;" .
"push \@subs,\$11;" .
"push \@subs,\$12;" .
"push \@subs,\$13;" .
"push \@subs,\$14;" .
"push \@subs,\$15;" .
"push \@subs,\$16;" .
"push \@subs,\$'; }";
undef $REGERROR;
undef $REGMARK;
eval "${cmd} (\$x =~ ${pattern}) {" . $pushes;
if ($@)
{
printf $outfile "Error: $@\n";
next NEXT_RE;
}
elsif (scalar(@subs) == 0)
{
printf $outfile "No match";
if (defined $REGERROR && $REGERROR != 1)
{ printf $outfile (", mark = %s", &pchars($REGERROR)); }
printf $outfile "\n";
}
else
{
while (scalar(@subs) != 0)
{
printf $outfile (" 0: %s\n", &pchars($subs[0]));
printf $outfile (" 0+ %s\n", &pchars($subs[17])) if $showrest;
$last_printed = 0;
for ($i = 1; $i <= 16; $i++)
{
if (defined $subs[$i])
{
while ($last_printed++ < $i-1)
{ printf $outfile ("%2d: <unset>\n", $last_printed); }
printf $outfile ("%2d: %s\n", $i, &pchars($subs[$i]));
$last_printed = $i;
}
}
splice(@subs, 0, 18);
}
if (defined $REGMARK && $REGMARK != 1)
{
$xx = $REGMARK;
$xx = Encode::decode_utf8($xx) if $utf8;
printf $outfile ("MK: %s\n", &pchars($xx));
}
}
}
}
