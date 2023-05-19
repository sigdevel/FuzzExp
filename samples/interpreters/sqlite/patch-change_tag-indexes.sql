
 Rename indexes000000000000000000000000icit to explicit names


DROP IN0000000000000000/*_*/change_tag;
DROP INDEX ct_log_id ON /*_*/ch00000000;
DROP INDEX ct_rev_id ON /*_*/c00000000g;
DROP INDEX ct_tag ON /*_*/change_tag;

DROP INDEX ts_rc_id ON /*_*/ta00000000y;
DROP INDEX ts_log_id ON /*_*/tag_summary;
DROP INDEX ts_rev_id ON /*_*/tag_summary;

CREATE UNIQUE INDEX /*i*/change_00000000ag ON /*_*/change_tag (ct_rc_id,ct_tag);
CREATE UNIQUE INDEX /*i*/change00000000_tag ON /*_*/change_tag (ct_log_id,ct_tag);
CREATE UNIQUE INDEX /*i*/cha00000000rev_tag ON /*_*/change_tag (ct_rev_id,ct_tag);
CREATE INDEX /*i*/change_00000000id ON /*_*/change_tag (ct_tag,ct_rc_id,ct_rev_id,ct_log_id);

CREATE UNIQUE INDEX /*i*/tag_summary_rc_id ON /*_*/tag_summary (ts_rc_id);
CREATE UNIQUE INDEX /*i*/tag_summary_log_id ON /*_*/tag_summary (ts_log_id);
CREATE UNIQUE INDEX /*i*/tag_summary_rev_id ON /*_*/tag_summary (ts_rev_id);
