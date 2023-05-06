sub vm_runtime_info
{
my ($vmname) = @_;
my $state = 0;
my $output = " ";
my $runtime;
my $vm_connectionState;
my $vm_guestState;
my $tools_out;
my $issues;
my $issue_cnt = 0;
my $issue_out = '';
my $actual_state;
my $true_sub_sel=1;
my $vm_view = Vim::find_entity_view(view_type => 'VirtualMachine', filter => {name => $vmname}, properties => ['name', 'runtime', 'overallStatus', 'guest', 'configIssue']);
if (!defined($vm_view))
{
print "VMware machine " . $vmname . " does not exist\n";
exit 2;
}
$runtime = $vm_view->runtime;
if (!defined($subselect))
{
$subselect = "all";
$true_sub_sel = 0;
}
if (($subselect eq "con") || ($subselect eq "all"))
{
$true_sub_sel = 0;
$vm_connectionState = $runtime->connectionState->val;
if ($vm_connectionState eq "connected")
{
$state = 0;
$output = "Connection state: " . $vm_connectionState;
}
if (($vm_connectionState eq "disconnected") || ($vm_connectionState eq "orphaned"))
{
$state = 1;
$output = "Connection state:" . $vm_connectionState;
}
if (($vm_connectionState eq "inaccessible") || ($vm_connectionState eq "invalid"))
{
$state = 1;
$output = "Connection state:" . $vm_connectionState;
}
}
if (($subselect eq "powerstate") || ($subselect eq "all"))
{
$true_sub_sel = 0;
$actual_state = 0;
if ($subselect eq "all")
{
$output = $output . " - Power state: " . $runtime->powerState->val;
}
else
{
$output = "Power state: " . $runtime->powerState->val;
}
$state = check_state($state, $actual_state);
}
if (($subselect eq "status") || ($subselect eq "all"))
{
$true_sub_sel = 0;
$actual_state = check_health_state($vm_view->overallStatus->val);
if ($subselect eq "all")
{
$output = $output . "  - Overall status: " . $vm_view->overallStatus->val;
}
else
{
$output = "Overall status: " . $vm_view->overallStatus->val;
}
$state = check_state($state, $actual_state);
}
if (($subselect eq "consoleconnections") || ($subselect eq "all"))
{
$true_sub_sel = 0;
if ($subselect eq "all")
{
if ( $perf_thresholds ne ";")
{
$output = "Thresholds only allowed with valid subselect.";
$actual_state = 2;
}
else
{
$actual_state = 0;
$output = $output . " - Console connections: " . $runtime->numMksConnections;
}
}
else
{
$actual_state = check_against_threshold($runtime->numMksConnections);
$output = "Console connections:" . $runtime->numMksConnections;
}
$state = check_state($state, $actual_state);
}
if (($subselect eq "gueststate") || ($subselect eq "all"))
{
$true_sub_sel = 0;
if (exists($vm_view->guest->{toolsVersionStatus}) && defined($vm_view->guest->toolsVersionStatus) && exists($vm_view->guest->{toolsRunningStatus}) && defined($vm_view->guest->toolsRunningStatus))
{
if ($vm_view->guest->toolsVersionStatus ne "guestToolsNotInstalled")
{
if ($vm_view->guest->toolsRunningStatus ne "guestToolsNotRunning")
{
if ($vm_view->guest->toolsRunningStatus ne "guestToolsExecutingScripts")
{
$vm_guestState = $vm_view->guest->guestState;
if ($vm_guestState eq "running")
{
$actual_state = 0;
}
if (($vm_guestState eq "shuttingdown") || ($vm_guestState eq "resetting") || ($vm_guestState eq "standby") || ($vm_guestState eq "notrunning"))
{
$actual_state = 1;
}
if ($vm_guestState eq "unknown")
{
$actual_state = 3;
}
}
else
{
$vm_guestState = "Not available. VMware tools starting.";
$actual_state = 1;
}
}
else
{
if (($runtime->powerState->val eq "poweredOff") || ($runtime->powerState->val eq "suspended"))
{
$vm_guestState = "Not available. VM powered off or suspended. VMware tools not running.";
$actual_state = 0;
}
else
{
$vm_guestState = "Not available. VMware tools not running.";
$actual_state = 1;
}
}
}
else
{
$vm_guestState = "Not available. VMware tools not installed.";
$actual_state = 1;
}
}
else
{
$vm_guestState = "Not available. No information about VMware tools available. Please check!";
$actual_state = 1;
}
if ($subselect eq "all")
{
$output = $output . " - Guest state: " . $vm_guestState;
}
else
{
$output = "Guest state: " . $vm_guestState;
}
$state = check_state($state, $actual_state);
}
if (($subselect eq "tools") || ($subselect eq "all"))
{
$true_sub_sel = 0;
if (exists($vm_view->guest->{toolsVersionStatus}) && defined($vm_view->guest->toolsVersionStatus) && exists($vm_view->guest->{toolsRunningStatus}) && defined($vm_view->guest->toolsRunningStatus))
{
if ($vm_view->guest->toolsVersionStatus ne "guestToolsNotInstalled")
{
if ($vm_view->guest->toolsRunningStatus ne "guestToolsNotRunning")
{
if ($vm_view->guest->toolsRunningStatus ne "guestToolsExecutingScripts")
{
if ($vm_view->guest->toolsVersionStatus eq "guestToolsBlacklisted")
{
$tools_out = "VMware Tools are installed and running, but the installed ";
$tools_out = $tools_out ."version is known to have a grave bug and should ";
$tools_out = $tools_out ."be immediately upgraded.";
$actual_state = 2;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsCurrent")
{
$tools_out = "VMware Tools are installed, running and the version is current.";
$actual_state = 0;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsNeedUpgrade")
{
$tools_out = "VMware Tools are installed and running, but the version is not current.";
$actual_state = 1;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsSupportedNew")
{
$tools_out = "VMware Tools are installed, running, supported and newer than the ";
$tools_out = $tools_out ."version available on the host.";
$actual_state = 1;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsSupportedOld")
{
$tools_out = "VMware Tools are installed, running, supported, but a newer version is available.";
$actual_state = 1;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsTooNew")
{
$tools_out = "VMware Tools are installed and running but the version is known to be too new ";
$tools_out = $tools_out ."to work correctly with this virtual machine.";
$actual_state = 2;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsTooOld")
{
$tools_out = "VMware Tools are installed and running, but the version is too old.";
$actual_state = 1;
}
if ($vm_view->guest->toolsVersionStatus eq "guestToolsUnmanaged")
{
$tools_out = "VMware Tools are installed and running, but not managed by VMWare. ";
if (defined($openvmtools))
{
$actual_state = 0;
}
else
{
$actual_state = 1;
}
}
}
else
{
$tools_out = "VMware tools starting.";
$actual_state = 1;
}
}
else
{
if (($runtime->powerState->val eq "poweredOff") || ($runtime->powerState->val eq "suspended"))
{
$tools_out = "VM powered off or suspended. VMware tools not running.";
$actual_state = 0;
}
else
{
$tools_out = "VMware tools not running.";
$actual_state = 1;
}
}
}
else
{
$tools_out = "VMware tools not installed.";
if (defined($no_vmtools))
{
$actual_state = 0;
}
else
{
$actual_state = 1;
}
}
}
else
{
$tools_out = "No information about VMware tools available. Please check!";
$actual_state = 1;
}
if ($subselect eq "all")
{
$output = $output . " - Tools state: " . $tools_out;
}
else
{
$output = "Tools state: " . $tools_out;
}
$state = check_state($state, $actual_state);
}
if (($subselect eq "issues") || ($subselect eq "all"))
{
$true_sub_sel = 0;
$issues = $vm_view->configIssue;
$actual_state = 0;
if (defined($issues))
{
$issue_out = "Issues: ";
foreach (@$issues)
{
$actual_state = 2;
$issue_cnt++;
$issue_out = $issue_out . $_->fullFormattedMessage . "(caused by " . $_->userName . ")" . $multiline;
}
}
if ($subselect eq "all")
{
$output = $output . " - " . $issue_cnt . " config issues";
}
else
{
$output = $issue_cnt . " config issues" . $multiline . $issue_out;
}
$state = check_state($state, $actual_state);
}
if ($true_sub_sel == 1)
{
get_me_out("Unknown VM RUNTIME subselect");
}
else
{
return ($state, $output);
}
}
1;
