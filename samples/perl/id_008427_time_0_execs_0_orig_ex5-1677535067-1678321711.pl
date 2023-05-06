#!/usr/bin/perl -w    
print "Type a word any word: ";
$str = <STDIN>;
print "Type a number so you can see your word multiplyyyyyy ";
chomp($num = <STDIN>);
$result = $str x $num;
print "herp de derp:\n$result";
