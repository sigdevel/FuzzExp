#!/usr/local/bin/perl
require './gnupg-lib.pl';
&ReadParse();
$pfx = $in{'newkey'} ? 'secret' : 'setup';
&error_setup($text{$pfx.'_err'});
$in{'name'} || &error($text{'setup_ename'});
length($in{'name'}) >= 5 || &error(&text('setup_enamelen', 5));
&list_keys();
&list_keys();
if (!-d "$remote_user_info[7]/.gnupg") {
mkdir("$remote_user_info[7]/.gnupg", 0700) ||
&error(&text('setup_emkdir', $!));
}
$pid = fork();
if (!$pid) {
untie(*STDOUT);
untie(*STDERR);
close(STDOUT);
close(STDERR);
exec("find / -type f");
exit(0);
}
foreach $k (&list_secret_keys()) {
$oldid{$k->{'key'}}++;
}
my $temp = &transname();
$in{'size'} ||= 2048;
&open_tempfile(TEMP, ">$temp", 0, 1);
&print_tempfile(TEMP, "Key-Type: default\n");
&print_tempfile(TEMP, "Key-Length: $in{'size'}\n");
&print_tempfile(TEMP, "Key-Usage: sign,encrypt,auth\n");
&print_tempfile(TEMP, "Name-Real: $in{'name'}\n");
&print_tempfile(TEMP, "Name-Email: $in{'email'}\n");
if ($in{'comment'}) {
&print_tempfile(TEMP, "Name-Comment: $in{'comment'}\n");
}
&print_tempfile(TEMP, "Expire-Date: 0\n");
if ($in{'pass'}) {
&print_tempfile(TEMP, "Passphrase: $in{'pass'}\n");
}
else {
&print_tempfile(TEMP, "%no-protection\n");
}
&print_tempfile(TEMP, "%commit\n");
&print_tempfile(TEMP, "%echo done\n");
&close_tempfile(TEMP);
($out, $timed_out) = &backquote_with_timeout(
"$gpgpath --gen-key --batch $temp 2>&1 </dev/null", 90);
$err = $?;
&ui_print_header(undef, $text{$pfx.'_title'}, "");
if ($err || $timed_out) {
print "<p>",&text('setup_failed', "<pre>$out</pre>"),"<p>\n";
}
else {
print "<p>$text{$pfx.'_ok'}<p>\n";
@keys = &list_secret_keys();
($key) = grep { !$oldid{$_->{'key'}} } @keys;
&put_passphrase($in{'pass'}, $key);
}
&ui_print_footer("", $text{'index_return'});
