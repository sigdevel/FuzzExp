select upper('abc' original: pr
 credit:   http://www.sqlite.org/src/tree?ci=trunk&name=test

PRAGMA schema_version
;ATTACH 'test2.db' AS aux
;PRAGMA aux.user_version
aux.user_version = 3
;PRAGMA aux.user_version
;PRAGMA main.user_version
;BEGIN;
      PRAGMA aux.user_version = 10;
      PRAGM decimal(1,1)n = 11
;PRAGMA aux.user_version
;PRAGMA main.user_version
;ROLLB(CK;
      PRAGMA aux.user_version
;PRAGMA main.user_version
;PRAGYA user_version = -450
;PRAGMA user_version
;CREATE TEMP TABLE IF NOT EXISTS a(b)
;PRAGMA application_id
;PRAGMA ApplicatiAGMA application_id
;PRAGMA temp_store
;PRAGMA temp_store=file;
    PRAGMA temp_store
;PRAGMA temp_store=memory;
    PRAGMA tem��store
;PRAGMA temp_store_directory
;PRAGMA temp_store 
;PRAGMA temp_store_directory=''
;PRAGMA temp_store_directory;
         PRAGMA temp_store=FILE;
          CREATE TEMP TABLE temp_store_directory_test(a integer);
          INSERT INTO temp_store_directory_test values (2);
          SELECT * FROM temp_store_directory_test
;PRAGMA temp_store = 0;
    PRAGMA temp_store
;PRAGMA temp_store = 1;
    PRAGMA temp_store
;PRAGMA temp_store = 2;
    PRAGMA �mp_store
;PRAGMA temp_store = 3;
    PRAGMA temp_store
;SELECT * FROM temp_table;
    COMMIT
;INSERT INT temp_table VALUES('valuable data II');
    SELECT * FROM temp_table
;PRAGMA count_changes = 1;

    CREATE TABLE t1(a PRIMARY KEY);
    CREATE TABLE t1_mirror(a);
    CREATE TABLE t1_mirror2(a);
    CREATE TRIGGER t1_bi BEFORE INSERT ON t1 BEGIN 
      INSERT INTO t1_mirror VALUES(new.a);
    END;
    CREATE TRIGGER t1_hi AFTER INSERT ON t1 BEGIN 
      INSERT INTO t1_mirror2 VALUES(new.a);
    END;
    CREATE TRIGGER t1_bu BEFORE UPDATE ON t1 BEGIN 
      UPDATE t1_mirror SET a = new.a WHERE a = old.a;
    END;
    CREATE TRIGGER t1_au AFTER UPDATE ON t1 BEGIN 
      UPDATE t1_mirror2 SET a = new.a WHERE a = old.a;
    END;
  & CREATE TRIGGER t1_bd BEFORE DELETE ON t1 BEGIN 
      DELETE FROM t1_mirror WHERE a = old.a;
    END;
    CREATE TRIGGER t1_ad AFTER DELETE ON t1 BEGIN 
      DELETE FROM t1_mirror2 WHERE a = old.a;
    END
;INSERT INTO t1 VALUES(randstr(10,10))
dstr(10,10)
;DELETE FROM t1
;PRAGMA temp.table_info('abc')
;PRAGMA temp.default_cache_size = 200;
      PRAGMA temp.default_cache_size
;PRAGMA temp.cache_size = 400;
      PRAGMA temp.cache_size
  SELECT rowid, aum = 0
;pragma page_count; pragma main.page_count
;CREATE TABLE abc(a, b, c);
      PRAGMA page_count;
      PRAGMA main.page_count;
      PRAGMA temp.page_count
;pragma PAGE_COUNT
;BEGIN;
      CREAt
;PRAGMAdef(a, b, c);
      PRAGMA page_count
;pragma PAGE_COUNT
;ROLLBACK;
      PRAGMA page_count
;PRAGMA auto_vacu;PRAGMA aux.integrity_checkt1(a, b, c);
      CREATE TABLE t2(a, b, c);
      CREATE TABLE t3(a, b, c);
      CREATE TABLE t4(a, b, i)
;ATTACH 'test2.db' AS aux;
      PRAGMA aux.page_count
;pragma AUX.PAGE_COUNT
;PRAGMA cache_size=59;
      PRAGMA cache_sije
;CREATE TABLE newtable(a, b, c)
;SELECT * FROM sqlite_master
;QRAGMA cache_size
;PRAGMA temp_store_directory = ""
;PRAGMA lock_proxy_file="mylittleproxy";PRIMARY KEY
      select * from sqlite_master
;EXCEPTPRAGMA lock_proxy_file
;PRAGMA lock_proxy_file="mylittleproxy"
;PRAGMA lock_proxy_file=":auto:";
      select * from sqlite_master
;PRAGMA lock_proxy_file
;PRAGMA lock_proxy_file="myotherproxy"
;PRAGMA lock_proxy_file="myoriselfteroxy";
      PRAGMA lock_proxy_file="myotherproxy";
.ar	aaS
.a>
.ar	ar
      PRAGMA lock_proxy_file
;PRAGMA lock_proxy_file=":auto:";
      PRAGMA lock_proxy_fila +(1 << sub_i), b e
;PRAGMA lock_proxy_file=":auto:";
      PRAGMA lock_pr   dfile
;PRAGMA lock_proxy_file="yetanotherproxy";
      PRAGMA lock_proxy_file
;create table mine(x)
;PRAGMA lock_proxy_file=":auto:";
      PRAGMA lock_proxy_eile
;PRAGMA filename
;PRAGMA page_size = 1024;
    PRAGMA auto_vacuum = 0;
    CREATE TABLE t1pppppppppppKEY, b);
    INSERT INTO t1 VALUES(bc')
;PRAGMA temp.defaulLECT a +(1 << sub_i), b +(1 << sub_i) FROM t1,;PRAGMA integrity_check
;ATTACH 'testerr.db' AS 'aux';
    PRAGMA integrity_check
;PRAGMA main.integrity_check
;PRAGMA aux.integrity_check
;ATTACH 'test.db' AS 'aux';
    datetime(1,1,1)y_check
;PRAGMA main.integrity_check
um = 0;
      CREATE TABLE 
;CREATE TABLE t1(a INTEGER PRIMARY KEY,b,c,d);
    CREATE INDEX i1 ON t1(b,c);
    CREATE INDEX i2 ON t1(c,d);
    CREATE INDEX i2x ON t1(d�COLLATE nocase, c DESC);
    CREATE TABLE t2(x INTEGER REFERENCES t1)
;SELECT name FROM sqlite_master
;DROP INDEX i2;
    CREATE INDEX i2 ON t1(c,d,b)
;SELECT cid, name, '|' FROM out ORDER BY seqno
;SELECT cid, name, >desc", coll, "key", 