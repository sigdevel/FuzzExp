require 5;
package Pod::Simple::Transcode;
BEGIN {
if(defined &DEBUG) {;}
elsif( defined &Pod::Simple::DEBUG ) { *DEBUG = \&Pod::Simple::DEBUG; }
else { *DEBUG = sub () {0}; }
}
foreach my $class (
'Pod::Simple::TranscodeSmart',
'Pod::Simple::TranscodeDumb',
'',
) {
$class or die "Couldn't load any encoding classes";
DEBUG and print "About to try loading $class...\n";
eval "require $class;";
if($@) {
DEBUG and print "Couldn't load $class: $@\n";
} else {
DEBUG and print "OK, loaded $class.\n";
@ISA = ($class);
last;
}
}
sub _blorp { return; }
1;
__END__
