#!/usr/bin/perl
undef $/;
$fileindex = 0;
$total = 0;
sub load
{
local $filename = shift;
local $f = "F".$fileindex++;
if(opendir($f, $filename))
{
while(local $newfilename = readdir($f))
{
if(!($newfilename =~ /^\.(\.)?$/))
{
local $longfilename = $filename."/".$newfilename;
load($longfilename);
}
}
closedir($f);
}
else
{
if($filename =~ /(config)$/)
{
print("-> $filename\n");
open(IN, $filename);
$whole_file = <IN>;
close(IN);
$c = 0;
$c += $whole_file =~ s!url = http://git.eclipse.org/gitroot/titan/!url = ssh://jbalasko\@git.eclipse.org:29418/titan/!gs;
if ( $c > 0 )
{
open(OUT, ">$filename");
print OUT $whole_file;
close(OUT);
print("Copyright info changed: $filename\n");
$total++;
}
}
}
}
load(".");
print("Total number of changed files: $total\n");
