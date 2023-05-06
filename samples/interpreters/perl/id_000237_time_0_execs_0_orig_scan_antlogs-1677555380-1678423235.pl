#!/usr/bin/perl
my $pdk_src = "../..";
my %missing_files;
my %damaged_components;
my %excluded_things;
my %damaged_bldinfs;
sub canonical_path($)
{
my ($path) = @_;
my @bits = split /\//, $path;
my @newbits = ();
foreach my $bit (@bits)
{
next if ($bit eq ".");
if ($bit eq "..")
{
pop @newbits;
next;
}
push @newbits, $bit;
}
return join("/", @newbits);
}
sub excluded_thing($$$)
{
my ($path, $missing, $reason) = @_;
if (!defined $excluded_things{$path})
{
@{$excluded_things{$path}} = ();
}
push @{$excluded_things{$path}}, $missing;
}
sub do_missing_file($$$)
{
my ($missing, $missing_from, $reason) = @_;
$missing = canonical_path($missing);
$missing_from = canonical_path($missing_from);
my $component = "??";
if ($missing_from ne "??")
{
my @dirs = split /\//, $missing_from;
shift @dirs if ($dirs[0] eq "sf");
$path = $pdk_src . "/sf/$dirs[0]/$dirs[1]";
if (!-e $path)
{
excluded_thing($path, $missing, $reason);
return;
}
$path .= "/$dirs[2]";
if (!-e $path)
{
excluded_thing($path, $missing, $reason);
return;
}
$path .= "/$dirs[3]";
if (!-e $path)
{
excluded_thing($path, $missing, $reason);
return;
}
$component = join("/", $dirs[0], $dirs[1], $dirs[2], $dirs[3]);
}
$missing_files{$missing} = $reason if ($missing ne "??");
if (!defined $damaged_components{$component})
{
@{$damaged_components{$component}} = ();
}
push @{$damaged_components{$component}}, $missing;
}
sub scan_logfile($)
{
my ($logfile) = @_;
open FILE, "<$logfile" or print "Error: cannot open $logfile: $!\n" and return;
my $line;
while ($line = <FILE>)
{
if ($line =~ /Source (of|zip for) export does not exist.\s+.*\/(sf\/.*)$/)
{
do_missing_file($2, "??", "source of export");
next;
}
if ($line =~ /No bld.inf found at (.*\/)?(sf\/.*) in /i)
{
my $bldinf = "$2/bld.inf";
do_missing_file($bldinf, $bldinf, "no bld.inf");
$damaged_bldinfs{"$bldinf\t(missing)"} = 1;
next;
}
if ($line =~ /Can.t find mmp file .*(sf\/.*)' referred to by .*(sf\/.*)'/i)
{
my $mmpfile = $1;
my $bldinf = $2;
do_missing_file($mmpfile, $bldinf, "no mmp file");
next;
}
if ($line =~ /cpp.exe: .*\/(sf\/[^:]*):.*\s+([^:]+): No such file/)
{
my $parent = $1;
my $relative = $2;
if ($parent =~ /\.inf$/i)
{
my $parent = canonical_path($parent);
$damaged_bldinfs{"$parent\t$relative"} = 1;
}
do_missing_file("$parent/../$relative", $parent, "
next;
}
if ($line =~ /No rule to make target .*(sf\/.*)', needed by .*(epoc32\/.*)'/)
{
my $missing = $1;
my $impact = "building $2";
if ($impact =~ /epoc32\/build\/[^\/]+\/[^\/]+\/([^\/]+)\//)
{
$impact = "building $1";
}
do_missing_file($missing, "??", $impact);
next;
}
}
close FILE;
}
my @logfiles = map(glob,@ARGV);
foreach my $logfile (@logfiles)
{
print "Scanning $logfile...\n";
scan_logfile($logfile);
}
printf "%d Excluded things\n", scalar keys %excluded_things;
foreach my $component (sort keys %excluded_things)
{
my @list = @{$excluded_things{$component}};
my %hash;
foreach my $missing (@list)
{
$hash{$missing} = 1;
}
printf "%s\t%d\n", $component, scalar keys %hash;
print "\t", join("\n\t", sort keys %hash), "\n";
}
print "\nDamaged components\n";
foreach my $component (sort keys %damaged_components)
{
my @list = @{$damaged_components{$component}};
my %hash;
foreach my $missing (@list)
{
$hash{$missing} = 1;
}
printf "%s\t%d\n", $component, scalar keys %hash;
print "\t", join("\n\t", sort keys %hash), "\n";
}
print "\nMissing files\n";
foreach my $missing (sort keys %missing_files)
{
my $reason = $missing_files{$missing};
my @dirs = split /\//, $missing;
my $path = shift @dirs;
my $dir;
while ($dir = shift @dirs)
{
if (-e "$pdk_src/$path/$dir")
{
$path .= "/$dir";
next;
}
print "\t$reason\t$path\t\t", join("/", $dir,@dirs), "\n";
last;
}
}
print "\nDamaged bld.infs\n";
print join("\n", sort keys %damaged_bldinfs, "");
print "\n\n";
printf "%d files missing from ", scalar keys %missing_files;
printf "%d damaged components\n", scalar keys %damaged_components;
