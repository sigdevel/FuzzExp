print "\e[?25l";
print "Enter anything, press RETURN: ";
$input = <>;
print "\e[0H\e[0J\e[?25h";
