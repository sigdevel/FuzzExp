#!/usr/bin/perl -d
use Test::More tests => 1;
BEGIN
{
no warnings 'once';
if($] <= 5.010000)
{
pass;
done_testing;
}
else
{
push(@DB::typeahead, 'c');
}
push(@DB::typeahead, 'q');
open(my $out, '>', \my $out_buf) or warn "Could not open new out handle - $!";
$DB::OUT = $out;
open(my $in, '<', \my $in_buf)  or warn "Could not open new in handle - $!";
$DB::IN = $in;
}
use FindBin qw($Bin);
use lib "$Bin/lib";
require Person1;
delete $INC{'Person1.pm'};
eval { require Person1 };
ok(!$@, 'double load');
done_testing;
