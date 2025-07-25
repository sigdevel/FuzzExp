#!/usr/bin/env perl
$flavour = shift || "o32";
while (($output=shift) && ($output!~/^\w[\w\-]*\.\w+$/)) {}
open STDOUT,">$output";
if ($flavour =~ /64|n32/i) {
$LD="ld";
$ST="sd";
$MULTU="dmultu";
$DIVU="ddivu";
$ADDU="daddu";
$SUBU="dsubu";
$SRL="dsrl";
$SLL="dsll";
$BNSZ=8;
$PTR_ADD="daddu";
$PTR_SUB="dsubu";
$SZREG=8;
$REG_S="sd";
$REG_L="ld";
} else {
$LD="lw";
$ST="sw";
$MULTU="multu";
$DIVU="divu";
$ADDU="addu";
$SUBU="subu";
$SRL="srl";
$SLL="sll";
$BNSZ=4;
$PTR_ADD="addu";
$PTR_SUB="subu";
$SZREG=4;
$REG_S="sw";
$REG_L="lw";
$code=".set	mips2\n";
}
($zero,$at,$v0,$v1)=map("\$$_",(0..3));
($a0,$a1,$a2,$a3,$a4,$a5,$a6,$a7)=map("\$$_",(4..11));
($t0,$t1,$t2,$t3,$t8,$t9)=map("\$$_",(12..15,24,25));
($s0,$s1,$s2,$s3,$s4,$s5,$s6,$s7)=map("\$$_",(16..23));
($gp,$sp,$fp,$ra)=map("\$$_",(28..31));
($ta0,$ta1,$ta2,$ta3)=($a4,$a5,$a6,$a7);
$gp=$v1 if ($flavour =~ /nubi/i);
$minus4=$v1;
$code.=<<___;
.rdata
.asciiz	"mips3.s, Version 1.2"
.asciiz	"MIPS II/III/IV ISA artwork by Andy Polyakov <appro\@fy.chalmers.se>"
.text
.set	noat
.align	5
.globl	bn_mul_add_words
.ent	bn_mul_add_words
bn_mul_add_words:
.set	noreorder
bgtz	$a2,bn_mul_add_words_internal
move	$v0,$zero
jr	$ra
move	$a0,$v0
.end	bn_mul_add_words
.align	5
.ent	bn_mul_add_words_internal
bn_mul_add_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
li	$minus4,-4
and	$ta0,$a2,$minus4
beqz	$ta0,.L_bn_mul_add_words_tail
.L_bn_mul_add_words_loop:
$LD	$t0,0($a1)
$MULTU	$t0,$a3
$LD	$t1,0($a0)
$LD	$t2,$BNSZ($a1)
$LD	$t3,$BNSZ($a0)
$LD	$ta0,2*$BNSZ($a1)
$LD	$ta1,2*$BNSZ($a0)
$ADDU	$t1,$v0
sltu	$v0,$t1,$v0
mflo	$at
mfhi	$t0
$ADDU	$t1,$at
$ADDU	$v0,$t0
$MULTU	$t2,$a3
sltu	$at,$t1,$at
$ST	$t1,0($a0)
$ADDU	$v0,$at
$LD	$ta2,3*$BNSZ($a1)
$LD	$ta3,3*$BNSZ($a0)
$ADDU	$t3,$v0
sltu	$v0,$t3,$v0
mflo	$at
mfhi	$t2
$ADDU	$t3,$at
$ADDU	$v0,$t2
$MULTU	$ta0,$a3
sltu	$at,$t3,$at
$ST	$t3,$BNSZ($a0)
$ADDU	$v0,$at
subu	$a2,4
$PTR_ADD $a0,4*$BNSZ
$PTR_ADD $a1,4*$BNSZ
$ADDU	$ta1,$v0
sltu	$v0,$ta1,$v0
mflo	$at
mfhi	$ta0
$ADDU	$ta1,$at
$ADDU	$v0,$ta0
$MULTU	$ta2,$a3
sltu	$at,$ta1,$at
$ST	$ta1,-2*$BNSZ($a0)
$ADDU	$v0,$at
and	$ta0,$a2,$minus4
$ADDU	$ta3,$v0
sltu	$v0,$ta3,$v0
mflo	$at
mfhi	$ta2
$ADDU	$ta3,$at
$ADDU	$v0,$ta2
sltu	$at,$ta3,$at
$ST	$ta3,-$BNSZ($a0)
.set	noreorder
bgtz	$ta0,.L_bn_mul_add_words_loop
$ADDU	$v0,$at
beqz	$a2,.L_bn_mul_add_words_return
nop
.L_bn_mul_add_words_tail:
.set	reorder
$LD	$t0,0($a1)
$MULTU	$t0,$a3
$LD	$t1,0($a0)
subu	$a2,1
$ADDU	$t1,$v0
sltu	$v0,$t1,$v0
mflo	$at
mfhi	$t0
$ADDU	$t1,$at
$ADDU	$v0,$t0
sltu	$at,$t1,$at
$ST	$t1,0($a0)
$ADDU	$v0,$at
beqz	$a2,.L_bn_mul_add_words_return
$LD	$t0,$BNSZ($a1)
$MULTU	$t0,$a3
$LD	$t1,$BNSZ($a0)
subu	$a2,1
$ADDU	$t1,$v0
sltu	$v0,$t1,$v0
mflo	$at
mfhi	$t0
$ADDU	$t1,$at
$ADDU	$v0,$t0
sltu	$at,$t1,$at
$ST	$t1,$BNSZ($a0)
$ADDU	$v0,$at
beqz	$a2,.L_bn_mul_add_words_return
$LD	$t0,2*$BNSZ($a1)
$MULTU	$t0,$a3
$LD	$t1,2*$BNSZ($a0)
$ADDU	$t1,$v0
sltu	$v0,$t1,$v0
mflo	$at
mfhi	$t0
$ADDU	$t1,$at
$ADDU	$v0,$t0
sltu	$at,$t1,$at
$ST	$t1,2*$BNSZ($a0)
$ADDU	$v0,$at
.L_bn_mul_add_words_return:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_mul_add_words_internal
.align	5
.globl	bn_mul_words
.ent	bn_mul_words
bn_mul_words:
.set	noreorder
bgtz	$a2,bn_mul_words_internal
move	$v0,$zero
jr	$ra
move	$a0,$v0
.end	bn_mul_words
.align	5
.ent	bn_mul_words_internal
bn_mul_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
li	$minus4,-4
and	$ta0,$a2,$minus4
beqz	$ta0,.L_bn_mul_words_tail
.L_bn_mul_words_loop:
$LD	$t0,0($a1)
$MULTU	$t0,$a3
$LD	$t2,$BNSZ($a1)
$LD	$ta0,2*$BNSZ($a1)
$LD	$ta2,3*$BNSZ($a1)
mflo	$at
mfhi	$t0
$ADDU	$v0,$at
sltu	$t1,$v0,$at
$MULTU	$t2,$a3
$ST	$v0,0($a0)
$ADDU	$v0,$t1,$t0
subu	$a2,4
$PTR_ADD $a0,4*$BNSZ
$PTR_ADD $a1,4*$BNSZ
mflo	$at
mfhi	$t2
$ADDU	$v0,$at
sltu	$t3,$v0,$at
$MULTU	$ta0,$a3
$ST	$v0,-3*$BNSZ($a0)
$ADDU	$v0,$t3,$t2
mflo	$at
mfhi	$ta0
$ADDU	$v0,$at
sltu	$ta1,$v0,$at
$MULTU	$ta2,$a3
$ST	$v0,-2*$BNSZ($a0)
$ADDU	$v0,$ta1,$ta0
and	$ta0,$a2,$minus4
mflo	$at
mfhi	$ta2
$ADDU	$v0,$at
sltu	$ta3,$v0,$at
$ST	$v0,-$BNSZ($a0)
.set	noreorder
bgtz	$ta0,.L_bn_mul_words_loop
$ADDU	$v0,$ta3,$ta2
beqz	$a2,.L_bn_mul_words_return
nop
.L_bn_mul_words_tail:
.set	reorder
$LD	$t0,0($a1)
$MULTU	$t0,$a3
subu	$a2,1
mflo	$at
mfhi	$t0
$ADDU	$v0,$at
sltu	$t1,$v0,$at
$ST	$v0,0($a0)
$ADDU	$v0,$t1,$t0
beqz	$a2,.L_bn_mul_words_return
$LD	$t0,$BNSZ($a1)
$MULTU	$t0,$a3
subu	$a2,1
mflo	$at
mfhi	$t0
$ADDU	$v0,$at
sltu	$t1,$v0,$at
$ST	$v0,$BNSZ($a0)
$ADDU	$v0,$t1,$t0
beqz	$a2,.L_bn_mul_words_return
$LD	$t0,2*$BNSZ($a1)
$MULTU	$t0,$a3
mflo	$at
mfhi	$t0
$ADDU	$v0,$at
sltu	$t1,$v0,$at
$ST	$v0,2*$BNSZ($a0)
$ADDU	$v0,$t1,$t0
.L_bn_mul_words_return:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_mul_words_internal
.align	5
.globl	bn_sqr_words
.ent	bn_sqr_words
bn_sqr_words:
.set	noreorder
bgtz	$a2,bn_sqr_words_internal
move	$v0,$zero
jr	$ra
move	$a0,$v0
.end	bn_sqr_words
.align	5
.ent	bn_sqr_words_internal
bn_sqr_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
li	$minus4,-4
and	$ta0,$a2,$minus4
beqz	$ta0,.L_bn_sqr_words_tail
.L_bn_sqr_words_loop:
$LD	$t0,0($a1)
$MULTU	$t0,$t0
$LD	$t2,$BNSZ($a1)
$LD	$ta0,2*$BNSZ($a1)
$LD	$ta2,3*$BNSZ($a1)
mflo	$t1
mfhi	$t0
$ST	$t1,0($a0)
$ST	$t0,$BNSZ($a0)
$MULTU	$t2,$t2
subu	$a2,4
$PTR_ADD $a0,8*$BNSZ
$PTR_ADD $a1,4*$BNSZ
mflo	$t3
mfhi	$t2
$ST	$t3,-6*$BNSZ($a0)
$ST	$t2,-5*$BNSZ($a0)
$MULTU	$ta0,$ta0
mflo	$ta1
mfhi	$ta0
$ST	$ta1,-4*$BNSZ($a0)
$ST	$ta0,-3*$BNSZ($a0)
$MULTU	$ta2,$ta2
and	$ta0,$a2,$minus4
mflo	$ta3
mfhi	$ta2
$ST	$ta3,-2*$BNSZ($a0)
.set	noreorder
bgtz	$ta0,.L_bn_sqr_words_loop
$ST	$ta2,-$BNSZ($a0)
beqz	$a2,.L_bn_sqr_words_return
nop
.L_bn_sqr_words_tail:
.set	reorder
$LD	$t0,0($a1)
$MULTU	$t0,$t0
subu	$a2,1
mflo	$t1
mfhi	$t0
$ST	$t1,0($a0)
$ST	$t0,$BNSZ($a0)
beqz	$a2,.L_bn_sqr_words_return
$LD	$t0,$BNSZ($a1)
$MULTU	$t0,$t0
subu	$a2,1
mflo	$t1
mfhi	$t0
$ST	$t1,2*$BNSZ($a0)
$ST	$t0,3*$BNSZ($a0)
beqz	$a2,.L_bn_sqr_words_return
$LD	$t0,2*$BNSZ($a1)
$MULTU	$t0,$t0
mflo	$t1
mfhi	$t0
$ST	$t1,4*$BNSZ($a0)
$ST	$t0,5*$BNSZ($a0)
.L_bn_sqr_words_return:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_sqr_words_internal
.align	5
.globl	bn_add_words
.ent	bn_add_words
bn_add_words:
.set	noreorder
bgtz	$a3,bn_add_words_internal
move	$v0,$zero
jr	$ra
move	$a0,$v0
.end	bn_add_words
.align	5
.ent	bn_add_words_internal
bn_add_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
li	$minus4,-4
and	$at,$a3,$minus4
beqz	$at,.L_bn_add_words_tail
.L_bn_add_words_loop:
$LD	$t0,0($a1)
$LD	$ta0,0($a2)
subu	$a3,4
$LD	$t1,$BNSZ($a1)
and	$at,$a3,$minus4
$LD	$t2,2*$BNSZ($a1)
$PTR_ADD $a2,4*$BNSZ
$LD	$t3,3*$BNSZ($a1)
$PTR_ADD $a0,4*$BNSZ
$LD	$ta1,-3*$BNSZ($a2)
$PTR_ADD $a1,4*$BNSZ
$LD	$ta2,-2*$BNSZ($a2)
$LD	$ta3,-$BNSZ($a2)
$ADDU	$ta0,$t0
sltu	$t8,$ta0,$t0
$ADDU	$t0,$ta0,$v0
sltu	$v0,$t0,$ta0
$ST	$t0,-4*$BNSZ($a0)
$ADDU	$v0,$t8
$ADDU	$ta1,$t1
sltu	$t9,$ta1,$t1
$ADDU	$t1,$ta1,$v0
sltu	$v0,$t1,$ta1
$ST	$t1,-3*$BNSZ($a0)
$ADDU	$v0,$t9
$ADDU	$ta2,$t2
sltu	$t8,$ta2,$t2
$ADDU	$t2,$ta2,$v0
sltu	$v0,$t2,$ta2
$ST	$t2,-2*$BNSZ($a0)
$ADDU	$v0,$t8
$ADDU	$ta3,$t3
sltu	$t9,$ta3,$t3
$ADDU	$t3,$ta3,$v0
sltu	$v0,$t3,$ta3
$ST	$t3,-$BNSZ($a0)
.set	noreorder
bgtz	$at,.L_bn_add_words_loop
$ADDU	$v0,$t9
beqz	$a3,.L_bn_add_words_return
nop
.L_bn_add_words_tail:
.set	reorder
$LD	$t0,0($a1)
$LD	$ta0,0($a2)
$ADDU	$ta0,$t0
subu	$a3,1
sltu	$t8,$ta0,$t0
$ADDU	$t0,$ta0,$v0
sltu	$v0,$t0,$ta0
$ST	$t0,0($a0)
$ADDU	$v0,$t8
beqz	$a3,.L_bn_add_words_return
$LD	$t1,$BNSZ($a1)
$LD	$ta1,$BNSZ($a2)
$ADDU	$ta1,$t1
subu	$a3,1
sltu	$t9,$ta1,$t1
$ADDU	$t1,$ta1,$v0
sltu	$v0,$t1,$ta1
$ST	$t1,$BNSZ($a0)
$ADDU	$v0,$t9
beqz	$a3,.L_bn_add_words_return
$LD	$t2,2*$BNSZ($a1)
$LD	$ta2,2*$BNSZ($a2)
$ADDU	$ta2,$t2
sltu	$t8,$ta2,$t2
$ADDU	$t2,$ta2,$v0
sltu	$v0,$t2,$ta2
$ST	$t2,2*$BNSZ($a0)
$ADDU	$v0,$t8
.L_bn_add_words_return:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_add_words_internal
.align	5
.globl	bn_sub_words
.ent	bn_sub_words
bn_sub_words:
.set	noreorder
bgtz	$a3,bn_sub_words_internal
move	$v0,$zero
jr	$ra
move	$a0,$zero
.end	bn_sub_words
.align	5
.ent	bn_sub_words_internal
bn_sub_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
li	$minus4,-4
and	$at,$a3,$minus4
beqz	$at,.L_bn_sub_words_tail
.L_bn_sub_words_loop:
$LD	$t0,0($a1)
$LD	$ta0,0($a2)
subu	$a3,4
$LD	$t1,$BNSZ($a1)
and	$at,$a3,$minus4
$LD	$t2,2*$BNSZ($a1)
$PTR_ADD $a2,4*$BNSZ
$LD	$t3,3*$BNSZ($a1)
$PTR_ADD $a0,4*$BNSZ
$LD	$ta1,-3*$BNSZ($a2)
$PTR_ADD $a1,4*$BNSZ
$LD	$ta2,-2*$BNSZ($a2)
$LD	$ta3,-$BNSZ($a2)
sltu	$t8,$t0,$ta0
$SUBU	$ta0,$t0,$ta0
$SUBU	$t0,$ta0,$v0
sgtu	$v0,$t0,$ta0
$ST	$t0,-4*$BNSZ($a0)
$ADDU	$v0,$t8
sltu	$t9,$t1,$ta1
$SUBU	$ta1,$t1,$ta1
$SUBU	$t1,$ta1,$v0
sgtu	$v0,$t1,$ta1
$ST	$t1,-3*$BNSZ($a0)
$ADDU	$v0,$t9
sltu	$t8,$t2,$ta2
$SUBU	$ta2,$t2,$ta2
$SUBU	$t2,$ta2,$v0
sgtu	$v0,$t2,$ta2
$ST	$t2,-2*$BNSZ($a0)
$ADDU	$v0,$t8
sltu	$t9,$t3,$ta3
$SUBU	$ta3,$t3,$ta3
$SUBU	$t3,$ta3,$v0
sgtu	$v0,$t3,$ta3
$ST	$t3,-$BNSZ($a0)
.set	noreorder
bgtz	$at,.L_bn_sub_words_loop
$ADDU	$v0,$t9
beqz	$a3,.L_bn_sub_words_return
nop
.L_bn_sub_words_tail:
.set	reorder
$LD	$t0,0($a1)
$LD	$ta0,0($a2)
subu	$a3,1
sltu	$t8,$t0,$ta0
$SUBU	$ta0,$t0,$ta0
$SUBU	$t0,$ta0,$v0
sgtu	$v0,$t0,$ta0
$ST	$t0,0($a0)
$ADDU	$v0,$t8
beqz	$a3,.L_bn_sub_words_return
$LD	$t1,$BNSZ($a1)
subu	$a3,1
$LD	$ta1,$BNSZ($a2)
sltu	$t9,$t1,$ta1
$SUBU	$ta1,$t1,$ta1
$SUBU	$t1,$ta1,$v0
sgtu	$v0,$t1,$ta1
$ST	$t1,$BNSZ($a0)
$ADDU	$v0,$t9
beqz	$a3,.L_bn_sub_words_return
$LD	$t2,2*$BNSZ($a1)
$LD	$ta2,2*$BNSZ($a2)
sltu	$t8,$t2,$ta2
$SUBU	$ta2,$t2,$ta2
$SUBU	$t2,$ta2,$v0
sgtu	$v0,$t2,$ta2
$ST	$t2,2*$BNSZ($a0)
$ADDU	$v0,$t8
.L_bn_sub_words_return:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_sub_words_internal
.align 5
.globl	bn_div_3_words
.ent	bn_div_3_words
bn_div_3_words:
.set	noreorder
move	$a3,$a0
$LD	$a0,($a3)
move	$ta2,$a1
bne	$a0,$a2,bn_div_3_words_internal
$LD	$a1,-$BNSZ($a3)
li	$v0,-1
jr	$ra
move	$a0,$v0
.end	bn_div_3_words
.align	5
.ent	bn_div_3_words_internal
bn_div_3_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
move	$ta3,$ra
bal	bn_div_words_internal
move	$ra,$ta3
$MULTU	$ta2,$v0
$LD	$t2,-2*$BNSZ($a3)
move	$ta0,$zero
mfhi	$t1
mflo	$t0
sltu	$t8,$t1,$a1
.L_bn_div_3_words_inner_loop:
bnez	$t8,.L_bn_div_3_words_inner_loop_done
sgeu	$at,$t2,$t0
seq	$t9,$t1,$a1
and	$at,$t9
sltu	$t3,$t0,$ta2
$ADDU	$a1,$a2
$SUBU	$t1,$t3
$SUBU	$t0,$ta2
sltu	$t8,$t1,$a1
sltu	$ta0,$a1,$a2
or	$t8,$ta0
.set	noreorder
beqz	$at,.L_bn_div_3_words_inner_loop
$SUBU	$v0,1
$ADDU	$v0,1
.set	reorder
.L_bn_div_3_words_inner_loop_done:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_div_3_words_internal
.align	5
.globl	bn_div_words
.ent	bn_div_words
bn_div_words:
.set	noreorder
bnez	$a2,bn_div_words_internal
li	$v0,-1
jr	$ra
move	$a0,$v0
.end	bn_div_words
.align	5
.ent	bn_div_words_internal
bn_div_words_internal:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
move	$v1,$zero
bltz	$a2,.L_bn_div_words_body
move	$t9,$v1
$SLL	$a2,1
bgtz	$a2,.-4
addu	$t9,1
.set	reorder
negu	$t1,$t9
li	$t2,-1
$SLL	$t2,$t1
and	$t2,$a0
$SRL	$at,$a1,$t1
.set	noreorder
beqz	$t2,.+12
nop
break	6
.set	reorder
$SLL	$a0,$t9
$SLL	$a1,$t9
or	$a0,$at
___
$QT=$ta0;
$HH=$ta1;
$DH=$v1;
$code.=<<___;
.L_bn_div_words_body:
$SRL	$DH,$a2,4*$BNSZ
sgeu	$at,$a0,$a2
.set	noreorder
beqz	$at,.+12
nop
$SUBU	$a0,$a2
.set	reorder
li	$QT,-1
$SRL	$HH,$a0,4*$BNSZ
$SRL	$QT,4*$BNSZ
beq	$DH,$HH,.L_bn_div_words_skip_div1
$DIVU	$zero,$a0,$DH
mflo	$QT
.L_bn_div_words_skip_div1:
$MULTU	$a2,$QT
$SLL	$t3,$a0,4*$BNSZ
$SRL	$at,$a1,4*$BNSZ
or	$t3,$at
mflo	$t0
mfhi	$t1
.L_bn_div_words_inner_loop1:
sltu	$t2,$t3,$t0
seq	$t8,$HH,$t1
sltu	$at,$HH,$t1
and	$t2,$t8
sltu	$v0,$t0,$a2
or	$at,$t2
.set	noreorder
beqz	$at,.L_bn_div_words_inner_loop1_done
$SUBU	$t1,$v0
$SUBU	$t0,$a2
b	.L_bn_div_words_inner_loop1
$SUBU	$QT,1
.set	reorder
.L_bn_div_words_inner_loop1_done:
$SLL	$a1,4*$BNSZ
$SUBU	$a0,$t3,$t0
$SLL	$v0,$QT,4*$BNSZ
li	$QT,-1
$SRL	$HH,$a0,4*$BNSZ
$SRL	$QT,4*$BNSZ
beq	$DH,$HH,.L_bn_div_words_skip_div2
$DIVU	$zero,$a0,$DH
mflo	$QT
.L_bn_div_words_skip_div2:
$MULTU	$a2,$QT
$SLL	$t3,$a0,4*$BNSZ
$SRL	$at,$a1,4*$BNSZ
or	$t3,$at
mflo	$t0
mfhi	$t1
.L_bn_div_words_inner_loop2:
sltu	$t2,$t3,$t0
seq	$t8,$HH,$t1
sltu	$at,$HH,$t1
and	$t2,$t8
sltu	$v1,$t0,$a2
or	$at,$t2
.set	noreorder
beqz	$at,.L_bn_div_words_inner_loop2_done
$SUBU	$t1,$v1
$SUBU	$t0,$a2
b	.L_bn_div_words_inner_loop2
$SUBU	$QT,1
.set	reorder
.L_bn_div_words_inner_loop2_done:
$SUBU	$a0,$t3,$t0
or	$v0,$QT
$SRL	$v1,$a0,$t9
$SRL	$a2,$t9
.set	noreorder
move	$a1,$v1
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
move	$a0,$v0
.end	bn_div_words_internal
___
undef $HH; undef $QT; undef $DH;
($a_0,$a_1,$a_2,$a_3)=($t0,$t1,$t2,$t3);
($b_0,$b_1,$b_2,$b_3)=($ta0,$ta1,$ta2,$ta3);
($a_4,$a_5,$a_6,$a_7)=($s0,$s2,$s4,$a1);
($b_4,$b_5,$b_6,$b_7)=($s1,$s3,$s5,$a2);
($t_1,$t_2,$c_1,$c_2,$c_3)=($t8,$t9,$v0,$v1,$a3);
$code.=<<___;
.align	5
.globl	bn_mul_comba8
.ent	bn_mul_comba8
bn_mul_comba8:
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,12*$SZREG,$ra
.mask	0x803ff008,-$SZREG
$PTR_SUB $sp,12*$SZREG
$REG_S	$ra,11*$SZREG($sp)
$REG_S	$s5,10*$SZREG($sp)
$REG_S	$s4,9*$SZREG($sp)
$REG_S	$s3,8*$SZREG($sp)
$REG_S	$s2,7*$SZREG($sp)
$REG_S	$s1,6*$SZREG($sp)
$REG_S	$s0,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___ if ($flavour !~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x003f0000,-$SZREG
$PTR_SUB $sp,6*$SZREG
$REG_S	$s5,5*$SZREG($sp)
$REG_S	$s4,4*$SZREG($sp)
$REG_S	$s3,3*$SZREG($sp)
$REG_S	$s2,2*$SZREG($sp)
$REG_S	$s1,1*$SZREG($sp)
$REG_S	$s0,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
$LD	$a_0,0($a1)
$LD	$b_0,0($a2)
$LD	$a_1,$BNSZ($a1)
$LD	$a_2,2*$BNSZ($a1)
$MULTU	$a_0,$b_0
$LD	$a_3,3*$BNSZ($a1)
$LD	$b_1,$BNSZ($a2)
$LD	$b_2,2*$BNSZ($a2)
$LD	$b_3,3*$BNSZ($a2)
mflo	$c_1
mfhi	$c_2
$LD	$a_4,4*$BNSZ($a1)
$LD	$a_5,5*$BNSZ($a1)
$MULTU	$a_0,$b_1
$LD	$a_6,6*$BNSZ($a1)
$LD	$a_7,7*$BNSZ($a1)
$LD	$b_4,4*$BNSZ($a2)
$LD	$b_5,5*$BNSZ($a2)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_1,$b_0
$ADDU	$c_3,$t_2,$at
$LD	$b_6,6*$BNSZ($a2)
$LD	$b_7,7*$BNSZ($a2)
$ST	$c_1,0($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_0
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
$ST	$c_2,$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_1,$b_1
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$b_2
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$b_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,2*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_1,$b_2
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$c_3,$c_2,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_2,$b_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_3,$b_0
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_4,$b_0
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,3*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_3,$b_1
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_2
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_1,$b_3
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_0,$b_4
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_0,$b_5
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,4*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_1,$b_4
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_2,$b_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_3,$b_2
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_4,$b_1
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_5,$b_0
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_6,$b_0
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,5*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_5,$b_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$c_3,$c_2,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_4,$b_2
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_3,$b_3
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_2,$b_4
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_1,$b_5
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_0,$b_6
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_0,$b_7
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,6*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_1,$b_6
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_5
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_3,$b_4
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_4,$b_3
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_5,$b_2
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_6,$b_1
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_7,$b_0
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_7,$b_1
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,7*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_6,$b_2
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_5,$b_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_4,$b_4
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_3,$b_5
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_2,$b_6
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_1,$b_7
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_2,$b_7
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,8*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_3,$b_6
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$c_3,$c_2,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_4,$b_5
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_5,$b_4
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_6,$b_3
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_7,$b_2
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_7,$b_3
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,9*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_6,$b_4
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_5,$b_5
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_4,$b_6
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_3,$b_7
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_4,$b_7
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,10*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_5,$b_6
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_6,$b_5
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_7,$b_4
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_7,$b_5
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,11*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_6,$b_6
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$c_3,$c_2,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_5,$b_7
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_6,$b_7
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,12*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_7,$b_6
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_7,$b_7
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,13*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
$ST	$c_3,14*$BNSZ($a0)
$ST	$c_1,15*$BNSZ($a0)
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$s5,10*$SZREG($sp)
$REG_L	$s4,9*$SZREG($sp)
$REG_L	$s3,8*$SZREG($sp)
$REG_L	$s2,7*$SZREG($sp)
$REG_L	$s1,6*$SZREG($sp)
$REG_L	$s0,5*$SZREG($sp)
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
jr	$ra
$PTR_ADD $sp,12*$SZREG
___
$code.=<<___ if ($flavour !~ /nubi/i);
$REG_L	$s5,5*$SZREG($sp)
$REG_L	$s4,4*$SZREG($sp)
$REG_L	$s3,3*$SZREG($sp)
$REG_L	$s2,2*$SZREG($sp)
$REG_L	$s1,1*$SZREG($sp)
$REG_L	$s0,0*$SZREG($sp)
jr	$ra
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
.end	bn_mul_comba8
.align	5
.globl	bn_mul_comba4
.ent	bn_mul_comba4
bn_mul_comba4:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
$LD	$a_0,0($a1)
$LD	$b_0,0($a2)
$LD	$a_1,$BNSZ($a1)
$LD	$a_2,2*$BNSZ($a1)
$MULTU	$a_0,$b_0
$LD	$a_3,3*$BNSZ($a1)
$LD	$b_1,$BNSZ($a2)
$LD	$b_2,2*$BNSZ($a2)
$LD	$b_3,3*$BNSZ($a2)
mflo	$c_1
mfhi	$c_2
$ST	$c_1,0($a0)
$MULTU	$a_0,$b_1
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_1,$b_0
$ADDU	$c_3,$t_2,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_0
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
$ST	$c_2,$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_1,$b_1
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$b_2
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$b_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,2*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_1,$b_2
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$c_3,$c_2,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_2,$b_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_3,$b_0
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_3,$b_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,3*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_2
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$c_1,$c_3,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_1,$b_3
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$b_3
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,4*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_3,$b_2
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$c_2,$c_1,$t_2
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_3,$b_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,5*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
$ST	$c_1,6*$BNSZ($a0)
$ST	$c_2,7*$BNSZ($a0)
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
nop
.end	bn_mul_comba4
___
($a_4,$a_5,$a_6,$a_7)=($b_0,$b_1,$b_2,$b_3);
sub add_c2 () {
my ($hi,$lo,$c0,$c1,$c2,
$warm,
$an,$bn
)=@_;
$code.=<<___;
mflo	$lo
mfhi	$hi
$ADDU	$c0,$lo
sltu	$at,$c0,$lo
$MULTU	$an,$bn
$ADDU	$c0,$lo
$ADDU	$at,$hi
sltu	$lo,$c0,$lo
$ADDU	$c1,$at
$ADDU	$hi,$lo
___
$code.=<<___	if (!$warm);
sltu	$c2,$c1,$at
$ADDU	$c1,$hi
sltu	$hi,$c1,$hi
$ADDU	$c2,$hi
___
$code.=<<___	if ($warm);
sltu	$at,$c1,$at
$ADDU	$c1,$hi
$ADDU	$c2,$at
sltu	$hi,$c1,$hi
$ADDU	$c2,$hi
___
}
$code.=<<___;
.align	5
.globl	bn_sqr_comba8
.ent	bn_sqr_comba8
bn_sqr_comba8:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
$LD	$a_0,0($a1)
$LD	$a_1,$BNSZ($a1)
$LD	$a_2,2*$BNSZ($a1)
$LD	$a_3,3*$BNSZ($a1)
$MULTU	$a_0,$a_0
$LD	$a_4,4*$BNSZ($a1)
$LD	$a_5,5*$BNSZ($a1)
$LD	$a_6,6*$BNSZ($a1)
$LD	$a_7,7*$BNSZ($a1)
mflo	$c_1
mfhi	$c_2
$ST	$c_1,0($a0)
$MULTU	$a_0,$a_1
mflo	$t_1
mfhi	$t_2
slt	$c_1,$t_2,$zero
$SLL	$t_2,1
$MULTU	$a_2,$a_0
slt	$a2,$t_1,$zero
$ADDU	$t_2,$a2
$SLL	$t_1,1
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$ADDU	$c_3,$t_2,$at
$ST	$c_2,$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_1,$a_1);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$a_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,2*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,0,
$a_1,$a_2);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_4,$a_0);
$code.=<<___;
$ST	$c_1,3*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,0,
$a_3,$a_1);
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,1,
$a_2,$a_2);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_0,$a_5
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,4*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_1,$a_4);
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,1,
$a_2,$a_3);
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,1,
$a_6,$a_0);
$code.=<<___;
$ST	$c_3,5*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,0,
$a_5,$a_1);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_4,$a_2);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_3,$a_3);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_0,$a_7
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,6*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,0,
$a_1,$a_6);
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,1,
$a_2,$a_5);
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,1,
$a_3,$a_4);
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,1,
$a_7,$a_1);
$code.=<<___;
$ST	$c_2,7*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_6,$a_2);
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,1,
$a_5,$a_3);
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,1,
$a_4,$a_4);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_2,$a_7
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,8*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,0,
$a_3,$a_6);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_4,$a_5);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_7,$a_3);
$code.=<<___;
$ST	$c_1,9*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,0,
$a_6,$a_4);
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,1,
$a_5,$a_5);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_4,$a_7
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,10*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_5,$a_6);
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,1,
$a_7,$a_5);
$code.=<<___;
$ST	$c_3,11*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,0,
$a_6,$a_6);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$MULTU	$a_6,$a_7
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
sltu	$at,$c_2,$t_2
$ADDU	$c_3,$at
$ST	$c_1,12*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,0,
$a_7,$a_7);
$code.=<<___;
$ST	$c_2,13*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
$ST	$c_3,14*$BNSZ($a0)
$ST	$c_1,15*$BNSZ($a0)
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
nop
.end	bn_sqr_comba8
.align	5
.globl	bn_sqr_comba4
.ent	bn_sqr_comba4
bn_sqr_comba4:
___
$code.=<<___ if ($flavour =~ /nubi/i);
.frame	$sp,6*$SZREG,$ra
.mask	0x8000f008,-$SZREG
.set	noreorder
$PTR_SUB $sp,6*$SZREG
$REG_S	$ra,5*$SZREG($sp)
$REG_S	$t3,4*$SZREG($sp)
$REG_S	$t2,3*$SZREG($sp)
$REG_S	$t1,2*$SZREG($sp)
$REG_S	$t0,1*$SZREG($sp)
$REG_S	$gp,0*$SZREG($sp)
___
$code.=<<___;
.set	reorder
$LD	$a_0,0($a1)
$LD	$a_1,$BNSZ($a1)
$MULTU	$a_0,$a_0
$LD	$a_2,2*$BNSZ($a1)
$LD	$a_3,3*$BNSZ($a1)
mflo	$c_1
mfhi	$c_2
$ST	$c_1,0($a0)
$MULTU	$a_0,$a_1
mflo	$t_1
mfhi	$t_2
slt	$c_1,$t_2,$zero
$SLL	$t_2,1
$MULTU	$a_2,$a_0
slt	$a2,$t_1,$zero
$ADDU	$t_2,$a2
$SLL	$t_1,1
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$ADDU	$c_3,$t_2,$at
$ST	$c_2,$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_1,$a_1);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_3,$t_1
sltu	$at,$c_3,$t_1
$MULTU	$a_0,$a_3
$ADDU	$t_2,$at
$ADDU	$c_1,$t_2
sltu	$at,$c_1,$t_2
$ADDU	$c_2,$at
$ST	$c_3,2*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,0,
$a_1,$a_2);
&add_c2($t_2,$t_1,$c_1,$c_2,$c_3,1,
$a_3,$a_1);
$code.=<<___;
$ST	$c_1,3*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_2,$c_3,$c_1,0,
$a_2,$a_2);
$code.=<<___;
mflo	$t_1
mfhi	$t_2
$ADDU	$c_2,$t_1
sltu	$at,$c_2,$t_1
$MULTU	$a_2,$a_3
$ADDU	$t_2,$at
$ADDU	$c_3,$t_2
sltu	$at,$c_3,$t_2
$ADDU	$c_1,$at
$ST	$c_2,4*$BNSZ($a0)
___
&add_c2($t_2,$t_1,$c_3,$c_1,$c_2,0,
$a_3,$a_3);
$code.=<<___;
$ST	$c_3,5*$BNSZ($a0)
mflo	$t_1
mfhi	$t_2
$ADDU	$c_1,$t_1
sltu	$at,$c_1,$t_1
$ADDU	$t_2,$at
$ADDU	$c_2,$t_2
$ST	$c_1,6*$BNSZ($a0)
$ST	$c_2,7*$BNSZ($a0)
.set	noreorder
___
$code.=<<___ if ($flavour =~ /nubi/i);
$REG_L	$t3,4*$SZREG($sp)
$REG_L	$t2,3*$SZREG($sp)
$REG_L	$t1,2*$SZREG($sp)
$REG_L	$t0,1*$SZREG($sp)
$REG_L	$gp,0*$SZREG($sp)
$PTR_ADD $sp,6*$SZREG
___
$code.=<<___;
jr	$ra
nop
.end	bn_sqr_comba4
___
print $code;
close STDOUT;
