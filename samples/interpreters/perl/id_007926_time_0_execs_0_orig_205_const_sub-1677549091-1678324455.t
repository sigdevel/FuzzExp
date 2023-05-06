#!/usr/bin/perl
print "1..21\n";
BEGIN { $SIG{__WARN__} = sub { } }
sub csubi() { 1 }
sub csubf() { 1.1 }
sub csubs() { 'abc' }
sub ncsub   { 1 }
print csubi   == 1 ? "ok\n" : "not ok - int\n";
print csubi() == 1 ? "ok\n" : "not ok - int\n";
print csubf   == 1.1 ? "ok\n" : "not ok - float\n";
print csubf() == 1.1 ? "ok\n" : "not ok - float\n";
print csubs   eq 'abc' ? "ok\n" : "not ok - string\n";
print csubs() eq 'abc' ? "ok\n" : "not ok - string\n";
print ncsub   == 2 ? "ok\n" : "not ok - non const\n";
print &csubi == 2 ? "ok\n" : "not ok - &sub\n";
sub csubi() { 2 }
sub csubf() { 2.2 }
sub csubs() { 'cde' }
sub ncsub   { 2 }
print csubi   == 2 ? "ok\n" : "not ok - int\n";
print csubi() == 2 ? "ok\n" : "not ok - int\n";
print csubf   == 2.2 ? "ok\n" : "not ok - float\n";
print csubs   eq 'cde' ? "ok\n" : "not ok - string\n";
print ncsub   == 2 ? "ok\n" : "not ok - non const\n";
sub make_const {
my( $name, $value ) = @_;
*$name = sub() { $value };
}
sub make_nconst {
my( $name, $value ) = @_;
*$name = sub { $value };
}
BEGIN {
make_const( 'ccsubi', 1 );
make_const( 'ccsubf', 1.1 );
make_const( 'ccsubs', 'abc' );
make_nconst( 'cncsub', 1 );
}
print ccsubi == 1 ? "ok\n" : "not ok - int\n";
print ccsubf == 1.1 ? "ok\n" : "not ok - float\n";
print ccsubs eq 'abc' ? "ok\n" : "not ok - string\n";
print cncsub == 2 ? "ok\n" : "not ok - non const\n";
BEGIN {
make_const( 'ccsubi', 2 );
make_const( 'ccsubf', 2.2 );
make_const( 'ccsubs', 'cde' );
make_nconst( 'cncsub', 2 );
}
print ccsubi == 2 ? "ok\n" : "not ok - int\n";
print ccsubf == 2.2 ? "ok\n" : "not ok - float\n";
print ccsubs eq 'cde' ? "ok\n" : "not ok - string\n";
print cncsub == 2 ? "ok\n" : "not ok - non const\n";
