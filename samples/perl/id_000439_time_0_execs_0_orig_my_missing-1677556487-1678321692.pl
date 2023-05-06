#!/usr/bin/env perl
use 5.010;
print_it('abc', 42) if 0==1 and check_it('abc') and sqrt($foo);
($fruit) = 'apple';
$fruit = 'apple';
say $fruit;
if ( $diet = 'paleo' ) {
$meat = 'Yes';
}
elsif ( $diet = 'vegan' ) {
$meat = 'No';
}
else {
$meat = 'Maybe';
}
say $meat;
$i = 0;
while ($i++<5) {
$j = $i;
}
say $j;
@array = grep { $_ % 2 == 0 } 1 .. 5;
$array[7] = 8;
$c = 0;
%hash = map { $_ => ++$c } grep { /a/ } grep /s/, qw( salami baloney );
%hash = map { $_ => ++$d } grep { /a/ } grep /s/, qw( salami baloney );
{
$grain = 'wheat';
say $grain;
}
sub foo1 {
if ( $burned_out ) {
$unstable++;
}
if ( !$burned_out ) {
$unstable--;
}
say 'hi!';
}
