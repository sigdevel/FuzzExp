#!./perl
BEGIN {
chdir 't' if -d 't';
@INC = qw(. ../lib);
}
print "1..69\n";
require 'test.pl';
$bar = "ok 1\n";
$foo = "ok 2\n";
{
local(*foo) = *bar;
print $foo;
}
print $foo;
$baz = "ok 3\n";
$foo = "ok 4\n";
{
local(*foo) = 'baz';
print $foo;
}
print $foo;
$foo = "ok 6\n";
{
local(*foo);
print $foo;
$foo = "ok 5\n";
print $foo;
}
print $foo;
$baz = "ok 7\n";
$bar = 'baz';
$foo = 'bar';
print $$$foo;
$FOO = \$BAR;
$BAR = \$BAZ;
$BAZ = "ok 8\n";
print $$$FOO;
@ary = (9,10,11,12);
$ref[0] = \@a;
$ref[1] = \@b;
$ref[2] = \@c;
$ref[3] = \@d;
for $i (3,1,2,0) {
push(@{$ref[$i]}, "ok $ary[$i]\n");
}
print @a;
print ${$ref[1]}[0];
print @{$ref[2]}[0];
print @{'d'};
$refref = \\$x;
$x = "ok 13\n";
print $$$refref;
$ref = [[],2,[3,4,5,]];
print scalar @$ref == 3 ? "ok 14\n" : "not ok 14\n";
print $$ref[1] == 2 ? "ok 15\n" : "not ok 15\n";
print ${$$ref[2]}[2] == 5 ? "ok 16\n" : "not ok 16\n";
print scalar @{$$ref[0]} == 0 ? "ok 17\n" : "not ok 17\n";
print $ref->[1] == 2 ? "ok 18\n" : "not ok 18\n";
print $ref->[2]->[0] == 3 ? "ok 19\n" : "not ok 19\n";
$refref = \%whatever;
$refref->{"key"} = $ref;
print $refref->{"key"}->[2]->[0] == 3 ? "ok 20\n" : "not ok 20\n";
$spring[5]->[0] = 123;
$spring[5]->[1] = 456;
push(@{$spring[5]}, 789);
print join(':',@{$spring[5]}) eq "123:456:789" ? "ok 21\n" : "not ok 21\n";
@{$spring2{"foo"}} = (1,2,3);
$spring2{"foo"}->[3] = 4;
print join(':',@{$spring2{"foo"}}) eq "1:2:3:4" ? "ok 22\n" : "not ok 22\n";
sub mysub { print "ok 23\n" }
$subref = \&mysub;
&$subref;
$subrefref = \\&mysub2;
$$subrefref->("ok 24\n");
sub mysub2 { print shift }
print ref $subref	eq CODE  ? "ok 25\n" : "not ok 25\n";
print ref $ref		eq ARRAY ? "ok 26\n" : "not ok 26\n";
print ref $refref	eq HASH  ? "ok 27\n" : "not ok 27\n";
$anonhash = {};
print ref $anonhash	eq HASH  ? "ok 28\n" : "not ok 28\n";
$anonhash2 = {FOO => BAR, ABC => XYZ,};
print join('', sort values %$anonhash2) eq BARXYZ ? "ok 29\n" : "not ok 29\n";
package MYHASH;
$object = bless $main'anonhash2;
print ref $object	eq MYHASH  ? "ok 30\n" : "not ok 30\n";
print $object->{ABC}	eq XYZ     ? "ok 31\n" : "not ok 31\n";
$object2 = bless {};
print ref $object2	eq MYHASH  ? "ok 32\n" : "not ok 32\n";
&mymethod($object,33);
sub mymethod {
local($THIS, @ARGS) = @_;
die 'Got a "' . ref($THIS). '" instead of a MYHASH'
unless ref $THIS eq MYHASH;
print $THIS->{FOO} eq BAR  ? "ok $ARGS[0]\n" : "not ok $ARGS[0]\n";
}
$string = "not ok 34\n";
$object = "foo";
$string = "ok 34\n";
$main'anonhash2 = "foo";
$string = "";
DESTROY {
return unless $string;
print $string;
print ref shift ne HASH ? "ok 35\n" : "not ok 35\n";
}
package OBJ;
@ISA = (BASEOBJ);
$main'object = bless {FOO => foo, BAR => bar};
package main;
print $object->doit("BAR") eq bar ? "ok 36\n" : "not ok 36\n";
$foo = doit $object "FOO";
print $foo eq foo ? "ok 37\n" : "not ok 37\n";
sub BASEOBJ'doit {
local $ref = shift;
die "Not an OBJ" unless ref $ref eq OBJ;
$ref->{shift()};
}
package UNIVERSAL;
@ISA = 'LASTCHANCE';
package LASTCHANCE;
sub foo { print $_[1] }
package WHATEVER;
foo WHATEVER "ok 38\n";
package main;
@foo = \(1..3);
@bar = \(@foo);
@baz = \(1,@foo,@bar);
print @bar == 3 ? "ok 39\n" : "not ok 39\n";
print grep(ref($_), @bar) == 3 ? "ok 40\n" : "not ok 40\n";
print @baz == 3 ? "ok 41\n" : "not ok 41\n";
my(@fuu) = \(1..2,3);
my(@baa) = \(@fuu);
my(@bzz) = \(1,@fuu,@baa);
print @baa == 3 ? "ok 42\n" : "not ok 42\n";
print grep(ref($_), @baa) == 3 ? "ok 43\n" : "not ok 43\n";
print @bzz == 3 ? "ok 44\n" : "not ok 44\n";
eval '\\($x, $y) = (1, 2);';
print $@ =~ /Can\'t modify.*ref.*in.*assignment/ ? "ok 45\n" : "not ok 45\n";
sub larry::DESTROY { print "
sub curly::DESTROY { print "
sub moe::DESTROY   { print "
{
my ($joe, @curly, %larry);
my $moe = bless \$joe, 'moe';
my $curly = bless \@curly, 'curly';
my $larry = bless \%larry, 'larry';
print "
}
print "
$foo = "not ok 49";
{ local(*bar) = "foo" }
$bar = "ok 49";
local(*bar) = *bar;
print "$bar\n";
$var = "ok 50";
$_   = \$var;
print $$_,"\n";
{
package A;
sub new { bless {}, shift }
DESTROY { print "
package _B;
sub new { bless {}, shift }
DESTROY { print "
package main;
my $b = _B->new;
}
{
my $i = 0;
local $SIG{'__DIE__'} = sub {
my $m = shift;
if ($i++ > 4) {
print "
exit 1;
}
print "
if ($m =~ /^Modification of a read-only/) { print "ok 53\n" }
};
package C;
sub new { bless {}, shift }
DESTROY { $_[0] = 'foo' }
{
print "
my $c = C->new;
}
print "
}
{
my @a;
$a[1] = "ok 54\n";
print ${\$_} for @a;
}
$a = [1,2,3];
$a = $a->[1];
print "not " unless $a == 2;
print "ok 55\n";
my $test = 56;
foreach my $lexical ('', 'my $a; ') {
my $expect = "pass\n";
my $result = runperl (switches => ['-wl'], stderr => 1,
prog => $lexical . 'BEGIN {$a = \q{pass}}; $a = $$a; print $a');
if ($? == 0 and $result eq $expect) {
print "ok $test\n";
} else {
print "not ok $test
print "
}
$test++;
}
sub x::DESTROY {print "ok ", $test + shift->[0], "\n"}
{ my $a1 = bless [3],"x";
my $a2 = bless [2],"x";
{ my $a3 = bless [1],"x";
my $a4 = bless [0],"x";
567;
}
}
$test+=4;
my $result = runperl (switches=>['-l'],
prog=> 'print 1; print qq-*$\*-;print 1;');
my $expect = "1\n*\n*\n1\n";
if ($result eq $expect) {
print "ok $test\n";
} else {
print "not ok $test\n";
foreach ($expect, $result) {
s/\n/\\n/gs;
}
print "
}
runperl(prog => 'sub UNIVERSAL::AUTOLOAD { qr// } a->p' );
if ($? != 0) { print "not " };
print "ok ",++$test," - UNIVERSAL::AUTOLOAD called when freeing qr//\n";
runperl(prog => 'sub UNIVERSAL::DESTROY { warn } bless \$a, A', stderr => 1);
if ($? != 0) { print "not " };
print "ok ",++$test," - warn called inside UNIVERSAL::DESTROY\n";
runperl(prog => 'sub f { my $x = shift; *z = $x; } f({}); f();');
if ($? != 0) { print "not " };
print "ok ",++$test," - coredump on typeglob = (SvRV && !SvROK)\n";
$result = runperl(
prog => 'use Symbol;my $x=bless \gensym,"t"; print;*$$x=$x',
stderr => 1
);
print "not " if length $result;
print "ok ",++$test," - freeing self-referential typeglob\n";
print "
++$test;
my $test1 = $test + 1;
my $test2 = $test + 2;
package FINALE;
{
$ref3 = bless ["ok $test2\n"];
my $ref2 = bless ["ok $test1\n"];
local $ref1 = bless ["ok $test\n"];
1;
}
DESTROY {
print $_[0][0];
}
