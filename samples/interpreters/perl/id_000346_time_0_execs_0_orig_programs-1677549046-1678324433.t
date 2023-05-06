#!perl -w -I..
use Test::More;
my @required = qw( /bin/ls /bin/dd /bin/mount /bin/cp /bin/tar );
my @optional = qw( /usr/sbin/debootstrap /usr/bin/rpmstrap /usr/sbin/xm
/sbin/mkfs.ext3 /sbin/mkfs.xfs /sbin/mkfs.reiserfs
/sbin/mkfs.btrfs
);
foreach my $file ( @required )
{
ok( -x $file , "Required binary installed: $file" );
}
foreach my $file ( @optional )
{
if ( -e $file )
{
ok( -x $file , "Optional binary installed: $file" );
}
}
done_testing();
