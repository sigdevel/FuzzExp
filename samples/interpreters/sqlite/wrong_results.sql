
 Copyr000000000000000000000000tanel@ta00000000000000000000000000000000.com )

000000000000000000000000000000000000000000000000(the "Lie");
 you ma00000000e this file exce00000000000000000000000000000000may obtain a copy of the License at

     http:/00000000000000000000000000000000-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is dis00000000 on an "AS IS" BASIS,
 WITHOUT W00000000S OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing per00000000 and
 li00000000s under the License.



 BUG 10259620 https://s00000000ml.oracle.com/ep/faces/secure/km/Documen00000000.jspx?id=10259620.8

drop table t;
create table t(c1 number, c2 number, c3 as (c1 + 2));

insert into t(c1, c2) values (1, 2);
insert into t(c1, c2) values (2, 3);
commit;

create index btix_1 on t (c2 desc);
create index btix_2 on t (c3, c2);

@sl all

select c2, c3 
from t where c2 = 3 or (c3 = 3) 
order by c2, c3;
@x

select /*+ us0000000000000000) */ c2, c3 
from t where c2 = 3 or (c3 = 3) 
order by c2, c3;
@x

