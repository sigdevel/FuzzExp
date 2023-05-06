#!/usr/bin/env perl
$hi=0;
$lo=4;
$output=shift;
open STDOUT,">$output";
$ctx="r0";
$inp="r1";
$len="r2";
$Tlo="r3";
$Thi="r4";
$Alo="r5";
$Ahi="r6";
$Elo="r7";
$Ehi="r8";
$t0="r9";
$t1="r10";
$t2="r11";
$t3="r12";
$Ktbl="r14";
$Aoff=8*0;
$Boff=8*1;
$Coff=8*2;
$Doff=8*3;
$Eoff=8*4;
$Foff=8*5;
$Goff=8*6;
$Hoff=8*7;
$Xoff=8*8;
sub BODY_00_15() {
my $magic = shift;
$code.=<<___;
ldr	$t2,[sp,
ldr	$t3,[sp,
@ Sigma1(x)	(ROTR((x),14) ^ ROTR((x),18)  ^ ROTR((x),41))
@ LO		lo>>14^hi<<18 ^ lo>>18^hi<<14 ^ hi>>9^lo<<23
@ HI		hi>>14^lo<<18 ^ hi>>18^lo<<14 ^ lo>>9^hi<<23
mov	$t0,$Elo,lsr
mov	$t1,$Ehi,lsr
eor	$t0,$t0,$Ehi,lsl
eor	$t1,$t1,$Elo,lsl
eor	$t0,$t0,$Elo,lsr
eor	$t1,$t1,$Ehi,lsr
eor	$t0,$t0,$Ehi,lsl
eor	$t1,$t1,$Elo,lsl
eor	$t0,$t0,$Ehi,lsr
eor	$t1,$t1,$Elo,lsr
eor	$t0,$t0,$Elo,lsl
eor	$t1,$t1,$Ehi,lsl
adds	$Tlo,$Tlo,$t0
adc	$Thi,$Thi,$t1		@ T += Sigma1(e)
adds	$Tlo,$Tlo,$t2
adc	$Thi,$Thi,$t3		@ T += h
ldr	$t0,[sp,
ldr	$t1,[sp,
ldr	$t2,[sp,
ldr	$t3,[sp,
str	$Elo,[sp,
str	$Ehi,[sp,
str	$Alo,[sp,
str	$Ahi,[sp,
eor	$t0,$t0,$t2
eor	$t1,$t1,$t3
and	$t0,$t0,$Elo
and	$t1,$t1,$Ehi
eor	$t0,$t0,$t2
eor	$t1,$t1,$t3		@ Ch(e,f,g)
ldr	$t2,[$Ktbl,
ldr	$t3,[$Ktbl,
ldr	$Elo,[sp,
ldr	$Ehi,[sp,
adds	$Tlo,$Tlo,$t0
adc	$Thi,$Thi,$t1		@ T += Ch(e,f,g)
adds	$Tlo,$Tlo,$t2
adc	$Thi,$Thi,$t3		@ T += K[i]
adds	$Elo,$Elo,$Tlo
adc	$Ehi,$Ehi,$Thi		@ d += T
and	$t0,$t2,
teq	$t0,
orreq	$Ktbl,$Ktbl,
ldr	$t2,[sp,
ldr	$t3,[sp,
@ Sigma0(x)	(ROTR((x),28) ^ ROTR((x),34) ^ ROTR((x),39))
@ LO		lo>>28^hi<<4  ^ hi>>2^lo<<30 ^ hi>>7^lo<<25
@ HI		hi>>28^lo<<4  ^ lo>>2^hi<<30 ^ lo>>7^hi<<25
mov	$t0,$Alo,lsr
mov	$t1,$Ahi,lsr
eor	$t0,$t0,$Ahi,lsl
eor	$t1,$t1,$Alo,lsl
eor	$t0,$t0,$Ahi,lsr
eor	$t1,$t1,$Alo,lsr
eor	$t0,$t0,$Alo,lsl
eor	$t1,$t1,$Ahi,lsl
eor	$t0,$t0,$Ahi,lsr
eor	$t1,$t1,$Alo,lsr
eor	$t0,$t0,$Alo,lsl
eor	$t1,$t1,$Ahi,lsl
adds	$Tlo,$Tlo,$t0
adc	$Thi,$Thi,$t1		@ T += Sigma0(a)
and	$t0,$Alo,$t2
orr	$Alo,$Alo,$t2
ldr	$t1,[sp,
ldr	$t2,[sp,
and	$Alo,$Alo,$t3
orr	$Alo,$Alo,$t0		@ Maj(a,b,c).lo
and	$t3,$Ahi,$t1
orr	$Ahi,$Ahi,$t1
and	$Ahi,$Ahi,$t2
orr	$Ahi,$Ahi,$t3		@ Maj(a,b,c).hi
adds	$Alo,$Alo,$Tlo
adc	$Ahi,$Ahi,$Thi		@ h += T
sub	sp,sp,
add	$Ktbl,$Ktbl,
___
}
$code=<<___;
.text
.code	32
.type	K512,%object
.align	5
K512:
.word	0x428a2f98,0xd728ae22, 0x71374491,0x23ef65cd
.word	0xb5c0fbcf,0xec4d3b2f, 0xe9b5dba5,0x8189dbbc
.word	0x3956c25b,0xf348b538, 0x59f111f1,0xb605d019
.word	0x923f82a4,0xaf194f9b, 0xab1c5ed5,0xda6d8118
.word	0xd807aa98,0xa3030242, 0x12835b01,0x45706fbe
.word	0x243185be,0x4ee4b28c, 0x550c7dc3,0xd5ffb4e2
.word	0x72be5d74,0xf27b896f, 0x80deb1fe,0x3b1696b1
.word	0x9bdc06a7,0x25c71235, 0xc19bf174,0xcf692694
.word	0xe49b69c1,0x9ef14ad2, 0xefbe4786,0x384f25e3
.word	0x0fc19dc6,0x8b8cd5b5, 0x240ca1cc,0x77ac9c65
.word	0x2de92c6f,0x592b0275, 0x4a7484aa,0x6ea6e483
.word	0x5cb0a9dc,0xbd41fbd4, 0x76f988da,0x831153b5
.word	0x983e5152,0xee66dfab, 0xa831c66d,0x2db43210
.word	0xb00327c8,0x98fb213f, 0xbf597fc7,0xbeef0ee4
.word	0xc6e00bf3,0x3da88fc2, 0xd5a79147,0x930aa725
.word	0x06ca6351,0xe003826f, 0x14292967,0x0a0e6e70
.word	0x27b70a85,0x46d22ffc, 0x2e1b2138,0x5c26c926
.word	0x4d2c6dfc,0x5ac42aed, 0x53380d13,0x9d95b3df
.word	0x650a7354,0x8baf63de, 0x766a0abb,0x3c77b2a8
.word	0x81c2c92e,0x47edaee6, 0x92722c85,0x1482353b
.word	0xa2bfe8a1,0x4cf10364, 0xa81a664b,0xbc423001
.word	0xc24b8b70,0xd0f89791, 0xc76c51a3,0x0654be30
.word	0xd192e819,0xd6ef5218, 0xd6990624,0x5565a910
.word	0xf40e3585,0x5771202a, 0x106aa070,0x32bbd1b8
.word	0x19a4c116,0xb8d2d0c8, 0x1e376c08,0x5141ab53
.word	0x2748774c,0xdf8eeb99, 0x34b0bcb5,0xe19b48a8
.word	0x391c0cb3,0xc5c95a63, 0x4ed8aa4a,0xe3418acb
.word	0x5b9cca4f,0x7763e373, 0x682e6ff3,0xd6b2b8a3
.word	0x748f82ee,0x5defb2fc, 0x78a5636f,0x43172f60
.word	0x84c87814,0xa1f0ab72, 0x8cc70208,0x1a6439ec
.word	0x90befffa,0x23631e28, 0xa4506ceb,0xde82bde9
.word	0xbef9a3f7,0xb2c67915, 0xc67178f2,0xe372532b
.word	0xca273ece,0xea26619c, 0xd186b8c7,0x21c0c207
.word	0xeada7dd6,0xcde0eb1e, 0xf57d4f7f,0xee6ed178
.word	0x06f067aa,0x72176fba, 0x0a637dc5,0xa2c898a6
.word	0x113f9804,0xbef90dae, 0x1b710b35,0x131c471b
.word	0x28db77f5,0x23047d84, 0x32caab7b,0x40c72493
.word	0x3c9ebe0a,0x15c9bebc, 0x431d67c4,0x9c100d4c
.word	0x4cc5d4be,0xcb3e42b6, 0x597f299c,0xfc657e2a
.word	0x5fcb6fab,0x3ad6faec, 0x6c44198c,0x4a475817
.size	K512,.-K512
.global	sha512_block_data_order
.type	sha512_block_data_order,%function
sha512_block_data_order:
sub	r3,pc,
add	$len,$inp,$len,lsl
stmdb	sp!,{r4-r12,lr}
sub	$Ktbl,r3,
sub	sp,sp,
ldr	$Elo,[$ctx,
ldr	$Ehi,[$ctx,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
.Loop:
str	$t0, [sp,
str	$t1, [sp,
str	$t2, [sp,
str	$t3, [sp,
ldr	$Alo,[$ctx,
ldr	$Ahi,[$ctx,
ldr	$Tlo,[$ctx,
ldr	$Thi,[$ctx,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
str	$Tlo,[sp,
str	$Thi,[sp,
str	$t0, [sp,
str	$t1, [sp,
str	$t2, [sp,
str	$t3, [sp,
ldr	$Tlo,[$ctx,
ldr	$Thi,[$ctx,
str	$Tlo,[sp,
str	$Thi,[sp,
.L00_15:
ldrb	$Tlo,[$inp,
ldrb	$t0, [$inp,
ldrb	$t1, [$inp,
ldrb	$t2, [$inp,
ldrb	$Thi,[$inp,
ldrb	$t3, [$inp,
orr	$Tlo,$Tlo,$t0,lsl
ldrb	$t0, [$inp,
orr	$Tlo,$Tlo,$t1,lsl
ldrb	$t1, [$inp],
orr	$Tlo,$Tlo,$t2,lsl
orr	$Thi,$Thi,$t3,lsl
orr	$Thi,$Thi,$t0,lsl
orr	$Thi,$Thi,$t1,lsl
str	$Tlo,[sp,
str	$Thi,[sp,
___
&BODY_00_15(0x94);
$code.=<<___;
tst	$Ktbl,
beq	.L00_15
bic	$Ktbl,$Ktbl,
.L16_79:
ldr	$t0,[sp,
ldr	$t1,[sp,
ldr	$t2,[sp,
ldr	$t3,[sp,
@ sigma0(x)	(ROTR((x),1)  ^ ROTR((x),8)  ^ ((x)>>7))
@ LO		lo>>1^hi<<31  ^ lo>>8^hi<<24 ^ lo>>7^hi<<25
@ HI		hi>>1^lo<<31  ^ hi>>8^lo<<24 ^ hi>>7
mov	$Tlo,$t0,lsr
mov	$Thi,$t1,lsr
eor	$Tlo,$Tlo,$t1,lsl
eor	$Thi,$Thi,$t0,lsl
eor	$Tlo,$Tlo,$t0,lsr
eor	$Thi,$Thi,$t1,lsr
eor	$Tlo,$Tlo,$t1,lsl
eor	$Thi,$Thi,$t0,lsl
eor	$Tlo,$Tlo,$t0,lsr
eor	$Thi,$Thi,$t1,lsr
eor	$Tlo,$Tlo,$t1,lsl
@ sigma1(x)	(ROTR((x),19) ^ ROTR((x),61) ^ ((x)>>6))
@ LO		lo>>19^hi<<13 ^ hi>>29^lo<<3 ^ lo>>6^hi<<26
@ HI		hi>>19^lo<<13 ^ lo>>29^hi<<3 ^ hi>>6
mov	$t0,$t2,lsr
mov	$t1,$t3,lsr
eor	$t0,$t0,$t3,lsl
eor	$t1,$t1,$t2,lsl
eor	$t0,$t0,$t3,lsr
eor	$t1,$t1,$t2,lsr
eor	$t0,$t0,$t2,lsl
eor	$t1,$t1,$t3,lsl
eor	$t0,$t0,$t2,lsr
eor	$t1,$t1,$t3,lsr
eor	$t0,$t0,$t3,lsl
ldr	$t2,[sp,
ldr	$t3,[sp,
adds	$Tlo,$Tlo,$t0
adc	$Thi,$Thi,$t1
ldr	$t0,[sp,
ldr	$t1,[sp,
adds	$Tlo,$Tlo,$t2
adc	$Thi,$Thi,$t3
adds	$Tlo,$Tlo,$t0
adc	$Thi,$Thi,$t1
str	$Tlo,[sp,
str	$Thi,[sp,
___
&BODY_00_15(0x17);
$code.=<<___;
tst	$Ktbl,
beq	.L16_79
bic	$Ktbl,$Ktbl,
ldr	$Tlo,[sp,
ldr	$Thi,[sp,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
adds	$t0,$Alo,$t0
adc	$t1,$Ahi,$t1
adds	$t2,$Tlo,$t2
adc	$t3,$Thi,$t3
str	$t0, [$ctx,
str	$t1, [$ctx,
str	$t2, [$ctx,
str	$t3, [$ctx,
ldr	$Alo,[sp,
ldr	$Ahi,[sp,
ldr	$Tlo,[sp,
ldr	$Thi,[sp,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
adds	$t0,$Alo,$t0
adc	$t1,$Ahi,$t1
adds	$t2,$Tlo,$t2
adc	$t3,$Thi,$t3
str	$t0, [$ctx,
str	$t1, [$ctx,
str	$t2, [$ctx,
str	$t3, [$ctx,
ldr	$Tlo,[sp,
ldr	$Thi,[sp,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
adds	$Elo,$Elo,$t0
adc	$Ehi,$Ehi,$t1
adds	$t2,$Tlo,$t2
adc	$t3,$Thi,$t3
str	$Elo,[$ctx,
str	$Ehi,[$ctx,
str	$t2, [$ctx,
str	$t3, [$ctx,
ldr	$Alo,[sp,
ldr	$Ahi,[sp,
ldr	$Tlo,[sp,
ldr	$Thi,[sp,
ldr	$t0, [$ctx,
ldr	$t1, [$ctx,
ldr	$t2, [$ctx,
ldr	$t3, [$ctx,
adds	$t0,$Alo,$t0
adc	$t1,$Ahi,$t1
adds	$t2,$Tlo,$t2
adc	$t3,$Thi,$t3
str	$t0, [$ctx,
str	$t1, [$ctx,
str	$t2, [$ctx,
str	$t3, [$ctx,
add	sp,sp,
sub	$Ktbl,$Ktbl,
teq	$inp,$len
bne	.Loop
add	sp,sp,
ldmia	sp!,{r4-r12,lr}
tst	lr,
moveq	pc,lr			@ be binary compatible with V4, yet
bx	lr			@ interoperable with Thumb ISA:-)
.size   sha512_block_data_order,.-sha512_block_data_order
.asciz  "SHA512 block transform for ARMv4, CRYPTOGAMS by <appro\@openssl.org>"
.align	2
___
$code =~ s/\`([^\`]*)\`/eval $1/gem;
$code =~ s/\bbx\s+lr\b/.word\t0xe12fff1e/gm;
print $code;
close STDOUT;
