open FOO, ">>file" or die;
truncate(FOO, 1234);
close FOO;
truncate("file", 567);
