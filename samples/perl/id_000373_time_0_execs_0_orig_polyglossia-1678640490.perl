package main;
sub load_babel_package {
local($dir) = '';
local($orig_cwd) = ($orig_cwd ? $orig_cwd : '.');
if (-f "$orig_cwd${dd}babel.perl") {
if (require("$orig_cwd${dd}babel.perl")) {
print "\nLoading $orig_cwd${dd}babel.perl";
return;
}
}
foreach $dir (split(/$envkey/,$LATEX2HTMLSTYLES)) {
if (-f "$dir${dd}babel.perl") {
if (require("$dir${dd}babel.perl")) {
print "\nLoading $dir${dd}babel.perl";
return;
}
}
}
}
sub load_luainputenc_package {
local($dir) = '';
local($orig_cwd) = ($orig_cwd ? $orig_cwd : '.');
if (-f "$orig_cwd${dd}luainputenc.perl") {
if (require("$orig_cwd${dd}luainputenc.perl")) {
print "\nLoading $orig_cwd${dd}luainputenc.perl";
return;
}
}
foreach $dir (split(/$envkey/,$LATEX2HTMLSTYLES)) {
if (-f "$dir${dd}luainputenc.perl") {
if (require("$dir${dd}luainputenc.perl")) {
print "\nLoading $dir${dd}luainputenc.perl";
return;
}
}
}
}
sub do_cmd_setdefaultlanguage {
local($_) = @_;
local($dum, $lang);
($dum,$lang) = &get_next_optional_argument;
$lang = &missing_braces unless(
(s/$next_pair_pr_rx/$lang=$2;''/eo)
||(s/$next_pair_rx/$lang=$2;''/eo));
local($trans) = "${lang}_translation";
local($titles) = "${lang}_titles";
local($encoding) = "${lang}_encoding";
print ("\nPolyglossia primary language:");
&load_babel_file($lang);
if (defined &$trans) {
if ($PREAMBLE) {
&make_language_rx;
$TITLES_LANGUAGE = $lang;
$default_language = $lang;
$CHARSET = $$encoding if ($$encoding);
if (defined &$titles) {
eval "&$titles()";
&translate_titles;
}
local($lcode) = $iso_languages{$lang};
&add_to_body('LANG',$lcode) unless ($HTML_VERSION < 4);
local($code) = 'sub do_cmd_text'.$lang.'{'             . "\n"
. 'local($_) = @_;'                                  . "\n"
. 'local($dum1,$dum2);'                              . "\n"
. '($dum1,$dum2) = &get_next_optional_argument;'     . "\n"
. 'local($text,$br_id)=("","0");'                    . "\n"
. '$text = &missing_braces unless('                  . "\n"
. '  (s/$next_pair_pr_rx/$text=$2;$br_id=$1;""/eo)'  . "\n"
. '  ||(s/$next_pair_rx/$text=$2;$br_id=$1;""/eo));' . "\n"
. 'join("",&translate_commands('                     . "\n"
. '&translate_environments("$O$br_id$C\\\\'.$lang.'TeX $text$O$br_id$C")),' . "\n"
. '$_);'                                             . "\n"
. '}'                                                . "\n"
. 'sub do_env_'.$lang.'{'                            . "\n"
. 'local($_) = @_;'                                  . "\n"
. 'local($dum1,$dum2);'                              . "\n"
. '($dum1,$dum2) = &get_next_optional_argument;'     . "\n"
. 'local($br_id) = ++$global{"max_id"};'             . "\n"
. '$_ = &translate_environments("$O$br_id$C\\\\'.$lang.'TeX $_$O$br_id$C");' . "\n"
. '$_ = &translate_commands($_);'                    . "\n"
. '$_;'                                              . "\n"
. '}'                                                . "\n";
eval $code;
}
} else { &no_lang_support($lang) }
$_;
}
sub do_cmd_setmainlanguage {
&do_cmd_setdefaultlanguage($_[0]);
}
sub do_cmd_resetdefaultlanguage {
&do_cmd_setdefaultlanguage($_[0]);
}
sub do_cmd_setotherlanguage {
local($_) = @_;
local($dum, $lang);
($dum,$lang) = &get_next_optional_argument;
$lang = &missing_braces unless(
(s/$next_pair_pr_rx/$lang=$2;''/eo)
||(s/$next_pair_rx/$lang=$2;''/eo));
local($trans) = "${lang}_translation";
local($titles) = "${lang}_titles";
local($encoding) = "${lang}_encoding";
local($save_tit_lang, $save_def_lang, $save_charset) = ('', '', '');
if ($PREAMBLE) {
$save_tit_lang = $TITLES_LANGUAGE  if defined $TITLES_LANGUAGE;
$save_def_lang = $default_language if defined $default_language;
$save_charset  = $CHARSET          if defined $CHARSET;
}
print ("\nPolyglossia secondary language:");
&load_babel_file($lang);
if (defined &$trans) {
if ($PREAMBLE) {
&make_language_rx;
$TITLES_LANGUAGE = $lang;
$default_language = $lang;
$CHARSET = $$encoding if ($$encoding);
if (defined &$titles) {
eval "&$titles()";
&translate_titles;
}
local($code) = 'sub do_cmd_text'.$lang.'{'             . "\n"
. 'local($_) = @_;'                                  . "\n"
. 'local($dum1,$dum2);'                              . "\n"
. '($dum1,$dum2) = &get_next_optional_argument;'     . "\n"
. 'local($text,$br_id)=("","0");'                    . "\n"
. '$text = &missing_braces unless('                  . "\n"
. '  (s/$next_pair_pr_rx/$text=$2;$br_id=$1;""/eo)'  . "\n"
. '  ||(s/$next_pair_rx/$text=$2;$br_id=$1;""/eo));' . "\n"
. 'join("",&translate_commands('                     . "\n"
. '&translate_environments("$O$br_id$C\\\\'.$lang.'TeX $text$O$br_id$C")),' . "\n"
. '$_);'                                             . "\n"
. '}'                                                . "\n"
. 'sub do_env_'.$lang.'{'                            . "\n"
. 'local($_) = @_;'                                  . "\n"
. 'local($dum1,$dum2);'                              . "\n"
. '($dum1,$dum2) = &get_next_optional_argument;'     . "\n"
. 'local($br_id) = ++$global{"max_id"};'             . "\n"
. '$_ = &translate_environments("$O$br_id$C\\\\'.$lang.'TeX $_$O$br_id$C");' . "\n"
. '$_ = &translate_commands($_);'                    . "\n"
. '$_;'                                              . "\n"
. '}'                                                . "\n";
eval $code;
$CHARSET = $save_charset if $save_charset  ne '';
if ($save_tit_lang ne '' || $save_def_lang ne '') {
$lang = $save_tit_lang || $save_def_lang;
$TITLES_LANGUAGE = $lang;
$default_language = $lang;
$trans = "${lang}_translation";
$titles = "${lang}_titles";
&make_language_rx if defined &$trans;
if (defined &$titles) {
eval "&$titles()";
&translate_titles;
}
}
}
} else { &no_lang_support($lang) }
$_;
}
sub do_cmd_setotherlanguages {
local($_) = @_;
local(@langs, $lang, $br_id);
$lang = &missing_braces unless(
(s/$next_pair_pr_rx/$lang=$2;''/eo)
||(s/$next_pair_rx/$lang=$2;''/eo));
@langs = split /,/, $lang;
foreach $lang (@langs) {
$br_id = ++$global{'max_id'};
&do_cmd_setotherlanguage("$O$br_id$C$lang$O$br_id$C");
}
$_;
}
&load_luainputenc_package();
&load_babel_package();
&process_commands_wrap_deferred (<<_RAW_ARG_DEFERRED_CMDS_);
textenglish
textgerman
textrussian
_RAW_ARG_DEFERRED_CMDS_
$POLYGLOSSIA = 1;
1;
