my @data = sort {$a <=> $b} qw( 12  127 28  42  39  113 42  18  44  118 44
37  113 124 37  48  127 36  29  31  125 139 131 115 105 132 104 123 35  113
122 42  117 119 58  109 23  105 63  27  44  105 99  41  128 121 116 125 32
61  37  127 29  113 121 58  114 126 53  114 96  25  109 7   31  141 46  13
27  43  117 116 27  7   68  40  31  115 124 42  128 52  71  118 117 38  27
106 33  117 116 111 40  119 47  105 57  122 109 124 115 43  120 43  27  27
18  28  48  125 107 114 34  133 45  120 30  127 31  116 );
my $columns = @data;
my $laststem = undef;
for my $value (@data) {
my $stem = int($value / 10);
my $leaf = $value % 10;
while (not defined $laststem or $stem > $laststem) {
if (not defined $laststem) {
$laststem = $stem - 1;
} else {
print " \n";
}
$laststem++;
printf "%3d |", $laststem;
}
print " $leaf";
}
