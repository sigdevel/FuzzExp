package OpenGL::Spec;
my %typemap = (
bitfield    => "GLbitfield",
boolean     => "GLboolean",
Boolean     => "GLboolean",
byte        => "GLbyte",
clampd      => "GLclampd",
clampf      => "GLclampf",
double      => "GLdouble",
enum        => "GLenum",
Glenum      => "GLenum",
float       => "GLfloat",
half        => "GLuint",
int         => "GLint",
short       => "GLshort",
sizei       => "GLsizei",
ubyte       => "GLubyte",
uint        => "GLuint",
ushort      => "GLushort",
DMbuffer    => "void *",
sizeiptrARB => "GLsizeiptrARB",
intptrARB   => "GLintptrARB",
charARB     => "GLcharARB",
handleARB   => "GLhandleARB",
);
my %void_typemap = (
void    => "GLvoid",
);
my $section_re  = qr{^[A-Z]};
my $function_re = qr{^(.+) ([a-z][a-z0-9_]*) \((.+)\)$}i;
my $token_re    = qr{^([A-Z0-9][A-Z0-9_]*):?\s+((?:0x)?[0-9A-F]+)(.*)$};
my $prefix_re   = qr{^(?:AGL | GLX | WGL)_}x;
my $eofnc_re    = qr{ \);?$ | ^$ }x;
my $function_re = qr{^(.+) ([a-z][a-z0-9_]*) \((.+)\)$}i;
my $prefix_re   = qr{^(?:gl | agl | wgl | glX)}x;
my $types_re    = __compile_wordlist_cap(keys %typemap);
my $voidtype_re = __compile_wordlist_cap(keys %void_typemap);
sub new($)
{
my $class = shift;
my $self = { section => {} };
$self->{filename} = shift;
local $/;
open(my $fh, "<$self->{filename}") or die "Can't open $self->{filename}";
my $content = <$fh>;
my $section;
my $s = $self->{section};
$content =~ s{[ \t]+$}{}mg;
$content =~ s{(\w)\n(\w)}{$1 $2}sg;
foreach (split /\n/, $content)
{
if (/$section_re/)
{
chomp;
s/^Name String$/Name Strings/;
$section = $_;
$s->{$section} = "";
}
elsif (defined $section and exists $s->{$section})
{
s{^\s+}{}mg;
$s->{$section} .= $_ . "\n";
}
}
$s->{$_} =~ s{(?:^\n+|\n+$)}{}s foreach keys %$s;
bless $self, $class;
}
sub sections()
{
my $self = shift;
keys %{$self->{section}};
}
sub name()
{
my $self = shift;
$self->{section}->{Name};
}
sub name_strings()
{
my $self = shift;
split("\n", $self->{section}->{"Name Strings"});
}
sub tokens()
{
my $self = shift;
my %tokens = ();
foreach (split /\n/, $self->{section}->{"New Tokens"})
{
next unless /$token_re/;
my ($name, $value) = ($1, $2);
$name =~ s{^}{GL_} unless $name =~ /$prefix_re/;
$tokens{$name} = $value;
}
return %tokens;
}
sub functions()
{
my $self = shift;
my %functions = ();
my @fnc = ();
foreach (split /\n/, $self->{section}->{"New Procedures and Functions"})
{
push @fnc, $_ unless ($_ eq "" or $_ eq "None");
next unless /$eofnc_re/;
if (__normalize_proto(@fnc) =~ /$function_re/)
{
my ($return, $name, $parms) = ($1, $2, $3);
if (!__ignore_function($name, $extname))
{
$name =~ s/^/gl/ unless $name =~ /$prefix_re/;
if ($name =~ /^gl/ && $name !~ /^glX/)
{
$return =~ s/$types_re/$typemap{$1}/g;
$return =~ s/$voidtype_re/$void_typemap{$1}/g;
$parms  =~ s/$types_re/$typemap{$1}/g;
$parms  =~ s/$voidtype_re/$void_typemap{$1}/g;
}
$functions{$name} = {
rtype => $return,
parms => $parms,
};
}
}
@fnc = ();
}
return %functions;
}
sub __normalize_proto
{
local $_ = join(" ", @_);
s/\s+/ /g;
s/\s*\(\s*/ \(/;
s/\s*\)\s*/\)/;
s/\s*\*([a-zA-Z])/\* $1/;
s/\*wgl/\* wgl/;
s/\*glX/\* glX/;
s/\.\.\./void/;
s/;$//;
return $_;
}
sub __ignore_function
{
return 0;
}
sub __compile_regex
{
my $regex = join('', @_);
return qr/$regex/
}
sub __compile_wordlist_cap
{
__compile_regex('\b(', join('|', @_), ')\b');
}
