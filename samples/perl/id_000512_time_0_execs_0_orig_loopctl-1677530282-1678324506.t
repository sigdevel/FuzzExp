#!./perl
print "1..44\n";
my $ok;
TEST1: {
$ok = 0;
my $x = 1;
my $first_time = 1;
while($x--) {
if (!$first_time) {
$ok = 1;
last TEST1;
}
$ok = 0;
$first_time = 0;
redo;
last TEST1;
}
continue {
$ok = 0;
last TEST1;
}
$ok = 0;
}
print ($ok ? "ok 1\n" : "not ok 1\n");
TEST2: {
$ok = 0;
my $x = 2;
my $first_time = 1;
my $been_in_continue = 0;
while($x--) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST2;
}
$ok = 0;
$first_time = 0;
next;
last TEST2;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 2\n" : "not ok 2\n");
TEST3: {
$ok = 0;
my $x = 1;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
while($x--) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST3;
}
$ok = 0;
$first_time = 0;
next;
last TEST3;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 3\n" : "not ok 3\n");
TEST4: {
$ok = 0;
my $x = 1;
my $first_time = 1;
while($x++) {
if (!$first_time) {
$ok = 0;
last TEST4;
}
$ok = 0;
$first_time = 0;
last;
last TEST4;
}
continue {
$ok = 0;
last TEST4;
}
$ok = 1;
}
print ($ok ? "ok 4\n" : "not ok 4\n");
TEST5: {
$ok = 0;
my $x = 0;
my $first_time = 1;
until($x++) {
if (!$first_time) {
$ok = 1;
last TEST5;
}
$ok = 0;
$first_time = 0;
redo;
last TEST5;
}
continue {
$ok = 0;
last TEST5;
}
$ok = 0;
}
print ($ok ? "ok 5\n" : "not ok 5\n");
TEST6: {
$ok = 0;
my $x = 0;
my $first_time = 1;
my $been_in_continue = 0;
until($x++ >= 2) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST6;
}
$ok = 0;
$first_time = 0;
next;
last TEST6;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 6\n" : "not ok 6\n");
TEST7: {
$ok = 0;
my $x = 0;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
until($x++) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST7;
}
$ok = 0;
$first_time = 0;
next;
last TEST7;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 7\n" : "not ok 7\n");
TEST8: {
$ok = 0;
my $x = 0;
my $first_time = 1;
until($x++ == 10) {
if (!$first_time) {
$ok = 0;
last TEST8;
}
$ok = 0;
$first_time = 0;
last;
last TEST8;
}
continue {
$ok = 0;
last TEST8;
}
$ok = 1;
}
print ($ok ? "ok 8\n" : "not ok 8\n");
TEST9: {
$ok = 0;
my $first_time = 1;
for(1) {
if (!$first_time) {
$ok = 1;
last TEST9;
}
$ok = 0;
$first_time = 0;
redo;
last TEST9;
}
continue {
$ok = 0;
last TEST9;
}
$ok = 0;
}
print ($ok ? "ok 9\n" : "not ok 9\n");
TEST10: {
$ok = 0;
my $first_time = 1;
my $been_in_continue = 0;
for(1,2) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST10;
}
$ok = 0;
$first_time = 0;
next;
last TEST10;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 10\n" : "not ok 10\n");
TEST11: {
$ok = 0;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
for(1) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST11;
}
$ok = 0;
$first_time = 0;
next;
last TEST11;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 11\n" : "not ok 11\n");
TEST12: {
$ok = 0;
my $first_time = 1;
for(1..10) {
if (!$first_time) {
$ok = 0;
last TEST12;
}
$ok = 0;
$first_time = 0;
last;
last TEST12;
}
continue {
$ok=0;
last TEST12;
}
$ok = 1;
}
print ($ok ? "ok 12\n" : "not ok 12\n");
TEST13: {
$ok = 0;
for(my $first_time = 1; 1;) {
if (!$first_time) {
$ok = 1;
last TEST13;
}
$ok = 0;
$first_time=0;
redo;
last TEST13;
}
$ok = 0;
}
print ($ok ? "ok 13\n" : "not ok 13\n");
TEST14: {
$ok = 0;
for(my $first_time = 1; 1; $first_time=0) {
if (!$first_time) {
$ok = 1;
last TEST14;
}
$ok = 0;
next;
last TEST14;
}
$ok = 0;
}
print ($ok ? "ok 14\n" : "not ok 14\n");
TEST15: {
$ok = 0;
my $x=1;
my $been_in_loop = 0;
for(my $first_time = 1; $x--;) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST15;
}
$ok = 0;
$first_time = 0;
next;
last TEST15;
}
$ok = $been_in_loop;
}
print ($ok ? "ok 15\n" : "not ok 15\n");
TEST16: {
$ok = 0;
for(my $first_time = 1; 1; last TEST16) {
if (!$first_time) {
$ok = 0;
last TEST16;
}
$ok = 0;
$first_time = 0;
last;
last TEST16;
}
$ok = 1;
}
print ($ok ? "ok 16\n" : "not ok 16\n");
TEST17: {
$ok = 0;
my $first_time = 1;
{
if (!$first_time) {
$ok = 1;
last TEST17;
}
$ok = 0;
$first_time=0;
redo;
last TEST17;
}
continue {
$ok = 0;
last TEST17;
}
$ok = 0;
}
print ($ok ? "ok 17\n" : "not ok 17\n");
TEST18: {
$ok = 0;
{
next;
last TEST18;
}
continue {
$ok = 1;
last TEST18;
}
$ok = 0;
}
print ($ok ? "ok 18\n" : "not ok 18\n");
TEST19: {
$ok = 0;
{
last;
last TEST19;
}
continue {
$ok = 0;
last TEST19;
}
$ok = 1;
}
print ($ok ? "ok 19\n" : "not ok 19\n");
TEST20: {
$ok = 0;
my $x = 1;
my $first_time = 1;
LABEL20: while($x--) {
if (!$first_time) {
$ok = 1;
last TEST20;
}
$ok = 0;
$first_time = 0;
redo LABEL20;
last TEST20;
}
continue {
$ok = 0;
last TEST20;
}
$ok = 0;
}
print ($ok ? "ok 20\n" : "not ok 20\n");
TEST21: {
$ok = 0;
my $x = 2;
my $first_time = 1;
my $been_in_continue = 0;
LABEL21: while($x--) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST21;
}
$ok = 0;
$first_time = 0;
next LABEL21;
last TEST21;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 21\n" : "not ok 21\n");
TEST22: {
$ok = 0;
my $x = 1;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
LABEL22: while($x--) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST22;
}
$ok = 0;
$first_time = 0;
next LABEL22;
last TEST22;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 22\n" : "not ok 22\n");
TEST23: {
$ok = 0;
my $x = 1;
my $first_time = 1;
LABEL23: while($x++) {
if (!$first_time) {
$ok = 0;
last TEST23;
}
$ok = 0;
$first_time = 0;
last LABEL23;
last TEST23;
}
continue {
$ok = 0;
last TEST23;
}
$ok = 1;
}
print ($ok ? "ok 23\n" : "not ok 23\n");
TEST24: {
$ok = 0;
my $x = 0;
my $first_time = 1;
LABEL24: until($x++) {
if (!$first_time) {
$ok = 1;
last TEST24;
}
$ok = 0;
$first_time = 0;
redo LABEL24;
last TEST24;
}
continue {
$ok = 0;
last TEST24;
}
$ok = 0;
}
print ($ok ? "ok 24\n" : "not ok 24\n");
TEST25: {
$ok = 0;
my $x = 0;
my $first_time = 1;
my $been_in_continue = 0;
LABEL25: until($x++ >= 2) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST25;
}
$ok = 0;
$first_time = 0;
next LABEL25;
last TEST25;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 25\n" : "not ok 25\n");
TEST26: {
$ok = 0;
my $x = 0;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
LABEL26: until($x++) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST26;
}
$ok = 0;
$first_time = 0;
next LABEL26;
last TEST26;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 26\n" : "not ok 26\n");
TEST27: {
$ok = 0;
my $x = 0;
my $first_time = 1;
LABEL27: until($x++ == 10) {
if (!$first_time) {
$ok = 0;
last TEST27;
}
$ok = 0;
$first_time = 0;
last LABEL27;
last TEST27;
}
continue {
$ok = 0;
last TEST8;
}
$ok = 1;
}
print ($ok ? "ok 27\n" : "not ok 27\n");
TEST28: {
$ok = 0;
my $first_time = 1;
LABEL28: for(1) {
if (!$first_time) {
$ok = 1;
last TEST28;
}
$ok = 0;
$first_time = 0;
redo LABEL28;
last TEST28;
}
continue {
$ok = 0;
last TEST28;
}
$ok = 0;
}
print ($ok ? "ok 28\n" : "not ok 28\n");
TEST29: {
$ok = 0;
my $first_time = 1;
my $been_in_continue = 0;
LABEL29: for(1,2) {
if (!$first_time) {
$ok = $been_in_continue;
last TEST29;
}
$ok = 0;
$first_time = 0;
next LABEL29;
last TEST29;
}
continue {
$been_in_continue = 1;
}
$ok = 0;
}
print ($ok ? "ok 29\n" : "not ok 29\n");
TEST30: {
$ok = 0;
my $first_time = 1;
my $been_in_loop = 0;
my $been_in_continue = 0;
LABEL30: for(1) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST30;
}
$ok = 0;
$first_time = 0;
next LABEL30;
last TEST30;
}
continue {
$been_in_continue = 1;
}
$ok = $been_in_loop && $been_in_continue;
}
print ($ok ? "ok 30\n" : "not ok 30\n");
TEST31: {
$ok = 0;
my $first_time = 1;
LABEL31: for(1..10) {
if (!$first_time) {
$ok = 0;
last TEST31;
}
$ok = 0;
$first_time = 0;
last LABEL31;
last TEST31;
}
continue {
$ok=0;
last TEST31;
}
$ok = 1;
}
print ($ok ? "ok 31\n" : "not ok 31\n");
TEST32: {
$ok = 0;
LABEL32: for(my $first_time = 1; 1;) {
if (!$first_time) {
$ok = 1;
last TEST32;
}
$ok = 0;
$first_time=0;
redo LABEL32;
last TEST32;
}
$ok = 0;
}
print ($ok ? "ok 32\n" : "not ok 32\n");
TEST33: {
$ok = 0;
LABEL33: for(my $first_time = 1; 1; $first_time=0) {
if (!$first_time) {
$ok = 1;
last TEST33;
}
$ok = 0;
next LABEL33;
last TEST33;
}
$ok = 0;
}
print ($ok ? "ok 33\n" : "not ok 33\n");
TEST34: {
$ok = 0;
my $x=1;
my $been_in_loop = 0;
LABEL34: for(my $first_time = 1; $x--;) {
$been_in_loop = 1;
if (!$first_time) {
$ok = 0;
last TEST34;
}
$ok = 0;
$first_time = 0;
next LABEL34;
last TEST34;
}
$ok = $been_in_loop;
}
print ($ok ? "ok 34\n" : "not ok 34\n");
TEST35: {
$ok = 0;
LABEL35: for(my $first_time = 1; 1; last TEST16) {
if (!$first_time) {
$ok = 0;
last TEST35;
}
$ok = 0;
$first_time = 0;
last LABEL35;
last TEST35;
}
$ok = 1;
}
print ($ok ? "ok 35\n" : "not ok 35\n");
TEST36: {
$ok = 0;
my $first_time = 1;
LABEL36: {
if (!$first_time) {
$ok = 1;
last TEST36;
}
$ok = 0;
$first_time=0;
redo LABEL36;
last TEST36;
}
continue {
$ok = 0;
last TEST36;
}
$ok = 0;
}
print ($ok ? "ok 36\n" : "not ok 36\n");
TEST37: {
$ok = 0;
LABEL37: {
next LABEL37;
last TEST37;
}
continue {
$ok = 1;
last TEST37;
}
$ok = 0;
}
print ($ok ? "ok 37\n" : "not ok 37\n");
TEST38: {
$ok = 0;
LABEL38: {
last LABEL38;
last TEST38;
}
continue {
$ok = 0;
last TEST38;
}
$ok = 1;
}
print ($ok ? "ok 38\n" : "not ok 38\n");
TEST39: {
$ok = 0;
my ($x, $y, $z) = (1,1,1);
one39: while ($x--) {
$ok = 0;
two39: while ($y--) {
$ok = 0;
three39: while ($z--) {
next two39;
}
continue {
$ok = 0;
last TEST39;
}
}
continue {
$ok = 1;
last TEST39;
}
$ok = 0;
}
}
print ($ok ? "ok 39\n" : "not ok 39\n");
sub test_last_label { last TEST40 }
TEST40: {
$ok = 1;
test_last_label();
$ok = 0;
}
print ($ok ? "ok 40\n" : "not ok 40\n");
sub test_last { last }
TEST41: {
$ok = 1;
test_last();
$ok = 0;
}
print ($ok ? "ok 41\n" : "not ok 41\n");
{
my $n=10; my $late_free = 0;
sub X::DESTROY { $late_free++ if $n < 0 };
{
($n-- && bless {}, 'X') && redo;
}
print $late_free ? "not " : "", "ok 42 - redo memory leak\n";
$n = 10; $late_free = 0;
{
($n-- && bless {}, 'X') && redo;
}
continue { }
print $late_free ? "not " : "", "ok 43 - redo with continue memory leak\n";
}
{
$a37725[3] = 1;
$i = 2;
for my $x (reverse @a37725) {
$x = $i++;
}
print "@a37725" == "5 4 3 2" ? "" : "not ",
"ok 44 - reverse with empty slots (@a37725)\n";
}
