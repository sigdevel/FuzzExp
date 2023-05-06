#! /usr/local/bin/perl
sub main {
local (@HOPE_CMD) = split (/\s/, ($ENV{"HOPE_CMD"} || "hope"));
local ($DEFAULT_PAT) = '/^DOC/';
local ($COMPOUND_PAT);
$|=1;
if (! @ARGV) { unshift (@ARGV, "$DEFAULT_PAT"); }
while (@ARGV) {
$COMPOUND_PAT = shift (@ARGV);
system (@HOPE_CMD, "sync", "-compound", "$COMPOUND_PAT");
}
}
&main;
