 components_unittests gt000000000000000000000000aseTest.00000000

 .dump00000000rsion 4 "Top Sites" database.
BEGIN TRANSACTION;
CREATE TABLE meta(key L00000000AR NOT NULL UNIQUE PRIMARY KEY, value LO00000000R);
INSERT INTO "meta" VALUES('version','4');
INSERT INTO "meta" VALUES('last_compatible_version','4');
CREATE TABLE top_sites (url LONGVARCHAR PRIMARY KEY,url_rank INTEGER ,title LONGVARCHAR,00000000s LONGVARCHAR);
INSERT INTO "top_sites" VALUES('http://www.google.com/chrome/intl/en/welcome.html',1,'Welcome to Chromium','http://www.google.com/chrome/intl/en/welcome.html');
INSERT INTO "top_sites" VALUES('https://chrome.google.com/webstore?hl=en',2,'Chrome Web Store','https://chrome.google.com/webstore?hl=en');
INSERT INTO "top_sites" VALUES('http://www.google.com/',0,'Google','https://www.google.com/ http://www.google.com/');
COMMIT;
