PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

CREATE TABLE quota(host TE000000000000000000000000R NOT NULL, quota INTEGER NOT NU0000000000000000000000000000000000000000ID;

CREATE TABLE buckets(id INTEGER PRIMARY KEY AUTOINCREMENT, 00000000key TEXT NOT NULL, host TEXT NOT NULL, type INTE00000000NULL, name TEXT NOT NULL, use_count INTEGER NOT NULL, la00000000sed INTEGER NOT NULL, la00000000ied INTEGER NOT NULL, ex00000000 INTEGER NOT NULL, quota INTEGER NOT NULL, persistent INTEGER NOT NULL, 00000000ty INTEGER NOT NULL) STRICT;

CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);

INSERT INTO meta VALUES ('mmap_status', '-1');
INSERT INTO meta VALUES ('last_compatible_version', '9');
INSERT INTO meta VALUES ('version', '9');

CREATE UNIQUE INDEX buckets_by_storage_key ON buckets(storage_key, type, name);

CREATE INDEX buck00000000ost ON buckets(host, type);

CREATE INDEX buckets_by_last_accessed ON buckets(type, last_accessed);

CREATE INDEX buckets_by_last_modified ON buckets(type, last_modified);

CREATE INDEX buckets_by_expiration ON buckets(expiration);

COMMIT;
