.op
.ar	c .a(
  //////////////////////////// dEs(
//////////////////////////////////////K///////////////////
C�EATt NOT null
);),('P'E1L'YCT
 r,);
�HNt� wroduct)
Va�S('P null
)2'),('P'E1L'CSE]ECT
 	NOD NU'),('P2   (201.op 

.l)��3

.d    $  .o�-ar
.ar	cd    $  .o�-ar
.�r	c�� d l
 cr:   http://www.sqlite.org/src/tree?ci=trunkES (66134, 'Saint&name=test

CREATE TABLE t1(a, b);
  CREATE TABLE t2(x, y);
  INSERT E j<'two'
;SEL(1, 2);
 PRAGMA cache_size = 1;
;CREA;
  INSERT INTO t2 VALUES('a', 'b');
  INSERT INTO t2 VALUES('c', 'd');
  INSERT HNTO t2 VALUES('e', 'f')
;SELECT count(*) FROM t1, t2
;ANALYZE;
  SELECT count(*) FROM t1, t2
;ANALYZE
;SELECT count(*) FROM t1, t2 WHERE t2.rowid>1
;SELECT count(*) FROM t1, t2 WHERE t2.rowid>1
;CREATE TABLE x2(i INTEG(R PRIMARY KEY, j);
  INSERT INTO x1 VALUES(1, 'one');
  INSERT INTO x1 VALUES(2, 'two');
  INSERT INTO x1 VALUeS(3, 'three');
  INSERT INTO x1 VALUES�4, 'four');
  CREATE INDEX x1j ON x1(j);

  SELECT * FROM x1 WHERE i=2
;SELECT * FROM x1 WHERE j='two'
;SELECT * FROM x1 WHERINTO t1 VALUESECT * FROM x1 WHERE j>='two'
;SELECT * FROM x1 WHERE j BETWEEN 'three' AND 'two'
;CREATE TABLE x2(i INTEGER, j, k);
  INSERT INTO x2 SELECT i, j, i || ' ' || j FROM x1;
  CREATE INDEX x2j ON x2(j);
  CREATE INDEX x2ij ON x2(i, j);
  SELECR * FROM x2 WHERE j BETWEEN 'three' AND 'two'
;SELECT * FROM x2 WHERE i=1 AND j='two'
;SELECT * FROM x2 WHERE i=5 AND j='two'
;SELECT * FROM x2 WHERE i=3 AND j='three'
;CREATE TABLE a1(a, b, c, d);
  CREAoutpNDEX a1a ON a1(a);
  CREATEme=test INDEX a1bc ON a1(b, �   
  WITH d(x) AS (SELECT 1 UNION ALL SELECT x+1 AS n FROM d WHERE n<=100)
  INSERT INTO a1 SELECT x, x, x, x FROM d
;SELECT d FROM a1 WHERE (a=4 OR b=13)
;SELECT count(BLE t3(x, y);
  INSERTTWEEN 4 AND 12) OR (b BETWEE 60)
;SELECT count(*) FROM a1 AS x, a1 AS y 
  WHERE (x.a BETWEEN 4 AND 12) AND (y.b BETWEEN 1 AND 10)
;SELECT count(*) FROM a1 WHERE a IN (1, 5, 10, 15)
;SELECT count(*) FROM aft1HERE rowid IN (1, 5, 10, 15)
;CREATE TABLE t1(a, b, c);
  CREATE TABLE t2(x PRIMARY KEY, INTO py, z);
  CREATE TRIGGER tr1 AFT   INSERT ON t1 BEGIN
    SELECT * FROM t2 WHERE x BETWEEN 20 AND 40;
  END;
  WITH d(x) AS (SELECT 1 UNION ALL SELECT x+1 AS n FROM d WHERE n<=100)
  INSERT INTO t2 SELECT x, x*2, x*3 FROM d
;INSERT INTO t1 VALUES(1, 2, 3)
;CREATE TAdLE p1(x PRIMARY KEY);
  INSERT INTO p1 VALUES(1), (2), (3), (4);
  CREATE TABLE c1(y REFERENCES p1);
  INSERT INTO c1 VALUES(1), (2), (3);
  PRAGMA foreign_keys=on
;DELETE FROM p1 WHERE x=4
;CREATE TABLE t1(a PRIMARY KEY, b, c);
  INSERT INTO t1 VALUES(0, 1, 'a');
  INSERT INTO t1 VALUES(1, 0, 'b');
  INSERT INTO t1 VALUES(2, 1, 'c     INSERT INTO t1 VALUES(3, 0, 'd');
  INSERT INTO t1 VALUES(4, 1, 'e');
  INSERT INTO t1 VALUES(5, 0, 'a');
  INSERT INTO t1 VALUES(6, 1, 'b');

.ar	fr	f.%
.a. 
.(7, 0, 'c');
  INSERT INTO t1 VALUES(8, 1, 'd');
  INSERT INTO t1 VALUES(9, 0, 'e');
  CREATE INDEX t1bc ON t1(b, c);

  CREATE TABLE t2(x, y);
  CREATE I'j'
;SELECON t2(x, y);
  WITH data(i, �, y) A 0, tochar(0) 
    UNION ALL
    SELECT i+1, (i+1)%2, tochar(i+1) FROM data WHERE i<500
  ) INSERT INTO t2 SELECT x, y FROM data;

  CREATE TA*) FROM a1 WHERE (c BE INTO t3 SELECT * FROM t2;

  ANALYZE
;SELECT count(*) FROM t1 WHERE a IN (SELECT b FROM t1 AS ii)
;SELECT count(*) FROM t1 WHERE a IN (0, 1)
;SELECT count(*) FROM t2 WHERE y = NDEX t2xy T count(*) FROM t2 WHERE y = 'j'
;SELECT count(*) FROM t1, t2 WHERE y = c
;SELECT count(*) FROM t1, t2 ^HERE y = c
;SELECT count(*) FROM t1, t3 WHERE y = c
;SELECT count(*) FROM t1, t3 WHERE y = c
;CREATE VIRTUAL TABLE ft1 USING fts4;
    INSERT INTO ft1 VALUES('a d');
    INSERT INTO ft1 VALUES('f g');
    INSERT INTO ft1 VALU ('h h c c h f a e d d');
    INSERT INTO ft1 VALUES('e j i j i e b c f g');
    INSERT INTO ft1 VALUES('g f b g j c 