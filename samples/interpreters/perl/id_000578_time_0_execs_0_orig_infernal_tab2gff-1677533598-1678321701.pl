#!/usr/bin/perl -w -I/groups/eddy/home/jonest/Demotic
use strict;
use demotic_infernal_tab;
use Getopt::Std;
getopts ('E:s:G:l:m:t:g:n:u:d:b');
our ($opt_E, $opt_s, $opt_G, $opt_l, $opt_m, $opt_t, $opt_g, $opt_n, $opt_b, $opt_u, $opt_d);
(my $script = $0) =~ s/^.*\///;
my $USAGE = "
Parse cmsearch tabfile output, filter hits on user-supplied cutoffs, and output hits
in GFF2 format.
======================================================================================
USAGE: $script <options> tabfile.out > foo.gff
======================================================================================
tabfile.out ==> Output file created by using cmsearch switch '--tabfile tab.out'
from Infernal rc1.0
OPTIONS
--------------------------------------------------------------------------------------
-E  Eval_cutoff       (E)-value cutoff -- reject hits with E-value > Eval_cutoff
-s  score_cutoff      (s)score cutoff -- reject hits with bitscore < score_cutoff
-G  GC_cutoff         (G)C percent cutoff (0..100) -- reject hits with GC < GC_cutoff
-l  len_cutoff        (l)ength cutoff -- reject hits with length < len_cutoff
-m  method            (m)ethod. Default is 'Infernal'
-t  type              (t)ype. Default is 'Infernal_hit'
-g  gene_name         (g)ene name. Default is CM query name
-n  \"a short note\"  (n)ote. No default
-u  X                 (u)pstream pad   -- add X NTs to BEGINNING of all hits   (2)
-d  Y                 (d)ownstream pad -- add Y Nts to END       of all hits   (2)
--------------------------------------------------------------------------------------
NOTES:
(1) == Default behavior obtains a (non-unique) 'gene name' from the CM name. For
multiple CM queries having the same name, Infernal differentiates the models
by adding a '.N' version (eg CM.1, CM.2, etc). Specifying the gene name by '-g'
results in the same gene name being used for all hits in all reports contained
in that tabfile.
(2) == The values always add to the length of the feature. X and Y cannot be negative!
It's highly recommended that you use the '-n NOTE' feature to annotate the
changes made to the GFF start and end sites due to these flags. Script warns
when padding beyond the 5' end of the contig (and sets it to 1), but cannot edge
detect for the 3' end of the contig.
*************      While this script can parse 'tabfile' files with output from
*  WARNING  *      multiple queries (possibly containing very different CMs), only one
*************      GENE name, METHOD and TYPE will be added to all GFF lines created!
";
my $CMs          = 0;
my $hits         = 0;
my $Eval_cutoff  = 10000;
my $score_cutoff = -1000;
my $GC_cutoff    = 0;
my $len_cutoff   = 0;
my $up_pad       = 0;
my $down_pad     = 0;
my $pass_filter  = 0;
$Eval_cutoff  = $opt_E              if ($opt_E);
$score_cutoff = $opt_s              if ($opt_s);
$GC_cutoff    = $opt_G              if ($opt_G);
$len_cutoff   = $opt_l              if ($opt_l);
$up_pad       = $opt_u              if ($opt_u);
$down_pad     = $opt_d              if ($opt_d);
if ($up_pad   !~ /^\+?\d+$/) { die "Illegal pad: '$up_pad'; must be a whole positive number.";   }
if ($down_pad !~ /^\+?\d+$/) { die "Illegal pad: '$down_pad'; must be a whole positive number."; }
if (($up_pad > 100000) || ($down_pad > 100000)) {
die "Whoa, whoa! Slow down their Feyman. You're being a bit excessive with your pads. --mgmt";
}
die $USAGE unless (@ARGV == 1);
my $tabfile = shift;
open (TABFILE, "$tabfile") || die "Can't open $tabfile. You fuckin' wif me?";
&demotic_infernal_tab::parse(\*TABFILE);
close TABFILE;
$CMs  = $demotic_infernal_tab::model_num;
foreach my $rep_num (0..$CMs-1) {
$hits = $demotic_infernal_tab::num_hits[$rep_num];
foreach my $hit_num (0..$hits-1) {
$pass_filter = &filter_hit($rep_num, $hit_num);
if ($pass_filter) {
if ($pass_filter) {
&print_GFF2 ($rep_num, $hit_num);
}
else  {  next;  }
}
}
}
if ($opt_b) {
foreach my $rep (0..($CMs-1)) {
my $name = $demotic_infernal_tab::cm_name[$rep];
$hits = $demotic_infernal_tab::num_hits[$rep];
print "------------------------------------------------\n";
print "Model \
print "------------------------------------------------\n";
foreach my $j (0..$hits-1) {
my $contig  = $demotic_infernal_tab::t_name[$rep]->[$j];
my $start_t = $demotic_infernal_tab::t_start[$rep]->[$j];
my $stop_t  = $demotic_infernal_tab::t_stop[$rep]->[$j];
my $start_q = $demotic_infernal_tab::q_start[$rep]->[$j];
my $stop_q  = $demotic_infernal_tab::q_stop[$rep]->[$j];
my $score   = $demotic_infernal_tab::bitscore[$rep]->[$j];
my $e_val   = $demotic_infernal_tab::Eval[$rep]->[$j];
my $gc      = $demotic_infernal_tab::GC[$rep]->[$j];
print "
"  Tar:S-E: ",      $start_t, "-", $stop_t,
"  Que:S-E: ",      $start_q, "-", $stop_q,
"  Score: ",        $score,
"  E-val: ",        $e_val,
"  %GC: ",          $gc,
"\n";
}
}
}
sub filter_hit {
my $CM_i   = shift;
my $hit_j  = shift;
my $evalue = $demotic_infernal_tab::Eval[$CM_i]->[$hit_j];
my $score  = $demotic_infernal_tab::bitscore[$CM_i]->[$hit_j];
my $gc     = $demotic_infernal_tab::GC[$CM_i]->[$hit_j];
my $begin  = $demotic_infernal_tab::t_start[$CM_i]->[$hit_j];
my $end    = $demotic_infernal_tab::t_stop[$CM_i]->[$hit_j];
my $len    = 0;
if ($begin < $end ) {  $len = $end   - $begin + 1;  }
else                {  $len = $begin - $end   + 1;  }
if (($evalue <= $Eval_cutoff) &&
($score  >= $score_cutoff) &&
($gc     >= $GC_cutoff) &&
($len    >= $len_cutoff)) {
return 1;
}
else {
return 0;
}
}
sub print_GFF2 {
my $CM_i   = shift;
my $hit_j  = shift;
my $ctg    = $demotic_infernal_tab::t_name[$CM_i]->[$hit_j];
my $start  = $demotic_infernal_tab::t_start[$CM_i]->[$hit_j];
my $stop   = $demotic_infernal_tab::t_stop[$CM_i]->[$hit_j];
my $score  = $demotic_infernal_tab::bitscore[$CM_i]->[$hit_j];
my $frame  = ".";
my $ori    = "";
my $gene   = "gene \"$demotic_infernal_tab::cm_name[$CM_i]\"";
my $method = "Infernal";
my $type   = "Infernal_hit";
my $note   = "";
my $GFFstart = 0;
my $GFFstop  = 0;
my $over     = 0;
if ($opt_g) {  $gene = "gene \"$opt_g\"";  }
if ($opt_m) {  $method = "$opt_m";  }
if ($opt_t) {  $type = "$opt_t";   }
if ($opt_n) {  $note = "; note \"$opt_n\"";  }
if ($start <= $stop ) {
$ori = "+";
$GFFstart = $start - $up_pad;
if ($GFFstart < 1) {
$over = ($GFFstart * -1) + 1;
$GFFstart = 1;
warn "(${ctg}:${start}-${stop}) couldn't be padded the full $up_pad NTs! START set to 1.";
print "\
}
$GFFstop  = $stop  + $down_pad;
print ("$ctg\t$method\t$type\t$GFFstart\t$GFFstop\t$score\t$ori\t$frame\t${gene}$note\n");
}
elsif ($start > $stop) {
$ori = "-";
$GFFstart = $stop  - $down_pad;
if ($GFFstart < 1) {
$over = ($GFFstart * -1) + 1;
$GFFstart = 1;
warn "(${ctg}:${start}-${stop}) couldn't be padded the full $up_pad NTs! START set to 1.";
print "\
}
$GFFstop  = $start + $up_pad;
print ("$ctg\t$method\t$type\t$GFFstart\t$GFFstop\t$score\t$ori\t$frame\t${gene}$note\n");
}
if ($GFFstart > $GFFstop) {
die "Illegal GFF coords: GFFstart ($GFFstart) > GFFstop ($GFFstop)\n!";
}
}
