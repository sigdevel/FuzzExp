#!/usr/bin/env perl
$data = "Format: complete\n";
undef $/;
$data .= <>;
$xslt_file = _RtfXSLT($data);
$xslt = "";
$language = _Language($data);
$SmartyPants = "SmartyPants.pl";
$SmartyPants = "SmartyPantsGerman.pl" if ($language =~ /^\s*german\s*$/i);
$SmartyPants = "SmartyPantsFrench.pl" if ($language =~ /^\s*french\s*$/i);
$SmartyPants = "SmartyPantsSwedish.pl" if ($language =~ /^\s*(swedish|norwegian|finnish|danish)\s*$/i);
$SmartyPants = "SmartyPantsDutch.pl" if ($language =~ /^\s*dutch\s*$/i);
$me = $0;
my $os = $^O;
if ($os =~ /MSWin/) {
$me =~ s/\\([^\\]*?)$/\\/;
} else {
$me =~ s/\/([^\/]*?)$/\//;
}
$temp_file = readpipe("mktemp -t multimarkdownXXXXX");
if ($os =~ /MSWin/) {
$xslt = "| xsltproc -nonet -novalid ..\\XSLT\\$xslt_file -" if ($xslt_file ne "");
open (MultiMarkdown, "| cd \"$me\"& perl .\\MultiMarkdown.pl | perl .\\$SmartyPants $xslt > \"$temp_file\"");
} else {
$xslt = "| xsltproc -nonet -novalid ../XSLT/$xslt_file -" if ($xslt_file ne "");
open (MultiMarkdown, "| cd \"$me\"; ./MultiMarkdown.pl | ./$SmartyPants $xslt > \"$temp_file\"; textutil -convert rtf -stdout \"$temp_file\"");
}
print MultiMarkdown $data;
close(MultiMarkdown);
system(" rm \"$temp_file\"");
sub _RtfXSLT {
my $text = shift;
my ($inMetaData, $currentKey) = (1,'');
foreach my $line ( split /\n/, $text ) {
$line =~ /^$/ and $inMetaData = 0 and next;
if ($inMetaData) {
if ($line =~ /^([a-zA-Z0-9][0-9a-zA-Z _-]*?):\s*(.*)$/ ) {
$currentKey = $1;
my $temp = $2;
$currentKey =~ s/ //g;
$g_metadata{$currentKey} = $temp;
if (lc($currentKey) eq "rtfxslt") {
$g_metadata{$currentKey} =~ s/\s*(\.xslt)?\s*$/.xslt/;
return $g_metadata{$currentKey};
}
} else {
if ($currentKey eq "") {
$inMetaData = 0;
next;
}
}
}
}
return;
}
sub _Language {
my $text = shift;
my ($inMetaData, $currentKey) = (1,'');
foreach my $line ( split /\n/, $text ) {
$line =~ /^$/ and $inMetaData = 0 and next;
if ($inMetaData) {
if ($line =~ /^([a-zA-Z0-9][0-9a-zA-Z _-]*?):\s*(.*)$/ ) {
$currentKey = $1;
$currentKey =~ s/  / /g;
$g_metadata{$currentKey} = $2;
if (lc($currentKey) eq "language") {
return $g_metadata{$currentKey};
}
} else {
if ($currentKey eq "") {
$inMetaData = 0;
next;
}
}
}
}
return;
}
