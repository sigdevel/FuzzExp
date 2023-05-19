 phpMyAdmin SQL Dump
 version 2.8.0.1
 http://www.phpmyadmin.net
 
 Host: custsql-ipw06.eigbox.net
 Generation Time: Sep 25, 2010 at 12:38 AM
 Server version: 5.0.83
 PHP Version: 4.4.9
 
 Database: `justin`
 

 

 
 Table structure for table `announcements`
 

USE justin;
CREATE TABLE `announcements` (
  `id` int(10) NOT NULL auto_increment,
  `date` datetime NOT NULL,
  `by` varchar(50) NOT NULL,
  `text` varchar(500) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

 
 Dumping data for table `announcements`
 

INSERT INTO `announcements` VALUES (1, '2010-08-21 14:08:32', 'justinjmc80@gmail.com', 'I''m testing the announcement system by directly inserting this announcement into the database, sans web interface.');

 

 
 Table structure for table `users`
 

CREATE TABLE `users` (
  `index` int(5) NOT NULL,
  `name` varchar(100) NOT NULL,
  `googleAccount` varchar(100) NOT NULL,
  `identifier` varchar(1000) NOT NULL,
  PRIMARY KEY  (`index`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

 
 Dumping data for table `users`
 

INSERT INTO `users` VALUES (0, 'Justin', 'justinjmc80', 'https://www.google.com/accounts/o8/id?id=AItOawlOLRPHEa2AuH4brBPvwx2Z8FSIolw1v9Q');
INSERT INTO `users` VALUES (1, 'Kevin', 'kdargatz', '');
INSERT INTO `users` VALUES (2, 'Dipika', 'dipika.mouli', 'https://www.google.com/accounts/o8/id?id=AItOawl1_AASoKO7DDjDiA7Bg0vSmAMUHGTamD8');
INSERT INTO `users` VALUES (3, 'mnacy', 'melissa.nacy', '');
INSERT INTO `users` VALUES (13, 'Amelia', 'amelia.ruslim', '');
INSERT INTO `users` VALUES (12, 'Sandra', 'fadel.sandra', '');
INSERT INTO `users` VALUES (11, 'Nieri', 'nessinarian', '');
INSERT INTO `users` VALUES (10, 'Kim', 'kimberly623', '');
INSERT INTO `users` VALUES (9, 'ER Daddy', 'ashwinch', 'https://www.google.com/accounts/o8/id?id=AItOawl6I45F0Xm9GpKR1N0pXVqvlUp7-6_sygU');
INSERT INTO `users` VALUES (8, 'Sonali', 'sonalirs14', '');
INSERT INTO `users` VALUES (7, 'Mary', 'mcgilvraym', 'https://www.google.com/accounts/o8/id?id=AItOawkAn2uAFmVIni9vClcwEjhSN1rClEXFwLU');
INSERT INTO `users` VALUES (6, 'Lilian', 'tse.lilian', '');
INSERT INTO `users` VALUES (5, 'Arthur', 'huertaarth', '');
INSERT INTO `users` VALUES (4, 'Ben Li', 'liben426', '');
INSERT INTO `users` VALUES (14, 'Danielle', 'dstaubman', '');
INSERT INTO `users` VALUES (15, 'Ellie', 'elijwang', '');
INSERT INTO `users` VALUES (16, 'Jess', 'jessica.s.bloch', '');
INSERT INTO `users` VALUES (17, 'Lindy', 'xcookiecrumbs', '');
INSERT INTO `users` VALUES (18, 'Mike', 'michaellacivita', '');
INSERT INTO `users` VALUES (19, 'Rick', 'patrick.vdp', '');
INSERT INTO `users` VALUES (20, 'Grayson', 'grayson.d.smith', '');
INSERT INTO `users` VALUES (21, 'Marco', 'marcoyfz312', '');
INSERT INTO `users` VALUES (22, 'Marissa', 'mgawel917', '');
INSERT INTO `users` VALUES (23, 'pchoi', 'choi.pyy', '');
INSERT INTO `users` VALUES (24, 'Allan aka Yixiao', 'allanyxz', '');
INSERT INTO `users` VALUES (25, 'Cristabel', 'cristabelchoong', '');
INSERT INTO `users` VALUES (26, 'Robo', 'robo24wolverine', '');
INSERT INTO `users` VALUES (27, 'Liting', 'liting.chen89', '');
INSERT INTO `users` VALUES (28, 'Stephanie', 'stephanie.chang6', '');

 

 
 Table structure for table `yearbookComments`
 

CREATE TABLE `yearbookComments` (
  `index` varchar(10) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `name` varchar(100) NOT NULL,
  `comment` mediumtext NOT NULL,
  PRIMARY KEY  (`index`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

 
 Dumping data for table `yearbookComments`
 

INSERT INTO `yearbookComments` VALUES ('10', 'http://www.aiesecmichigan.com/yearbook/eventIvogue.php', 'grayson', 'i like this.  also glad to see the infamous cigar made it in.');
INSERT INTO `yearbookComments` VALUES ('11', 'http://www.aiesecmichigan.com/yearbook/fl.php', 'BAMF', 'i feel like a traitor, but have i mentioned that this is my favorite team of all time? They''re so baller they don''t need a description! ');
INSERT INTO `yearbookComments` VALUES ('9', 'http://www.aiesecmichigan.com/yearbook/eventMisc.php', 'steph', 'awwwwww we should have taken more pictures at OSS and GMMs!');
INSERT INTO `yearbookComments` VALUES ('8', 'http://www.aiesecmichigan.com/yearbook/eventRoksF.php', 'Justin', 'Also, I''m really happy someone managed to get a picture of Grayson''s lapdance.');
INSERT INTO `yearbookComments` VALUES ('7', 'http://www.aiesecmichigan.com/yearbook/eventRoksF.php', 'Justin', 'I never noticed that, the video is twice as entertaining if you just watch Dante the whole time haha.  I think he missed our rehearsal at GMM, yet he still wound up in the front row.');
INSERT INTO `yearbookComments` VALUES ('6', 'http://www.aiesecmichigan.com/yearbook/eventChristmas.php', 'Justin', 'The one at the top with Patrick as a reindeer with Dipika is my favorite picture ever');
INSERT INTO `yearbookComments` VALUES ('5', 'http://www.aiesecmichigan.com/yearbook/index.php', 'Lanes', 'Awesome yearbook :) Congrats again to Dipik becoming the Prez this year!! You will rock it, girl... And BLee, keep stuntin coz your muscle shirts are the only reason I came to GMM. Ha!!!');
INSERT INTO `yearbookComments` VALUES ('4', 'http://www.aiesecmichigan.com/yearbook/eventRoksF.php', 'Robo', 'The key is Dante on the video, lol.  Priceless!');
INSERT INTO `yearbookComments` VALUES ('2', 'http://www.aiesecmichigan.com/yearbook/er.php', 'Justin', 'I felt like the first part of that comment was too weak so I had to toughen it up at the end.');
INSERT INTO `yearbookComments` VALUES ('3', 'http://www.aiesecmichigan.com/yearbook/eventMisc.php', 'Robo', 'Does miscellaneous mean "Parties"?  haha');
INSERT INTO `yearbookComments` VALUES ('1', 'http://www.aiesecmichigan.com/yearbook/er.php', 'Justin', 'Best team ever, I miss you guys!  PS get ready to work like crazy next year now that I''m in charge, punks.');
INSERT INTO `yearbookComments` VALUES ('0', 'http://www.aiesecmichigan.com/yearbook/index.php', 'Justin', 'Thank you to Ashwin, Micaela, and all of ER for helping to make this yearbook happen.  And thanks to everybody in AIESEC Michigan for the year!  The yearbook couldn''t hope to capture half the awesomeness.');

