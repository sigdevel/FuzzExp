$smtpplver = 'YaBB 3.0 Beta $Revision: 100 $';
if ($action eq 'detailedversion') { return 1; }
eval q^
use IO::Socket::INET;
use Digest::HMAC_MD5 qw(hmac_md5_hex);
^;
&LoadLanguage('Smtp');
sub use_smtp {
$| = 1;
my ($proto)    = (getprotobyname('tcp'))[2];
my ($port)     = (getservbyname('smtp', 'tcp'))[2] || 25;
my ($smtpaddr) = ($smtp_server =~ /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/) ? pack('C4', $1, $2, $3, $4) : (gethostbyname($smtp_server))[4];
$sendlog = "";
$auth_ok = 0;
$sock = IO::Socket::INET->new(
PeerAddr => $smtp_server,
PeerPort => $port,
Proto => 'tcp',
Timeout => 5)
or &fatal_error("smtp_unavail");
&get_line;
&say_hello ($smtp_server) or exit (1);
if (defined ($features{'AUTH'}) && $smtp_auth_required) {
if ($auth_ok == 0 && ($features{'AUTH'} =~ /CRAM-MD5/i || $smtp_auth_required == 3 || $smtp_auth_required == 4)) {
&send_line ("AUTH CRAM-MD5\r\n");
($code, $text, $more) = &get_line;
if ($code != 334 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
my $response = &encode_cram_md5 ($text, $authuser, $authpass);
&send_line ("%s\r\n", $response);
($code, $text, $more) = &get_line;
if ($code != 235 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
$auth_ok = 1;
}
elsif ($auth_ok == 0 && ($features{'AUTH'} =~ /LOGIN/i  || $smtp_auth_required == 2 || $smtp_auth_required == 4)) {
&send_line ("AUTH LOGIN\r\n");
($code, $text, $more) = &get_line;
if ($code != 334 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
&send_line ("%s\r\n", encode_smtp64 ($authuser, ""));
($code, $text, $more) = &get_line;
if ($code != 334 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
&send_line ("%s\r\n", encode_smtp64 ($authpass, ""));
($code, $text, $more) = &get_line;
if ($code != 235 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
$auth_ok = 1;
}
elsif ($auth_ok == 0 && ($features{'AUTH'} =~ /PLAIN/i || $smtp_auth_required == 1 || $smtp_auth_required == 4)) {
&send_line ("AUTH PLAIN %s\r\n",
encode_smtp64 ("$authuser\0$authuser\0$authpass", ""));
($code, $text, $more) = &get_line;
if ($code != 235 && $smtp_auth_required != 4)
{
&fatal_error("smtp_error","[$code]: $smtp_txt{$code}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
$auth_ok = 1;
}
else
{
&fatal_error("smtp_error","$smtp_txt{'notsupported'}<br /><br /><b>$smtp_txt{'5'}</b><br />$sendlog");
}
}
($smtpsec, $smtpmin, $smtphour, $smtpmday, $smtpmon, $smtpyear, $smtpwday, $smtpyday, $smtpisdst) = gmtime($date + (3600 * $timeoffset));
$smtpyear       = sprintf("%02d", ($smtpyear - 100));
$smtphour       = sprintf("%02d", $smtphour);
$smtpmin        = sprintf("%02d", $smtpmin);
$smtpsec        = sprintf("%02d", $smtpsec);
my @months2     = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
$smtpyear       = qq~20$smtpyear~;
$smtptimestring = qq~$days_short[$smtpwday], $smtpmday $months2[$smtpmon] $smtpyear $smtphour\:$smtpmin\:$smtpsec +0000~;
&send_line ("MAIL FROM: <$smtp_from>\r\n");
($code, $text, $more) = &get_line;
foreach (split(/, /, $smtp_to)) {
&send_line ("RCPT TO: <$_>\r\n");
($code, $text, $more) = &get_line;
}
&send_line ("DATA\r\n");
($code, $text, $more) = &get_line;
&send_line ("To: $toheader\r\n");
&send_line ("Date: $smtptimestring\r\n");
&send_line ("From: $fromheader\r\n");
&send_line ("X-Mailer: YaBB SMTP\r\n");
&send_line ("Subject: $smtp_subject\r\n");
&send_line ("Content-Type: text/plain\; charset=$smtp_charset\r\n\r\n");
&send_line ("$smtp_message");
&send_line ("\r\n.\r\n");
&send_line ("QUIT\r\n");
if ($smtp_from eq ""){ $proto_error = "$smtp_txt{'no_from'}<br />"; }
if ($smtp_to eq ""){ $proto_error .= "$smtp_txt{'no_to'}<br />"; }
if ($proto_error){
&fatal_error("smtp_error","<br />$proto_error<br />$sendlog");
}
return 1;
}
sub get_line {
my ($code, $sep, $text) = ($sock->getline() =~ /(\d+)(.)([^\r]*)/);
my $more;
$code =~ s/ //g;
if ($sep eq "-") { $more = 1; } else { $more = 0; }
$sendlog .= qq~S:$code $text $sep~;
$sendlog .= qq~<br />~;
return ($code, $text, $more);
}
sub send_line (@) {
my @args = @_;
$sendlog .= qq~C:$args[0]~;
$sendlog =~ s/\r\n//g;
$sendlog .= qq~<br />~;
$sock->printf (@args);
}
sub encode_cram_md5 ($$$) {
my ($ticket64, $username, $password) = @_;
my $ticket = decode_smtp64($ticket64) or
die ("Unable to decode Base64 encoded string '$ticket64'\n");
my $password_md5 = hmac_md5_hex($ticket, $password);
return encode_smtp64 ("$username $password_md5", "");
}
sub encode_smtp64 {
if ($] >= 5.006) {
require bytes;
if (bytes::length($_[0]) > length($_[0]) ||
($] >= 5.008 && $_[0] =~ /[^\0-\xFF]/))
{
require Carp;
Carp::croak("The Base64 encoding is only defined for bytes");
}
}
require integer;
import integer;
my $eol = $_[1];
$eol = "\n" unless defined $eol;
my $res = pack("u", $_[0]);
$res =~ s/^.//mg;
$res =~ s/\n//g;
$res =~ tr|` -_|AA-Za-z0-9+/|;
my $padding = (3 - length($_[0]) % 3) % 3;
$res =~ s/.{$padding}$/'=' x $padding/e if $padding;
if (length $eol) {
$res =~ s/(.{1,76})/$1$eol/g;
}
chomp $res;
return $res;
}
sub decode_smtp64 ($)
{
local($^W) = 0;
require integer;
import integer;
my $str = shift;
$str =~ tr|A-Za-z0-9+=/||cd;
$str =~ s/=+$//;
$str =~ tr|A-Za-z0-9+/| -_|;
return "" unless length $str;
my $uustr = '';
my ($i, $l);
$l = length($str) - 60;
for ($i = 0; $i <= $l; $i += 60) {
$uustr .= "M" . substr($str, $i, 60);
}
$str = substr($str, $i);
if ($str ne "") {
$uustr .= chr(32 + length($str)*3/4) . $str;
}
return unpack ("u", $uustr);
}
sub say_hello ($) {
my ($hello_host) = $_[0];
my ($feat, $param);
&send_line ("EHLO $hello_host\r\n");
($code, $text, $more) = &get_line;
if($code != 250){
&send_line ("HELO $hello_host\r\n");
}
($code, $text, $more) = &get_line;
if($code == 250){
&read_features(\%features);
}
return 1;
}
sub read_features ($) {
my ($featref) = $_[0];
%{$featref} = ();
($feat, $param) = ($text =~ /^(\w+)[= ]*(.*)$/);
$featref->{$feat} = $param;
while ($more == 1) {
($code, $text, $more) = &get_line;
($feat, $param) = ($text =~ /^(\w+)[= ]*(.*)$/);
$featref->{$feat} = $param;
}
return 1;
}
1;
