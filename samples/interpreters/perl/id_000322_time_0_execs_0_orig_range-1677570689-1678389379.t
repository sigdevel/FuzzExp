#!./perl
print "1..12\n";
print join(':',1..5) eq '1:2:3:4:5' ? "ok 1\n" : "not ok 1\n";
@foo = (1,2,3,4,5,6,7,8,9);
@foo[2..4] = ('c','d','e');
print join(':',@foo[$foo[0]..5]) eq '2:c:d:e:6' ? "ok 2\n" : "not ok 2\n";
@bar[2..4] = ('c','d','e');
print join(':',@bar[1..5]) eq ':c:d:e:' ? "ok 3\n" : "not ok 3\n";
($a,@bcd[0..2],$e) = ('a','b','c','d','e');
print join(':',$a,@bcd[0..2],$e) eq 'a:b:c:d:e' ? "ok 4\n" : "not ok 4\n";
$x = 0;
for (1..100) {
$x += $_;
}
print $x == 5050 ? "ok 5\n" : "not ok 5 $x\n";
$x = 0;
for ((100,2..99,1)) {
$x += $_;
}
print $x == 5050 ? "ok 6\n" : "not ok 6 $x\n";
$x = join('','a'..'z');
print $x eq 'abcdefghijklmnopqrstuvwxyz' ? "ok 7\n" : "not ok 7 $x\n";
@x = 'A'..'ZZ';
print @x == 27 * 26 ? "ok 8\n" : "not ok 8\n";
@x = '09' .. '08';
print "not " unless join(",", @x) eq
join(",", map {sprintf "%02d",$_} 9..99);
print "ok 9\n";
@y = ();
foreach ('09'..'08') {
push(@y, $_);
}
print "not " unless join(",", @y) eq join(",", @x);
print "ok 10\n";
@a = 0x7ffffffe..0x7fffffff;
print "not " unless "@a" eq "2147483646 2147483647";
print "ok 11\n";
@a = -0x7fffffff..-0x7ffffffe;
print "not " unless "@a" eq "-2147483647 -2147483646";
print "ok 12\n";
