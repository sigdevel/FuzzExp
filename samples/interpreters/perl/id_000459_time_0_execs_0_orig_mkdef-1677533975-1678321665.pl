#!/usr/local/bin/perl -w
my $debug=0;
my $crypto_num= "util/libeay.num";
my $ssl_num=    "util/ssleay.num";
my $libname;
my $do_update = 0;
my $do_rewrite = 1;
my $do_crypto = 0;
my $do_ssl = 0;
my $do_ctest = 0;
my $do_ctestall = 0;
my $do_checkexist = 0;
my $VMSVAX=0;
my $VMSAlpha=0;
my $VMS=0;
my $W32=0;
my $W16=0;
my $NT=0;
my $OS2=0;
my $safe_stack_def = 0;
my @known_platforms = ( "__FreeBSD__", "PERL5", "NeXT",
"EXPORT_VAR_AS_FUNCTION" );
my @known_ossl_platforms = ( "VMS", "WIN16", "WIN32", "WINNT", "OS2" );
my @known_algorithms = ( "RC2", "RC4", "RC5", "IDEA", "DES", "BF",
"CAST", "MD2", "MD4", "MD5", "SHA", "SHA0", "SHA1",
"SHA256", "SHA512", "RIPEMD",
"MDC2", "RSA", "DSA", "DH", "EC", "ECDH", "ECDSA", "HMAC", "AES",
"EVP", "X509", "ASN1_TYPEDEFS",
"BIO", "COMP", "BUFFER", "LHASH", "STACK", "ERR",
"LOCKING",
"FP_API", "STDIO", "SOCK", "KRB5", "DGRAM",
"STATIC_ENGINE", "ENGINE", "HW", "GMP",
"DEPRECATED" );
my $options="";
open(IN,"<Makefile") || die "unable to open Makefile!\n";
while(<IN>) {
$options=$1 if (/^OPTIONS=(.*)$/);
}
close(IN);
my $no_rc2; my $no_rc4; my $no_rc5; my $no_idea; my $no_des; my $no_bf;
my $no_cast;
my $no_md2; my $no_md4; my $no_md5; my $no_sha; my $no_ripemd; my $no_mdc2;
my $no_rsa; my $no_dsa; my $no_dh; my $no_hmac=0; my $no_aes; my $no_krb5;
my $no_ec; my $no_ecdsa; my $no_ecdh; my $no_engine; my $no_hw;
my $no_fp_api; my $no_static_engine; my $no_gmp; my $no_deprecated;
foreach (@ARGV, split(/ /, $options))
{
$debug=1 if $_ eq "debug";
$W32=1 if $_ eq "32";
$W16=1 if $_ eq "16";
if($_ eq "NT") {
$W32 = 1;
$NT = 1;
}
if ($_ eq "VMS-VAX") {
$VMS=1;
$VMSVAX=1;
}
if ($_ eq "VMS-Alpha") {
$VMS=1;
$VMSAlpha=1;
}
$VMS=1 if $_ eq "VMS";
$OS2=1 if $_ eq "OS2";
$do_ssl=1 if $_ eq "ssleay";
if ($_ eq "ssl") {
$do_ssl=1;
$libname=$_
}
$do_crypto=1 if $_ eq "libeay";
if ($_ eq "crypto") {
$do_crypto=1;
$libname=$_;
}
$do_update=1 if $_ eq "update";
$do_rewrite=1 if $_ eq "rewrite";
$do_ctest=1 if $_ eq "ctest";
$do_ctestall=1 if $_ eq "ctestall";
$do_checkexist=1 if $_ eq "exist";
if    (/^no-rc2$/)      { $no_rc2=1; }
elsif (/^no-rc4$/)      { $no_rc4=1; }
elsif (/^no-rc5$/)      { $no_rc5=1; }
elsif (/^no-idea$/)     { $no_idea=1; }
elsif (/^no-des$/)      { $no_des=1; $no_mdc2=1; }
elsif (/^no-bf$/)       { $no_bf=1; }
elsif (/^no-cast$/)     { $no_cast=1; }
elsif (/^no-md2$/)      { $no_md2=1; }
elsif (/^no-md4$/)      { $no_md4=1; }
elsif (/^no-md5$/)      { $no_md5=1; }
elsif (/^no-sha$/)      { $no_sha=1; }
elsif (/^no-ripemd$/)   { $no_ripemd=1; }
elsif (/^no-mdc2$/)     { $no_mdc2=1; }
elsif (/^no-rsa$/)      { $no_rsa=1; }
elsif (/^no-dsa$/)      { $no_dsa=1; }
elsif (/^no-dh$/)       { $no_dh=1; }
elsif (/^no-ec$/)       { $no_ec=1; }
elsif (/^no-ecdsa$/)	{ $no_ecdsa=1; }
elsif (/^no-ecdh$/) 	{ $no_ecdh=1; }
elsif (/^no-hmac$/)	{ $no_hmac=1; }
elsif (/^no-aes$/)	{ $no_aes=1; }
elsif (/^no-evp$/)	{ $no_evp=1; }
elsif (/^no-lhash$/)	{ $no_lhash=1; }
elsif (/^no-stack$/)	{ $no_stack=1; }
elsif (/^no-err$/)	{ $no_err=1; }
elsif (/^no-buffer$/)	{ $no_buffer=1; }
elsif (/^no-bio$/)	{ $no_bio=1; }
elsif (/^no-comp$/)	{ $no_comp=1; }
elsif (/^no-dso$/)	{ $no_dso=1; }
elsif (/^no-krb5$/)	{ $no_krb5=1; }
elsif (/^no-engine$/)	{ $no_engine=1; }
elsif (/^no-hw$/)	{ $no_hw=1; }
elsif (/^no-gmp$/)	{ $no_gmp=1; }
}
if (!$libname) {
if ($do_ssl) {
$libname="SSLEAY";
}
if ($do_crypto) {
$libname="LIBEAY";
}
}
if ($W32 + $W16 + $VMS + $OS2 == 0) {
$W32 = 1;
}
if ($W16) {
$no_fp_api=1;
}
if (!$do_ssl && !$do_crypto)
{
print STDERR "usage: $0 ( ssl | crypto ) [ 16 | 32 | NT | OS2 ]\n";
exit(1);
}
%ssl_list=&load_numbers($ssl_num);
$max_ssl = $max_num;
%crypto_list=&load_numbers($crypto_num);
$max_crypto = $max_num;
my $ssl="ssl/ssl.h";
$ssl.=" ssl/kssl.h";
my $crypto ="crypto/crypto.h";
$crypto.=" crypto/o_dir.h";
$crypto.=" crypto/des/des.h crypto/des/des_old.h" ;
$crypto.=" crypto/idea/idea.h" ;
$crypto.=" crypto/rc4/rc4.h" ;
$crypto.=" crypto/rc5/rc5.h" ;
$crypto.=" crypto/rc2/rc2.h" ;
$crypto.=" crypto/bf/blowfish.h" ;
$crypto.=" crypto/cast/cast.h" ;
$crypto.=" crypto/md2/md2.h" ;
$crypto.=" crypto/md4/md4.h" ;
$crypto.=" crypto/md5/md5.h" ;
$crypto.=" crypto/mdc2/mdc2.h" ;
$crypto.=" crypto/sha/sha.h" ;
$crypto.=" crypto/ripemd/ripemd.h" ;
$crypto.=" crypto/aes/aes.h" ;
$crypto.=" crypto/bn/bn.h";
$crypto.=" crypto/rsa/rsa.h" ;
$crypto.=" crypto/dsa/dsa.h" ;
$crypto.=" crypto/dh/dh.h" ;
$crypto.=" crypto/ec/ec.h" ;
$crypto.=" crypto/ecdsa/ecdsa.h" ;
$crypto.=" crypto/ecdh/ecdh.h" ;
$crypto.=" crypto/hmac/hmac.h" ;
$crypto.=" crypto/engine/engine.h";
$crypto.=" crypto/stack/stack.h" ;
$crypto.=" crypto/buffer/buffer.h" ;
$crypto.=" crypto/bio/bio.h" ;
$crypto.=" crypto/dso/dso.h" ;
$crypto.=" crypto/lhash/lhash.h" ;
$crypto.=" crypto/conf/conf.h";
$crypto.=" crypto/txt_db/txt_db.h";
$crypto.=" crypto/evp/evp.h" ;
$crypto.=" crypto/objects/objects.h";
$crypto.=" crypto/pem/pem.h";
$crypto.=" crypto/asn1/asn1.h";
$crypto.=" crypto/asn1/asn1t.h";
$crypto.=" crypto/asn1/asn1_mac.h";
$crypto.=" crypto/err/err.h" ;
$crypto.=" crypto/pkcs7/pkcs7.h";
$crypto.=" crypto/pkcs12/pkcs12.h";
$crypto.=" crypto/x509/x509.h";
$crypto.=" crypto/x509/x509_vfy.h";
$crypto.=" crypto/x509v3/x509v3.h";
$crypto.=" crypto/rand/rand.h";
$crypto.=" crypto/comp/comp.h" ;
$crypto.=" crypto/ocsp/ocsp.h";
$crypto.=" crypto/ui/ui.h crypto/ui/ui_compat.h";
$crypto.=" crypto/krb5/krb5_asn.h";
$crypto.=" crypto/tmdiff.h";
$crypto.=" crypto/store/store.h";
$crypto.=" crypto/pqueue/pqueue.h";
my $symhacks="crypto/symhacks.h";
my @ssl_symbols = &do_defs("SSLEAY", $ssl, $symhacks);
my @crypto_symbols = &do_defs("LIBEAY", $crypto, $symhacks);
if ($do_update) {
if ($do_ssl == 1) {
&maybe_add_info("SSLEAY",*ssl_list,@ssl_symbols);
if ($do_rewrite == 1) {
open(OUT, ">$ssl_num");
&rewrite_numbers(*OUT,"SSLEAY",*ssl_list,@ssl_symbols);
} else {
open(OUT, ">>$ssl_num");
}
&update_numbers(*OUT,"SSLEAY",*ssl_list,$max_ssl,@ssl_symbols);
close OUT;
}
if($do_crypto == 1) {
&maybe_add_info("LIBEAY",*crypto_list,@crypto_symbols);
if ($do_rewrite == 1) {
open(OUT, ">$crypto_num");
&rewrite_numbers(*OUT,"LIBEAY",*crypto_list,@crypto_symbols);
} else {
open(OUT, ">>$crypto_num");
}
&update_numbers(*OUT,"LIBEAY",*crypto_list,$max_crypto,@crypto_symbols);
close OUT;
}
} elsif ($do_checkexist) {
&check_existing(*ssl_list, @ssl_symbols)
if $do_ssl == 1;
&check_existing(*crypto_list, @crypto_symbols)
if $do_crypto == 1;
} elsif ($do_ctest || $do_ctestall) {
print <<"EOF";
/* Test file to check all DEF file symbols are present by trying
* to link to all of them. This is *not* intended to be run!
*/
int main()
{
EOF
&print_test_file(*STDOUT,"SSLEAY",*ssl_list,$do_ctestall,@ssl_symbols)
if $do_ssl == 1;
&print_test_file(*STDOUT,"LIBEAY",*crypto_list,$do_ctestall,@crypto_symbols)
if $do_crypto == 1;
print "}\n";
} else {
&print_def_file(*STDOUT,$libname,*ssl_list,@ssl_symbols)
if $do_ssl == 1;
&print_def_file(*STDOUT,$libname,*crypto_list,@crypto_symbols)
if $do_crypto == 1;
}
sub do_defs
{
my($name,$files,$symhacksfile)=@_;
my $file;
my @ret;
my %syms;
my %platform;
my %kind;
my %algorithm;
my %variant;
my %variant_cnt;
my $cpp;
my %unknown_algorithms = ();
foreach $file (split(/\s+/,$symhacksfile." ".$files))
{
print STDERR "DEBUG: starting on $file:\n" if $debug;
open(IN,"<$file") || die "unable to open $file:$!\n";
my $line = "", my $def= "";
my %tag = (
(map { $_ => 0 } @known_platforms),
(map { "OPENSSL_SYS_".$_ => 0 } @known_ossl_platforms),
(map { "OPENSSL_NO_".$_ => 0 } @known_algorithms),
NOPROTO		=> 0,
PERL5		=> 0,
_WINDLL		=> 0,
CONST_STRICT	=> 0,
TRUE		=> 1,
);
my $symhacking = $file eq $symhacksfile;
my @current_platforms = ();
my @current_algorithms = ();
my $make_variant = sub
{
my ($s, $a, $p, $k) = @_;
my ($a1, $a2);
print STDERR "DEBUG: make_variant: Entered with ",$s,", ",$a,", ",(defined($p)?$p:""),", ",(defined($k)?$k:""),"\n" if $debug;
if (defined($p))
{
$a1 = join(",",$p,
grep(!/^$/,
map { $tag{$_} == 1 ? $_ : "" }
@known_platforms));
}
else
{
$a1 = join(",",
grep(!/^$/,
map { $tag{$_} == 1 ? $_ : "" }
@known_platforms));
}
$a2 = join(",",
grep(!/^$/,
map { $tag{"OPENSSL_SYS_".$_} == 1 ? $_ : "" }
@known_ossl_platforms));
print STDERR "DEBUG: make_variant: a1 = $a1; a2 = $a2\n" if $debug;
if ($a1 eq "") { $a1 = $a2; }
elsif ($a1 ne "" && $a2 ne "") { $a1 .= ",".$a2; }
if ($a eq $s)
{
if (!defined($variant_cnt{$s}))
{
$variant_cnt{$s} = 0;
}
$variant_cnt{$s}++;
$a .= "{$variant_cnt{$s}}";
}
my $toadd = $a.":".$a1.(defined($k)?":".$k:"");
my $togrep = $s.'(\{[0-9]+\})?:'.$a1.(defined($k)?":".$k:"");
if (!grep(/^$togrep$/,
split(/;/, defined($variant{$s})?$variant{$s}:""))) {
if (defined($variant{$s})) { $variant{$s} .= ";"; }
$variant{$s} .= $toadd;
}
print STDERR "DEBUG: make_variant: Exit with variant of ",$s," = ",$variant{$s},"\n" if $debug;
};
print STDERR "DEBUG: parsing ----------\n" if $debug;
while(<IN>) {
if (/\/\* Error codes for the \w+ functions\. \*\//)
{
undef @tag;
last;
}
if ($line ne '') {
$_ = $line . $_;
$line = '';
}
if (/\\$/) {
chomp;
chop;
$line = $_;
next;
}
$cpp = 1 if /^\
if ($cpp) {
$cpp = 0 if /^\
next;
}
s/\/\*.*?\*\///gs;
if (/\/\*/) {
$line = $_;
next;
}
s/{[^{}]*}//gs;
print STDERR "DEBUG: \$def=\"$def\"\n" if $debug && $def ne "";
print STDERR "DEBUG: \$_=\"$_\"\n" if $debug;
if (/^\
push(@tag,"-");
push(@tag,$1);
$tag{$1}=-1;
print STDERR "DEBUG: $file: found tag $1 = -1\n" if $debug;
} elsif (/^\
push(@tag,"-");
if (/^\
my $tmp_1 = $1;
my $tmp_;
foreach $tmp_ (split '\&\&',$tmp_1) {
$tmp_ =~ /!defined\(([^\)]+)\)/;
print STDERR "DEBUG: $file: found tag $1 = -1\n" if $debug;
push(@tag,$1);
$tag{$1}=-1;
}
} else {
print STDERR "Warning: $file: complicated expression: $_" if $debug;
print STDERR "DEBUG: $file: found tag $1 = -1\n" if $debug;
push(@tag,$1);
$tag{$1}=-1;
}
} elsif (/^\
push(@tag,"-");
push(@tag,$1);
$tag{$1}=1;
print STDERR "DEBUG: $file: found tag $1 = 1\n" if $debug;
} elsif (/^\
push(@tag,"-");
if (/^\
my $tmp_1 = $1;
my $tmp_;
foreach $tmp_ (split '\|\|',$tmp_1) {
$tmp_ =~ /defined\(([^\)]+)\)/;
print STDERR "DEBUG: $file: found tag $1 = 1\n" if $debug;
push(@tag,$1);
$tag{$1}=1;
}
} else {
print STDERR "Warning: $file: complicated expression: $_\n" if $debug;
print STDERR "DEBUG: $file: found tag $1 = 1\n" if $debug;
push(@tag,$1);
$tag{$1}=1;
}
} elsif (/^\
my $tag_i = $
while($tag[$tag_i] ne "-") {
if ($tag[$tag_i] eq "OPENSSL_NO_".$1) {
$tag{$tag[$tag_i]}=2;
print STDERR "DEBUG: $file: chaged tag $1 = 2\n" if $debug;
}
$tag_i--;
}
} elsif (/^\
my $tag_i = $
while($tag_i > 0 && $tag[$tag_i] ne "-") {
my $t=$tag[$tag_i];
print STDERR "DEBUG: \$t=\"$t\"\n" if $debug;
if ($tag{$t}==2) {
$tag{$t}=-1;
} else {
$tag{$t}=0;
}
print STDERR "DEBUG: $file: changed tag ",$t," = ",$tag{$t},"\n" if $debug;
pop(@tag);
if ($t =~ /^OPENSSL_NO_([A-Z0-9_]+)$/) {
$t=$1;
} else {
$t="";
}
if ($t ne ""
&& !grep(/^$t$/, @known_algorithms)) {
$unknown_algorithms{$t} = 1;
}
$tag_i--;
}
pop(@tag);
} elsif (/^\
my $tag_i = $
while($tag[$tag_i] ne "-") {
my $t=$tag[$tag_i];
$tag{$t}= -$tag{$t};
print STDERR "DEBUG: $file: changed tag ",$t," = ",$tag{$t},"\n" if $debug;
$tag_i--;
}
} elsif (/^\
push(@tag,"-");
push(@tag,"TRUE");
$tag{"TRUE"}=1;
print STDERR "DEBUG: $file: found 1\n" if $debug;
} elsif (/^\
push(@tag,"-");
push(@tag,"TRUE");
$tag{"TRUE"}=-1;
print STDERR "DEBUG: $file: found 0\n" if $debug;
} elsif (/^\
&& $symhacking && $tag{'TRUE'} != -1) {
&$make_variant($1,$2);
print STDERR "DEBUG: $file: defined $1 = $2\n" if $debug;
}
if (/^\
@current_platforms =
grep(!/^$/,
map { $tag{$_} == 1 ? $_ :
$tag{$_} == -1 ? "!".$_  : "" }
@known_platforms);
push @current_platforms
, grep(!/^$/,
map { $tag{"OPENSSL_SYS_".$_} == 1 ? $_ :
$tag{"OPENSSL_SYS_".$_} == -1 ? "!".$_  : "" }
@known_ossl_platforms);
@current_algorithms =
grep(!/^$/,
map { $tag{"OPENSSL_NO_".$_} == -1 ? $_ : "" }
@known_algorithms);
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
next;
}
if ($tag{'TRUE'} != -1) {
if (/^\s*DECLARE_STACK_OF\s*\(\s*(\w*)\s*\)/) {
next;
} elsif (/^\s*DECLARE_ASN1_ENCODE_FUNCTIONS\s*\(\s*(\w*)\s*,\s*(\w*)\s*,\s*(\w*)\s*\)/) {
$def .= "int d2i_$3(void);";
$def .= "int i2d_$3(void);";
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $2_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$2_it","$2_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_FUNCTIONS_fname\s*\(\s*(\w*)\s*,\s*(\w*)\s*,\s*(\w*)\s*\)/) {
$def .= "int d2i_$3(void);";
$def .= "int i2d_$3(void);";
$def .= "int $3_free(void);";
$def .= "int $3_new(void);";
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $2_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$2_it","$2_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_FUNCTIONS\s*\(\s*(\w*)\s*\)/ ||
/^\s*DECLARE_ASN1_FUNCTIONS_const\s*\(\s*(\w*)\s*\)/) {
$def .= "int d2i_$1(void);";
$def .= "int i2d_$1(void);";
$def .= "int $1_free(void);";
$def .= "int $1_new(void);";
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $1_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$1_it","$1_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_ENCODE_FUNCTIONS_const\s*\(\s*(\w*)\s*,\s*(\w*)\s*\)/) {
$def .= "int d2i_$2(void);";
$def .= "int i2d_$2(void);";
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $2_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$2_it","$2_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_ALLOC_FUNCTIONS\s*\(\s*(\w*)\s*\)/) {
$def .= "int $1_free(void);";
$def .= "int $1_new(void);";
next;
} elsif (/^\s*DECLARE_ASN1_FUNCTIONS_name\s*\(\s*(\w*)\s*,\s*(\w*)\s*\)/) {
$def .= "int d2i_$2(void);";
$def .= "int i2d_$2(void);";
$def .= "int $2_free(void);";
$def .= "int $2_new(void);";
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $2_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$2_it","$2_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_ITEM\s*\(\s*(\w*)\s*\)/) {
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int $1_it;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("$1_it","$1_it",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
next;
} elsif (/^\s*DECLARE_ASN1_NDEF_FUNCTION\s*\(\s*(\w*)\s*\)/) {
$def .= "int i2d_$1_NDEF(void);";
} elsif (/^\s*DECLARE_ASN1_SET_OF\s*\(\s*(\w*)\s*\)/) {
next;
} elsif (/^\s*DECLARE_PKCS12_STACK_OF\s*\(\s*(\w*)\s*\)/) {
next;
} elsif (/^DECLARE_PEM_rw\s*\(\s*(\w*)\s*,/ ||
/^DECLARE_PEM_rw_cb\s*\(\s*(\w*)\s*,/ ||
/^DECLARE_PEM_rw_const\s*\(\s*(\w*)\s*,/ ) {
$def .=
"
.join(',',"!WIN16",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_read_$1(void);";
$def .= "int PEM_write_$1(void);";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_read_bio_$1(void);";
$def .= "int PEM_write_bio_$1(void);";
next;
} elsif (/^DECLARE_PEM_write\s*\(\s*(\w*)\s*,/ ||
/^DECLARE_PEM_write_cb\s*\(\s*(\w*)\s*,/ ) {
$def .=
"
.join(',',"!WIN16",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_write_$1(void);";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_write_bio_$1(void);";
next;
} elsif (/^DECLARE_PEM_read\s*\(\s*(\w*)\s*,/ ||
/^DECLARE_PEM_read_cb\s*\(\s*(\w*)\s*,/ ) {
$def .=
"
.join(',',"!WIN16",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_read_$1(void);";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "int PEM_read_bio_$1(void);";
next;
} elsif (/^OPENSSL_DECLARE_GLOBAL\s*\(\s*(\w*)\s*,\s*(\w*)\s*\)/) {
$def .=
"
.join(',',"!EXPORT_VAR_AS_FUNCTION",@current_platforms).":"
.join(',',@current_algorithms).";";
$def .= "OPENSSL_EXTERN int _shadow_$2;";
$def .=
"
.join(',',@current_platforms).":"
.join(',',@current_algorithms).";";
&$make_variant("_shadow_$2","_shadow_$2",
"EXPORT_VAR_AS_FUNCTION",
"FUNCTION");
} elsif ($tag{'CONST_STRICT'} != 1) {
if (/\{|\/\*|\([^\)]*$/) {
$line = $_;
} else {
$def .= $_;
}
}
}
}
close(IN);
my $algs;
my $plays;
print STDERR "DEBUG: postprocessing ----------\n" if $debug;
foreach (split /;/, $def) {
my $s; my $k = "FUNCTION"; my $p; my $a;
s/^[\n\s]*//g;
s/[\n\s]*$//g;
next if(/\
next if(/typedef\W/);
next if(/\
print STDERR "DEBUG: \$_ = \"$_\"\n" if $debug;
if (/^\
$plats = $1;
$algs = $2;
print STDERR "DEBUG: found info on platforms ($plats) and algorithms ($algs)\n" if $debug;
next;
} elsif (/^\s*OPENSSL_EXTERN\s.*?(\w+(\{[0-9]+\})?)(\[[0-9]*\])*\s*$/) {
$s = $1;
$k = "VARIABLE";
print STDERR "DEBUG: found external variable $s\n" if $debug;
} elsif (/\(\*(\w*(\{[0-9]+\})?)\([^\)]+/) {
$s = $1;
print STDERR "DEBUG: found ANSI C function $s\n" if $debug;
} elsif (/\w+\W+(\w+)\W*\(\s*\)(\s*__attribute__\(.*\)\s*)?$/s) {
print STDERR "DEBUG: found K&R C function $s\n" if $debug;
next;
} elsif (/\w+\W+\w+(\{[0-9]+\})?\W*\(.*\)(\s*__attribute__\(.*\)\s*)?$/s) {
while (not /\(\)(\s*__attribute__\(.*\)\s*)?$/s) {
s/[^\(\)]*\)(\s*__attribute__\(.*\)\s*)?$/\)/s;
s/\([^\(\)]*\)\)(\s*__attribute__\(.*\)\s*)?$/\)/s;
}
s/\(void\)//;
/(\w+(\{[0-9]+\})?)\W*\(\)/s;
$s = $1;
print STDERR "DEBUG: found function $s\n" if $debug;
} elsif (/TYPEDEF_\w+_OF/) {
next;
} elsif (/\(/ and not (/=/)) {
print STDERR "File $file: cannot parse: $_;\n";
next;
} else {
next;
}
$syms{$s} = 1;
$kind{$s} = $k;
$p = $plats;
$a = $algs;
$a .= ",BF" if($s =~ /EVP_bf/);
$a .= ",CAST" if($s =~ /EVP_cast/);
$a .= ",DES" if($s =~ /EVP_des/);
$a .= ",DSA" if($s =~ /EVP_dss/);
$a .= ",IDEA" if($s =~ /EVP_idea/);
$a .= ",MD2" if($s =~ /EVP_md2/);
$a .= ",MD4" if($s =~ /EVP_md4/);
$a .= ",MD5" if($s =~ /EVP_md5/);
$a .= ",RC2" if($s =~ /EVP_rc2/);
$a .= ",RC4" if($s =~ /EVP_rc4/);
$a .= ",RC5" if($s =~ /EVP_rc5/);
$a .= ",RIPEMD" if($s =~ /EVP_ripemd/);
$a .= ",SHA" if($s =~ /EVP_sha/);
$a .= ",RSA" if($s =~ /EVP_(Open|Seal)(Final|Init)/);
$a .= ",RSA" if($s =~ /PEM_Seal(Final|Init|Update)/);
$a .= ",RSA" if($s =~ /RSAPrivateKey/);
$a .= ",RSA" if($s =~ /SSLv23?_((client|server)_)?method/);
$platform{$s} =
&reduce_platforms((defined($platform{$s})?$platform{$s}.',':"").$p);
$algorithm{$s} .= ','.$a;
if (defined($variant{$s})) {
foreach $v (split /;/,$variant{$s}) {
(my $r, my $p, my $k) = split(/:/,$v);
my $ip = join ',',map({ /^!(.*)$/ ? $1 : "!".$_ } split /,/, $p);
$syms{$r} = 1;
if (!defined($k)) { $k = $kind{$s}; }
$kind{$r} = $k."(".$s.")";
$algorithm{$r} = $algorithm{$s};
$platform{$r} = &reduce_platforms($platform{$s}.",".$p.",".$p);
$platform{$s} = &reduce_platforms($platform{$s}.','.$ip.','.$ip);
print STDERR "DEBUG: \$variant{\"$s\"} = ",$v,"; \$r = $r; \$p = ",$platform{$r},"; \$a = ",$algorithm{$r},"; \$kind = ",$kind{$r},"\n" if $debug;
}
}
print STDERR "DEBUG: \$s = $s; \$p = ",$platform{$s},"; \$a = ",$algorithm{$s},"; \$kind = ",$kind{$s},"\n" if $debug;
}
}
delete $syms{"bn_dump1"};
$platform{"BIO_s_log"} .= ",!WIN32,!WIN16,!macintosh";
$platform{"PEM_read_NS_CERT_SEQ"} = "VMS";
$platform{"PEM_write_NS_CERT_SEQ"} = "VMS";
$platform{"PEM_read_P8_PRIV_KEY_INFO"} = "VMS";
$platform{"PEM_write_P8_PRIV_KEY_INFO"} = "VMS";
push @ret, map { $_."\\".&info_string($_,"EXIST",
$platform{$_},
$kind{$_},
$algorithm{$_}) } keys %syms;
if (keys %unknown_algorithms) {
print STDERR "WARNING: mkdef.pl doesn't know the following algorithms:\n";
print STDERR "\t",join("\n\t",keys %unknown_algorithms),"\n";
}
return(@ret);
}
sub reduce_platforms
{
my ($platforms) = @_;
my $pl = defined($platforms) ? $platforms : "";
my %p = map { $_ => 0 } split /,/, $pl;
my $ret;
print STDERR "DEBUG: Entered reduce_platforms with \"$platforms\"\n"
if $debug;
foreach $platform (split /,/, $pl) {
if ($platform =~ /^!(.*)$/) {
$p{$1}--;
} else {
$p{$platform}++;
}
}
foreach $platform (keys %p) {
if ($p{$platform} == 0) { delete $p{$platform}; }
}
delete $p{""};
$ret = join(',',sort(map { $p{$_} < 0 ? "!".$_ : $_ } keys %p));
print STDERR "DEBUG: Exiting reduce_platforms with \"$ret\"\n"
if $debug;
return $ret;
}
sub info_string {
(my $symbol, my $exist, my $platforms, my $kind, my $algorithms) = @_;
my %a = defined($algorithms) ?
map { $_ => 1 } split /,/, $algorithms : ();
my $k = defined($kind) ? $kind : "FUNCTION";
my $ret;
my $p = &reduce_platforms($platforms);
delete $a{""};
$ret = $exist;
$ret .= ":".$p;
$ret .= ":".$k;
$ret .= ":".join(',',sort keys %a);
return $ret;
}
sub maybe_add_info {
(my $name, *nums, my @symbols) = @_;
my $sym;
my $new_info = 0;
my %syms=();
print STDERR "Updating $name info\n";
foreach $sym (@symbols) {
(my $s, my $i) = split /\\/, $sym;
if (defined($nums{$s})) {
$i =~ s/^(.*?:.*?:\w+)(\(\w+\))?/$1/;
(my $n, my $dummy) = split /\\/, $nums{$s};
if (!defined($dummy) || $i ne $dummy) {
$nums{$s} = $n."\\".$i;
$new_info++;
print STDERR "DEBUG: maybe_add_info for $s: \"$dummy\" => \"$i\"\n" if $debug;
}
}
$syms{$s} = 1;
}
my @s=sort { &parse_number($nums{$a},"n") <=> &parse_number($nums{$b},"n") } keys %nums;
foreach $sym (@s) {
(my $n, my $i) = split /\\/, $nums{$sym};
if (!defined($syms{$sym}) && $i !~ /^NOEXIST:/) {
$new_info++;
print STDERR "DEBUG: maybe_add_info for $sym: -> undefined\n" if $debug;
}
}
if ($new_info) {
print STDERR "$new_info old symbols got an info update\n";
if (!$do_rewrite) {
print STDERR "You should do a rewrite to fix this.\n";
}
} else {
print STDERR "No old symbols needed info update\n";
}
}
sub is_valid
{
my ($keywords_txt,$platforms) = @_;
my (@keywords) = split /,/,$keywords_txt;
my ($falsesum, $truesum) = (0, 1);
sub recognise
{
my ($keyword,$platforms) = @_;
if ($platforms) {
if ($keyword eq "VMS" && $VMS) { return 1; }
if ($keyword eq "WIN32" && $W32) { return 1; }
if ($keyword eq "WIN16" && $W16) { return 1; }
if ($keyword eq "WINNT" && $NT) { return 1; }
if ($keyword eq "OS2" && $OS2) { return 1; }
if ($keyword eq "EXPORT_VAR_AS_FUNCTION" && ($VMSVAX || $W32 || $W16)) {
return 1;
}
return 0;
} else {
if ($keyword eq "RC2" && $no_rc2) { return 0; }
if ($keyword eq "RC4" && $no_rc4) { return 0; }
if ($keyword eq "RC5" && $no_rc5) { return 0; }
if ($keyword eq "IDEA" && $no_idea) { return 0; }
if ($keyword eq "DES" && $no_des) { return 0; }
if ($keyword eq "BF" && $no_bf) { return 0; }
if ($keyword eq "CAST" && $no_cast) { return 0; }
if ($keyword eq "MD2" && $no_md2) { return 0; }
if ($keyword eq "MD4" && $no_md4) { return 0; }
if ($keyword eq "MD5" && $no_md5) { return 0; }
if ($keyword eq "SHA" && $no_sha) { return 0; }
if ($keyword eq "RIPEMD" && $no_ripemd) { return 0; }
if ($keyword eq "MDC2" && $no_mdc2) { return 0; }
if ($keyword eq "RSA" && $no_rsa) { return 0; }
if ($keyword eq "DSA" && $no_dsa) { return 0; }
if ($keyword eq "DH" && $no_dh) { return 0; }
if ($keyword eq "EC" && $no_ec) { return 0; }
if ($keyword eq "ECDSA" && $no_ecdsa) { return 0; }
if ($keyword eq "ECDH" && $no_ecdh) { return 0; }
if ($keyword eq "HMAC" && $no_hmac) { return 0; }
if ($keyword eq "AES" && $no_aes) { return 0; }
if ($keyword eq "EVP" && $no_evp) { return 0; }
if ($keyword eq "LHASH" && $no_lhash) { return 0; }
if ($keyword eq "STACK" && $no_stack) { return 0; }
if ($keyword eq "ERR" && $no_err) { return 0; }
if ($keyword eq "BUFFER" && $no_buffer) { return 0; }
if ($keyword eq "BIO" && $no_bio) { return 0; }
if ($keyword eq "COMP" && $no_comp) { return 0; }
if ($keyword eq "DSO" && $no_dso) { return 0; }
if ($keyword eq "KRB5" && $no_krb5) { return 0; }
if ($keyword eq "ENGINE" && $no_engine) { return 0; }
if ($keyword eq "HW" && $no_hw) { return 0; }
if ($keyword eq "FP_API" && $no_fp_api) { return 0; }
if ($keyword eq "STATIC_ENGINE" && $no_static_engine) { return 0; }
if ($keyword eq "GMP" && $no_gmp) { return 0; }
if ($keyword eq "DEPRECATED" && $no_deprecated) { return 0; }
return 1;
}
}
foreach $k (@keywords) {
if ($k =~ /^!(.*)$/) {
$falsesum += &recognise($1,$platforms);
} else {
$truesum *= &recognise($k,$platforms);
}
}
print STDERR "DEBUG: [",$
return (!$falsesum) && $truesum;
}
sub print_test_file
{
(*OUT,my $name,*nums,my $testall,my @symbols)=@_;
my $n = 1; my @e; my @r;
my $sym; my $prev = ""; my $prefSSLeay;
(@e)=grep(/^SSLeay(\{[0-9]+\})?\\.*?:.*?:.*/,@symbols);
(@r)=grep(/^\w+(\{[0-9]+\})?\\.*?:.*?:.*/ && !/^SSLeay(\{[0-9]+\})?\\.*?:.*?:.*/,@symbols);
@symbols=((sort @e),(sort @r));
foreach $sym (@symbols) {
(my $s, my $i) = $sym =~ /^(.*?)\\(.*)$/;
my $v = 0;
$v = 1 if $i=~ /^.*?:.*?:VARIABLE/;
my $p = ($i =~ /^[^:]*:([^:]*):/,$1);
my $a = ($i =~ /^[^:]*:[^:]*:[^:]*:([^:]*)/,$1);
if (!defined($nums{$s})) {
print STDERR "Warning: $s does not have a number assigned\n"
if(!$do_update);
} elsif (is_valid($p,1) && is_valid($a,0)) {
my $s2 = ($s =~ /^(.*?)(\{[0-9]+\})?$/, $1);
if ($prev eq $s2) {
print OUT "\t/* The following has already appeared previously */\n";
print STDERR "Warning: Symbol '",$s2,"' redefined. old=",($nums{$prev} =~ /^(.*?)\\/,$1),", new=",($nums{$s2} =~ /^(.*?)\\/,$1),"\n";
}
$prev = $s2;
($nn,$ni)=($nums{$s2} =~ /^(.*?)\\(.*)$/);
if ($v) {
print OUT "\textern int $s2; /* type unknown */ /* $nn $ni */\n";
} else {
print OUT "\textern int $s2(); /* type unknown */ /* $nn $ni */\n";
}
}
}
}
sub get_version {
local *MF;
my $v = '?';
open MF, 'Makefile' or return $v;
while (<MF>) {
$v = $1, last if /^VERSION=(.*?)\s*$/;
}
close MF;
return $v;
}
sub print_def_file
{
(*OUT,my $name,*nums,my @symbols)=@_;
my $n = 1; my @e; my @r; my @v; my $prev="";
my $liboptions="";
my $libname = $name;
my $http_vendor = 'www.openssl.org/';
my $version = get_version();
my $what = "OpenSSL: implementation of Secure Socket Layer";
my $description = "$what $version, $name - http://$http_vendor";
if ($W32)
{ $libname.="32"; }
elsif ($W16)
{ $libname.="16"; }
elsif ($OS2)
{
my %translate = (ssl => 'open_ssl', crypto => 'cryptssl');
$libname = $translate{$name} || $name;
$liboptions = <<EOO;
INITINSTANCE
DATA MULTIPLE NONSHARED
EOO
$description = "\@
}
print OUT <<"EOF";
;
; Definition file for the DLL version of the $name library from OpenSSL
;
LIBRARY         $libname	$liboptions
DESCRIPTION     '$description'
EOF
if ($W16) {
print <<"EOF";
CODE            PRELOAD MOVEABLE
DATA            PRELOAD MOVEABLE SINGLE
EXETYPE		WINDOWS
HEAPSIZE	4096
STACKSIZE	8192
EOF
}
print "EXPORTS\n";
(@e)=grep(/^SSLeay(\{[0-9]+\})?\\.*?:.*?:FUNCTION/,@symbols);
(@r)=grep(/^\w+(\{[0-9]+\})?\\.*?:.*?:FUNCTION/ && !/^SSLeay(\{[0-9]+\})?\\.*?:.*?:FUNCTION/,@symbols);
(@v)=grep(/^\w+(\{[0-9]+\})?\\.*?:.*?:VARIABLE/,@symbols);
@symbols=((sort @e),(sort @r), (sort @v));
foreach $sym (@symbols) {
(my $s, my $i) = $sym =~ /^(.*?)\\(.*)$/;
my $v = 0;
$v = 1 if $i =~ /^.*?:.*?:VARIABLE/;
if (!defined($nums{$s})) {
printf STDERR "Warning: $s does not have a number assigned\n"
if(!$do_update);
} else {
(my $n, my $dummy) = split /\\/, $nums{$s};
my %pf = ();
my $p = ($i =~ /^[^:]*:([^:]*):/,$1);
my $a = ($i =~ /^[^:]*:[^:]*:[^:]*:([^:]*)/,$1);
if (is_valid($p,1) && is_valid($a,0)) {
my $s2 = ($s =~ /^(.*?)(\{[0-9]+\})?$/, $1);
if ($prev eq $s2) {
print STDERR "Warning: Symbol '",$s2,"' redefined. old=",($nums{$prev} =~ /^(.*?)\\/,$1),", new=",($nums{$s2} =~ /^(.*?)\\/,$1),"\n";
}
$prev = $s2;
if($v && !$OS2) {
printf OUT "    %s%-39s @%-8d DATA\n",($W32)?"":"_",$s2,$n;
} else {
printf OUT "    %s%-39s @%d\n",($W32||$OS2)?"":"_",$s2,$n;
}
}
}
}
printf OUT "\n";
}
sub load_numbers
{
my($name)=@_;
my(@a,%ret);
$max_num = 0;
$num_noinfo = 0;
$prev = "";
$prev_cnt = 0;
open(IN,"<$name") || die "unable to open $name:$!\n";
while (<IN>) {
chop;
s/
next if /^\s*$/;
@a=split;
if (defined $ret{$a[0]}) {
}
if ($max_num > $a[1]) {
print STDERR "Warning: Number decreased from ",$max_num," to ",$a[1],"\n";
}
elsif ($max_num == $a[1]) {
if ($a[0] eq $prev) {
$prev_cnt++;
$a[0] .= "{$prev_cnt}";
}
}
else {
$prev_cnt = 0;
}
if ($
$ret{$a[0]}=$a[1];
$num_noinfo++;
} else {
$ret{$a[0]}=$a[1]."\\".$a[2];
}
$max_num = $a[1] if $a[1] > $max_num;
$prev=$a[0];
}
if ($num_noinfo) {
print STDERR "Warning: $num_noinfo symbols were without info.";
if ($do_rewrite) {
printf STDERR "  The rewrite will fix this.\n";
} else {
printf STDERR "  You should do a rewrite to fix this.\n";
}
}
close(IN);
return(%ret);
}
sub parse_number
{
(my $str, my $what) = @_;
(my $n, my $i) = split(/\\/,$str);
if ($what eq "n") {
return $n;
} else {
return $i;
}
}
sub rewrite_numbers
{
(*OUT,$name,*nums,@symbols)=@_;
my $thing;
print STDERR "Rewriting $name\n";
my @r = grep(/^\w+(\{[0-9]+\})?\\.*?:.*?:\w+\(\w+\)/,@symbols);
my $r; my %r; my %rsyms;
foreach $r (@r) {
(my $s, my $i) = split /\\/, $r;
my $a = $1 if $i =~ /^.*?:.*?:\w+\((\w+)\)/;
$i =~ s/^(.*?:.*?:\w+)\(\w+\)/$1/;
$r{$a} = $s."\\".$i;
$rsyms{$s} = 1;
}
my %syms = ();
foreach $_ (@symbols) {
(my $n, my $i) = split /\\/;
$syms{$n} = 1;
}
my @s=sort {
&parse_number($nums{$a},"n") <=> &parse_number($nums{$b},"n")
|| $a cmp $b
} keys %nums;
foreach $sym (@s) {
(my $n, my $i) = split /\\/, $nums{$sym};
next if defined($i) && $i =~ /^.*?:.*?:\w+\(\w+\)/;
next if defined($rsyms{$sym});
print STDERR "DEBUG: rewrite_numbers for sym = ",$sym,": i = ",$i,", n = ",$n,", rsym{sym} = ",$rsyms{$sym},"syms{sym} = ",$syms{$sym},"\n" if $debug;
$i="NOEXIST::FUNCTION:"
if !defined($i) || $i eq "" || !defined($syms{$sym});
my $s2 = $sym;
$s2 =~ s/\{[0-9]+\}$//;
printf OUT "%s%-39s %d\t%s\n","",$s2,$n,$i;
if (exists $r{$sym}) {
(my $s, $i) = split /\\/,$r{$sym};
my $s2 = $s;
$s2 =~ s/\{[0-9]+\}$//;
printf OUT "%s%-39s %d\t%s\n","",$s2,$n,$i;
}
}
}
sub update_numbers
{
(*OUT,$name,*nums,my $start_num, my @symbols)=@_;
my $new_syms = 0;
print STDERR "Updating $name numbers\n";
my @r = grep(/^\w+(\{[0-9]+\})?\\.*?:.*?:\w+\(\w+\)/,@symbols);
my $r; my %r; my %rsyms;
foreach $r (@r) {
(my $s, my $i) = split /\\/, $r;
my $a = $1 if $i =~ /^.*?:.*?:\w+\((\w+)\)/;
$i =~ s/^(.*?:.*?:\w+)\(\w+\)/$1/;
$r{$a} = $s."\\".$i;
$rsyms{$s} = 1;
}
foreach $sym (@symbols) {
(my $s, my $i) = $sym =~ /^(.*?)\\(.*)$/;
next if $i =~ /^.*?:.*?:\w+\(\w+\)/;
next if defined($rsyms{$sym});
die "ERROR: Symbol $sym had no info attached to it."
if $i eq "";
if (!exists $nums{$s}) {
$new_syms++;
my $s2 = $s;
$s2 =~ s/\{[0-9]+\}$//;
printf OUT "%s%-39s %d\t%s\n","",$s2, ++$start_num,$i;
if (exists $r{$s}) {
($s, $i) = split /\\/,$r{$s};
$s =~ s/\{[0-9]+\}$//;
printf OUT "%s%-39s %d\t%s\n","",$s, $start_num,$i;
}
}
}
if($new_syms) {
print STDERR "$new_syms New symbols added\n";
} else {
print STDERR "No New symbols Added\n";
}
}
sub check_existing
{
(*nums, my @symbols)=@_;
my %existing; my @remaining;
@remaining=();
foreach $sym (@symbols) {
(my $s, my $i) = $sym =~ /^(.*?)\\(.*)$/;
$existing{$s}=1;
}
foreach $sym (keys %nums) {
if (!exists $existing{$sym}) {
push @remaining, $sym;
}
}
if(@remaining) {
print STDERR "The following symbols do not seem to exist:\n";
foreach $sym (@remaining) {
print STDERR "\t",$sym,"\n";
}
}
}
