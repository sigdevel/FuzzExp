#!/usr/bin/env perl
my $flavour = shift;
my $output = shift;
open STDOUT,">$output" || die "can't open $output: $!";
my %GLOBALS;
my $dotinlocallabels=($flavour=~/linux/)?1:0;
my $globl = sub {
my $junk = shift;
my $name = shift;
my $global = \$GLOBALS{$name};
my $ret;
$name =~ s|^[\.\_]||;
SWITCH: for ($flavour) {
/aix/		&& do { $name = ".$name";
last;
};
/osx/		&& do { $name = "_$name";
last;
};
/linux.*32/	&& do {	$ret .= ".globl	$name\n";
$ret .= ".type	$name,\@function";
last;
};
/linux.*64/	&& do {	$ret .= ".globl	.$name\n";
$ret .= ".type	.$name,\@function\n";
$ret .= ".section	\".opd\",\"aw\"\n";
$ret .= ".globl	$name\n";
$ret .= ".align	3\n";
$ret .= "$name:\n";
$ret .= ".quad	.$name,.TOC.\@tocbase,0\n";
$ret .= ".size	$name,24\n";
$ret .= ".previous\n";
$name = ".$name";
last;
};
}
$ret = ".globl	$name" if (!$ret);
$$global = $name;
$ret;
};
my $text = sub {
($flavour =~ /aix/) ? ".csect" : ".text";
};
my $machine = sub {
my $junk = shift;
my $arch = shift;
if ($flavour =~ /osx/)
{	$arch =~ s/\"//g;
$arch = ($flavour=~/64/) ? "ppc970-64" : "ppc970" if ($arch eq "any");
}
".machine	$arch";
};
my $asciz = sub {
shift;
my $line = join(",",@_);
if ($line =~ /^"(.*)"$/)
{	".byte	" . join(",",unpack("C*",$1),0) . "\n.align	2";	}
else
{	"";	}
};
my $cmplw = sub {
my $f = shift;
my $cr = 0; $cr = shift if ($
($flavour =~ /linux.*32/) ?
"	.long	".sprintf "0x%x",31<<26|$cr<<23|$_[0]<<16|$_[1]<<11|64 :
"	cmplw	".join(',',$cr,@_);
};
my $bdnz = sub {
my $f = shift;
my $bo = $f=~/[\+\-]/ ? 16+9 : 16;
"	bc	$bo,0,".shift;
} if ($flavour!~/linux/);
my $bltlr = sub {
my $f = shift;
my $bo = $f=~/\-/ ? 12+2 : 12;
($flavour =~ /linux/) ?
"	.long	".sprintf "0x%x",19<<26|$bo<<21|16<<1 :
"	bclr	$bo,0";
};
my $bnelr = sub {
my $f = shift;
my $bo = $f=~/\-/ ? 4+2 : 4;
($flavour =~ /linux/) ?
"	.long	".sprintf "0x%x",19<<26|$bo<<21|2<<16|16<<1 :
"	bclr	$bo,2";
};
my $beqlr = sub {
my $f = shift;
my $bo = $f=~/-/ ? 12+2 : 12;
($flavour =~ /linux/) ?
"	.long	".sprintf "0x%X",19<<26|$bo<<21|2<<16|16<<1 :
"	bclr	$bo,2";
};
my $extrdi = sub {
my ($f,$ra,$rs,$n,$b) = @_;
$b = ($b+$n)&63; $n = 64-$n;
"	rldicl	$ra,$rs,$b,$n";
};
while($line=<>) {
$line =~ s|[
$line =~ s|/\*.*\*/||;
$line =~ s|^\s+||;
$line =~ s|\s+$||;
{
$line =~ s|\b\.L(\w+)|L$1|g;
$line =~ s|\bL(\w+)|\.L$1|g	if ($dotinlocallabels);
}
{
$line =~ s|(^[\.\w]+)\:\s*||;
my $label = $1;
printf "%s:",($GLOBALS{$label} or $label) if ($label);
}
{
$line =~ s|^\s*(\.?)(\w+)([\.\+\-]?)\s*||;
my $c = $1; $c = "\t" if ($c eq "");
my $mnemonic = $2;
my $f = $3;
my $opcode = eval("\$$mnemonic");
$line =~ s|\bc?[rf]([0-9]+)\b|$1|g if ($c ne "." and $flavour !~ /osx/);
if (ref($opcode) eq 'CODE') { $line = &$opcode($f,split(',',$line)); }
elsif ($mnemonic)           { $line = $c.$mnemonic.$f."\t".$line; }
}
print $line if ($line);
print "\n";
}
close STDOUT;
