#!/usr/bin/env perl
$flavour=shift;
$output=shift;
open STDOUT,">$output";
if ($output =~ /512/) {
$BITS=512;
$SZ=8;
@Sigma0=(28,34,39);
@Sigma1=(14,18,41);
@sigma0=(1,  8, 7);
@sigma1=(19,61, 6);
$rounds=80;
$reg_t="x";
} else {
$BITS=256;
$SZ=4;
@Sigma0=( 2,13,22);
@Sigma1=( 6,11,25);
@sigma0=( 7,18, 3);
@sigma1=(17,19,10);
$rounds=64;
$reg_t="w";
}
$func="sha${BITS}_block_data_order";
($ctx,$inp,$num,$Ktbl)=map("x$_",(0..2,30));
@X=map("$reg_t$_",(3..15,0..2));
@V=($A,$B,$C,$D,$E,$F,$G,$H)=map("$reg_t$_",(20..27));
($t0,$t1,$t2,$t3)=map("$reg_t$_",(16,17,19,28));
sub BODY_00_xx {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
my $j=($i+1)&15;
my ($T0,$T1,$T2)=(@X[($i-8)&15],@X[($i-9)&15],@X[($i-10)&15]);
$T0=@X[$i+3] if ($i<11);
$code.=<<___	if ($i<16);
rev	@X[$i],@X[$i]			// $i
___
$code.=<<___	if ($i<13 && ($i&1));
ldp	@X[$i+1],@X[$i+2],[$inp],
___
$code.=<<___	if ($i==13);
ldp	@X[14],@X[15],[$inp]
___
$code.=<<___	if ($i>=14);
ldr	@X[($i-11)&15],[sp,
___
$code.=<<___	if ($i>0 && $i<16);
add	$a,$a,$t1			// h+=Sigma0(a)
___
$code.=<<___	if ($i>=11);
str	@X[($i-8)&15],[sp,
___
$code.=<<___	if ($i<15);
ror	$t0,$e,
add	$h,$h,$t2			// h+=K[i]
eor	$T0,$e,$e,ror
and	$t1,$f,$e
bic	$t2,$g,$e
add	$h,$h,@X[$i&15]			// h+=X[i]
orr	$t1,$t1,$t2			// Ch(e,f,g)
eor	$t2,$a,$b			// a^b, b^c in next round
eor	$t0,$t0,$T0,ror
ror	$T0,$a,
add	$h,$h,$t1			// h+=Ch(e,f,g)
eor	$t1,$a,$a,ror
add	$h,$h,$t0			// h+=Sigma1(e)
and	$t3,$t3,$t2			// (b^c)&=(a^b)
add	$d,$d,$h			// d+=h
eor	$t3,$t3,$b			// Maj(a,b,c)
eor	$t1,$T0,$t1,ror
add	$h,$h,$t3			// h+=Maj(a,b,c)
ldr	$t3,[$Ktbl],
//add	$h,$h,$t1			// h+=Sigma0(a)
___
$code.=<<___	if ($i>=15);
ror	$t0,$e,
add	$h,$h,$t2			// h+=K[i]
ror	$T1,@X[($j+1)&15],
and	$t1,$f,$e
ror	$T2,@X[($j+14)&15],
bic	$t2,$g,$e
ror	$T0,$a,
add	$h,$h,@X[$i&15]			// h+=X[i]
eor	$t0,$t0,$e,ror
eor	$T1,$T1,@X[($j+1)&15],ror
orr	$t1,$t1,$t2			// Ch(e,f,g)
eor	$t2,$a,$b			// a^b, b^c in next round
eor	$t0,$t0,$e,ror
eor	$T0,$T0,$a,ror
add	$h,$h,$t1			// h+=Ch(e,f,g)
and	$t3,$t3,$t2			// (b^c)&=(a^b)
eor	$T2,$T2,@X[($j+14)&15],ror
eor	$T1,$T1,@X[($j+1)&15],lsr
add	$h,$h,$t0			// h+=Sigma1(e)
eor	$t3,$t3,$b			// Maj(a,b,c)
eor	$t1,$T0,$a,ror
eor	$T2,$T2,@X[($j+14)&15],lsr
add	@X[$j],@X[$j],@X[($j+9)&15]
add	$d,$d,$h			// d+=h
add	$h,$h,$t3			// h+=Maj(a,b,c)
ldr	$t3,[$Ktbl],
add	@X[$j],@X[$j],$T1
add	$h,$h,$t1			// h+=Sigma0(a)
add	@X[$j],@X[$j],$T2
___
($t2,$t3)=($t3,$t2);
}
$code.=<<___;
.text
.globl	$func
.type	$func,%function
.align	6
$func:
___
$code.=<<___	if ($SZ==4);
ldr	x16,.LOPENSSL_armcap_P
adr	x17,.LOPENSSL_armcap_P
add	x16,x16,x17
ldr	w16,[x16]
tst	w16,
b.ne	.Lv8_entry
___
$code.=<<___;
stp	x29,x30,[sp,
add	x29,sp,
stp	x19,x20,[sp,
stp	x21,x22,[sp,
stp	x23,x24,[sp,
stp	x25,x26,[sp,
stp	x27,x28,[sp,
sub	sp,sp,
ldp	$A,$B,[$ctx]				// load context
ldp	$C,$D,[$ctx,
ldp	$E,$F,[$ctx,
add	$num,$inp,$num,lsl
ldp	$G,$H,[$ctx,
adr	$Ktbl,K$BITS
stp	$ctx,$num,[x29,
.Loop:
ldp	@X[0],@X[1],[$inp],
ldr	$t2,[$Ktbl],
eor	$t3,$B,$C				// magic seed
str	$inp,[x29,
___
for ($i=0;$i<16;$i++)	{ &BODY_00_xx($i,@V); unshift(@V,pop(@V)); }
$code.=".Loop_16_xx:\n";
for (;$i<32;$i++)	{ &BODY_00_xx($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
cbnz	$t2,.Loop_16_xx
ldp	$ctx,$num,[x29,
ldr	$inp,[x29,
sub	$Ktbl,$Ktbl,
ldp	@X[0],@X[1],[$ctx]
ldp	@X[2],@X[3],[$ctx,
add	$inp,$inp,
ldp	@X[4],@X[5],[$ctx,
add	$A,$A,@X[0]
ldp	@X[6],@X[7],[$ctx,
add	$B,$B,@X[1]
add	$C,$C,@X[2]
add	$D,$D,@X[3]
stp	$A,$B,[$ctx]
add	$E,$E,@X[4]
add	$F,$F,@X[5]
stp	$C,$D,[$ctx,
add	$G,$G,@X[6]
add	$H,$H,@X[7]
cmp	$inp,$num
stp	$E,$F,[$ctx,
stp	$G,$H,[$ctx,
b.ne	.Loop
ldp	x19,x20,[x29,
add	sp,sp,
ldp	x21,x22,[x29,
ldp	x23,x24,[x29,
ldp	x25,x26,[x29,
ldp	x27,x28,[x29,
ldp	x29,x30,[sp],
ret
.size	$func,.-$func
.align	6
.type	K$BITS,%object
K$BITS:
___
$code.=<<___ if ($SZ==8);
.quad	0x428a2f98d728ae22,0x7137449123ef65cd
.quad	0xb5c0fbcfec4d3b2f,0xe9b5dba58189dbbc
.quad	0x3956c25bf348b538,0x59f111f1b605d019
.quad	0x923f82a4af194f9b,0xab1c5ed5da6d8118
.quad	0xd807aa98a3030242,0x12835b0145706fbe
.quad	0x243185be4ee4b28c,0x550c7dc3d5ffb4e2
.quad	0x72be5d74f27b896f,0x80deb1fe3b1696b1
.quad	0x9bdc06a725c71235,0xc19bf174cf692694
.quad	0xe49b69c19ef14ad2,0xefbe4786384f25e3
.quad	0x0fc19dc68b8cd5b5,0x240ca1cc77ac9c65
.quad	0x2de92c6f592b0275,0x4a7484aa6ea6e483
.quad	0x5cb0a9dcbd41fbd4,0x76f988da831153b5
.quad	0x983e5152ee66dfab,0xa831c66d2db43210
.quad	0xb00327c898fb213f,0xbf597fc7beef0ee4
.quad	0xc6e00bf33da88fc2,0xd5a79147930aa725
.quad	0x06ca6351e003826f,0x142929670a0e6e70
.quad	0x27b70a8546d22ffc,0x2e1b21385c26c926
.quad	0x4d2c6dfc5ac42aed,0x53380d139d95b3df
.quad	0x650a73548baf63de,0x766a0abb3c77b2a8
.quad	0x81c2c92e47edaee6,0x92722c851482353b
.quad	0xa2bfe8a14cf10364,0xa81a664bbc423001
.quad	0xc24b8b70d0f89791,0xc76c51a30654be30
.quad	0xd192e819d6ef5218,0xd69906245565a910
.quad	0xf40e35855771202a,0x106aa07032bbd1b8
.quad	0x19a4c116b8d2d0c8,0x1e376c085141ab53
.quad	0x2748774cdf8eeb99,0x34b0bcb5e19b48a8
.quad	0x391c0cb3c5c95a63,0x4ed8aa4ae3418acb
.quad	0x5b9cca4f7763e373,0x682e6ff3d6b2b8a3
.quad	0x748f82ee5defb2fc,0x78a5636f43172f60
.quad	0x84c87814a1f0ab72,0x8cc702081a6439ec
.quad	0x90befffa23631e28,0xa4506cebde82bde9
.quad	0xbef9a3f7b2c67915,0xc67178f2e372532b
.quad	0xca273eceea26619c,0xd186b8c721c0c207
.quad	0xeada7dd6cde0eb1e,0xf57d4f7fee6ed178
.quad	0x06f067aa72176fba,0x0a637dc5a2c898a6
.quad	0x113f9804bef90dae,0x1b710b35131c471b
.quad	0x28db77f523047d84,0x32caab7b40c72493
.quad	0x3c9ebe0a15c9bebc,0x431d67c49c100d4c
.quad	0x4cc5d4becb3e42b6,0x597f299cfc657e2a
.quad	0x5fcb6fab3ad6faec,0x6c44198c4a475817
.quad	0	// terminator
___
$code.=<<___ if ($SZ==4);
.long	0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5
.long	0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5
.long	0xd807aa98,0x12835b01,0x243185be,0x550c7dc3
.long	0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174
.long	0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc
.long	0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da
.long	0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7
.long	0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967
.long	0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13
.long	0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85
.long	0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3
.long	0xd192e819,0xd6990624,0xf40e3585,0x106aa070
.long	0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5
.long	0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3
.long	0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208
.long	0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
.long	0	//terminator
___
$code.=<<___;
.size	K$BITS,.-K$BITS
.align	3
.LOPENSSL_armcap_P:
.quad	OPENSSL_armcap_P-.
.asciz	"SHA$BITS block transform for ARMv8, CRYPTOGAMS by <appro\@openssl.org>"
.align	2
___
if ($SZ==4) {
my $Ktbl="x3";
my ($ABCD,$EFGH,$abcd)=map("v$_.16b",(0..2));
my @MSG=map("v$_.16b",(4..7));
my ($W0,$W1)=("v16.4s","v17.4s");
my ($ABCD_SAVE,$EFGH_SAVE)=("v18.16b","v19.16b");
$code.=<<___;
.type	sha256_block_armv8,%function
.align	6
sha256_block_armv8:
.Lv8_entry:
stp		x29,x30,[sp,
add		x29,sp,
ld1.32		{$ABCD,$EFGH},[$ctx]
adr		$Ktbl,K256
.Loop_hw:
ld1		{@MSG[0]-@MSG[3]},[$inp],
sub		$num,$num,
ld1.32		{$W0},[$Ktbl],
rev32		@MSG[0],@MSG[0]
rev32		@MSG[1],@MSG[1]
rev32		@MSG[2],@MSG[2]
rev32		@MSG[3],@MSG[3]
orr		$ABCD_SAVE,$ABCD,$ABCD		// offload
orr		$EFGH_SAVE,$EFGH,$EFGH
___
for($i=0;$i<12;$i++) {
$code.=<<___;
ld1.32		{$W1},[$Ktbl],
add.i32		$W0,$W0,@MSG[0]
sha256su0	@MSG[0],@MSG[1]
orr		$abcd,$ABCD,$ABCD
sha256h		$ABCD,$EFGH,$W0
sha256h2	$EFGH,$abcd,$W0
sha256su1	@MSG[0],@MSG[2],@MSG[3]
___
($W0,$W1)=($W1,$W0);	push(@MSG,shift(@MSG));
}
$code.=<<___;
ld1.32		{$W1},[$Ktbl],
add.i32		$W0,$W0,@MSG[0]
orr		$abcd,$ABCD,$ABCD
sha256h		$ABCD,$EFGH,$W0
sha256h2	$EFGH,$abcd,$W0
ld1.32		{$W0},[$Ktbl],
add.i32		$W1,$W1,@MSG[1]
orr		$abcd,$ABCD,$ABCD
sha256h		$ABCD,$EFGH,$W1
sha256h2	$EFGH,$abcd,$W1
ld1.32		{$W1},[$Ktbl]
add.i32		$W0,$W0,@MSG[2]
sub		$Ktbl,$Ktbl,
orr		$abcd,$ABCD,$ABCD
sha256h		$ABCD,$EFGH,$W0
sha256h2	$EFGH,$abcd,$W0
add.i32		$W1,$W1,@MSG[3]
orr		$abcd,$ABCD,$ABCD
sha256h		$ABCD,$EFGH,$W1
sha256h2	$EFGH,$abcd,$W1
add.i32		$ABCD,$ABCD,$ABCD_SAVE
add.i32		$EFGH,$EFGH,$EFGH_SAVE
cbnz		$num,.Loop_hw
st1.32		{$ABCD,$EFGH},[$ctx]
ldr		x29,[sp],
ret
.size	sha256_block_armv8,.-sha256_block_armv8
___
}
$code.=<<___;
.comm	OPENSSL_armcap_P,4,4
___
{   my  %opcode = (
"sha256h"	=> 0x5e004000,	"sha256h2"	=> 0x5e005000,
"sha256su0"	=> 0x5e282800,	"sha256su1"	=> 0x5e006000	);
sub unsha256 {
my ($mnemonic,$arg)=@_;
$arg =~ m/[qv]([0-9]+)[^,]*,\s*[qv]([0-9]+)[^,]*(?:,\s*[qv]([0-9]+))?/o
&&
sprintf ".inst\t0x%08x\t//%s %s",
$opcode{$mnemonic}|$1|($2<<5)|($3<<16),
$mnemonic,$arg;
}
}
foreach(split("\n",$code)) {
s/\`([^\`]*)\`/eval($1)/geo;
s/\b(sha256\w+)\s+([qv].*)/unsha256($1,$2)/geo;
s/\.\w?32\b//o		and s/\.16b/\.4s/go;
m/(ld|st)1[^\[]+\[0\]/o	and s/\.4s/\.s/go;
print $_,"\n";
}
close STDOUT;
