#!/usr/bin/perl -w
%D_STAT=(
RQ => 0,
RR => 1,
RIQ => 2,
RNXD => 3,
RFwdQ => 4,
RFwdR => 5,
RDupQ => 6,
RDupR => 7,
RFail => 8,
RFErr => 9,
RErr => 10,
RTCP => 11,
RAXFR => 12,
RLame => 13,
ROpts => 14,
SSysQ => 15,
SAns => 16,
SFwdQ => 17,
SDupQ => 18,
SFail => 19,
SFErr => 20,
SErr => 21,
RNotNsq => 22,
SNaAns => 23,
SNXD => 24,
);
my $HOSTNAME = "HOST\.YOURE\.DOMAIN";
my $LOG = "/home/";
my $RUN = "/home/";
my $INCOMING  = $D_STAT{"RQ"};
my $OUTGOING = $D_STAT{"RFail"};
my $QUE_P_MIN =();
my $QUE_P_OTHER = ();
my @N_STATS=();
my @OLD_S=();
my $UPTIME = ();
sub HIST {
open (STAT , "$LOG") or die "could not find or open file $LOG";
@N_STAT = <STAT>;
close (STAT);
open (V_OLD , "$RUN/OLD");
my @OLD_S = <V_OLD>;
close (V_OLD);
my $G_FLAG = "no";
foreach $line (@N_STAT) {
if ( $line =~ m/^([0-9]+)\s+\S+\s+\S+\sreset/ ){
$UPTIME = $1;
}
if ( $G_FLAG =~ /yes/) {
my @NUM_QUE=split ' ',$line;
open ( LOGGER , "> $RUN/OLD");
print LOGGER "$NUM_QUE[$INCOMING]\n";
print LOGGER "$NUM_QUE[$OUTGOING]\n";
close ( LOGGER );
$QUE_P_MIN = $NUM_QUE[$INCOMING]-$OLD_S[0];
$QUE_P_OTHER = $NUM_QUE[$OUTGOING]-$OLD_S[1];
$G_FLAG = "no";
}
if ($line =~ /(Global)/) {
$G_FLAG = "yes";
}
}
print "$QUE_P_MIN\n$QUE_P_OTHER\n$UPTIME\n$HOSTNAME\n";
}
&HIST();
