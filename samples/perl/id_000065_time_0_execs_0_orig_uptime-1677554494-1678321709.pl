if ( $OS_win or $^O eq 'cygwin' ) {
return "$Tk_objects{label_uptime_mh} &nbsp;&nbsp; $Tk_objects{label_uptime_cpu}";
}
else {
return `uptime`;
}
