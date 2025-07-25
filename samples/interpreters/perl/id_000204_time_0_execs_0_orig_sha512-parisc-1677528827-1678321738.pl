#!/usr/bin/env perl
$flavour = shift;
$output = shift;
open STDOUT,">$output";
if ($flavour =~ /64/) {
$LEVEL		="2.0W";
$SIZE_T		=8;
$FRAME_MARKER	=80;
$SAVED_RP	=16;
$PUSH		="std";
$PUSHMA		="std,ma";
$POP		="ldd";
$POPMB		="ldd,mb";
} else {
$LEVEL		="1.0";
$SIZE_T		=4;
$FRAME_MARKER	=48;
$SAVED_RP	=20;
$PUSH		="stw";
$PUSHMA		="stwm";
$POP		="ldw";
$POPMB		="ldwm";
}
if ($output =~ /512/) {
$func="sha512_block_data_order";
$SZ=8;
@Sigma0=(28,34,39);
@Sigma1=(14,18,41);
@sigma0=(1,  8, 7);
@sigma1=(19,61, 6);
$rounds=80;
$LAST10BITS=0x017;
$LD="ldd";
$LDM="ldd,ma";
$ST="std";
} else {
$func="sha256_block_data_order";
$SZ=4;
@Sigma0=( 2,13,22);
@Sigma1=( 6,11,25);
@sigma0=( 7,18, 3);
@sigma1=(17,19,10);
$rounds=64;
$LAST10BITS=0x0f2;
$LD="ldw";
$LDM="ldwm";
$ST="stw";
}
$FRAME=16*$SIZE_T+$FRAME_MARKER;
$XOFF=16*$SZ+32;
$FRAME+=$XOFF;
$XOFF+=$FRAME_MARKER;
$ctx="%r26";
$inp="%r25";
$num="%r24";
$a0 ="%r26";
$a1 ="%r25";
$t0 ="%r24";
$t1 ="%r29";
$Tbl="%r31";
@V=($A,$B,$C,$D,$E,$F,$G,$H)=("%r17","%r18","%r19","%r20","%r21","%r22","%r23","%r28");
@X=("%r1", "%r2", "%r3", "%r4", "%r5", "%r6", "%r7", "%r8",
"%r9", "%r10","%r11","%r12","%r13","%r14","%r15","%r16",$inp);
sub ROUND_00_15 {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
$code.=<<___;
_ror	$e,$Sigma1[0],$a0
and	$f,$e,$t0
_ror	$e,$Sigma1[1],$a1
addl	$t1,$h,$h
andcm	$g,$e,$t1
xor	$a1,$a0,$a0
_ror	$a1,`$Sigma1[2]-$Sigma1[1]`,$a1
or	$t0,$t1,$t1		; Ch(e,f,g)
addl	@X[$i%16],$h,$h
xor	$a0,$a1,$a1		; Sigma1(e)
addl	$t1,$h,$h
_ror	$a,$Sigma0[0],$a0
addl	$a1,$h,$h
_ror	$a,$Sigma0[1],$a1
and	$a,$b,$t0
and	$a,$c,$t1
xor	$a1,$a0,$a0
_ror	$a1,`$Sigma0[2]-$Sigma0[1]`,$a1
xor	$t1,$t0,$t0
and	$b,$c,$t1
xor	$a0,$a1,$a1		; Sigma0(a)
addl	$h,$d,$d
xor	$t1,$t0,$t0		; Maj(a,b,c)
`"$LDM	$SZ($Tbl),$t1" if ($i<15)`
addl	$a1,$h,$h
addl	$t0,$h,$h
___
}
sub ROUND_16_xx {
my ($i,$a,$b,$c,$d,$e,$f,$g,$h)=@_;
$i-=16;
$code.=<<___;
_ror	@X[($i+1)%16],$sigma0[0],$a0
_ror	@X[($i+1)%16],$sigma0[1],$a1
addl	@X[($i+9)%16],@X[$i],@X[$i]
_ror	@X[($i+14)%16],$sigma1[0],$t0
_ror	@X[($i+14)%16],$sigma1[1],$t1
xor	$a1,$a0,$a0
_shr	@X[($i+1)%16],$sigma0[2],$a1
xor	$t1,$t0,$t0
_shr	@X[($i+14)%16],$sigma1[2],$t1
xor	$a1,$a0,$a0		; sigma0(X[(i+1)&0x0f])
xor	$t1,$t0,$t0		; sigma1(X[(i+14)&0x0f])
$LDM	$SZ($Tbl),$t1
addl	$a0,@X[$i],@X[$i]
addl	$t0,@X[$i],@X[$i]
___
$code.=<<___ if ($i==15);
extru	$t1,31,10,$a1
comiclr,<> $LAST10BITS,$a1,%r0
ldo	1($Tbl),$Tbl		; signal end of $Tbl
___
&ROUND_00_15($i+16,$a,$b,$c,$d,$e,$f,$g,$h);
}
$code=<<___;
.LEVEL	$LEVEL
.SPACE	\$TEXT\$
.SUBSPA	\$CODE\$,QUAD=0,ALIGN=8,ACCESS=0x2C,CODE_ONLY
.ALIGN	64
L\$table
___
$code.=<<___ if ($SZ==8);
.WORD	0x428a2f98,0xd728ae22,0x71374491,0x23ef65cd
.WORD	0xb5c0fbcf,0xec4d3b2f,0xe9b5dba5,0x8189dbbc
.WORD	0x3956c25b,0xf348b538,0x59f111f1,0xb605d019
.WORD	0x923f82a4,0xaf194f9b,0xab1c5ed5,0xda6d8118
.WORD	0xd807aa98,0xa3030242,0x12835b01,0x45706fbe
.WORD	0x243185be,0x4ee4b28c,0x550c7dc3,0xd5ffb4e2
.WORD	0x72be5d74,0xf27b896f,0x80deb1fe,0x3b1696b1
.WORD	0x9bdc06a7,0x25c71235,0xc19bf174,0xcf692694
.WORD	0xe49b69c1,0x9ef14ad2,0xefbe4786,0x384f25e3
.WORD	0x0fc19dc6,0x8b8cd5b5,0x240ca1cc,0x77ac9c65
.WORD	0x2de92c6f,0x592b0275,0x4a7484aa,0x6ea6e483
.WORD	0x5cb0a9dc,0xbd41fbd4,0x76f988da,0x831153b5
.WORD	0x983e5152,0xee66dfab,0xa831c66d,0x2db43210
.WORD	0xb00327c8,0x98fb213f,0xbf597fc7,0xbeef0ee4
.WORD	0xc6e00bf3,0x3da88fc2,0xd5a79147,0x930aa725
.WORD	0x06ca6351,0xe003826f,0x14292967,0x0a0e6e70
.WORD	0x27b70a85,0x46d22ffc,0x2e1b2138,0x5c26c926
.WORD	0x4d2c6dfc,0x5ac42aed,0x53380d13,0x9d95b3df
.WORD	0x650a7354,0x8baf63de,0x766a0abb,0x3c77b2a8
.WORD	0x81c2c92e,0x47edaee6,0x92722c85,0x1482353b
.WORD	0xa2bfe8a1,0x4cf10364,0xa81a664b,0xbc423001
.WORD	0xc24b8b70,0xd0f89791,0xc76c51a3,0x0654be30
.WORD	0xd192e819,0xd6ef5218,0xd6990624,0x5565a910
.WORD	0xf40e3585,0x5771202a,0x106aa070,0x32bbd1b8
.WORD	0x19a4c116,0xb8d2d0c8,0x1e376c08,0x5141ab53
.WORD	0x2748774c,0xdf8eeb99,0x34b0bcb5,0xe19b48a8
.WORD	0x391c0cb3,0xc5c95a63,0x4ed8aa4a,0xe3418acb
.WORD	0x5b9cca4f,0x7763e373,0x682e6ff3,0xd6b2b8a3
.WORD	0x748f82ee,0x5defb2fc,0x78a5636f,0x43172f60
.WORD	0x84c87814,0xa1f0ab72,0x8cc70208,0x1a6439ec
.WORD	0x90befffa,0x23631e28,0xa4506ceb,0xde82bde9
.WORD	0xbef9a3f7,0xb2c67915,0xc67178f2,0xe372532b
.WORD	0xca273ece,0xea26619c,0xd186b8c7,0x21c0c207
.WORD	0xeada7dd6,0xcde0eb1e,0xf57d4f7f,0xee6ed178
.WORD	0x06f067aa,0x72176fba,0x0a637dc5,0xa2c898a6
.WORD	0x113f9804,0xbef90dae,0x1b710b35,0x131c471b
.WORD	0x28db77f5,0x23047d84,0x32caab7b,0x40c72493
.WORD	0x3c9ebe0a,0x15c9bebc,0x431d67c4,0x9c100d4c
.WORD	0x4cc5d4be,0xcb3e42b6,0x597f299c,0xfc657e2a
.WORD	0x5fcb6fab,0x3ad6faec,0x6c44198c,0x4a475817
___
$code.=<<___ if ($SZ==4);
.WORD	0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5
.WORD	0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5
.WORD	0xd807aa98,0x12835b01,0x243185be,0x550c7dc3
.WORD	0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174
.WORD	0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc
.WORD	0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da
.WORD	0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7
.WORD	0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967
.WORD	0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13
.WORD	0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85
.WORD	0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3
.WORD	0xd192e819,0xd6990624,0xf40e3585,0x106aa070
.WORD	0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5
.WORD	0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3
.WORD	0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208
.WORD	0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
___
$code.=<<___;
.EXPORT	$func,ENTRY,ARGW0=GR,ARGW1=GR,ARGW2=GR
.ALIGN	64
$func
.PROC
.CALLINFO	FRAME=`$FRAME-16*$SIZE_T`,NO_CALLS,SAVE_RP,ENTRY_GR=18
.ENTRY
$PUSH	%r2,-$SAVED_RP(%sp)	; standard prologue
$PUSHMA	%r3,$FRAME(%sp)
$PUSH	%r4,`-$FRAME+1*$SIZE_T`(%sp)
$PUSH	%r5,`-$FRAME+2*$SIZE_T`(%sp)
$PUSH	%r6,`-$FRAME+3*$SIZE_T`(%sp)
$PUSH	%r7,`-$FRAME+4*$SIZE_T`(%sp)
$PUSH	%r8,`-$FRAME+5*$SIZE_T`(%sp)
$PUSH	%r9,`-$FRAME+6*$SIZE_T`(%sp)
$PUSH	%r10,`-$FRAME+7*$SIZE_T`(%sp)
$PUSH	%r11,`-$FRAME+8*$SIZE_T`(%sp)
$PUSH	%r12,`-$FRAME+9*$SIZE_T`(%sp)
$PUSH	%r13,`-$FRAME+10*$SIZE_T`(%sp)
$PUSH	%r14,`-$FRAME+11*$SIZE_T`(%sp)
$PUSH	%r15,`-$FRAME+12*$SIZE_T`(%sp)
$PUSH	%r16,`-$FRAME+13*$SIZE_T`(%sp)
$PUSH	%r17,`-$FRAME+14*$SIZE_T`(%sp)
$PUSH	%r18,`-$FRAME+15*$SIZE_T`(%sp)
_shl	$num,`log(16*$SZ)/log(2)`,$num
addl	$inp,$num,$num		; $num to point at the end of $inp
$PUSH	$num,`-$FRAME_MARKER-4*$SIZE_T`(%sp)	; save arguments
$PUSH	$inp,`-$FRAME_MARKER-3*$SIZE_T`(%sp)
$PUSH	$ctx,`-$FRAME_MARKER-2*$SIZE_T`(%sp)
blr	%r0,$Tbl
ldi	3,$t1
L\$pic
andcm	$Tbl,$t1,$Tbl		; wipe privilege level
ldo	L\$table-L\$pic($Tbl),$Tbl
___
$code.=<<___ if ($SZ==8 && $SIZE_T==4);
ldi	31,$t1
mtctl	$t1,%cr11
extrd,u,*= $t1,%sar,1,$t1	; executes on PA-RISC 1.0
b	L\$parisc1
nop
___
$code.=<<___;
$LD	`0*$SZ`($ctx),$A	; load context
$LD	`1*$SZ`($ctx),$B
$LD	`2*$SZ`($ctx),$C
$LD	`3*$SZ`($ctx),$D
$LD	`4*$SZ`($ctx),$E
$LD	`5*$SZ`($ctx),$F
$LD	`6*$SZ`($ctx),$G
$LD	`7*$SZ`($ctx),$H
extru	$inp,31,`log($SZ)/log(2)`,$t0
sh3addl	$t0,%r0,$t0
subi	`8*$SZ`,$t0,$t0
mtctl	$t0,%cr11		; load %sar with align factor
L\$oop
ldi	`$SZ-1`,$t0
$LDM	$SZ($Tbl),$t1
andcm	$inp,$t0,$t0		; align $inp
___
for ($i=0;$i<15;$i++) {
$code.="\t$LD	`$SZ*$i`($t0),@X[$i]\n";		}
$code.=<<___;
cmpb,*=	$inp,$t0,L\$aligned
$LD	`$SZ*15`($t0),@X[15]
$LD	`$SZ*16`($t0),@X[16]
___
for ($i=0;$i<16;$i++) {
$code.="\t_align	@X[$i],@X[$i+1],@X[$i]\n";	}
$code.=<<___;
L\$aligned
nop	; otherwise /usr/ccs/bin/as is confused by below .WORD
___
for($i=0;$i<16;$i++)	{ &ROUND_00_15($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
L\$rounds
nop	; otherwise /usr/ccs/bin/as is confused by below .WORD
___
for(;$i<32;$i++)	{ &ROUND_16_xx($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
bb,>=	$Tbl,31,L\$rounds	; end of $Tbl signalled?
nop
$POP	`-$FRAME_MARKER-2*$SIZE_T`(%sp),$ctx	; restore arguments
$POP	`-$FRAME_MARKER-3*$SIZE_T`(%sp),$inp
$POP	`-$FRAME_MARKER-4*$SIZE_T`(%sp),$num
ldo	`-$rounds*$SZ-1`($Tbl),$Tbl		; rewind $Tbl
$LD	`0*$SZ`($ctx),@X[0]	; load context
$LD	`1*$SZ`($ctx),@X[1]
$LD	`2*$SZ`($ctx),@X[2]
$LD	`3*$SZ`($ctx),@X[3]
$LD	`4*$SZ`($ctx),@X[4]
$LD	`5*$SZ`($ctx),@X[5]
addl	@X[0],$A,$A
$LD	`6*$SZ`($ctx),@X[6]
addl	@X[1],$B,$B
$LD	`7*$SZ`($ctx),@X[7]
ldo	`16*$SZ`($inp),$inp	; advance $inp
$ST	$A,`0*$SZ`($ctx)	; save context
addl	@X[2],$C,$C
$ST	$B,`1*$SZ`($ctx)
addl	@X[3],$D,$D
$ST	$C,`2*$SZ`($ctx)
addl	@X[4],$E,$E
$ST	$D,`3*$SZ`($ctx)
addl	@X[5],$F,$F
$ST	$E,`4*$SZ`($ctx)
addl	@X[6],$G,$G
$ST	$F,`5*$SZ`($ctx)
addl	@X[7],$H,$H
$ST	$G,`6*$SZ`($ctx)
$ST	$H,`7*$SZ`($ctx)
cmpb,*<>,n $inp,$num,L\$oop
$PUSH	$inp,`-$FRAME_MARKER-3*$SIZE_T`(%sp)	; save $inp
___
if ($SZ==8 && $SIZE_T==4)
{{
$code.=<<___;
b	L\$done
nop
.ALIGN	64
L\$parisc1
___
@V=(  $Ahi,  $Alo,  $Bhi,  $Blo,  $Chi,  $Clo,  $Dhi,  $Dlo,
$Ehi,  $Elo,  $Fhi,  $Flo,  $Ghi,  $Glo,  $Hhi,  $Hlo) =
( "%r1", "%r2", "%r3", "%r4", "%r5", "%r6", "%r7", "%r8",
"%r9","%r10","%r11","%r12","%r13","%r14","%r15","%r16");
$a0 ="%r17";
$a1 ="%r18";
$a2 ="%r19";
$a3 ="%r20";
$t0 ="%r21";
$t1 ="%r22";
$t2 ="%r28";
$t3 ="%r29";
$Tbl="%r31";
@X=("%r23","%r24","%r25","%r26");
sub ROUND_00_15_pa1 {
my ($i,$ahi,$alo,$bhi,$blo,$chi,$clo,$dhi,$dlo,
$ehi,$elo,$fhi,$flo,$ghi,$glo,$hhi,$hlo,$flag)=@_;
my ($Xhi,$Xlo,$Xnhi,$Xnlo) = @X;
$code.=<<___ if (!$flag);
ldw	`-$XOFF+8*(($i+1)%16)`(%sp),$Xnhi
ldw	`-$XOFF+8*(($i+1)%16)+4`(%sp),$Xnlo	; load X[i+1]
___
$code.=<<___;
shd	$ehi,$elo,$Sigma1[0],$t0
add	$Xlo,$hlo,$hlo
shd	$elo,$ehi,$Sigma1[0],$t1
addc	$Xhi,$hhi,$hhi		; h += X[i]
shd	$ehi,$elo,$Sigma1[1],$t2
ldwm	8($Tbl),$Xhi
shd	$elo,$ehi,$Sigma1[1],$t3
ldw	-4($Tbl),$Xlo		; load K[i]
xor	$t2,$t0,$t0
xor	$t3,$t1,$t1
and	$flo,$elo,$a0
and	$fhi,$ehi,$a1
shd	$ehi,$elo,$Sigma1[2],$t2
andcm	$glo,$elo,$a2
shd	$elo,$ehi,$Sigma1[2],$t3
andcm	$ghi,$ehi,$a3
xor	$t2,$t0,$t0
xor	$t3,$t1,$t1		; Sigma1(e)
add	$Xlo,$hlo,$hlo
xor	$a2,$a0,$a0
addc	$Xhi,$hhi,$hhi		; h += K[i]
xor	$a3,$a1,$a1		; Ch(e,f,g)
add	$t0,$hlo,$hlo
shd	$ahi,$alo,$Sigma0[0],$t0
addc	$t1,$hhi,$hhi		; h += Sigma1(e)
shd	$alo,$ahi,$Sigma0[0],$t1
add	$a0,$hlo,$hlo
shd	$ahi,$alo,$Sigma0[1],$t2
addc	$a1,$hhi,$hhi		; h += Ch(e,f,g)
shd	$alo,$ahi,$Sigma0[1],$t3
xor	$t2,$t0,$t0
xor	$t3,$t1,$t1
shd	$ahi,$alo,$Sigma0[2],$t2
and	$alo,$blo,$a0
shd	$alo,$ahi,$Sigma0[2],$t3
and	$ahi,$bhi,$a1
xor	$t2,$t0,$t0
xor	$t3,$t1,$t1		; Sigma0(a)
and	$alo,$clo,$a2
and	$ahi,$chi,$a3
xor	$a2,$a0,$a0
add	$hlo,$dlo,$dlo
xor	$a3,$a1,$a1
addc	$hhi,$dhi,$dhi		; d += h
and	$blo,$clo,$a2
add	$t0,$hlo,$hlo
and	$bhi,$chi,$a3
addc	$t1,$hhi,$hhi		; h += Sigma0(a)
xor	$a2,$a0,$a0
add	$a0,$hlo,$hlo
xor	$a3,$a1,$a1		; Maj(a,b,c)
addc	$a1,$hhi,$hhi		; h += Maj(a,b,c)
___
$code.=<<___ if ($i==15 && $flag);
extru	$Xlo,31,10,$Xlo
comiclr,= $LAST10BITS,$Xlo,%r0
b	L\$rounds_pa1
nop
___
push(@X,shift(@X)); push(@X,shift(@X));
}
sub ROUND_16_xx_pa1 {
my ($Xhi,$Xlo,$Xnhi,$Xnlo) = @X;
my ($i)=shift;
$i-=16;
$code.=<<___;
ldw	`-$XOFF+8*(($i+1)%16)`(%sp),$Xnhi
ldw	`-$XOFF+8*(($i+1)%16)+4`(%sp),$Xnlo	; load X[i+1]
ldw	`-$XOFF+8*(($i+9)%16)`(%sp),$a1
ldw	`-$XOFF+8*(($i+9)%16)+4`(%sp),$a0	; load X[i+9]
ldw	`-$XOFF+8*(($i+14)%16)`(%sp),$a3
ldw	`-$XOFF+8*(($i+14)%16)+4`(%sp),$a2	; load X[i+14]
shd	$Xnhi,$Xnlo,$sigma0[0],$t0
shd	$Xnlo,$Xnhi,$sigma0[0],$t1
add	$a0,$Xlo,$Xlo
shd	$Xnhi,$Xnlo,$sigma0[1],$t2
addc	$a1,$Xhi,$Xhi
shd	$Xnlo,$Xnhi,$sigma0[1],$t3
xor	$t2,$t0,$t0
shd	$Xnhi,$Xnlo,$sigma0[2],$t2
xor	$t3,$t1,$t1
extru	$Xnhi,`31-$sigma0[2]`,`32-$sigma0[2]`,$t3
xor	$t2,$t0,$t0
shd	$a3,$a2,$sigma1[0],$a0
xor	$t3,$t1,$t1		; sigma0(X[i+1)&0x0f])
shd	$a2,$a3,$sigma1[0],$a1
add	$t0,$Xlo,$Xlo
shd	$a3,$a2,$sigma1[1],$t2
addc	$t1,$Xhi,$Xhi
shd	$a2,$a3,$sigma1[1],$t3
xor	$t2,$a0,$a0
shd	$a3,$a2,$sigma1[2],$t2
xor	$t3,$a1,$a1
extru	$a3,`31-$sigma1[2]`,`32-$sigma1[2]`,$t3
xor	$t2,$a0,$a0
xor	$t3,$a1,$a1		; sigma0(X[i+14)&0x0f])
add	$a0,$Xlo,$Xlo
addc	$a1,$Xhi,$Xhi
stw	$Xhi,`-$XOFF+8*($i%16)`(%sp)
stw	$Xlo,`-$XOFF+8*($i%16)+4`(%sp)
___
&ROUND_00_15_pa1($i,@_,1);
}
$code.=<<___;
ldw	`0*4`($ctx),$Ahi		; load context
ldw	`1*4`($ctx),$Alo
ldw	`2*4`($ctx),$Bhi
ldw	`3*4`($ctx),$Blo
ldw	`4*4`($ctx),$Chi
ldw	`5*4`($ctx),$Clo
ldw	`6*4`($ctx),$Dhi
ldw	`7*4`($ctx),$Dlo
ldw	`8*4`($ctx),$Ehi
ldw	`9*4`($ctx),$Elo
ldw	`10*4`($ctx),$Fhi
ldw	`11*4`($ctx),$Flo
ldw	`12*4`($ctx),$Ghi
ldw	`13*4`($ctx),$Glo
ldw	`14*4`($ctx),$Hhi
ldw	`15*4`($ctx),$Hlo
extru	$inp,31,2,$t0
sh3addl	$t0,%r0,$t0
subi	32,$t0,$t0
mtctl	$t0,%cr11		; load %sar with align factor
L\$oop_pa1
extru	$inp,31,2,$a3
comib,=	0,$a3,L\$aligned_pa1
sub	$inp,$a3,$inp
ldw	`0*4`($inp),$X[0]
ldw	`1*4`($inp),$X[1]
ldw	`2*4`($inp),$t2
ldw	`3*4`($inp),$t3
ldw	`4*4`($inp),$a0
ldw	`5*4`($inp),$a1
ldw	`6*4`($inp),$a2
ldw	`7*4`($inp),$a3
vshd	$X[0],$X[1],$X[0]
vshd	$X[1],$t2,$X[1]
stw	$X[0],`-$XOFF+0*4`(%sp)
ldw	`8*4`($inp),$t0
vshd	$t2,$t3,$t2
stw	$X[1],`-$XOFF+1*4`(%sp)
ldw	`9*4`($inp),$t1
vshd	$t3,$a0,$t3
___
{
my @t=($t2,$t3,$a0,$a1,$a2,$a3,$t0,$t1);
for ($i=2;$i<=(128/4-8);$i++) {
$code.=<<___;
stw	$t[0],`-$XOFF+$i*4`(%sp)
ldw	`(8+$i)*4`($inp),$t[0]
vshd	$t[1],$t[2],$t[1]
___
push(@t,shift(@t));
}
for (;$i<(128/4-1);$i++) {
$code.=<<___;
stw	$t[0],`-$XOFF+$i*4`(%sp)
vshd	$t[1],$t[2],$t[1]
___
push(@t,shift(@t));
}
$code.=<<___;
b	L\$collected_pa1
stw	$t[0],`-$XOFF+$i*4`(%sp)
___
}
$code.=<<___;
L\$aligned_pa1
ldw	`0*4`($inp),$X[0]
ldw	`1*4`($inp),$X[1]
ldw	`2*4`($inp),$t2
ldw	`3*4`($inp),$t3
ldw	`4*4`($inp),$a0
ldw	`5*4`($inp),$a1
ldw	`6*4`($inp),$a2
ldw	`7*4`($inp),$a3
stw	$X[0],`-$XOFF+0*4`(%sp)
ldw	`8*4`($inp),$t0
stw	$X[1],`-$XOFF+1*4`(%sp)
ldw	`9*4`($inp),$t1
___
{
my @t=($t2,$t3,$a0,$a1,$a2,$a3,$t0,$t1);
for ($i=2;$i<(128/4-8);$i++) {
$code.=<<___;
stw	$t[0],`-$XOFF+$i*4`(%sp)
ldw	`(8+$i)*4`($inp),$t[0]
___
push(@t,shift(@t));
}
for (;$i<128/4;$i++) {
$code.=<<___;
stw	$t[0],`-$XOFF+$i*4`(%sp)
___
push(@t,shift(@t));
}
$code.="L\$collected_pa1\n";
}
for($i=0;$i<16;$i++)	{ &ROUND_00_15_pa1($i,@V); unshift(@V,pop(@V)); unshift(@V,pop(@V)); }
$code.="L\$rounds_pa1\n";
for(;$i<32;$i++)	{ &ROUND_16_xx_pa1($i,@V); unshift(@V,pop(@V)); unshift(@V,pop(@V)); }
$code.=<<___;
$POP	`-$FRAME_MARKER-2*$SIZE_T`(%sp),$ctx	; restore arguments
$POP	`-$FRAME_MARKER-3*$SIZE_T`(%sp),$inp
$POP	`-$FRAME_MARKER-4*$SIZE_T`(%sp),$num
ldo	`-$rounds*$SZ`($Tbl),$Tbl		; rewind $Tbl
ldw	`0*4`($ctx),$t1		; update context
ldw	`1*4`($ctx),$t0
ldw	`2*4`($ctx),$t3
ldw	`3*4`($ctx),$t2
ldw	`4*4`($ctx),$a1
ldw	`5*4`($ctx),$a0
ldw	`6*4`($ctx),$a3
add	$t0,$Alo,$Alo
ldw	`7*4`($ctx),$a2
addc	$t1,$Ahi,$Ahi
ldw	`8*4`($ctx),$t1
add	$t2,$Blo,$Blo
ldw	`9*4`($ctx),$t0
addc	$t3,$Bhi,$Bhi
ldw	`10*4`($ctx),$t3
add	$a0,$Clo,$Clo
ldw	`11*4`($ctx),$t2
addc	$a1,$Chi,$Chi
ldw	`12*4`($ctx),$a1
add	$a2,$Dlo,$Dlo
ldw	`13*4`($ctx),$a0
addc	$a3,$Dhi,$Dhi
ldw	`14*4`($ctx),$a3
add	$t0,$Elo,$Elo
ldw	`15*4`($ctx),$a2
addc	$t1,$Ehi,$Ehi
stw	$Ahi,`0*4`($ctx)
add	$t2,$Flo,$Flo
stw	$Alo,`1*4`($ctx)
addc	$t3,$Fhi,$Fhi
stw	$Bhi,`2*4`($ctx)
add	$a0,$Glo,$Glo
stw	$Blo,`3*4`($ctx)
addc	$a1,$Ghi,$Ghi
stw	$Chi,`4*4`($ctx)
add	$a2,$Hlo,$Hlo
stw	$Clo,`5*4`($ctx)
addc	$a3,$Hhi,$Hhi
stw	$Dhi,`6*4`($ctx)
ldo	`16*$SZ`($inp),$inp	; advance $inp
stw	$Dlo,`7*4`($ctx)
stw	$Ehi,`8*4`($ctx)
stw	$Elo,`9*4`($ctx)
stw	$Fhi,`10*4`($ctx)
stw	$Flo,`11*4`($ctx)
stw	$Ghi,`12*4`($ctx)
stw	$Glo,`13*4`($ctx)
stw	$Hhi,`14*4`($ctx)
comb,=	$inp,$num,L\$done
stw	$Hlo,`15*4`($ctx)
b	L\$oop_pa1
$PUSH	$inp,`-$FRAME_MARKER-3*$SIZE_T`(%sp)	; save $inp
L\$done
___
}}
$code.=<<___;
$POP	`-$FRAME-$SAVED_RP`(%sp),%r2		; standard epilogue
$POP	`-$FRAME+1*$SIZE_T`(%sp),%r4
$POP	`-$FRAME+2*$SIZE_T`(%sp),%r5
$POP	`-$FRAME+3*$SIZE_T`(%sp),%r6
$POP	`-$FRAME+4*$SIZE_T`(%sp),%r7
$POP	`-$FRAME+5*$SIZE_T`(%sp),%r8
$POP	`-$FRAME+6*$SIZE_T`(%sp),%r9
$POP	`-$FRAME+7*$SIZE_T`(%sp),%r10
$POP	`-$FRAME+8*$SIZE_T`(%sp),%r11
$POP	`-$FRAME+9*$SIZE_T`(%sp),%r12
$POP	`-$FRAME+10*$SIZE_T`(%sp),%r13
$POP	`-$FRAME+11*$SIZE_T`(%sp),%r14
$POP	`-$FRAME+12*$SIZE_T`(%sp),%r15
$POP	`-$FRAME+13*$SIZE_T`(%sp),%r16
$POP	`-$FRAME+14*$SIZE_T`(%sp),%r17
$POP	`-$FRAME+15*$SIZE_T`(%sp),%r18
bv	(%r2)
.EXIT
$POPMB	-$FRAME(%sp),%r3
.PROCEND
.STRINGZ "SHA`64*$SZ` block transform for PA-RISC, CRYPTOGAMS by <appro\@openssl.org>"
___
my $ldd = sub {
my ($mod,$args) = @_;
my $orig = "ldd$mod\t$args";
if ($args =~ /(\-?[0-9]+)\(%r([0-9]+)\),%r([0-9]+)/)
{	my $opcode=(0x14<<26)|($2<<21)|($3<<16)|(($1&0x1FF8)<<1)|(($1>>13)&1);
$opcode|=(1<<3) if ($mod =~ /^,m/);
$opcode|=(1<<2) if ($mod =~ /^,mb/);
sprintf "\t.WORD\t0x%08x\t; %s",$opcode,$orig;
}
else { "\t".$orig; }
};
my $std = sub {
my ($mod,$args) = @_;
my $orig = "std$mod\t$args";
if ($args =~ /%r([0-9]+),(\-?[0-9]+)\(%r([0-9]+)\)/)
{	my $opcode=(0x1c<<26)|($3<<21)|($1<<16)|(($2&0x1FF8)<<1)|(($2>>13)&1);
sprintf "\t.WORD\t0x%08x\t; %s",$opcode,$orig;
}
else { "\t".$orig; }
};
my $extrd = sub {
my ($mod,$args) = @_;
my $orig = "extrd$mod\t$args";
if ($args =~ /%r([0-9]+),([0-9]+),([0-9]+),%r([0-9]+)/)
{	my $opcode=(0x36<<26)|($1<<21)|($4<<16);
my $len=32-$3;
$opcode |= (($2&0x20)<<6)|(($2&0x1f)<<5);
$opcode |= (($len&0x20)<<7)|($len&0x1f);
sprintf "\t.WORD\t0x%08x\t; %s",$opcode,$orig;
}
elsif ($args =~ /%r([0-9]+),%sar,([0-9]+),%r([0-9]+)/)
{	my $opcode=(0x34<<26)|($1<<21)|($3<<16)|(2<<11)|(1<<9);
my $len=32-$2;
$opcode |= (($len&0x20)<<3)|($len&0x1f);
$opcode |= (1<<13) if ($mod =~ /,\**=/);
sprintf "\t.WORD\t0x%08x\t; %s",$opcode,$orig;
}
else { "\t".$orig; }
};
my $shrpd = sub {
my ($mod,$args) = @_;
my $orig = "shrpd$mod\t$args";
if ($args =~ /%r([0-9]+),%r([0-9]+),([0-9]+),%r([0-9]+)/)
{	my $opcode=(0x34<<26)|($2<<21)|($1<<16)|(1<<10)|$4;
my $cpos=63-$3;
$opcode |= (($cpos&0x20)<<6)|(($cpos&0x1f)<<5);
sprintf "\t.WORD\t0x%08x\t; %s",$opcode,$orig;
}
elsif ($args =~ /%r([0-9]+),%r([0-9]+),%sar,%r([0-9]+)/)
{	sprintf "\t.WORD\t0x%08x\t; %s",
(0x34<<26)|($2<<21)|($1<<16)|(1<<9)|$3,$orig;
}
else { "\t".$orig; }
};
sub assemble {
my ($mnemonic,$mod,$args)=@_;
my $opcode = eval("\$$mnemonic");
ref($opcode) eq 'CODE' ? &$opcode($mod,$args) : "\t$mnemonic$mod\t$args";
}
foreach (split("\n",$code)) {
s/\`([^\`]*)\`/eval $1/ge;
s/shd\s+(%r[0-9]+),(%r[0-9]+),([0-9]+)/
$3>31 ? sprintf("shd\t%$2,%$1,%d",$3-32)
:       sprintf("shd\t%$1,%$2,%d",$3)/e			or
s/_ror(\s+)(%r[0-9]+),/
($SZ==4 ? "shd" : "shrpd")."$1$2,$2,"/e			or
s/_shr(\s+%r[0-9]+),([0-9]+),/
$SZ==4 ? sprintf("extru%s,%d,%d,",$1,31-$2,32-$2)
:        sprintf("extrd,u%s,%d,%d,",$1,63-$2,64-$2)/e	or
s/_align(\s+%r[0-9]+,%r[0-9]+),/
($SZ==4 ? "vshd$1," : "shrpd$1,%sar,")/e		or
s/_shl(\s+%r[0-9]+),([0-9]+),/
$SIZE_T==4 ? sprintf("zdep%s,%d,%d,",$1,31-$2,32-$2)
:            sprintf("depd,z%s,%d,%d,",$1,63-$2,64-$2)/e;
s/^\s+([a-z]+)([\S]*)\s+([\S]*)/&assemble($1,$2,$3)/e if ($SIZE_T==4);
s/cmpb,\*/comb,/ if ($SIZE_T==4);
print $_,"\n";
}
close STDOUT;
