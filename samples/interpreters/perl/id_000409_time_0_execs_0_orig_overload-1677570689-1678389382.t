#!./perl
BEGIN {
chdir 't' if -d 't';
@INC = '../lib';
}
package Oscalar;
use overload (
'+'	=>	sub {new Oscalar $ {$_[0]}+$_[1]},
'-'	=>	sub {new Oscalar
$_[2]? $_[1]-${$_[0]} : ${$_[0]}-$_[1]},
'<=>'	=>	sub {new Oscalar
$_[2]? $_[1]-${$_[0]} : ${$_[0]}-$_[1]},
'cmp'	=>	sub {new Oscalar
$_[2]? ($_[1] cmp ${$_[0]}) : (${$_[0]} cmp $_[1])},
'*'	=>	sub {new Oscalar ${$_[0]}*$_[1]},
'/'	=>	sub {new Oscalar
$_[2]? $_[1]/${$_[0]} :
${$_[0]}/$_[1]},
'%'	=>	sub {new Oscalar
$_[2]? $_[1]%${$_[0]} : ${$_[0]}%$_[1]},
'**'	=>	sub {new Oscalar
$_[2]? $_[1]**${$_[0]} : ${$_[0]}-$_[1]},
qw(
""	stringify
0+	numify)
);
sub new {
my $foo = $_[1];
bless \$foo, $_[0];
}
sub stringify { "${$_[0]}" }
sub numify { 0 + "${$_[0]}" }
package main;
$test = 0;
$| = 1;
print "1..",&last,"\n";
sub test {
$test++;
if (@_ > 1) {
if ($_[0] eq $_[1]) {
print "ok $test\n";
} else {
print "not ok $test: '$_[0]' ne '$_[1]'\n";
}
} else {
if (shift) {
print "ok $test\n";
} else {
print "not ok $test\n";
}
}
}
$a = new Oscalar "087";
$b= "$a";
test(1);
test ($b eq $a);
test ($b eq "087");
test (ref $a eq "Oscalar");
test ($a eq $a);
test ($a eq "087");
$c = $a + 7;
test (ref $c eq "Oscalar");
test (!($c eq $a));
test ($c eq "94");
$b=$a;
test (ref $a eq "Oscalar");
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
$c=$b;
$c-=$a;
test (ref $c eq "Oscalar");
test ( $a eq "087");
test ( $c eq "1");
test (ref $a eq "Oscalar");
$b=1;
$b+=$a;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
eval q[ package Oscalar; use overload ('++' => sub { $ {$_[0]}++;$_[0] } ) ];
$b=$a;
test (ref $a eq "Oscalar");
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
package Oscalar;
$dummy=bless \$dummy;
package main;
$b=$a;
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
eval q[package Oscalar; use overload ('++' => sub { $ {$_[0]} += 2; $_[0] } ) ];
$b=$a;
test (ref $a eq "Oscalar");
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
package Oscalar;
$dummy=bless \$dummy;
package main;
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "90");
test (ref $a eq "Oscalar");
$b=$a;
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "89");
test (ref $a eq "Oscalar");
test ($b? 1:0);
eval q[ package Oscalar; use overload ('=' => sub {$main::copies++;
package Oscalar;
local $new=$ {$_[0]};
bless \$new } ) ];
$b=new Oscalar "$a";
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "087");
test (ref $a eq "Oscalar");
$b++;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "89");
test (ref $a eq "Oscalar");
test ($copies == 0);
$b+=1;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "90");
test (ref $a eq "Oscalar");
test ($copies == 0);
$b=$a;
$b+=1;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "88");
test (ref $a eq "Oscalar");
test ($copies == 0);
$b=$a;
$b++;
test (ref $b eq "Oscalar") || print ref $b,"=ref(b)\n";
test ( $a eq "087");
test ( $b eq "89");
test (ref $a eq "Oscalar");
test ($copies == 1);
eval q[package Oscalar; use overload ('+=' => sub {$ {$_[0]} += 3*$_[1];
$_[0] } ) ];
$c=new Oscalar;
$b=$a;
$b+=1;
test (ref $b eq "Oscalar");
test ( $a eq "087");
test ( $b eq "90");
test (ref $a eq "Oscalar");
test ($copies == 2);
$b+=$b;
test (ref $b eq "Oscalar");
test ( $b eq "360");
test ($copies == 2);
$b=-$b;
test (ref $b eq "Oscalar");
test ( $b eq "-360");
test ($copies == 2);
$b=abs($b);
test (ref $b eq "Oscalar");
test ( $b eq "360");
test ($copies == 2);
$b=abs($b);
test (ref $b eq "Oscalar");
test ( $b eq "360");
test ($copies == 2);
eval q[package Oscalar;
use overload ('x' => sub {new Oscalar ( $_[2] ? "_.$_[1]._" x $ {$_[0]}
: "_.${$_[0]}._" x $_[1])}) ];
$a=new Oscalar "yy";
$a x= 3;
test ($a eq "_.yy.__.yy.__.yy._");
eval q[package Oscalar;
use overload ('.' => sub {new Oscalar ( $_[2] ?
"_.$_[1].__.$ {$_[0]}._"
: "_.$ {$_[0]}.__.$_[1]._")}) ];
$a=new Oscalar "xx";
test ("b${a}c" eq "_._.b.__.xx._.__.c._");
{
package OscalarI;
@ISA = 'Oscalar';
}
$aI = new OscalarI "$a";
test (ref $aI eq "OscalarI");
test ("$aI" eq "xx");
test ($aI eq "xx");
test ("b${aI}c" eq "_._.b.__.xx._.__.c._");
eval "package Oscalar; no overload '.'";
test ("b${a}" eq "_.b.__.xx._");
$x="1";
bless \$x, Oscalar;
test ("b${a}c" eq "bxxc");
new Oscalar 1;
test ("b${a}c" eq "bxxc");
$na = eval { ~$a };
test($@ =~ /no method found/);
*Oscalar::AUTOLOAD =
sub { *{"Oscalar::$AUTOLOAD"} = sub {"_!_" . shift() . "_!_"} ;
goto &{"Oscalar::$AUTOLOAD"}};
eval "package Oscalar; sub comple; use overload '~' => 'comple'";
$na = eval { ~$a };
test($@ =~ /no method found/);
bless \$x, Oscalar;
$na = eval { ~$a };
warn "`$na', $@" if $@;
test !$@;
test($na eq '_!_xx_!_');
$na = 0;
$na = eval { ~$aI };
test($@ =~ /no method found/);
bless \$x, OscalarI;
$na = eval { ~$aI };
print $@;
test !$@;
test($na eq '_!_xx_!_');
eval "package Oscalar; sub rshft; use overload '>>' => 'rshft'";
$na = eval { $aI >> 1 };
test($@ =~ /no method found/);
bless \$x, OscalarI;
$na = 0;
$na = eval { $aI >> 1 };
print $@;
test !$@;
test($na eq '_!_xx_!_');
test (overload::Method($a, '0+') eq \&Oscalar::numify);
test (overload::Method($aI,'0+') eq \&Oscalar::numify);
test (overload::Overloaded($aI));
test (!overload::Overloaded('overload'));
test (! defined overload::Method($aI, '<<'));
test (! defined overload::Method($a, '<'));
test (overload::StrVal($aI) =~ /^OscalarI=SCALAR\(0x[\da-fA-F]+\)$/);
test (overload::StrVal(\$aI) eq "@{[\$aI]}");
{
package OscalarII;
@ISA = 'OscalarI';
sub Oscalar::lshft {"_<<_" . shift() . "_<<_"}
eval "package OscalarI; use overload '<<' => 'lshft', '|' => 'lshft'";
}
$aaII = "087";
$aII = \$aaII;
bless $aII, 'OscalarII';
bless \$fake, 'OscalarI';
test(($aI | 3) eq '_<<_xx_<<_');
test(($aII << 3) eq '_<<_087_<<_');
{
BEGIN { $int = 7; overload::constant 'integer' => sub {$int++; shift}; }
$out = 2**10;
}
test($int, 9);
test($out, 1024);
$foo = 'foo';
$foo1 = 'f\'o\\o';
{
BEGIN { $q = $qr = 7;
overload::constant 'q' => sub {$q++; push @q, shift, ($_[1] || 'none'); shift},
'qr' => sub {$qr++; push @qr, shift, ($_[1] || 'none'); shift}; }
$out = 'foo';
$out1 = 'f\'o\\o';
$out2 = "a\a$foo,\,";
/b\b$foo.\./;
}
test($out, 'foo');
test($out, $foo);
test($out1, 'f\'o\\o');
test($out1, $foo1);
test($out2, "a\afoo,\,");
test("@q", "foo q f'o\\\\o q a\\a qq ,\\, qq");
test($q, 11);
test("@qr", "b\\b qq .\\. qq");
test($qr, 9);
{
$_ = '!<b>!foo!<-.>!';
BEGIN { overload::constant 'q' => sub {push @q1, shift, ($_[1] || 'none'); "_<" . (shift) . ">_"},
'qr' => sub {push @qr1, shift, ($_[1] || 'none'); "!<" . (shift) . ">!"}; }
$out = 'foo';
$out1 = 'f\'o\\o';
$out2 = "a\a$foo,\,";
$res = /b\b$foo.\./;
$a = <<EOF;
oups
EOF
$b = <<'EOF';
oups1
EOF
$c = bareword;
m'try it';
s'first part'second part';
s/yet another/tail here/;
tr/z-Z/z-Z/;
}
test($out, '_<foo>_');
test($out1, '_<f\'o\\o>_');
test($out2, "_<a\a>_foo_<,\,>_");
test("@q1", "foo q f'o\\\\o q a\\a qq ,\\, qq oups
qq oups1
q second part q tail here s z-Z tr z-Z tr");
test("@qr1", "b\\b qq .\\. qq try it q first part q yet another qq");
test($res, 1);
test($a, "_<oups
>_");
test($b, "_<oups1
>_");
test($c, "bareword");
{
package symbolic;
use overload nomethod => \&wrap, '""' => \&str, '0+' => \&num,
'=' => \&cpy, '++' => \&inc, '--' => \&dec;
sub new { shift; bless ['n', @_] }
sub cpy {
my $self = shift;
bless [@$self], ref $self;
}
sub inc { $_[0] = bless ['++', $_[0], 1]; }
sub dec { $_[0] = bless ['--', $_[0], 1]; }
sub wrap {
my ($obj, $other, $inv, $meth) = @_;
if ($meth eq '++' or $meth eq '--') {
@$obj = ($meth, (bless [@$obj]), 1);
return $obj;
}
($obj, $other) = ($other, $obj) if $inv;
bless [$meth, $obj, $other];
}
sub str {
my ($meth, $a, $b) = @{+shift};
$a = 'u' unless defined $a;
if (defined $b) {
"[$meth $a $b]";
} else {
"[$meth $a]";
}
}
my %subr = ( 'n' => sub {$_[0]} );
foreach my $op (split " ", $overload::ops{with_assign}) {
$subr{$op} = $subr{"$op="} = eval "sub {shift() $op shift()}";
}
my @bins = qw(binary 3way_comparison num_comparison str_comparison);
foreach my $op (split " ", "@overload::ops{ @bins }") {
$subr{$op} = eval "sub {shift() $op shift()}";
}
foreach my $op (split " ", "@overload::ops{qw(unary func)}") {
$subr{$op} = eval "sub {$op shift()}";
}
$subr{'++'} = $subr{'+'};
$subr{'--'} = $subr{'-'};
sub num {
my ($meth, $a, $b) = @{+shift};
my $subr = $subr{$meth}
or die "Do not know how to ($meth) in symbolic";
$a = $a->num if ref $a eq __PACKAGE__;
$b = $b->num if ref $b eq __PACKAGE__;
$subr->($a,$b);
}
sub TIESCALAR { my $pack = shift; $pack->new(@_) }
sub FETCH { shift }
sub nop {  }
sub vars { my $p = shift; tie($_, $p), $_->nop foreach @_; }
sub STORE {
my $obj = shift;
$
@$obj->[0,1] = ('=', shift);
}
}
{
my $foo = new symbolic 11;
my $baz = $foo++;
test( (sprintf "%d", $foo), '12');
test( (sprintf "%d", $baz), '11');
my $bar = $foo;
$baz = ++$foo;
test( (sprintf "%d", $foo), '13');
test( (sprintf "%d", $bar), '12');
test( (sprintf "%d", $baz), '13');
my $ban = $foo;
$baz = ($foo += 1);
test( (sprintf "%d", $foo), '14');
test( (sprintf "%d", $bar), '12');
test( (sprintf "%d", $baz), '14');
test( (sprintf "%d", $ban), '13');
$baz = 0;
$baz = $foo++;
test( (sprintf "%d", $foo), '15');
test( (sprintf "%d", $baz), '14');
test( "$foo", '[++ [+= [++ [++ [n 11] 1] 1] 1] 1]');
}
{
my $iter = new symbolic 2;
my $side = new symbolic 1;
my $cnt = $iter;
while ($cnt) {
$cnt = $cnt - 1;
$side = (sqrt(1 + $side**2) - 1)/$side;
}
my $pi = $side*(2**($iter+2));
test "$side", '[/ [- [sqrt [+ 1 [** [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]] 2]]] 1] [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]]]';
test( (sprintf "%f", $pi), '3.182598');
}
{
my $iter = new symbolic 2;
my $side = new symbolic 1;
my $cnt = $iter;
while ($cnt--) {
$side = (sqrt(1 + $side**2) - 1)/$side;
}
my $pi = $side*(2**($iter+2));
test "$side", '[/ [- [sqrt [+ 1 [** [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]] 2]]] 1] [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]]]';
test( (sprintf "%f", $pi), '3.182598');
}
{
my ($a, $b);
symbolic->vars($a, $b);
my $c = sqrt($a**2 + $b**2);
$a = 3; $b = 4;
test( (sprintf "%d", $c), '5');
$a = 12; $b = 5;
test( (sprintf "%d", $c), '13');
}
{
package symbolic1;
use overload nomethod => \&wrap, '""' => \&str, '0+' => \&num, '=' => \&cpy;
sub new { shift; bless ['n', @_] }
sub cpy {
my $self = shift;
bless [@$self], ref $self;
}
sub wrap {
my ($obj, $other, $inv, $meth) = @_;
if ($meth eq '++' or $meth eq '--') {
@$obj = ($meth, (bless [@$obj]), 1);
return $obj;
}
($obj, $other) = ($other, $obj) if $inv;
bless [$meth, $obj, $other];
}
sub str {
my ($meth, $a, $b) = @{+shift};
$a = 'u' unless defined $a;
if (defined $b) {
"[$meth $a $b]";
} else {
"[$meth $a]";
}
}
my %subr = ( 'n' => sub {$_[0]} );
foreach my $op (split " ", $overload::ops{with_assign}) {
$subr{$op} = $subr{"$op="} = eval "sub {shift() $op shift()}";
}
my @bins = qw(binary 3way_comparison num_comparison str_comparison);
foreach my $op (split " ", "@overload::ops{ @bins }") {
$subr{$op} = eval "sub {shift() $op shift()}";
}
foreach my $op (split " ", "@overload::ops{qw(unary func)}") {
$subr{$op} = eval "sub {$op shift()}";
}
$subr{'++'} = $subr{'+'};
$subr{'--'} = $subr{'-'};
sub num {
my ($meth, $a, $b) = @{+shift};
my $subr = $subr{$meth}
or die "Do not know how to ($meth) in symbolic";
$a = $a->num if ref $a eq __PACKAGE__;
$b = $b->num if ref $b eq __PACKAGE__;
$subr->($a,$b);
}
sub TIESCALAR { my $pack = shift; $pack->new(@_) }
sub FETCH { shift }
sub nop {  }
sub vars { my $p = shift; tie($_, $p), $_->nop foreach @_; }
sub STORE {
my $obj = shift;
$
@$obj->[0,1] = ('=', shift);
}
}
{
my $foo = new symbolic1 11;
my $baz = $foo++;
test( (sprintf "%d", $foo), '12');
test( (sprintf "%d", $baz), '11');
my $bar = $foo;
$baz = ++$foo;
test( (sprintf "%d", $foo), '13');
test( (sprintf "%d", $bar), '12');
test( (sprintf "%d", $baz), '13');
my $ban = $foo;
$baz = ($foo += 1);
test( (sprintf "%d", $foo), '14');
test( (sprintf "%d", $bar), '12');
test( (sprintf "%d", $baz), '14');
test( (sprintf "%d", $ban), '13');
$baz = 0;
$baz = $foo++;
test( (sprintf "%d", $foo), '15');
test( (sprintf "%d", $baz), '14');
test( "$foo", '[++ [+= [++ [++ [n 11] 1] 1] 1] 1]');
}
{
my $iter = new symbolic1 2;
my $side = new symbolic1 1;
my $cnt = $iter;
while ($cnt) {
$cnt = $cnt - 1;
$side = (sqrt(1 + $side**2) - 1)/$side;
}
my $pi = $side*(2**($iter+2));
test "$side", '[/ [- [sqrt [+ 1 [** [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]] 2]]] 1] [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]]]';
test( (sprintf "%f", $pi), '3.182598');
}
{
my $iter = new symbolic1 2;
my $side = new symbolic1 1;
my $cnt = $iter;
while ($cnt--) {
$side = (sqrt(1 + $side**2) - 1)/$side;
}
my $pi = $side*(2**($iter+2));
test "$side", '[/ [- [sqrt [+ 1 [** [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]] 2]]] 1] [/ [- [sqrt [+ 1 [** [n 1] 2]]] 1] [n 1]]]';
test( (sprintf "%f", $pi), '3.182598');
}
{
my ($a, $b);
symbolic1->vars($a, $b);
my $c = sqrt($a**2 + $b**2);
$a = 3; $b = 4;
test( (sprintf "%d", $c), '5');
$a = 12; $b = 5;
test( (sprintf "%d", $c), '13');
}
{
package two_face;
sub new { my $p = shift; bless [@_], $p }
use overload '""' => \&str, '0+' => \&num, fallback => 1;
sub num {shift->[1]}
sub str {shift->[0]}
}
{
my $seven = new two_face ("vii", 7);
test( (sprintf "seven=$seven, seven=%d, eight=%d", $seven, $seven+1),
'seven=vii, seven=7, eight=8');
test( scalar ($seven =~ /i/), '1')
}
{
package sorting;
use overload 'cmp' => \&comp;
sub new { my ($p, $v) = @_; bless \$v, $p }
sub comp { my ($x,$y) = @_; ($$x * 3 % 10) <=> ($$y * 3 % 10) or $$x cmp $$y }
}
{
my @arr = map sorting->new($_), 0..12;
my @sorted1 = sort @arr;
my @sorted2 = map $$_, @sorted1;
test "@sorted2", '0 10 7 4 1 11 8 5 12 2 9 6 3';
}
sub last {174}
