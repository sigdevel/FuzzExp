package SelfLoader;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(AUTOLOAD);
$VERSION = "1.0904";
sub Version {$VERSION}
$DEBUG = 0;
my %Cache;
our $nested;
$nested = qr{ \( (?: (?> [^()]+ ) | (??{ $nested }) )* \) }x;
our $one_attr = qr{ (?> (?! \d) \w+ (?:$nested)? ) (?:\s*\:\s*|\s+(?!\:)) }x;
our $attr_list = qr{ \s* : \s* (?: $one_attr )* }x;
sub croak { require Carp; goto &Carp::croak }
AUTOLOAD {
print STDERR "SelfLoader::AUTOLOAD for $AUTOLOAD\n" if $DEBUG;
my $SL_code = $Cache{$AUTOLOAD};
my $save = $@;
unless ($SL_code) {
$AUTOLOAD =~ m/^(.*)::/;
SelfLoader->_load_stubs($1) unless exists $Cache{"${1}::<DATA"};
$SL_code = $Cache{$AUTOLOAD};
$SL_code = "sub $AUTOLOAD { }"
if (!$SL_code and $AUTOLOAD =~ m/::DESTROY$/);
croak "Undefined subroutine $AUTOLOAD" unless $SL_code;
}
print STDERR "SelfLoader::AUTOLOAD eval: $SL_code\n" if $DEBUG;
eval $SL_code;
if ($@) {
$@ =~ s/ at .*\n//;
croak $@;
}
$@ = $save;
defined(&$AUTOLOAD) || die "SelfLoader inconsistency error";
delete $Cache{$AUTOLOAD};
goto &$AUTOLOAD
}
sub load_stubs { shift->_load_stubs((caller)[0]) }
sub _load_stubs {
my($self, $callpack, $endlines) = @_;
my $fh = \*{"${callpack}::DATA"};
my $currpack = $callpack;
my($line,$name,@lines, @stubs, $protoype);
print STDERR "SelfLoader::load_stubs($callpack)\n" if $DEBUG;
croak("$callpack doesn't contain an __DATA__ token")
unless fileno($fh);
$Cache{"${currpack}::<DATA"} = 1;
local($/) = "\n";
while(defined($line = <$fh>) and $line !~ m/^__END__/) {
if ($line =~ m/^sub\s+([\w:]+)\s*((?:\([\\\$\@\%\&\*\;]*\))?(?:$attr_list)?)/) {
push(@stubs, $self->_add_to_cache($name, $currpack, \@lines, $protoype));
$protoype = $2;
@lines = ($line);
if (index($1,'::') == -1) {
$name = "${currpack}::$1";
} else {
$name = $1;
$name =~ m/^(.*)::/;
if (defined(&{"${1}::AUTOLOAD"})) {
\&{"${1}::AUTOLOAD"} == \&SelfLoader::AUTOLOAD ||
die 'SelfLoader Error: attempt to specify Selfloading',
" sub $name in non-selfloading module $1";
} else {
$self->export($1,'AUTOLOAD');
}
}
} elsif ($line =~ m/^package\s+([\w:]+)/) {
push(@stubs, $self->_add_to_cache($name, $currpack, \@lines, $protoype));
$self->_package_defined($line);
$name = '';
@lines = ();
$currpack = $1;
$Cache{"${currpack}::<DATA"} = 1;
if (defined(&{"${1}::AUTOLOAD"})) {
\&{"${1}::AUTOLOAD"} == \&SelfLoader::AUTOLOAD ||
die 'SelfLoader Error: attempt to specify Selfloading',
" package $currpack which already has AUTOLOAD";
} else {
$self->export($currpack,'AUTOLOAD');
}
} else {
push(@lines,$line);
}
}
if (defined($line) && $line =~ /^__END__/) {
unless ($line =~ /^__END__\s*DATA/) {
if ($endlines) {
@$endlines = <$fh>;
}
close($fh);
}
}
push(@stubs, $self->_add_to_cache($name, $currpack, \@lines, $protoype));
eval join('', @stubs) if @stubs;
}
sub _add_to_cache {
my($self,$fullname,$pack,$lines, $protoype) = @_;
return () unless $fullname;
(require Carp), Carp::carp("Redefining sub $fullname")
if exists $Cache{$fullname};
$Cache{$fullname} = join('', "package $pack; ",@$lines);
print STDERR "SelfLoader cached $fullname: $Cache{$fullname}" if $DEBUG;
defined($protoype) ? "sub $fullname $protoype;" : "sub $fullname;"
}
sub _package_defined {}
1;
__END__
=head1 NAME
SelfLoader - load functions only on demand
=head1 SYNOPSIS
package FOOBAR;
use SelfLoader;
... (initializing code)
__DATA__
sub {....
=head1 DESCRIPTION
This module tells its users that functions in the FOOBAR package are to be
autoloaded from after the C<__DATA__> token.  See also
L<perlsub/"Autoloading">.
=head2 The __DATA__ token
The C<__DATA__> token tells the perl compiler that the perl code
for compilation is finished. Everything after the C<__DATA__> token
is available for reading via the filehandle FOOBAR::DATA,
where FOOBAR is the name of the current package when the C<__DATA__>
token is reached. This works just the same as C<__END__> does in
package 'main', but for other modules data after C<__END__> is not
automatically retrievable, whereas data after C<__DATA__> is.
The C<__DATA__> token is not recognized in versions of perl prior to
5.001m.
Note that it is possible to have C<__DATA__> tokens in the same package
in multiple files, and that the last C<__DATA__> token in a given
package that is encountered by the compiler is the one accessible
by the filehandle. This also applies to C<__END__> and main, i.e. if
the 'main' program has an C<__END__>, but a module 'require'd (_not_ 'use'd)
by that program has a 'package main;' declaration followed by an 'C<__DATA__>',
then the C<DATA> filehandle is set to access the data after the C<__DATA__>
in the module, _not_ the data after the C<__END__> token in the 'main'
program, since the compiler encounters the 'require'd file later.
=head2 SelfLoader autoloading
The B<SelfLoader> works by the user placing the C<__DATA__>
token I<after> perl code which needs to be compiled and
run at 'require' time, but I<before> subroutine declarations
that can be loaded in later - usually because they may never
be called.
The B<SelfLoader> will read from the FOOBAR::DATA filehandle to
load in the data after C<__DATA__>, and load in any subroutine
when it is called. The costs are the one-time parsing of the
data after C<__DATA__>, and a load delay for the _first_
call of any autoloaded function. The benefits (hopefully)
are a speeded up compilation phase, with no need to load
functions which are never used.
The B<SelfLoader> will stop reading from C<__DATA__> if
it encounters the C<__END__> token - just as you would expect.
If the C<__END__> token is present, and is followed by the
token DATA, then the B<SelfLoader> leaves the FOOBAR::DATA
filehandle open on the line after that token.
The B<SelfLoader> exports the C<AUTOLOAD> subroutine to the
package using the B<SelfLoader>, and this loads the called
subroutine when it is first called.
There is no advantage to putting subroutines which will _always_
be called after the C<__DATA__> token.
=head2 Autoloading and package lexicals
A 'my $pack_lexical' statement makes the variable $pack_lexical
local _only_ to the file up to the C<__DATA__> token. Subroutines
declared elsewhere _cannot_ see these types of variables,
just as if you declared subroutines in the package but in another
file, they cannot see these variables.
So specifically, autoloaded functions cannot see package
lexicals (this applies to both the B<SelfLoader> and the Autoloader).
The C<vars> pragma provides an alternative to defining package-level
globals that will be visible to autoloaded routines. See the documentation
on B<vars> in the pragma section of L<perlmod>.
=head2 SelfLoader and AutoLoader
The B<SelfLoader> can replace the AutoLoader - just change 'use AutoLoader'
to 'use SelfLoader' (though note that the B<SelfLoader> exports
the AUTOLOAD function - but if you have your own AUTOLOAD and
are using the AutoLoader too, you probably know what you're doing),
and the C<__END__> token to C<__DATA__>. You will need perl version 5.001m
or later to use this (version 5.001 with all patches up to patch m).
There is no need to inherit from the B<SelfLoader>.
The B<SelfLoader> works similarly to the AutoLoader, but picks up the
subs from after the C<__DATA__> instead of in the 'lib/auto' directory.
There is a maintenance gain in not needing to run AutoSplit on the module
at installation, and a runtime gain in not needing to keep opening and
closing files to load subs. There is a runtime loss in needing
to parse the code after the C<__DATA__>. Details of the B<AutoLoader> and
another view of these distinctions can be found in that module's
documentation.
=head2 __DATA__, __END__, and the FOOBAR::DATA filehandle.
This section is only relevant if you want to use
the C<FOOBAR::DATA> together with the B<SelfLoader>.
Data after the C<__DATA__> token in a module is read using the
FOOBAR::DATA filehandle. C<__END__> can still be used to denote the end
of the C<__DATA__> section if followed by the token DATA - this is supported
by the B<SelfLoader>. The C<FOOBAR::DATA> filehandle is left open if an
C<__END__> followed by a DATA is found, with the filehandle positioned at
the start of the line after the C<__END__> token. If no C<__END__> token is
present, or an C<__END__> token with no DATA token on the same line, then
the filehandle is closed.
The B<SelfLoader> reads from wherever the current
position of the C<FOOBAR::DATA> filehandle is, until the
EOF or C<__END__>. This means that if you want to use
that filehandle (and ONLY if you want to), you should either
1. Put all your subroutine declarations immediately after
the C<__DATA__> token and put your own data after those
declarations, using the C<__END__> token to mark the end
of subroutine declarations. You must also ensure that the B<SelfLoader>
reads first by  calling 'SelfLoader-E<gt>load_stubs();', or by using a
function which is selfloaded;
or
2. You should read the C<FOOBAR::DATA> filehandle first, leaving
the handle open and positioned at the first line of subroutine
declarations.
You could conceivably do both.
=head2 Classes and inherited methods.
For modules which are not classes, this section is not relevant.
This section is only relevant if you have methods which could
be inherited.
A subroutine stub (or forward declaration) looks like
sub stub;
i.e. it is a subroutine declaration without the body of the
subroutine. For modules which are not classes, there is no real
need for stubs as far as autoloading is concerned.
For modules which ARE classes, and need to handle inherited methods,
stubs are needed to ensure that the method inheritance mechanism works
properly. You can load the stubs into the module at 'require' time, by
adding the statement 'SelfLoader-E<gt>load_stubs();' to the module to do
this.
The alternative is to put the stubs in before the C<__DATA__> token BEFORE
releasing the module, and for this purpose the C<Devel::SelfStubber>
module is available.  However this does require the extra step of ensuring
that the stubs are in the module. If this is done I strongly recommend
that this is done BEFORE releasing the module - it should NOT be done
at install time in general.
=head1 Multiple packages and fully qualified subroutine names
Subroutines in multiple packages within the same file are supported - but you
should note that this requires exporting the C<SelfLoader::AUTOLOAD> to
every package which requires it. This is done automatically by the
B<SelfLoader> when it first loads the subs into the cache, but you should
really specify it in the initialization before the C<__DATA__> by putting
a 'use SelfLoader' statement in each package.
Fully qualified subroutine names are also supported. For example,
__DATA__
sub foo::bar {23}
package baz;
sub dob {32}
will all be loaded correctly by the B<SelfLoader>, and the B<SelfLoader>
will ensure that the packages 'foo' and 'baz' correctly have the
B<SelfLoader> C<AUTOLOAD> method when the data after C<__DATA__> is first
parsed.
=cut
