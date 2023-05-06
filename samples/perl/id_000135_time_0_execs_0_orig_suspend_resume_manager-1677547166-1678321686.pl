my $Old_umask = sprintf("%lo", umask());
umask(oct("022"));
my $Hash;
my $tmp = "";
while (<STDIN>) {
$tmp .= $_;
}
$Hash = eval($tmp);
my $Cpuset_name = $Hash->{name};
if (!defined($Cpuset_name)) {
print("[suspend_resume_manager] Bad SSH hashtable transfered\n");
exit(2);
}
my $oarexec_pid_file = $Hash->{oarexec_pid_file};
if ($ARGV[0] eq "suspend") {
if (-r "/dev/oar_cgroups_links/freezer/oar/$Cpuset_name/freezer.state") {
system(
'echo FROZEN > /dev/oar_cgroups_links/freezer/oar/' . $Cpuset_name . '/freezer.state');
} else {
system(
'
PROC=0;
test -e ' . $oarexec_pid_file . ' && PROC=$(cat ' . $oarexec_pid_file . ');
for p in $(cat /dev/cpuset/oar/' . $Cpuset_name . '/tasks)
do
if [ $PROC != $p ]
then
oardodo kill -SIGSTOP $p;
fi
done
');
}
} elsif ($ARGV[0] eq "resume") {
if (-r "/dev/oar_cgroups_links/freezer/oar/$Cpuset_name/freezer.state") {
system(
'echo THAWED > /dev/oar_cgroups_links/freezer/oar/' . $Cpuset_name . '/freezer.state');
} else {
system(
'PROCESSES=$(cat /dev/cpuset/oar/' . $Cpuset_name . '/tasks)
oardodo kill -SIGCONT $PROCESSES
');
}
} else {
print("[suspend_resume_manager] Bad command line argument $ARGV[0].\n");
exit(3);
}
exit(0);
