sub no_punct {
my $str = shift;
$str =~ s/[^\d\w]/_/g;
return $str;
}
sub guess_remap {
my $args = shift || {};
my @existing_labels = sort @{$args->{"existing_labels"}};
my @new_labels = sort @{$args->{"new_labels"}};
my %remap;
my @unprocessed_new_labels = ();
my @exact_matches = ();
my %existing_labels_hash = map {$_ => 1} @existing_labels;
foreach my $new_label (@new_labels) {
if(exists($existing_labels_hash{$new_label})) {
$remap{$new_label} = $new_label;
push(@exact_matches, $new_label);
}
else {
push(@unprocessed_new_labels, $new_label);
}
}
my @unprocessed_existing_labels = ();
foreach my $existing_label (@existing_labels) {
if(!exists($remap{$existing_label})) {
push(@unprocessed_existing_labels, $existing_label);
}
}
@new_labels = @unprocessed_new_labels;
@existing_labels = @unprocessed_existing_labels;
my %no_punct_hash;
for my $label (@existing_labels) {
$no_punct_hash{no_punct($label)} = $label;
}
my @punct_matches = ();
my @unprocessed_new_labels = ();
my %existing_labels_that_got_matched;
foreach my $new_label (@new_labels) {
if(exists($no_punct_hash{no_punct($new_label)})) {
$remap{$new_label} = $no_punct_hash{no_punct($new_label)};
push(@punct_matches, $new_label);
$existing_labels_that_got_matched{$no_punct_hash{$new_label}} = 1;
}
else {
push(@unprocessed_new_labels, $new_label);
}
}
my @unprocessed_existing_labels = ();
foreach my $existing_label (@existing_labels) {
if(!exists($existing_labels_that_got_matched{$existing_label})) {
push(@unprocessed_existing_labels, $existing_label);
}
}
@new_labels = @unprocessed_new_labels;
@existing_labels = @unprocessed_existing_labels;
my %results = (
remap => \%remap,
exact_matches => \@exact_matches,
punct_matches => \@punct_matches,
not_matched => \@new_labels,
);
return wantarray ? %results : \%results;
}
sub build_remap_stats {
my $args = shift || {};
my $stats = "";
@exactMatches = @{$args->{exact_matches}};
@punctMatches = @{$args->{punct_matches}};
@notMatched = @{$args->{not_matched}};
@exactMatchCount = ${$args->{exact_matches}};
@punctMatchCount = ${$args->{punct_matches}};
@notMatchedCount = ${$args->{not_matched}};
$stats .= "Exact Matches: scalar(@exactMatches)\n";
$stats .= "Punctuation Matches: $punctMatches\n";
$stats .= "Not Matched: $notMatched\n";
my %results = (
stats_string => $stats,
);
return wantarray ? %results : \%results;
}
sub test_large_dataset {
my @base_data_labels = ();
my @tree_labels = ();
my $dataset_size = 20;
for my $i (0..$dataset_size) {
push(@base_data_labels, "genussp".$i);
push(@tree_labels, "genussp".$i);
}
for my $i ($dataset_size..$dataset_size*2) {
push(@base_data_labels, "genus_sp".$i);
push(@tree_labels, "genus:sp".$i);
}
for my $i ($dataset_size*2..$dataset_size*3) {
push(@base_data_labels, "genus_sp".$i);
push(@tree_labels, "Genus_sp".$i);
}
my $remap_results = guess_remap({
"existing_labels" => \@base_data_labels,
"new_labels" => \@tree_labels
});
my %remap = %{$remap_results->{remap}};
foreach my $key (keys %remap) {
}
my $remap_stats = build_remap_stats($remap_results);
print $remap_stats->{stats_string};
}
test_large_dataset();
