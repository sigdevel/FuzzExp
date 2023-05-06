sub ev
{my $exp = shift;
$exp =~ tr {0-9.+-/*()} {}cd;
return ev_ast(astize($exp));}
{my $balanced_paren_regex;
$balanced_paren_regex = qr
{\( ( [^()]+ | (??{$balanced_paren_regex}) )+ \)}x;
sub astize
{my $exp = shift;
$exp =~ /[^0-9.]/ or return $exp;
$exp = substr($exp, 1, -1)
while $exp =~ /\A($balanced_paren_regex)\z/;
my @paren_contents;
$exp =~ s {($balanced_paren_regex)}
{push(@paren_contents, $1);
"[p$
$exp =~ m{(.+) ([+-]) (.+)}x or
$exp =~ m{(.+) ([*/]) (.+)}x or
die "Eh?: [$exp]\n";
my ($op, $lo, $ro) = ($2, $1, $3);
s {\[p(\d+)\]} {($paren_contents[$1])}eg
foreach $lo, $ro;
return [$op, astize($lo), astize($ro)];}}
{my %ops =
('+' => sub {$_[0] + $_[1]},
'-' => sub {$_[0] - $_[1]},
'*' => sub {$_[0] * $_[1]},
'/' => sub {$_[0] / $_[1]});
sub ev_ast
{my $ast = shift;
ref $ast or return $ast;
my ($op, @operands) = @$ast;
$_ = ev_ast($_) foreach @operands;
return $ops{$op}->(@operands);}}
