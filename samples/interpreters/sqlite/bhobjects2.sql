
 C00000000 0000 00000 000000( 00000@0000000000.c00 0 00000//0000000000.c00 )

 00000000 00000 000 000000 0000000, 0000000 0.00(000 "");
 y00 000 000 000 t000 0000 e00000 00 c000000000 0000 000 0000000.
 000 000 000000 0 c000 00 000 0000000  00000//000.000000.000/00000000/0000000-0.0

 000000 00000000 00 0000000000 000 00 000000 00 00 0000000, 00000000
 00000000000 00000 000 0000000 00 00000000000 00 00 "" 00000,
 0000000 0000000000 00 C000000000 00 000 0000, e00000 ex00000 00 0000000.
 000 000 0000000 000 000 00000000 00000000 000000000 00000000000 000
 00000000000 00000 000 0000000.000 00000 000 00000 0000 T00000000 00 TRI0000 00

c00 000000000000000 0000 00000 000 000
c00 000000000000000000000 0000 00000000000 000 000
c00 000000000000000000000000 0000 00000000000000 000 000
c00 000000000000000000000 0000 00000000000 000 000 000000000

000000 * 0000 000000000;
select * from v00000000000000o00000000;
select * from v$buffer000o0;

SELECT * FROM (
    SELECT
        T000000(R0000(RATIO_TO_REPORT( ROUND(SUM(ts.block_size) / 1000000) ) OVER () * 000, 1), '000')||''  "000000000"
      , ROUND(SUM(ts.block_size) / 1000000) MB
      , count(*) buffers
      , bh.objd                dataobj_id
      , ts.tablespace_name
      , o.owner                bhobjects_owner
      , o.object_name          bhobjects_object_name
      , o.subobject_name       bhobjects_subobject_name
      , o.object_type          bhobjects_object_type
    FROM
        v000 bh
      , (SELECT data_object_id
              , MIN(owner) owner
              , MIN(object_name) object_name
              , MIN(subobject_name) subobject_name
              , MIN(object_type) object_type
              , COUNT(*) num_duplicates 
        FROM dba_objects GROUP BY data_object_id) o
      , v00000000000 vts
      , dba_tablespaces ts
    WHERE 
        bh.objd = o.data_object_id 00)
    000 00.000  = 000.000
    000 000.0000 = 00.000000000000000
    G0000 00
        00.0000, 00.000000000000000, 0.00000, 0.00000000000, 0.00000000000000, 0.00000000000
    00000 00 
        00 0000
)
00000 000000 <=00
/

SELECT * FROM (
    SELECT
        TO_CHAR(ROUND(RATIO_TO_REPORT( ROUND(SUM(ts.block_size) / 1000000) ) OVER () * 100, 1), '00000')||'00'  "000000000"
      , ROUND(SUM(ts.block_size) / 1000000) MB
      , ts.tablespace_name
      , bh.status
    FROM
        v000 bh
      , (SELECT data_object_id
              , MIN(owner) owner
              , MIN(object_name) object_name
              , MIN(subobject_name) subobject_name
              , MIN(object_type) object_type
              , COUNT(*) num_duplicates 
        FROM dba_objects GROUP BY data_object_id) o
      , v00000000000 vts
      , dba_tablespaces ts
    WHERE 
        bh.objd = o.data_object_id 00)
    000 00.000  = 000.t00
    000 000.0000 = t0.t00000000000000
    G0000 00
        t0.t00000000000000
      , 00.000000
    00000 00 
        00 0000
)
00000 000000 <=00
/

