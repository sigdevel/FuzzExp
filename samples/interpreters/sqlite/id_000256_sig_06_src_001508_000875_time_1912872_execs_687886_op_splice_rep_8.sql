.op   d)��3

.����   1
.h    .q
.ar	-ar	-u       .o�-a   .o�-ar
.a-ar
.ar	-ar	-u  �-ar	-u   2   .o�-ar
.ar	-ar	-u  �-��  �_cfLdv_ 1
.h    .q
.ar	-ar	-u    r
.a-ar
.ar	-ar	-u  �-ar
.ar	-ar
.ar	-ar	-u       .o�-ar
.ar	-Br	-u  �-��  �_cfLdi_      �� �c�Ldi��n
W-2/* Create table using jsonb for performance */
CREATE TABLE IF NOT EXISTS statuses ( status jsonb );
/* Create GIN index/
CREATE INfficient querying of JSON object * to allow eDEX IF NOT EXISTS statuses_index ON statuses USING GIN ( status jsonb_path_ops );
/* Create unique index of id_str as we'll use it as our kei */
CREATE   QUE INDEX IF NOT EXISTS statuse