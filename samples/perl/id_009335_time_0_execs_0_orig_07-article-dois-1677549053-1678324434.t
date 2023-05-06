#!perl
BEGIN {
binmode STDOUT, ':encoding(utf8)';
binmode STDERR, ':encoding(utf8)';
}
use Test::More;
use Gcis::Client;
use strict;
my $c = Gcis::Client->new->use_env;
my $d = Gcis::Client->new->accept("application/vnd.citationstyles.csl+json;q=0.5")
->url("http://dx.doi.org");
my $r = Gcis::Client->new->accept("application/json;q=0.5")
->url("http://api.crossref.org");
my $param="?all=1";
my $articles = $c->get("/article$param");
ok scalar @$articles, "got some articles";
note "count : ".@$articles;
for my $article (@$articles) {
my $doi = $article->{doi};
my $uri = $article->{uri};
my $href = $article->{href};
$href =~ s/.json$//;
ok $doi, "got a doi";
my $crossref = $d->get("/$doi");
ok keys %$crossref, "Valid doi : http://dx.doi.org/$doi";
SKIP: {
skip "Missing crossref data for $doi", 1 unless keys %$crossref;
is $article->{title}, $crossref->{title}, "title for $href" or diag "got http://dx.doi.org/$doi for $href";
my $year = $crossref->{issued}{'date-parts'}[0][0];
if ($article->{year} == ($year + 1)) {
ok $article->{year}, "year off by one for $href";
} else {
is $article->{year}, $year, "year for $href";
}
is $article->{journal_vol}, $crossref->{volume}, "volume for $href";
my $journal = $c->get("/journal/$article->{journal_identifier}");
my $issn = $crossref->{ISSN}[0];
my $crossref_journal = $r->get("/journals/issn:$issn");
is $journal->{title}, $crossref_journal->{message}{title}, "journal title for $href";
}
}
done_testing();
