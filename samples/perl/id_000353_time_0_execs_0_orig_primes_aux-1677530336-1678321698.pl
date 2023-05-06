#!/usr/local/bin/perl -w
@known=qw(2 3 5 7);
for (1..100) {
if (check_prime($_)) {
warn "$_ is prime\n";
}
}
sub check_prime {
my ($n)=@_;
if ($n < 2) {
return 0;
}
for (1..scalar(@known)) {
if ($n==$known[$_-1]) {
return 1;
}
if (($n/$known[$_-1]) == int($n/$known[$_-1])) {
return 0;
}
}
for ($known[-1]..int(sqrt($n))) {
if (($n/$_) == int($n/$_)) {
return 0;
}
}
push(@known,$n);
return 1;
}
