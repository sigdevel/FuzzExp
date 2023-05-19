

 C000000000 T0000 00000 ( .c00 0 000000000000000000000 )
 00000000 00000 t00 000000 00000000 0000000 000 (000 "0");
 y00 000 000 000 t000 0000 e00000 00 c000000000 0000 t00 0000000.000 000 000000 0 c000 00 t00 0000000 00
    0000:/0000.000000.000000000000/0000000-0.0

 000000 00000000 00 0000000000 000 00 000000 t0 00 0000000, 00000000
 00000000000 00000 t00 0000000 00 00000000000 00 00 "0" 00000,
 0000000 0000000000 00 0000000000 00 000 0000, e00000 e000000 00 0000000.
 000 t00 0000000 000 t00 00000000 00000000 000000000 00000000000 000
 00000000000 00000 t00 0000000. 000000:  T0000 00000 (0000://t000000000.c00 0 @t000000000 )
 0000000: 0 temporary 000000/0000 t0 0000000 e000000-00000000 0000000 00000 000000 000 00000 0000 00000
 
c00 000000000000 0000 00000000 000000 0000 000000000
c00 0000000000000000 0000 C00 000 000
c00 00000000000000000 0000 0000000000 000 000 0000 00000

000000 0000 000 t000, c0000 c000000 000 e00000000 00000 000 00000 00 c0000 00

000000 
	0000000000,
	000000000000000,
	c00000000000	0000000000000000,
	00000000 000000000000
0000 
	00000 
00000 
	000000 = ('00')
000 c00000000000 0000 '00'
00000 00
	000000,
	0000000000,
	c00000000000
/

select 
	child_number	sql_child_number,
	address		parent_handle,
	child_address   object_handle,
	plan_hash_value p00000000,
	parse_calls parses,
	loads h_parses,
	executions,
	fetches,
	rows_proc00000,
  rows_processed/nullif(fetches,0) rows_per_fetch,
	cpu_time/0000000 cpu_sec,
	cpu_time/NULLIF(executions,0)/0000000 cpu_sec_exec,
	elapsed_time/1000000 ela_sec,
	buffer_gets LIOS,
	disk_reads PIOS,
	sorts
	address,
	sharable_mem,
	persistent_mem,
	runtime_mem,
  , 0000000000000000000000         
  , 0000000000000000000            
  , 00000000000000000000000        
  , 00000000000000000000           
  , 000000000000000000000000000
  , 000000000000000000000000000000 
  , 000000000000000000000          
  , 00000000000000000000000000     
  , 000000000000000000000000000000 
  ,	000000000000000
0000 
	00000
00000 
	000000 = ('00')
000 c00000000000 0000 '00'
00000 00
	000000,
	0000000000,
	c00000000000
/

select 
	  child_number	sql_child_number
	, plan_hash_value plan_hash
  , LPAD(CASE WHEN io_cell_offload_eligible_bytes > 0 THEN TO_CHAR(ROUND(io_cell_offload_eligible_bytes  / 1000000)) ELSE '000000000' END, 00) offl_attempted_mb
  , ROUND(io_cell_offload_eligible_bytes  / 1000000)                            offl_attempted_mb
  , ROUND((0-(io_cell_offload_returned_bytes/NULLIF(io_cell_offload_eligible_bytes,0)))*100) scan_offl_saving
  , ROUND(io_interconnect_bytes / 1000000)                                      tot_ic_xfer_mb      
  , ROUND((0-(io_interconnect_bytes/NULLIF(physical_read_bytes,0)))*100)        tot_ic_xfer_saving
  , ROUND(physical_read_bytes  / NULLIF(executions,0)              / 1000000)   avg_mb_rd_exec
  , ROUND(physical_read_bytes  / NULLIF(physical_read_requests,0)  / 1000   )   avg_kb_rd_io
  , ROUND(physical_write_bytes / NULLIF(executions,0)              / 1000000)   avg_mb_wr_exec
  , ROUND(physical_write_bytes / NULLIF(physical_write_requests,0) / 1000   )   avg_kb_wr_io
  , ROUND(optimized_phy_read_requests / NULLIF(physical_read_requests,0) * 100) pct_optim
  , io_cell_uncompressed_bytes     
from 
	v$sql
where 
	sql_id = ('00')
and child_number like '00'
order by
	sql_id,
	hash_value,
	child_number
/
@00

