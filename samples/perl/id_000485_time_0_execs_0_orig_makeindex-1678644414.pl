#!/usr/bin/perl
sub Usage {
print
"Usage: makeindex xhtmldir xmldir
where xhtmldir contains a directory full of OpenGL .xml XHTML man pages -AND-
where xmldir contains a directory full of OpenGL .xml source XML man pages
probably want to redirect output into a file like
./makeindex.pl . .. > ./index.html
"
}
sub PrintHeader {
print '<html>
<head>
<title>OpenGL Documentation</title>
<style type="text/css">
html, body, table
{   color:
padding: 4px 4px;
margin: 0px 0 0 0;
text-align: center;
font-family: Arial, Lucida, sans-serif;
font-size: 10pt;
}
margin: 10px;
font-size: 14pt;
text-decoration:none;
}
table.sample {
border-width: 1px;
border-spacing: 5px;
border-style: dotted;
border-color: black;
border-collapse: separate;
background-color:
}
table.sample th {
border-width: 1px;
padding: 5px;
border-style: none;
}
table.sample td {
border-width: 1px;
padding: 1px;
border-style: none;
}
</style>
</head>
<body>
<a name="top"></a>
<h1>OpenGL 2.1 Reference Pages</h1>
<br/><br/>
';
}
sub PrintFooter {
print '
</body>
</html>
';
}
sub TableElementForFilename {
my $name = shift;
my $strippedname = $name;
$strippedname =~ s/\.xml//;
print "\t";
print '<tr><td><a target="pagedisp" href="' , $name , '">';
print "$strippedname";
print "</a></td></tr>\n";
}
sub BeginTable {
my $letter = shift;
print "<a name=\"$letter\"></a><br/><br/>\n";
print '<table width="200" align="center" class="sample">';
print "\t<th>";
print "$letter</th>\n";
}
sub EndTable {
print "\t";
print '<tr><td><center><a href="
print "\n</table>\n\n";
}
if (@ARGV != 2)
{
Usage();
die;
}
opendir(DIR,$ARGV[0]) or die "couldn't open directory";
@files = readdir(DIR);
close(DIR);
@files = sort @files;
PrintHeader();
my @glX;
my @glut;
my @glu;
my @gl;
my @realEntrypoints;
my @pageNames;
foreach (@files)
{
if (/xml/)
{
$parentName = $ARGV[1] . '/' . $_;
if (open(PARENT, $parentName))
{
@funcs = <PARENT>;
@funcs = grep(/<funcdef>/, @funcs);
foreach (@funcs)
{
$func = $_;
$func =~ s/.*<function>//;
$func =~ s/<\/function>.*\n//;
push (@realEntrypoints, $func);
}
close(PARENT);
}
}
}
foreach (@files)
{
if (/xml/)
{
$parentName = $ARGV[1] . '/' . $_;
if (open(PARENT, $parentName))
{
my $entrypoint = $_;
$entrypoint =~ s/\.xml//;
push (@pageNames, $entrypoint);
close(PARENT);
}
}
}
foreach (@files)
{
if (/xml/)
{
my $needIndexEntry = 0;
my $entrypoint = $_;
$entrypoint =~ s/\.xml//;
foreach (@pageNames)
{
if ($_ eq $entrypoint)
{
$needIndexEntry = 1;
}
}
if ($needIndexEntry == 0)
{
foreach (@realEntrypoints)
{
if ($_ eq $entrypoint)
{
$needIndexEntry = 1;
foreach (@pageNames)
{
my $alteredEntrypoint = $entrypoint;
$alteredEntrypoint =~ s/$_//;
if (!($alteredEntrypoint eq $entrypoint))
{
$needIndexEntry = 0;
}
}
}
}
}
if ($needIndexEntry)
{
if (/^glX/)
{
push (@glX, $_);
}
elsif (/^glut/)
{
push (@glut, $_);
}
elsif (/^glu/)
{
push (@glu, $_);
}
elsif (/^gl/)
{
push (@gl, $_);
}
}
}
}
my @toc;
if ($
{
$currentletter = "";
$opentable = 0;
foreach (@gl)
{
$name = $_;
$name =~ s/^gl//;
$firstletter = substr($name, 0, 1);
if ($firstletter ne $currentletter)
{
push (@toc, $firstletter);
$currentletter = $firstletter;
}
}
if ($
if ($
if ($
}
print '<div id="container">';
foreach (@toc)
{
print '<b><a href="
print $_;
print '" style="text-decoration:none"> ';
print $_;
print " </a></b> &nbsp; ";
}
print "</div>\n\n\n";
if ($
{
$currentletter = "";
$opentable = 0;
foreach (@gl)
{
$name = $_;
$name =~ s/^gl//;
$firstletter = substr($name, 0, 1);
if ($firstletter ne $currentletter)
{
if ($opentable == 1)
{
EndTable();
}
BeginTable($firstletter);
$opentable =1;
$currentletter = $firstletter;
}
TableElementForFilename($_);
}
if ($opentable)
{
EndTable();
}
}
if ($
{
BeginTable("glu");
foreach (@glu)
{
TableElementForFilename($_);
}
EndTable();
}
if ($
{
BeginTable("glut");
foreach (@glut)
{
TableElementForFilename($_);
}
EndTable();
}
if ($
{
BeginTable("glX");
foreach (@glX)
{
TableElementForFilename($_);
}
EndTable();
}
PrintFooter();
