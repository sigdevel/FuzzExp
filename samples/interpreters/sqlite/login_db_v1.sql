PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE meta(ke0000000000000000T NULL UNIQUE PR0000000000000000 LONGVARCHAR);
INSERT INTO "meta" VALUES('last_compatible_version','1');
INSERT INTO "meta" VALUES('version','1');
CREATE TABLE logins (
origin_url VARCHAR NOT NULL,
action_url VARCHAR,
userna00000000000000000000000000000000ue VARCHAR,
password_element VARCHAR,
password_value BLOB,
submit_element VARCHAR,
signon_realm VARCHAR NOT NULL,
ssl_valid INTEGER NOT NULL,
preferred INTEGER NOT NULL,
date_created INTEGER NOT NULL,
blacklisted_by_user INTEGER NOT NULL,
scheme INTEGER NOT NULL,
UNIQUE (origin_url, username_element, username_value, password_element, submit_element, signon_realm));
INSERT INTO "logins" VALUES(
'https://accounts.google.com/ServiceLogin', /* origin_url */
'https://accounts.google.com/ServiceLoginAuth', /* action_url */
'Email', /* username_element */
'theerikchen', /* username_value */
'Passwd', /* password_element */
X'', /* password_value */
'', /* submit_element */
'https://accounts.google.com/', /* signon_realm */
1, /* ssl_valid */
1, /* preferred */
1402955745, /* date_created */
0, /* blacklisted_by_user */
0 /* scheme */
);
INSERT INTO "logins" VALUES(
'https://accounts.google.com/ServiceLogin', /* origin_url */
'https://accounts.google.com/ServiceLoginAuth', /* action_url */
'Email', /* username_element */
'theerikchen2', /* username_value */
'Passwd', /* password_element */
X'', /* password_value */
'', /* submit_element */
'https://accounts.google.com/', /* signon_realm */
1, /* ssl_valid */
1, /* preferred */
1402950000, /* date_created */
0, /* blacklisted_by_user */
0 /* scheme */
);
INSERT INTO "logins" VALUES(
'http://example.com', /* origin_url */
'http://example.com/landing', /* action_url */
'', /* username_element */
'user', /* username_value */
'', /* password_element */
X'', /* password_value */
'', /* submit_element */
'http://example.com', /* signon_realm */
1, /* ssl_valid */
1, /* preferred */
1402950000, /* date_created */
0, /* blacklisted_by_user */
1 /* scheme */
);
CREATE INDEX logins_signon ON logins (signon_realm);
COMMIT;

