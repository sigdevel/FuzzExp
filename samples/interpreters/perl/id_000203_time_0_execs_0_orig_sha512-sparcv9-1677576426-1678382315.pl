#!/usr/bin/env perl
$bits=32;
for (@ARGV)	{ $bits=64 if (/\-m64/ || /\-xarch\=v9/); }
if ($bits==64)	{ $bias=2047; $frame=192; }
else		{ $bias=0;    $frame=112; }
$output=shift;
open STDOUT,">$output";
if ($output =~ /512/) {
$label="512";
$SZ=8;
$LD="ldx";
$ST="stx";
$SLL="sllx";
$SRL="srlx";
@Sigma0=(28,34,39);
@Sigma1=(14,18,41);
@sigma0=( 7, 1, 8);
@sigma1=( 6,19,61);
$lastK=0x817;
$rounds=80;
$align=4;
$locals=16*$SZ;
$A="%o0";
$B="%o1";
$C="%o2";
$D="%o3";
$E="%o4";
$F="%o5";
$G="%g1";
$H="%o7";
@V=($A,$B,$C,$D,$E,$F,$G,$H);
} else {
$label="256";
$SZ=4;
$LD="ld";
$ST="st";
$SLL="sll";
$SRL="srl";
@Sigma0=( 2,13,22);
@Sigma1=( 6,11,25);
@sigma0=( 3, 7,18);
@sigma1=(10,17,19);
$lastK=0x8f2;
$rounds=64;
$align=8;
$locals=0;
@X=("%o0","%o1","%o2","%o3","%o4","%o5","%g1","%o7");
$A="%l0";
$B="%l1";
$C="%l2";
$D="%l3";
$E="%l4";
$F="%l5";
$G="%l6";
$H="%l7";
@V=($A,$B,$C,$D,$E,$F,$G,$H);
}
$T1="%g2";
$tmp0="%g3";
$tmp1="%g4";
$tmp2="%g5";
$ctx="%i0";
$inp="%i1";
$len="%i2";
$Ktbl="%i3";
$tmp31="%i4";
$tmp32="%i5";
$Xload = sub {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
if ($i==0) {
$code.=<<___;
ldx	[$inp+0],@X[0]
ldx	[$inp+16],@X[2]
ldx	[$inp+32],@X[4]
ldx	[$inp+48],@X[6]
ldx	[$inp+8],@X[1]
ldx	[$inp+24],@X[3]
subcc	%g0,$tmp31,$tmp32 ! should be 64-$tmp31, but -$tmp31 works too
ldx	[$inp+40],@X[5]
bz,pt	%icc,.Laligned
ldx	[$inp+56],@X[7]
sllx	@X[0],$tmp31,@X[0]
ldx	[$inp+64],$T1
___
for($j=0;$j<7;$j++)
{   $code.=<<___;
srlx	@X[$j+1],$tmp32,$tmp1
sllx	@X[$j+1],$tmp31,@X[$j+1]
or	$tmp1,@X[$j],@X[$j]
___
}
$code.=<<___;
srlx	$T1,$tmp32,$T1
or	$T1,@X[7],@X[7]
.Laligned:
___
}
if ($i&1) {
$code.="\tadd	@X[$i/2],$h,$T1\n";
} else {
$code.="\tsrlx	@X[$i/2],32,$T1\n\tadd	$h,$T1,$T1\n";
}
} if ($SZ==4);
$Xload = sub {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
my @pair=("%l".eval(($i*2)%8),"%l".eval(($i*2)%8+1),"%l".eval((($i+1)*2)%8));
$code.=<<___ if ($i==0);
ld	[$inp+0],%l0
ld	[$inp+4],%l1
ld	[$inp+8],%l2
ld	[$inp+12],%l3
ld	[$inp+16],%l4
ld	[$inp+20],%l5
ld	[$inp+24],%l6
ld	[$inp+28],%l7
___
$code.=<<___ if ($i<15);
sllx	@pair[1],$tmp31,$tmp2	! Xload($i)
add	$tmp31,32,$tmp0
sllx	@pair[0],$tmp0,$tmp1
`"ld	[$inp+".eval(32+0+$i*8)."],@pair[0]"	if ($i<12)`
srlx	@pair[2],$tmp32,@pair[1]
or	$tmp1,$tmp2,$tmp2
or	@pair[1],$tmp2,$tmp2
`"ld	[$inp+".eval(32+4+$i*8)."],@pair[1]"	if ($i<12)`
add	$h,$tmp2,$T1
$ST	$tmp2,[%sp+`$bias+$frame+$i*$SZ`]
___
$code.=<<___ if ($i==12);
brnz,a	$tmp31,.+8
ld	[$inp+128],%l0
___
$code.=<<___ if ($i==15);
ld	[%sp+`$bias+$frame+(($i+1+1)%16)*$SZ+0`],%l2
sllx	@pair[1],$tmp31,$tmp2	! Xload($i)
add	$tmp31,32,$tmp0
ld	[%sp+`$bias+$frame+(($i+1+1)%16)*$SZ+4`],%l3
sllx	@pair[0],$tmp0,$tmp1
ld	[%sp+`$bias+$frame+(($i+1+9)%16)*$SZ+0`],%l4
srlx	@pair[2],$tmp32,@pair[1]
or	$tmp1,$tmp2,$tmp2
ld	[%sp+`$bias+$frame+(($i+1+9)%16)*$SZ+4`],%l5
or	@pair[1],$tmp2,$tmp2
ld	[%sp+`$bias+$frame+(($i+1+14)%16)*$SZ+0`],%l6
add	$h,$tmp2,$T1
$ST	$tmp2,[%sp+`$bias+$frame+$i*$SZ`]
ld	[%sp+`$bias+$frame+(($i+1+14)%16)*$SZ+4`],%l7
ld	[%sp+`$bias+$frame+(($i+1+0)%16)*$SZ+0`],%l0
ld	[%sp+`$bias+$frame+(($i+1+0)%16)*$SZ+4`],%l1
___
} if ($SZ==8);
sub BODY_00_15 {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
if ($i<16) {
&$Xload(@_);
} else {
$code.="\tadd	$h,$T1,$T1\n";
}
$code.=<<___;
$SRL	$e,@Sigma1[0],$h	!! $i
xor	$f,$g,$tmp2
$SLL	$e,`$SZ*8-@Sigma1[2]`,$tmp1
and	$e,$tmp2,$tmp2
$SRL	$e,@Sigma1[1],$tmp0
xor	$tmp1,$h,$h
$SLL	$e,`$SZ*8-@Sigma1[1]`,$tmp1
xor	$tmp0,$h,$h
$SRL	$e,@Sigma1[2],$tmp0
xor	$tmp1,$h,$h
$SLL	$e,`$SZ*8-@Sigma1[0]`,$tmp1
xor	$tmp0,$h,$h
xor	$g,$tmp2,$tmp2		! Ch(e,f,g)
xor	$tmp1,$h,$tmp0		! Sigma1(e)
$SRL	$a,@Sigma0[0],$h
add	$tmp2,$T1,$T1
$LD	[$Ktbl+`$i*$SZ`],$tmp2	! K[$i]
$SLL	$a,`$SZ*8-@Sigma0[2]`,$tmp1
add	$tmp0,$T1,$T1
$SRL	$a,@Sigma0[1],$tmp0
xor	$tmp1,$h,$h
$SLL	$a,`$SZ*8-@Sigma0[1]`,$tmp1
xor	$tmp0,$h,$h
$SRL	$a,@Sigma0[2],$tmp0
xor	$tmp1,$h,$h
$SLL	$a,`$SZ*8-@Sigma0[0]`,$tmp1
xor	$tmp0,$h,$h
xor	$tmp1,$h,$h		! Sigma0(a)
or	$a,$b,$tmp0
and	$a,$b,$tmp1
and	$c,$tmp0,$tmp0
or	$tmp0,$tmp1,$tmp1	! Maj(a,b,c)
add	$tmp2,$T1,$T1		! +=K[$i]
add	$tmp1,$h,$h
add	$T1,$d,$d
add	$T1,$h,$h
___
}
$BODY_16_XX = sub {
my $i=@_[0];
my $xi;
if ($i&1) {
$xi=$tmp32;
$code.="\tsrlx	@X[(($i+1)/2)%8],32,$xi\n";
} else {
$xi=@X[(($i+1)/2)%8];
}
$code.=<<___;
srl	$xi,@sigma0[0],$T1		!! Xupdate($i)
sll	$xi,`32-@sigma0[2]`,$tmp1
srl	$xi,@sigma0[1],$tmp0
xor	$tmp1,$T1,$T1
sll	$tmp1,`@sigma0[2]-@sigma0[1]`,$tmp1
xor	$tmp0,$T1,$T1
srl	$xi,@sigma0[2],$tmp0
xor	$tmp1,$T1,$T1
___
if ($i&1) {
$xi=@X[(($i+14)/2)%8];
} else {
$xi=$tmp32;
$code.="\tsrlx	@X[(($i+14)/2)%8],32,$xi\n";
}
$code.=<<___;
srl	$xi,@sigma1[0],$tmp2
xor	$tmp0,$T1,$T1			! T1=sigma0(X[i+1])
sll	$xi,`32-@sigma1[2]`,$tmp1
srl	$xi,@sigma1[1],$tmp0
xor	$tmp1,$tmp2,$tmp2
sll	$tmp1,`@sigma1[2]-@sigma1[1]`,$tmp1
xor	$tmp0,$tmp2,$tmp2
srl	$xi,@sigma1[2],$tmp0
xor	$tmp1,$tmp2,$tmp2
___
if ($i&1) {
$xi=@X[($i/2)%8];
$code.=<<___;
srlx	@X[(($i+9)/2)%8],32,$tmp1	! X[i+9]
xor	$tmp0,$tmp2,$tmp2		! sigma1(X[i+14])
srl	@X[($i/2)%8],0,$tmp0
add	$xi,$T1,$T1			! +=X[i]
xor	$tmp0,@X[($i/2)%8],@X[($i/2)%8]
add	$tmp2,$T1,$T1
add	$tmp1,$T1,$T1
srl	$T1,0,$T1
or	$T1,@X[($i/2)%8],@X[($i/2)%8]
___
} else {
$xi=@X[(($i+9)/2)%8];
$code.=<<___;
srlx	@X[($i/2)%8],32,$tmp1		! X[i]
xor	$tmp0,$tmp2,$tmp2		! sigma1(X[i+14])
srl	@X[($i/2)%8],0,@X[($i/2)%8]
add	$xi,$T1,$T1			! +=X[i+9]
add	$tmp2,$T1,$T1
add	$tmp1,$T1,$T1
sllx	$T1,32,$tmp0
or	$tmp0,@X[($i/2)%8],@X[($i/2)%8]
___
}
&BODY_00_15(@_);
} if ($SZ==4);
$BODY_16_XX = sub {
my $i=@_[0];
my @pair=("%l".eval(($i*2)%8),"%l".eval(($i*2)%8+1));
$code.=<<___;
sllx	%l2,32,$tmp0		!! Xupdate($i)
or	%l3,$tmp0,$tmp0
srlx	$tmp0,@sigma0[0],$T1
ld	[%sp+`$bias+$frame+(($i+1+1)%16)*$SZ+0`],%l2
sllx	$tmp0,`64-@sigma0[2]`,$tmp1
ld	[%sp+`$bias+$frame+(($i+1+1)%16)*$SZ+4`],%l3
srlx	$tmp0,@sigma0[1],$tmp0
xor	$tmp1,$T1,$T1
sllx	$tmp1,`@sigma0[2]-@sigma0[1]`,$tmp1
xor	$tmp0,$T1,$T1
srlx	$tmp0,`@sigma0[2]-@sigma0[1]`,$tmp0
xor	$tmp1,$T1,$T1
sllx	%l6,32,$tmp2
xor	$tmp0,$T1,$T1		! sigma0(X[$i+1])
or	%l7,$tmp2,$tmp2
srlx	$tmp2,@sigma1[0],$tmp1
ld	[%sp+`$bias+$frame+(($i+1+14)%16)*$SZ+0`],%l6
sllx	$tmp2,`64-@sigma1[2]`,$tmp0
ld	[%sp+`$bias+$frame+(($i+1+14)%16)*$SZ+4`],%l7
srlx	$tmp2,@sigma1[1],$tmp2
xor	$tmp0,$tmp1,$tmp1
sllx	$tmp0,`@sigma1[2]-@sigma1[1]`,$tmp0
xor	$tmp2,$tmp1,$tmp1
srlx	$tmp2,`@sigma1[2]-@sigma1[1]`,$tmp2
xor	$tmp0,$tmp1,$tmp1
sllx	%l4,32,$tmp0
xor	$tmp2,$tmp1,$tmp1	! sigma1(X[$i+14])
ld	[%sp+`$bias+$frame+(($i+1+9)%16)*$SZ+0`],%l4
or	%l5,$tmp0,$tmp0
ld	[%sp+`$bias+$frame+(($i+1+9)%16)*$SZ+4`],%l5
sllx	%l0,32,$tmp2
add	$tmp1,$T1,$T1
ld	[%sp+`$bias+$frame+(($i+1+0)%16)*$SZ+0`],%l0
or	%l1,$tmp2,$tmp2
add	$tmp0,$T1,$T1		! +=X[$i+9]
ld	[%sp+`$bias+$frame+(($i+1+0)%16)*$SZ+4`],%l1
add	$tmp2,$T1,$T1		! +=X[$i]
$ST	$T1,[%sp+`$bias+$frame+($i%16)*$SZ`]
___
&BODY_00_15(@_);
} if ($SZ==8);
$code.=<<___ if ($bits==64);
.register	%g2,
.register	%g3,
___
$code.=<<___;
.section	".text",
.align	64
K${label}:
.type	K${label},
___
if ($SZ==4) {
$code.=<<___;
.long	0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5
.long	0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5
.long	0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3
.long	0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174
.long	0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc
.long	0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da
.long	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7
.long	0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967
.long	0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13
.long	0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85
.long	0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3
.long	0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070
.long	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5
.long	0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3
.long	0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208
.long	0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
___
} else {
$code.=<<___;
.long	0x428a2f98,0xd728ae22, 0x71374491,0x23ef65cd
.long	0xb5c0fbcf,0xec4d3b2f, 0xe9b5dba5,0x8189dbbc
.long	0x3956c25b,0xf348b538, 0x59f111f1,0xb605d019
.long	0x923f82a4,0xaf194f9b, 0xab1c5ed5,0xda6d8118
.long	0xd807aa98,0xa3030242, 0x12835b01,0x45706fbe
.long	0x243185be,0x4ee4b28c, 0x550c7dc3,0xd5ffb4e2
.long	0x72be5d74,0xf27b896f, 0x80deb1fe,0x3b1696b1
.long	0x9bdc06a7,0x25c71235, 0xc19bf174,0xcf692694
.long	0xe49b69c1,0x9ef14ad2, 0xefbe4786,0x384f25e3
.long	0x0fc19dc6,0x8b8cd5b5, 0x240ca1cc,0x77ac9c65
.long	0x2de92c6f,0x592b0275, 0x4a7484aa,0x6ea6e483
.long	0x5cb0a9dc,0xbd41fbd4, 0x76f988da,0x831153b5
.long	0x983e5152,0xee66dfab, 0xa831c66d,0x2db43210
.long	0xb00327c8,0x98fb213f, 0xbf597fc7,0xbeef0ee4
.long	0xc6e00bf3,0x3da88fc2, 0xd5a79147,0x930aa725
.long	0x06ca6351,0xe003826f, 0x14292967,0x0a0e6e70
.long	0x27b70a85,0x46d22ffc, 0x2e1b2138,0x5c26c926
.long	0x4d2c6dfc,0x5ac42aed, 0x53380d13,0x9d95b3df
.long	0x650a7354,0x8baf63de, 0x766a0abb,0x3c77b2a8
.long	0x81c2c92e,0x47edaee6, 0x92722c85,0x1482353b
.long	0xa2bfe8a1,0x4cf10364, 0xa81a664b,0xbc423001
.long	0xc24b8b70,0xd0f89791, 0xc76c51a3,0x0654be30
.long	0xd192e819,0xd6ef5218, 0xd6990624,0x5565a910
.long	0xf40e3585,0x5771202a, 0x106aa070,0x32bbd1b8
.long	0x19a4c116,0xb8d2d0c8, 0x1e376c08,0x5141ab53
.long	0x2748774c,0xdf8eeb99, 0x34b0bcb5,0xe19b48a8
.long	0x391c0cb3,0xc5c95a63, 0x4ed8aa4a,0xe3418acb
.long	0x5b9cca4f,0x7763e373, 0x682e6ff3,0xd6b2b8a3
.long	0x748f82ee,0x5defb2fc, 0x78a5636f,0x43172f60
.long	0x84c87814,0xa1f0ab72, 0x8cc70208,0x1a6439ec
.long	0x90befffa,0x23631e28, 0xa4506ceb,0xde82bde9
.long	0xbef9a3f7,0xb2c67915, 0xc67178f2,0xe372532b
.long	0xca273ece,0xea26619c, 0xd186b8c7,0x21c0c207
.long	0xeada7dd6,0xcde0eb1e, 0xf57d4f7f,0xee6ed178
.long	0x06f067aa,0x72176fba, 0x0a637dc5,0xa2c898a6
.long	0x113f9804,0xbef90dae, 0x1b710b35,0x131c471b
.long	0x28db77f5,0x23047d84, 0x32caab7b,0x40c72493
.long	0x3c9ebe0a,0x15c9bebc, 0x431d67c4,0x9c100d4c
.long	0x4cc5d4be,0xcb3e42b6, 0x597f299c,0xfc657e2a
.long	0x5fcb6fab,0x3ad6faec, 0x6c44198c,0x4a475817
___
}
$code.=<<___;
.size	K${label},.-K${label}
.globl	sha${label}_block_data_order
sha${label}_block_data_order:
save	%sp,`-$frame-$locals`,%sp
and	$inp,`$align-1`,$tmp31
sllx	$len,`log(16*$SZ)/log(2)`,$len
andn	$inp,`$align-1`,$inp
sll	$tmp31,3,$tmp31
add	$inp,$len,$len
___
$code.=<<___ if ($SZ==8);
mov	32,$tmp32
sub	$tmp32,$tmp31,$tmp32
___
$code.=<<___;
.Lpic:	call	.+8
add	%o7,K${label}-.Lpic,$Ktbl
$LD	[$ctx+`0*$SZ`],$A
$LD	[$ctx+`1*$SZ`],$B
$LD	[$ctx+`2*$SZ`],$C
$LD	[$ctx+`3*$SZ`],$D
$LD	[$ctx+`4*$SZ`],$E
$LD	[$ctx+`5*$SZ`],$F
$LD	[$ctx+`6*$SZ`],$G
$LD	[$ctx+`7*$SZ`],$H
.Lloop:
___
for ($i=0;$i<16;$i++)	{ &BODY_00_15($i,@V); unshift(@V,pop(@V)); }
$code.=".L16_xx:\n";
for (;$i<32;$i++)	{ &$BODY_16_XX($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
and	$tmp2,0xfff,$tmp2
cmp	$tmp2,$lastK
bne	.L16_xx
add	$Ktbl,`16*$SZ`,$Ktbl	! Ktbl+=16
___
$code.=<<___ if ($SZ==4);
$LD	[$ctx+`0*$SZ`],@X[0]
$LD	[$ctx+`1*$SZ`],@X[1]
$LD	[$ctx+`2*$SZ`],@X[2]
$LD	[$ctx+`3*$SZ`],@X[3]
$LD	[$ctx+`4*$SZ`],@X[4]
$LD	[$ctx+`5*$SZ`],@X[5]
$LD	[$ctx+`6*$SZ`],@X[6]
$LD	[$ctx+`7*$SZ`],@X[7]
add	$A,@X[0],$A
$ST	$A,[$ctx+`0*$SZ`]
add	$B,@X[1],$B
$ST	$B,[$ctx+`1*$SZ`]
add	$C,@X[2],$C
$ST	$C,[$ctx+`2*$SZ`]
add	$D,@X[3],$D
$ST	$D,[$ctx+`3*$SZ`]
add	$E,@X[4],$E
$ST	$E,[$ctx+`4*$SZ`]
add	$F,@X[5],$F
$ST	$F,[$ctx+`5*$SZ`]
add	$G,@X[6],$G
$ST	$G,[$ctx+`6*$SZ`]
add	$H,@X[7],$H
$ST	$H,[$ctx+`7*$SZ`]
___
$code.=<<___ if ($SZ==8);
ld	[$ctx+`0*$SZ+0`],%l0
ld	[$ctx+`0*$SZ+4`],%l1
ld	[$ctx+`1*$SZ+0`],%l2
ld	[$ctx+`1*$SZ+4`],%l3
ld	[$ctx+`2*$SZ+0`],%l4
ld	[$ctx+`2*$SZ+4`],%l5
ld	[$ctx+`3*$SZ+0`],%l6
sllx	%l0,32,$tmp0
ld	[$ctx+`3*$SZ+4`],%l7
sllx	%l2,32,$tmp1
or	%l1,$tmp0,$tmp0
or	%l3,$tmp1,$tmp1
add	$tmp0,$A,$A
add	$tmp1,$B,$B
$ST	$A,[$ctx+`0*$SZ`]
sllx	%l4,32,$tmp2
$ST	$B,[$ctx+`1*$SZ`]
sllx	%l6,32,$T1
or	%l5,$tmp2,$tmp2
or	%l7,$T1,$T1
add	$tmp2,$C,$C
$ST	$C,[$ctx+`2*$SZ`]
add	$T1,$D,$D
$ST	$D,[$ctx+`3*$SZ`]
ld	[$ctx+`4*$SZ+0`],%l0
ld	[$ctx+`4*$SZ+4`],%l1
ld	[$ctx+`5*$SZ+0`],%l2
ld	[$ctx+`5*$SZ+4`],%l3
ld	[$ctx+`6*$SZ+0`],%l4
ld	[$ctx+`6*$SZ+4`],%l5
ld	[$ctx+`7*$SZ+0`],%l6
sllx	%l0,32,$tmp0
ld	[$ctx+`7*$SZ+4`],%l7
sllx	%l2,32,$tmp1
or	%l1,$tmp0,$tmp0
or	%l3,$tmp1,$tmp1
add	$tmp0,$E,$E
add	$tmp1,$F,$F
$ST	$E,[$ctx+`4*$SZ`]
sllx	%l4,32,$tmp2
$ST	$F,[$ctx+`5*$SZ`]
sllx	%l6,32,$T1
or	%l5,$tmp2,$tmp2
or	%l7,$T1,$T1
add	$tmp2,$G,$G
$ST	$G,[$ctx+`6*$SZ`]
add	$T1,$H,$H
$ST	$H,[$ctx+`7*$SZ`]
___
$code.=<<___;
add	$inp,`16*$SZ`,$inp		! advance inp
cmp	$inp,$len
bne	`$bits==64?"%xcc":"%icc"`,.Lloop
sub	$Ktbl,`($rounds-16)*$SZ`,$Ktbl	! rewind Ktbl
ret
restore
.type	sha${label}_block_data_order,
.size	sha${label}_block_data_order,(.-sha${label}_block_data_order)
.asciz	"SHA${label} block transform for SPARCv9, CRYPTOGAMS by <appro\@openssl.org>"
___
$code =~ s/\`([^\`]*)\`/eval $1/gem;
print $code;
close STDOUT;
