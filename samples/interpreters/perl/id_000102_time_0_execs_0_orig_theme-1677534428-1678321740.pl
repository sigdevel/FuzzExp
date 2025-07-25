$WRAPPER_OPEN = 0;
$COLUMNS_WRAPPER_OPEN = 0;
sub theme_ui_post_header
{
my ($text) = @_;
my $rv;
$rv .= "<div class='ui_post_header'>$text</div>\n" if (defined($text));
$rv .= "<p></p>" if (!defined($text));
return $rv;
}
sub theme_ui_pre_footer
{
my $rv;
$rv .= "<p></p>\n";
return $rv;
}
sub theme_ui_print_footer
{
local @args = @_;
print &ui_pre_footer();
&footer(@args);
}
sub theme_icons_table
{
my ($i, $need_tr);
my $cols = $_[3] ? $_[3] : 4;
my $per = int(100.0 / $cols);
print "<div class='wrapper'>\n";
print "<table id='main' width=100% cellpadding=5 class='icons_table'>\n";
for($i=0; $i<@{$_[0]}; $i++) {
if ($i%$cols == 0) { print "<tr>\n"; }
print "<td width=$per% align=center valign=top>\n";
&generate_icon($_[2]->[$i], $_[1]->[$i], $_[0]->[$i],
$_[4], $_[5], $_[6], $_[7]->[$i], $_[8]->[$i]);
print "</td>\n";
if ($i%$cols == $cols-1) { print "</tr>\n"; }
}
while($i++%$cols) { print "<td width=$per%></td>\n"; $need_tr++; }
print "</tr>\n" if ($need_tr);
print "</table>\n";
print "</div>\n";
}
sub theme_generate_icon
{
my $w = !defined($_[4]) ? "width=48" : $_[4] ? "width=$_[4]" : "";
my $h = !defined($_[5]) ? "height=48" : $_[5] ? "height=$_[5]" : "";
if ($tconfig{'noicons'}) {
if ($_[2]) {
print "$_[6]<a href=\"$_[2]\" $_[3]>$_[1]</a>$_[7]\n";
}
else {
print "$_[6]$_[1]$_[7]\n";
}
}
elsif ($_[2]) {
print "<table><tr><td width=48 height=48>\n",
"<a href=\"$_[2]\" $_[3]><img src=\"$_[0]\" alt=\"\" border=0 ",
"$w $h></a></td></tr></table>\n";
print "$_[6]<a href=\"$_[2]\" $_[3]>$_[1]</a>$_[7]\n";
}
else {
print "<table><tr><td width=48 height=48>\n",
"<img src=\"$_[0]\" alt=\"\" border=0 $w $h>",
"</td></tr></table>\n$_[6]$_[1]$_[7]\n";
}
}
sub theme_post_save_domain
{
local ($d, $action) = @_;
print "<script>\n";
if ($action eq 'create') {
print "top.left.location = '$gconfig{'webprefix'}/left.cgi?dom=$d->{'id'}';\n";
}
else {
print "top.left.location = top.left.location;\n";
}
print "</script>\n";
}
sub theme_post_save_domains
{
print "<script>\n";
print "top.left.location = top.left.location;\n";
print "</script>\n";
}
sub theme_post_save_server
{
local ($s, $action) = @_;
if ($action eq 'create' || $action eq 'delete' ||
!$done_theme_post_save_server++) {
print "<script>\n";
print "top.left.location = top.left.location;\n";
print "</script>\n";
}
}
sub theme_select_server
{
local ($server) = @_;
print <<EOF;
<script>
if (window.parent && window.parent.frames[0]) {
var leftdoc = window.parent.frames[0].document;
var leftform = leftdoc.forms[0];
if (leftform) {
var serversel = leftform['sid'];
if (serversel && serversel.value != '$server->{'id'}' ||
!serversel) {
//if (serversel) {
//	// Need to change value of selector
//	serversel.value = '$server->{'id'}';
//	}
window.parent.frames[0].location = '$gconfig{'webprefix'}/left.cgi?mode=vm2&sid=$server->{'id'}';
}
}
}
</script>
EOF
}
sub theme_select_domain
{
local ($d) = @_;
print <<EOF;
<script>
if (window.parent && window.parent.frames[0]) {
var leftdoc = window.parent.frames[0].document;
var leftform = leftdoc.forms[0];
if (leftform) {
var domsel = leftform['dom'];
if (domsel && domsel.value != '$d->{'id'}') {
// Need to change value
// domsel.value = '$d->{'id'}';
window.parent.frames[0].location = '$gconfig{'webprefix'}/left.cgi?mode=virtualmin&dom=$d->{'id'}';
}
}
}
</script>
EOF
}
sub theme_post_save_folder
{
local ($folder, $action) = @_;
my $ref;
if ($action eq 'create' || $action eq 'delete' || $action eq 'modify') {
$ref = 1;
}
else {
if (defined(&mailbox::should_show_unread) &&
&mailbox::should_show_unread($folder)) {
$ref = 1;
}
}
if ($ref) {
print "<script>\n";
print "top.frames[0].document.location = top.frames[0].document.location;\n";
print "</script>\n";
}
}
sub theme_post_change_modules
{
print <<EOF;
<script type='text/javascript'>
var url = '' + top.left.location;
if ( url.match(/mode=.*/) ) {
if ( url.indexOf('mode=webmin') > 0) {
top.left.location = url;
}
} else {
top.left.location = url;
}
</script>
EOF
}
sub theme_prebody
{
if ($script_name =~ /session_login.cgi/) {
print "<link rel='stylesheet' type='text/css' href='$gconfig{'webprefix'}/unauthenticated/gray-reset-fonts-grids-base.css'>\n";
print "<link rel='stylesheet' type='text/css' href='$gconfig{'webprefix'}/unauthenticated/gray-virtual-server-style.css'>\n";
print "<!--[if IE]>\n";
print "<style type=\"text/css\">\n";
print "table.formsection, table.ui_table, table.loginform { border-collapse: collapse; }\n";
print "</style>\n";
print "<![endif]-->\n";
}
}
sub theme_prehead
{
print "<link rel='stylesheet' type='text/css' href='$gconfig{'webprefix'}/unauthenticated/gray-reset-fonts-grids-base.css'>\n";
print "<link rel='stylesheet' type='text/css' href='$gconfig{'webprefix'}/unauthenticated/gray-virtual-server-style.css' />\n";
print "<!--[if IE]>\n";
print "<style type=\"text/css\">\n";
print "table.formsection, table.ui_table, table.loginform { border-collapse: collapse; }\n";
print "</style>\n";
print "<![endif]-->\n";
print "<script>\n";
print "var rowsel = new Array();\n";
print "</script>\n";
print "<script type='text/javascript' src='$gconfig{'webprefix'}/unauthenticated/sorttable.js'></script>\n";
if ($ENV{'HTTP_USER_AGENT'} =~ /Chrome/) {
print "<style type=\"text/css\">\n";
print "textarea,pre { font-size:120%; }\n";
print "textarea { font-family:monospace; }\n";
print "</style>\n";
}
}
sub theme_popup_prehead
{
return &theme_prehead();
}
sub theme_ui_table_start
{
my ($heading, $tabletags, $cols, $tds, $rightheading) = @_;
if (! $tabletags =~ /width/) { $tabletages .= " width=100%"; }
if (defined($main::ui_table_cols)) {
push(@main::ui_table_cols_stack, $main::ui_table_cols);
push(@main::ui_table_pos_stack, $main::ui_table_pos);
push(@main::ui_table_default_tds_stack, $main::ui_table_default_tds);
}
my $rv;
my $colspan = 1;
if (!$WRAPPER_OPEN) {
$rv .= "<table class='shrinkwrapper' $tabletags>\n";
$rv .= "<tr><td>\n";
}
$WRAPPER_OPEN++;
$rv .= "<table class='ui_table' $tabletags>\n";
if (defined($heading) || defined($rightheading)) {
$rv .= "<thead><tr>";
if (defined($heading)) {
$rv .= "<td><b>$heading</b></td>"
}
if (defined($rightheading)) {
$rv .= "<td align=right>$rightheading</td>";
$colspan++;
}
$rv .= "</tr></thead>\n";
}
$rv .= "<tbody> <tr class='ui_table_body'> <td colspan=$colspan>".
"<table width=100%>\n";
$main::ui_table_cols = $cols || 4;
$main::ui_table_pos = 0;
$main::ui_table_default_tds = $tds;
return $rv;
}
sub theme_ui_table_row
{
my ($label, $value, $cols, $tds) = @_;
$cols ||= 1;
$tds ||= $main::ui_table_default_tds;
my $rv;
if ($main::ui_table_pos+$cols+1 > $main::ui_table_cols &&
$main::ui_table_pos != 0) {
$rv .= "</tr>\n";
$main::ui_table_pos = 0;
}
if (defined($label) &&
($value =~ /id="([^"]+)"/ || $value =~ /id='([^']+)'/ ||
$value =~ /id=([^>\s]+)/)) {
my $id = $1;
$label = "<label for=\"".&quote_escape($id)."\">$label</label>";
}
$rv .= "<tr class='ui_form_pair'>\n" if ($main::ui_table_pos%$main::ui_table_cols == 0);
$rv .= "<td class='ui_form_label' $tds->[0]><b>$label</b></td>\n" if (defined($label));
$rv .= "<td class='ui_form_value' colspan=$cols $tds->[1]>$value</td>\n";
$main::ui_table_pos += $cols+(defined($label) ? 1 : 0);
if ($main::ui_table_pos%$main::ui_table_cols == 0) {
$rv .= "</tr>\n";
$main::ui_table_pos = 0;
}
return $rv;
}
sub theme_ui_table_end
{
my $rv;
if ($main::ui_table_cols == 4 && $main::ui_table_pos) {
$rv .= &ui_table_row(" ", " ");
}
if (@main::ui_table_cols_stack) {
$main::ui_table_cols = pop(@main::ui_table_cols_stack);
$main::ui_table_pos = pop(@main::ui_table_pos_stack);
$main::ui_table_default_tds = pop(@main::ui_table_default_tds_stack);
}
else {
$main::ui_table_cols = undef;
$main::ui_table_pos = undef;
$main::ui_table_default_tds = undef;
}
$rv .= "</tbody></table></td></tr></table>\n";
if ($WRAPPER_OPEN==1) {
$rv .= "</td></tr>\n";
$rv .= "</table>\n";
}
$WRAPPER_OPEN--;
return $rv;
}
sub theme_ui_tabs_start
{
my ($tabs, $name, $sel, $border) = @_;
my $rv;
if (!$main::ui_hidden_start_donejs++) {
$rv .= &ui_hidden_javascript();
}
my $tabnames = "[".join(",", map { "\"".&quote_escape($_->[0])."\"" } @$tabs)."]";
my $tabtitles = "[".join(",", map { "\"".&quote_escape($_->[1])."\"" } @$tabs)."]";
$rv .= "<script>\n";
$rv .= "document.${name}_tabnames = $tabnames;\n";
$rv .= "document.${name}_tabtitles = $tabtitles;\n";
$rv .= "</script>\n";
my $imgdir = "$gconfig{'webprefix'}/images";
$rv .= &ui_hidden($name, $sel)."\n";
$rv .= "<table border=0 cellpadding=0 cellspacing=0 class='ui_tabs'>\n";
$rv .= "<tr><td bgcolor=
if ($ENV{'HTTP_USER_AGENT'} !~ /msie/i) {
$rv .= "<img src=$imgdir/1x1.gif>";
}
$rv .= "</td></tr>\n";
$rv .= "<tr>\n";
$rv .= "<td bgcolor=
foreach my $t (@$tabs) {
if ($t ne $tabs[0]) {
$rv .= "<td width=2 bgcolor=
"<img src=$imgdir/1x1.gif></td>\n";
}
my $tabid = "tab_".$t->[0];
$rv .= "<td id=${tabid} class='ui_tab'>";
$rv .= "<table cellpadding=0 cellspacing=0 border=0><tr>";
if ($t->[0] eq $sel) {
$rv .= "<td valign=top class='tabSelected'>".
"<img src=$imgdir/lc2.gif alt=\"\"></td>";
$rv .= "<td class='tabSelected' nowrap>".
"&nbsp;<b>$t->[1]</b>&nbsp;</td>";
$rv .= "<td valign=top class='tabSelected'>".
"<img src=$imgdir/rc2.gif alt=\"\"></td>";
}
else {
$rv .= "<td valign=top class='tabUnselected'>".
"<img src=$imgdir/lc1.gif alt=\"\"></td>";
$rv .= "<td class='tabUnselected' nowrap>".
"&nbsp;<a href='$t->[2]' ".
"onClick='return select_tab(\"$name\", \"$t->[0]\")'>".
"$t->[1]</a>&nbsp;</td>";
$rv .= "<td valign=top class='tabUnselected'>".
"<img src=$imgdir/rc1.gif ".
"alt=\"\"></td>";
$rv .= "</td>\n";
}
$rv .= "</tr></table>";
$rv .= "</td>\n";
}
$rv .= "<td bgcolor=
$rv .= "</table>\n";
if ($border) {
$rv .= "<table width=100% cellpadding=0 cellspacing=0 ".
"class='ui_tabs_box'>\n";
$rv .= "<tr> <td bgcolor=
$rv .= "<td $cb colspan=3 height=2><img src=$imgdir/1x1.gif></td> </tr>\n";
$rv .= "<tr> <td $cb width=2><img src=$imgdir/1x1.gif></td>\n";
$rv .= "<td valign=top>";
}
$main::ui_tabs_selected = $sel;
return $rv;
}
sub theme_ui_columns_start
{
my ($heads, $width, $noborder, $tdtags, $title) = @_;
my ($href) = grep { $_ =~ /<a\s+href/i } @$heads;
my $rv;
$theme_ui_columns_row_toggle = 0;
if (!$noborder && !$COLUMNS_WRAPPER_OPEN) {
$rv .= "<table class='wrapper' width="
. ($width ? $width : "100")
. "%>\n";
$rv .= "<tr><td>\n";
}
if (!$noborder) {
$COLUMNS_WRAPPER_OPEN++;
}
my @classes;
push(@classes, "ui_table") if (!$noborder);
push(@classes, "sortable") if (!$href);
push(@classes, "ui_columns");
$rv .= "<table".(@classes ? " class='".join(" ", @classes)."'" : "").
(defined($width) ? " width=$width%" : "").">\n";
if ($title) {
$rv .= "<thead> <tr $tb class='ui_columns_heading'>".
"<td colspan=".scalar(@$heads)."><b>$title</b></td>".
"</tr> </thead> <tbody>\n";
}
$rv .= "<thead> <tr $tb class='ui_columns_heads'>\n";
my $i;
for($i=0; $i<@$heads; $i++) {
$rv .= "<td ".$tdtags->[$i]."><b>".
($heads->[$i] eq "" ? "<br>" : $heads->[$i])."</b></td>\n";
}
$rv .= "</tr></thead> <tbody>\n";
$theme_ui_columns_count++;
return $rv;
}
sub theme_ui_columns_row
{
$theme_ui_columns_row_toggle = $theme_ui_columns_row_toggle ? '0' : '1';
local ($cols, $tdtags) = @_;
my $rv;
$rv .= "<tr class='ui_columns_row row$theme_ui_columns_row_toggle' onMouseOver=\"this.className='mainhigh'\" onMouseOut=\"this.className='mainbody row$theme_ui_columns_row_toggle'\">\n";
my $i;
for($i=0; $i<@$cols; $i++) {
$rv .= "<td ".$tdtags->[$i].">".
($cols->[$i] !~ /\S/ ? "<br>" : $cols->[$i])."</td>\n";
}
$rv .= "</tr>\n";
return $rv;
}
sub theme_ui_columns_end
{
my $rv;
$rv = "</tbody> </table>\n";
if ($COLUMNS_WRAPPER_OPEN == 1) {
$rv .= "</td> </tr> </table>\n";
}
$COLUMNS_WRAPPER_OPEN--;
return $rv;
}
sub theme_ui_grid_table
{
my ($elements, $cols, $width, $tds, $tabletags, $title) = @_;
return "" if (!@$elements);
my $rv = "<table class='wrapper' "
. ($width ? " width=$width%" : " width=100%")
. ($tabletags ? " ".$tabletags : "")
. "><tr><td>\n";
$rv .= "<table class='ui_table ui_grid_table'"
. ($width ? " width=$width%" : "")
. ($tabletags ? " ".$tabletags : "")
. ">\n";
if ($title) {
$rv .= "<thead><tr class='ui_grid_heading'> ".
"<td colspan=$cols><b>$title</b></td> </tr></thead>\n";
}
$rv .= "<tbody>\n";
my $i;
for($i=0; $i<@$elements; $i++) {
$rv .= "<tr class='ui_grid_row'>" if ($i%$cols == 0);
$rv .= "<td ".$tds->[$i%$cols]." valign=top class='ui_grid_cell'>".
$elements->[$i]."</td>\n";
$rv .= "</tr>" if ($i%$cols == $cols-1);
}
if ($i%$cols) {
while($i%$cols) {
$rv .= "<td ".$tds->[$i%$cols]." class='ui_grid_cell'><br></td>\n";
$i++;
}
$rv .= "</tr>\n";
}
$rv .= "</table>\n";
$rv .= "</tbody>\n";
$rv .= "</td></tr></table>\n";
return $rv;
}
sub theme_ui_hidden_table_start
{
my ($heading, $tabletags, $cols, $name, $status, $tds, $rightheading) = @_;
my $rv;
if (!$main::ui_hidden_start_donejs++) {
$rv .= &ui_hidden_javascript();
}
my $divid = "hiddendiv_$name";
my $openerid = "hiddenopener_$name";
my $defimg = $status ? "open.gif" : "closed.gif";
my $defclass = $status ? 'opener_shown' : 'opener_hidden';
my $text = defined($tconfig{'cs_text'}) ? $tconfig{'cs_text'} :
defined($gconfig{'cs_text'}) ? $gconfig{'cs_text'} : "000000";
if (!$WRAPPER_OPEN) {
$rv .= "<table class='shrinkwrapper' $tabletags>\n";
$rv .= "<tr><td>\n";
}
$WRAPPER_OPEN++;
my $colspan = 1;
$rv .= "<table class='ui_table' $tabletags>\n";
if (defined($heading) || defined($rightheading)) {
$rv .= "<thead><tr>";
if (defined($heading)) {
$rv .= "<td><a href=\"javascript:hidden_opener('$divid', '$openerid')\" id='$openerid'><img border=0 src='$gconfig{'webprefix'}/images/$defimg'></a> <a href=\"javascript:hidden_opener('$divid', '$openerid')\" class='ui-hidden-table-title'><b>$heading</b></a></td>";
}
if (defined($rightheading)) {
$rv .= "<td align=right>$rightheading</td>";
$colspan++;
}
$rv .= "</tr> </thead>\n";
}
$rv .= "<tbody><tr> <td colspan=$colspan><div class='$defclass' id='$divid'><table width=100%>\n";
$main::ui_table_cols = $cols || 4;
$main::ui_table_pos = 0;
$main::ui_table_default_tds = $tds;
return $rv;
}
sub theme_ui_hidden_table_end
{
my ($name) = @_;
local $rv = "</table></div></td></tr></tbody></table>\n";
if ( $WRAPPER_OPEN == 1 ) {
$WRAPPER_OPEN--;
$rv .= "</td></tr></table>\n";
}
elsif ($WRAPPER_OPEN) { $WRAPPER_OPEN--; }
return $rv;
}
sub theme_select_all_link
{
local ($field, $form, $text) = @_;
$form = int($form);
$text ||= $text{'ui_selall'};
return "<a class='select_all' href='
}
sub theme_select_invert_link
{
local ($field, $form, $text) = @_;
$form = int($form);
$text ||= $text{'ui_selinv'};
return "<a class='select_invert' href='
}
sub theme_select_rows_link
{
local ($field, $form, $text, $rows) = @_;
$form = int($form);
my $js = "var sel = { ".join(",", map { "\"".&quote_escape($_)."\":1" } @$rows)." }; ";
$js .= "for(var i=0; i<document.forms[$form].${field}.length; i++) { var ff = document.forms[$form].${field}[i]; var r = document.getElementById(\"row_\"+ff.id); ff.checked = sel[ff.value]; if (r) { r.className = ff.checked ? \"mainsel\" : \"mainbody row\"+((i+1)%2) } } ";
$js .= "return false;";
return "<a class='select_rows' href='
}
sub theme_ui_checked_columns_row
{
$theme_ui_columns_row_toggle = $theme_ui_columns_row_toggle ? '0' : '1';
local ($cols, $tdtags, $checkname, $checkvalue, $checked, $disabled, $tags) = @_;
my $rv;
my $cbid = &quote_escape(quotemeta("${checkname}_${checkvalue}"));
my $rid = &quote_escape(quotemeta("row_${checkname}_${checkvalue}"));
my $ridtr = &quote_escape("row_${checkname}_${checkvalue}");
my $mycb = $cb;
if ($checked) {
$mycb =~ s/mainbody/mainsel/g;
}
$mycb =~ s/class='/class='row$theme_ui_columns_row_toggle ui_checked_columns /;
$rv .= "<tr id=\"$ridtr\" $mycb onMouseOver=\"this.className = document.getElementById('$cbid').checked ? 'mainhighsel' : 'mainhigh'\" onMouseOut=\"this.className = document.getElementById('$cbid').checked ? 'mainsel' : 'mainbody row$theme_ui_columns_row_toggle'\">\n";
$rv .= "<td class='ui_checked_checkbox' ".$tdtags->[0].">".
&ui_checkbox($checkname, $checkvalue, undef, $checked, $tags." "."onClick=\"document.getElementById('$rid').className = this.checked ? 'mainhighsel' : 'mainhigh';\"", $disabled).
"</td>\n";
my $i;
for($i=0; $i<@$cols; $i++) {
$rv .= "<td ".$tdtags->[$i+1].">";
if ($cols->[$i] !~ /<a\s+href|<input|<select|<textarea/) {
$rv .= "<label for=\"".
&quote_escape("${checkname}_${checkvalue}")."\">";
}
$rv .= ($cols->[$i] !~ /\S/ ? "<br>" : $cols->[$i]);
if ($cols->[$i] !~ /<a\s+href|<input|<select|<textarea/) {
$rv .= "</label>";
}
$rv .= "</td>\n";
}
$rv .= "</tr>\n";
return $rv;
}
sub theme_ui_radio_columns_row
{
local ($cols, $tdtags, $checkname, $checkvalue, $checked) = @_;
my $rv;
my $cbid = &quote_escape(quotemeta("${checkname}_${checkvalue}"));
my $rid = &quote_escape(quotemeta("row_${checkname}_${checkvalue}"));
my $ridtr = &quote_escape("row_${checkname}_${checkvalue}");
my $mycb = $cb;
if ($checked) {
$mycb =~ s/mainbody/mainsel/g;
}
$mycb =~ s/class='/class='ui_radio_columns /;
$rv .= "<tr $mycb id=\"$ridtr\" onMouseOver=\"this.className = document.getElementById('$cbid').checked ? 'mainhighsel' : 'mainhigh'\" onMouseOut=\"this.className = document.getElementById('$cbid').checked ? 'mainsel' : 'mainbody'\">\n";
$rv .= "<td ".$tdtags->[0]." class='ui_radio_radio'>".
&ui_oneradio($checkname, $checkvalue, undef, $checked, "onClick=\"for(i=0; i<form.$checkname.length; i++) { ff = form.${checkname}[i]; r = document.getElementById('row_'+ff.id); if (r) { r.className = 'mainbody' } } document.getElementById('$rid').className = this.checked ? 'mainhighsel' : 'mainhigh';\"").
"</td>\n";
my $i;
for($i=0; $i<@$cols; $i++) {
$rv .= "<td ".$tdtags->[$i+1].">";
if ($cols->[$i] !~ /<a\s+href|<input|<select|<textarea/) {
$rv .= "<label for=\"".
&quote_escape("${checkname}_${checkvalue}")."\">";
}
$rv .= ($cols->[$i] !~ /\S/ ? "<br>" : $cols->[$i]);
if ($cols->[$i] !~ /<a\s+href|<input|<select|<textarea/) {
$rv .= "</label>";
}
$rv .= "</td>\n";
}
$rv .= "</tr>\n";
return $rv;
}
sub theme_ui_nav_link
{
my ($direction, $url, $disabled) = @_;
my $alt = $direction eq "left" ? '<-' : '->';
if ($disabled) {
return "<img alt=\"$alt\" align=\"middle\""
. "src=\"$gconfig{'webprefix'}/images/$direction-grey.gif\">\n";
}
else {
return "<a href=\"$url\"><img alt=\"$alt\" align=\"top\""
. "src=\"$gconfig{'webprefix'}/images/$direction.gif\"></a>\n";
}
}
sub theme_footer
{
my $i;
my $count = 0;
my %module_info = get_module_info(get_module_name());
for($i=0; $i+1<@_; $i+=2) {
local $url = $_[$i];
if ($url ne '/' || !$tconfig{'noindex'}) {
if ($url eq '/') {
$url = "/?cat=$module_info{'category'}";
}
elsif ($url eq '' && get_module_name()) {
$url = "/".get_module_name()."/".
$module_info{'index_link'};
}
elsif ($url =~ /^\?/ && get_module_name()) {
$url = "/".get_module_name()."/$url";
}
$url = "$gconfig{'webprefix'}$url" if ($url =~ /^\//);
if ($count++ == 0) {
print theme_ui_nav_link("left", $url);
}
else {
print "&nbsp;|\n";
}
print "&nbsp;<a href=\"$url\">",&text('main_return', $_[$i+1]),"</a>\n";
}
}
print "<br>\n";
if (!$_[$i]) {
print "</body></html>\n";
}
}
sub theme_ui_hidden_javascript
{
my $rv;
my $imgdir = "$gconfig{'webprefix'}/images";
return <<EOF;
<style>
.opener_shown {display:inline}
.opener_hidden {display:none}
</style>
<script>
// Open or close a hidden section
function hidden_opener(divid, openerid)
{
var divobj = document.getElementById(divid);
var openerobj = document.getElementById(openerid);
if (divobj.className == 'opener_shown') {
divobj.className = 'opener_hidden';
openerobj.innerHTML = '<img border=0 src=$imgdir/closed.gif>';
}
else {
divobj.className = 'opener_shown';
openerobj.innerHTML = '<img border=0 src=$imgdir/open.gif>';
}
}
// Show a tab
function select_tab(name, tabname, form)
{
var tabnames = document[name+'_tabnames'];
var tabtitles = document[name+'_tabtitles'];
for(var i=0; i<tabnames.length; i++) {
var tabobj = document.getElementById('tab_'+tabnames[i]);
var divobj = document.getElementById('div_'+tabnames[i]);
var title = tabtitles[i];
if (tabnames[i] == tabname) {
// Selected table
tabobj.innerHTML = '<table cellpadding=0 cellspacing=0><tr>'+
'<td valign=top class=\\'tabSelected\\'>'+
'<img src=$imgdir/lc2.gif alt=""></td>'+
'<td class=\\'tabSelected\\' nowrap>'+
'&nbsp;<b>'+title+'</b>&nbsp;</td>'+
'<td valign=top class=\\'tabSelected\\'>'+
'<img src=$imgdir/rc2.gif alt=""></td>'+
'</tr></table>';
divobj.className = 'opener_shown';
}
else {
// Non-selected tab
tabobj.innerHTML = '<table cellpadding=0 cellspacing=0><tr>'+
'<td valign=top class=\\'tabUnselected\\'>'+
'<img src=$imgdir/lc1.gif alt=""></td>'+
'<td class=\\'tabUnselected\\' nowrap>'+
'&nbsp;<a href=\\'\\' onClick=\\'return select_tab("'+
name+'", "'+tabnames[i]+'")\\'>'+title+'</a>&nbsp;</td>'+
'<td valign=top class=\\'tabUnselected\\'>'+
'<img src=$imgdir/rc1.gif alt=""></td>'+
'</tr></table>';
divobj.className = 'opener_hidden';
}
}
if (document.forms[0] && document.forms[0][name]) {
document.forms[0][name].value = tabname;
}
return false;
}
</script>
EOF
}
=yui
Functions for generating YUI CSS grids markup.
=cut
sub theme_ui_yui_grid_start {
my ($id, $type) = @_;
return "<div id='grid_$id' class='yui-$type'>\n";
}
sub theme_ui_yui_grid_end {
my ($id) = @_;
return "</div> <!-- grid_$id -->\n";
}
sub theme_ui_yui_grid_section_start {
my ($id, $first) = @_;
if ($first) { return "<div id='grid_$id' class='yui-u first'>\n"; }
else { return "<div id='grid_$id' class='yui-u'>\n"; }
}
sub theme_ui_yui_grid_section_end {
my ($id) = @_;
return "</div> <!-- grid_$id -->\n";
}
1;
