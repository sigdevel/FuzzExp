package IO::Seekable;
use 5.006_001;
use Carp;
use strict;
our($VERSION, @EXPORT, @ISA);
use IO::Handle ();
use Fcntl qw(SEEK_SET SEEK_CUR SEEK_END);
require Exporter;
@EXPORT = qw(SEEK_SET SEEK_CUR SEEK_END);
@ISA = qw(Exporter);
$VERSION = "1.10";
$VERSION = eval $VERSION;
sub seek {
@_ == 3 or croak 'usage: $io->seek(POS, WHENCE)';
seek($_[0], $_[1], $_[2]);
}
sub sysseek {
@_ == 3 or croak 'usage: $io->sysseek(POS, WHENCE)';
sysseek($_[0], $_[1], $_[2]);
}
sub tell {
@_ == 1 or croak 'usage: $io->tell()';
tell($_[0]);
}
1;
