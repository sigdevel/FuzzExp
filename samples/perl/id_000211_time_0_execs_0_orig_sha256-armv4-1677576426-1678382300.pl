#!/usr/bin/env perl
$output=shift;
open STDOUT,">$output";
$ctx="r0";	$t0="r0";
$inp="r1";
$len="r2";	$t1="r2";
$T1="r3";
$A="r4";
$B="r5";
$C="r6";
$D="r7";
$E="r8";
$F="r9";
$G="r10";
$H="r11";
@V=($A,$B,$C,$D,$E,$F,$G,$H);
$t2="r12";
$Ktbl="r14";
@Sigma0=( 2,13,22);
@Sigma1=( 6,11,25);
@sigma0=( 7,18, 3);
@sigma1=(17,19,10);
sub BODY_00_15 {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h) = @_;
$code.=<<___ if ($i<16);
ldrb	$T1,[$inp,
ldrb	$t2,[$inp,
ldrb	$t1,[$inp,
ldrb	$t0,[$inp],
orr	$T1,$T1,$t2,lsl
orr	$T1,$T1,$t1,lsl
orr	$T1,$T1,$t0,lsl
`"str	$inp,[sp,
___
$code.=<<___;
ldr	$t2,[$Ktbl],
str	$T1,[sp,
mov	$t0,$e,ror
eor	$t0,$t0,$e,ror
eor	$t0,$t0,$e,ror
add	$T1,$T1,$t0
eor	$t1,$f,$g
and	$t1,$t1,$e
eor	$t1,$t1,$g			@ Ch(e,f,g)
add	$T1,$T1,$t1
add	$T1,$T1,$h
add	$T1,$T1,$t2
mov	$h,$a,ror
eor	$h,$h,$a,ror
eor	$h,$h,$a,ror
orr	$t0,$a,$b
and	$t0,$t0,$c
and	$t1,$a,$b
orr	$t0,$t0,$t1			@ Maj(a,b,c)
add	$h,$h,$t0
add	$d,$d,$T1
add	$h,$h,$T1
___
}
sub BODY_16_XX {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h) = @_;
$code.=<<___;
ldr	$t1,[sp,
ldr	$t2,[sp,
ldr	$T1,[sp,
ldr	$inp,[sp,
mov	$t0,$t1,ror
eor	$t0,$t0,$t1,ror
eor	$t0,$t0,$t1,lsr
mov	$t1,$t2,ror
eor	$t1,$t1,$t2,ror
eor	$t1,$t1,$t2,lsr
add	$T1,$T1,$t0
add	$T1,$T1,$t1
add	$T1,$T1,$inp
___
&BODY_00_15(@_);
}
$code=<<___;
.text
.code	32
.type	K256,%object
.align	5
K256:
.word	0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5
.word	0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5
.word	0xd807aa98,0x12835b01,0x243185be,0x550c7dc3
.word	0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174
.word	0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc
.word	0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da
.word	0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7
.word	0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967
.word	0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13
.word	0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85
.word	0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3
.word	0xd192e819,0xd6990624,0xf40e3585,0x106aa070
.word	0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5
.word	0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3
.word	0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208
.word	0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
.size	K256,.-K256
.global	sha256_block_data_order
.type	sha256_block_data_order,%function
sha256_block_data_order:
sub	r3,pc,
add	$len,$inp,$len,lsl
stmdb	sp!,{$ctx,$inp,$len,r4-r12,lr}
ldmia	$ctx,{$A,$B,$C,$D,$E,$F,$G,$H}
sub	$Ktbl,r3,
sub	sp,sp,
.Loop:
___
for($i=0;$i<16;$i++)	{ &BODY_00_15($i,@V); unshift(@V,pop(@V)); }
$code.=".Lrounds_16_xx:\n";
for (;$i<32;$i++)	{ &BODY_16_XX($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
and	$t2,$t2,
cmp	$t2,
bne	.Lrounds_16_xx
ldr	$T1,[sp,
ldr	$t0,[$T1,
ldr	$t1,[$T1,
ldr	$t2,[$T1,
add	$A,$A,$t0
ldr	$t0,[$T1,
add	$B,$B,$t1
ldr	$t1,[$T1,
add	$C,$C,$t2
ldr	$t2,[$T1,
add	$D,$D,$t0
ldr	$t0,[$T1,
add	$E,$E,$t1
ldr	$t1,[$T1,
add	$F,$F,$t2
ldr	$inp,[sp,
ldr	$t2,[sp,
add	$G,$G,$t0
add	$H,$H,$t1
stmia	$T1,{$A,$B,$C,$D,$E,$F,$G,$H}
cmp	$inp,$t2
sub	$Ktbl,$Ktbl,
bne	.Loop
add	sp,sp,
ldmia	sp!,{r4-r12,lr}
tst	lr,
moveq	pc,lr			@ be binary compatible with V4, yet
bx	lr			@ interoperable with Thumb ISA:-)
.size   sha256_block_data_order,.-sha256_block_data_order
.asciz  "SHA256 block transform for ARMv4, CRYPTOGAMS by <appro\@openssl.org>"
.align	2
___
$code =~ s/\`([^\`]*)\`/eval $1/gem;
$code =~ s/\bbx\s+lr\b/.word\t0xe12fff1e/gm;
print $code;
close STDOUT;
