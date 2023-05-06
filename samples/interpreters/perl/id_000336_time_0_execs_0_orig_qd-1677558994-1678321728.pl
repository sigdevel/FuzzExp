#!/usr/local/bin/perl
{
package qd;
$X11FONTS = '/usr/local/X11R5/X11/fonts/bdf';
$TIMES = 20;
$HELVETICA = 21;
$COURIER = 22;
$SYMBOL = 23;
$NEWCENTURYSCHOOLBK = 34;
$PLAIN = 0;
$BOLD = 1;
$ITALIC = 2;
$UNDERLINE = 4;
$GRAY = pack ('n4',0xAA55,0xAA55,0xAA55,0xAA55);
$DKGRAY = pack ('n4',0xDD77,0xDD77,0xDD77,0xDD77);
$LTGRAY = pack ('n4',0x8822,0x8822,0x8822,0x8822);
$WHITE = pack('n4',0x0000,0x0000,0x0000,0x0000);
$BLACK = pack ('n4',0xFFFF,0xFFFF,0xFFFF,0xFFFF);
$BLACKCOLOR = 33;
$WHITECOLOR = 30;
$REDCOLOR = 209;
$GREENCOLOR = 329;
$BLUECOLOR = 389;
$CYANCOLOR = 269;
$MAGENTACOLOR = 149;
$YELLOWCOLOR = 89;
$PICTHEADER = "\0" x 512;
$fudgefactor = 0.55;
$ITALICEXTRA = 0.05;
$BOLDEXTRA = 0.08;
$textFont = $HELVETICA;
$textSize = 12;
$textFace = $PLAIN;
$rgbfgcolor = pack('n*',0xFFFF,0xFFFF,0xFFFF);
$rgbbgcolor = pack('n*',0,0,0);
$fgcolor = $BLACKCOLOR;
$bgcolor = $WHITECOLOR;
$polySave = undef;
$_PnPattern = $BLACK;
$_polyName = "polygon000";
sub OpenPicture {
local($rect) = @_;
$currH = $currV = 0;
$pict = $PICTHEADER;
$pict .= pack('n',0);
$pict .= $rect;
$pict .= pack('n',0x0011);
$pict .= pack('n',0x02FF);
$pict .= pack('nC24',0x0C00,0);
&TextFont($textFont);
&TextSize($textSize);
&TextFace($textFace);
}
sub ClosePicture {
$pict .= pack ('n',0x00FF);
substr($pict,512,2) = pack('n',length($pict) - 512);
return $pict;
}
sub ClipRect {
local($rect) = @_;
$pict .= pack('nn',0x0001,0x0A) . $rect;
}
sub PenPat {
local($newpat) = @_;
return unless $newpat ne $_PnPattern;
$_PnPattern = $newpat;
$pict .= pack('n',0x0009) . $_PnPattern;
}
sub RGBForeColor {
local($rgb) = pack('n3',@_);
return unless $rgb ne $rgbfgcolor;
$rgbfgcolor = $rgb;
$pict .= pack('n',0x001A) . $rgbfgcolor;
}
sub RGBBackColor {
local($rgb) = pack('n3',@_);
return unless $rgb ne $rgbbgcolor;
$rgbbgcolor = $rgb;
$pict .= pack('n',0x001B) . $rgbbgcolor;
}
sub FgColor {
local($color) = @_;
return unless $color != $fgcolor;
$fgcolor = $color;
$pict .= pack('nL',0x000E,$color);
}
sub BgColor {
local($color) = @_;
return unless $color != $bgcolor;
$bgcolor = $color;
$pict .= pack('nL',0x000F,$color);
}
sub TextFont {
local($font) = @_;
$textFont = $font;
$pict .= pack('nn',0x0003,$font);
}
sub TextSize {
local($size) = @_;
$textSize = $size;
$pict .= pack('nn',0x000D,$size);
}
sub PenSize {
local($h,$v) = @_;
$pict .= pack('nnn',0x0007,$v,$h);
}
sub TextFace {
return if $textFace == @_[0];
$textFace = @_[0];
$pict .= pack ('nCC',0x0004,$textFace,0);
}
sub DrawString {
local($text) = @_;
$text .= "\0" x ((length($text) + 1) % 2);
$pict .= pack('nnnC',0x0028,$currV,$currH,length($text)) . $text;
}
sub SetRect {
local(*r,$h1,$v1,$h2,$v2) = @_;
$r = pack ('n4',$v1,$h1,$v2,$h2);
}
sub OffsetRect {
local(*r,$x,$y) = @_;
local($v1,$h1,$v2,$h2) = unpack('n4',$r);
$h1 += $x; $h2 += $x;
$v1 += $y; $v2 += $y;
$r = pack ('n4',$v1,$h1,$v2,$h2);
}
sub InsetRect {
local(*r,$x,$y) = @_;
local($v1,$h1,$v2,$h2) = unpack('n4',$r);
$h1 -= int($x/2); $h2 -= int($x/2);
$v1 -= int($y/2); $v2 -= int($y/2);
$r = pack ('n4',$v1,$h1,$v2,$h2);
}
sub a2r {
local($top,$left,$bottom,$right) = @_;
return pack('n4',$top,$left,$bottom,$right);
}
sub r2a {
local($rect) = @_;
return unpack('n4',$rect);
}
sub aa2r {
local(%r) = @_;
return pack('n4',$r{'top'},$r{'left'},$r{'bottom'},$r{'right'});
}
sub r2aa {
local($r) = @_;
local(%r);
($r{'top'},$r{'left'},$r{'bottom'},$r{'right'}) = unpack('n4',$r);
return %r;
}
sub MoveTo {
($currH,$currV) = @_;
}
sub Move {
local($dh,$dv) = @_;
$currH += $dh;
$currV += $dv;
}
sub LineTo {
local($h,$v) = @_;
if (defined(@polySave)) {
&_addVertex(*polySave,$h,$v)
} else {
$pict .= pack('nn4',0x0020,$currV,$currH,$v,$h);
}
($currH,$currV) = ($h,$v);
}
sub Line {
local($dh,$dv) = @_;
if (defined(@polySave)) {
&_addVertex(*polySave,$h,$v);
} else {
$pict .= pack('nn4',0x0020,$currV,$currH,$currV+$dv,$currH+$dh);
}
($currH,$currV) = ($currH+$dh,$currV+$dv);
}
sub Scale {
local($numerator,$denominator)= @_;
$pict .= pack('nnnn2',0x00A1,182,4,$numerator,$denominator);
}
sub FrameRect {
local($rect) = @_;
$pict .= pack('n',0x0030) . $rect;
}
sub PaintRect {
local($rect) = @_;
$pict .= pack('n',0x0031) . $rect;
}
sub EraseRect {
local($rect) = @_;
$pict .= pack('n',0x0032) . $rect;
}
sub InvertRect {
local($rect) = @_;
$pict .= pack('n',0x0033) . $rect;
}
sub FillRect {
local($rect,$pattern) = @_;
local($oldpat) = $_PnPattern;
&PenPat($pattern);
&PaintRect($rect);
&PenPat($oldpat);
}
sub FrameOval {
local($rect) = @_;
$pict .= pack('n',0x0050) . $rect;
}
sub PaintOval {
local($rect) = @_;
$pict .= pack('n',0x0051) . $rect;
}
sub EraseOval {
local($rect) = @_;
$pict .= pack('n',0x0052) . $rect;
}
sub InvertOval {
local($rect) = @_;
$pict .= pack('n',0x0053) . $rect;
}
sub FillOval {
local($rect,$pattern) = @_;
local($oldpat) = $_PnPattern;
&PenPat($pattern);
&PaintOval($rect);
&PenPat($oldpat);
}
sub FrameArc {
local($rect,$startAngle,$arcAngle) = @_;
$pict .= pack('n',0x0060) . $rect;
$pict .= pack('nn',$startAngle,$arcAngle);
}
sub PaintArc {
local($rect,$startAngle,$arcAngle) = @_;
$pict .= pack('n',0x0061) . $rect;
$pict .= pack('nn',$startAngle,$arcAngle);
}
sub EraseArc {
local($rect,$startAngle,$arcAngle) = @_;
$pict .= pack('n',0x0062) . $rect;
$pict .= pack('nn',$startAngle,$arcAngle);
}
sub InvertArc {
local($rect,$startAngle,$arcAngle) = @_;
$pict .= pack('n',0x0063) . $rect;
$pict .= pack('nn',$startAngle,$arcAngle);
}
sub FillArc {
local($rect,$startAngle,$arcAngle,$pattern) = @_;
local($oldpat) = $_PnPattern;
&PenPat($pattern);
&PaintArc($rect,$startAngle,$arcAngle);
&PenPat($oldpat);
}
sub FrameRoundRect {
local($rect,$ovalWidth,$ovalHeight) = @_;
unless ($_roundRectCurvature eq "$ovalWidth $ovalHeight") {
$pict .= pack('nn2',0x000B,$ovalHeight,$ovalWidth);
$_roundRectCurvature = "$ovalWidth $ovalHeight";
}
$pict .= pack('n',0x0040) . $rect;
}
sub PaintRoundRect {
local($rect,$ovalWidth,$ovalHeight) = @_;
unless ($_roundRectCurvature eq "$ovalWidth $ovalHeight") {
$pict .= pack('nn2',0x000B,$ovalHeight,$ovalWidth);
$_roundRectCurvature = "$ovalWidth $ovalHeight";
}
$pict .= pack('n',0x0041) . $rect;
}
sub EraseRoundRect {
local($rect,$ovalWidth,$ovalHeight) = @_;
unless ($_roundRectCurvature eq "$ovalWidth $ovalHeight") {
$pict .= pack('nn2',0x000B,$ovalHeight,$ovalWidth);
$_roundRectCurvature = "$ovalWidth $ovalHeight";
}
$pict .= pack('n',0x0042) . $rect;
}
sub InvertRoundRect {
local($rect,$ovalWidth,$ovalHeight) = @_;
unless ($_roundRectCurvature eq "$ovalWidth $ovalHeight") {
$pict .= pack('nn2',0x000B,$ovalHeight,$ovalWidth);
$_roundRectCurvature = "$ovalWidth $ovalHeight";
}
$pict .= pack('n',0x0043) . $rect;
}
sub FillRoundRect {
local($rect,$ovalWidth,$ovalHeight,$pattern) = @_;
local($oldpat) = $_PnPattern;
&PenPat($pattern);
&PaintRoundRect($rect,$ovalWidth,$ovalHeight);
&PenPat($oldpat);
}
sub OpenPoly {
$_polyName++;
undef $polySave;
*polySave = $_polyName;
@polySave = (10,0,0,0,0);
return $_polyName;
}
sub ClosePoly {
*polySave = 'scratch';
undef @polySave;
}
sub KillPoly {
local(*poly) = @_;
undef @poly;
}
sub FramePoly {
local(*poly) = @_;
return unless @poly;
$pict .= pack('n*',0x0070,@poly);
}
sub PaintPoly {
local(*poly) = @_;
return unless @poly;
$pict .= pack('n*',0x0071,@poly);
}
sub ErasePoly {
local(*poly) = @_;
return unless @poly;
$pict .= pack('n*',0x0072,@poly);
}
sub InvertPoly {
local(*poly) = @_;
return unless @poly;
$pict .= pack('n*',0x0073,@poly);
}
sub FillPoly {
local(*poly,$pattern) = @_;
return unless @poly;
local($oldpat) = $_PnPattern;
&PenPat($pattern);
&PaintPoly(*poly);
&PenPat($oldpat);
}
sub OffsetPoly {
local(*poly,$dh,$dv) = @_;
return unless @poly;
local($size,@vertices) = @poly;
local($i);
for ($i=0;$i<@vertices;$i+=2) {
$vertices[$i] += $dv;
$vertices[$i+1] += $dh;
}
@poly = ($size,@vertices);
}
sub MapPoly {
local(*poly,$srcRect,$destRect) = @_;
return unless @poly;
local($size,@vertices) = @poly;
local(@src) = unpack('n4',$srcRect);
local(@dest) = unpack('n4',$destRect);
local($factorV) = ($dest[2]-$dest[0])/($src[2]-$src[0]);
local($factorH) = ($dest[3]-$dest[1])/($src[3]-$src[1]);
for ($i=0;$i<@vertices;$i+=2) {
$vertices[$i] = int($dest[0] + ($vertices[$i] - $src[0]) * $factorV);
$vertices[$i+1] = int($dest[1] + ($vertices[$i+1] - $src[1]) * $factorH);
}
@poly = ($size,@vertices);
}
sub _addVertex {
local(*polygon,$h,$v) = @_;
local($size,$top,$left,$bottom,$right,@vertices) = @polygon;
unless (@vertices) {
push(@vertices,$currV,$currH);
$size += 4;
$top = $bottom = $currV;
$left = $right = $currH;
}
push (@vertices,$v,$h);
$size += 4;
$top = $v if $v < $top;
$bottom = $v if $v > $bottom;
$left = $h if $h < $left;
$right = $h if $h > $right;
@polygon=($size,$top,$left,$bottom,$right,@vertices);
}
sub TextWidth {
local($text) = @_;
local($face) = 0xFB & $textFace;
local($metric_name) = &_getFontMetrics($textFont,$textSize,$face);
if ($metric_name && (*metrics = $metric_name) && defined(%metrics)) {
local($length);
foreach (split('',$text)) {
$length += $metrics{ord($_)};
}
return $length;
} else {
local($extra);
$extra += $ITALICEXTRA if vec($textFace,$ITALIC,1);
$extra += $BOLDEXTRA if vec($textFace,$BOLD,1);
return length($text) * $textSize * ($fudgefactor+$extra);
}
}
sub _getFontMetrics {
local($font,$size,$face) = @_;
local($key) = "$font $size $face";
return $_metricsArrays{$key} if $_metricsArrays{$key};
return undef unless $font_metric_files{$key};
return undef if $_failed_metric{$key};
unless (open(BDF,"$font_metric_files{$key}")) {
$_failed_metric_files{$key}++;
return undef;
}
$next_metric++;
local(*metrics) = $next_metric; local($char);
while (<BDF>) {
next unless /^STARTCHAR/../^ENDCHAR/;
if (/^ENCODING\s+(\d+)/) { $char = $1; }
elsif (/^DWIDTH\s+(\d+)/)   { $metrics{$char}=$1; }
}
close(BDF);
return $_metricsArrays{$key} = $next_metric;
}
%font_metric_files = (
"22 8 1","$X11FONTS/courB08.bdf",
"22 10 1","$X11FONTS/courB10.bdf",
"22 12 1","$X11FONTS/courB12.bdf",
"22 14 1","$X11FONTS/courB14.bdf",
"22 18 1","$X11FONTS/courB18.bdf",
"22 24 1","$X11FONTS/courB24.bdf",
"22 8 2","$X11FONTS/courO08.bdf",
"22 10 2","$X11FONTS/courO10.bdf",
"22 12 2","$X11FONTS/courO12.bdf",
"22 14 2","$X11FONTS/courO14.bdf",
"22 18 2","$X11FONTS/courO18.bdf",
"22 24 2","$X11FONTS/courO24.bdf",
"22 8 0","$X11FONTS/courR08.bdf",
"22 10 0","$X11FONTS/courR10.bdf",
"22 12 0","$X11FONTS/courR12.bdf",
"22 14 0","$X11FONTS/courR14.bdf",
"22 18 0","$X11FONTS/courR18.bdf",
"22 24 0","$X11FONTS/courR24.bdf",
"21 8 1","$X11FONTS/helvB08.bdf",
"21 10 1","$X11FONTS/helvB10.bdf",
"21 12 1","$X11FONTS/helvB12.bdf",
"21 14 1","$X11FONTS/helvB14.bdf",
"21 18 1","$X11FONTS/helvB18.bdf",
"21 24 1","$X11FONTS/helvB24.bdf",
"21 8 2","$X11FONTS/helvO08.bdf",
"21 10 2","$X11FONTS/helvO10.bdf",
"21 12 2","$X11FONTS/helvO12.bdf",
"21 14 2","$X11FONTS/helvO14.bdf",
"21 18 2","$X11FONTS/helvO18.bdf",
"21 24 2","$X11FONTS/helvO24.bdf",
"21 8 0","$X11FONTS/helvR08.bdf",
"21 10 0","$X11FONTS/helvR10.bdf",
"21 12 0","$X11FONTS/helvR12.bdf",
"21 14 0","$X11FONTS/helvR14.bdf",
"21 18 0","$X11FONTS/helvR18.bdf",
"21 24 0","$X11FONTS/helvR24.bdf",
"20 8 1","$X11FONTS/timB08.bdf",
"20 10 1","$X11FONTS/timB10.bdf",
"20 12 1","$X11FONTS/timB12.bdf",
"20 14 1","$X11FONTS/timB14.bdf",
"20 18 1","$X11FONTS/timB18.bdf",
"20 24 1","$X11FONTS/timB24.bdf",
"20 8 3","$X11FONTS/timBI08.bdf",
"20 10 3","$X11FONTS/timBI10.bdf",
"20 12 3","$X11FONTS/timBI12.bdf",
"20 14 3","$X11FONTS/timBI14.bdf",
"20 18 3","$X11FONTS/timBI18.bdf",
"20 24 3","$X11FONTS/timBI24.bdf",
"20 8 2","$X11FONTS/timI08.bdf",
"20 10 2","$X11FONTS/timI10.bdf",
"20 12 2","$X11FONTS/timI12.bdf",
"20 14 2","$X11FONTS/timI14.bdf",
"20 18 2","$X11FONTS/timI18.bdf",
"20 24 2","$X11FONTS/timI24.bdf",
"20 8 0","$X11FONTS/timR08.bdf",
"20 10 0","$X11FONTS/timR10.bdf",
"20 12 0","$X11FONTS/timR12.bdf",
"20 14 0","$X11FONTS/timR14.bdf",
"20 18 0","$X11FONTS/timR18.bdf",
"20 24 0","$X11FONTS/timR24.bdf",
"34 8 1","$X11FONTS/ncenB08.bdf",
"34 10 1","$X11FONTS/ncenB10.bdf",
"34 12 1","$X11FONTS/ncenB12.bdf",
"34 14 1","$X11FONTS/ncenB14.bdf",
"34 18 1","$X11FONTS/ncenB18.bdf",
"34 24 1","$X11FONTS/ncenB24.bdf",
"34 8 3","$X11FONTS/ncenBI08.bdf",
"34 10 3","$X11FONTS/ncenBI10.bdf",
"34 12 3","$X11FONTS/ncenBI12.bdf",
"34 14 3","$X11FONTS/ncenBI14.bdf",
"34 18 3","$X11FONTS/ncenBI18.bdf",
"34 24 3","$X11FONTS/ncenBI24.bdf",
"34 8 2","$X11FONTS/ncenI08.bdf",
"34 10 2","$X11FONTS/ncenI10.bdf",
"34 12 2","$X11FONTS/ncenI12.bdf",
"34 14 2","$X11FONTS/ncenI14.bdf",
"34 18 2","$X11FONTS/ncenI18.bdf",
"34 24 2","$X11FONTS/ncenI24.bdf",
"34 8 0","$X11FONTS/ncenR08.bdf",
"34 10 0","$X11FONTS/ncenR10.bdf",
"34 12 0","$X11FONTS/ncenR12.bdf",
"34 14 0","$X11FONTS/ncenR14.bdf",
"34 18 0","$X11FONTS/ncenR18.bdf",
"34 24 0","$X11FONTS/ncenR24.bdf"
);
$next_metric = "metrics0000";
1;
}
