#!/usr/bin/perl -w
$DATAFILE = "earplug_data.txt";
open(DATAFILE);
for ($i = 0; $i < 368; $i++) {
$_ = <DATAFILE>;
$_ = <DATAFILE>;
for ($j = 0 ; $j < 128 ; $j++) {
while (m|([0-9.-]+) ([0-9.-]+) |g) {
$impulses[$i][0][$j] = $1;
$impulses[$i][1][$j] = $2;
}
}
$_ = <DATAFILE>;
}
close(DATAFILE);
print("t_float impulses\[368\]\[2\]\[128\] = {\n");
for ($i = 0; $i < 368; $i++) {
print("{\n{");
for ($j = 0 ; $j < 128 ; $j++) {
print("$impulses[$i][0][$j], ");
}
print("},\n{");
for ($j = 0 ; $j < 128 ; $j++) {
print("$impulses[$i][1][$j], ");
}
print("}\n},\n");
}
print("\n};\n\n");
