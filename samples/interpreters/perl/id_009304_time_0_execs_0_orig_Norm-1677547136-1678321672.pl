sub normquery {
my ($in) = @_;
$in = " $in ";
$in =~ s/ (where|what|who)\s+(\S+)\s+(is|are) / $1 $3 $2 /i;
$in =~ s/ (where|what|who)\s+(.*)\s+(is|are) / $1 $3 $2 /i;
$in =~ s/^\s*(.*?)\s*/$1/;
$in =~ s/be tellin\'?g?/tell/i;
$in =~ s/ \'?bout/ about/i;
$in =~ s/,? any(hoo?w?|ways?)/ /ig;
$in =~ s/,?\s*(pretty )*please\??\s*$/\?/i;
if ($in =~
s/wh(at|ich)\s+(add?res?s|country|place|net (suffix|domain))/wh$1 /ig) {
if ((length($in) == 2) && ($in !~ /^\./)) {
$in = '.'.$in;
}
$in .= '?';
}
$in =~ s/th(e|at|is) (((m(o|u)th(a|er) ?)?fuck(in\'?g?)?|hell|heck|(god-?)?damn?(ed)?) ?)+//ig;
$in =~ s/wtf/where/gi;
$in =~ s/this (.*) thingy?/ $1/gi;
$in =~ s/this thingy? (called )?//gi;
$in =~ s/ha(s|ve) (an?y?|some|ne) (idea|clue|guess|seen) /know /ig;
$in =~ s/does (any|ne|some) ?(1|one|body) know //ig;
$in =~ s/do you know //ig;
$in =~ s/can (you|u|((any|ne|some) ?(1|one|body)))( please)? tell (me|us|him|her)//ig;
$in =~ s/where (\S+) can \S+ (a|an|the)?//ig;
$in =~ s/(can|do) (i|you|one|we|he|she) (find|get)( this)?/is/i;
$in =~ s/(i|one|we|he|she) can (find|get)/is/gi;
$in =~ s/(the )?(address|url) (for|to) //i;
$in =~ s/(where is )+/where is /ig;
$in =~ s/\s+/ /g;
$in =~ s/^\s+//;
if ($in =~ s/\s*[\/?!]*\?+\s*$//) {
$finalQMark = 1;
}
$in =~ s/\s+/ /g;
$in =~ s/^\s*(.*?)\s*$/$1/;
$in;
}
sub switchPerson {
my($in) = @_;
my $safeWho;
if ($target) {
$safeWho = &purifyNick($target);
} else {
$safeWho = &purifyNick($who);
}
$in =~ s/(^|\W)${safeWho}s\s+/$1${who}\'s /ig;
$in =~ s/(^|\W)${safeWho}s$/$1${who}\'s/ig;
$in =~ s/(^|\W)${safeWho}\'(\s|$)/$1${who}\'s$2/ig;
$in =~ s/(^|\s)i\'m(\W|$)/$1$who is$2/ig;
$in =~ s/(^|\s)i\'ve(\W|$)/$1$who has$2/ig;
$in =~ s/(^|\s)i have(\W|$)/$1$who has$2/ig;
$in =~ s/(^|\s)i haven\'?t(\W|$)/$1$who has not$2/ig;
$in =~ s/(^|\s)i(\W|$)/$1$who$2/ig;
$in =~ s/ am\b/ is/i;
$in =~ s/\bam /is/i;
$in =~ s/yourself/$param{'ident'}/i if ($addressed);
$in =~ s/(^|\s)(me|myself)(\W|$)/$1$who$3/ig;
$in =~ s/(^|\s)my(\W|$)/$1${who}\'s$2/ig;
$in =~ s/(^|\W)you\'?re(\W|$)/$1you are$2/ig;
if ($addressed > 0) {
$in =~ s/(^|\W)are you(\W|$)/$1is $param{'nick'}$2/ig;
$in =~ s/(^|\W)you are(\W|$)/$1$param{'nick'} is$2/ig;
$in =~ s/(^|\W)you(\W|$)/$1$param{'nick'}$2/ig;
$in =~ s/(^|\W)your(\W|$)/$1$param{'nick'}\'s$2/ig;
}
$in;
}
1;
