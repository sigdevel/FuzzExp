#!./perl
BEGIN {
chdir 't' if -d 't';
@INC = '../lib' if -d '../lib';
END;
@funcs  = qw[cacheout cacheout_close];
$i      = 0;
print "1..8\n";
}
BEGIN {
for my $f (@funcs) {
++$i;
print 'not ' if __PACKAGE__->can($f);
print "ok $i\n";
}
}
BEGIN {
use FileCache ();
for my $f (@funcs) {
++$i;
print 'not ' if __PACKAGE__->can($f);
print "ok $i\n";
}
}
{   use FileCache;
for my $f (@funcs) {
++$i;
print 'not ' if !__PACKAGE__->can($f);
print "ok $i\n";
}
}
{   package X;
use FileCache;
for my $f (@main::funcs) {
++$main::i;
print 'not ' if !__PACKAGE__->can($f);
print "ok $main::i\n";
}
}
