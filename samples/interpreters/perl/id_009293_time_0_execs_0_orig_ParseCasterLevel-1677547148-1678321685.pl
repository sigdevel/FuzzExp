#!/usr/bin/perl
$version = "0.1c";
%atoi = (
one => 1,
One => 1,
"one additional" => 1,
"an extra" => 1,
another => 1,
two => 2,
Two => 2,
three => 3,
Three => 3,
four => 4,
Four => 4,
five => 5,
Five => 5,
six => 6,
Six => 6,
seven => 7,
Seven => 7,
eight => 8,
Eight => 8,
nine => 9,
Nine => 9,
ten => 10,
Ten => 10
);
$number = "one additional|an extra|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|one|two|three|four|five|six|seven|eight|nine|ten";
%validCharBeforeBase = (
" " => 1,
"+" => 1,
"(" => 1,
":" => 1
);
$postUnitText = "s| diameter| in radius| emanation| radius|\-radius emanation| of force";
$preUnitText = " quasi\-real";
$perIdentifier = "\/| per| for every";
$levelDescriptor = " additional| ?caster";
$maxIndicator = "Max|max|max\.|maximum";
sub PluralizeBlurb
{
local($subject, $postUnitText) = @_;
if ($postUnitText eq "s" ||
($postUnitText =~ /^ radius/i) ||
($subject =~ m/^\-/) ||
($subject =~ m/^ ?(([a-zA-Z]*\.)|(feet))/) ||
($subject =~ m/^ ?(HD|HP)/i) ||
($subject =~ m/dead$/i))
{
$subject = $subject;
}
else
{
for (1..3)
{
if ($subject =~ m/^(.*?)\b(\w*)([^s ])\b( of )(.*?)$/i)
{
$subject = $1 . $2 . $3 . "s" . $4 . $5;
}
elsif ($subject =~ m/^(.*?)([^\-])\b(cube|globe|sphere|square|block|figure|giant|individual|round|target|turn)(\.\))?$/i)
{
$subject = $1 . $2 . $3 . "s" . $4;
}
elsif ($subject =~ m/^(cube|globe|sphere|square|block|day|duplicate|figure|gem|giant|hour|individual|mile|minute|missile|pebble|ray|round|serving|subject|tendril|target|turn|week)(\.\))?$/i)
{
$subject = $1 . "s" . $2;
}
elsif ($subject =~ m/^(.*?)\b(animal|bolt|burst|chain|creature|giant|horse|humanoid|mount|object|plant|servant|tree|weapon)([^s]?)\b(.*?)$/i)
{
$subject = $1 . $2 . "s" . $3 . $4;
}
elsif ($subject =~ m/^(.*?)\b(ally)\b(.*?)$/i)
{
$subject = $1 . "allies" . $3;
}
elsif ($subject =~ m/^(.*?)\b(person)\b(.*?)$/i)
{
$subject = $1 . "people" . $3;
}
elsif ($subject =~ m/^(touch)\b(.*?)$/i)
{
$subject = "touches" . $3;
}
}
}
return $subject;
}
sub FixCasterLevelForAdjustment
{
local($temp) = @_;
my $afterEquation;
my $casterLevel;
if ($temp =~ m/^([^\t]*?) *(above |beyond )(\d+)(st|nd|rd|th)\b(.*)$/)
{
$afterEquation = $1 . $5;
$casterLevel = "max(0,(CASTERLEVEL-" . $3 . "))";
}
else
{
$afterEquation = $temp;
$casterLevel = "CASTERLEVEL";
}
return ($afterEquation, $casterLevel);
}
sub FixCasterLevelForMaximumValue
{
local($beforeEqn, $eqn, $afterEqn, $incrVal) = @_;
if ($afterEqn =~ m/^d(\d+)([ \-\w]*) [\(\[]($maxIndicator) \+?(\d+)d(\d+)([^0-9\)\]]*?)[\)\]](.*)$/ &&
$4 > $incrVal*2)
{
$afterEqn = "d" . $1 . $2 . $7;
$eqn = "(min(" . $4 . "," . $eqn . "))";
}
elsif ($afterEqn =~ m/^d(\d+)([ \-\w]*)\, ($maxIndicator) \+?(\d+)d(\d+)([^0-9\)\]]*?)([\)\]])(.*)$/ &&
$4 > $incrVal*2)
{
$afterEqn = "d" . $1 . $2 . $7 . $8;
$eqn = "(min(" . $4 . "," . $eqn . "))";
}
elsif ($afterEqn =~ m/^d(\d+)([ \-\w]*) ($maxIndicator) [\(\[](\d+)d(\d+)[\)\]](.*)$/ &&
$4 > $incrVal*2)
{
$afterEqn = "d" . $1 . $2 . $6;
$eqn = "(min(" . $4 . "," . $eqn . "))";
}
elsif ($afterEqn =~ m/^d(\d+)([ \-\w]*) [\(\[]\+?(\d+)d(\d+) (.*?)($maxIndicator)[\)\]](.*)$/ &&
$3 > $incrVal*2)
{
$afterEqn = "d" . $1 . $2 . $7;
$eqn = "(min(" . $3 . "," . $eqn . "))";
}
elsif ($afterEqn =~ m/^([ \.\-\w]*) [\(\[]($maxIndicator) (\+|\-)?(\d+)([^0-9\)\]]*?)[\)\]](.*)$/ &&
$4 > $incrVal*2)
{
$afterEqn = $1 . $6;
if ($3 eq "+" &&
substr($beforeEqn, length($beforeEqn)-1) ne "+" &&
index($eqn, "+") > 0)
{
($part1, $part2) = split(/\+/, $eqn, 2);
$eqn = $part1 . "+(min(" . $4 . "," . $part2 . "))";
}
else
{
$eqn = "(min(" . $4 . "," . $eqn . "))";
}
}
elsif ($afterEqn =~ m/^([ \-\,\w]*) [\(\[]($maxIndicator) ($number)([^0-9\)\]]*?)[\)\]](.*)$/ &&
$atoi{$3} > $incrVal*2)
{
$afterEqn = $1 . $5;
$eqn = "(min(" . $atoi{$3} . "," . $eqn . "))";
}
elsif ($afterEqn =~ m/^([ \-\w]*)\, ($maxIndicator) (\+|\-)?(\d+)(\;|\.|\)|\])(.*)$/ &&
$4 > $incrVal*2)
{
$afterEqn = $5 . $6;
if ($3 eq "+" &&
substr($beforeEqn, length($beforeEqn)-1) ne "+" &&
index($eqn, "+") > 0)
{
($part1, $part2) = split(/\+/, $eqn, 2);
$eqn = $part1 . "+(min(" . $4 . "," . $part2 . "))";
}
else
{
$eqn = "(min(" . $4 . "," . $eqn . "))";
}
}
elsif ($afterEqn =~ m/^([ \-\,\.\w]*) ($maxIndicator) (\d|\d\d|$number)(.*)$/)
{
$eqn .= "<<TODO:add max<<";
}
elsif ($afterEqn =~ m/^([ \-\,\.\w]*) [\(\[]($maxIndicator) (\d|\d\d|$number)([ \+\w]*?)[\)\]](.*)$/)
{
$eqn .= "<<TODO:add max<<";
}
return ($eqn, $afterEqn);
}
sub ParseCasterLevel
{
local($temp, $depth) = @_;
++$depth;
my $beforeEquation;
my $casterLevel;
my $equation;
my $afterEquation;
if ($temp =~ m/^(.*)\b($number)\b($preUnitText)?( |\-)?([^\t]*?)($postUnitText)?(,? ?\+ ?|,? plus )\b($number|another)\b( |\-)?([^\t]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/ &&
$5 eq $10)
{
$baseVal = $atoi{$2};
$incrVal = $atoi{$8};
$diviser = $12;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$12};
}
$beforeEquation = $1;
$pluralized = PluralizeBlurb($5, $6);
$afterEquation  = $3 . $4 . $pluralized . $6 . $15;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "(" . $baseVal . "+($casterLevel*" . $incrVal . "))";
}
else
{
$equation = "(" . $baseVal . "+(floor($casterLevel/$diviser)*" . $incrVal . "))";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)\b(\d+)($preUnitText)?( |\-)?([^\t]*?)($postUnitText)?(,? ?\+ ?|,? plus )\b(\d+)( |\-)?([^\t]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/ &&
$5 eq $10 &&
($1 eq "" || exists($validCharBeforeBase{substr($1, length($1)-1)}) ))
{
$baseVal = $2;
$incrVal = $8;
$diviser = $12;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$12};
}
$beforeEquation = $1;
$afterEquation  = $3;
if ($5 ne "")
{
$pluralized = PluralizeBlurb($5, $6);
$afterEquation  = $4 . $pluralized;
}
$afterEquation .= $6 . $15;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "(" . $baseVal . "+($casterLevel*" . $incrVal . "))";
}
else
{
$equation = "(" . $baseVal . "+(floor($casterLevel/$diviser)*" . $incrVal . "))";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)(\+ ?)(\d)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/)
{
$incrVal = $3;
$diviser = $5;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1 . $2;
$afterEquation = PluralizeBlurb($8);
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)\b(\d)d(\d+)([ a-zA-Z\-]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/ &&
($foo = split($number,$4)) < 2)
{
$incrVal = $2;
$diviser = $6;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1;
$afterEquation  = "d" . $3 . $4 . $9;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)\b($number)\b (\w*)( \(?or )\b($number)\b (\w*)(\))?($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/)
{
$incrVal1 = $2;
if ($incrVal1 == 0)
{
$incrVal1 = $atoi{$incrVal1};
}
$incrVal2 = $5;
if ($incrVal2 == 0)
{
$incrVal2 = $atoi{$incrVal2};
}
$diviser = $9;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1;
$pluralized = PluralizeBlurb($6, $7);
$afterEquation  = $pluralized . $7 . $12;
$pluralized = PluralizeBlurb($3, $4);
my $inBetween = $pluralized . $4;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal1 . ") " . $inBetween . "($casterLevel*" . $incrVal2 . ") ";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal1 . ") " . $inBetween . "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal2 . ") ";
}
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*) twice caster level (.*)$/)
{
$beforeEquation = $1;
$afterEquation  = $2;
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . " (CASTERLEVEL*2) " . $afterEquation;
}
elsif ($temp =~ m/^(.*?)(\d+) \+ (your )?caster level(.*)$/)
{
$beforeEquation = $1;
$afterEquation  = $4;
$equation = "(" . $2 . "+CASTERLEVEL)";
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)\b(\d|\d\d|\d\d\d|$number)( ?)([a-z\.]*)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/)
{
$incrVal = $2;
if ($incrVal == 0)
{
$incrVal = $atoi{$incrVal};
}
$diviser = $6;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1;
$pluralized = PluralizeBlurb($4, $9);
$afterEquation  = $3 . $pluralized . $9;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif (($temp =~ m/^(.*)([Uu]p to )(a? )?\b($number)\b([^\t]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/) ||
($temp =~ m/^(.*)([Uu]p to )(a? )?\b(\d+)([^\t]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/) )
{
$incrVal = $4;
if ($incrVal == 0)
{
$incrVal = $atoi{$incrVal};
}
$diviser = $7;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1 . $2 . $3;
$pluralized = PluralizeBlurb($5);
$afterEquation  = $pluralized . $10;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif (($temp =~ m/^(.*)\b(\d|\d\d|\d\d\d|$number)\b([^\d\-\)\,\;])([^\t\)\;\+]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/) ||
($temp =~ m/^(.*)\b(\d+)([^\d\-\)\,\;])([^\t\)\;\+]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/))
{
$incrVal = $2;
if ($incrVal == 0)
{
$incrVal = $atoi{$incrVal};
}
$diviser = $6;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
if ($2 eq "an extra")
{
$beforeEquation = $1 . "+";
}
else
{
$beforeEquation = $1;
}
$pluralized = PluralizeBlurb($4);
$afterEquation  = $3 . $pluralized . $9;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
elsif ($temp =~ m/^(.*)\b(\d|\d\d|\d\d\d|$number)([^\t\d\)\,\;\+]*?)($perIdentifier) ?(\d?|$number)($levelDescriptor)? ?level(s?)(.*?)$/)
{
$incrVal = $2;
if ($incrVal == 0)
{
$incrVal = $atoi{$incrVal};
}
$diviser = $5;
if ($diviser ne "" && $diviser == 0)
{
$diviser = $atoi{$diviser};
}
$beforeEquation = $1;
$afterEquation  = $3 . $8;
($afterEquation, $casterLevel) = FixCasterLevelForAdjustment($afterEquation);
if ($diviser eq "")
{
$equation = "($casterLevel*" . $incrVal . ")";
}
elsif ($casterLevel ne "CASTERLEVEL")
{
$equation = "(floor($casterLevel/$diviser)*$incrVal)";
}
else
{
$equation = "(floor(max(1,($casterLevel/$diviser)))*" . $incrVal . ")";
}
($equation, $afterEquation) = FixCasterLevelForMaximumValue($beforeEquation, $equation, $afterEquation, $incrVal);
$beforeEquation = ParseCasterLevel($beforeEquation, $depth);
$afterEquation = ParseCasterLevel($afterEquation, $depth);
$temp = $beforeEquation . $equation . $afterEquation;
}
return $temp;
}
print "
while ( <> )
{
chomp;
$result = ParseCasterLevel($_, 0);
print $result . "\n";
}
