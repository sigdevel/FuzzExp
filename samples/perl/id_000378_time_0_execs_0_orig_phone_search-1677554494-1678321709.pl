=begin comment
This file is called directly from the browser with:
http://localhost:8080/bin/phone_search.pl?search_string
This requires you to create a &search_phone_calls function
to search your phone database (e.g. mh/code/common/phone.pl)
=cut
my ($string) = @ARGV;
$string =~ s/search=//;
my $results = '';
if ($string) {
$results = &search_phone_calls($string) if $string;
print "db r=$results\n";
my $font_size = ( &http_agent_size < 800 ) ? 1 : 3;
$results =~ s/[^\w-\n= :]//g;
$results =~ s/[\r\f]//g;
$results =~
s/^results:(.+) matched (.+)\n/$1 matched "$2".<\/font><\/td><\/tr><tr id="resultrow" bgcolor="
$results = "<table border=0 cellpadding=0 cellspacing=1 align=center width=600><tr><td colspan=4><font size=$font_size>$results";
$results =~ s/\n\n/\n/g;
$results =~
s/ *([\d-P]*) calls= *(\d*) *last= ([a-zA-Z0-9 :]{24}) *([^\n]*)\n/\n<tr id="resultrow" bgcolor="
$results = "\n$results";
print "db3 r=$results\n";
}
my $header = html_header('Search Phone Calls');
$header .= qq[<style>
th: {backgroundColor:
</style>
];
$header .=
qq[<table><tr><form action='/bin/phone_search.pl'><td>Search String:</td><td><input align='left' size='25' name='search' value='$string'></td></form></tr></table>];
$results .= qq[
<script language="javascript">
<!--
try{
document.forms[0].search.focus();
if (document.forms[0].search.value.length>0) {document.forms[0].search.select();}
if (resultrow.length>1) {
for (x=1;x<resultrow.length;x++) {
if (x%2==0) {resultrow[x].style.backgroundColor='
}
}
}
catch(er){}
// -->
</script>
];
return &html_page( '', $header . '<br>' . $results . '</body></html>' );
