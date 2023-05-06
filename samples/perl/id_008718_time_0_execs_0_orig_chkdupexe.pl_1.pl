$execdirs='/bin /sbin /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin '.
'/usr/X11/bin /usr/bin/X11 /usr/local/X11/bin '.
'/usr/TeX/bin /usr/tex/bin /usr/games '.
'/usr/local/games';
$|=1;
$ENOENT=2;
%didthis=();
foreach $dir (split(/\s+/, "$execdirs"), "\0", split(/:/, $ENV{PATH})) {
if ($dir eq "\0") { $checkingpath = 1; next; }
($device,$inode)=stat($dir);
if (!defined($device)) {
($dum)=lstat($dir);
next if $! == $ENOENT;
if (!$dum) {
print "Dangling symlink: $dir\n";
next;
}
warn "Nonexistent directory: $dir\n" if ($checkingpath);
next;
}
if (!-d _) {
print "Not a directory: $dir\n";
next;
}
next if defined($didthis{$device,$inode});
$didthis{$device,$inode}=1;
chdir($dir) || die "Could not chdir $dir: $!\n";
opendir(DIR,".") ||
die "NUTS! Personaly I think your perl or filesystem is broken.\n".
"I've done all sorts of checks on $dir, and now I can't open it!\n";
foreach $_ (readdir(DIR)) {
lstat($_);
if (-l _) {
($dum)=stat($_);
print "Dangling symlink: $dir/$_\n" unless defined($dum);
next;
}
if (defined($count{$_})) {
$progs{$_}.=" $dir/$_";
$count{$_}++;
} else {
$progs{$_}="$dir/$_";
$count{$_}=1;
}
}
closedir(DIR);
}
open(LS,"| xargs -r ls -ldU");
while (($prog,$paths)=each %progs) {
print LS "$paths\n" if ($count{$prog}>1);
}
close(LS);
exit 0;
@unchecked=();
foreach $dir (split(/:/,$ENV{'PATH'})) {
($device,$inode)=stat($dir);
next unless defined($device);
next if defined($didthis{$device,$inode});
push(@unchecked,$dir);
$didthis{$device,$inode}=1;
}
print "Warning: Your path contains these directories which chkdupexe has not checked:\n",join(',',@unchecked),
".\nPlease review the execdirs list in chkdupexe.\n"
