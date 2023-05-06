#!/usr/bin/perl -w
package Foo;
sub a { $_[0]->{a} }
sub s_a { 2 }
package Bar;
@ISA = 'Foo';
package Baz;
@ISA = 'Foo';
sub a { $_[0]->{b} }
sub s_a { 4 }
package main;
print "1..15\n";
print Foo->s_a == 2 ? "ok 1\n" : "ok 2\n";
$oa = bless { a => 1, b => 3 }, 'Foo';
print $oa->a == 1 ? "ok 2\n" : "not ok 2\n";
print $oa->s_a == 2 ? "ok 3\n" : "not ok 3\n";
print Bar->s_a == 2 ? "ok 4\n" : "ok 4\n";
$ob = bless { a => 1, b => 3 }, 'Bar';
print $ob->a == 1 ? "ok 5\n" : "not ok 5\n";
print $ob->s_a == 2 ? "ok 6\n" : "not ok 6\n";
print Baz->s_a == 4 ? "ok 7\n" : "ok 7\n";
$oc = bless { a => 1, b => 3 }, 'Baz';
print $oc->a == 3 ? "ok 8\n" : "not ok 8\n";
print $oc->s_a == 4 ? "ok 9\n" : "not ok 9\n";
print $oc->Bar::a == 1 ? "ok\n" : "not ok\n";
$c = ref $oc;
print $c eq 'Baz' ? "ok\n" : "not ok - $c\n";
$c = ref $ob;
print $c eq 'Bar' ? "ok\n" : "not ok - $c\n";
$foo_a1 = \&Foo::a;
$foo_a2 = "Foo::a";
$a = "a";
print $oc->$foo_a1 == 1 ? "ok\n" : "not ok\n";
print $oc->$foo_a2 == 1 ? "ok\n" : "not ok\n";
print $oc->$a == 3 ? "ok\n" : "not ok\n";
