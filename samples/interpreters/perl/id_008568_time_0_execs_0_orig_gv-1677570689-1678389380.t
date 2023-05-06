#!./perl
print "1..23\n";
$foo = 'foo';
$bar = *main::foo;
$bar = $foo;
print ref(\$bar) eq 'SCALAR' ? "ok 1\n" : "not ok 1\n";
$foo = *main::bar;
if ($foo) {
print ref(\$foo) eq 'GLOB' ? "ok 2\n" : "not ok 2\n";
}
unless ($foo =~ /abcd/) {
print ref(\$foo) eq 'GLOB' ? "ok 3\n" : "not ok 3\n";
}
if ($foo eq '*main::bar') {
print ref(\$foo) eq 'GLOB' ? "ok 4\n" : "not ok 4\n";
}
$a = *main::foo;
$b = $a;
$a =~ s/^X//;
print ref(\$a) eq 'GLOB' ? "ok 5\n" : "not ok 5\n";
$a =~ s/^\*//;
print $a eq 'main::foo' ? "ok 6\n" : "not ok 6\n";
print ref(\$b) eq 'GLOB' ? "ok 7\n" : "not ok 7\n";
substr($foo, 0, 1) = "XXX";
print ref(\$foo) eq 'SCALAR' ? "ok 8\n" : "not ok 8\n";
print $foo eq 'XXXmain::bar' ? "ok 9\n" : "not ok 9\n";
sub foo {
local($bar) = *main::foo;
$foo = *main::bar;
return ($foo, $bar);
}
($fuu, $baa) = foo();
if (defined $fuu) {
print ref(\$fuu) eq 'GLOB' ? "ok 10\n" : "not ok 10\n";
}
if (defined $baa) {
print ref(\$baa) eq 'GLOB' ? "ok 11\n" : "not ok 11\n";
}
{ package Foo::Bar }
print exists $Foo::{'Bar::'} ? "ok 12\n" : "not ok 12\n";
print $Foo::{'Bar::'} eq '*Foo::Bar::' ? "ok 13\n" : "not ok 13\n";
$foo = 'stuff';
@foo = qw(more stuff);
%foo = qw(even more random stuff);
undef *foo;
print +($foo || @foo || %foo) ? "not ok" : "ok", " 14\n";
{
my $msg;
local $SIG{__WARN__} = sub { $msg = $_[0] };
local $^W = 1;
*foo = 'bar';
print $msg ? "not ok" : "ok", " 15\n";
*foo = undef;
print $msg ? "ok" : "not ok", " 16\n";
}
$x = "ok 17\n";
@x = ("ok 18\n");
%x = ("ok 19" => "\n");
sub x { "ok 20\n" }
print ${*x{SCALAR}}, @{*x{ARRAY}}, %{*x{HASH}}, &{*x{CODE}};
*x = *STDOUT;
print *{*x{GLOB}} eq "*main::STDOUT" ? "ok 21\n" : "not ok 21\n";
print {*x{IO}} "ok 22\n";
print {*x{FILEHANDLE}} "ok 23\n";
