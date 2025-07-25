#!/usr/bin/env perl
$bits=32;
for (@ARGV)	{ $bits=64 if (/\-m64/ || /\-xarch\=v9/); }
if ($bits==64)	{ $bias=2047; $frame=192; }
else		{ $bias=0;    $frame=112; }
$output=shift;
open STDOUT,">$output";
@X=("%o0","%o1","%o2","%o3","%o4","%o5","%g1","%o7");
$rot1m="%g2";
$tmp64="%g3";
$Xi="%g4";
$A="%l0";
$B="%l1";
$C="%l2";
$D="%l3";
$E="%l4";
@V=($A,$B,$C,$D,$E);
$K_00_19="%l5";
$K_20_39="%l6";
$K_40_59="%l7";
$K_60_79="%g5";
@K=($K_00_19,$K_20_39,$K_40_59,$K_60_79);
$ctx="%i0";
$inp="%i1";
$len="%i2";
$tmp0="%i3";
$tmp1="%i4";
$tmp2="%i5";
sub BODY_00_15 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $xi=($i&1)?@X[($i/2)%8]:$Xi;
$code.=<<___;
sll	$a,5,$tmp0		!! $i
add	@K[$i/20],$e,$e
srl	$a,27,$tmp1
add	$tmp0,$e,$e
and	$c,$b,$tmp0
add	$tmp1,$e,$e
sll	$b,30,$tmp2
andn	$d,$b,$tmp1
srl	$b,2,$b
or	$tmp1,$tmp0,$tmp1
or	$tmp2,$b,$b
add	$xi,$e,$e
___
if ($i&1 && $i<15) {
$code.=
"	srlx	@X[(($i+1)/2)%8],32,$Xi\n";
}
$code.=<<___;
add	$tmp1,$e,$e
___
}
sub Xupdate {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i/2;
if ($i&1) {
$code.=<<___;
sll	$a,5,$tmp0		!! $i
add	@K[$i/20],$e,$e
srl	$a,27,$tmp1
___
} else {
$code.=<<___;
sllx	@X[($j+6)%8],32,$Xi	! Xupdate($i)
xor	@X[($j+1)%8],@X[$j%8],@X[$j%8]
srlx	@X[($j+7)%8],32,$tmp1
xor	@X[($j+4)%8],@X[$j%8],@X[$j%8]
sll	$a,5,$tmp0		!! $i
or	$tmp1,$Xi,$Xi
add	@K[$i/20],$e,$e		!!
xor	$Xi,@X[$j%8],@X[$j%8]
srlx	@X[$j%8],31,$Xi
add	@X[$j%8],@X[$j%8],@X[$j%8]
and	$Xi,$rot1m,$Xi
andn	@X[$j%8],$rot1m,@X[$j%8]
srl	$a,27,$tmp1		!!
or	$Xi,@X[$j%8],@X[$j%8]
___
}
}
sub BODY_16_19 {
my ($i,$a,$b,$c,$d,$e)=@_;
&Xupdate(@_);
if ($i&1) {
$xi=@X[($i/2)%8];
} else {
$xi=$Xi;
$code.="\tsrlx	@X[($i/2)%8],32,$xi\n";
}
$code.=<<___;
add	$tmp0,$e,$e		!!
and	$c,$b,$tmp0
add	$tmp1,$e,$e
sll	$b,30,$tmp2
add	$xi,$e,$e
andn	$d,$b,$tmp1
srl	$b,2,$b
or	$tmp1,$tmp0,$tmp1
or	$tmp2,$b,$b
add	$tmp1,$e,$e
___
}
sub BODY_20_39 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $xi;
&Xupdate(@_);
if ($i&1) {
$xi=@X[($i/2)%8];
} else {
$xi=$Xi;
$code.="\tsrlx	@X[($i/2)%8],32,$xi\n";
}
$code.=<<___;
add	$tmp0,$e,$e		!!
xor	$c,$b,$tmp0
add	$tmp1,$e,$e
sll	$b,30,$tmp2
xor	$d,$tmp0,$tmp1
srl	$b,2,$b
add	$tmp1,$e,$e
or	$tmp2,$b,$b
add	$xi,$e,$e
___
}
sub BODY_40_59 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $xi;
&Xupdate(@_);
if ($i&1) {
$xi=@X[($i/2)%8];
} else {
$xi=$Xi;
$code.="\tsrlx	@X[($i/2)%8],32,$xi\n";
}
$code.=<<___;
add	$tmp0,$e,$e		!!
and	$c,$b,$tmp0
add	$tmp1,$e,$e
sll	$b,30,$tmp2
or	$c,$b,$tmp1
srl	$b,2,$b
and	$d,$tmp1,$tmp1
add	$xi,$e,$e
or	$tmp1,$tmp0,$tmp1
or	$tmp2,$b,$b
add	$tmp1,$e,$e
___
}
$code.=<<___ if ($bits==64);
.register	%g2,
.register	%g3,
___
$code.=<<___;
.section	".text",
.align	32
.globl	sha1_block_data_order
sha1_block_data_order:
save	%sp,-$frame,%sp
sllx	$len,6,$len
add	$inp,$len,$len
or	%g0,1,$rot1m
sllx	$rot1m,32,$rot1m
or	$rot1m,1,$rot1m
ld	[$ctx+0],$A
ld	[$ctx+4],$B
ld	[$ctx+8],$C
ld	[$ctx+12],$D
ld	[$ctx+16],$E
andn	$inp,7,$tmp0
sethi	%hi(0x5a827999),$K_00_19
or	$K_00_19,%lo(0x5a827999),$K_00_19
sethi	%hi(0x6ed9eba1),$K_20_39
or	$K_20_39,%lo(0x6ed9eba1),$K_20_39
sethi	%hi(0x8f1bbcdc),$K_40_59
or	$K_40_59,%lo(0x8f1bbcdc),$K_40_59
sethi	%hi(0xca62c1d6),$K_60_79
or	$K_60_79,%lo(0xca62c1d6),$K_60_79
.Lloop:
ldx	[$tmp0+0],@X[0]
ldx	[$tmp0+16],@X[2]
ldx	[$tmp0+32],@X[4]
ldx	[$tmp0+48],@X[6]
and	$inp,7,$tmp1
ldx	[$tmp0+8],@X[1]
sll	$tmp1,3,$tmp1
ldx	[$tmp0+24],@X[3]
subcc	%g0,$tmp1,$tmp2	! should be 64-$tmp1, but -$tmp1 works too
ldx	[$tmp0+40],@X[5]
bz,pt	%icc,.Laligned
ldx	[$tmp0+56],@X[7]
sllx	@X[0],$tmp1,@X[0]
ldx	[$tmp0+64],$tmp64
___
for($i=0;$i<7;$i++)
{   $code.=<<___;
srlx	@X[$i+1],$tmp2,$Xi
sllx	@X[$i+1],$tmp1,@X[$i+1]
or	$Xi,@X[$i],@X[$i]
___
}
$code.=<<___;
srlx	$tmp64,$tmp2,$tmp64
or	$tmp64,@X[7],@X[7]
.Laligned:
srlx	@X[0],32,$Xi
___
for ($i=0;$i<16;$i++)	{ &BODY_00_15($i,@V); unshift(@V,pop(@V)); }
for (;$i<20;$i++)	{ &BODY_16_19($i,@V); unshift(@V,pop(@V)); }
for (;$i<40;$i++)	{ &BODY_20_39($i,@V); unshift(@V,pop(@V)); }
for (;$i<60;$i++)	{ &BODY_40_59($i,@V); unshift(@V,pop(@V)); }
for (;$i<80;$i++)	{ &BODY_20_39($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
ld	[$ctx+0],@X[0]
ld	[$ctx+4],@X[1]
ld	[$ctx+8],@X[2]
ld	[$ctx+12],@X[3]
add	$inp,64,$inp
ld	[$ctx+16],@X[4]
cmp	$inp,$len
add	$A,@X[0],$A
st	$A,[$ctx+0]
add	$B,@X[1],$B
st	$B,[$ctx+4]
add	$C,@X[2],$C
st	$C,[$ctx+8]
add	$D,@X[3],$D
st	$D,[$ctx+12]
add	$E,@X[4],$E
st	$E,[$ctx+16]
bne	`$bits==64?"%xcc":"%icc"`,.Lloop
andn	$inp,7,$tmp0
ret
restore
.type	sha1_block_data_order,
.size	sha1_block_data_order,(.-sha1_block_data_order)
.asciz	"SHA1 block transform for SPARCv9, CRYPTOGAMS by <appro\@openssl.org>"
___
$code =~ s/\`([^\`]*)\`/eval $1/gem;
print $code;
close STDOUT;
