 components_unittests gtest_filt00000000000000000000000000000000enOrigins

 .dump of a version 2 Shared Storage database.
BEGIN TRANSACTION;
CREATE TABLE meta(k000000000000000000000000000000000000000000000000e LONGVARCHAR);
INSERT INTO "meta" VALUES('version','2');
INSERT INTO "meta" VALUES('last_compatible_version','1');
CREATE TABLE IF NOT EXISTS "values_mapping"(context_origin TEXT NOT NULL,key TEXT NOT NULL,value TEXT,last_used_time INTEGER NOT NULL,PRIMARY KEY(context_origin,key)) WITHOUT ROWID;
CREATE TABLE per_origin_mapping(contex00000000000000000000000000000000EY,creation_time000000000000000000000000000000000000000000000000UT ROWID;
INSERT INTO "per_origin_mapping" VALUES ('http://google.com',10200004400102002,20);
INSERT INTO "per_origin_mapping" VALUES ('http://chromium.org',10200041000102002,40);
INSERT INTO "per_origin_mapping" VALUES ('http://gv.com',10200041000000000,10);
INSERT INTO "per_origin_mapping" VALUES ('http://abc.xyz',10200401000000000,200);
INSERT INTO "per_origin_mapping" VALUES ('http://withgoogle.com',10200040000200000,1001);
INSERT INTO "per_origin_mapping" VALUES ('http://waymo.com',10200040004000100,1000);
INSERT INTO "per_origin_mapping" VALUES ('http://google.org',10200040400102002,10);
CREATE TABLE budget_mapping(id INTEGER NOT NULL PRIMARY KEY,context_origin TEXT NOT NULL,time_stamp INTEGER NOT NULL,bits_debit REAL NOT NULL);
CREATE INDEX budget_mapping_origin_time_stamp_idx ON budget_mapping(context_origin,time_stamp);
CREATE INDEX values_mapping_last_used_time_idx ON values_mapping(last_used_time);
CREATE INDEX per_origin_mapping_creation_time_idx ON per_origin_mapping(creation_time);
COMMIT;
