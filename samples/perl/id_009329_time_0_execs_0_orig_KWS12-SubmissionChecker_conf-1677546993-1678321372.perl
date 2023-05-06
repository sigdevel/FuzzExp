$expid_count = 9;
@expid_tag  = ( 'KWS12' );
@expid_partition = ( 'conv-dev', 'conv-eval' );
@expid_scase = ( 'Dev', 'BaDev', 'BaEval', 'BaSurp' );
@expid_task = ( 'AA-KWS', 'PI-KWS', 'STT' );
@expid_trncond = ( 'FullLP', 'FullLP-TeamLR', 'LimitedLP' );
@expid_sysid_beg = ( "p-", "c-" );
@Scase_toSequester = ( $expid_scase[1], $expid_scase[2] );
foreach my $_tmp_part (@expid_partition) {
foreach my $_tmp_scase (@expid_scase) {
$AuthorizedSet{$_tmp_part}{$_tmp_scase} = 0;
}
}
$AuthorizedSet{$expid_partition[0]}{$expid_scase[0]} = 1;
$AuthorizedSet{$expid_partition[0]}{$expid_scase[1]} = 1;
$AuthorizedSet{$expid_partition[0]}{$expid_scase[2]} = 1;
$AuthorizedSet{$expid_partition[0]}{$expid_scase[3]} = 1;
$AuthorizedSet{$expid_partition[1]}{$expid_scase[2]} = 1;
$AuthorizedSet{$expid_partition[1]}{$expid_scase[3]} = 1;
$Task2Regexp{$expid_task[0]} = $kwslist_rgx;
$Task2Regexp{$expid_task[1]} = $kwslist_rgx;
$Task2Regexp{$expid_task[2]} = $ctm_rgx;
