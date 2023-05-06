sub ok {
my ($num, $ok, $name) = @_;
$num .= " - $name" if defined $name and length $name;
print $ok ? "ok $num\n" : "not ok $num\n";
$ok;
}
sub num_equal {
my ($num, $left, $right, $name) = @_;
my $ok = ((defined $left) ? $left == $right : undef);
unless (ok ($num, $ok, $name)) {
print "
if (!defined $left) {
print "
} elsif ($left !~ tr/0-9//c) {
print "
} else {
$left =~ s/([^-a-zA-Z0-9_+])/sprintf "\\%03o", ord $1/ge;
print "
}
}
$ok;
}
package dump;
use Carp;
%dump = (
'SCALAR'	=> 'dump_scalar',
'LVALUE'	=> 'dump_scalar',
'ARRAY'		=> 'dump_array',
'HASH'		=> 'dump_hash',
'REF'		=> 'dump_ref',
);
sub main'dump {
my ($object) = @_;
croak "Not a reference!" unless ref($object);
local %dumped;
local %object;
local $count = 0;
local $dumped = '';
&recursive_dump($object, 1);
return $dumped;
}
sub recursive_dump {
my ($object, $link) = @_;
my $what = "$object";
my ($bless, $ref, $addr) = $what =~ /^(\w+)=(\w+)\((0x.*)\)$/;
($ref, $addr) = $what =~ /^(\w+)\((0x.*)\)$/ unless $bless;
$ref = 'REF' if ref($object) eq 'REF';
if ($link && $dumped{$addr}++) {
my $num = $object{$addr};
$dumped .= "OBJECT
return;
}
my $objcount = $count++;
$object{$addr} = $objcount;
croak "Unknown simple type '$ref'" unless defined $dump{$ref};
&{$dump{$ref}}($object);
&bless($bless) if $bless;
$dumped .= "OBJECT $objcount\n";
}
sub bless {
my ($class) = @_;
$dumped .= "BLESS $class\n";
}
sub dump_scalar {
my ($sref) = @_;
my $scalar = $$sref;
unless (defined $scalar) {
$dumped .= "UNDEF\n";
return;
}
my $len = length($scalar);
$dumped .= "SCALAR len=$len $scalar\n";
}
sub dump_array {
my ($aref) = @_;
my $items = 0 + @{$aref};
$dumped .= "ARRAY items=$items\n";
foreach $item (@{$aref}) {
unless (defined $item) {
$dumped .= 'ITEM_UNDEF' . "\n";
next;
}
$dumped .= 'ITEM ';
&recursive_dump(\$item, 1);
}
}
sub dump_hash {
my ($href) = @_;
my $items = scalar(keys %{$href});
$dumped .= "HASH items=$items\n";
foreach $key (sort keys %{$href}) {
$dumped .= 'KEY ';
&recursive_dump(\$key, undef);
unless (defined $href->{$key}) {
$dumped .= 'VALUE_UNDEF' . "\n";
next;
}
$dumped .= 'VALUE ';
&recursive_dump(\$href->{$key}, 1);
}
}
sub dump_ref {
my ($rref) = @_;
my $deref = $$rref;
$dumped .= 'REF ';
&recursive_dump($deref, 1);
}
1;
