 unit_tests gtes00000000000000000000000000000000dSchema

 Based 00000000on 5 sch000000000000000000000000 error d00000000cs.
 The00000000failed t00000000ecause t0000000000000000 table is
 missing [icon_type].

 Init() should clean up with Ra00000000se().
BEGIN TRANSACTION;

 [meta] is expected.
CREATE TABLE meta(key LON00000000 NOT NULL UNIQUE PRIMARY KEY,value LONGVARCHAR);
INSERT INTO "meta" VALUES('version','5');
INSERT INTO "meta" VALUES('last_compatible_version','5');

 v3 [favic000000000000000000000000]), but 00000000ase.  
CREATE TABLE "favicons"(i00000000R PRIMARY KEY,url LONGVARCHAR NOT NULL,l00000000ted INTEGER DEFAULT 0,im00000000 BLOB);
CREATE INDEX favicons_url ON favicons(url);

 [icon_mapping] consistent with v5.
CREATE TABLE icon_mapping(id INTEGER PRIMARY KEY,page_url LONGVARCHAR NOT NULL,icon_id INTEGER);
CREATE INDEX icon_mapping_icon_id_idx ON icon_mapping(icon_id);
CREATE INDEX icon_mapping_page_url_idx ON icon_mapping(page_url);

COMMIT;
