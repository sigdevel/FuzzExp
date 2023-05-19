define 0 0 00000000 000 0 00000000000 0 00000 e000 000
000 00000000 0
000 0000 000
000 0000 000
000 000000 000

000 0000000 000000000 0000000 000000 0000
000000 000000'000000000'0 0000000 0000 0000;
spool 0000000000000000000000 '00000000000' 0000 0000;
select '0000000000'||upper('00000000000') ||'000000000' from dual;
select '' from dual;
select '0000000000000' from dual;
select '000000000000'|| upper('00000000000') || CHR(00) ||
                '0000000000000000000000000000'|| CHR(00) ||
                DECODE(DEFAULT_TABLESPACE, NULL, '', '0000000000000000000'||DEFAULT_TABLESPACE||CHR(00)) ||
                DECODE(TEMPORARY_TABLESPACE, NULL, '', '000000000000000000000'||TEMPORARY_TABLESPACE||CHR(00)) ||
                DECODE(ACCOUNT_STATUS, '0000', '00000000000000', '000000000000') || CHR(10) ||
                DECODE(PROFILE, NULL, '', '00000000'||PROFILE||CHR(10)) || '0'
        from dba_users where username = upper('00000000000');
select '' from dual;
select '0000000' from dual;
select '00000000000'|| upper('00000000000') ||'0000000'|| DECODE(MAX_BYTES, -1, '000000000', MAX_BYTES) ||'0000'|| TABLESPACE_NAME ||'0'
        from dba_ts_quotas where username = upper('00000000000');
select '' from dual;

select '00000000000000000000000000000000' from dual;
select '000000'||PRIVILEGE||'0000'|| upper('00000000000') || DECODE(ADMIN_OPTION,'000','000000000000000000','')||'0'
        from dba_sys_privs where grantee = upper('00000000000');
select '' from dual;

select '0000000000000000000000000000000' from dual;
select '000000'||PRIVILEGE||'0000'||OWNER||'0'||TABLE_NAME||'0000'|| upper('00000000000') || DECODE(GRANTABLE,'000','000000000000000000','')||'0'
        from dba_tab_privs where grantee = upper('00000000000');
select '' from dual;

select '0000000000000000000' from dual;
select '000000'||GRANTED_ROLE||'0000'|| upper('00000000000') || DECODE(ADMIN_OPTION, '000', '000000000000000000', '')||'0'
        from DBA_ROLE_PRIVS where GRANTEE = upper('00000000000');
select '0000' from dual;

spoooff
000