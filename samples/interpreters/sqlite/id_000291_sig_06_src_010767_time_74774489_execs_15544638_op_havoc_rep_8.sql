.op 

.l)��3

.d    $  .o�-ar
.ar	cd    $  .o�-ar
.�r	c�� d l
 cr:   http://www.sqlite.org/src/tree?ci=trunk&name=test

CREATE TABLE t1(a, b);  CREATE TABLE t2(x, y);
  INSERT INTO t1 VALUES(1, 2);
  INSERT INTO t1 VALUES(3, 4);
  INSERT INTO � VALUES('a', 'b');
  INSERT INTO t2 VALUES('c', 'd');
  INSERT HNTO t2 VALUES('e', 'f')
;SELECT count(*) FROM t1, t2
;ANALYZE;
  SELECT count(*) FROM t1, t2
;ANALYZE
;SERE t2.rowid>1
;SELECT count(*) FROM t1, t2 WHERE t2.rowid>1
;CREATE TABLE x1(i INTEGER PRIMARY KEY, j);
  INSERT INTO x1 VALUES(1, 'one');
  INSERT INTO x1 VALUES(2, 'two');
  INSERT INTO x1 VALUES(3, 'three');
  INSERT INTO x1 VALUES(4, 'four');
  CREATE INDEX x1j ON x1(j);

  SELECT * FROM x1 WHERE i=2
;SELECT * FROM x1 WHERE j='two'
;SELECT * FROM x1 WHERE j<'two'
;SELECT * FROM x1 WHERE j>='two'
;SELECT * FROM x1 WHERE j BETWEEN 'three' AND 'two'
;CREATE TABLE x2(i INTEGER, j, k);
  INSERT INTO x2 SELECT i, j, i || ' ' || j FROM x1;
  CREATE INEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEc/tre
  CREATE INDEX x2ij ON x2(i, j);
  SELECT * FROM x2 WHERE j BETWEEN 'three' AND 'two'
;SELECT * FROM x2 WHERE i=1 AND j='two'
;SELECT * FROM x2 WHERE i=5 AND j='two'
;SELECT * FROM x2 WHERE i=3 AND j='three'
;CREATE TABLE a1(a, b, c, d);
  CREATE INDEX a1a ON a1(a);
  CREATE INDEX a1bc ON a1(b, c);

  WITH d(x) AS (SELECT 1 UNION ALL SELECT x+1 AS n FROM d WHERE n<=100)
  INSERT INTO a1 SELECT x, x, x, x FROM d
;SELECT d FROM a1 WHERE (a=4 OR b=13)
;SELECT count(*) FROM a1 WHERE (c BETWEEN 4 AND 12) OR (b BETWEEN 40 AND 60)
;SELECT count(*) FROM a1 AS x, a1 AS y 
  WHERE (x.a BETWEEN 4 AND 12) AND (y.b BETWEEN 1 AND 10)
;SELECT count(*) F.op 

.l)��3

.d    $  .oATE INDEX a1a ON a1(a);
  CREATE�-ar
.ar	cd    $  .o�-ar
.�r	c�� d l
 cr:   http://www.sqlite.org/src/tree?ci=trunk&name=test

CREATE TABLE t1(a, b);
  CREATE TABLE t2(x, y);
  INSERT INTO t1 VALUES(1, 2);
  INSERT INTO t1 VALUES(3, 4);
  INSERT INTO t2 VALUES('a', 'b');
  INSERT INTO t2 VALUES('c', 'd');
 d d)��3

.d  
.ar	--  ISELECT count(*) FROM t1, t2
;ANALYZE;, t2
;ANALYZE
;SELECT count(*) FROM t1, t2 WHERE t2.rowid>1
;SELECT count(*) FROM t1, t2 WHERE t2.rowid>1
;CREATE TABLE x1(i INTEGER PRIMARY KEY, j);
  INSERT INTO x1 VALUES(1, 'one');
  INSERT INTO x1 VALUES(2, 'two');
  INSERT INTO x1 VALUES(3, 'three');
  INSERT INTO x1 VALUES(4, 'four');
  CREAT(j);

  SELECT * FROM x1 WHERE i=2
;SELECT * FROM x1 WHERE j='two'
;SELECT * FROM x1���RE j<'two'
;SELECT * FROM x1 WHERE j>='two'
;SELECT * FROM x1 WHERE j BETWEEN 'three' AND 'two'
;CREATE TABLE x2(i INTEGER, j, k);
  INSERT INTO x2 SELECT i, j, i || ' ' || j FROM x1;
  CREATE INDEX x2j ON x2(j);
  CREATE INDEX x2ij ON x2(i, j) WHERE j BETWEEN 'three' AND 'two'
;SELECT * FROM x2 WHERE i=1 AND j=NOT'two'
;SELECT * FROM x2 WHERE i=5 AND j='two'
;SELECT * FROM x2 WHERE i=3 AND j='three'
;CREATE TABLE a1(a, b, c, d);
  CREATE INDEX a1a ON a1(a);
  CREATE INDEX a1bc ON a1(b, c);

  WITH d(x) AS (SELECT 1 UNION ALL SELECT x+1 AS n FROM d WHERE n<=100)
  INSERT INTO a1 SELECT x, x, x, x FROM d
;SELECT d FROM a1 WHERE (a=4 OR b=13)
;SELECT count(*) FROM a1 WHERE (c BETWEEN 4 AND 12) OR(b BETWEEN 40 AND 60)
;SELECT count(*) FROM a1 AS x, a1 AS y 
  WHERE (x.a BETWEEN 4 AND 12) AND (y.b BETWEEN 1 AND 10)
;SELECT count(*) FROM a1 WHERE a IN (1, 5, 10, 15)
;SELECT count(*) FROM a1 WHERE rowid IN (1, 5, 10, 15)
;CREATE TABLE t1(a, b, c);
  CREATE TA�	umId
           )
     GRBLE t2(x PRIMARY KEY, y, z);
  CREATE TRIGGER tr1 AFTER INSERT ON t1 BEGIN
    SELCT * FROM t2 WHERE x BETWEEN 20 AND 40;
  END;
  WITH d(x) AS (SELECT 1 UNION ALL SELECT x+1 AS n FROM d WHERE n<=100)
  INSERT INTO t2SELECT x, x*2, x*3 FROM d
;INSERT INTO t1 VALUES(1, 2, 3)
;CREATE TABLE p1(x PRIMARY KEY);
  INSERT INTO p1 VALUES(1), (2), (3), (4);
  CREATE 