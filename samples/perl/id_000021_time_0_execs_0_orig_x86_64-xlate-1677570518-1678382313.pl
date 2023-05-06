#!/usr/bin/env perl
my $output = shift;
open STDOUT,">$output" || die "can't open $output: $!";
my $masm=1 if ($output =~ /\.asm/);
my $current_segment;
my $current_function;
{ package opcode;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
if ($line =~ /^([a-z]+)/i) {
$self->{op} = $1;
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
undef $self->{sz};
if ($self->{op} =~ /(movz)b.*/) {
$self->{op} = $1;
$self->{sz} = "b";
} elsif ($self->{op} =~ /([a-z]{3,})([qlwb])/) {
$self->{op} = $1;
$self->{sz} = $2;
}
}
$ret;
}
sub size {
my $self = shift;
my $sz   = shift;
$self->{sz} = $sz if (defined($sz) && !defined($self->{sz}));
$self->{sz};
}
sub out {
my $self = shift;
if (!$masm) {
if ($self->{op} eq "movz") {
sprintf "%s%s%s",$self->{op},$self->{sz},shift;
} elsif ($self->{op} eq "ret") {
".byte	0xf3,0xc3";
} else {
"$self->{op}$self->{sz}";
}
} else {
$self->{op} =~ s/movz/movzx/;
if ($self->{op} eq "ret") {
$self->{op} = "";
if ($current_function->{abi} eq "svr4") {
$self->{op} = "mov	rdi,QWORD PTR 8[rsp]\t;WIN64 epilogue\n\t".
"mov	rsi,QWORD PTR 16[rsp]\n\t";
}
$self->{op} .= "DB\t0F3h,0C3h\t\t;repret";
}
$self->{op};
}
}
}
{ package const;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
if ($line =~ /^\$([^,]+)/) {
$self->{value} = $1;
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
}
$ret;
}
sub out {
my $self = shift;
if (!$masm) {
sprintf "\$%s",$self->{value};
} else {
$self->{value} =~ s/0x([0-9a-f]+)/0$1h/ig;
sprintf "%s",$self->{value};
}
}
}
{ package ea;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
if ($line =~ /^([^\(,]*)\(([%\w,]+)\)/) {
$self->{label} = $1;
($self->{base},$self->{index},$self->{scale})=split(/,/,$2);
$self->{scale} = 1 if (!defined($self->{scale}));
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
$self->{base}  =~ s/^%//;
$self->{index} =~ s/^%// if (defined($self->{index}));
}
$ret;
}
sub size {}
sub out {
my $self = shift;
my $sz = shift;
if (!$masm) {
$self->{index} =~ s/^[er](.?[0-9xp])[d]?$/r\1/;
$self->{base}  =~ s/^[er](.?[0-9xp])[d]?$/r\1/;
$self->{label} =~ s/(?<![0-9a-f])(0[x0-9a-f]+)/oct($1)/eg;
$self->{label} =~ s/([0-9]+\s*[\*\/\%]\s*[0-9]+)/eval($1)/eg;
if (defined($self->{index})) {
sprintf "%s(%%%s,%%%s,%d)",
$self->{label},$self->{base},
$self->{index},$self->{scale};
} else {
sprintf "%s(%%%s)",	$self->{label},$self->{base};
}
} else {
%szmap = ( b=>"BYTE", w=>"WORD", l=>"DWORD", q=>"QWORD" );
$self->{label} =~ s/\./\$/g;
$self->{label} =~ s/0x([0-9a-f]+)/0$1h/ig;
$self->{label} = "($self->{label})" if ($self->{label} =~ /[\*\+\-\/]/);
if (defined($self->{index})) {
sprintf "%s PTR %s[%s*%d+%s]",$szmap{$sz},
$self->{label},
$self->{index},$self->{scale},
$self->{base};
} else {
sprintf "%s PTR %s[%s]",$szmap{$sz},
$self->{label},$self->{base};
}
}
}
}
{ package register;
sub re {
my	$class = shift;
my	$self = {};
local	*line = shift;
undef	$ret;
if ($line =~ /^%(\w+)/) {
bless $self,$class;
$self->{value} = $1;
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
}
$ret;
}
sub size {
my	$self = shift;
undef	$ret;
if    ($self->{value} =~ /^r[\d]+b$/i)	{ $ret="b"; }
elsif ($self->{value} =~ /^r[\d]+w$/i)	{ $ret="w"; }
elsif ($self->{value} =~ /^r[\d]+d$/i)	{ $ret="l"; }
elsif ($self->{value} =~ /^r[\w]+$/i)	{ $ret="q"; }
elsif ($self->{value} =~ /^[a-d][hl]$/i){ $ret="b"; }
elsif ($self->{value} =~ /^[\w]{2}l$/i)	{ $ret="b"; }
elsif ($self->{value} =~ /^[\w]{2}$/i)	{ $ret="w"; }
elsif ($self->{value} =~ /^e[a-z]{2}$/i){ $ret="l"; }
$ret;
}
sub out {
my $self = shift;
sprintf $masm?"%s":"%%%s",$self->{value};
}
}
{ package label;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
if ($line =~ /(^[\.\w]+\:)/) {
$self->{value} = $1;
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
$self->{value} =~ s/\.L/\$L/ if ($masm);
}
$ret;
}
sub out {
my $self = shift;
if (!$masm) {
$self->{value};
} elsif ($self->{value} ne "$current_function->{name}:") {
$self->{value};
} elsif ($current_function->{abi} eq "svr4") {
my $func =	"$current_function->{name}	PROC\n".
"	mov	QWORD PTR 8[rsp],rdi\t;WIN64 prologue\n".
"	mov	QWORD PTR 16[rsp],rsi\n";
my $narg = $current_function->{narg};
$narg=6 if (!defined($narg));
$func .= "	mov	rdi,rcx\n" if ($narg>0);
$func .= "	mov	rsi,rdx\n" if ($narg>1);
$func .= "	mov	rdx,r8\n"  if ($narg>2);
$func .= "	mov	rcx,r9\n"  if ($narg>3);
$func .= "	mov	r8,QWORD PTR 40[rsp]\n" if ($narg>4);
$func .= "	mov	r9,QWORD PTR 48[rsp]\n" if ($narg>5);
$func .= "\n";
} else {
"$current_function->{name}	PROC";
}
}
}
{ package expr;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
if ($line =~ /(^[^,]+)/) {
$self->{value} = $1;
$ret = $self;
$line = substr($line,@+[0]); $line =~ s/^\s+//;
$self->{value} =~ s/\.L/\$L/g if ($masm);
}
$ret;
}
sub out {
my $self = shift;
$self->{value};
}
}
{ package directive;
sub re {
my	$self = shift;
local	*line = shift;
undef	$ret;
my	$dir;
my	%opcode =
(	"%rax"=>0x01058d48,	"%rcx"=>0x010d8d48,
"%rdx"=>0x01158d48,	"%rbx"=>0x011d8d48,
"%rsp"=>0x01258d48,	"%rbp"=>0x012d8d48,
"%rsi"=>0x01358d48,	"%rdi"=>0x013d8d48,
"%r8" =>0x01058d4c,	"%r9" =>0x010d8d4c,
"%r10"=>0x01158d4c,	"%r11"=>0x011d8d4c,
"%r12"=>0x01258d4c,	"%r13"=>0x012d8d4c,
"%r14"=>0x01358d4c,	"%r15"=>0x013d8d4c	);
if ($line =~ /^\s*(\.\w+)/) {
if (!$masm) {
$self->{value} = $1;
$line =~ s/\@abi\-omnipotent/\@function/;
$line =~ s/\@function.*/\@function/;
if ($line =~ /\.picmeup\s+(%r[\w]+)/i) {
$self->{value} = sprintf "\t.long\t0x%x,0x90000000",$opcode{$1};
} else {
$self->{value} = $line;
}
$line = "";
return $self;
}
$dir = $1;
$ret = $self;
undef $self->{value};
$line = substr($line,@+[0]); $line =~ s/^\s+//;
SWITCH: for ($dir) {
/\.(text)/
&& do { my $v=undef;
$v="$current_segment\tENDS\n" if ($current_segment);
$current_segment = "_$1\$";
$current_segment =~ tr/[a-z]/[A-Z]/;
$v.="$current_segment\tSEGMENT ALIGN(64) 'CODE'";
$self->{value} = $v;
last;
};
/\.globl/   && do { $self->{value} = "PUBLIC\t".$line; last; };
/\.type/    && do { ($sym,$type,$narg) = split(',',$line);
if ($type eq "\@function") {
undef $current_function;
$current_function->{name} = $sym;
$current_function->{abi}  = "svr4";
$current_function->{narg} = $narg;
} elsif ($type eq "\@abi-omnipotent") {
undef $current_function;
$current_function->{name} = $sym;
}
last;
};
/\.size/    && do { if (defined($current_function)) {
$self->{value}="$current_function->{name}\tENDP";
undef $current_function;
}
last;
};
/\.align/   && do { $self->{value} = "ALIGN\t".$line; last; };
/\.(byte|value|long|quad)/
&& do { my @arr = split(',',$line);
my $sz  = substr($1,0,1);
my $last = pop(@arr);
$sz =~ tr/bvlq/BWDQ/;
$self->{value} = "\tD$sz\t";
for (@arr) { $self->{value} .= sprintf"0%Xh,",oct; }
$self->{value} .= sprintf"0%Xh",oct($last);
last;
};
/\.picmeup/ && do { $self->{value} = sprintf"\tDD\t 0%Xh,090000000h",$opcode{$line};
last;
};
}
$line = "";
}
$ret;
}
sub out {
my $self = shift;
$self->{value};
}
}
while($line=<>) {
chomp($line);
$line =~ s|[
$line =~ s|/\*.*\*/||;
$line =~ s|^\s+||;
undef $label;
undef $opcode;
undef $dst;
undef $src;
undef $sz;
if ($label=label->re(\$line))	{ print $label->out(); }
if (directive->re(\$line)) {
printf "%s",directive->out();
} elsif ($opcode=opcode->re(\$line)) { ARGUMENT: {
if ($src=register->re(\$line))	{ opcode->size($src->size()); }
elsif ($src=const->re(\$line))	{ }
elsif ($src=ea->re(\$line))	{ }
elsif ($src=expr->re(\$line))	{ }
last ARGUMENT if ($line !~ /^,/);
$line = substr($line,1); $line =~ s/^\s+//;
if ($dst=register->re(\$line))	{ opcode->size($dst->size()); }
elsif ($dst=const->re(\$line))	{ }
elsif ($dst=ea->re(\$line))	{ }
}
$sz=opcode->size();
if (defined($dst)) {
if (!$masm) {
printf "\t%s\t%s,%s",	$opcode->out($dst->size()),
$src->out($sz),$dst->out($sz);
} else {
printf "\t%s\t%s,%s",	$opcode->out(),
$dst->out($sz),$src->out($sz);
}
} elsif (defined($src)) {
printf "\t%s\t%s",$opcode->out(),$src->out($sz);
} else {
printf "\t%s",$opcode->out();
}
}
print $line,"\n";
}
print "\n$current_segment\tENDS\nEND\n" if ($masm);
close STDOUT;
