package
Devel::NYTProf::Test;
require Devel::NYTProf::Core;
require Exporter;
our @ISA = qw(Exporter);
our @EXPORT_OK = qw(example_sub example_xsub example_xsub_eval);
sub example_sub { }
1;
