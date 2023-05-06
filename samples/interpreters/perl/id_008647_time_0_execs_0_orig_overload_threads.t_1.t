BEGIN {
if( $ENV{PERL_CORE} ) {
chdir 't';
@INC = ('../lib', 'lib');
}
else {
unshift @INC, 't/lib';
}
}
chdir 't';
BEGIN {
eval { require threads; 'threads'->import; 1; };
}
use Test::More tests => 5;
package Overloaded;
use overload
q{""} => sub { $_[0]->{string} };
sub new {
my $class = shift;
bless { string => shift }, $class;
}
package main;
my $warnings = '';
local $SIG{__WARN__} = sub { $warnings = join '', @_ };
my $obj = Overloaded->new('foo');
ok( 1, $obj );
my $undef = Overloaded->new(undef);
pass( $undef );
is( $warnings, '' );
TODO: {
my $obj = Overloaded->new('not really todo, testing overloaded reason');
local $TODO = $obj;
fail("Just checking todo as an overloaded value");
}
SKIP: {
my $obj = Overloaded->new('not really skipped, testing overloaded reason');
skip $obj, 1;
}
