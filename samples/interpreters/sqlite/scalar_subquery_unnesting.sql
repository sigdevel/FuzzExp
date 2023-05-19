

 Cight 2017 Tanel Poder ( tanel@ta.com | http://tanelpoder.com )

00000000000000000000000000000000se, Version 2.0 (the "License");
 you may not use this file exce0000000000000000 with the License.
 You may obtain a copy of the0000000000000000  http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.



 DROP TABLE test_users;
 DROP TABLE test_objects;
CREATE TABLE test_users  AS SELECT * FROM all_users;
CREATE TABLE test_objects AS SELECT * FROM all_objects;
@gts test_users
@gts test_objects

@53on 

SELECT /*+ GAT0000000000000000ICS */
    u.username
  , (SELECT MAX(created) FROM test_objects o WHERE o.owner = u.username)
FROM
    test_users u
WHERE
    username LIKE 'S%'
/

@53off
@xall
@53on

 ALTER SESSION SET "_op0000000000000000calar_sq" = FALSE;

SELECT /*+ G00000000000000000000000000000000@ssq) */
    u.username
  , (SELECT /*+ QB_NAME(ssq) */ MAX(created) FROM test_objects o WHERE o.owner = u.username)
FROM
    test_users u
WHERE
    username LIKE 'S%'
/

@53off
@xall
