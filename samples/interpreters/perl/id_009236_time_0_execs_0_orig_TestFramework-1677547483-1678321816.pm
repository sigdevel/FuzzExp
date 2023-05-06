package TestFramework;
$PACKAGE = $Package = "TestFramework";
$VERSION = 20080321;
@ISA= qw( Exporter DynaLoader );
@EXPORT = qw();
@EXPORT_OK = qw();
return( 1 );
sub new
{
my( $type, @Options ) = @_;
my $self = bless {};
my ( $SCRIPT_DIR, $SCRIPT_FILE_NAME ) = ( Win32::GetFullPathName( $0 ) =~ /^(.*)\\([^\\]*)$/ );
@{$self->{default}->{log_path_list}} = ( "$SCRIPT_DIR\\$SCRIPT_FILE_NAME.log", "\\\\.\\pipe\\syslog" );
$self->{log_path_list} = ();
return( $self );
}
sub DESTROY
{
my( $self ) = @_;
$self->LogClose();
undef $self;
}
sub _LogConnect
{
my( $self, $Path ) = @_;
my $FileHandle;
if( open( $FileHandle, ">$Path" ) )
{
local *LOG = $FileHandle;
my $StartTime = localtime();
my $BackupHandle = select( LOG );
$| = 1;
select( $BackupHandle );
push( @{$self->{log_filehandle_list}}, $FileHandle );
print LOG << "EOT"
EOT
}
}
sub LogClear
{
my( $self ) = @_;
$self->{log_path_list} = ();
}
sub LogClose
{
my( $self ) = @_;
foreach $FileHandle ( @{$self->{log_filehandle_list}} )
{
local *LOG = $FileHandle;
if( fileno( LOG ) )
{
close( LOG );
}
}
}
sub LogMessage
{
my( $self, $Message ) = @_;
foreach my $FileHandle ( @{$self->{log_filehandle_list}} )
{
local *LOG = $FileHandle;
if( fileno( LOG ) )
{
print LOG "[" . localtime() . "] $Message\n";
}
}
}
sub LogAdd
{
my( $self, @PathList ) = @_;
if( scalar @{$self->{log_filehandle_list}} )
{
foreach my $Path ( @PathList )
{
$self->_LogConnect( $Path );
}
}
else
{
push( @{$self->{log_path_list}}, @PathList );
}
}
sub LogStart
{
my( $self ) = @_;
return if( scalar @{$self->{log_filehandle_list}} );
if( 0 == scalar @{$self->{log_path_list}} )
{
push( @{$self->{log_path_list}}, @{$self->{default}->{log_path_list}} );
}
foreach my $Path ( @{$self->{log_path_list}} )
{
$self->_LogConnect( $Path );
}
}
