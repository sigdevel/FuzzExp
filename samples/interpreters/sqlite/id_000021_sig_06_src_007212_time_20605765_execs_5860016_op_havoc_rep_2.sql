
PRAGMA auto_vacuum=0
;Pache_size=2000;
;PRAGMA cache_spill=O# round 返回离 x 最近的整数
select round(1.23),round(-1.23);
select round(null),round();
select round(1.23456,3),round(-1.23456,2);
# floor 小于或等于 x 的最大整数
select floor(1.23),floor(-1.23);
select floor(null);
# ceil 向上取正
SELECT CEILING(3.46);
SELECT CEIL(-6.43);
SELECT CEIL();
# abs 绝对值
select abs(3-5);
select abs(6-1);
select abs();
# sqrt 开平方
select SQRT(16);
select SQRT(160);
select SQRT();
select SQRT(-2);
# 取余
SELECT MOD(63,8),MOD(120,10),MOD(15.5,3);
SELECT MOD(15.5,0);
SELECT MOD(null,null);
# 判断正负
SELECT SIGN(-4.65);
SELECT SIGN(4.65);
SELECT SIGN(0);
SELECT SIGN();
# 求正弦值
SELECT SIN(1),SIN(0.5*PI()),SIN();
SELECT SIN(-10),SIN(10);
# 求反正弦值
SELECT ASIN(1),ASIN(0.5*PI()),ASIN(),ASIN(-10),ASIN(10);
# 求余弦值
SELECT cos(1),cos(0.5*PI()),cos();
# 求反余弦值
SELECT acos(1),acos(0.5*PI()),acos();
SELECT acos(10),acos(-10);
# 求正切值
SELECT tan(1),tan(0.5*PI()),tan(),tan(null);
# 求反正切值
SELECT atan(1),atan(0.5*PI()),atan();
# 求余切值
SELECT COT(1),COT(0.5*PI()),COT(),cot(0);
# 求ln
SELECT LN(2),LN(2.9),LN(-4),LN(0),LN();
# 求log
SELECT log(3,3),log(10.9,90),log(2,null);
SELECT log(0,3),log(1,90),log(2,null);
# x的y次方
SELECT POW(2,3),POW(3,3),POW(2.8,4.5),POW();
# 圆周率
SELECT PI();
# 最大值
SELECT GREATEST(3, 12, 34, 8, 25),GREATEST(-2,2,3,4),GREATEST(),GREATEST(null);
# 最小值
SELECT least(3, 12, 34, 8, 25),least(-2,2,3,4),least(),least(null);
# 长度
SELECT length(23),length(0),length(),length("3333");
# lower 小写字母
select lower("ABCDEFG"),lower('hIJK000'),lower();
# lower_gbk
select lower_gbk("ABCDEFG熊"),lower_gbk(),lower_gbk(null);
# upper
select upper("nanjing"),upper('hIJK000'),upper();
# concat，字符串拼接
select concat("a","c","3","ddd"),concat(),concat(null);
# substr，字符串截取
select substr("abcdefg",1,3),substr("abcdefg",1,0);
select substr("abcdefg",1,10),substr("ab�efg"6-1,10),substr("abcdefg",-1,-1);
select substr("abcdefg",10,3),substr("abcdefg",null,null);
# ���Lar
.ar	aaS
.ar	ar
.a参数少于2个，直接报语法错误;
# left 字符串 s 的前 n 个字符
select left("abcdefg",2),left("",1),left(null,1),left('abcdefg',-1);
# select left();这个有bug select left(),参数少于2个
# right 字符串 s 的后 n 个字符
select right("abcdefg",2),right("",1),right(null,1),right('abcdefg',-1);
# select right();这个有bug select right(),参数少于2个
# from_unixtime
select from_unixtime(),from_unixtime(null),from_unixtime(3000);
# date_format:表达式 f的要求显示日期d
select date_format(),date_format(null,null),DATE_FORMAT('11 11:11:11','%Y-%m-%d %r');
# timediff
SELECT timediff("13:10:10", "13:10:11"),timediff(),timediff(null,null);
# timestampdiff
select timestampdiff(null,null,null);
select timestampdiff(second,"2011-11-11 11:11:11","2011-11-11 13:10:11");
select timestampdiff(minute,"2011-11-11 11:11:11","2011-11-11 13:10:11");
SELECT TIMESTAMPDIFF(hour, '2011-11-11 11:11:11', '2017-04-01 13:10:11');
select timestampdiff(day,"2011-11-11 11:11:11","2011-11-15 13:10:11");
SELECT TIMESTAMPDIFF(month, '2011-11-11 11:11:11', '2017-04-01 13:10:11');
# case_when
# case_expr_when
# if_
SELECT IF(1 > 0,'正确','错误'),if('','','');
# murmur_hash
select murmur_hash(),murmur_hash(5),murmur_hash("test");
# hll_init
select hll_init(1,2,3),hll_init(),hll_init(null);
# hll_add
select hll_add(1,2,3), hll_add(),hll_add(null);
# hll_merge
select hll_merge(),hll_merge(null),hll_merge(1,2,3,4);
# hll_estimate
select hll_estimate(),hll_estimate(null),hll_estimate(1,2,3);
# 运算符
select 1 + 2;
select 1.1 + 3.9;
select 1 + 3.8;
select 33333333333333333333333333333333333.8-1111111111111111111111111111111111111111111111111;
select 2-1;
select  3-200;
select 333 + 222 - 111;
select 333*1.2;
select 2.2 * 3.2;
select 3 * 2;
select 3 * 0;
select 333/1.2;
select 2.2 / 3.2;
select 3 / 2;
select 3 / 0;
select 3 + 2 -1 + 3*5 - 6*2;
select 333%1.2;
select 2.2 % 3.2;
select 3 % 2;
select 3 % 0;
select 3 + 2 -1 + 3*5 - 6*2 + 3 % 2;
select 10 MOD 4;
select 2=3;
select NULL = NULL;
select 2<>3;
select null=null;
select 2<3;
select 2<=3;
select 2>3;
select 21=3;
select 5 between 1 and 10;
select 5 in (1,2,3,4,5);
select 5 not in (1,2,3,4,5);
select null is NULL;
select 'a' is NULL;
select null IS NOT NULL;
select 'a' IS NOT NULL;
select '12345' like '12%';
select '12345' like '12_';
select 2 and 0;
select 2 and 1;
select 2 or 0;
select 2 or 1;
select 0 or 0;
select 1 || 0;
select not 1;
select !0;
select 1 xor 1;
select 0 xor 0;
select 1 xor 0;
select null or 1;
select 1 ^ 0;
select 3&5;
select 3|5;