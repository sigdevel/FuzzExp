package main;
$CITE_OPEN_DELIM = '(' unless $CITE_OPEN_DELIM;
$CITE_CLOSE_DELIM = ')' unless $CITE_CLOSE_DELIM;
$CITE_ENUM = '; ' unless $CITE_ENUM;
$SORT_MULTIPLE = 0 unless $SORT_MULTIPLE;
$NUMERIC=0 unless defined ($NUMERIC);
$BEFORE_PAR_YEAR=', ' unless $BEFORE_PAR_YEAR;
$COMMON_AUTHOR_SEP=',' unless $COMMON_AUTHOR_SEP;
$POST_NOTE=',' unless $POST_NOTE;
$CITEINDEX=0 unless defined ($CITEINDEX);
$HARVARD=0 unless defined ($HARVARD);
$cite_mark = '<tex2html_cite_mark>';
$cite_full_mark = '<tex2html_cite_full_mark>';
$cite_par_mark = '<tex2html_cite_par_mark>';
$cite_par_full_mark = '<tex2html_cite_par_full_mark>';
$citet_mark = '<tex2html_citet_mark>';
$citet_full_mark = '<tex2html_citet_full_mark>';
$citet_ext_mark = '<tex2html_citet_ext_mark>';
$citealp_mark = '<tex2html_citealp_mark>';
$citealp_full_mark = '<tex2html_citealp_full_mark>';
$citealt_mark = '<tex2html_citealt_mark>';
$citealt_full_mark = '<tex2html_citealt_full_mark>';
$cite_author_mark = '<tex2html_cite_author_mark>';
$cite_author_full_mark = '<tex2html_cite_author_full_mark>';
$cite_year_mark = '<tex2html_cite_year_mark>';
$cite_multiple_mark = '<tex2html_cite_multiple_mark>';
$HARVARDAND="&amp;";
@citestyle_chicago  =('(',  ')',  '; ',  'a',  ', ',  ',' );
@citestyle_named    =('[',  ']',  '; ',  'a',  ', ',  ',' );
@citestyle_agu      =('[',  ']',  '; ',  'a',  ', ',  ', ');
@citestyle_egs      =('(',  ')',  '; ',  'a',  ', ',  ',' );
@citestyle_agsm     =('(',  ')',  ', ',  'a',  ''  ,  ',' );
@citestyle_kluwer   =('(',  ')',  ', ',  'a',  ''  ,  ',' );
@citestyle_dcu      =('(',  ')',  '; ',  'a',  '; ',  ',' );
@citestyle_aa       =('(',  ')',  '; ',  'a',  ''  ,  ',' );
@citestyle_pass     =('(',  ')',  '; ',  'a',  ', ',  ',' );
@citestyle_anngeo   =('(',  ')',  '; ',  'a',  ', ',  ',' );
@citestyle_nlinproc =('(',  ')',  '; ',  'a',  ', ',  ',' );
$HARVARDAND_dcu = 'and';
sub do_natbib_round {
$CITE_OPEN_DELIM = '(';
$CITE_CLOSE_DELIM = ')'; }
sub do_natbib_square {
$CITE_OPEN_DELIM = '[';
$CITE_CLOSE_DELIM = ']'; }
sub do_natbib_curly {
$CITE_OPEN_DELIM = '{';
$CITE_CLOSE_DELIM = '}'; }
sub do_natbib_angle {
$CITE_OPEN_DELIM = '&lt;';
$CITE_CLOSE_DELIM = '&gt;'; }
sub do_natbib_colon {
$CITE_ENUM = '; '; }
sub do_natbib_comma {
$CITE_ENUM = ', '; }
sub do_natbib_authoryear {
$NUMERIC=0; }
sub do_natbib_numbers {
$NUMERIC=1; }
sub do_natbib_sectionbib {
$section_commands{'bibliography'} = 3; }
sub do_natbib_sort {
$SORT_MULTIPLE = 1; }
sub do_cmd_cite {
local($_) = @_;
local($cite_key, @cite_keys);
local($has_optional,$optional1,$optional2)=&cite_check_options;
local ($c_mark) = ($has_optional ? $cite_par_mark : $cite_mark);
$c_mark = $cite_par_mark if ($NUMERIC);
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join(''
, &do_cite_keys($br_id,($has_optional || $NUMERIC)
,$optional1,$optional2,$c_mark,$cite_key )
, $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citestar {
local($_) = @_;
local($cite_key, @cite_keys);
local($has_optional,$optional1,$optional2)=&cite_check_options;
local ($c_mark) = ($has_optional ? $cite_par_full_mark : $cite_full_mark);
$c_mark = $cite_par_mark if ($NUMERIC);
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,($has_optional || $NUMERIC)
,$optional1,$optional2,$c_mark,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citeaffixed {
local($_) = @_;
local($cite_key, @cite_keys);
local ($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
$cite_key=$2;
s/$next_pair_pr_rx//o;
local($optional2)=$2;
if ($cite_key) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,1,
$optional1,$optional2,$cite_par_mark,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citeaffixedstar {
local($_) = @_;
local($cite_key, @cite_keys);
local ($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
$cite_key=$2;
s/$next_pair_pr_rx//o;
local($optional2)=$2;
if ($cite_key) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,1,
$optional1,$optional2,
($NUMERIC ? $cite_par_mark: $cite_par_full_mark),
$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citeasnoun {
local($_) = @_;
local($cite_key, @cite_keys);
local($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,
$optional1,'',($NUMERIC? $cite_par_mark : $cite_mark)
,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citeasnounstar {
local($_) = @_;
local($cite_key, @cite_keys);
local($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,
$optional1,'',($NUMERIC? $cite_par_mark : $cite_full_mark)
,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_possessivecite {
local($_) = @_;
local($cite_key, @cite_keys);
local($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,
$optional1,'',($NUMERIC? $cite_par_mark : $citealt_mark)
,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_possessivecitestar {
local($_) = @_;
local($cite_key, @cite_keys);
local($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,
$optional1,'',($NUMERIC? $cite_par_mark : $citealt_full_mark)
,$cite_key), $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citename {
local($_) = @_;
local($cite_key, @cite_keys);
local($optional1,$dummy)=&get_next_optional_argument;
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,$optional1,'',
($NUMERIC ? $cite_par_mark : $cite_author_mark)
,$cite_key),$_);
}
else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_citenamestar {
local($_) = @_;
local($optional1,$dummy)=&get_next_optional_argument;
local($cite_key, @cite_keys);
s/^\s*\\space//o;
s/$next_pair_pr_rx//o;
if ($cite_key = $2) {
local ($br_id)=$1;
$_ = join('',
&do_cite_keys($br_id,$NUMERIC,$optional1,'',
($NUMERIC ? $cite_par_mark :$cite_author_full_mark)
,$cite_key),$_);
}
else {print "Cannot find citation argument\n";}
$_;
}
sub do_cmd_harvardparenthesis {
local ($_)=@_;
s/$next_pair_pr_rx//o;
local($arg)=$2;
SWITCH: {
$arg =~ /round/ && do {
$CITE_OPEN_DELIM='(';
$CITE_CLOSE_DELIM=')';
last SWITCH};
$arg =~ /curly/ && do {
$CITE_OPEN_DELIM='{';
$CITE_CLOSE_DELIM='}';
last SWITCH};
$arg =~ /square/ && do {
$CITE_OPEN_DELIM='[';
$CITE_CLOSE_DELIM=']';
last SWITCH};
$arg =~ /angle/ && do {
$CITE_OPEN_DELIM='&lt';
$CITE_CLOSE_DELIM='&gt';
last SWITCH};
$arg =~ /none/ && do {
$CITE_OPEN_DELIM='';
$CITE_CLOSE_DELIM='';
last SWITCH};
print "\nInvalid argument to \\harvardparenthesis: $arg!\n"
}
$_;
}
sub do_cmd_citeyear    {
do_cite_common($HARVARD,($HARVARD ? $cite_par_mark : $cite_year_mark),
$cite_year_mark,@_); }
sub do_cmd_citeyearpar {
do_cite_common(1,$cite_year_mark,$cite_year_mark,@_); }
sub do_cmd_citeyearstar {
do_cite_common($NUMERIC,$cite_par_mark,$cite_year_mark,@_) }
sub do_cmd_citeyearparstar {
do_cite_common($NUMERIC,$cite_par_mark,$cite_year_mark,@_) }
sub do_cmd_citet {
do_cite_common('',$citet_mark,$citet_mark,@_) }
sub do_cmd_citetstar {
do_cite_common('',$citet_full_mark,$citet_full_mark,@_) }
sub do_cmd_citep {
do_cite_common(1,$cite_par_mark,$cite_par_mark,@_) }
sub do_cmd_citepstar {
do_cite_common(1,$cite_par_mark,$cite_par_full_mark,@_) }
sub do_cmd_citealt {
do_cite_common(0,$citealt_mark,$citealt_mark,@_); }
sub do_cmd_citealtstar {
do_cite_common(0,$citealt_full_mark,$citealt_full_mark,@_); }
sub do_cmd_citealp {
do_cite_common(0,$cite_par_mark,$citealp_mark,@_) }
sub do_cmd_citealpstar {
do_cite_common(0,$cite_par_mark,$citealp_full_mark,@_) }
sub do_cmd_citeauthor {
do_cite_common(0,$cite_author_mark,$cite_author_mark,@_) }
sub do_cmd_citeauthorstar {   &do_cmd_citefullauthor(@_); }
sub do_cmd_citefullauthor {
do_cite_common(0,$cite_author_full_mark,$cite_author_full_mark,@_) }
sub do_cite_common {
local($has_parens,$num_mark,$norm_mark,$_) = @_;
local($cite_key, @cite_keys);
local($has_optional,$optional1,$optional2)=&cite_check_options;
s/^\s*\\space//o;
if (s/$next_pair_pr_rx//) {
$cite_key = $2;
local ($br_id)=$1;
$_ = join(''
, &do_cite_keys ($br_id, $has_parens, $optional1, $optional2
,($NUMERIC ? $num_mark : $norm_mark)
,$cite_key)
, $_);
} else {print "Cannot find citation argument\n";}
$_;
}
sub cite_check_options {
if ($HARVARD) {
local($opt1,$dummy)=&get_next_optional_argument;
(1,$opt1,'')
} else {
local($hasopt) = (/^\s*\[([^]]*)\]/ && (! $`));
local($opt1,$dummy)= &get_next_optional_argument;
local($opt2,$dummy)= &get_next_optional_argument;
if ($dummy) {
($opt1,$opt2) = ($opt2,$opt1);
};
($hasopt,$opt1,$opt2)
}
}
sub do_cite_keys{
local($br_id,$hasopt,$first,$second,$c_mark,$cite_key) = @_;
local(@cite_keys) = (split(/,/,$cite_key));
local ($multiple,$cite_anchor,$key,$extra);
if (($CITEINDEX) && (! $NUMERIC)) {
foreach $key (@cite_keys) {$cite_anchor=&make_cite_index("$br_id",$key);};};
if ($
else { $multiple = '';};
local($citauth)=($c_mark =~ /($cite_author_mark|$cite_author_full_mark)/);
$first = "$POST_NOTE $first" if ($first && !($HARVARD && $citauth));
grep ( do { &cite_check_segmentation($_);
if (($first && !$multiple) &&
(($HARVARD &&!$hasopt)||($c_mark =~ /citet/))) {
$extra = $first; $first = '';
} else { $extra = '' }
$_ = "
, @cite_keys);
$second .= ' ' if ($second);
local($this_cite);
if ($hasopt) {
$this_cite = join('', $CITE_OPEN_DELIM, $second,$multiple
, join($CITE_ENUM,@cite_keys)
, (($first&&($c_mark =~/^($citet_mark|$citet_full_mark)$/))?
$first.'
, $CITE_CLOSE_DELIM
);
} else {
$this_cite = join ('',$second,$multiple
, join($CITE_ENUM,@cite_keys)
, (($first&&($c_mark =~/^($citet_mark|$citet_full_mark)$/))?
$first.'
);
}
join ('',$cite_anchor,$this_cite);
}
sub make_cite_index {
local ($br_id,$cite_key) =@_;
local ($index_key)="$cite_short{$cite_key} ($cite_year{$cite_key})";
local ($sort_key)="$cite_short{$cite_key}$cite_year{$cite_key}$cite_key";
if (defined  &named_index_entry ) {
&named_index_entry($br_id,"$sort_key\@$index_key") }
elsif ($br_id > 0) {
&do_cmd_index("$OP$br_id$CP$index_key$OP$br_id$CP") }
else { $name++; &do_cmd_index("$OP$name$CP$index_key$OP$name$CP") }
}
sub parse_citeauthoryear {
local($_) = @_;
s/$comment_mark\d+.*\n//gs;
s/\n//gs;
my ($long,$short,$year);
s/^\\protect\\citeauthoryear//;
$long = &missing_braces unless (
(s/$next_pair_pr_rx/$long=$2;''/eo)
||(s/$next_pair_rx/$long=$2;''/eo));
$long =~ s/($O|$OP)(\d+)($C|$CP)($O|$OP)\2($C|$CP)//go;
$short = &missing_braces unless (
(s/$next_pair_pr_rx/$short=$2;''/eo)
||(s/$next_pair_rx/$short=$2;''/eo));
$short =~ s/($O|$OP)(\d+)($C|$CP)($O|$OP)\2($C|$CP)//go;
$year = &missing_braces unless (
(s/$next_pair_pr_rx/$year=$2;''/eo)
||(s/$next_pair_rx/$year=$2;''/eo));
$year =~ s/($O|$OP)(\d+)($C|$CP)($O|$OP)\2($C|$CP)//go;
($long,$short,$year);
}
sub do_cmd_citeauthoryear {
local($_) = @_;
my ($long,$short,$year) = parse_citeauthoryear($_);
join('', "$short($year)$long",$_);
}
sub do_real_bibitem {
local($thisfile, $_) = @_;
local ($tmp,$label);
$bbl_cnt++;
local($label, $dummy) = &get_next_optional_argument;
local($short, $year, $long, $supported);
if ($label =~ /^\\protect\\citeauthoryear/) {
($long,$short,$year)=parse_citeauthoryear($label);
$supported=1;
} else {
$tmp = ($label =~ /([^\(]*)(\([^\)]*\))([\w\W]*)$/s);
($supported) = ($tmp && !($label =~ /\\protect/));
($short, $year, $long) = ($1,$2,($3 ? $3 : $1));
}
if (! $NUMERIC) { $year =~ s/[\(\)]//g; }
else { $label=++$bibitem_counter; };
$year =~ s/[\(\)]//g;
$year =~ s/($O|$OP)\d+($C|$CP)//g;
$cite_key = &missing_braces unless (
(s/$next_pair_pr_rx/$cite_key=$2;''/eo)
||(s/$next_pair_rx/$cite_key=$2;''/eo));
$cite_key = &translate_commands($2);
if ($cite_key) {
$tmp = $_;
$_ = $short;
s/$next_pair_pr_rx//o;
if (!($2 eq $cite_key))
{$short =$2; $short =~ s/$OP[^\
$_ = $long;
s/$next_pair_pr_rx//o;
if (!($2 eq $cite_key))
{$long = $2; $long =~ s/$OP[^\
$_ = "$tmp";
if ($supported) {
$cite_short{$cite_key} = &translate_commands($short);
$cite_year{$cite_key} = &translate_commands($year);
$cite_long{$cite_key} = &translate_commands($long)}
else {
&write_warnings(
"\n\\bibitem label format not supported, using \\bibcite information!");
}
if (!($ref_files{'cite_'."$cite_key"} eq $thisfile)) {
$ref_files{'cite_'."$cite_key"} = $thisfile;
$changed = 1; }
$citefiles{$cite_key} = $thisfile;
$_=&make_cite_reference ($cite_key,$_);
} else {
$label = &bibitem_style($label) if (defined &bibitem_style);
print "Cannot find bibitem labels: $label\n";
$_=join('',"\n<DT>$label\n<DD>", $_);
}
$_;
}
sub make_cite_reference {
local ($cite_key,$_)=@_;
local($label)=$cite_info{$cite_key};
local($next_lines, $after_lines);
local($sort_key, $indexdata);
if (defined  &named_index_entry ) {
$sort_key = "$cite_short{$cite_key}$cite_year{$cite_key}$cite_key";
$sort_key =~ tr/A-Z/a-z/;
} else {$sort_key = "$cite_short{$cite_key} ($cite_year{$cite_key})";}
if ($index{$sort_key}) {
$indexdata = $index{$sort_key};
$indexdata =~ s/[\|] $//;
$indexdata = join('',"\n<DD>cited: ", "$indexdata");
$index{$sort_key} = '';
if ($CITEINDEX) { &make_cite_index("$cite_key",$cite_key);}
elsif (defined  &named_index_entry ) {$printable_key{$sort_key} = '';}
} else { $indexdata = '';}
$indexdata .= "\n<P>";
local ($found) = /(\\bibitem|\\harvarditem)/o;
if ($found) { $after_lines = $&.$'; $next_lines = $`;}
else { $after_lines = ''; $next_lines = $_;}
$next_lines .= $indexdata;
$indexdata = '';
$_ = $next_lines.$after_lines;
if ($NUMERIC) {
if (defined &bibitem_style) {
$label = &bibitem_style($label);
} else {
$label = '<STRONG>'.$label.'</STRONG>';
};
join('',"\n<DT><A ID=\"$cite_key\">$label</A>\n<DD>",$_);
} else {
$found = /\<BR\>/o;
local($nbefore,$nafter) = ($`,$');
if ($found) {
if (defined &bibitem_style) {
$nbefore = &bibitem_style($nbefore);
} elsif ($nbefore =~/\\/) {
$nbefore = &translate_commands($nbefore);
} else {
$nbefore = join('','<STRONG>',$nbefore,'</STRONG>');
}
join('',"\n<DT><A ID=\"$cite_key\">", $nbefore
, "</A>\n<DD>", &translate_commands($nafter));
} else {
$found= /(\\bibitem|\\harvarditem)/o;
if ($found) {
local($nbefore,$nafter) = ($`,$');
if (defined &bibitem_style) {
$nbefore = &bibitem_style($nbefore);
} elsif ($nbefore =~/\\/) {
$nbefore = &translate_commands($nbefore);
} else {
$nbefore = join('','<STRONG>',$nbefore,'</STRONG>');
}
join('',"\n<DT><A ID=\"$cite_key\">", $nbefore
,"</A>\n<DD>", $nafter );
} else {
if (defined &bibitem_style) {
$_ = &bibitem_style($_);
} elsif ($_ =~ /\\/) {
$_ = &translate_commands($_);
} else {
$_ = join('','<STRONG>',$_,'</STRONG>');
}
join('',"\n<DT><A ID=\"$cite_key\">", $_,"</A>\n<DD>",' ');
};
};
}
}
if (!(defined &do_cmd_harvarditem)) {
eval 'sub do_cmd_harvarditem { &do_real_harvarditem($CURRENT_FILE, @_) }';
} else {
print "\n *** sub do_cmd_harvarditem  is already defined. ***\n"
}
sub do_real_harvarditem {
local ($thisfile,$_)=@_;
local ($dum,$short)=&get_next_optional_argument;
$short =~ s/[\[\]]//g;
$bbl_cnt++;
s/$next_pair_pr_rx//o; local ($long)=$2;
s/$next_pair_pr_rx//o; local ($year)=$2;
$year =~ s/<
s/$next_pair_pr_rx//o; local ($cite_key)=$2;
if ($cite_key) {
if (!($short)) {$short=$long};
local($tmp) = $_;
$_ = $short;
s/$next_pair_pr_rx//o;
if (!($2 eq $cite_key))
{$short =$2; $short =~ s/<\
$_ = $long;
s/$next_pair_pr_rx//o;
if (!($2 eq $cite_key))
{$long = $2; $long =~ s/<\
$_ = "$tmp";
$cite_short{$cite_key} = &translate_commands($short);
$cite_year{$cite_key} = &translate_commands($year);
$cite_long{$cite_key} = &translate_commands($long);
if (!($ref_files{'cite_'."$cite_key"} eq $thisfile)) {
$ref_files{'cite_'."$cite_key"} = $thisfile;
$changed = 1; }
$citefiles{$cite_key} = $thisfile;
&make_harvard_reference ($cite_key,$year,$_);
} else {
$label = &bibitem_style($label) if (defined &bibitem_style);
print "Cannot find bibitem labels: $label\n";
join('',"\n<DT><STRONG>$label</STRONG>\n<DD>", $_);
}
}
sub make_harvard_reference {
local ($cite_key,$year,$_)=@_;
local($label)=$cite_info{$cite_key};
local($next_lines, $after_lines);
local($sort_key, $indexdata);
if (defined  &named_index_entry ) {
$sort_key = "$cite_short{$cite_key}$cite_year{$cite_key}$cite_key";
$sort_key =~ tr/A-Z/a-z/;
} else {$sort_key = "$cite_short{$cite_key} ($cite_year{$cite_key})";}
if ($index{$sort_key}) {
$indexdata = $index{$sort_key};
$indexdata =~ s/[\|] $//;
$indexdata = join('',"\n<DD>cited: ", "$indexdata");
$index{$sort_key} = '';
if ($CITEINDEX) { &make_cite_index("$cite_key",$cite_key);}
elsif (defined  &named_index_entry ) {$printable_key{$sort_key} = '';}
} else { $indexdata = '';}
$indexdata .= "\n<P>";
local ($found) = /(\\bibitem|\\harvarditem)/o;
if ($found) { $after_lines = $&.$'; $next_lines = $`;}
else { $after_lines = ''; $next_lines = $_;}
$next_lines .= $indexdata;
$indexdata = '';
$_ = $next_lines.$after_lines;
if ($NUMERIC) {
$label = &bibitem_style($label) if (defined &bibitem_style);
join('',"\n<DT><A ID=\"$cite_key\"><STRONG>$label</STRONG></A>\n<DD>",$_);
} else {
$year =~ /\d+/;
local($numyear) = $&;
local ($found)= /$numyear(.*?)[.,:;\n]/s;
if ($found) {
join('',"\n<DT><A ID=\"$cite_key\"><STRONG>",
&translate_commands($`.$&),"</STRONG></A>\n<DD>",
$')
} else {
$found= /(\\bibitem|\\harvarditem)/o;
if ($found) {
join('',"\n<DT><A ID=\"$cite_key\"><STRONG>",
&translate_commands($`),"</STRONG></A>\n<DD>",
$');
} else {
join('',"\n<DT><A ID=\"$cite_key\"><STRONG>",
&translate_commands($_),"</STRONG></A>\n<DD>",' ');
};
};
}
}
sub do_cmd_harvardand {
&translate_commands("$HARVARDAND".$_[0]);
}
sub do_cmd_harvardleft {
&translate_commands("$CITE_OPEN_DELIM".$_[0]);
}
sub do_cmd_harvardright {
&translate_commands("$CITE_CLOSE_DELIM".$_[0]);
}
sub do_cmd_harvardyearleft {
&translate_commands("$CITE_OPEN_DELIM".$_[0]);
}
sub do_cmd_harvardyearright {
&translate_commands("$CITE_CLOSE_DELIM".$_[0]);
}
sub do_cmd_harvardurl{
local($_) = @_;
local($text, $url, $href);
local($name, $dummy) = &get_next_optional_argument;
$url = &missing_braces unless (
(s/$next_pair_pr_rx/$url = $2;''/eo)
||(s/$next_pair_rx/$url = $2;''/eo));
$url = &translate_commands($url) if ($url=~/\\/);
$text = "<b>URL:</b> ".$url;
if ($name) { $href = &make_named_href($name,$url,$text) }
else { $href = &make_href($url,$text) }
print "\nHREF:$href" if ($VERBOSITY > 3);
$_ =~ s/^[ \t]*\n?/\n/;
join ('',$href,$_);
}
sub do_cmd_bibcite {
local($_) = @_;
s/$next_pair_pr_rx//o;
local($br_id, $cite_key) = ($1, $2);
s/$next_pair_pr_rx//o;
local($br_id, $print_key) = ($1, $2);
local($rest) = "$_";
$_ = $print_key;
s/$next_pair_pr_rx//o;
($br_id, $print_key) = ($1, $2);
$print_key =~ s/<\
print ("\nWARNING: natbib.perl: no valid citation key found in \bibitem.",
"\n    Perhaps you are running a natbib.sty version earlier than 6.x?",
"\n    Unable to generate citation references correctly.\n")
if (! $print_key);
$cite_info{$cite_key} = &translate_commands($print_key);
s/$next_pair_pr_rx//o;
($br_id, $print_key) = ($1, $2);
$print_key =~ s/<\
$cite_year{$cite_key} = &translate_commands($print_key);
s/$next_pair_pr_rx//o;
($br_id, $print_key) = ($1, $2);
$print_key =~ s/<\
$cite_short{$cite_key} = &translate_commands($print_key);
s/$next_pair_pr_rx//o;
($br_id, $print_key) = ($1, $2);
$print_key =~ s/<\
if ($print_key) {
$cite_long{$cite_key} = &translate_commands($print_key);}
else {$cite_long{$cite_key}=$cite_short{$cite_key}};
$NUMERIC=($NUMERIC ||
(! $cite_short{$cite_key}) ||
(! $cite_year{$cite_key}));
$rest;
}
sub do_cmd_harvardcite {
local($_) = @_;
s/$next_pair_pr_rx//o;
local($br_id, $cite_key) = ($1, $2);
s/$next_pair_pr_rx//o;
$cite_long{$cite_key}=&translate_commands($2);
s/$next_pair_pr_rx//o;
$cite_short{$cite_key}=&translate_commands($2);
s/$next_pair_pr_rx//o;
$cite_year{$cite_key}=&translate_commands($2);
$cite_year{$cite_key} =~ s/<
$_;
}
sub replace_cite_references_hook {
local($target) = 'contents';
if (/$cite_multiple_mark/) {&replace_multiple_cite_references };
&replace_nat_cite_references if
/$cite_mark|$cite_full_mark|$cite_year_mark|$cite_par_mark|$cite_par_full_mark|$cite_author_mark|$cite_author_full_mark|$citealt_mark|$citealt_full_mark|$citealp_mark|$citealp_full_mark|$citet_mark|$citet_full_mark/;
}
sub replace_multiple_cite_references {
local($saved) = $_ ;
while (s/$cite_multiple_mark(.*?)$cite_multiple_mark/&do_multiple_citation($1)/se) {
last if ($_ eq $saved);
$saved = $_;
};
undef $saved;
}
sub do_multiple_citation {
local($cit)=@_;
local($before_year,$after_year);
local($author,$thisyear,$lastyear,$lastauth,$theauth,$year);
local($thetext,$lasttext,$thekey,$lastkey);
local($mark,$key,$extra,$citet_ext,%second,@sorted);
local($useindex) = $NUMERIC;
undef %second;
undef @sorted;
while ($cit =~
s/
$mark=$2;
$extra=$3;
$citet_ext = $6 if (($mark eq $citet_mark)||($mark eq $citet_full_mark));
($key=$1) =~ s/[\s]//g;
%second=(%second,$key,$extra.$citet_ext);
};
if (0){
@sorted = keys (%second);
@sorted=sort {$cite_info{$a} cmp $cite_info{$b}} @sorted if $SORT_MULTIPLE;
$_=join($CITE_ENUM,
map { &make_href("$citefiles{$_}
@sorted);
} else {
SWITCH:	{
$mark =~ /^$cite_par_mark|$cite_par_full_mark/ && do {
if ($NUMERIC) {
($before_year,$after_year)=('','');
} else {
($before_year,$after_year)=($BEFORE_PAR_YEAR,'');
}
last SWITCH;};
$mark =~ /^$cite_mark|$cite_full_mark/ && do {
($before_year,$after_year)=
(" $CITE_OPEN_DELIM","$CITE_CLOSE_DELIM");
last SWITCH;};
$mark =~ /^$citet_mark|$citet_full_mark/ && do {
($before_year,$after_year) =
(" $CITE_OPEN_DELIM","$CITE_CLOSE_DELIM");
last SWITCH;};
$mark =~ /^$citealp_mark|$citealp_full_mark/ && do {
($before_year,$after_year)=($BEFORE_PAR_YEAR,'');
last SWITCH;};
$mark =~ /^$cite_year_mark/ && do {
($before_year,$after_year)=(' ','');
$useindex=0;
last SWITCH;};
($before_year,$after_year)=(' ','');
}
if ($NUMERIC && $mark =~ /^$cite_par_mark|$cite_par_full_mark/) {
$author='';
} elsif ($mark =~
/^$cite_par_full_mark|$cite_full_mark|$citet_full_mark|$citealt_full_mark|$citealp_full_mark|$cite_author_full_mark/)
{ $author=\%cite_long;
} else { $author=\%cite_short; }
@sorted = keys (%second);
@sorted = sort {$$author{$a}.$cite_year{$a} cmp $$author{$b}.$cite_year{$b}}
@sorted if $SORT_MULTIPLE;
$lastkey=shift(@sorted);
($lastauth,$lastyear)=($$author{$lastkey},$cite_year{$lastkey});
$lasttext=join(''
, (($mark =~ /$cite_year_mark/)? '' : $$author{$lastkey})
, (($mark =~ /$cite_author_mark|$cite_author_full_mark/)? ''
: $before_year
. ($useindex ? $cite_info{$lastkey}:$cite_year{$lastkey}))
, $second{$lastkey}
);
$_='';
while ($thekey=shift(@sorted)) {
($theauth,$theyear)=($$author{$thekey},
($useindex ? $cite_info{$thekey}:$cite_year{$thekey}));
if ($lastauth eq $theauth) {
$lastyear =~ /^\d+/;
$year=$&;
$thetext=($theyear =~ /^$year/ ? $' : ' '.$theyear);
$thetext=' '.$theyear unless ($thetext);
$_=join('',
$_,
&make_href("$citefiles{$lastkey}
$lasttext),
$COMMON_AUTHOR_SEP);
} else {
$lasttext=$lasttext.$after_year;
$thetext=join(''
, (($mark =~ /$cite_year_mark/)? '' : $$author{$thekey})
, (($mark =~ /$cite_author_mark|$cite_author_full_mark/)? ''
: $before_year
. ($useindex ? $cite_info{$thekey}:$cite_year{$thekey}))
, $second{$thekey}
);
$_=join('',
$_,
&make_href("$citefiles{$lastkey}
$lasttext),
$CITE_ENUM);
};
($lastkey,$lastauth,$lastyear,$lasttext)=
($thekey,$theauth,$theyear,$thetext);
};
$_=join('',$_,
&make_href("$citefiles{$lastkey}
$lasttext.$after_year));
};
$_;
}
sub replace_nat_cite_references {
local($savedRS) = $/; $/='';
if ($NUMERIC) {
s/
,"$citefiles{$1}
s/
,"$citefiles{$1}
,"$cite_short{$1} $CITE_OPEN_DELIM"."$cite_info{$1}$CITE_CLOSE_DELIM")/ge;
s/
,"$cite_long{$1} $CITE_OPEN_DELIM"."$cite_info{$1}$CITE_CLOSE_DELIM")/ge;
s/
,"$cite_year{$1}$2")/ge;
s/
,"$cite_short{$1}".($2? " $CITE_OPEN_DELIM$2$CITE_CLOSE_DELIM": ""))/ge;
s/
,"$cite_long{$1}".($2? " $CITE_OPEN_DELIM$2$CITE_CLOSE_DELIM": ""))/ge;
s/
&make_named_href(""
, "$citefiles{$1}
, join(''
,"$cite_short{$1} $CITE_OPEN_DELIM$cite_info{$1}$2"
, ($3 ? $BEFORE_PAR_YEAR.$4 : ''), $CITE_CLOSE_DELIM)
)
/ge;
s/
&make_named_href(""
, "$citefiles{$1}
, join(''
,"$cite_long{$1} $CITE_OPEN_DELIM$cite_info{$1}$2"
, ($3 ? $BEFORE_PAR_YEAR.$3 : ''), $CITE_CLOSE_DELIM)
)
/ge;
s/
,"$citefiles{$1}
s/
,"$citefiles{$1}
} else {
s/
,"$cite_short{$1} ". "$CITE_OPEN_DELIM$cite_year{$1}$2$CITE_CLOSE_DELIM")/ge;
s/
,"$cite_long{$1} "."$CITE_OPEN_DELIM$cite_year{$1}$2$CITE_CLOSE_DELIM")/ge;
if ($HARVARD) {
s/
,"$citefiles{$1}
,"$cite_short{$1}\'s "."$CITE_OPEN_DELIM$cite_year{$1}$2$CITE_CLOSE_DELIM")/ge;
s/
,"$cite_long{$1}\'s "."$CITE_OPEN_DELIM$cite_year{$1}$2$CITE_CLOSE_DELIM")/ge
} else {
s/
,"$citefiles{$1}
s/
,"$citefiles{$1}
}
s/
,"$citefiles{$1}
s/
,"$citefiles{$1}
s/
&make_named_href(""
, "$citefiles{$1}
, join(''
,"$cite_short{$1} $CITE_OPEN_DELIM$cite_year{$1}$2"
, ($3 ? $BEFORE_PAR_YEAR.$4 : ''), $CITE_CLOSE_DELIM)
)
/ge;
s/
&make_named_href(""
, "$citefiles{$1}
, join(''
,"$cite_long{$1} $CITE_OPEN_DELIM$cite_year{$1}$2"
, ($3 ? $BEFORE_PAR_YEAR.$4 : ''), $CITE_CLOSE_DELIM)
)
/ge;
s/
"$citefiles{$1}
s/
"$citefiles{$1}
s/
,"$cite_year{$1}$2")/ge;
s/
,"$cite_short{$1}".($2? " $CITE_OPEN_DELIM$2$CITE_CLOSE_DELIM": ""))/ge;
s/
,"$cite_long{$1}".($2? " $CITE_OPEN_DELIM$2$CITE_CLOSE_DELIM": ""))/ge;
}
$/ = $savedRS;
}
sub cite_check_segmentation {
local($c_key)=@_;
if  ($ref_files{"cite_$c_key"})  {
$citefiles{$c_key} = $ref_files{"cite_$c_key" };
};
$citefiles{$c_key};
}
sub do_env_thebibliography {
local($_) = @_;
$bibitem_counter = 0;
$citefile = $CURRENT_FILE;
$citefiles{$bbl_nr} = $citefile;
s/$next_pair_rx//o;
s/\\newblock/\<BR\>/gm;
s/\\penalty\d+//mg;
local($this_item,$this_kind, $title);
s/\\(bibitem|harvarditem)/$this_kind=$1;''/eo;
$_ = $';
local(@bibitems) = split(/\\(bib|harvard)item/, $_);
while (@bibitems) {
$this_item = shift (@bibitems);
$this_item =~ s/$par_rx\s*$/\n/;
$this_item = &translate_environments("\\$this_kind $this_item\\newblock");
$citations .= &translate_commands($this_item);
last unless  (@bibitems);
$this_kind = shift (@bibitems).'item';
}
$citations = join('',"\n<DL class=\"COMPACT\">",$citations,"\n</DL>");
$citations{$bbl_nr} = $citations;
$title = &make_bibliography_title();
$_ = join('','<P>' , "\n<H2><A ID=\"SECTIONREF\">"
, "$title</A>\n</H2>\n$bbl_mark
$bbl_nr++ if $bbl_cnt > 1;
$_;
}
sub do_cmd_bibpunct {
local($_) = @_;
local($post, $dummy) = &get_next_optional_argument;
$POST_NOTE=$post." " if ($post);
s/$next_pair_pr_rx//o;
$CITE_OPEN_DELIM=$2;
s/$next_pair_pr_rx//o;
$CITE_CLOSE_DELIM=$2;
s/$next_pair_pr_rx//o;
$CITE_ENUM=$2." " if ($2);
s/$next_pair_pr_rx//o;
local($style)=$2;
$NUMERIC=($style =~ /[ns]/);
s/$next_pair_pr_rx//o;
$BEFORE_PAR_YEAR=$2." " if ($2);
s/$next_pair_pr_rx//o;
$COMMON_AUTHOR_SEP=$2;
$_;
}
sub do_cmd_citeindexfalse {
$CITEINDEX=0; $_[0];
}
sub do_cmd_citeindextrue {
$CITEINDEX=1; $_[0];
}
sub do_cmd_citestyle {
local($_) = @_;
s/$next_pair_pr_rx//o;
local($style)="citestyle_$2";
if (@$style) {
($CITE_OPEN_DELIM,
$CITE_CLOSE_DELIM,
$CITE_ENUM,
$NUMERIC,
$BEFORE_PAR_YEAR,
$COMMON_AUTHOR_SEP)=@$style;
$NUMERIC=($NUMERIC =~ /[sn]/);
local($and)="HARVARDAND_$2";
defined $$and && do { $HARVARDAND=$$and }
} else { print "\nnatbib.perl: invalid argument to \\citestyle!" };
$_;
}
sub do_cmd_citationstyle {
&do_cmd_citestyle
}
&do_require_package('babelbst');
&ignore_commands ( <<_IGNORED_CMDS_);
bibsection
bibfont
bibhang
bibsep
citeindextype
harvardyearparenthesis
_IGNORED_CMDS_
1;
