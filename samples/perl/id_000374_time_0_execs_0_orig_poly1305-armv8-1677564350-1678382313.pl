#!/usr/bin/env perl
$flavour=shift;
$output=shift;
if ($flavour && $flavour ne "void") {
$0 =~ m/(.*[\/\\])[^\/\\]+$/; $dir=$1;
( $xlate="${dir}arm-xlate.pl" and -f $xlate ) or
( $xlate="${dir}../../perlasm/arm-xlate.pl" and -f $xlate) or
die "can't locate arm-xlate.pl";
open STDOUT,"| \"$^X\" $xlate $flavour $output";
} else {
open STDOUT,">$output";
}
my ($ctx,$inp,$len,$padbit) = map("x$_",(0..3));
my ($mac,$nonce)=($inp,$len);
my ($h0,$h1,$h2,$r0,$r1,$s1,$t0,$t1,$d0,$d1,$d2) = map("x$_",(4..14));
$code.=<<___;
.extern	OPENSSL_armcap_P
.text
// forward "declarations" are required for Apple
.globl	poly1305_blocks
.globl	poly1305_emit
.globl	poly1305_init
.type	poly1305_init,%function
.align	5
poly1305_init:
cmp	$inp,xzr
stp	xzr,xzr,[$ctx]		// zero hash value
stp	xzr,xzr,[$ctx,
csel	x0,xzr,x0,eq
b.eq	.Lno_key
adrp	x17,OPENSSL_armcap_P
ldr	w17,[x17,
ldp	$r0,$r1,[$inp]		// load key
mov	$s1,
movk	$s1,
rev	$r0,$r0			// flip bytes
rev	$r1,$r1
and	$r0,$r0,$s1		// &=0ffffffc0fffffff
and	$s1,$s1,
and	$r1,$r1,$s1		// &=0ffffffc0ffffffc
mov	w
stp	$r0,$r1,[$ctx,
str	w
tst	w17,
adr	$d0,.Lpoly1305_blocks
adr	$r0,.Lpoly1305_blocks_neon
adr	$d1,.Lpoly1305_emit
csel	$d0,$d0,$r0,eq
stp	w
stp	$d0,$d1,[$len]
mov	x0,
.Lno_key:
ret
.size	poly1305_init,.-poly1305_init
.type	poly1305_blocks,%function
.align	5
poly1305_blocks:
.Lpoly1305_blocks:
ands	$len,$len,
b.eq	.Lno_data
ldp	$h0,$h1,[$ctx]		// load hash value
ldp	$h2,x17,[$ctx,
ldp	$r0,$r1,[$ctx,
lsr	$d0,$h0,
mov	w
lsr	$d2,$h1,
mov	w15,w
lsr	x16,$h2,
mov	w
lsr	$d1,$h0,
mov	w
lsr	x15,$h1,
mov	w16,w
add	$d0,$d0,$d1,lsl
lsr	$d1,$d2,
adds	$d0,$d0,$d2,lsl
add	$d1,$d1,x15,lsl
adc	$d1,$d1,xzr
lsr	$d2,x16,
adds	$d1,$d1,x16,lsl
adc	$d2,$d2,xzr
cmp	x17,
add	$s1,$r1,$r1,lsr
csel	$h0,$h0,$d0,eq		// choose between radixes
csel	$h1,$h1,$d1,eq
csel	$h2,$h2,$d2,eq
.Loop:
ldp	$t0,$t1,[$inp],
sub	$len,$len,
rev	$t0,$t0
rev	$t1,$t1
adds	$h0,$h0,$t0		// accumulate input
adcs	$h1,$h1,$t1
mul	$d0,$h0,$r0		// h0*r0
adc	$h2,$h2,$padbit
umulh	$d1,$h0,$r0
mul	$t0,$h1,$s1		// h1*5*r1
umulh	$t1,$h1,$s1
adds	$d0,$d0,$t0
mul	$t0,$h0,$r1		// h0*r1
adc	$d1,$d1,$t1
umulh	$d2,$h0,$r1
adds	$d1,$d1,$t0
mul	$t0,$h1,$r0		// h1*r0
adc	$d2,$d2,xzr
umulh	$t1,$h1,$r0
adds	$d1,$d1,$t0
mul	$t0,$h2,$s1		// h2*5*r1
adc	$d2,$d2,$t1
mul	$t1,$h2,$r0		// h2*r0
adds	$d1,$d1,$t0
adc	$d2,$d2,$t1
and	$t0,$d2,
and	$h2,$d2,
add	$t0,$t0,$d2,lsr
adds	$h0,$d0,$t0
adcs	$h1,$d1,xzr
adc	$h2,$h2,xzr
cbnz	$len,.Loop
stp	$h0,$h1,[$ctx]		// store hash value
stp	$h2,xzr,[$ctx,
.Lno_data:
ret
.size	poly1305_blocks,.-poly1305_blocks
.type	poly1305_emit,%function
.align	5
poly1305_emit:
.Lpoly1305_emit:
ldp	$h0,$h1,[$ctx]		// load hash base 2^64
ldp	$h2,$r0,[$ctx,
ldp	$t0,$t1,[$nonce]	// load nonce
lsr	$d0,$h0,
mov	w
lsr	$d2,$h1,
mov	w15,w
lsr	x16,$h2,
mov	w
lsr	$d1,$h0,
mov	w
lsr	x15,$h1,
mov	w16,w
add	$d0,$d0,$d1,lsl
lsr	$d1,$d2,
adds	$d0,$d0,$d2,lsl
add	$d1,$d1,x15,lsl
adc	$d1,$d1,xzr
lsr	$d2,x16,
adds	$d1,$d1,x16,lsl
adc	$d2,$d2,xzr
cmp	$r0,
csel	$h0,$h0,$d0,eq		// choose between radixes
csel	$h1,$h1,$d1,eq
csel	$h2,$h2,$d2,eq
adds	$d0,$h0,
adcs	$d1,$h1,xzr
adc	$d2,$h2,xzr
tst	$d2,
csel	$h0,$h0,$d0,eq
csel	$h1,$h1,$d1,eq
ror	$t0,$t0,
ror	$t1,$t1,
adds	$h0,$h0,$t0		// accumulate nonce
adc	$h1,$h1,$t1
rev	$h0,$h0			// flip output bytes
rev	$h1,$h1
stp	$h0,$h1,[$mac]		// write result
ret
.size	poly1305_emit,.-poly1305_emit
___
my ($R0,$R1,$S1,$R2,$S2,$R3,$S3,$R4,$S4) = map("v$_.4s",(0..8));
my ($IN01_0,$IN01_1,$IN01_2,$IN01_3,$IN01_4) = map("v$_.2s",(9..13));
my ($IN23_0,$IN23_1,$IN23_2,$IN23_3,$IN23_4) = map("v$_.2s",(14..18));
my ($ACC0,$ACC1,$ACC2,$ACC3,$ACC4) = map("v$_.2d",(19..23));
my ($H0,$H1,$H2,$H3,$H4) = map("v$_.2s",(24..28));
my ($T0,$T1,$MASK) = map("v$_",(29..31));
my ($in2,$zeros)=("x16","x17");
my $is_base2_26 = $zeros;
$code.=<<___;
.type	poly1305_mult,%function
.align	5
poly1305_mult:
mul	$d0,$h0,$r0		// h0*r0
umulh	$d1,$h0,$r0
mul	$t0,$h1,$s1		// h1*5*r1
umulh	$t1,$h1,$s1
adds	$d0,$d0,$t0
mul	$t0,$h0,$r1		// h0*r1
adc	$d1,$d1,$t1
umulh	$d2,$h0,$r1
adds	$d1,$d1,$t0
mul	$t0,$h1,$r0		// h1*r0
adc	$d2,$d2,xzr
umulh	$t1,$h1,$r0
adds	$d1,$d1,$t0
mul	$t0,$h2,$s1		// h2*5*r1
adc	$d2,$d2,$t1
mul	$t1,$h2,$r0		// h2*r0
adds	$d1,$d1,$t0
adc	$d2,$d2,$t1
and	$t0,$d2,
and	$h2,$d2,
add	$t0,$t0,$d2,lsr
adds	$h0,$d0,$t0
adcs	$h1,$d1,xzr
adc	$h2,$h2,xzr
ret
.size	poly1305_mult,.-poly1305_mult
.type	poly1305_splat,%function
.align	4
poly1305_splat:
and	x12,$h0,
ubfx	x13,$h0,
extr	x14,$h1,$h0,
and	x14,x14,
ubfx	x15,$h1,
extr	x16,$h2,$h1,
str	w12,[$ctx,
add	w12,w13,w13,lsl
str	w13,[$ctx,
add	w13,w14,w14,lsl
str	w12,[$ctx,
str	w14,[$ctx,
add	w14,w15,w15,lsl
str	w13,[$ctx,
str	w15,[$ctx,
add	w15,w16,w16,lsl
str	w14,[$ctx,
str	w16,[$ctx,
str	w15,[$ctx,
ret
.size	poly1305_splat,.-poly1305_splat
.globl	poly1305_blocks_neon
.type	poly1305_blocks_neon,%function
.align	5
poly1305_blocks_neon:
.Lpoly1305_blocks_neon:
ldr	$is_base2_26,[$ctx,
cmp	$len,
b.lo	.Lpoly1305_blocks
.inst	0xd503233f		// paciasp
stp	x29,x30,[sp,
add	x29,sp,
stp	d8,d9,[sp,
stp	d10,d11,[sp,
stp	d12,d13,[sp,
stp	d14,d15,[sp,
cbz	$is_base2_26,.Lbase2_64_neon
ldp	w10,w11,[$ctx]		// load hash value base 2^26
ldp	w12,w13,[$ctx,
ldr	w14,[$ctx,
tst	$len,
b.eq	.Leven_neon
ldp	$r0,$r1,[$ctx,
add	$h0,x10,x11,lsl
lsr	$h1,x12,
adds	$h0,$h0,x12,lsl
add	$h1,$h1,x13,lsl
adc	$h1,$h1,xzr
lsr	$h2,x14,
adds	$h1,$h1,x14,lsl
adc	$d2,$h2,xzr		// can be partially reduced...
ldp	$d0,$d1,[$inp],
sub	$len,$len,
add	$s1,$r1,$r1,lsr
rev	$d0,$d0
rev	$d1,$d1
adds	$h0,$h0,$d0		// accumulate input
adcs	$h1,$h1,$d1
adc	$h2,$h2,$padbit
bl	poly1305_mult
and	x10,$h0,
ubfx	x11,$h0,
extr	x12,$h1,$h0,
and	x12,x12,
ubfx	x13,$h1,
extr	x14,$h2,$h1,
b	.Leven_neon
.align	4
.Lbase2_64_neon:
ldp	$r0,$r1,[$ctx,
ldp	$h0,$h1,[$ctx]		// load hash value base 2^64
ldr	$h2,[$ctx,
tst	$len,
b.eq	.Linit_neon
ldp	$d0,$d1,[$inp],
sub	$len,$len,
add	$s1,$r1,$r1,lsr
rev	$d0,$d0
rev	$d1,$d1
adds	$h0,$h0,$d0		// accumulate input
adcs	$h1,$h1,$d1
adc	$h2,$h2,$padbit
bl	poly1305_mult
.Linit_neon:
ldr	w17,[$ctx,
and	x10,$h0,
ubfx	x11,$h0,
extr	x12,$h1,$h0,
and	x12,x12,
ubfx	x13,$h1,
extr	x14,$h2,$h1,
cmp	w17,
b.ne	.Leven_neon
fmov	${H0},x10
fmov	${H1},x11
fmov	${H2},x12
fmov	${H3},x13
fmov	${H4},x14
////////////////////////////////// initialize r^n table
mov	$h0,$r0			// r^1
add	$s1,$r1,$r1,lsr
mov	$h1,$r1
mov	$h2,xzr
add	$ctx,$ctx,
bl	poly1305_splat
bl	poly1305_mult		// r^2
sub	$ctx,$ctx,
bl	poly1305_splat
bl	poly1305_mult		// r^3
sub	$ctx,$ctx,
bl	poly1305_splat
bl	poly1305_mult		// r^4
sub	$ctx,$ctx,
bl	poly1305_splat
sub	$ctx,$ctx,
b	.Ldo_neon
.align	4
.Leven_neon:
fmov	${H0},x10
fmov	${H1},x11
fmov	${H2},x12
fmov	${H3},x13
fmov	${H4},x14
.Ldo_neon:
ldp	x8,x12,[$inp,
subs	$len,$len,
ldp	x9,x13,[$inp,
add	$in2,$inp,
adr	$zeros,.Lzeros
lsl	$padbit,$padbit,
add	x15,$ctx,
rev	x8,x8
rev	x12,x12
rev	x9,x9
rev	x13,x13
and	x4,x8,
and	x5,x9,
ubfx	x6,x8,
ubfx	x7,x9,
add	x4,x4,x5,lsl
extr	x8,x12,x8,
extr	x9,x13,x9,
add	x6,x6,x7,lsl
fmov	$IN23_0,x4
and	x8,x8,
and	x9,x9,
ubfx	x10,x12,
ubfx	x11,x13,
add	x12,$padbit,x12,lsr
add	x13,$padbit,x13,lsr
add	x8,x8,x9,lsl
fmov	$IN23_1,x6
add	x10,x10,x11,lsl
add	x12,x12,x13,lsl
fmov	$IN23_2,x8
fmov	$IN23_3,x10
fmov	$IN23_4,x12
ldp	x8,x12,[$inp],
ldp	x9,x13,[$inp],
ld1	{$R0,$R1,$S1,$R2},[x15],
ld1	{$S2,$R3,$S3,$R4},[x15],
ld1	{$S4},[x15]
rev	x8,x8
rev	x12,x12
rev	x9,x9
rev	x13,x13
and	x4,x8,
and	x5,x9,
ubfx	x6,x8,
ubfx	x7,x9,
add	x4,x4,x5,lsl
extr	x8,x12,x8,
extr	x9,x13,x9,
add	x6,x6,x7,lsl
fmov	$IN01_0,x4
and	x8,x8,
and	x9,x9,
ubfx	x10,x12,
ubfx	x11,x13,
add	x12,$padbit,x12,lsr
add	x13,$padbit,x13,lsr
add	x8,x8,x9,lsl
fmov	$IN01_1,x6
add	x10,x10,x11,lsl
add	x12,x12,x13,lsl
movi	$MASK.2d,
fmov	$IN01_2,x8
fmov	$IN01_3,x10
fmov	$IN01_4,x12
ushr	$MASK.2d,$MASK.2d,
b.ls	.Lskip_loop
.align	4
.Loop_neon:
////////////////////////////////////////////////////////////////
// ((inp[0]*r^4+inp[2]*r^2+inp[4])*r^4+inp[6]*r^2
// ((inp[1]*r^4+inp[3]*r^2+inp[5])*r^3+inp[7]*r
//   \___________________/
// ((inp[0]*r^4+inp[2]*r^2+inp[4])*r^4+inp[6]*r^2+inp[8])*r^2
// ((inp[1]*r^4+inp[3]*r^2+inp[5])*r^4+inp[7]*r^2+inp[9])*r
//   \___________________/ \____________________/
//
// Note that we start with inp[2:3]*r^2. This is because it
// doesn't depend on reduction in previous iteration.
////////////////////////////////////////////////////////////////
// d4 = h0*r4 + h1*r3   + h2*r2   + h3*r1   + h4*r0
// d3 = h0*r3 + h1*r2   + h2*r1   + h3*r0   + h4*5*r4
// d2 = h0*r2 + h1*r1   + h2*r0   + h3*5*r4 + h4*5*r3
// d1 = h0*r1 + h1*r0   + h2*5*r4 + h3*5*r3 + h4*5*r2
// d0 = h0*r0 + h1*5*r4 + h2*5*r3 + h3*5*r2 + h4*5*r1
subs	$len,$len,
umull	$ACC4,$IN23_0,${R4}[2]
csel	$in2,$zeros,$in2,lo
umull	$ACC3,$IN23_0,${R3}[2]
umull	$ACC2,$IN23_0,${R2}[2]
ldp	x8,x12,[$in2],
umull	$ACC1,$IN23_0,${R1}[2]
ldp	x9,x13,[$in2],
umull	$ACC0,$IN23_0,${R0}[2]
rev	x8,x8
rev	x12,x12
rev	x9,x9
rev	x13,x13
umlal	$ACC4,$IN23_1,${R3}[2]
and	x4,x8,
umlal	$ACC3,$IN23_1,${R2}[2]
and	x5,x9,
umlal	$ACC2,$IN23_1,${R1}[2]
ubfx	x6,x8,
umlal	$ACC1,$IN23_1,${R0}[2]
ubfx	x7,x9,
umlal	$ACC0,$IN23_1,${S4}[2]
add	x4,x4,x5,lsl
umlal	$ACC4,$IN23_2,${R2}[2]
extr	x8,x12,x8,
umlal	$ACC3,$IN23_2,${R1}[2]
extr	x9,x13,x9,
umlal	$ACC2,$IN23_2,${R0}[2]
add	x6,x6,x7,lsl
umlal	$ACC1,$IN23_2,${S4}[2]
fmov	$IN23_0,x4
umlal	$ACC0,$IN23_2,${S3}[2]
and	x8,x8,
umlal	$ACC4,$IN23_3,${R1}[2]
and	x9,x9,
umlal	$ACC3,$IN23_3,${R0}[2]
ubfx	x10,x12,
umlal	$ACC2,$IN23_3,${S4}[2]
ubfx	x11,x13,
umlal	$ACC1,$IN23_3,${S3}[2]
add	x8,x8,x9,lsl
umlal	$ACC0,$IN23_3,${S2}[2]
fmov	$IN23_1,x6
add	$IN01_2,$IN01_2,$H2
add	x12,$padbit,x12,lsr
umlal	$ACC4,$IN23_4,${R0}[2]
add	x13,$padbit,x13,lsr
umlal	$ACC3,$IN23_4,${S4}[2]
add	x10,x10,x11,lsl
umlal	$ACC2,$IN23_4,${S3}[2]
add	x12,x12,x13,lsl
umlal	$ACC1,$IN23_4,${S2}[2]
fmov	$IN23_2,x8
umlal	$ACC0,$IN23_4,${S1}[2]
fmov	$IN23_3,x10
////////////////////////////////////////////////////////////////
// (hash+inp[0:1])*r^4 and accumulate
add	$IN01_0,$IN01_0,$H0
fmov	$IN23_4,x12
umlal	$ACC3,$IN01_2,${R1}[0]
ldp	x8,x12,[$inp],
umlal	$ACC0,$IN01_2,${S3}[0]
ldp	x9,x13,[$inp],
umlal	$ACC4,$IN01_2,${R2}[0]
umlal	$ACC1,$IN01_2,${S4}[0]
umlal	$ACC2,$IN01_2,${R0}[0]
rev	x8,x8
rev	x12,x12
rev	x9,x9
rev	x13,x13
add	$IN01_1,$IN01_1,$H1
umlal	$ACC3,$IN01_0,${R3}[0]
umlal	$ACC4,$IN01_0,${R4}[0]
and	x4,x8,
umlal	$ACC2,$IN01_0,${R2}[0]
and	x5,x9,
umlal	$ACC0,$IN01_0,${R0}[0]
ubfx	x6,x8,
umlal	$ACC1,$IN01_0,${R1}[0]
ubfx	x7,x9,
add	$IN01_3,$IN01_3,$H3
add	x4,x4,x5,lsl
umlal	$ACC3,$IN01_1,${R2}[0]
extr	x8,x12,x8,
umlal	$ACC4,$IN01_1,${R3}[0]
extr	x9,x13,x9,
umlal	$ACC0,$IN01_1,${S4}[0]
add	x6,x6,x7,lsl
umlal	$ACC2,$IN01_1,${R1}[0]
fmov	$IN01_0,x4
umlal	$ACC1,$IN01_1,${R0}[0]
and	x8,x8,
add	$IN01_4,$IN01_4,$H4
and	x9,x9,
umlal	$ACC3,$IN01_3,${R0}[0]
ubfx	x10,x12,
umlal	$ACC0,$IN01_3,${S2}[0]
ubfx	x11,x13,
umlal	$ACC4,$IN01_3,${R1}[0]
add	x8,x8,x9,lsl
umlal	$ACC1,$IN01_3,${S3}[0]
fmov	$IN01_1,x6
umlal	$ACC2,$IN01_3,${S4}[0]
add	x12,$padbit,x12,lsr
umlal	$ACC3,$IN01_4,${S4}[0]
add	x13,$padbit,x13,lsr
umlal	$ACC0,$IN01_4,${S1}[0]
add	x10,x10,x11,lsl
umlal	$ACC4,$IN01_4,${R0}[0]
add	x12,x12,x13,lsl
umlal	$ACC1,$IN01_4,${S2}[0]
fmov	$IN01_2,x8
umlal	$ACC2,$IN01_4,${S3}[0]
fmov	$IN01_3,x10
fmov	$IN01_4,x12
/////////////////////////////////////////////////////////////////
// lazy reduction as discussed in "NEON crypto" by D.J. Bernstein
// and P. Schwabe
//
// [see discussion in poly1305-armv4 module]
ushr	$T0.2d,$ACC3,
xtn	$H3,$ACC3
ushr	$T1.2d,$ACC0,
and	$ACC0,$ACC0,$MASK.2d
add	$ACC4,$ACC4,$T0.2d	// h3 -> h4
bic	$H3,
add	$ACC1,$ACC1,$T1.2d	// h0 -> h1
ushr	$T0.2d,$ACC4,
xtn	$H4,$ACC4
ushr	$T1.2d,$ACC1,
xtn	$H1,$ACC1
bic	$H4,
add	$ACC2,$ACC2,$T1.2d	// h1 -> h2
add	$ACC0,$ACC0,$T0.2d
shl	$T0.2d,$T0.2d,
shrn	$T1.2s,$ACC2,
xtn	$H2,$ACC2
add	$ACC0,$ACC0,$T0.2d	// h4 -> h0
bic	$H1,
add	$H3,$H3,$T1.2s		// h2 -> h3
bic	$H2,
shrn	$T0.2s,$ACC0,
xtn	$H0,$ACC0
ushr	$T1.2s,$H3,
bic	$H3,
bic	$H0,
add	$H1,$H1,$T0.2s		// h0 -> h1
add	$H4,$H4,$T1.2s		// h3 -> h4
b.hi	.Loop_neon
.Lskip_loop:
dup	$IN23_2,${IN23_2}[0]
add	$IN01_2,$IN01_2,$H2
////////////////////////////////////////////////////////////////
// multiply (inp[0:1]+hash) or inp[2:3] by r^2:r^1
adds	$len,$len,
b.ne	.Long_tail
dup	$IN23_2,${IN01_2}[0]
add	$IN23_0,$IN01_0,$H0
add	$IN23_3,$IN01_3,$H3
add	$IN23_1,$IN01_1,$H1
add	$IN23_4,$IN01_4,$H4
.Long_tail:
dup	$IN23_0,${IN23_0}[0]
umull2	$ACC0,$IN23_2,${S3}
umull2	$ACC3,$IN23_2,${R1}
umull2	$ACC4,$IN23_2,${R2}
umull2	$ACC2,$IN23_2,${R0}
umull2	$ACC1,$IN23_2,${S4}
dup	$IN23_1,${IN23_1}[0]
umlal2	$ACC0,$IN23_0,${R0}
umlal2	$ACC2,$IN23_0,${R2}
umlal2	$ACC3,$IN23_0,${R3}
umlal2	$ACC4,$IN23_0,${R4}
umlal2	$ACC1,$IN23_0,${R1}
dup	$IN23_3,${IN23_3}[0]
umlal2	$ACC0,$IN23_1,${S4}
umlal2	$ACC3,$IN23_1,${R2}
umlal2	$ACC2,$IN23_1,${R1}
umlal2	$ACC4,$IN23_1,${R3}
umlal2	$ACC1,$IN23_1,${R0}
dup	$IN23_4,${IN23_4}[0]
umlal2	$ACC3,$IN23_3,${R0}
umlal2	$ACC4,$IN23_3,${R1}
umlal2	$ACC0,$IN23_3,${S2}
umlal2	$ACC1,$IN23_3,${S3}
umlal2	$ACC2,$IN23_3,${S4}
umlal2	$ACC3,$IN23_4,${S4}
umlal2	$ACC0,$IN23_4,${S1}
umlal2	$ACC4,$IN23_4,${R0}
umlal2	$ACC1,$IN23_4,${S2}
umlal2	$ACC2,$IN23_4,${S3}
b.eq	.Lshort_tail
////////////////////////////////////////////////////////////////
// (hash+inp[0:1])*r^4:r^3 and accumulate
add	$IN01_0,$IN01_0,$H0
umlal	$ACC3,$IN01_2,${R1}
umlal	$ACC0,$IN01_2,${S3}
umlal	$ACC4,$IN01_2,${R2}
umlal	$ACC1,$IN01_2,${S4}
umlal	$ACC2,$IN01_2,${R0}
add	$IN01_1,$IN01_1,$H1
umlal	$ACC3,$IN01_0,${R3}
umlal	$ACC0,$IN01_0,${R0}
umlal	$ACC4,$IN01_0,${R4}
umlal	$ACC1,$IN01_0,${R1}
umlal	$ACC2,$IN01_0,${R2}
add	$IN01_3,$IN01_3,$H3
umlal	$ACC3,$IN01_1,${R2}
umlal	$ACC0,$IN01_1,${S4}
umlal	$ACC4,$IN01_1,${R3}
umlal	$ACC1,$IN01_1,${R0}
umlal	$ACC2,$IN01_1,${R1}
add	$IN01_4,$IN01_4,$H4
umlal	$ACC3,$IN01_3,${R0}
umlal	$ACC0,$IN01_3,${S2}
umlal	$ACC4,$IN01_3,${R1}
umlal	$ACC1,$IN01_3,${S3}
umlal	$ACC2,$IN01_3,${S4}
umlal	$ACC3,$IN01_4,${S4}
umlal	$ACC0,$IN01_4,${S1}
umlal	$ACC4,$IN01_4,${R0}
umlal	$ACC1,$IN01_4,${S2}
umlal	$ACC2,$IN01_4,${S3}
.Lshort_tail:
////////////////////////////////////////////////////////////////
// horizontal add
addp	$ACC3,$ACC3,$ACC3
ldp	d8,d9,[sp,
addp	$ACC0,$ACC0,$ACC0
ldp	d10,d11,[sp,
addp	$ACC4,$ACC4,$ACC4
ldp	d12,d13,[sp,
addp	$ACC1,$ACC1,$ACC1
ldp	d14,d15,[sp,
addp	$ACC2,$ACC2,$ACC2
ldr	x30,[sp,
.inst	0xd50323bf		// autiasp
////////////////////////////////////////////////////////////////
// lazy reduction, but without narrowing
ushr	$T0.2d,$ACC3,
and	$ACC3,$ACC3,$MASK.2d
ushr	$T1.2d,$ACC0,
and	$ACC0,$ACC0,$MASK.2d
add	$ACC4,$ACC4,$T0.2d	// h3 -> h4
add	$ACC1,$ACC1,$T1.2d	// h0 -> h1
ushr	$T0.2d,$ACC4,
and	$ACC4,$ACC4,$MASK.2d
ushr	$T1.2d,$ACC1,
and	$ACC1,$ACC1,$MASK.2d
add	$ACC2,$ACC2,$T1.2d	// h1 -> h2
add	$ACC0,$ACC0,$T0.2d
shl	$T0.2d,$T0.2d,
ushr	$T1.2d,$ACC2,
and	$ACC2,$ACC2,$MASK.2d
add	$ACC0,$ACC0,$T0.2d	// h4 -> h0
add	$ACC3,$ACC3,$T1.2d	// h2 -> h3
ushr	$T0.2d,$ACC0,
and	$ACC0,$ACC0,$MASK.2d
ushr	$T1.2d,$ACC3,
and	$ACC3,$ACC3,$MASK.2d
add	$ACC1,$ACC1,$T0.2d	// h0 -> h1
add	$ACC4,$ACC4,$T1.2d	// h3 -> h4
////////////////////////////////////////////////////////////////
// write the result, can be partially reduced
st4	{$ACC0,$ACC1,$ACC2,$ACC3}[0],[$ctx],
mov	x4,
st1	{$ACC4}[0],[$ctx]
str	x4,[$ctx,
ldr	x29,[sp],
ret
.size	poly1305_blocks_neon,.-poly1305_blocks_neon
.align	5
.Lzeros:
.long	0,0,0,0,0,0,0,0
.asciz	"Poly1305 for ARMv8, CRYPTOGAMS by \@dot-asm"
.align	2
.comm	OPENSSL_armcap_P,4,4
.hidden	OPENSSL_armcap_P
___
foreach (split("\n",$code)) {
s/\b(shrn\s+v[0-9]+)\.[24]d/$1.2s/			or
s/\b(fmov\s+)v([0-9]+)[^,]*,\s*x([0-9]+)/$1d$2,x$3/	or
(m/\bdup\b/ and (s/\.[24]s/.2d/g or 1))			or
(m/\b(eor|and)/ and (s/\.[248][sdh]/.16b/g or 1))	or
(m/\bum(ul|la)l\b/ and (s/\.4s/.2s/g or 1))		or
(m/\bum(ul|la)l2\b/ and (s/\.2s/.4s/g or 1))		or
(m/\bst[1-4]\s+{[^}]+}\[/ and (s/\.[24]d/.s/g or 1));
s/\.[124]([sd])\[/.$1\[/;
s/w
print $_,"\n";
}
close STDOUT;
