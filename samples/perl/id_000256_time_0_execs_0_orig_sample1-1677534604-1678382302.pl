our ( %COMMON, %PAC, %TERMINAL, %SHARED );
sub SESSION
{
$SHARED{cmd} = $COMMON{subst}( "<ASK:Command to send|ls -lF|df -h|uptime|date>" );
$PAC{msg}( "Starting connections\nPlease, wait..." );
my ( $uuid1, $tmp_uuid1 ) = $PAC{start_manual}( 'localhost' );
if ( ! $uuid1 ) {
$PAC{msg}( "'localhost' not found!", 1 );
return 0;
}
my ( $uuid2, $tmp_uuid2 ) = $PAC{start}( 'connection2' );
if ( ! $uuid2 ) {
$PAC{msg}( "'connection2' not found!", 1 );
}
my ( $uuid3, $tmp_uuid3 ) = $PAC{start_manual}( 'connection3' );
if ( ! $uuid3 ) {
$PAC{msg}( "'connection3' not found!", 1 );
}
$PAC{msg}();
return 1;
}
sub CONNECTION
{
my $prompt;
if ( $TERMINAL{name} eq 'connection1' ) {
$prompt = '\[david@connection1 ~\]';
}
elsif ( $TERMINAL{name} eq 'connection2' ) {
$prompt = '\[root@connection2 .+\]';
}
elsif ( $TERMINAL{name} eq 'localhost' ) {
$prompt = '\[david@david-laptop ~\]';
}
if ( $TERMINAL{name} eq 'localhost' ) {
$TERMINAL{send}( "password3\n" );
if ( ! $TERMINAL{expect}( $prompt, 2 ) )
{
$TERMINAL{msg}( "Wrong password provided. Asking for one..." );
$TERMINAL{send}( $TERMINAL{ask}( "Enter Password for $TERMINAL{name}...", 0 ) . "\n" );
}
if ( ! $TERMINAL{expect}( $prompt, 2 ) )
{
$TERMINAL{msg}( "2nd Wrong password provided. Finishing..." );
return 0;
}
}
$TERMINAL{send}( "$SHARED{cmd}\n" );
$TERMINAL{expect}( $prompt, 2 ) or $TERMINAL{msg}( "Error3: $TERMINAL{error}" );
if ( ! defined $TERMINAL{out1} ) {
$TERMINAL{msg}( "Could not capture command output (check if '\$prompt' variable ($prompt) matches real prompt)" );
return 0;
}
if ( ! open( F, '>>/tmp/sample1.txt' ) ) {
$TERMINAL{msg}( "Could not open file '/tmp/sample1.txt' for writting: $!" );
}
print F "**** CONNECTION '$TERMINAL{name}' OUTPUT:\n";
print F $TERMINAL{out1} . "\n";
close F;
return 1;
}
return 1;
