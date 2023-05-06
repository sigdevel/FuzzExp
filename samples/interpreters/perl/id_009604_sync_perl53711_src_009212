#!/usr/bin/perl
undef $/;
$LastYear = "2021";
$LastMonth = "May";
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
if(!($newfilename =~ /^\.(\.|git)?$/))
{
local $longfilename = $filename."/".$newfilename;
load($longfilename);
}
}
closedir($f);
}
else
{
if($filename =~ /(README.*|ttcn3_help|titanver|Makefile.*|\.(adoc|properties|iml|g4|tpd|java|ttcn|cc|hh|xml|prj|py|xsd|sh|c|h|html|l|y|asn|1|xsl|fast_script|script|pl|cfg|txt|hhc|hhp|dot|ttcnpp|converter|ttcnin|ttcn3|dat|grp|prj|awk|ddf|pats|css|js|launch|rdf|lex|tpl)|Readme|ttcn3.*|compiler|make|license|script_not_running|compiler\.1|ttcn3_logmerge\.1|ttcn3_logformat\.1|ttcn3_logfilter\.1|ttcn3_makefilegen\.1)$/)
{
open(IN, $filename);
$whole_file = <IN>;
close(IN);
$c = 0;
$c += $whole_file =~ s/Copyright \(c\) 2000-2020 Ericsson Telecom AB/Copyright (c) 2000-${LastYear} Ericsson Telecom AB/gs;
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
