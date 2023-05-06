#!/usr/bin/perl
local %filter = (
"Russell Klophaus" => 1,
"rklophaus" => 1,
"dkpsystem" => 1,
"Sidello Website" => 1,
"Bracketpal User" => 1,
"root" => 1,
"unknown" => 1
);
local $pwd = `pwd`;
chomp($pwd);
local $git_cmd = "git log --shortstat --date=short | sed '/^commit/d' | sed '/^ /d' | sed '/^\$/d'";
local %authors = {};
&do_repo("");
&do_repo("nitrogen_core");
&do_repo("simple_bridge");
&do_repo("nprocreg");
&do_repo("simple_cache");
&do_repo("rekt");
&do_repo("NitrogenProject.com");
foreach $author (sort compare_date (keys(%authors))) {
print "$author\n" if not exists($filter{$author});
}
sub compare_date {
$authors{$a} cmp $authors{$b}
}
sub do_repo {
my ($repo) = @_;
chdir "$pwd/$repo";
my @lines = `$git_cmd`;
my $author = "";
for(@lines) {
if(/^Author:\s*(.*?)\s<.*>$/) {
$author = $1;
}
elsif(/^Date:\s*(.*)$/) {
my $date = $1;
if(not exists($authors{$author}) or $date lt $authors{$author}) {
$authors{$author} = $date;
}
}
}
}
