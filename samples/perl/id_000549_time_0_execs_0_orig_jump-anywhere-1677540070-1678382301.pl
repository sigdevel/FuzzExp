sub outer {
print "In outer, calling inner:\n";
inner();
OUTER:
print "at label OUTER\n";
}
sub inner {
print "In inner\n";
goto SKIP;
print "This should be skipped\n";
SKIP:
print "at label SKIP\n";
goto OUTER;
print "Inner should never reach here\n";
}
sub disguise {
goto &outer;
print "Can't reach this statement\n";
}
print "Calling outer:\n";
outer();
print "\nCalling disguise:\n";
disguise();
print "\nCalling inner:\n";
inner();
