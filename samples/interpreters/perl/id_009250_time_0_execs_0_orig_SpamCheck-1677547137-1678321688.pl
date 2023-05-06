$spamcheckplver = 'YaBB 3.0 Beta $Revision: 100 $';
if ($action eq 'detailedversion') { return 1; }
sub spamcheck {
my ($rawcontent) = $_[0];
$rawcontent =~ s/[\r\n\t]/ /g;
$rawcontent =~ s/\[(.*?){1,2}\]//g;
$rawcontent =~ s/\<(.*?){1,2}\>//g;
my $testcontent = lc(" $rawcontent");
my ($spamline,$spamcnt,$searchtype);
if (&checkfor_DBorFILE("$vardir/spamrules.txt")) {
foreach my $buffer (&read_DBorFILE(0,'',$vardir,'spamrules','txt')) {
chomp $buffer;
$spamline = "";
if ($buffer =~ m/\~\;/) {
($spamcnt,$spamline) = split(/\~\;/, $buffer);
$searchtype = "S";
} elsif ($buffer =~ m/\=\;/) {
($spamcnt,$spamline) = split(/\=\;/, $buffer);
$searchtype = "E";
} else {
if ($buffer ne ""){
$spamline = $buffer;
$spamcnt = 0;
$searchtype = "S";
}
}
if(!$spamcnt){ $spamcnt = 0;}
if($spamline ne ""){ push(@spamlines, [$spamline, $spamcnt, $searchtype]); }
}
}
for $spamrule (@spamlines) {
chomp $spamrule;
$is_spam = 0;
($spamword,$spamlimit,$spamtype) = @{$spamrule};
if ($spamtype eq "S" ) {
@spamcount = $testcontent =~ /$spamword/gsi;
} elsif ($spamtype eq "E" ) {
@spamcount = $testcontent =~ /\b$spamword\b/gsi;
}
$spamcounter = $
if ($spamcounter > $spamlimit){
$is_spam = 1;
last;
}
}
return $is_spam;
return $spamword;
}
1;
