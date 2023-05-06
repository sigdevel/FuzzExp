#!/usr/bin/perl -w
my @bytes = ();
my $base = 0;
my %opcodes = (
0x69 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'ADC'
},
0x65 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'ADC'
},
0x75 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'ADC'
},
0x6d => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'ADC'
},
0x7d => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'ADC'
},
0x79 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'ADC'
},
0x61 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'ADC'
},
0x71 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'ADC'
},
0x72 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'ADC'
},
0x29 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'AND'
},
0x25 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'AND'
},
0x35 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'AND'
},
0x2d => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'AND'
},
0x3d => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'AND'
},
0x39 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'AND'
},
0x21 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'AND'
},
0x31 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'AND'
},
0x32 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'AND'
},
0x0a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'ASL',
'operand' => 'A'
},
0x06 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'ASL'
},
0x16 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'ASL'
},
0x0e => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'ASL'
},
0x1e => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'ASL'
},
0x0f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR0'
},
0x1f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR1'
},
0x2f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR2'
},
0x3f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR3'
},
0x4f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR4'
},
0x5f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR5'
},
0x6f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR6'
},
0x7f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBR7'
},
0x8f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS0'
},
0x9f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS1'
},
0xaf => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS2'
},
0xbf => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS3'
},
0xcf => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS4'
},
0xdf => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS5'
},
0x3f => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS6'
},
0xff => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BBS7'
},
0x90 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BCC'
},
0xb0 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BCS'
},
0xf0 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BEQ'
},
0x89 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'BIT'
},
0x24 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'BIT'
},
0x34 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'BIT'
},
0x2c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'BIT'
},
0x3c => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'BIT'
},
0x30 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BMI'
},
0xd0 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BNE'
},
0x10 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BPL'
},
0x80 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BRA'
},
0x00 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'BRK'
},
0x50 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BVC'
},
0x70 => {
'modesub' => \&mode_Relative,
'mnemonic' => 'BVS'
},
0x18 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'CLC'
},
0xd8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'CLD'
},
0x58 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'CLI'
},
0xb8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'CLV'
},
0xc9 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'CMP'
},
0xc5 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'CMP'
},
0xd5 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'CMP'
},
0xcd => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'CMP'
},
0xdd => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'CMP'
},
0xd9 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'CMP'
},
0xc1 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'CMP'
},
0xd1 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'CMP'
},
0xd2 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'CMP'
},
0xe0 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'CPX'
},
0xe4 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'CPA'
},
0xec => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'CPX'
},
0xc0 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'CPY'
},
0xc4 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'CPY'
},
0xcc => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'CPY'
},
0x3a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'DEA'
},
0xc6 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'DEC'
},
0xd6 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'DEC'
},
0xce => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'DEC'
},
0xde => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'DEC'
},
0xca => {
'modesub' => \&mode_Implied,
'mnemonic' => 'DEX'
},
0x88 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'DEY'
},
0x49 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'EOR'
},
0x45 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'EOR'
},
0x55 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'EOR'
},
0x4d => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'EOR'
},
0x5d => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'EOR'
},
0x59 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'EOR'
},
0x41 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'EOR'
},
0x51 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'EOR'
},
0x52 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'EOR'
},
0x1a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'INA'
},
0xe6 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'INC'
},
0xf6 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'INC'
},
0xee => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'INC'
},
0xfe => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'INC'
},
0xe8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'INX'
},
0xc8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'INY'
},
0x4c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'JMP'
},
0x6c => {
'modesub' => \&mode_Indirect_Absolute,
'mnemonic' => 'JMP'
},
0x7c => {
'modesub' => \&mode_Indirect_Absolute_X,
'mnemonic' => 'JMP'
},
0x20 => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'JSR'
},
0xa9 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'LDA'
},
0xa5 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'LDA'
},
0xb5 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'LDA'
},
0xad => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'LDA'
},
0xbd => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'LDA'
},
0xb9 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'LDA'
},
0xa1 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'LDA'
},
0xb1 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'LDA'
},
0xb2 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'LDA'
},
0xa2 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'LDX'
},
0xa6 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'LDX'
},
0xb6 => {
'modesub' => \&mode_Zero_Page_Y,
'mnemonic' => 'LDX'
},
0xae => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'LDX'
},
0xbe => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'LDX'
},
0xa0 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'LDY'
},
0xa4 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'LDY'
},
0xb4 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'LDY'
},
0xac => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'LDY'
},
0xbc => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'LDY'
},
0x4a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'LSR',
'operand' => 'A'
},
0x46 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'LSR'
},
0x56 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'LSR'
},
0x4e => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'LSR'
},
0x5e => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'LSR'
},
0xea => {
'modesub' => \&mode_Implied,
'mnemonic' => 'NOP'
},
0x09 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'ORA'
},
0x05 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'ORA'
},
0x15 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'ORA'
},
0x0d => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'ORA'
},
0x1d => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'ORA'
},
0x19 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'ORA'
},
0x01 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'ORA'
},
0x11 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'ORA'
},
0x12 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'ORA'
},
0x48 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PHA'
},
0x08 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PHP'
},
0xda => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PHX'
},
0x5a => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PHY'
},
0x68 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PLA'
},
0x68 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PLP'
},
0xfa => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PLX'
},
0x7a => {
'modesub' => \&mode_Implied,
'mnemonic' => 'PLY'
},
0x2a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'ROL',
'operand' => 'A'
},
0x26 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'ROL'
},
0x36 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'ROL'
},
0x2e => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'ROL'
},
0x3e => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'ROL'
},
0x6a => {
'modesub' => \&mode_Accumulator,
'mnemonic' => 'ROR',
'operand' => 'A'
},
0x66 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'ROR'
},
0x76 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'ROR'
},
0x6e => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'ROR'
},
0x7e => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'ROR'
},
0x40 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'RTI'
},
0x60 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'RTS'
},
0xe9 => {
'modesub' => \&mode_Immediate,
'mnemonic' => 'SBC'
},
0xe5 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'SBC'
},
0xf5 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'SBC'
},
0xed => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'SBC'
},
0xfd => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'SBC'
},
0xf9 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'SBC'
},
0xe1 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'SBC'
},
0xf1 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'SBC'
},
0xf2 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'SBC'
},
0x38 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'SEC'
},
0xf8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'SED'
},
0x78 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'SEI'
},
0x85 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'STA'
},
0x95 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'STA'
},
0x8d => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'STA'
},
0x9d => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'STA'
},
0x99 => {
'modesub' => \&mode_Absolute_Y,
'mnemonic' => 'STA'
},
0x81 => {
'modesub' => \&mode_Indirect_Zero_Page_X,
'mnemonic' => 'STA'
},
0x91 => {
'modesub' => \&mode_Indirect_Zero_Page_Y,
'mnemonic' => 'STA'
},
0x92 => {
'modesub' => \&mode_Indirect_Zero_Page,
'mnemonic' => 'STA'
},
0x86 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'STX'
},
0x96 => {
'modesub' => \&mode_Zero_Page_Y,
'mnemonic' => 'STX'
},
0x8e => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'STX'
},
0x84 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'STY'
},
0x94 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'STY'
},
0x8c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'STY'
},
0x64 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'STZ'
},
0x74 => {
'modesub' => \&mode_Zero_Page_X,
'mnemonic' => 'STZ'
},
0x9c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'STZ'
},
0x9e => {
'modesub' => \&mode_Absolute_X,
'mnemonic' => 'STZ'
},
0xaa => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TAX'
},
0xa8 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TAY'
},
0x14 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'TRB'
},
0x1c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'TRB'
},
0x04 => {
'modesub' => \&mode_Zero_Page,
'mnemonic' => 'TSB'
},
0x0c => {
'modesub' => \&mode_Absolute,
'mnemonic' => 'TSB'
},
0xba => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TSX'
},
0x8a => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TXA'
},
0x9a => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TXS'
},
0x98 => {
'modesub' => \&mode_Implied,
'mnemonic' => 'TYA'
}
);
sub usage {
print "Usage:\n";
print "$0 [-i] [-x \$addr] [-a addr] <input file>\n";
print " -i : input mode (for feeding to an assembler\n";
print " -x : base address in hex\n";
print " -a : base address in decimal\n";
print " -h : this help message\n";
}
if (!defined $ARGV[0]) {
usage();
exit;
}
my $input_mode = 0;
while (defined $ARGV[0] && $ARGV[0] =~ /^-/) {
if ($ARGV[0] eq '-a' && defined $ARGV[1] && $ARGV[1] =~ /^\d+$/) {
$base = $ARGV[1];
shift;
shift;
} elsif ($ARGV[0] eq '-x' && defined $ARGV[1] && $ARGV[1] =~ /^[a-z0-9A-Z]+$/) {
$base = hex($ARGV[1]);
shift;
shift;
} elsif ($ARGV[0] eq '-i') {
$input_mode = 1;
shift;
} elsif ($ARGV[0] eq '-h') {
usage();
exit;
} else {
die "Invalid argument $ARGV[0]\n";
}
}
my $input_file = shift;
die "Must supply filename\n" unless defined $input_file && $input_file;
sub mode_Immediate {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s
} else {
print uc sprintf("%08x  %02x %02x      %3.3s
}
$_[0] += 2;
}
sub mode_Zero_Page {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s \$%02x\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Zero_Page_X {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x,X\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s \$%02x,X\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Zero_Page_Y {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x,Y\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s \$%02x,Y\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Absolute {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x%02x\n", $addr + $base, $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x %02x   %3.3s \$%02x%02x\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $bytes[$addr + 2], $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
}
$_[0] += 3;
}
sub mode_Indirect_Absolute {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s (\$%02x%02x)\n", $addr + $base, $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x %02x   %3.3s (\$%02x%02x)\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $bytes[$addr + 2], $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
}
$_[0] += 3;
}
sub mode_Indirect_Absolute_X {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s (\$%02x%02x,X)\n", $addr + $base, $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x %02x   %3.3s (\$%02x%02x,X)\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $bytes[$addr + 2], $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
}
$_[0] += 3;
}
sub mode_Absolute_X {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x%02x,X\n", $addr + $base, $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x %02x   %3.3s \$%02x%02x,X\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $bytes[$addr + 2], $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
}
$_[0] += 3;
}
sub mode_Absolute_Y {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%02x%02x,Y\n", $addr + $base, $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x %02x   %3.3s \$%02x%02x,Y\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $bytes[$addr + 2], $instr, $bytes[$addr + 2], $bytes[$addr + 1]);
}
$_[0] += 3;
}
sub mode_Indirect_Zero_Page_X {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s (\$%02x,X)\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s (\$%02x,X)\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Indirect_Zero_Page_Y {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s (\$%02x),Y\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s (\$%02x),Y\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Indirect_Zero_Page {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s (\$%02x)\n", $addr + $base, $instr, $bytes[$addr + 1]);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s (\$%02x)\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $bytes[$addr + 1]);
}
$_[0] += 2;
}
sub mode_Relative {
my ($addr, $instr) = @_;
my $rel = ($addr + $base) - (254 - $bytes[$addr + 1]);
if ($bytes[$addr + 1] < 127) {
$rel += 256;
}
if ($input_mode) {
print uc sprintf("%04x:    %3.3s \$%04x\n", $addr + $base, $instr, $rel);
} else {
print uc sprintf("%08x  %02x %02x      %3.3s \$%04x\n", $addr + $base, $bytes[$addr], $bytes[$addr + 1], $instr, $rel);
}
$_[0] += 2;
}
sub mode_Implied {
my ($addr, $instr) = @_;
if ($input_mode) {
print uc sprintf("%04x:    %3.3s\n", $addr + $base, $instr);
} else {
print uc sprintf("%08x  %02x         %3.3s\n", $addr + $base, $bytes[$addr], $instr);
}
$_[0]++;
}
sub mode_Accumulator {
my ($addr, $instr, $operand) = @_;
if ($input_mode) {
if (defined $operand) {
print uc sprintf("%04x:    %3.3s %s\n", $addr + $base, $instr, $operand);
} else {
print uc sprintf("%04x:    %3.3s\n", $addr + $base, $instr);
}
} else {
if (defined $operand) {
print uc sprintf("%08x  %02x         %3.3s %s\n", $addr + $base, $bytes[$addr], $instr, $operand);
} else {
print uc sprintf("%08x  %02x         %3.3s\n", $addr + $base, $bytes[$addr], $instr);
}
}
$_[0]++;
}
my $expected = -s $input_file;
my $fh;
my $buffer = '';
if (open($fh, "<$input_file")) {
binmode $fh;
my $size = read($fh, $buffer, $expected);
if ($size != $expected) {
print "Error reading $input_file, got $size, expected $expected\n";
}
close $fh;
@bytes = unpack "C$size", $buffer;
my $addr = 0;
while ($addr < $size) {
if (defined $opcodes{$bytes[$addr]}{'modesub'}) {
my $func = $opcodes{$bytes[$addr]}{'modesub'};
$func->($addr, $opcodes{$bytes[$addr]}{'mnemonic'}, $opcodes{$bytes[$addr]}{'operand'});
} else {
mode_Implied($addr, '???');
}
}
} else {
die "Can't open $input_file\n";
}
1;
