#!/usr/bin/env perl
$output=shift;
open STDOUT,">$output";
$inline=0;
$t0="r0";
$t1="r1";
$t2="r2";
$a="r3";
$b="r4";
$c="r5";
$d="r6";
$e="r7";
$K="r8";
$ctx="r9";
$inp="r10";
$len="r11";
$Xi="r12";
sub common {
<<___;
sub	$t0,
ldr	$t1,[$t0]
add	$e,$K			@ E+=K_xx_xx
lsl	$t2,$a,
add	$t2,$e
lsr	$e,$a,
add	$t2,$e			@ E+=ROR(A,27)
add	$t2,$t1			@ E+=X[i]
___
}
sub rotate {
<<___;
mov	$e,$d			@ E=D
mov	$d,$c			@ D=C
lsl	$c,$b,
lsr	$b,$b,
orr	$c,$b			@ C=ROR(B,2)
mov	$b,$a			@ B=A
add	$a,$t2,$t1		@ A=E+F_xx_xx(B,C,D)
___
}
sub BODY_00_19 {
$code.=$inline?&common():"\tbl	.Lcommon\n";
$code.=<<___;
mov	$t1,$c
eor	$t1,$d
and	$t1,$b
eor	$t1,$d			@ F_00_19(B,C,D)
___
$code.=$inline?&rotate():"\tbl	.Lrotate\n";
}
sub BODY_20_39 {
$code.=$inline?&common():"\tbl	.Lcommon\n";
$code.=<<___;
mov	$t1,$b
eor	$t1,$c
eor	$t1,$d			@ F_20_39(B,C,D)
___
$code.=$inline?&rotate():"\tbl	.Lrotate\n";
}
sub BODY_40_59 {
$code.=$inline?&common():"\tbl	.Lcommon\n";
$code.=<<___;
mov	$t1,$b
and	$t1,$c
mov	$e,$b
orr	$e,$c
and	$e,$d
orr	$t1,$e			@ F_40_59(B,C,D)
___
$code.=$inline?&rotate():"\tbl	.Lrotate\n";
}
$code=<<___;
.text
.code	16
.global	sha1_block_data_order
.type	sha1_block_data_order,%function
.align	2
sha1_block_data_order:
___
if ($cheat_on_binutils) {
$code.=<<___;
.code	32
add	r3,pc,
bx	r3			@ switch to Thumb ISA
.code	16
___
}
$code.=<<___;
push	{r4-r7}
mov	r3,r8
mov	r4,r9
mov	r5,r10
mov	r6,r11
mov	r7,r12
push	{r3-r7,lr}
lsl	r2,
mov	$ctx,r0			@ save context
mov	$inp,r1			@ save inp
mov	$len,r2			@ save len
add	$len,$inp		@ $len to point at inp end
.Lloop:
mov	$Xi,sp
mov	$t2,sp
sub	$t2,
.LXload:
ldrb	$a,[$t1,
ldrb	$b,[$t1,
ldrb	$c,[$t1,
ldrb	$d,[$t1,
lsl	$a,
lsl	$b,
lsl	$c,
orr	$a,$b
orr	$a,$c
orr	$a,$d
add	$t1,
push	{$a}
cmp	sp,$t2
bne	.LXload			@ [+14*16]
mov	$inp,$t1		@ update $inp
sub	$t2,
sub	$t2,
mov	$e,
.LXupdate:
ldr	$a,[sp,
ldr	$b,[sp,
ldr	$c,[sp,
ldr	$d,[sp,
eor	$a,$b
eor	$a,$c
eor	$a,$d
ror	$a,$e
push	{$a}
cmp	sp,$t2
bne	.LXupdate		@ [+(11+1)*64]
ldmia	$t0!,{$a,$b,$c,$d,$e}	@ $t0 is r0 and holds ctx
mov	$t0,$Xi
ldr	$t2,.LK_00_19
mov	$t1,$t0
sub	$t1,
mov	$Xi,$t1
mov	$K,$t2			@ [+7+4]
.L_00_19:
___
&BODY_00_19();
$code.=<<___;
cmp	$Xi,$t0
bne	.L_00_19		@ [+(2+9+4+2+8+2)*20]
ldr	$t2,.LK_20_39
mov	$t1,$t0
sub	$t1,
mov	$Xi,$t1
mov	$K,$t2			@ [+5]
.L_20_39_or_60_79:
___
&BODY_20_39();
$code.=<<___;
cmp	$Xi,$t0
bne	.L_20_39_or_60_79	@ [+(2+9+3+2+8+2)*20*2]
cmp	sp,$t0
beq	.Ldone			@ [+2]
ldr	$t2,.LK_40_59
mov	$t1,$t0
sub	$t1,
mov	$Xi,$t1
mov	$K,$t2			@ [+5]
.L_40_59:
___
&BODY_40_59();
$code.=<<___;
cmp	$Xi,$t0
bne	.L_40_59		@ [+(2+9+6+2+8+2)*20]
ldr	$t2,.LK_60_79
mov	$Xi,sp
mov	$K,$t2
b	.L_20_39_or_60_79	@ [+4]
.Ldone:
mov	$t0,$ctx
ldr	$t1,[$t0,
ldr	$t2,[$t0,
add	$a,$t1
ldr	$t1,[$t0,
add	$b,$t2
ldr	$t2,[$t0,
add	$c,$t1
ldr	$t1,[$t0,
add	$d,$t2
add	$e,$t1
stmia	$t0!,{$a,$b,$c,$d,$e}	@ [+20]
add	sp,
mov	$t0,$ctx		@ restore ctx
mov	$t1,$inp		@ restore inp
cmp	$t1,$len
beq	.Lexit
b	.Lloop			@ [+6] total 3212 cycles
.Lexit:
pop	{r2-r7}
mov	r8,r2
mov	r9,r3
mov	r10,r4
mov	r11,r5
mov	r12,r6
mov	lr,r7
pop	{r4-r7}
bx	lr
.align	2
___
$code.=".Lcommon:\n".&common()."\tmov	pc,lr\n" if (!$inline);
$code.=".Lrotate:\n".&rotate()."\tmov	pc,lr\n" if (!$inline);
$code.=<<___;
.align	2
.LK_00_19:	.word	0x5a827999
.LK_20_39:	.word	0x6ed9eba1
.LK_40_59:	.word	0x8f1bbcdc
.LK_60_79:	.word	0xca62c1d6
.size	sha1_block_data_order,.-sha1_block_data_order
.asciz	"SHA1 block transform for Thumb, CRYPTOGAMS by <appro\@openssl.org>"
___
print $code;
close STDOUT;
