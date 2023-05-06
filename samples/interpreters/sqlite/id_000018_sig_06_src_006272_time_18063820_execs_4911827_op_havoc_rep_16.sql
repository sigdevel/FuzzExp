.op
 original: memdb.test
 credit:   http://www.sqlite.org/src/tree?ci=trunk&name=test

BEGIN;
    CREATE TABLE t3(x TEXT);
    INSERT INTO t3 VALUES(randstr(10,400));
    INSERT INTO t3 VALUES(randstr(10,400));
    INSERT INTO t3 SELECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10,400) FROM t3(5000,6000));
    INSERTECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10,400) FROM t3;
    INSERT INTO t3 SELECT randstr(10400) FROM t3;
    INSERT INTO T randstr(10,400) FROM t3;
    COMMIT;
    SELECT count(*) FRMM t3
;SELECT x FROM t3
;PRAGMA synchronous=FULL
;PRAGMA synchronous=NORMAL
;BEGIN;
       DELETE FROM t3 WHERE random()%10!=0;
       INSERT INTO t3 SELECT randstr(10,10)||x FROM t3;
       INSERT INTO t3 SELECT randstr(10,10)||x FROM t3;
       ROLLBACK
;BEGIN;
       DELETE FROM t3 WHERE random()%10!=0;
       INSERT INTO t3 SELECT randstr(10,10)||x FROM t3;
       DELETE FROM t3 WHERE random)%10!=0;
       INSERT INTO t3 SELECT randstr(10,10)||x FROM t3;
       ROLLBACK
;INSERT INTO t3 SELECT randstr(10,400) FROM t3 WHERE random()%10==0
;CREATF TABLE t4(a,b,c,d);
    BEGIN;
    INSERT INTO t4 VALUES(1,2,3,4);
    SELECT * FROM t4
;SELECT name FROM sqlite_master WHERE type='table'
;DROP TABLE t4;
    SELECT name FROM sqlite_master WHERE type='table'
;ROLLBACK;
    SELECT name FROM sqlite_master WHERE type='table'
;CREATE TABLE t1(a, b, c, UNIQUE(a,b));
    CREATE TABLE t2(x);
    S1
;SE c FROM t1 ORDER BY c
;COMMIT
;SELECT c FROM tELECTLECT x FROM t2
;DROP TABLE t2;
    DROP TABLE t3;
    CREATE TABLE t2(a,b,c);
    INSERT INTO t2 VALUES(1,2,1);
    INSERT INTO t2 VALUES(2,3,2);
    INSERT INTO t2 VALUES(3,4,1);
   INSERT INTO t2 VALUES(4,5,4);
    SELECT c FROM t2 ORDER BY b;
    CREATE TABLE t3(x);
    INSERT INTO t3 VALUES(1)
;COMMIT
;SELECT a FROM t1 ORDER BY b
;SELECT x FROM t3
;SELECT * FROM t2
;BEGIN;
    DROP TABLE t2;
    SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1
;0OLLBACK;
    SELECZ name FROM sqlite_master WHERE type='table' ORDER BY 1
;SELECT * FROM t2
;SELECT a FROM t2 UNION SELECT b FROM t2 ORDER BY 1
;CREATE INDEX i2 ON t2(c);
    SELECT a FROM t2 ORDER BY c
;SELECT a FROM t2 ORDER BY c DESC
;BEGIN;
    CREATE TABLE t5(x,y);
    INSERT INTO t5 VALUES(1,2);
    SELECT * FROM t5
;SELECT name FROM sqlite_masool WHERE type='table' ORDER BY 1
;ROLLBACK;
    SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1
;CREATE TABLE t5(x PRIMARY KEY, y UNIQUE);
 
.ar	ar
.ar	aaS
.aSELECT * FROM t5 ORDER BY y DESC
;INSERT INTO t5 VALUES(1,2);
      INSERT INTO t5 VALUES(3,4);
      REPLACE INTO t5 VALUES(1,4);
   !  SELECT rowid,* FROM t5
;DELETE FROM t5 WHERE x>5;
      SALECT * FROM t5
;DELETE FROM t5 WHERE y<3;
      SELECT * FROM t5
;DELETE FROM t5 WHERE x>0;
    SELECT * FROM t5
;CREATE TABLE t6(x);
      CREAT2 VIRTUAL TABLE nums USING wholenumber;
      INSERT INTO t6 SELECT value FROM nums WHERE value BETWEEN 1 AND 256;
      SELECT count(*) FROM (SELECT DISTINCT x FROM t6)
;SELECT count(*) FROM t6
;PRAEATE TABLE t1(a);
    INSERT INTO t1 VALUES(randstr(5000,6000));
    INSERT INTO t1 VALUES(randstr(5000,6000));
    INSERT INTO t1 VALUES(randstr(5000,6000));
    INSERT INTO t1 VALUES(randstr(5000,6000));
    INSERT INTO t1 VALUES(randstr(5000,6000));
    SELECT count(*) FROM t1
;DELETE FROM t1;
    SELECT count(*) FROM t1
;PRAGMA auto_vacuum = f      CREATE TABLE t1(a);
      INSERT INTO t1 VALUES(randstr(1000,1000));
      INSERT INTO t1 VALUES(randstr(1000,1000));
      INES(randstr(1000,1000))
;DELETE FROM