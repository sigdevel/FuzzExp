package Text::Soundex;
require 5.000;
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(&soundex $soundex_nocode);
$soundex_nocode = undef;
sub soundex
{
local (@s, $f, $fc, $_) = @_;
push @s, '' unless @s;
foreach (@s)
{
$_ = uc $_;
tr/A-Z//cd;
if ($_ eq '')
{
$_ = $soundex_nocode;
}
else
{
($f) = /^(.)/;
tr/AEHIOUWYBFPVCGJKQSXZDTLMNR/00000000111122222222334556/;
($fc) = /^(.)/;
s/^$fc+//;
tr///cs;
tr/0//d;
$_ = $f . $_ . '000';
s/^(.{4}).*/$1/;
}
}
wantarray ? @s : shift @s;
}
1;
__END__
=head1 NAME
Text::Soundex - Implementation of the Soundex Algorithm as Described by Knuth
=head1 SYNOPSIS
use Text::Soundex;
$code = soundex $string;
@codes = soundex @list;
$soundex_nocode = 'Z000';
=head1 DESCRIPTION
This module implements the soundex algorithm as described by Donald Knuth
in Volume 3 of B<The Art of Computer Programming>.  The algorithm is
intended to hash words (in particular surnames) into a small space using a
simple model which approximates the sound of the word when spoken by an English
speaker.  Each word is reduced to a four character string, the first
character being an upper case letter and the remaining three being digits.
If there is no soundex code representation for a string then the value of
C<$soundex_nocode> is returned.  This is initially set to C<undef>, but
many people seem to prefer an I<unlikely> value like C<Z000>
(how unlikely this is depends on the data set being dealt with.)  Any value
can be assigned to C<$soundex_nocode>.
In scalar context C<soundex> returns the soundex code of its first
argument, and in array context a list is returned in which each element is the
soundex code for the corresponding argument passed to C<soundex> e.g.
@codes = soundex qw(Mike Stok);
leaves C<@codes> containing C<('M200', 'S320')>.
=head1 EXAMPLES
Knuth's examples of various names and the soundex codes they map to
are listed below:
Euler, Ellery -> E460
Gauss, Ghosh -> G200
Hilbert, Heilbronn -> H416
Knuth, Kant -> K530
Lloyd, Ladd -> L300
Lukasiewicz, Lissajous -> L222
so:
$code = soundex 'Knuth';
@list = soundex qw(Lloyd Gauss);
=head1 LIMITATIONS
As the soundex algorithm was originally used a B<long> time ago in the US
it considers only the English alphabet and pronunciation.
As it is mapping a large space (arbitrary length strings) onto a small
space (single letter plus 3 digits) no inference can be made about the
similarity of two strings which end up with the same soundex code.  For
example, both C<Hilbert> and C<Heilbronn> end up with a soundex code
of C<H416>.
=head1 AUTHOR
This code was implemented by Mike Stok (C<stok@cybercom.net>) from the
description given by Knuth.  Ian Phillips (C<ian@pipex.net>) and Rich Pinder
(C<rpinder@hsc.usc.edu>) supplied ideas and spotted mistakes.
