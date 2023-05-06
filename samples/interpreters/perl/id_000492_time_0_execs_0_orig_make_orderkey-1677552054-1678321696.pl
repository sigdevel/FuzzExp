$c->{make_orderkey_ignore_extras} = sub
{
my ($name) = @_;
my  @orderkey;
my $orderkey = uc( unidecode( $name ) );
$orderkey =~ s/[\.]/_/g;
$orderkey =~ s/[^_A-Z0-9]//g;
return $orderkey;
};
$c->{make_name_orderkey} = sub
{
my ($field, $value, $session, $langid, $dataset) = @_;
return unless ref($value) eq 'HASH';
my  @orderkey;
foreach( "family", "given", "honourific" )
{
next unless defined($value->{$_}) && $value->{$_} ne "";
my $name = $value->{$_};
my $orderkey = &$c->{make_orderkey_ignore_extras}( $name );
push  @orderkey, $orderkey;
}
return join( "_" ,  @orderkey );
};
$c->{make_title_orderkey} = sub
{
my( $field, $value, $dataset ) = @_;
$value =~ s/^[^a-z0-9]+//gi;
if( $value =~ s/^(a|an|the) [^a-z0-9]*//i ) { $value .= ", $1"; }
return &$c->{make_orderkey_ignore_extras}( $value );
};
$c->{make_sanitised_value_orderkey} = sub
{
my ($field, $value, $session, $langid, $dataset) = @_;
my $orderkey = &$c->{make_orderkey_ignore_extras}( $value );
return $orderkey;
};
