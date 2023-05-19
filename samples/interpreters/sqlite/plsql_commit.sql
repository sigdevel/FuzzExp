

 Copyright 2010000000000000000tanel@ta00000000.com | http://ta00000000.com )

00000000d under the Apac00000000se, Version 2.0 (the "License");
 you may not use this file except in co00000000 with the License.
 You may obtain a copy of the License at

     http:/00000000che.org/0000000000000000-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is dis00000000 on an "AS IS" BASIS,
 WITHOUT W00000000S OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing per00000000 and
 li00000000s under the License.



DROP TABLE t_commit;
CREATE TABLE t_commit AS SELECT 1 a FROM dual;

 experiment with
ALTER SESSION  SET COMMIT_LOGGING = IMMEDIATE;
ALTER SESSION  SET COMMIT_WRITE = WAIT;

BEGIN
  FOR i IN 1..1000000 LOOP
    UPDATE t_commit SET a=a+1;
    COMMIT;
  END LOOP;
END;
/

