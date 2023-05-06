#!/usr/bin/perl
require 'globalvariables.pl';
require 'logfile_helper.pl';
$datestr2 = &GetTimeStamp;
$addr = $ENV{'REMOTE_ADDR'};
$host = $ENV{'REMOTE_HOST'};
read(STDIN, $stdin, $ENV{'CONTENT_LENGTH'});
$stdin =~ s/\n//g;
$stdin =~ tr/\t//d;
$stdin =~ tr/\r//d;
($fname,$junk) = split("</filename>",$stdin);
($junk,$fname) = split("<filename>",$fname);
if (index($fname, ".") != -1) {
$fname = substr($fname,0,length($fname)-4);
}
$fname =~ tr/\-0-9A-Z_a-z//cd;
($folder,$junk) = split("</folder>",$stdin);
($junk,$folder) = split("<folder>",$folder);
$folder =~ tr/\-0-9A-Z_a-z\///cd;
($global_count,$username,$edited,$old_name,$new_name,$modifiedControlPoints, $video_mode) = &GetPrivateData($stdin);
($left_side,$stdin) = split("<private>",$stdin);
($junk,$stdin) = split("</private>",$stdin);
$stdin = "$left_side$stdin";
$path = $LM_HOME . "Annotations";
$tmpPath = $LM_HOME . "annotationCache/TmpAnnotations";
if ($video_mode){
$path = $LM_HOME . "VLMAnnotations";
}
$stdin =~ s/<date\/>/<date>$datestr2<\/date>/g;
if(!&IsSubmittedXmlOk($stdin)) {
open(FP,">>$LM_HOME/annotationCache/Logs/logfile.txt");
print FP "\n$datestr2 $folder $fname $addr *XML_ERROR $username";
close(FP);
print "Content-type: text/xml\n\n" ;
print "There was a problem saving the submitted XML to the LabelMe server.  Please try again.  If this problem persists, please contact the Labelme developers." ;
return;
}
open(FP,"$path/$folder/$fname.xml");
@before_lines = readline(FP);
$tot_before = 0;
$tot_del_before = 0;
foreach $i (@before_lines) {
@poly_split = split("<object>",$i);
$tot_before = $tot_before + scalar(@poly_split)-1;
@del_split = split("<deleted>1</deleted>",$i);
$tot_del_before = $tot_del_before + scalar(@del_split)-1;
}
close(FP);
@poly_split = split("<object>",$stdin);
$tot_after = scalar(@poly_split)-1;
@del_split = split("<deleted>1</deleted>",$stdin);
$tot_del_after = scalar(@del_split)-1;
($stdin) = &InsertImageSize($stdin,$folder,$fname);
@all_folders = split("/",$folder);
$accum_path = "";
foreach $i (@all_folders) {
unless(-d "$tmpPath/$accum_path$i") {
mkdir "$tmpPath/$accum_path$i" or die;
}
unless(-d "$path/$accum_path$i") {
mkdir "$path/$accum_path$i" or die;
}
$accum_path = "$accum_path$i/";
}
open(FP,">$tmpPath/$folder/$fname.xml");
print FP $stdin;
close(FP);
system("cp $tmpPath/$folder/$fname.xml $path/$folder/$fname.xml");
if($edited) {
$objname = "$old_name->$new_name";
}
else {
$objname = $old_name;
}
$objname =~ s/\s/_/g;
$username =~ s/\s/_/g;
&WriteLogfile($datestr2,$folder,$fname,$tot_before,$tot_after,$addr,$host,$objname,$global_count,$username,$modifiedControlPoints,$tot_del_before,$tot_del_after);
print "Content-type: text/xml\n\n" ;
print $stdin;
print $fname;
