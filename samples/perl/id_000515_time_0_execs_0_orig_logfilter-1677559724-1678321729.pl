#!perl.exe
%icmp = ();
%udp = ();
%tcp = ();
%openfiles = ();
$TIDBITSFILE = "unknown.log";
while (<DATA>) {
chomp;
s/
s/^\s+//;
s/\s+$//;
next unless length;
$_ = lc;
($proto, $identifier, $filename) = m/(\S+)\s+(\S+)\s+(\S+)/;
SWITCH: {
if ($proto =~ m/^icmp$/) { $icmp{$identifier} = $filename; last SWITCH; };
if ($proto =~ m/^udp$/) { $udp{$identifier} = $filename; last SWITCH; };
if ($proto =~ m/^tcp$/) { $tcp{$identifier} = $filename; last SWITCH; };
die "An unknown protocol listed in the proto defs\n$_\n";
}
}
$filename = shift;
unless (defined($filename)) { die "Usage: logfilter.pl <log file>\n"; }
open(LOGFILE, $filename) || die "Could not open the firewall log file.\n";
$openfiles{$filename} = "LOGFILE";
$linenum = 0;
while($line = <LOGFILE>) {
chomp($line);
$linenum++;
SWITCH: {
($line =~ m /\sicmp\s/) && do {
($icmptype) = $line =~ m/icmp (\d+)\/\d+/;
$filename = $TIDBITSFILE;
$filename = $icmp{$icmptype} if (defined($icmp{$icmptype}));
last SWITCH;
};
($line =~ m /\stcp\s/) && do {
($sport, $dport) = $line =~ m/\d+\.\d+\.\d+\.\d+,(\d+) -> \d+\.\d+\.\d+\.\d+,(\d+)/;
$filename = $TIDBITSFILE;
$filename = $tcp{$sport} if (defined($tcp{$sport}));
$filename = $tcp{$dport} if (defined($tcp{$dport}));
last SWITCH;
};
($line =~ m /\sudp\s/) && do {
($sport, $dport) = $line =~ m/\d+\.\d+\.\d+\.\d+,(\d+) -> \d+\.\d+\.\d+\.\d+,(\d+)/;
$filename = $TIDBITSFILE;
$filename = $udp{$sport} if (defined($udp{$sport}));
$filename = $udp{$dport} if (defined($udp{$dport}));
last SWITCH;
};
$filename = $TIDBITSFILE;
}
if (defined($openfiles{$filename})) {
$handle = $openfiles{$filename};
} else {
$handle = "HANDLE" . keys %openfiles;
open ($handle, ">>".$filename) || die "Couldn't open|create the file $filename";
$openfiles{$filename} = $handle;
}
print $handle "
}
foreach $key (keys %openfiles) {
close($openfiles{$key});
}
close(LOGFILE);
__DATA__
icmp    3         destunreach.log
icmp    8         ping.log
icmp    9         router.log
icmp    10        router.log
icmp    11        ttl.log
tcp     23        telnet.log
tcp     25        smtp.log
udp     25        smtp.log
udp     53        dns.log
tcp     80        http.log
tcp     110       pop3.log
tcp     111       rpc.log
udp     111       rpc.log
tcp     137       netbios.log
udp     137       netbios.log
tcp     143       imap.log
udp     161       snmp.log
udp     370       backweb.log
udp     371       backweb.log
tcp     443       https.log
udp     443       https.log
udp     512       syslog.log
tcp     635       nfs.log
udp     635       nfs.log
tcp     1080      socks.log
udp     1080      socks.log
tcp     6112      games.log
tcp     6667      irc.log
tcp     7070      realaudio.log
tcp     8080      http.log
tcp     12345     netbus.log
udp     31337     backorifice.log
