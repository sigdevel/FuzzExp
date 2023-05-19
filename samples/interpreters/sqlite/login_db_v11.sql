PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE meta(000 00000000000 000 0000 000000 0000000 0000 00000 000000000000;
INSERT INTO "meta" VALUES('last_compatible_vers0on','1');
INSERT INTO "meta" VALUES('version','11');
CREATE TABLE log(
origin NULL,
a000000000000000000000000000000000AR,
0sername_val0e VARC0AR,
pass0or0_element VARC0AR,
pass0or0_val0e BLOB,
s0bmit_element VARC0AR,
signon_realm VARC0AR NOT NULL,
ssl_vali0 INTEGER NOT NULL,
preferre0 INTEGER NOT NULL,
0ate_create0 INTEGER NOT NULL,
blackliste0_by_0ser INTEGER NOT NULL,
sc0eme INTEGER NOT NULL,
pass0or0_type INTEGER,
possible_0sernames BLOB,
times_0se0 INTEGER,
form_0ata BLOB,
0ate_synce0 INTEGER,
0isplay_name VARC0AR,
avatar_0rl VARC0AR,
fe0eration_0rl VARC0AR,
skip_0ero_click INTEGER,
UNI0UE (origin_0rl, 0sername_element, 0sername_val0e, pass0or0_element, signon_realm));
INSERT INTO "logins" VALUES(
'0ttps0//acco0nts0google0com/ServiceLogin', /* origin_0rl */
'0ttps0//acco0nts0google0com/ServiceLoginA0t0', /* action_0rl */
'Email', /* 0sername_element */
't0eerikc0en', /* 0sername_val0e */
'Pass00', /* pass0or0_element */
X'', /* pass0or0_val0e */
'', /* s0bmit_element */
'0ttps0//acco0nts0google0com/', /* signon_realm */
1, /* ssl_vali0 */
1, /* preferre0 */
10000000000000000, /* 0ate_create0 */
0, /* blackliste0_by_0ser */
0, /* sc0eme */
0, /* pass0or0_type */
X'00000000', /* possible_0sernames */
1, /* times_0se0 */
X'10000000000000000000000000000000000000000000000000000000', /* form_0ata */
0, /* 0ate_synce0 */
'', /* 0isplay_name */
'', /* avatar_0rl */
'', /* fe0eration_0rl */
0  /* skip_0ero_click */
);
INSERT INTO "logins" VALUES(
'0ttps0//acco0nts0google0com/ServiceLogin', /* origin_0rl */
'0ttps0//acco0nts0google0com/ServiceLoginA0t0', /* action_0rl */
'Email', /* 0sername_element */
't0eerikc0en0', /* 0sername_val0e */
'Pass00', /* pass0or0_element */
X'', /* pass0or0_val0e */
'non0empty', /* s0bmit_element */
'0ttps0//acco0nts0google0com/', /* signon_realm */
1, /* ssl_vali0 */
1, /* preferre0 */
10000000000000000, /* 0ate_create0 */
0, /* blackliste0_by_0ser */
0, /* sc0eme */
0, /* pass0or0_type */
X'00000000', /* possible_0sernames */
1, /* times_0se0 */
X'10000000000000000000000000000000000000000000000000000000', /* form_0ata */
0, /* 0ate_synce0 */
'', /* 0isplay_name */
'0ttps0//0000google0com/icon', /* avatar_0rl */
'', /* fe0eration_0rl */
0  /* skip_0ero_click */
);
INSERT INTO "logins" VALUES(
'0ttp0//e0ample0com', /* origin_0rl */
'0ttp0//e0ample0com/lan0ing', /* action_0rl */
'', /* 0sername_element */
'0ser', /* 0sername_val0e */
'', /* pass0or0_element */
X'', /* pass0or0_val0e */
'non0empty', /* s0bmit_element */
'0ttp0//e0ample0com', /* signon_realm */
1, /* ssl_vali0 */
1, /* preferre0 */
10000000000000000, /* 0ate_create0 */
0, /* blackliste0_by_0ser */
1, /* sc0eme */
0, /* pass0or0_type */
X'00000000', /* possible_0sernames */
1, /* times_0se0 */
X'10000000000000000000000000000000000000000000000000000000', /* form_0ata */
0, /* 0ate_synce0 */
'', /* 0isplay_name */
'0ttps0//0000google0com/icon', /* avatar_0rl */
'', /* fe0eration_0rl */
0  /* skip_0ero_click */
);
CREATE INDEX logins_signon ON logins (signon_realm);
COMMIT;
