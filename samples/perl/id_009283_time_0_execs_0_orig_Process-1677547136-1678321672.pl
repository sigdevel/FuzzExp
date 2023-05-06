$SIG{'ALRM'} = 'TimerAlarm';
sub process {
($who, $msgType, $message) = @_;
my ($result, $caughtBy);
$origMessage = $message;
return 'SELF' if (lc($who) eq lc($param{'nick'}));
$message =~ s/[\cA-\c_]//ig;
$msgFilter = "NOFILTER";
$msgFilter = ($1 || $2) if $message =~ s!\s+(?:=~)?\s?/(?:\((?:\?:)?([^)]*)\)|([^()]*))/i?\s*$!!;
$addressed = 0;
$karma = 0;
return 'ANTIHELP' if $instance =~ /antihelp/;
my ($n, $uh) = ($nuh =~ /^([^!]+)!(.*)/);
if ($param{'VERBOSITY'} > 3) {
&status("Splitting incoming address into $n and $uh");
}
if ($msgType =~ /private/ and $message =~ /^hey, what is/) {
$infobots{$nuh} = $who;
&msg($who, "inter-infobot communication now requires version 0.43 or higher.");
return 'INTERBOT';
}
return 'INTERBOT' if $message =~ /^...but/;
return 'INTERBOT' if $message =~ /^.* already had it that way/;
return 'INTERBOT' if $message =~ /^told /;
return 'INTERBOT' if $message =~ /^told /;
return 'INTERBOT' if ($message =~ /^[!\*]/);
return 'INTERBOT' if ($message =~ /^gotcha/i);
if (&get(ignore => $uh) or &get(ignore => $who)) {
&status("IGNORE <$who> $message");
return 'IGNORE';
}
foreach (&getDBMKeys('ignore')) {
my $ignoreRE = $_;
my @parts = split /\*/, "a${ignoreRE}a";
my $recast = join '\S*', map quotemeta($_), @parts;
$recast =~ s/^a(.*)a$/$1/;
if ($nuh =~ /^$recast$/) {
&status("IGNORE <$who> $message");
return 'IGNORE';
}
}
if ($msgType =~ /private/ and $message =~ s/^:INFOBOT://) {
&status("infobot <$nuh> identified") unless $infobots{$nuh};
$infobots{$nuh} = $who;
}
if ($infobots{$nuh}) {
if ($msgType =~ /private/) {
if ($message =~ /^QUERY (<.*?>) (.*)/) {
my $r;
my $target = $1;
my $item = $2;
$item =~ s/[.\?]$//;
&status(":INFOBOT:QUERY $who: $message");
if ($r = &get("is", $item)) {
&msg($who, ":INFOBOT:REPLY $target $item =is=> $r");
}
if ($r = &get("are", $item)) {
&msg($who, ":INFOBOT:REPLY $target $item =are=> $r");
}
} elsif ($message =~ /^REPLY <(.*?)> (.*)/) {
my $r;
my $target = $1;
my $item = $2;
&status(":INFOBOT:REPLY $who: $message");
my ($X, $V, $Y) = $item =~ /^(.*?) =(.*?)=> (.*)/;
if ((getparam('acceptUrl') !~ /REQUIRE/) or ($Y =~ /(http|ftp|mailto|telnet|file):/)) {
&set($V, $X, $Y);
&msg($target, "$who knew: $X $V $Y");
}
}
}
return 'INFOBOT';
}
$VerifWho = &verifyUser($nuh);
if ($VerifWho) {
if (IsFlag("i") eq "i") {
&status("Ignoring $who: $VerifWho");
return 'IGNORED';
}
if ($msgType =~ /private/) {
my ($potentialPass) = $message =~ /^\s*(\S+)/;
if (exists($verified{$VerifWho})) {
if (time() - $verified{$VerifWho} < 60*60) {
$verified{$VerifWho} = $now;
} else {
&status("verification for $VerifWho expired");
delete $verified{$VerifWho};
}
}
if ($uPasswd eq "NONE_NEEDED") {
&status("no password needed for $VerifWho");
$verified{$VerifWho} = $now;
}
if (&ckpasswd($potentialPass, $uPasswd)) {
$message =~ s/^\s*\S+\s*//;
$origMessage =~ s/^\s*\S+\s*/<PASSWORD> /;
&status("password verified for $VerifWho");
$verified{$VerifWho} = $now;
if ($message =~ /^\s*$/) {
&msg($who, "i recognize you there");
return 'PASSWD';
}
}
}
}
return 'NOREPLY' if &userProcessing() eq 'NOREPLY';
if ($msgType !~ /public/) { $addressed = 1; }
if (($message =~ s/^(no,?\s+$param{'nick'},?\s*)//i)
or ($addressed and $message =~ s/^(no,?\s+)//i)) {
$correction_plausible = 1;
&status("correction is plausible, initial negative and nick deleted ($1)") if ($param{VERBOSITY} > 2);
} else {
$correction_plausible = 0;
}
if ($message =~ /^\s*$param{'nick'}\s*\?*$/i) {
&status("feedback addressing from $who");
$addressed = 1;
$blocked = 0;
if ($msgType =~ /public/) {
if (rand() > 0.5) {
&performSay("yes, $who?");
} else {
&performSay("$who?");
}
} else {
&msg($who, "yes?");
}
$lastaddressedby = $who;
$lastaddressedtime = time();
return "FEEDBACK";
}
if (($message =~ /^\s*$param{'nick'}\s*([\,\:\> ]+) */i)
or ($message =~ /^\s*$param{'nick'}\s*-+ *\??/i)) {
my($it) = $&;
if ($' !~ /^\s*is/i) {
$message = $';
$addressed = 1;
$blocked = 0;
}
}
if ($message =~ /, ?$param{nick}(\W+)?$/i) {
my($it) = $&;
if ($` !~ /^\s*i?s\s*$/i) {
$xxx = quotemeta($it);
$message =~ s/$xxx//;
$addressed = 1;
$blocked = 0;
}
}
if ($addressed) {
&status("$who is addressing me");
$lastaddressedby = $who;
$lastaddressedtime = time();
if ($message =~ /^showmode/i ) {
if ($msgType =~ /public/) {
if ((getparam('addressing') ne 'REQUIRE') or $addressed) {
&performSay ($who.", addressing is currently ".getparam('addressing'));
}
} else {
&msg($who, "addressing is currently ".getparam('addressing'));
}
return "SHOWMODE";
}
my $channel = &channel();
$continuity = 0;
} else {
my ($now, $diff);
if (getparam('continuity') and $who eq $lastaddressedby) {
$now = time();
$diff = $now - $lastaddressedtime;
if ($diff < getparam('continuity')) {
&status("assuming continuity of address by $who ($diff seconds elapsed)");
$continuity = 1;
}
} else {
$continuity = 0;
}
}
$skipReply = 0;
$message_input_length = length($message);
return if ($who eq $param{'nick'});
$message =~ s/^\s+//;
if (($message =~ s/^\S+\s*:\s+//) or ($message =~ s/^\S+\s+--+\s+//)) {
$reallyTalkingTo = $1;
} else {
$reallyTalkingTo = '';
if ($addressed) {
$reallyTalkingTo = $param{'nick'};
}
}
$message =~ s/^\s*hey,*\s+where/where/i;
$message =~ s/whois/who is/ig;
$message =~ s/where can i find/where is/i;
$message =~ s/how about/where is/i;
$message =~ s/^(gee|boy|golly|gosh),? //i;
$message =~ s/^(well|and|but|or|yes),? //i;
$message =~ s/^(does )?(any|ne)(1|one|body) know //i;
$message =~ s/ da / the /ig;
$message =~ s/^heya*,*( folks)?,*\.* *//i;
$message =~ s/^[uh]+m*[,\.]* +//i;
$message =~ s/^o+[hk]+(a+y+)?,*\.* +//i;
$message =~ s/^g(eez|osh|olly)+,*\.* +(.+)/$2/i;
$message =~ s/^w(ow|hee|o+ho+)+,*\.* +(.+)/$2/i;
$message =~ s/^still,* +//i;
$message =~ s/^well,* +//i;
$message =~ s/^\s*(stupid )?q(uestion)?:\s+//i;
my $holdMessage = $message;
($tell_obj, $target) = (undef,undef,undef);
if (getparam('allowTelling')) {
if ($message =~ /^tell\s+(\S+)\s+about\s+(.*)/i) {
($target, $tell_obj) = ($1, $2);
} elsif ($message =~ /tell\s+(\S+)\s+where\s+(\S+)\s+can\s+(\S+)\s+(.*)/i) {
($target, $tell_obj) = ($1, $4);
} elsif ($message =~ /tell\s+(\S+)\s+(what|where)\s+(.*?)\s+(is|are)[.?!]*$/i) {
($target, $qWord, $tell_obj, $verb) = ($1, $2, $3, $4);
$tell_obj = "$qWord $verb $tell_obj";
}
if (($target =~/^\s*[\&\
$result = "No, ".$who.", i won\'t";
$target = $who;
$caughtBy = "tell";
}
if ($target eq $param{'nick'}) {
$result = "Isn\'t that a bit silly, ".$who."?";
$target = $who;
$caughtBy = "tell";
}
$tell_obj =~ s/[\.\?!]+$// if defined $tell_obj;
}
if (not defined $result) {
$target   = $who     unless defined $target;
$target   = $who     if     $target eq 'me';
$target   = undef    if     $target eq 'us';
$message  = $tell_obj if $tell_obj;
if ($continuity or $addressed or
(getparam('addressing') ne "REQUIRE")) {
if (defined ($result = &myRoutines())) {
$caughtBy = "myRoutines";
} elsif (defined($result = &Extras())) {
$caughtBy = "Extras";
} elsif (defined($result = &doQuestion($msgType, $message, $msgFilter))) {
$caughtBy = "Question";
}
if (($result eq 'NOREPLY') or ($who eq 'NOREPLY')) {
return '';
}
if ($message =~ /(?:\+\+|--)/) { $karma = 1; }
if (!$finalQMark and !$addressed and !$tell_obj and
!$karma and
($input_message_length < getparam('minVolunteerLength'))) {
$in = '';
return 'NOREPLY';
}
}
if ($caughtBy) {
if ($tell_obj) {
$message = $tell_obj;
&status("$caughtBy: <$who>->$target<  [$message] -> $result");
} else {
&status("$caughtBy: <$who>  $message");
}
$questionCount++;
}
}
if (defined $result) {
if ($msgType =~ /public/) {
if ($target eq $who) {
&performSay($result) if ($result and not $blocked);
} else {
my $r = "$who wants you to know: $result";
&msg($target, $r);
if ($who ne $target) {
&msg($who, "told $target about $tell_obj ($r)");
}
return 'NOREPLY';
}
} else {
if ($who eq $target) {
&msg($who, $result);
} else {
my $r;
if (lc($who) eq lc($target)) {
&msg($target, $result);
} else {
$r = "$who wants you to know: $result";
&msg($target, $r);
&msg($who, "told $target about $tell_obj ($r)");
}
}
}
} else {
return "No authorization to teach" unless (IsFlag("t") eq "t");
if (!getparam('allowUpdate')) {
return '';
}
$result = &doStatement($msgType, $holdMessage);
if (($who eq 'NOREPLY')||($result eq 'NOREPLY')) { return ''; };
return 'NOREPLY' if grep $_ eq $who, split /\s+/, $param{friendlyBots};
if (defined $result) {
$caughtBy = "Statement";
if ($msgType =~ /public/) {
&say("OK, $who.") if $addressed;
} else {
&msg($who, "gotcha.");
}
}
}
if ($addressed and not $caughtBy) {
if ($msgType =~ /public/) {
&say("$who: ".$confused[int(rand(@confused))]) if $addressed;
} else {
&msg($who, $confused[int(rand(@confused))]);
}
return "NOPARSE";
}
}
1;
