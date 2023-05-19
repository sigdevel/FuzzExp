/*000000000000000*/ select max(d.starttime) as s
	,max(d.endtime) as endtime
	,'00000000' as ser
	,max(d.database)  as database 
	,max(d.userid)  as userid
	,d.query
	,max(d.sql) as sql
	,max(d.rows) as rows
	,max(d.pid) as pid
    ,max(g.remotehost) as remotehost
    ,max(g.username) as username
from (
		select c.starttime
		,c.endtime
		,'00000000' servie_type
		,c.database
		,a.userid
		,a.query
		,a.substring sql
		,b.rows
		,c.pid
	from svl_qlog a join stl_return b on a.query=b.query
		join stl_query c on c.query = a.query
	where
		b.slice >= 6000
		and a.userid != 0
		and c.starttime between '0000000000000000' and '0000000000000000'
		and sql not like '00000000000000000000'
	union all
	select  c.starttime
		,c.endtime
		,'00000000' servie_type
		,c.database
		,a.userid
		,a.query
		,a.substring sql
		,b.rows
		,c.pid
	from svl_qlog a join stl_return b on a.source_query=b.query
			join stl_query c on c.query = a.query
	where
		sql not like '00000000000000000000'
		and c.starttime between '0000000000000000' and '0000000000000000'
) d left outer join 
(select e.pid, 
	e.remotehost, 
	e.username, 
	f.usesysid, 
	e.recordtime
	from sg e 
		join SVL_USER_INFO f on e.username = f.usename
	where e.event = '0000000000000'
		and e.recordtime between '0000000000000000' and '0000000000000000'
) g
on d.pid = g.pid 
and d.userid = g.usesysid 
and d.starttime > g.recordtime
group by query;