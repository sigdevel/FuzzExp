package Java;
sub inline {
}
sub type ($$) {
my ( $class, $type ) = @_;
my $array = "";
while ( index($type, "<") != -1 ) {
$type =~ s/<[^<>]*>//;
}
while ( substr( $type, -2, 2 ) eq "[]" ) {
$type = substr( $type, 0, -2 );
$array .= "[";
}
if    ( $type eq "boolean" ) { $type = $array . "Z"; }
elsif ( $type eq "byte" )    { $type = $array . "B"; }
elsif ( $type eq "char" )    { $type = $array . "C"; }
elsif ( $type eq "double" )  { $type = $array . "D"; }
elsif ( $type eq "float" )   { $type = $array . "F"; }
elsif ( $type eq "int" )     { $type = $array . "I"; }
elsif ( $type eq "long" )    { $type = $array . "J"; }
elsif ( $type eq "short" )   { $type = $array . "S"; }
elsif ( $array )             { $type = $array . "L" . $type . ";" }
_type($type);
}
sub _type ($) {
my $class;
eval {
$class = Java::inline q{
Class.forName( List__.aget(0).toString() )
}
};
return $class;
}
1;
