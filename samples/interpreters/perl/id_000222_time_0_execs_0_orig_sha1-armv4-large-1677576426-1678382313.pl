#!/usr/bin/env perl
$output=shift;
open STDOUT,">$output";
$ctx="r0";
$inp="r1";
$len="r2";
$a="r3";
$b="r4";
$c="r5";
$d="r6";
$e="r7";
$K="r8";
$t0="r9";
$t1="r10";
$t2="r11";
$t3="r12";
$Xi="r14";
@V=($a,$b,$c,$d,$e);
sub Xload {
my ($a,$b,$c,$d,$e)=@_;
$code.=<<___;
ldrb	$t0,[$inp],
ldrb	$t1,[$inp,
ldrb	$t2,[$inp,
ldrb	$t3,[$inp,
add	$e,$K,$e,ror
orr	$t0,$t1,$t0,lsl
add	$e,$e,$a,ror
orr	$t0,$t2,$t0,lsl
eor	$t1,$c,$d			@ F_xx_xx
orr	$t0,$t3,$t0,lsl
add	$e,$e,$t0			@ E+=X[i]
str	$t0,[$Xi,
___
}
sub Xupdate {
my ($a,$b,$c,$d,$e,$flag)=@_;
$code.=<<___;
ldr	$t0,[$Xi,
ldr	$t1,[$Xi,
ldr	$t2,[$Xi,
ldr	$t3,[$Xi,
add	$e,$K,$e,ror
eor	$t0,$t0,$t1
eor	$t0,$t0,$t2
eor	$t0,$t0,$t3
add	$e,$e,$a,ror
___
$code.=<<___ if (!defined($flag));
eor	$t1,$c,$d			@ F_xx_xx, but not in 40_59
___
$code.=<<___;
mov	$t0,$t0,ror
add	$e,$e,$t0			@ E+=X[i]
str	$t0,[$Xi,
___
}
sub BODY_00_15 {
my ($a,$b,$c,$d,$e)=@_;
&Xload(@_);
$code.=<<___;
and	$t1,$b,$t1,ror
eor	$t1,$t1,$d,ror
add	$e,$e,$t1			@ E+=F_00_19(B,C,D)
___
}
sub BODY_16_19 {
my ($a,$b,$c,$d,$e)=@_;
&Xupdate(@_);
$code.=<<___;
and	$t1,$b,$t1,ror
eor	$t1,$t1,$d,ror
add	$e,$e,$t1			@ E+=F_00_19(B,C,D)
___
}
sub BODY_20_39 {
my ($a,$b,$c,$d,$e)=@_;
&Xupdate(@_);
$code.=<<___;
eor	$t1,$b,$t1,ror
add	$e,$e,$t1			@ E+=F_20_39(B,C,D)
___
}
sub BODY_40_59 {
my ($a,$b,$c,$d,$e)=@_;
&Xupdate(@_,1);
$code.=<<___;
and	$t1,$b,$c,ror
orr	$t2,$b,$c,ror
and	$t2,$t2,$d,ror
orr	$t1,$t1,$t2			@ F_40_59(B,C,D)
add	$e,$e,$t1			@ E+=F_40_59(B,C,D)
___
}
$code=<<___;
.text
.global	sha1_block_data_order
.type	sha1_block_data_order,%function
.align	2
sha1_block_data_order:
stmdb	sp!,{r4-r12,lr}
add	$len,$inp,$len,lsl
ldmia	$ctx,{$a,$b,$c,$d,$e}
.Lloop:
ldr	$K,.LK_00_19
mov	$Xi,sp
sub	sp,sp,
mov	$c,$c,ror
mov	$d,$d,ror
mov	$e,$e,ror
.L_00_15:
___
for($i=0;$i<5;$i++) {
&BODY_00_15(@V);	unshift(@V,pop(@V));
}
$code.=<<___;
teq	$Xi,sp
bne	.L_00_15		@ [((11+4)*5+2)*3]
___
&BODY_00_15(@V);	unshift(@V,pop(@V));
&BODY_16_19(@V);	unshift(@V,pop(@V));
&BODY_16_19(@V);	unshift(@V,pop(@V));
&BODY_16_19(@V);	unshift(@V,pop(@V));
&BODY_16_19(@V);	unshift(@V,pop(@V));
$code.=<<___;
ldr	$K,.LK_20_39		@ [+15+16*4]
sub	sp,sp,
cmn	sp,
.L_20_39_or_60_79:
___
for($i=0;$i<5;$i++) {
&BODY_20_39(@V);	unshift(@V,pop(@V));
}
$code.=<<___;
teq	$Xi,sp			@ preserve carry
bne	.L_20_39_or_60_79	@ [+((12+3)*5+2)*4]
bcs	.L_done			@ [+((12+3)*5+2)*4], spare 300 bytes
ldr	$K,.LK_40_59
sub	sp,sp,
.L_40_59:
___
for($i=0;$i<5;$i++) {
&BODY_40_59(@V);	unshift(@V,pop(@V));
}
$code.=<<___;
teq	$Xi,sp
bne	.L_40_59		@ [+((12+5)*5+2)*4]
ldr	$K,.LK_60_79
sub	sp,sp,
cmp	sp,
b	.L_20_39_or_60_79	@ [+4], spare 300 bytes
.L_done:
add	sp,sp,
ldmia	$ctx,{$K,$t0,$t1,$t2,$t3}
add	$a,$K,$a
add	$b,$t0,$b
add	$c,$t1,$c,ror
add	$d,$t2,$d,ror
add	$e,$t3,$e,ror
stmia	$ctx,{$a,$b,$c,$d,$e}
teq	$inp,$len
bne	.Lloop			@ [+18], total 1307
ldmia	sp!,{r4-r12,lr}
tst	lr,
moveq	pc,lr			@ be binary compatible with V4, yet
bx	lr			@ interoperable with Thumb ISA:-)
.align	2
.LK_00_19:	.word	0x5a827999
.LK_20_39:	.word	0x6ed9eba1
.LK_40_59:	.word	0x8f1bbcdc
.LK_60_79:	.word	0xca62c1d6
.size	sha1_block_data_order,.-sha1_block_data_order
.asciz	"SHA1 block transform for ARMv4, CRYPTOGAMS by <appro\@openssl.org>"
.align	2
___
$code =~ s/\bbx\s+lr\b/.word\t0xe12fff1e/gm;
print $code;
close STDOUT;
