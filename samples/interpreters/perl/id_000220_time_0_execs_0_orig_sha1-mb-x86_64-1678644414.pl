#!/usr/bin/env perl
$flavour = shift;
$output  = shift;
if ($flavour =~ /\./) { $output = $flavour; undef $flavour; }
$win64=0; $win64=1 if ($flavour =~ /[nm]asm|mingw64/ || $output =~ /\.asm$/);
$0 =~ m/(.*[\/\\])[^\/\\]+$/; $dir=$1;
( $xlate="${dir}x86_64-xlate.pl" and -f $xlate ) or
( $xlate="${dir}../../perlasm/x86_64-xlate.pl" and -f $xlate) or
die "can't locate x86_64-xlate.pl";
$avx=0;
if (`$ENV{CC} -Wa,-v -c -o /dev/null -x assembler /dev/null 2>&1`
=~ /GNU assembler version ([2-9]\.[0-9]+)/) {
$avx = ($1>=2.19) + ($1>=2.22);
}
if (!$avx && $win64 && ($flavour =~ /nasm/ || $ENV{ASM} =~ /nasm/) &&
`nasm -v 2>&1` =~ /NASM version ([2-9]\.[0-9]+)/) {
$avx = ($1>=2.09) + ($1>=2.10);
}
if (!$avx && $win64 && ($flavour =~ /masm/ || $ENV{ASM} =~ /ml64/) &&
`ml64 2>&1` =~ /Version ([0-9]+)\./) {
$avx = ($1>=10) + ($1>=11);
}
if (!$avx && `$ENV{CC} -v 2>&1` =~ /((?:^clang|LLVM) version|.*based on LLVM) ([3-9]\.[0-9]+)/) {
$avx = ($2>=3.0) + ($2>3.0);
}
open OUT,"| \"$^X\" $xlate $flavour $output";
*STDOUT=*OUT;
$ctx="%rdi";
$inp="%rsi";
$num="%edx";
@ptr=map("%r$_",(8..11));
$Tbl="%rbp";
@V=($A,$B,$C,$D,$E)=map("%xmm$_",(0..4));
($t0,$t1,$t2,$t3,$tx)=map("%xmm$_",(5..9));
@Xi=map("%xmm$_",(10..14));
$K="%xmm15";
if (1) {
@Xi=map("%xmm$_",(0..4));
($tx,$t0,$t1,$t2,$t3)=map("%xmm$_",(5..9));
@V=($A,$B,$C,$D,$E)=map("%xmm$_",(10..14));
}
$REG_SZ=16;
sub Xi_off {
my $off = shift;
$off %= 16; $off *= $REG_SZ;
$off<256 ? "$off-128(%rax)" : "$off-256-128(%rbx)";
}
sub BODY_00_19 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
my $k=$i+2;
$code.=<<___ if ($i==0);
movd		(@ptr[0]),@Xi[0]
lea		`16*4`(@ptr[0]),@ptr[0]
movd		(@ptr[1]),@Xi[2]
lea		`16*4`(@ptr[1]),@ptr[1]
movd		(@ptr[2]),@Xi[3]
lea		`16*4`(@ptr[2]),@ptr[2]
movd		(@ptr[3]),@Xi[4]
lea		`16*4`(@ptr[3]),@ptr[3]
punpckldq	@Xi[3],@Xi[0]
movd		`4*$j-16*4`(@ptr[0]),@Xi[1]
punpckldq	@Xi[4],@Xi[2]
movd		`4*$j-16*4`(@ptr[1]),$t3
punpckldq	@Xi[2],@Xi[0]
movd		`4*$j-16*4`(@ptr[2]),$t2
pshufb		$tx,@Xi[0]
___
$code.=<<___ if ($i<14);
movd		`4*$j-16*4`(@ptr[3]),$t1
punpckldq	$t2,@Xi[1]
movdqa	$a,$t2
paddd	$K,$e
punpckldq	$t1,$t3
movdqa	$b,$t1
movdqa	$b,$t0
pslld	\$5,$t2
pandn	$d,$t1
pand	$c,$t0
punpckldq	$t3,@Xi[1]
movdqa	$a,$t3
movdqa	@Xi[0],`&Xi_off($i)`
paddd	@Xi[0],$e
movd		`4*$k-16*4`(@ptr[0]),@Xi[2]
psrld	\$27,$t3
pxor	$t1,$t0
movdqa	$b,$t1
por	$t3,$t2
movd		`4*$k-16*4`(@ptr[1]),$t3
pslld	\$30,$t1
paddd	$t0,$e
psrld	\$2,$b
paddd	$t2,$e
pshufb	$tx,@Xi[1]
movd		`4*$k-16*4`(@ptr[2]),$t2
por	$t1,$b
___
$code.=<<___ if ($i==14);
movd		`4*$j-16*4`(@ptr[3]),$t1
punpckldq	$t2,@Xi[1]
movdqa	$a,$t2
paddd	$K,$e
punpckldq	$t1,$t3
movdqa	$b,$t1
movdqa	$b,$t0
pslld	\$5,$t2
prefetcht0	63(@ptr[0])
pandn	$d,$t1
pand	$c,$t0
punpckldq	$t3,@Xi[1]
movdqa	$a,$t3
movdqa	@Xi[0],`&Xi_off($i)`
paddd	@Xi[0],$e
psrld	\$27,$t3
pxor	$t1,$t0
movdqa	$b,$t1
prefetcht0	63(@ptr[1])
por	$t3,$t2
pslld	\$30,$t1
paddd	$t0,$e
prefetcht0	63(@ptr[2])
psrld	\$2,$b
paddd	$t2,$e
pshufb	$tx,@Xi[1]
prefetcht0	63(@ptr[3])
por	$t1,$b
___
$code.=<<___ if ($i>=13 && $i<15);
movdqa	`&Xi_off($j+2)`,@Xi[3]
___
$code.=<<___ if ($i>=15);
pxor	@Xi[-2],@Xi[1]
movdqa	`&Xi_off($j+2)`,@Xi[3]
movdqa	$a,$t2
pxor	`&Xi_off($j+8)`,@Xi[1]
paddd	$K,$e
movdqa	$b,$t1
pslld	\$5,$t2
pxor	@Xi[3],@Xi[1]
movdqa	$b,$t0
pandn	$d,$t1
movdqa	@Xi[1],$tx
pand	$c,$t0
movdqa	$a,$t3
psrld	\$31,$tx
paddd	@Xi[1],@Xi[1]
movdqa	@Xi[0],`&Xi_off($i)`
paddd	@Xi[0],$e
psrld	\$27,$t3
pxor	$t1,$t0
movdqa	$b,$t1
por	$t3,$t2
pslld	\$30,$t1
paddd	$t0,$e
psrld	\$2,$b
paddd	$t2,$e
por	$tx,@Xi[1]
por	$t1,$b
___
push(@Xi,shift(@Xi));
}
sub BODY_20_39 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
$code.=<<___ if ($i<79);
pxor	@Xi[-2],@Xi[1]
movdqa	`&Xi_off($j+2)`,@Xi[3]
movdqa	$a,$t2
movdqa	$d,$t0
pxor	`&Xi_off($j+8)`,@Xi[1]
paddd	$K,$e
pslld	\$5,$t2
pxor	$b,$t0
movdqa	$a,$t3
___
$code.=<<___ if ($i<72);
movdqa	@Xi[0],`&Xi_off($i)`
___
$code.=<<___ if ($i<79);
paddd	@Xi[0],$e
pxor	@Xi[3],@Xi[1]
psrld	\$27,$t3
pxor	$c,$t0
movdqa	$b,$t1
pslld	\$30,$t1
movdqa	@Xi[1],$tx
por	$t3,$t2
psrld	\$31,$tx
paddd	$t0,$e
paddd	@Xi[1],@Xi[1]
psrld	\$2,$b
paddd	$t2,$e
por	$tx,@Xi[1]
por	$t1,$b
___
$code.=<<___ if ($i==79);
movdqa	$a,$t2
paddd	$K,$e
movdqa	$d,$t0
pslld	\$5,$t2
pxor	$b,$t0
movdqa	$a,$t3
paddd	@Xi[0],$e
psrld	\$27,$t3
movdqa	$b,$t1
pxor	$c,$t0
pslld	\$30,$t1
por	$t3,$t2
paddd	$t0,$e
psrld	\$2,$b
paddd	$t2,$e
por	$t1,$b
___
push(@Xi,shift(@Xi));
}
sub BODY_40_59 {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
$code.=<<___;
pxor	@Xi[-2],@Xi[1]
movdqa	`&Xi_off($j+2)`,@Xi[3]
movdqa	$a,$t2
movdqa	$d,$t1
pxor	`&Xi_off($j+8)`,@Xi[1]
pxor	@Xi[3],@Xi[1]
paddd	$K,$e
pslld	\$5,$t2
movdqa	$a,$t3
pand	$c,$t1
movdqa	$d,$t0
movdqa	@Xi[1],$tx
psrld	\$27,$t3
paddd	$t1,$e
pxor	$c,$t0
movdqa	@Xi[0],`&Xi_off($i)`
paddd	@Xi[0],$e
por	$t3,$t2
psrld	\$31,$tx
pand	$b,$t0
movdqa	$b,$t1
pslld	\$30,$t1
paddd	@Xi[1],@Xi[1]
paddd	$t0,$e
psrld	\$2,$b
paddd	$t2,$e
por	$tx,@Xi[1]
por	$t1,$b
___
push(@Xi,shift(@Xi));
}
$code.=<<___;
.text
.extern	OPENSSL_ia32cap_P
.globl	sha1_multi_block
.type	sha1_multi_block,\@function,3
.align	32
sha1_multi_block:
mov	OPENSSL_ia32cap_P+4(%rip),%rcx
bt	\$61,%rcx
jc	_shaext_shortcut
___
$code.=<<___ if ($avx);
test	\$`1<<28`,%ecx
jnz	_avx_shortcut
___
$code.=<<___;
mov	%rsp,%rax
push	%rbx
push	%rbp
___
$code.=<<___ if ($win64);
lea	-0xa8(%rsp),%rsp
movaps	%xmm6,(%rsp)
movaps	%xmm7,0x10(%rsp)
movaps	%xmm8,0x20(%rsp)
movaps	%xmm9,0x30(%rsp)
movaps	%xmm10,-0x78(%rax)
movaps	%xmm11,-0x68(%rax)
movaps	%xmm12,-0x58(%rax)
movaps	%xmm13,-0x48(%rax)
movaps	%xmm14,-0x38(%rax)
movaps	%xmm15,-0x28(%rax)
___
$code.=<<___;
sub	\$`$REG_SZ*18`,%rsp
and	\$-256,%rsp
mov	%rax,`$REG_SZ*17`(%rsp)
.Lbody:
lea	K_XX_XX(%rip),$Tbl
lea	`$REG_SZ*16`(%rsp),%rbx
.Loop_grande:
mov	$num,`$REG_SZ*17+8`(%rsp)
xor	$num,$num
___
for($i=0;$i<4;$i++) {
$code.=<<___;
mov	`16*$i+0`($inp),@ptr[$i]
mov	`16*$i+8`($inp),%ecx
cmp	$num,%ecx
cmovg	%ecx,$num
test	%ecx,%ecx
mov	%ecx,`4*$i`(%rbx)
cmovle	$Tbl,@ptr[$i]
___
}
$code.=<<___;
test	$num,$num
jz	.Ldone
movdqu	0x00($ctx),$A
lea	128(%rsp),%rax
movdqu	0x20($ctx),$B
movdqu	0x40($ctx),$C
movdqu	0x60($ctx),$D
movdqu	0x80($ctx),$E
movdqa	0x60($Tbl),$tx
movdqa	-0x20($Tbl),$K
jmp	.Loop
.align	32
.Loop:
___
for($i=0;$i<20;$i++)	{ &BODY_00_19($i,@V); unshift(@V,pop(@V)); }
$code.="	movdqa	0x00($Tbl),$K\n";
for(;$i<40;$i++)	{ &BODY_20_39($i,@V); unshift(@V,pop(@V)); }
$code.="	movdqa	0x20($Tbl),$K\n";
for(;$i<60;$i++)	{ &BODY_40_59($i,@V); unshift(@V,pop(@V)); }
$code.="	movdqa	0x40($Tbl),$K\n";
for(;$i<80;$i++)	{ &BODY_20_39($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
movdqa	(%rbx),@Xi[0]
mov	\$1,%ecx
cmp	4*0(%rbx),%ecx
pxor	$t2,$t2
cmovge	$Tbl,@ptr[0]
cmp	4*1(%rbx),%ecx
movdqa	@Xi[0],@Xi[1]
cmovge	$Tbl,@ptr[1]
cmp	4*2(%rbx),%ecx
pcmpgtd	$t2,@Xi[1]
cmovge	$Tbl,@ptr[2]
cmp	4*3(%rbx),%ecx
paddd	@Xi[1],@Xi[0]
cmovge	$Tbl,@ptr[3]
movdqu	0x00($ctx),$t0
pand	@Xi[1],$A
movdqu	0x20($ctx),$t1
pand	@Xi[1],$B
paddd	$t0,$A
movdqu	0x40($ctx),$t2
pand	@Xi[1],$C
paddd	$t1,$B
movdqu	0x60($ctx),$t3
pand	@Xi[1],$D
paddd	$t2,$C
movdqu	0x80($ctx),$tx
pand	@Xi[1],$E
movdqu	$A,0x00($ctx)
paddd	$t3,$D
movdqu	$B,0x20($ctx)
paddd	$tx,$E
movdqu	$C,0x40($ctx)
movdqu	$D,0x60($ctx)
movdqu	$E,0x80($ctx)
movdqa	@Xi[0],(%rbx)
movdqa	0x60($Tbl),$tx
movdqa	-0x20($Tbl),$K
dec	$num
jnz	.Loop
mov	`$REG_SZ*17+8`(%rsp),$num
lea	$REG_SZ($ctx),$ctx
lea	`16*$REG_SZ/4`($inp),$inp
dec	$num
jnz	.Loop_grande
.Ldone:
mov	`$REG_SZ*17`(%rsp),%rax
___
$code.=<<___ if ($win64);
movaps	-0xb8(%rax),%xmm6
movaps	-0xa8(%rax),%xmm7
movaps	-0x98(%rax),%xmm8
movaps	-0x88(%rax),%xmm9
movaps	-0x78(%rax),%xmm10
movaps	-0x68(%rax),%xmm11
movaps	-0x58(%rax),%xmm12
movaps	-0x48(%rax),%xmm13
movaps	-0x38(%rax),%xmm14
movaps	-0x28(%rax),%xmm15
___
$code.=<<___;
mov	-16(%rax),%rbp
mov	-8(%rax),%rbx
lea	(%rax),%rsp
.Lepilogue:
ret
.size	sha1_multi_block,.-sha1_multi_block
___
{{{
my ($ABCD0,$E0,$E0_,$BSWAP,$ABCD1,$E1,$E1_)=map("%xmm$_",(0..3,8..10));
my @MSG0=map("%xmm$_",(4..7));
my @MSG1=map("%xmm$_",(11..14));
$code.=<<___;
.type	sha1_multi_block_shaext,\@function,3
.align	32
sha1_multi_block_shaext:
_shaext_shortcut:
mov	%rsp,%rax
push	%rbx
push	%rbp
___
$code.=<<___ if ($win64);
lea	-0xa8(%rsp),%rsp
movaps	%xmm6,(%rsp)
movaps	%xmm7,0x10(%rsp)
movaps	%xmm8,0x20(%rsp)
movaps	%xmm9,0x30(%rsp)
movaps	%xmm10,-0x78(%rax)
movaps	%xmm11,-0x68(%rax)
movaps	%xmm12,-0x58(%rax)
movaps	%xmm13,-0x48(%rax)
movaps	%xmm14,-0x38(%rax)
movaps	%xmm15,-0x28(%rax)
___
$code.=<<___;
sub	\$`$REG_SZ*18`,%rsp
shl	\$1,$num
and	\$-256,%rsp
lea	0x40($ctx),$ctx
mov	%rax,`$REG_SZ*17`(%rsp)
.Lbody_shaext:
lea	`$REG_SZ*16`(%rsp),%rbx
movdqa	K_XX_XX+0x80(%rip),$BSWAP
.Loop_grande_shaext:
mov	$num,`$REG_SZ*17+8`(%rsp)
xor	$num,$num
___
for($i=0;$i<2;$i++) {
$code.=<<___;
mov	`16*$i+0`($inp),@ptr[$i]
mov	`16*$i+8`($inp),%ecx
cmp	$num,%ecx
cmovg	%ecx,$num
test	%ecx,%ecx
mov	%ecx,`4*$i`(%rbx)
cmovle	%rsp,@ptr[$i]
___
}
$code.=<<___;
test	$num,$num
jz	.Ldone_shaext
movq		0x00-0x40($ctx),$ABCD0
movq		0x20-0x40($ctx),@MSG0[0]
movq		0x40-0x40($ctx),@MSG0[1]
movq		0x60-0x40($ctx),@MSG0[2]
movq		0x80-0x40($ctx),@MSG0[3]
punpckldq	@MSG0[0],$ABCD0
punpckldq	@MSG0[2],@MSG0[1]
movdqa		$ABCD0,$ABCD1
punpcklqdq	@MSG0[1],$ABCD0
punpckhqdq	@MSG0[1],$ABCD1
pshufd		\$0b00111111,@MSG0[3],$E0
pshufd		\$0b01111111,@MSG0[3],$E1
pshufd		\$0b00011011,$ABCD0,$ABCD0
pshufd		\$0b00011011,$ABCD1,$ABCD1
jmp		.Loop_shaext
.align	32
.Loop_shaext:
movdqu		0x00(@ptr[0]),@MSG0[0]
movdqu		0x00(@ptr[1]),@MSG1[0]
movdqu		0x10(@ptr[0]),@MSG0[1]
movdqu		0x10(@ptr[1]),@MSG1[1]
movdqu		0x20(@ptr[0]),@MSG0[2]
pshufb		$BSWAP,@MSG0[0]
movdqu		0x20(@ptr[1]),@MSG1[2]
pshufb		$BSWAP,@MSG1[0]
movdqu		0x30(@ptr[0]),@MSG0[3]
lea		0x40(@ptr[0]),@ptr[0]
pshufb		$BSWAP,@MSG0[1]
movdqu		0x30(@ptr[1]),@MSG1[3]
lea		0x40(@ptr[1]),@ptr[1]
pshufb		$BSWAP,@MSG1[1]
movdqa		$E0,0x50(%rsp)
paddd		@MSG0[0],$E0
movdqa		$E1,0x70(%rsp)
paddd		@MSG1[0],$E1
movdqa		$ABCD0,0x40(%rsp)
movdqa		$ABCD0,$E0_
movdqa		$ABCD1,0x60(%rsp)
movdqa		$ABCD1,$E1_
sha1rnds4	\$0,$E0,$ABCD0
sha1nexte	@MSG0[1],$E0_
sha1rnds4	\$0,$E1,$ABCD1
sha1nexte	@MSG1[1],$E1_
pshufb		$BSWAP,@MSG0[2]
prefetcht0	127(@ptr[0])
sha1msg1	@MSG0[1],@MSG0[0]
pshufb		$BSWAP,@MSG1[2]
prefetcht0	127(@ptr[1])
sha1msg1	@MSG1[1],@MSG1[0]
pshufb		$BSWAP,@MSG0[3]
movdqa		$ABCD0,$E0
pshufb		$BSWAP,@MSG1[3]
movdqa		$ABCD1,$E1
sha1rnds4	\$0,$E0_,$ABCD0
sha1nexte	@MSG0[2],$E0
sha1rnds4	\$0,$E1_,$ABCD1
sha1nexte	@MSG1[2],$E1
pxor		@MSG0[2],@MSG0[0]
sha1msg1	@MSG0[2],@MSG0[1]
pxor		@MSG1[2],@MSG1[0]
sha1msg1	@MSG1[2],@MSG1[1]
___
for($i=2;$i<20-4;$i++) {
$code.=<<___;
movdqa		$ABCD0,$E0_
movdqa		$ABCD1,$E1_
sha1rnds4	\$`int($i/5)`,$E0,$ABCD0
sha1nexte	@MSG0[3],$E0_
sha1rnds4	\$`int($i/5)`,$E1,$ABCD1
sha1nexte	@MSG1[3],$E1_
sha1msg2	@MSG0[3],@MSG0[0]
sha1msg2	@MSG1[3],@MSG1[0]
pxor		@MSG0[3],@MSG0[1]
sha1msg1	@MSG0[3],@MSG0[2]
pxor		@MSG1[3],@MSG1[1]
sha1msg1	@MSG1[3],@MSG1[2]
___
($E0,$E0_)=($E0_,$E0);		($E1,$E1_)=($E1_,$E1);
push(@MSG0,shift(@MSG0));	push(@MSG1,shift(@MSG1));
}
$code.=<<___;
movdqa		$ABCD0,$E0_
movdqa		$ABCD1,$E1_
sha1rnds4	\$3,$E0,$ABCD0
sha1nexte	@MSG0[3],$E0_
sha1rnds4	\$3,$E1,$ABCD1
sha1nexte	@MSG1[3],$E1_
sha1msg2	@MSG0[3],@MSG0[0]
sha1msg2	@MSG1[3],@MSG1[0]
pxor		@MSG0[3],@MSG0[1]
pxor		@MSG1[3],@MSG1[1]
mov		\$1,%ecx
pxor		@MSG0[2],@MSG0[2]
cmp		4*0(%rbx),%ecx
cmovge		%rsp,@ptr[0]
movdqa		$ABCD0,$E0
movdqa		$ABCD1,$E1
sha1rnds4	\$3,$E0_,$ABCD0
sha1nexte	@MSG0[0],$E0
sha1rnds4	\$3,$E1_,$ABCD1
sha1nexte	@MSG1[0],$E1
sha1msg2	@MSG0[0],@MSG0[1]
sha1msg2	@MSG1[0],@MSG1[1]
cmp		4*1(%rbx),%ecx
cmovge		%rsp,@ptr[1]
movq		(%rbx),@MSG0[0]
movdqa		$ABCD0,$E0_
movdqa		$ABCD1,$E1_
sha1rnds4	\$3,$E0,$ABCD0
sha1nexte	@MSG0[1],$E0_
sha1rnds4	\$3,$E1,$ABCD1
sha1nexte	@MSG1[1],$E1_
pshufd		\$0x00,@MSG0[0],@MSG1[2]
pshufd		\$0x55,@MSG0[0],@MSG1[3]
movdqa		@MSG0[0],@MSG0[1]
pcmpgtd		@MSG0[2],@MSG1[2]
pcmpgtd		@MSG0[2],@MSG1[3]
movdqa		$ABCD0,$E0
movdqa		$ABCD1,$E1
sha1rnds4	\$3,$E0_,$ABCD0
sha1nexte	$MSG0[2],$E0
sha1rnds4	\$3,$E1_,$ABCD1
sha1nexte	$MSG0[2],$E1
pcmpgtd		@MSG0[2],@MSG0[1]
pand		@MSG1[2],$ABCD0
pand		@MSG1[2],$E0
pand		@MSG1[3],$ABCD1
pand		@MSG1[3],$E1
paddd		@MSG0[1],@MSG0[0]
paddd		0x40(%rsp),$ABCD0
paddd		0x50(%rsp),$E0
paddd		0x60(%rsp),$ABCD1
paddd		0x70(%rsp),$E1
movq		@MSG0[0],(%rbx)
dec		$num
jnz		.Loop_shaext
mov		`$REG_SZ*17+8`(%rsp),$num
pshufd		\$0b00011011,$ABCD0,$ABCD0
pshufd		\$0b00011011,$ABCD1,$ABCD1
movdqa		$ABCD0,@MSG0[0]
punpckldq	$ABCD1,$ABCD0
punpckhdq	$ABCD1,@MSG0[0]
punpckhdq	$E1,$E0
movq		$ABCD0,0x00-0x40($ctx)
psrldq		\$8,$ABCD0
movq		@MSG0[0],0x40-0x40($ctx)
psrldq		\$8,@MSG0[0]
movq		$ABCD0,0x20-0x40($ctx)
psrldq		\$8,$E0
movq		@MSG0[0],0x60-0x40($ctx)
movq		$E0,0x80-0x40($ctx)
lea	`$REG_SZ/2`($ctx),$ctx
lea	`16*2`($inp),$inp
dec	$num
jnz	.Loop_grande_shaext
.Ldone_shaext:
___
$code.=<<___ if ($win64);
movaps	-0xb8(%rax),%xmm6
movaps	-0xa8(%rax),%xmm7
movaps	-0x98(%rax),%xmm8
movaps	-0x88(%rax),%xmm9
movaps	-0x78(%rax),%xmm10
movaps	-0x68(%rax),%xmm11
movaps	-0x58(%rax),%xmm12
movaps	-0x48(%rax),%xmm13
movaps	-0x38(%rax),%xmm14
movaps	-0x28(%rax),%xmm15
___
$code.=<<___;
mov	-16(%rax),%rbp
mov	-8(%rax),%rbx
lea	(%rax),%rsp
.Lepilogue_shaext:
ret
.size	sha1_multi_block_shaext,.-sha1_multi_block_shaext
___
}}}
if ($avx) {{{
sub BODY_00_19_avx {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
my $k=$i+2;
my $vpack = $REG_SZ==16 ? "vpunpckldq" : "vinserti128";
my $ptr_n = $REG_SZ==16 ? @ptr[1] : @ptr[4];
$code.=<<___ if ($i==0 && $REG_SZ==16);
vmovd		(@ptr[0]),@Xi[0]
lea		`16*4`(@ptr[0]),@ptr[0]
vmovd		(@ptr[1]),@Xi[2]
lea		`16*4`(@ptr[1]),@ptr[1]
vpinsrd		\$1,(@ptr[2]),@Xi[0],@Xi[0]
lea		`16*4`(@ptr[2]),@ptr[2]
vpinsrd		\$1,(@ptr[3]),@Xi[2],@Xi[2]
lea		`16*4`(@ptr[3]),@ptr[3]
vmovd		`4*$j-16*4`(@ptr[0]),@Xi[1]
vpunpckldq	@Xi[2],@Xi[0],@Xi[0]
vmovd		`4*$j-16*4`($ptr_n),$t3
vpshufb		$tx,@Xi[0],@Xi[0]
___
$code.=<<___ if ($i<15 && $REG_SZ==16);
vpinsrd	\$1,`4*$j-16*4`(@ptr[2]),@Xi[1],@Xi[1]
vpinsrd	\$1,`4*$j-16*4`(@ptr[3]),$t3,$t3
___
$code.=<<___ if ($i==0 && $REG_SZ==32);
vmovd		(@ptr[0]),@Xi[0]
lea		`16*4`(@ptr[0]),@ptr[0]
vmovd		(@ptr[4]),@Xi[2]
lea		`16*4`(@ptr[4]),@ptr[4]
vmovd		(@ptr[1]),$t2
lea		`16*4`(@ptr[1]),@ptr[1]
vmovd		(@ptr[5]),$t1
lea		`16*4`(@ptr[5]),@ptr[5]
vpinsrd		\$1,(@ptr[2]),@Xi[0],@Xi[0]
lea		`16*4`(@ptr[2]),@ptr[2]
vpinsrd		\$1,(@ptr[6]),@Xi[2],@Xi[2]
lea		`16*4`(@ptr[6]),@ptr[6]
vpinsrd		\$1,(@ptr[3]),$t2,$t2
lea		`16*4`(@ptr[3]),@ptr[3]
vpunpckldq	$t2,@Xi[0],@Xi[0]
vpinsrd		\$1,(@ptr[7]),$t1,$t1
lea		`16*4`(@ptr[7]),@ptr[7]
vpunpckldq	$t1,@Xi[2],@Xi[2]
vmovd		`4*$j-16*4`(@ptr[0]),@Xi[1]
vinserti128	@Xi[2],@Xi[0],@Xi[0]
vmovd		`4*$j-16*4`($ptr_n),$t3
vpshufb		$tx,@Xi[0],@Xi[0]
___
$code.=<<___ if ($i<15 && $REG_SZ==32);
vmovd		`4*$j-16*4`(@ptr[1]),$t2
vmovd		`4*$j-16*4`(@ptr[5]),$t1
vpinsrd	\$1,`4*$j-16*4`(@ptr[2]),@Xi[1],@Xi[1]
vpinsrd	\$1,`4*$j-16*4`(@ptr[6]),$t3,$t3
vpinsrd	\$1,`4*$j-16*4`(@ptr[3]),$t2,$t2
vpunpckldq	$t2,@Xi[1],@Xi[1]
vpinsrd	\$1,`4*$j-16*4`(@ptr[7]),$t1,$t1
vpunpckldq	$t1,$t3,$t3
___
$code.=<<___ if ($i<14);
vpaddd	$K,$e,$e
vpslld	\$5,$a,$t2
vpandn	$d,$b,$t1
vpand	$c,$b,$t0
vmovdqa	@Xi[0],`&Xi_off($i)`
vpaddd	@Xi[0],$e,$e
$vpack		$t3,@Xi[1],@Xi[1]
vpsrld	\$27,$a,$t3
vpxor	$t1,$t0,$t0
vmovd		`4*$k-16*4`(@ptr[0]),@Xi[2]
vpslld	\$30,$b,$t1
vpor	$t3,$t2,$t2
vmovd		`4*$k-16*4`($ptr_n),$t3
vpaddd	$t0,$e,$e
vpsrld	\$2,$b,$b
vpaddd	$t2,$e,$e
vpshufb	$tx,@Xi[1],@Xi[1]
vpor	$t1,$b,$b
___
$code.=<<___ if ($i==14);
vpaddd	$K,$e,$e
prefetcht0	63(@ptr[0])
vpslld	\$5,$a,$t2
vpandn	$d,$b,$t1
vpand	$c,$b,$t0
vmovdqa	@Xi[0],`&Xi_off($i)`
vpaddd	@Xi[0],$e,$e
$vpack		$t3,@Xi[1],@Xi[1]
vpsrld	\$27,$a,$t3
prefetcht0	63(@ptr[1])
vpxor	$t1,$t0,$t0
vpslld	\$30,$b,$t1
vpor	$t3,$t2,$t2
prefetcht0	63(@ptr[2])
vpaddd	$t0,$e,$e
vpsrld	\$2,$b,$b
vpaddd	$t2,$e,$e
prefetcht0	63(@ptr[3])
vpshufb	$tx,@Xi[1],@Xi[1]
vpor	$t1,$b,$b
___
$code.=<<___ if ($i>=13 && $i<15);
vmovdqa	`&Xi_off($j+2)`,@Xi[3]
___
$code.=<<___ if ($i>=15);
vpxor	@Xi[-2],@Xi[1],@Xi[1]
vmovdqa	`&Xi_off($j+2)`,@Xi[3]
vpaddd	$K,$e,$e
vpslld	\$5,$a,$t2
vpandn	$d,$b,$t1
`"prefetcht0	63(@ptr[4])"		if ($i==15 && $REG_SZ==32)`
vpand	$c,$b,$t0
vmovdqa	@Xi[0],`&Xi_off($i)`
vpaddd	@Xi[0],$e,$e
vpxor	`&Xi_off($j+8)`,@Xi[1],@Xi[1]
vpsrld	\$27,$a,$t3
vpxor	$t1,$t0,$t0
vpxor	@Xi[3],@Xi[1],@Xi[1]
`"prefetcht0	63(@ptr[5])"		if ($i==15 && $REG_SZ==32)`
vpslld	\$30,$b,$t1
vpor	$t3,$t2,$t2
vpaddd	$t0,$e,$e
`"prefetcht0	63(@ptr[6])"		if ($i==15 && $REG_SZ==32)`
vpsrld	\$31,@Xi[1],$tx
vpaddd	@Xi[1],@Xi[1],@Xi[1]
vpsrld	\$2,$b,$b
`"prefetcht0	63(@ptr[7])"		if ($i==15 && $REG_SZ==32)`
vpaddd	$t2,$e,$e
vpor	$tx,@Xi[1],@Xi[1]
vpor	$t1,$b,$b
___
push(@Xi,shift(@Xi));
}
sub BODY_20_39_avx {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
$code.=<<___ if ($i<79);
vpxor	@Xi[-2],@Xi[1],@Xi[1]
vmovdqa	`&Xi_off($j+2)`,@Xi[3]
vpslld	\$5,$a,$t2
vpaddd	$K,$e,$e
vpxor	$b,$d,$t0
___
$code.=<<___ if ($i<72);
vmovdqa	@Xi[0],`&Xi_off($i)`
___
$code.=<<___ if ($i<79);
vpaddd	@Xi[0],$e,$e
vpxor	`&Xi_off($j+8)`,@Xi[1],@Xi[1]
vpsrld	\$27,$a,$t3
vpxor	$c,$t0,$t0
vpxor	@Xi[3],@Xi[1],@Xi[1]
vpslld	\$30,$b,$t1
vpor	$t3,$t2,$t2
vpaddd	$t0,$e,$e
vpsrld	\$31,@Xi[1],$tx
vpaddd	@Xi[1],@Xi[1],@Xi[1]
vpsrld	\$2,$b,$b
vpaddd	$t2,$e,$e
vpor	$tx,@Xi[1],@Xi[1]
vpor	$t1,$b,$b
___
$code.=<<___ if ($i==79);
vpslld	\$5,$a,$t2
vpaddd	$K,$e,$e
vpxor	$b,$d,$t0
vpsrld	\$27,$a,$t3
vpaddd	@Xi[0],$e,$e
vpxor	$c,$t0,$t0
vpslld	\$30,$b,$t1
vpor	$t3,$t2,$t2
vpaddd	$t0,$e,$e
vpsrld	\$2,$b,$b
vpaddd	$t2,$e,$e
vpor	$t1,$b,$b
___
push(@Xi,shift(@Xi));
}
sub BODY_40_59_avx {
my ($i,$a,$b,$c,$d,$e)=@_;
my $j=$i+1;
$code.=<<___;
vpxor	@Xi[-2],@Xi[1],@Xi[1]
vmovdqa	`&Xi_off($j+2)`,@Xi[3]
vpaddd	$K,$e,$e
vpslld	\$5,$a,$t2
vpand	$c,$d,$t1
vpxor	`&Xi_off($j+8)`,@Xi[1],@Xi[1]
vpaddd	$t1,$e,$e
vpsrld	\$27,$a,$t3
vpxor	$c,$d,$t0
vpxor	@Xi[3],@Xi[1],@Xi[1]
vmovdqu	@Xi[0],`&Xi_off($i)`
vpaddd	@Xi[0],$e,$e
vpor	$t3,$t2,$t2
vpsrld	\$31,@Xi[1],$tx
vpand	$b,$t0,$t0
vpaddd	@Xi[1],@Xi[1],@Xi[1]
vpslld	\$30,$b,$t1
vpaddd	$t0,$e,$e
vpsrld	\$2,$b,$b
vpaddd	$t2,$e,$e
vpor	$tx,@Xi[1],@Xi[1]
vpor	$t1,$b,$b
___
push(@Xi,shift(@Xi));
}
$code.=<<___;
.type	sha1_multi_block_avx,\@function,3
.align	32
sha1_multi_block_avx:
_avx_shortcut:
___
$code.=<<___ if ($avx>1);
shr	\$32,%rcx
cmp	\$2,$num
jb	.Lavx
test	\$`1<<5`,%ecx
jnz	_avx2_shortcut
jmp	.Lavx
.align	32
.Lavx:
___
$code.=<<___;
mov	%rsp,%rax
push	%rbx
push	%rbp
___
$code.=<<___ if ($win64);
lea	-0xa8(%rsp),%rsp
movaps	%xmm6,(%rsp)
movaps	%xmm7,0x10(%rsp)
movaps	%xmm8,0x20(%rsp)
movaps	%xmm9,0x30(%rsp)
movaps	%xmm10,-0x78(%rax)
movaps	%xmm11,-0x68(%rax)
movaps	%xmm12,-0x58(%rax)
movaps	%xmm13,-0x48(%rax)
movaps	%xmm14,-0x38(%rax)
movaps	%xmm15,-0x28(%rax)
___
$code.=<<___;
sub	\$`$REG_SZ*18`, %rsp
and	\$-256,%rsp
mov	%rax,`$REG_SZ*17`(%rsp)
.Lbody_avx:
lea	K_XX_XX(%rip),$Tbl
lea	`$REG_SZ*16`(%rsp),%rbx
vzeroupper
.Loop_grande_avx:
mov	$num,`$REG_SZ*17+8`(%rsp)
xor	$num,$num
___
for($i=0;$i<4;$i++) {
$code.=<<___;
mov	`16*$i+0`($inp),@ptr[$i]
mov	`16*$i+8`($inp),%ecx
cmp	$num,%ecx
cmovg	%ecx,$num
test	%ecx,%ecx
mov	%ecx,`4*$i`(%rbx)
cmovle	$Tbl,@ptr[$i]
___
}
$code.=<<___;
test	$num,$num
jz	.Ldone_avx
vmovdqu	0x00($ctx),$A
lea	128(%rsp),%rax
vmovdqu	0x20($ctx),$B
vmovdqu	0x40($ctx),$C
vmovdqu	0x60($ctx),$D
vmovdqu	0x80($ctx),$E
vmovdqu	0x60($Tbl),$tx
jmp	.Loop_avx
.align	32
.Loop_avx:
___
$code.="	vmovdqa	-0x20($Tbl),$K\n";
for($i=0;$i<20;$i++)	{ &BODY_00_19_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x00($Tbl),$K\n";
for(;$i<40;$i++)	{ &BODY_20_39_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x20($Tbl),$K\n";
for(;$i<60;$i++)	{ &BODY_40_59_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x40($Tbl),$K\n";
for(;$i<80;$i++)	{ &BODY_20_39_avx($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
mov	\$1,%ecx
___
for($i=0;$i<4;$i++) {
$code.=<<___;
cmp	`4*$i`(%rbx),%ecx
cmovge	$Tbl,@ptr[$i]
___
}
$code.=<<___;
vmovdqu	(%rbx),$t0
vpxor	$t2,$t2,$t2
vmovdqa	$t0,$t1
vpcmpgtd $t2,$t1,$t1
vpaddd	$t1,$t0,$t0
vpand	$t1,$A,$A
vpand	$t1,$B,$B
vpaddd	0x00($ctx),$A,$A
vpand	$t1,$C,$C
vpaddd	0x20($ctx),$B,$B
vpand	$t1,$D,$D
vpaddd	0x40($ctx),$C,$C
vpand	$t1,$E,$E
vpaddd	0x60($ctx),$D,$D
vpaddd	0x80($ctx),$E,$E
vmovdqu	$A,0x00($ctx)
vmovdqu	$B,0x20($ctx)
vmovdqu	$C,0x40($ctx)
vmovdqu	$D,0x60($ctx)
vmovdqu	$E,0x80($ctx)
vmovdqu	$t0,(%rbx)
vmovdqu	0x60($Tbl),$tx
dec	$num
jnz	.Loop_avx
mov	`$REG_SZ*17+8`(%rsp),$num
lea	$REG_SZ($ctx),$ctx
lea	`16*$REG_SZ/4`($inp),$inp
dec	$num
jnz	.Loop_grande_avx
.Ldone_avx:
mov	`$REG_SZ*17`(%rsp),%rax
vzeroupper
___
$code.=<<___ if ($win64);
movaps	-0xb8(%rax),%xmm6
movaps	-0xa8(%rax),%xmm7
movaps	-0x98(%rax),%xmm8
movaps	-0x88(%rax),%xmm9
movaps	-0x78(%rax),%xmm10
movaps	-0x68(%rax),%xmm11
movaps	-0x58(%rax),%xmm12
movaps	-0x48(%rax),%xmm13
movaps	-0x38(%rax),%xmm14
movaps	-0x28(%rax),%xmm15
___
$code.=<<___;
mov	-16(%rax),%rbp
mov	-8(%rax),%rbx
lea	(%rax),%rsp
.Lepilogue_avx:
ret
.size	sha1_multi_block_avx,.-sha1_multi_block_avx
___
if ($avx>1) {
$code =~ s/\`([^\`]*)\`/eval $1/gem;
$REG_SZ=32;
@ptr=map("%r$_",(12..15,8..11));
@V=($A,$B,$C,$D,$E)=map("%ymm$_",(0..4));
($t0,$t1,$t2,$t3,$tx)=map("%ymm$_",(5..9));
@Xi=map("%ymm$_",(10..14));
$K="%ymm15";
$code.=<<___;
.type	sha1_multi_block_avx2,\@function,3
.align	32
sha1_multi_block_avx2:
_avx2_shortcut:
mov	%rsp,%rax
push	%rbx
push	%rbp
push	%r12
push	%r13
push	%r14
push	%r15
___
$code.=<<___ if ($win64);
lea	-0xa8(%rsp),%rsp
movaps	%xmm6,(%rsp)
movaps	%xmm7,0x10(%rsp)
movaps	%xmm8,0x20(%rsp)
movaps	%xmm9,0x30(%rsp)
movaps	%xmm10,0x40(%rsp)
movaps	%xmm11,0x50(%rsp)
movaps	%xmm12,-0x78(%rax)
movaps	%xmm13,-0x68(%rax)
movaps	%xmm14,-0x58(%rax)
movaps	%xmm15,-0x48(%rax)
___
$code.=<<___;
sub	\$`$REG_SZ*18`, %rsp
and	\$-256,%rsp
mov	%rax,`$REG_SZ*17`(%rsp)
.Lbody_avx2:
lea	K_XX_XX(%rip),$Tbl
shr	\$1,$num
vzeroupper
.Loop_grande_avx2:
mov	$num,`$REG_SZ*17+8`(%rsp)
xor	$num,$num
lea	`$REG_SZ*16`(%rsp),%rbx
___
for($i=0;$i<8;$i++) {
$code.=<<___;
mov	`16*$i+0`($inp),@ptr[$i]
mov	`16*$i+8`($inp),%ecx
cmp	$num,%ecx
cmovg	%ecx,$num
test	%ecx,%ecx
mov	%ecx,`4*$i`(%rbx)
cmovle	$Tbl,@ptr[$i]
___
}
$code.=<<___;
vmovdqu	0x00($ctx),$A
lea	128(%rsp),%rax
vmovdqu	0x20($ctx),$B
lea	256+128(%rsp),%rbx
vmovdqu	0x40($ctx),$C
vmovdqu	0x60($ctx),$D
vmovdqu	0x80($ctx),$E
vmovdqu	0x60($Tbl),$tx
jmp	.Loop_avx2
.align	32
.Loop_avx2:
___
$code.="	vmovdqa	-0x20($Tbl),$K\n";
for($i=0;$i<20;$i++)	{ &BODY_00_19_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x00($Tbl),$K\n";
for(;$i<40;$i++)	{ &BODY_20_39_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x20($Tbl),$K\n";
for(;$i<60;$i++)	{ &BODY_40_59_avx($i,@V); unshift(@V,pop(@V)); }
$code.="	vmovdqa	0x40($Tbl),$K\n";
for(;$i<80;$i++)	{ &BODY_20_39_avx($i,@V); unshift(@V,pop(@V)); }
$code.=<<___;
mov	\$1,%ecx
lea	`$REG_SZ*16`(%rsp),%rbx
___
for($i=0;$i<8;$i++) {
$code.=<<___;
cmp	`4*$i`(%rbx),%ecx
cmovge	$Tbl,@ptr[$i]
___
}
$code.=<<___;
vmovdqu	(%rbx),$t0
vpxor	$t2,$t2,$t2
vmovdqa	$t0,$t1
vpcmpgtd $t2,$t1,$t1
vpaddd	$t1,$t0,$t0
vpand	$t1,$A,$A
vpand	$t1,$B,$B
vpaddd	0x00($ctx),$A,$A
vpand	$t1,$C,$C
vpaddd	0x20($ctx),$B,$B
vpand	$t1,$D,$D
vpaddd	0x40($ctx),$C,$C
vpand	$t1,$E,$E
vpaddd	0x60($ctx),$D,$D
vpaddd	0x80($ctx),$E,$E
vmovdqu	$A,0x00($ctx)
vmovdqu	$B,0x20($ctx)
vmovdqu	$C,0x40($ctx)
vmovdqu	$D,0x60($ctx)
vmovdqu	$E,0x80($ctx)
vmovdqu	$t0,(%rbx)
lea	256+128(%rsp),%rbx
vmovdqu	0x60($Tbl),$tx
dec	$num
jnz	.Loop_avx2
.Ldone_avx2:
mov	`$REG_SZ*17`(%rsp),%rax
vzeroupper
___
$code.=<<___ if ($win64);
movaps	-0xd8(%rax),%xmm6
movaps	-0xc8(%rax),%xmm7
movaps	-0xb8(%rax),%xmm8
movaps	-0xa8(%rax),%xmm9
movaps	-0x98(%rax),%xmm10
movaps	-0x88(%rax),%xmm11
movaps	-0x78(%rax),%xmm12
movaps	-0x68(%rax),%xmm13
movaps	-0x58(%rax),%xmm14
movaps	-0x48(%rax),%xmm15
___
$code.=<<___;
mov	-48(%rax),%r15
mov	-40(%rax),%r14
mov	-32(%rax),%r13
mov	-24(%rax),%r12
mov	-16(%rax),%rbp
mov	-8(%rax),%rbx
lea	(%rax),%rsp
.Lepilogue_avx2:
ret
.size	sha1_multi_block_avx2,.-sha1_multi_block_avx2
___
}	}}}
$code.=<<___;
.align	256
.long	0x5a827999,0x5a827999,0x5a827999,0x5a827999
.long	0x5a827999,0x5a827999,0x5a827999,0x5a827999
K_XX_XX:
.long	0x6ed9eba1,0x6ed9eba1,0x6ed9eba1,0x6ed9eba1
.long	0x6ed9eba1,0x6ed9eba1,0x6ed9eba1,0x6ed9eba1
.long	0x8f1bbcdc,0x8f1bbcdc,0x8f1bbcdc,0x8f1bbcdc
.long	0x8f1bbcdc,0x8f1bbcdc,0x8f1bbcdc,0x8f1bbcdc
.long	0xca62c1d6,0xca62c1d6,0xca62c1d6,0xca62c1d6
.long	0xca62c1d6,0xca62c1d6,0xca62c1d6,0xca62c1d6
.long	0x00010203,0x04050607,0x08090a0b,0x0c0d0e0f
.long	0x00010203,0x04050607,0x08090a0b,0x0c0d0e0f
.byte	0xf,0xe,0xd,0xc,0xb,0xa,0x9,0x8,0x7,0x6,0x5,0x4,0x3,0x2,0x1,0x0
.asciz	"SHA1 multi-block transform for x86_64, CRYPTOGAMS by <appro\@openssl.org>"
___
if ($win64) {
$rec="%rcx";
$frame="%rdx";
$context="%r8";
$disp="%r9";
$code.=<<___;
.extern	__imp_RtlVirtualUnwind
.type	se_handler,\@abi-omnipotent
.align	16
se_handler:
push	%rsi
push	%rdi
push	%rbx
push	%rbp
push	%r12
push	%r13
push	%r14
push	%r15
pushfq
sub	\$64,%rsp
mov	120($context),%rax
mov	248($context),%rbx
mov	8($disp),%rsi
mov	56($disp),%r11
mov	0(%r11),%r10d
lea	(%rsi,%r10),%r10
cmp	%r10,%rbx
jb	.Lin_prologue
mov	152($context),%rax
mov	4(%r11),%r10d
lea	(%rsi,%r10),%r10
cmp	%r10,%rbx
jae	.Lin_prologue
mov	`16*17`(%rax),%rax
mov	-8(%rax),%rbx
mov	-16(%rax),%rbp
mov	%rbx,144($context)
mov	%rbp,160($context)
lea	-24-10*16(%rax),%rsi
lea	512($context),%rdi
mov	\$20,%ecx
.long	0xa548f3fc
.Lin_prologue:
mov	8(%rax),%rdi
mov	16(%rax),%rsi
mov	%rax,152($context)
mov	%rsi,168($context)
mov	%rdi,176($context)
mov	40($disp),%rdi
mov	$context,%rsi
mov	\$154,%ecx
.long	0xa548f3fc
mov	$disp,%rsi
xor	%rcx,%rcx
mov	8(%rsi),%rdx
mov	0(%rsi),%r8
mov	16(%rsi),%r9
mov	40(%rsi),%r10
lea	56(%rsi),%r11
lea	24(%rsi),%r12
mov	%r10,32(%rsp)
mov	%r11,40(%rsp)
mov	%r12,48(%rsp)
mov	%rcx,56(%rsp)
call	*__imp_RtlVirtualUnwind(%rip)
mov	\$1,%eax
add	\$64,%rsp
popfq
pop	%r15
pop	%r14
pop	%r13
pop	%r12
pop	%rbp
pop	%rbx
pop	%rdi
pop	%rsi
ret
.size	se_handler,.-se_handler
___
$code.=<<___ if ($avx>1);
.type	avx2_handler,\@abi-omnipotent
.align	16
avx2_handler:
push	%rsi
push	%rdi
push	%rbx
push	%rbp
push	%r12
push	%r13
push	%r14
push	%r15
pushfq
sub	\$64,%rsp
mov	120($context),%rax
mov	248($context),%rbx
mov	8($disp),%rsi
mov	56($disp),%r11
mov	0(%r11),%r10d
lea	(%rsi,%r10),%r10
cmp	%r10,%rbx
jb	.Lin_prologue
mov	152($context),%rax
mov	4(%r11),%r10d
lea	(%rsi,%r10),%r10
cmp	%r10,%rbx
jae	.Lin_prologue
mov	`32*17`($context),%rax
mov	-8(%rax),%rbx
mov	-16(%rax),%rbp
mov	-24(%rax),%r12
mov	-32(%rax),%r13
mov	-40(%rax),%r14
mov	-48(%rax),%r15
mov	%rbx,144($context)
mov	%rbp,160($context)
mov	%r12,216($context)
mov	%r13,224($context)
mov	%r14,232($context)
mov	%r15,240($context)
lea	-56-10*16(%rax),%rsi
lea	512($context),%rdi
mov	\$20,%ecx
.long	0xa548f3fc
jmp	.Lin_prologue
.size	avx2_handler,.-avx2_handler
___
$code.=<<___;
.section	.pdata
.align	4
.rva	.LSEH_begin_sha1_multi_block
.rva	.LSEH_end_sha1_multi_block
.rva	.LSEH_info_sha1_multi_block
.rva	.LSEH_begin_sha1_multi_block_shaext
.rva	.LSEH_end_sha1_multi_block_shaext
.rva	.LSEH_info_sha1_multi_block_shaext
___
$code.=<<___ if ($avx);
.rva	.LSEH_begin_sha1_multi_block_avx
.rva	.LSEH_end_sha1_multi_block_avx
.rva	.LSEH_info_sha1_multi_block_avx
___
$code.=<<___ if ($avx>1);
.rva	.LSEH_begin_sha1_multi_block_avx2
.rva	.LSEH_end_sha1_multi_block_avx2
.rva	.LSEH_info_sha1_multi_block_avx2
___
$code.=<<___;
.section	.xdata
.align	8
.LSEH_info_sha1_multi_block:
.byte	9,0,0,0
.rva	se_handler
.rva	.Lbody,.Lepilogue
.LSEH_info_sha1_multi_block_shaext:
.byte	9,0,0,0
.rva	se_handler
.rva	.Lbody_shaext,.Lepilogue_shaext
___
$code.=<<___ if ($avx);
.LSEH_info_sha1_multi_block_avx:
.byte	9,0,0,0
.rva	se_handler
.rva	.Lbody_avx,.Lepilogue_avx
___
$code.=<<___ if ($avx>1);
.LSEH_info_sha1_multi_block_avx2:
.byte	9,0,0,0
.rva	avx2_handler
.rva	.Lbody_avx2,.Lepilogue_avx2
___
}
sub rex {
local *opcode=shift;
my ($dst,$src)=@_;
my $rex=0;
$rex|=0x04			if ($dst>=8);
$rex|=0x01			if ($src>=8);
unshift @opcode,$rex|0x40	if ($rex);
}
sub sha1rnds4 {
if (@_[0] =~ /\$([x0-9a-f]+),\s*%xmm([0-9]+),\s*%xmm([0-9]+)/) {
my @opcode=(0x0f,0x3a,0xcc);
rex(\@opcode,$3,$2);
push @opcode,0xc0|($2&7)|(($3&7)<<3);
my $c=$1;
push @opcode,$c=~/^0/?oct($c):$c;
return ".byte\t".join(',',@opcode);
} else {
return "sha1rnds4\t".@_[0];
}
}
sub sha1op38 {
my $instr = shift;
my %opcodelet = (
"sha1nexte" => 0xc8,
"sha1msg1"  => 0xc9,
"sha1msg2"  => 0xca	);
if (defined($opcodelet{$instr}) && @_[0] =~ /%xmm([0-9]+),\s*%xmm([0-9]+)/) {
my @opcode=(0x0f,0x38);
rex(\@opcode,$2,$1);
push @opcode,$opcodelet{$instr};
push @opcode,0xc0|($1&7)|(($2&7)<<3);
return ".byte\t".join(',',@opcode);
} else {
return $instr."\t".@_[0];
}
}
foreach (split("\n",$code)) {
s/\`([^\`]*)\`/eval($1)/ge;
s/\b(sha1rnds4)\s+(.*)/sha1rnds4($2)/geo		or
s/\b(sha1[^\s]*)\s+(.*)/sha1op38($1,$2)/geo		or
s/\b(vmov[dq])\b(.+)%ymm([0-9]+)/$1$2%xmm$3/go		or
s/\b(vmovdqu)\b(.+)%x%ymm([0-9]+)/$1$2%xmm$3/go		or
s/\b(vpinsr[qd])\b(.+)%ymm([0-9]+),%ymm([0-9]+)/$1$2%xmm$3,%xmm$4/go	or
s/\b(vpextr[qd])\b(.+)%ymm([0-9]+)/$1$2%xmm$3/go	or
s/\b(vinserti128)\b(\s+)%ymm/$1$2\$1,%xmm/go		or
s/\b(vpbroadcast[qd]\s+)%ymm([0-9]+)/$1%xmm$2/go;
print $_,"\n";
}
close STDOUT;
