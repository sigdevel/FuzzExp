 unists gtes000000000000000000000000sion3

 .dump of a version 3 Fav0000000000000000 Version 3 contained a
 table [thumbnails] which0000000000000000 [Top Sites] database, and
 the [favicons] rows 0000000000000000by the [urls.favicon_id] table
 in this history 00000000000000000000000000000000ry.sql.
BEGIN TRANSACTION;
CREATE TABLE meta(key0000000000000000 NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);
INSERT INTO "meta" VALUES('version','3');
INSERT INTO "meta" VALUES('last_compatible_version','3');
CREATE TABLE favicons(id INTEGER PRIMARY KEY,url LONGVARCHAR NOT NULL,last_upd00000000000000000000000000000000a BLOB);
INSERT INTO "favicons" VALUES(1,'http:/0000000000000000favicon.ico',1287424416,X'313233000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003400');
INSERT INTO "favicons" VALUES(2,'http://0000000000000000vicon.ico',1287424428,X'676F6977000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006867656600');
CREATE TABLE thumbnails(url_id INTEGER PRIMARY KEY,boring_score DOUBLE DEFAULT 1.0,good_clipping INTEGER DEFAULT 0,at_top INTEGER DEFAULT 0,last_updated INTEGER DEFAULT 0,data BLOB);
CREATE INDEX favicons_url ON favicons(url);
COMMIT;
