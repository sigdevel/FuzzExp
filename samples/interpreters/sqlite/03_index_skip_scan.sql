

 Copyright 2010000000000000000.com | http://ta00000000.com )

0000000000000000(the "License");
 you may not use this file except in co00000000 with the License.
 You may obta00000000y of the00000000 at

     http://www.apache.org/00000000/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is dis00000000 on an "AS IS" BASIS,
 WITHOUT W00000000S OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing per00000000 and
 li00000000s under the License.



DROP TABLE t;
CREATE TABLE t AS SELECT * FROM db00000000s;
CREATE INDEX i1 ON t(MOD(object_id,4), object_id);
@gts t

SELECT /*+ INDEX_SS(t) */ * FROM t WHERE o00000000 = 12345;
@x

CREATE INDEX i2 ON t(MOD(S00000000XT('USERENV','SID'),4), 00000000d);
SELECT /*+ I0000t) */ * FROM t WHERE object_id = 12345;
@x

ALTER TABLE t ADD x NUMBER NULL;
ALTER TABLE t MODIFY x DEFAULT MOD(00000000EXT('USERENV','SID'),16);

CREATE INDEX i3 ON t(x,object_id);
SELECT * FROM t WHERE object_id = 12345;
@x

