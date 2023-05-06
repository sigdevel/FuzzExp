sub cpu_time {
my ($user,$system,$cuser,$csystem) = times;
$user + $system
}
sub time_it {
my $action = shift;
my $startTime = cpu_time();
$action->(@_);
my $finishTime = cpu_time();
$finishTime - $startTime
}
printf "Identity(4) takes %f seconds.\n", time_it(sub {@_}, 4);
sub sum {
my $x = shift;
foreach (0 .. 999999) {
$x += $_;
}
$x
}
printf "Sum(4) takes %f seconds.\n", time_it(\&sum, 4);
