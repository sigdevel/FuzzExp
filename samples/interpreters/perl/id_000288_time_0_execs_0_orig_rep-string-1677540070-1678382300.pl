foreach (qw(1001110011 1110111011 0010010010 1010101010 1111111111 0100101101 0100100 101 11 00 1)) {
print "$_\n";
if (/^(.+)\1+(.*$)(?(?{ substr($1, 0, length $2) eq $2 })|(?!))/) {
print ' ' x length $1, "$1\n\n";
} else {
print " (no repeat)\n\n";
}
}
