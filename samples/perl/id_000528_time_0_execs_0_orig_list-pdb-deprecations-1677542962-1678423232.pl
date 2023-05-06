#!/usr/bin/perl -w
$show_arg_counts = 0;
if (@ARGV)
{
if ($ARGV[0] eq "-h" || $ARGV[0] eq "--help")
{
print "Usage: $0 [-c|-h|--help]\n";
print "       -h, --help Show this usage information\n";
print "       -c         Show procedure argument counts in output\n";
print "\n";
exit;
}
if ($ARGV[0] eq "-c")
{
$show_arg_counts = 1;
shift(@ARGV);
}
}
$obsolete = ();
while (<>)
{
if ($_ =~ /^.register-procedure/)
{
$old_procedure_name = &get_old_procedure_name($_);
&check_if_procedure_is_deprecated($old_procedure_name);
&find_procedure_input_arguments;
$procedures{$old_procedure_name} = &get_argument_count;
}
}
print "The following is a list of replacement procedures that do not exist:\n";
foreach $new_procedure_name (sort(values(%deprecated)))
{
if (!exists($procedures{$new_procedure_name}))
{
print "    $new_procedure_name\n";
}
}
print "\n";
print "The following deprecated functions have no replacement:\n";
foreach $old_procedure_name (@obsolete)
{
print "    $old_procedure_name\n";
}
print "\n";
print "Deprecated procedures with a one-to-one replacement:\n";
foreach $old_procedure_name (sort(keys(%deprecated)))
{
$new_procedure_name = $deprecated{$old_procedure_name};
if (exists($procedures{$new_procedure_name}) &&
$procedures{$old_procedure_name} == $procedures{$new_procedure_name})
{
print "    \"$old_procedure_name\", \"$new_procedure_name\"\n";
}
}
print "\n";
print "Deprecated procedures where the replacement has more arguments:\n";
foreach $old_procedure_name (sort(keys(%deprecated)))
{
$new_procedure_name = $deprecated{$old_procedure_name};
if (exists($procedures{$new_procedure_name}) &&
$procedures{$new_procedure_name} > $procedures{$old_procedure_name})
{
if ($show_arg_counts == 0)
{ print "    \"$old_procedure_name\", \"$new_procedure_name\"\n"; }
else
{ print "    \"$old_procedure_name\" (", $procedures{$old_procedure_name}, "), \"$new_procedure_name\" (", $procedures{$new_procedure_name}, ")\n"; }
}
}
print "\n";
print "Deprecated procedures where the replacement has fewer arguments\nand is not one of the item API procedures:\n";
foreach $old_procedure_name (sort(keys(%deprecated)))
{
$new_procedure_name = $deprecated{$old_procedure_name};
if (exists($procedures{$new_procedure_name}) &&
$procedures{$new_procedure_name} < $procedures{$old_procedure_name} &&
$new_procedure_name !~ /-item/)
{
if ($show_arg_counts == 0)
{ print "    \"$old_procedure_name\", \"$new_procedure_name\"\n"; }
else
{ print "    \"$old_procedure_name\" (", $procedures{$old_procedure_name}, "), \"$new_procedure_name\" (", $procedures{$new_procedure_name}, ")\n"; }
}
}
print "\n";
print "Deprecated procedures where the replacement has fewer arguments\nand is one of the item API procedures:\n";
foreach $old_procedure_name (sort(keys(%deprecated)))
{
$new_procedure_name = $deprecated{$old_procedure_name};
if (exists($procedures{$new_procedure_name}) &&
$procedures{$new_procedure_name} < $procedures{$old_procedure_name} &&
$new_procedure_name =~ /-item/)
{
if ($show_arg_counts == 0)
{ print "    \"$old_procedure_name\", \"$new_procedure_name\"\n"; }
else
{ print "    \"$old_procedure_name\" (", $procedures{$old_procedure_name}, "), \"$new_procedure_name\" (", $procedures{$new_procedure_name}, ")\n"; }
}
}
exit;
sub get_old_procedure_name
{
local (@words);
@words = split(/\"/, "@_");
$words[1] =~ s/_/-/g;
$words[1] =~ s/ [<]1[>]//;
return $words[1];
}
sub check_if_procedure_is_deprecated
{
local ($old_procedure_name) = @_;
local ($line, @words);
$line = <>;
if ($line !~ /[Dd]eprecated/)
{
return 0;
}
$new_procedure_name = "";
$line =~ s/^\s+//;
@words = split(/ /, $line);
if ($line =~ /[Uu]se /)
{
if ($line =~ /Deprecated:/)
{
$words[2] =~ s/\'//g;
$words[2] =~ s/_/-/g;
$new_procedure_name = $words[2];
}
else
{
$words[5] =~ s/\'//g;
$words[5] =~ s/_/-/g;
$new_procedure_name = $words[5];
}
}
if ($new_procedure_name eq "")
{
push (@obsolete, $old_procedure_name);
}
else
{
$deprecated{$old_procedure_name} = $new_procedure_name;
}
return 1;
}
sub find_procedure_input_arguments
{
while (<> !~ /^  \(/)
{
}
}
sub get_argument_count
{
local ($arg_count, $line);
$arg_count = 0;
do
{
$line = <>;
if ($line =~ /^  \)/)
{
return $arg_count;
}
++$arg_count;
do {
$line = <>;
} while ($line !~ /^    \)/);
} while ($line !~ /^  \)/);
return $arg_count;
}
