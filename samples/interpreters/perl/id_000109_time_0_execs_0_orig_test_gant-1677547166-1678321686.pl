#!/usr/bin/perl -I../Iolib -I../ConfLib -w
use strict;
use Data::Dumper;
use OAR::IO;
use OAR::Schedulers::OarResourceTree;
use OAR::Schedulers::GanttHoleStorage;
my $max = 30;
my $gantt = OAR::Schedulers::GanttHoleStorage::new($max);
my $vec = '';
vec($vec, 3, 1) = 1;
OAR::Schedulers::GanttHoleStorage::add_new_resources($gantt, $vec);
$vec = '';
vec($vec, 2, 1) = 1;
vec($vec, 1, 1) = 1;
OAR::Schedulers::GanttHoleStorage::add_new_resources($gantt, $vec);
my $base = OAR::IO::connect();
$vec = '';
$vec = '';
vec($vec, 3, 1) = 1;
OAR::Schedulers::GanttHoleStorage::set_occupation($gantt, 5, 5, $vec);
vec($vec, 2, 1) = 1;
OAR::Schedulers::GanttHoleStorage::set_occupation($gantt, 8, 5, $vec);
$vec = '';
vec($vec, 1, 1) = 1;
OAR::Schedulers::GanttHoleStorage::set_occupation($gantt, 5, 10, $vec);
OAR::Schedulers::GanttHoleStorage::pretty_print($gantt);
$vec = '';
vec($vec, 2, 1) = 1;
vec($vec, 1, 1) = 1;
print(OAR::Schedulers::GanttHoleStorage::is_resources_free($gantt, 2, 2, $vec) . "\n");
exit;
print("INIT\n");
my $resGroup = OAR::IO::get_resources_data_structure_job($base, 2);
print(Dumper($resGroup));
my $h1 =
OAR::IO::get_possible_wanted_resources($base, [], [], "", $resGroup->[0]->[0]->[0]->{resources});
print(Dumper($h1));
my @a = Gantt::find_first_hole($gantt, 3, 30, [$h1]);
print(Dumper(@a));
print("TO_OT\n");
foreach my $t (@{ $a[1] }) {
print(Dumper(OAR::Schedulers::ResourceTree::delete_unnecessary_subtrees($t)));
}
