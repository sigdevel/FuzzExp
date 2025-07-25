my $PLATFORM;
my $CCTYPE;
while (@ARGV) {
my $flag = shift;
if ($flag =~ s/^CC_FLAGS=/ /) {
for my $fflag ($flag =~ /(?:^|\s)-D(\S+)/g) {
$fflag     .= '=1' unless $fflag =~ /^(\w+)=/;
$define{$1} = $2   if $fflag =~ /^(\w+)=(.+)$/;
}
next;
}
$define{$1} = 1 if ($flag =~ /^-D(\w+)$/);
$define{$1} = $2 if ($flag =~ /^-D(\w+)=(.+)$/);
$CCTYPE   = $1 if ($flag =~ /^CCTYPE=(\w+)$/);
$PLATFORM = $1 if ($flag =~ /^PLATFORM=(\w+)$/);
if ($PLATFORM eq 'netware') {
$FILETYPE = $1 if ($flag =~ /^FILETYPE=(\w+)$/);
}
}
my @PLATFORM = qw(aix win32 wince os2 MacOS netware);
my %PLATFORM;
@PLATFORM{@PLATFORM} = ();
defined $PLATFORM || die "PLATFORM undefined, must be one of: @PLATFORM\n";
exists $PLATFORM{$PLATFORM} || die "PLATFORM must be one of: @PLATFORM\n";
if ($PLATFORM eq 'win32' or $PLATFORM eq "aix") {
my $config = `$^X -Ilib -V`;
my($options) = $config =~ /^  Compile-time options: (.*?)\n^  \S/ms;
$options =~ s/\s+/ /g;
print STDERR "Options: ($options)\n";
foreach (split /\s+/, $options) {
$define{$_} = 1;
}
}
my %exportperlmalloc =
(
Perl_malloc		=>	"malloc",
Perl_mfree		=>	"free",
Perl_realloc		=>	"realloc",
Perl_calloc		=>	"calloc",
);
my $exportperlmalloc = $PLATFORM eq 'os2';
my $config_sh   = "config.sh";
my $config_h    = "config.h";
my $thrdvar_h   = "thrdvar.h";
my $intrpvar_h  = "intrpvar.h";
my $perlvars_h  = "perlvars.h";
my $global_sym  = "global.sym";
my $pp_sym      = "pp.sym";
my $globvar_sym = "globvar.sym";
my $perlio_sym  = "perlio.sym";
my $static_ext = "";
if ($PLATFORM eq 'aix') {
}
elsif ($PLATFORM =~ /^win(?:32|ce)$/ || $PLATFORM eq 'netware') {
$CCTYPE = "MSVC" unless defined $CCTYPE;
foreach ($thrdvar_h, $intrpvar_h, $perlvars_h, $global_sym,
$pp_sym, $globvar_sym, $perlio_sym) {
s!^!..\\!;
}
}
elsif ($PLATFORM eq 'MacOS') {
foreach ($thrdvar_h, $intrpvar_h, $perlvars_h, $global_sym,
$pp_sym, $globvar_sym, $perlio_sym) {
s!^!::!;
}
}
unless ($PLATFORM eq 'win32' || $PLATFORM eq 'wince' || $PLATFORM eq 'MacOS' || $PLATFORM eq 'netware') {
open(CFG,$config_sh) || die "Cannot open $config_sh: $!\n";
while (<CFG>) {
if (/^(?:ccflags|optimize)='(.+)'$/) {
$_ = $1;
$define{$1} = 1 while /-D(\w+)/g;
}
if ($PLATFORM eq 'os2') {
$CONFIG_ARGS = $1 if /^config_args='(.+)'$/;
$ARCHNAME =    $1 if /^archname='(.+)'$/;
$PATCHLEVEL =  $1 if /^perl_patchlevel='(.+)'$/;
}
}
close(CFG);
}
if ($PLATFORM eq 'win32' || $PLATFORM eq 'wince') {
open(CFG,"<..\\$config_sh") || die "Cannot open ..\\$config_sh: $!\n";
if ((join '', <CFG>) =~ /^static_ext='(.*)'$/m) {
$static_ext = $1;
}
close(CFG);
}
open(CFG,$config_h) || die "Cannot open $config_h: $!\n";
while (<CFG>) {
$define{$1} = 1 if /^\s*
$define{$1} = 1 if /^\s*
$define{$1} = 1 if /^\s*
$define{$1} = 1 if /^\s*
}
close(CFG);
if ($define{PERL_IMPLICIT_SYS}) {
$define{PL_OP_SLAB_ALLOC} = 1;
}
if ($define{USE_ITHREADS}) {
if (!$define{MULTIPLICITY}) {
$define{MULTIPLICITY} = 1;
}
}
$define{PERL_IMPLICIT_CONTEXT} ||=
$define{USE_ITHREADS} ||
$define{USE_5005THREADS}  ||
$define{MULTIPLICITY} ;
if ($define{USE_ITHREADS} && $PLATFORM ne 'win32' && $^O ne 'darwin') {
$define{USE_REENTRANT_API} = 1;
}
my $sym_ord = 0;
print STDERR "Defines: (" . join(' ', sort keys %define) . ")\n";
if ($PLATFORM =~ /^win(?:32|ce)$/) {
($dll = ($define{PERL_DLL} || "perl58")) =~ s/\.dll$//i;
print "LIBRARY $dll\n";
print "DESCRIPTION 'Perl interpreter'\n";
print "EXPORTS\n";
if ($define{PERL_IMPLICIT_SYS}) {
output_symbol("perl_get_host_info");
output_symbol("perl_alloc_override");
}
if ($define{USE_ITHREADS} and $define{PERL_IMPLICIT_SYS}) {
output_symbol("perl_clone_host");
}
}
elsif ($PLATFORM eq 'os2') {
if (open my $fh, '<', 'perl5.def') {
while (<$fh>) {
last if /^\s*EXPORTS\b/;
}
while (<$fh>) {
$ordinal{$1} = $2 if /^\s*"(\w+)"\s*(?:=\s*"\w+"\s*)?\@(\d+)\s*$/;
$sym_ord = $1 if /^\s*;\s*LAST_ORDINAL\s*=\s*(\d+)\s*$/;
}
$sym_ord < $_ and $sym_ord = $_ for values %ordinal;
}
($v = $]) =~ s/(\d\.\d\d\d)(\d\d)$/$1_$2/;
$v .= '-thread' if $ARCHNAME =~ /-thread/;
($dll = $define{PERL_DLL}) =~ s/\.dll$//i;
$v .= "\@$PATCHLEVEL" if $PATCHLEVEL;
$d = "DESCRIPTION '\@
$d = substr($d, 0, 249) . "...'" if length $d > 253;
print <<"---EOP---";
LIBRARY '$dll' INITINSTANCE TERMINSTANCE
$d
STACKSIZE 32768
CODE LOADONCALL
DATA LOADONCALL NONSHARED MULTIPLE
EXPORTS
---EOP---
}
elsif ($PLATFORM eq 'aix') {
$OSVER = `uname -v`;
chop $OSVER;
$OSREL = `uname -r`;
chop $OSREL;
if ($OSVER > 4 || ($OSVER == 4 && $OSREL >= 3)) {
print "
} else {
print "
}
}
elsif ($PLATFORM eq 'netware') {
if ($FILETYPE eq 'def') {
print "LIBRARY perl58\n";
print "DESCRIPTION 'Perl interpreter for NetWare'\n";
print "EXPORTS\n";
}
if ($define{PERL_IMPLICIT_SYS}) {
output_symbol("perl_get_host_info");
output_symbol("perl_alloc_override");
output_symbol("perl_clone_host");
}
}
my %skip;
my %export;
sub skip_symbols {
my $list = shift;
foreach my $symbol (@$list) {
$skip{$symbol} = 1;
}
}
sub emit_symbols {
my $list = shift;
foreach my $symbol (@$list) {
my $skipsym = $symbol;
if ($define{MULTIPLICITY}) {
$skipsym =~ s/^Perl_[GIT](\w+)_ptr$/PL_$1/;
}
emit_symbol($symbol) unless exists $skip{$skipsym};
}
}
if ($PLATFORM eq 'win32') {
skip_symbols [qw(
PL_statusvalue_vms
PL_archpat_auto
PL_cryptseen
PL_DBcv
PL_generation
PL_lastgotoprobe
PL_linestart
PL_modcount
PL_pending_ident
PL_sortcxix
PL_sublex_info
PL_timesbuf
main
Perl_ErrorNo
Perl_GetVars
Perl_do_exec3
Perl_do_ipcctl
Perl_do_ipcget
Perl_do_msgrcv
Perl_do_msgsnd
Perl_do_semop
Perl_do_shmio
Perl_dump_fds
Perl_init_thread_intern
Perl_my_bzero
Perl_my_bcopy
Perl_my_htonl
Perl_my_ntohl
Perl_my_swap
Perl_my_chsize
Perl_same_dirent
Perl_setenv_getix
Perl_unlnk
Perl_watch
Perl_safexcalloc
Perl_safexmalloc
Perl_safexfree
Perl_safexrealloc
Perl_my_memcmp
Perl_my_memset
PL_cshlen
PL_cshname
PL_opsave
Perl_do_exec
Perl_getenv_len
Perl_my_pclose
Perl_my_popen
Perl_my_sprintf
)];
}
else {
skip_symbols [qw(
Perl_do_spawn
Perl_do_spawn_nowait
Perl_do_aspawn
)];
}
if ($PLATFORM eq 'wince') {
skip_symbols [qw(
PL_statusvalue_vms
PL_archpat_auto
PL_cryptseen
PL_DBcv
PL_generation
PL_lastgotoprobe
PL_linestart
PL_modcount
PL_pending_ident
PL_sortcxix
PL_sublex_info
PL_timesbuf
PL_collation_ix
PL_collation_name
PL_collation_standard
PL_collxfrm_base
PL_collxfrm_mult
PL_numeric_compat1
PL_numeric_local
PL_numeric_name
PL_numeric_radix_sv
PL_numeric_standard
PL_vtbl_collxfrm
Perl_sv_collxfrm
setgid
setuid
win32_free_childdir
win32_free_childenv
win32_get_childdir
win32_get_childenv
win32_spawnvp
main
Perl_ErrorNo
Perl_GetVars
Perl_do_exec3
Perl_do_ipcctl
Perl_do_ipcget
Perl_do_msgrcv
Perl_do_msgsnd
Perl_do_semop
Perl_do_shmio
Perl_dump_fds
Perl_init_thread_intern
Perl_my_bzero
Perl_my_bcopy
Perl_my_htonl
Perl_my_ntohl
Perl_my_swap
Perl_my_chsize
Perl_same_dirent
Perl_setenv_getix
Perl_unlnk
Perl_watch
Perl_safexcalloc
Perl_safexmalloc
Perl_safexfree
Perl_safexrealloc
Perl_my_memcmp
Perl_my_memset
PL_cshlen
PL_cshname
PL_opsave
Perl_do_exec
Perl_getenv_len
Perl_my_pclose
Perl_my_popen
Perl_my_sprintf
)];
}
elsif ($PLATFORM eq 'aix') {
skip_symbols([qw(
Perl_dump_fds
Perl_ErrorNo
Perl_GetVars
Perl_my_bcopy
Perl_my_bzero
Perl_my_chsize
Perl_my_htonl
Perl_my_memcmp
Perl_my_memset
Perl_my_ntohl
Perl_my_swap
Perl_safexcalloc
Perl_safexfree
Perl_safexmalloc
Perl_safexrealloc
Perl_same_dirent
Perl_unlnk
Perl_sys_intern_clear
Perl_sys_intern_dup
Perl_sys_intern_init
PL_cryptseen
PL_opsave
PL_statusvalue_vms
PL_sys_intern
)]);
}
elsif ($PLATFORM eq 'os2') {
emit_symbols([qw(
ctermid
get_sysinfo
Perl_OS2_init
Perl_OS2_init3
Perl_OS2_term
OS2_Perl_data
dlopen
dlsym
dlerror
dlclose
dup2
dup
my_tmpfile
my_tmpnam
my_flock
my_rmdir
my_mkdir
my_getpwuid
my_getpwnam
my_getpwent
my_setpwent
my_endpwent
fork_with_resources
croak_with_os2error
setgrent
endgrent
getgrent
malloc_mutex
threads_mutex
nthreads
nthreads_cond
os2_cond_wait
os2_stat
os2_execname
async_mssleep
msCounter
InfoTable
pthread_join
pthread_create
pthread_detach
XS_Cwd_change_drive
XS_Cwd_current_drive
XS_Cwd_extLibpath
XS_Cwd_extLibpath_set
XS_Cwd_sys_abspath
XS_Cwd_sys_chdir
XS_Cwd_sys_cwd
XS_Cwd_sys_is_absolute
XS_Cwd_sys_is_relative
XS_Cwd_sys_is_rooted
XS_DynaLoader_mod2fname
XS_File__Copy_syscopy
Perl_Register_MQ
Perl_Deregister_MQ
Perl_Serve_Messages
Perl_Process_Messages
init_PMWIN_entries
PMWIN_entries
Perl_hab_GET
loadByOrdinal
pExtFCN
os2error
ResetWinError
CroakWinError
PL_do_undump
)]);
emit_symbols([qw(os2_cond_wait
pthread_join
pthread_create
pthread_detach
)])
if $define{'USE_5005THREADS'} or $define{'USE_ITHREADS'};
}
elsif ($PLATFORM eq 'MacOS') {
skip_symbols [qw(
Perl_GetVars
PL_cryptseen
PL_cshlen
PL_cshname
PL_statusvalue_vms
PL_sys_intern
PL_opsave
PL_timesbuf
Perl_dump_fds
Perl_my_bcopy
Perl_my_bzero
Perl_my_chsize
Perl_my_htonl
Perl_my_memcmp
Perl_my_memset
Perl_my_ntohl
Perl_my_swap
Perl_safexcalloc
Perl_safexfree
Perl_safexmalloc
Perl_safexrealloc
Perl_unlnk
Perl_sys_intern_clear
Perl_sys_intern_init
)];
}
elsif ($PLATFORM eq 'netware') {
skip_symbols [qw(
PL_statusvalue_vms
PL_archpat_auto
PL_cryptseen
PL_DBcv
PL_generation
PL_lastgotoprobe
PL_linestart
PL_modcount
PL_pending_ident
PL_sortcxix
PL_sublex_info
PL_timesbuf
main
Perl_ErrorNo
Perl_GetVars
Perl_do_exec3
Perl_do_ipcctl
Perl_do_ipcget
Perl_do_msgrcv
Perl_do_msgsnd
Perl_do_semop
Perl_do_shmio
Perl_dump_fds
Perl_init_thread_intern
Perl_my_bzero
Perl_my_htonl
Perl_my_ntohl
Perl_my_swap
Perl_my_chsize
Perl_same_dirent
Perl_setenv_getix
Perl_unlnk
Perl_watch
Perl_safexcalloc
Perl_safexmalloc
Perl_safexfree
Perl_safexrealloc
Perl_my_memcmp
Perl_my_memset
PL_cshlen
PL_cshname
PL_opsave
Perl_do_exec
Perl_getenv_len
Perl_my_pclose
Perl_my_popen
Perl_sys_intern_init
Perl_sys_intern_dup
Perl_sys_intern_clear
Perl_my_bcopy
Perl_PerlIO_write
Perl_PerlIO_unread
Perl_PerlIO_tell
Perl_PerlIO_stdout
Perl_PerlIO_stdin
Perl_PerlIO_stderr
Perl_PerlIO_setlinebuf
Perl_PerlIO_set_ptrcnt
Perl_PerlIO_set_cnt
Perl_PerlIO_seek
Perl_PerlIO_read
Perl_PerlIO_get_ptr
Perl_PerlIO_get_cnt
Perl_PerlIO_get_bufsiz
Perl_PerlIO_get_base
Perl_PerlIO_flush
Perl_PerlIO_fill
Perl_PerlIO_fileno
Perl_PerlIO_error
Perl_PerlIO_eof
Perl_PerlIO_close
Perl_PerlIO_clearerr
PerlIO_perlio
)];
}
unless ($define{'DEBUGGING'}) {
skip_symbols [qw(
Perl_deb_growlevel
Perl_debop
Perl_debprofdump
Perl_debstack
Perl_debstackptrs
Perl_sv_peek
PL_block_type
PL_watchaddr
PL_watchok
)];
}
if ($define{'PERL_IMPLICIT_SYS'}) {
skip_symbols [qw(
Perl_getenv_len
Perl_my_popen
Perl_my_pclose
)];
}
else {
skip_symbols [qw(
PL_Mem
PL_MemShared
PL_MemParse
PL_Env
PL_StdIO
PL_LIO
PL_Dir
PL_Sock
PL_Proc
)];
}
unless ($define{'PERL_FLEXIBLE_EXCEPTIONS'}) {
skip_symbols [qw(
PL_protect
Perl_default_protect
Perl_vdefault_protect
)];
}
unless ($define{'USE_REENTRANT_API'}) {
skip_symbols [qw(
PL_reentrant_buffer
)];
}
if ($define{'MYMALLOC'}) {
emit_symbols [qw(
Perl_dump_mstats
Perl_get_mstats
Perl_strdup
Perl_putenv
MallocCfg_ptr
MallocCfgP_ptr
)];
if ($define{'USE_5005THREADS'} || $define{'USE_ITHREADS'}) {
emit_symbols [qw(
PL_malloc_mutex
)];
}
else {
skip_symbols [qw(
PL_malloc_mutex
)];
}
}
else {
skip_symbols [qw(
PL_malloc_mutex
Perl_dump_mstats
Perl_get_mstats
Perl_malloced_size
MallocCfg_ptr
MallocCfgP_ptr
)];
}
if ($define{'PERL_USE_SAFE_PUTENV'}) {
skip_symbols [qw(
PL_use_safe_putenv
)];
}
unless ($define{'USE_5005THREADS'} || $define{'USE_ITHREADS'}) {
skip_symbols [qw(
PL_thr_key
)];
}
unless ($define{'USE_5005THREADS'}) {
skip_symbols [qw(
PL_sv_mutex
PL_strtab_mutex
PL_svref_mutex
PL_cred_mutex
PL_eval_mutex
PL_fdpid_mutex
PL_sv_lock_mutex
PL_eval_cond
PL_eval_owner
PL_threads_mutex
PL_nthreads
PL_nthreads_cond
PL_threadnum
PL_threadsv_names
PL_thrsv
PL_vtbl_mutex
Perl_condpair_magic
Perl_new_struct_thread
Perl_per_thread_magicals
Perl_thread_create
Perl_find_threadsv
Perl_unlock_condpair
Perl_magic_mutexfree
Perl_sv_lock
)];
}
unless ($define{'USE_ITHREADS'}) {
skip_symbols [qw(
PL_ptr_table
PL_pte_root
PL_pte_arenaroot
PL_op_mutex
PL_regex_pad
PL_regex_padav
PL_sharedsv_space
PL_sharedsv_space_mutex
PL_dollarzero_mutex
Perl_dirp_dup
Perl_cx_dup
Perl_si_dup
Perl_any_dup
Perl_ss_dup
Perl_fp_dup
Perl_gp_dup
Perl_he_dup
Perl_mg_dup
Perl_re_dup
Perl_sv_dup
Perl_rvpv_dup
Perl_sys_intern_dup
Perl_ptr_table_clear
Perl_ptr_table_fetch
Perl_ptr_table_free
Perl_ptr_table_new
Perl_ptr_table_clear
Perl_ptr_table_free
Perl_ptr_table_split
Perl_ptr_table_store
perl_clone
perl_clone_using
Perl_sharedsv_find
Perl_sharedsv_init
Perl_sharedsv_lock
Perl_sharedsv_new
Perl_sharedsv_thrcnt_dec
Perl_sharedsv_thrcnt_inc
Perl_sharedsv_unlock
Perl_stashpv_hvname_match
)];
}
unless ($define{'PERL_IMPLICIT_CONTEXT'}) {
skip_symbols [qw(
Perl_croak_nocontext
Perl_die_nocontext
Perl_deb_nocontext
Perl_form_nocontext
Perl_load_module_nocontext
Perl_mess_nocontext
Perl_warn_nocontext
Perl_warner_nocontext
Perl_newSVpvf_nocontext
Perl_sv_catpvf_nocontext
Perl_sv_setpvf_nocontext
Perl_sv_catpvf_mg_nocontext
Perl_sv_setpvf_mg_nocontext
)];
}
unless ($define{'PERL_IMPLICIT_SYS'}) {
skip_symbols [qw(
perl_alloc_using
perl_clone_using
)];
}
unless ($define{'FAKE_THREADS'}) {
skip_symbols [qw(PL_curthr)];
}
unless ($define{'PL_OP_SLAB_ALLOC'}) {
skip_symbols [qw(
PL_OpPtr
PL_OpSlab
PL_OpSpace
Perl_Slab_Alloc
Perl_Slab_Free
)];
}
unless ($define{'THREADS_HAVE_PIDS'}) {
skip_symbols [qw(PL_ppid)];
}
unless ($define{'DEBUG_LEAKING_SCALARS_FORK_DUMP'}) {
skip_symbols [qw(
PL_dumper_fd
)];
}
unless ($define{'PERL_DONT_CREATE_GVSV'}) {
skip_symbols [qw(
Perl_gv_SVadd
)];
}
sub readvar {
my $file = shift;
my $proc = shift || sub { "PL_$_[2]" };
open(VARS,$file) || die "Cannot open $file: $!\n";
my @syms;
while (<VARS>) {
push(@syms, &$proc($1,$2,$3)) if (/\bPERLVAR(A?I?C?)\(([IGT])(\w+)/);
}
close(VARS);
return \@syms;
}
if ($define{'USE_5005THREADS'}) {
my $thrd = readvar($thrdvar_h);
skip_symbols $thrd;
}
if ($define{'PERL_GLOBAL_STRUCT'}) {
my $global = readvar($perlvars_h);
skip_symbols $global;
emit_symbol('Perl_GetVars');
emit_symbols [qw(PL_Vars PL_VarsPtr)] unless $CCTYPE eq 'GCC';
}
my @syms = ($global_sym, $globvar_sym);
my @layer_syms = qw(
PerlIOBase_binmode
PerlIOBase_clearerr
PerlIOBase_close
PerlIOBase_dup
PerlIOBase_eof
PerlIOBase_error
PerlIOBase_fileno
PerlIOBase_noop_fail
PerlIOBase_noop_ok
PerlIOBase_popped
PerlIOBase_pushed
PerlIOBase_read
PerlIOBase_setlinebuf
PerlIOBase_unread
PerlIOBuf_bufsiz
PerlIOBuf_close
PerlIOBuf_dup
PerlIOBuf_fill
PerlIOBuf_flush
PerlIOBuf_get_base
PerlIOBuf_get_cnt
PerlIOBuf_get_ptr
PerlIOBuf_open
PerlIOBuf_popped
PerlIOBuf_pushed
PerlIOBuf_read
PerlIOBuf_seek
PerlIOBuf_set_ptrcnt
PerlIOBuf_tell
PerlIOBuf_unread
PerlIOBuf_write
PerlIO_allocate
PerlIO_apply_layera
PerlIO_apply_layers
PerlIO_arg_fetch
PerlIO_debug
PerlIO_define_layer
PerlIO_isutf8
PerlIO_layer_fetch
PerlIO_list_free
PerlIO_modestr
PerlIO_parse_layers
PerlIO_pending
PerlIO_perlio
PerlIO_pop
PerlIO_push
PerlIO_sv_dup
Perl_PerlIO_clearerr
Perl_PerlIO_close
Perl_PerlIO_eof
Perl_PerlIO_error
Perl_PerlIO_fileno
Perl_PerlIO_fill
Perl_PerlIO_flush
Perl_PerlIO_get_base
Perl_PerlIO_get_bufsiz
Perl_PerlIO_get_cnt
Perl_PerlIO_get_ptr
Perl_PerlIO_read
Perl_PerlIO_seek
Perl_PerlIO_set_cnt
Perl_PerlIO_set_ptrcnt
Perl_PerlIO_setlinebuf
Perl_PerlIO_stderr
Perl_PerlIO_stdin
Perl_PerlIO_stdout
Perl_PerlIO_tell
Perl_PerlIO_unread
Perl_PerlIO_write
);
if ($PLATFORM eq 'netware') {
push(@layer_syms,'PL_def_layerlist','PL_known_layers','PL_perlio');
}
if ($define{'USE_PERLIO'}) {
push @syms, $perlio_sym;
if ($define{'USE_SFIO'}) {
skip_symbols \@layer_syms;
skip_symbols [qw(perlsio_binmode)];
skip_symbols [qw(
PerlIO_canset_cnt
PerlIO_clearerr
PerlIO_close
PerlIO_eof
PerlIO_error
PerlIO_exportFILE
PerlIO_fast_gets
PerlIO_fdopen
PerlIO_fileno
PerlIO_findFILE
PerlIO_flush
PerlIO_get_base
PerlIO_get_bufsiz
PerlIO_get_cnt
PerlIO_get_ptr
PerlIO_getc
PerlIO_getname
PerlIO_has_base
PerlIO_has_cntptr
PerlIO_importFILE
PerlIO_open
PerlIO_printf
PerlIO_putc
PerlIO_puts
PerlIO_read
PerlIO_releaseFILE
PerlIO_reopen
PerlIO_rewind
PerlIO_seek
PerlIO_set_cnt
PerlIO_set_ptrcnt
PerlIO_setlinebuf
PerlIO_sprintf
PerlIO_stderr
PerlIO_stdin
PerlIO_stdout
PerlIO_stdoutf
PerlIO_tell
PerlIO_ungetc
PerlIO_vprintf
PerlIO_write
PerlIO_perlio
Perl_PerlIO_clearerr
Perl_PerlIO_close
Perl_PerlIO_eof
Perl_PerlIO_error
Perl_PerlIO_fileno
Perl_PerlIO_fill
Perl_PerlIO_flush
Perl_PerlIO_get_base
Perl_PerlIO_get_bufsiz
Perl_PerlIO_get_cnt
Perl_PerlIO_get_ptr
Perl_PerlIO_read
Perl_PerlIO_seek
Perl_PerlIO_set_cnt
Perl_PerlIO_set_ptrcnt
Perl_PerlIO_setlinebuf
Perl_PerlIO_stderr
Perl_PerlIO_stdin
Perl_PerlIO_stdout
Perl_PerlIO_tell
Perl_PerlIO_unread
Perl_PerlIO_write
PL_def_layerlist
PL_known_layers
PL_perlio
)];
}
else {
emit_symbols \@layer_syms;
emit_symbols [qw(perlsio_binmode)];
}
} else {
skip_symbols \@layer_syms;
skip_symbols [qw(perlsio_binmode)];
skip_symbols [qw(PL_def_layerlist PL_known_layers PL_perlio)];
}
for my $syms (@syms) {
open (GLOBAL, "<$syms") || die "failed to open $syms: $!\n";
while (<GLOBAL>) {
next if (!/^[A-Za-z]/);
chomp($_);
my $symbol = ($syms =~ /var\.sym$/i ? "PL_" : "");
$symbol .= $_;
emit_symbol($symbol) unless exists $skip{$symbol};
}
close(GLOBAL);
}
if ($define{'MULTIPLICITY'}) {
for my $f ($perlvars_h, $intrpvar_h, $thrdvar_h) {
my $glob = readvar($f, sub { "Perl_" . $_[1] . $_[2] . "_ptr" });
emit_symbols $glob;
}
if ($PLATFORM eq 'aix' or $PLATFORM eq 'os2') {
my $glob = readvar($perlvars_h);
emit_symbols $glob;
}
}
else {
unless ($define{'PERL_GLOBAL_STRUCT'}) {
my $glob = readvar($perlvars_h);
emit_symbols $glob;
}
unless ($define{'MULTIPLICITY'}) {
my $glob = readvar($intrpvar_h);
emit_symbols $glob;
}
unless ($define{'MULTIPLICITY'} || $define{'USE_5005THREADS'}) {
my $glob = readvar($thrdvar_h);
emit_symbols $glob;
}
}
sub try_symbol {
my $symbol = shift;
return if $symbol !~ /^[A-Za-z_]/;
return if $symbol =~ /^\
$symbol =~s/\r//g;
chomp($symbol);
return if exists $skip{$symbol};
emit_symbol($symbol);
}
while (<DATA>) {
try_symbol($_);
}
if ($PLATFORM =~ /^win(?:32|ce)$/) {
foreach my $symbol (qw(
setuid
setgid
boot_DynaLoader
Perl_init_os_extras
Perl_thread_create
Perl_win32_init
Perl_win32_term
RunPerl
win32_async_check
win32_errno
win32_environ
win32_abort
win32_fstat
win32_stat
win32_pipe
win32_popen
win32_pclose
win32_rename
win32_setmode
win32_chsize
win32_lseek
win32_tell
win32_dup
win32_dup2
win32_open
win32_close
win32_eof
win32_read
win32_write
win32_spawnvp
win32_mkdir
win32_rmdir
win32_chdir
win32_flock
win32_execv
win32_execvp
win32_htons
win32_ntohs
win32_htonl
win32_ntohl
win32_inet_addr
win32_inet_ntoa
win32_socket
win32_bind
win32_listen
win32_accept
win32_connect
win32_send
win32_sendto
win32_recv
win32_recvfrom
win32_shutdown
win32_closesocket
win32_ioctlsocket
win32_setsockopt
win32_getsockopt
win32_getpeername
win32_getsockname
win32_gethostname
win32_gethostbyname
win32_gethostbyaddr
win32_getprotobyname
win32_getprotobynumber
win32_getservbyname
win32_getservbyport
win32_select
win32_endhostent
win32_endnetent
win32_endprotoent
win32_endservent
win32_getnetent
win32_getnetbyname
win32_getnetbyaddr
win32_getprotoent
win32_getservent
win32_sethostent
win32_setnetent
win32_setprotoent
win32_setservent
win32_getenv
win32_putenv
win32_perror
win32_malloc
win32_calloc
win32_realloc
win32_free
win32_sleep
win32_times
win32_access
win32_alarm
win32_chmod
win32_open_osfhandle
win32_get_osfhandle
win32_ioctl
win32_link
win32_unlink
win32_utime
win32_gettimeofday
win32_uname
win32_wait
win32_waitpid
win32_kill
win32_str_os_error
win32_opendir
win32_readdir
win32_telldir
win32_seekdir
win32_rewinddir
win32_closedir
win32_longpath
win32_os_id
win32_getpid
win32_crypt
win32_dynaload
win32_get_childenv
win32_free_childenv
win32_clearenv
win32_get_childdir
win32_free_childdir
win32_stdin
win32_stdout
win32_stderr
win32_ferror
win32_feof
win32_strerror
win32_fprintf
win32_printf
win32_vfprintf
win32_vprintf
win32_fread
win32_fwrite
win32_fopen
win32_fdopen
win32_freopen
win32_fclose
win32_fputs
win32_fputc
win32_ungetc
win32_getc
win32_fileno
win32_clearerr
win32_fflush
win32_ftell
win32_fseek
win32_fgetpos
win32_fsetpos
win32_rewind
win32_tmpfile
win32_setbuf
win32_setvbuf
win32_flushall
win32_fcloseall
win32_fgets
win32_gets
win32_fgetc
win32_putc
win32_puts
win32_getchar
win32_putchar
))
{
try_symbol($symbol);
}
if ($CCTYPE eq "BORLAND") {
try_symbol('_matherr');
}
}
elsif ($PLATFORM eq 'os2') {
open MAP, 'miniperl.map' or die 'Cannot read miniperl.map';
/^\s*[\da-f:]+\s+(\w+)/i and $mapped{$1}++ foreach <MAP>;
close MAP or die 'Cannot close miniperl.map';
@missing = grep { !exists $mapped{$_} }
keys %export;
@missing = grep { !exists $exportperlmalloc{$_} } @missing;
delete $export{$_} foreach @missing;
}
elsif ($PLATFORM eq 'MacOS') {
open MACSYMS, 'macperl.sym' or die 'Cannot read macperl.sym';
while (<MACSYMS>) {
try_symbol($_);
}
close MACSYMS;
}
elsif ($PLATFORM eq 'netware') {
foreach my $symbol (qw(
boot_DynaLoader
Perl_init_os_extras
Perl_thread_create
Perl_nw5_init
RunPerl
AllocStdPerl
FreeStdPerl
do_spawn2
do_aspawn
nw_uname
nw_stdin
nw_stdout
nw_stderr
nw_feof
nw_ferror
nw_fopen
nw_fclose
nw_clearerr
nw_getc
nw_fgets
nw_fputc
nw_fputs
nw_fflush
nw_ungetc
nw_fileno
nw_fdopen
nw_freopen
nw_fread
nw_fwrite
nw_setbuf
nw_setvbuf
nw_vfprintf
nw_ftell
nw_fseek
nw_rewind
nw_tmpfile
nw_fgetpos
nw_fsetpos
nw_dup
nw_access
nw_chmod
nw_chsize
nw_close
nw_dup2
nw_flock
nw_isatty
nw_link
nw_lseek
nw_stat
nw_mktemp
nw_open
nw_read
nw_rename
nw_setmode
nw_unlink
nw_utime
nw_write
nw_chdir
nw_rmdir
nw_closedir
nw_opendir
nw_readdir
nw_rewinddir
nw_seekdir
nw_telldir
nw_htonl
nw_htons
nw_ntohl
nw_ntohs
nw_accept
nw_bind
nw_connect
nw_endhostent
nw_endnetent
nw_endprotoent
nw_endservent
nw_gethostbyaddr
nw_gethostbyname
nw_gethostent
nw_gethostname
nw_getnetbyaddr
nw_getnetbyname
nw_getnetent
nw_getpeername
nw_getprotobyname
nw_getprotobynumber
nw_getprotoent
nw_getservbyname
nw_getservbyport
nw_getservent
nw_getsockname
nw_getsockopt
nw_inet_addr
nw_listen
nw_socket
nw_recv
nw_recvfrom
nw_select
nw_send
nw_sendto
nw_sethostent
nw_setnetent
nw_setprotoent
nw_setservent
nw_setsockopt
nw_inet_ntoa
nw_shutdown
nw_crypt
nw_execvp
nw_kill
nw_Popen
nw_Pclose
nw_Pipe
nw_times
nw_waitpid
nw_getpid
nw_spawnvp
nw_os_id
nw_open_osfhandle
nw_get_osfhandle
nw_abort
nw_sleep
nw_wait
nw_dynaload
nw_strerror
fnFpSetMode
fnInsertHashListAddrs
fnGetHashListAddrs
Perl_deb
Perl_sv_setsv
Perl_sv_catsv
Perl_sv_catpvn
Perl_sv_2pv
nw_freeenviron
Remove_Thread_Ctx
))
{
try_symbol($symbol);
}
}
$static_ext =~ s/\//__/g;
$static_ext =~ s/\bDynaLoader\b//;
my @stat_mods = map {"boot_$_"} grep {/\S/} split /\s+/, $static_ext;
foreach my $symbol (@stat_mods)
{
try_symbol($symbol);
}
foreach my $symbol (sort keys %export) {
output_symbol($symbol);
}
if ($PLATFORM eq 'os2') {
print <<EOP;
dll_perlmain=main
fill_extLibpath
dir_subst
Perl_OS2_handler_install
; LAST_ORDINAL=$sym_ord
EOP
}
sub emit_symbol {
my $symbol = shift;
chomp($symbol);
$export{$symbol} = 1;
}
sub output_symbol {
my $symbol = shift;
if ($PLATFORM =~ /^win(?:32|ce)$/) {
$symbol = "_$symbol" if $CCTYPE eq 'BORLAND';
print "\t$symbol\n";
}
elsif ($PLATFORM eq 'os2') {
printf qq(    %-31s \@%s\n),
qq("$symbol"), $ordinal{$symbol} || ++$sym_ord;
printf qq(    %-31s \@%s\n),
qq("$exportperlmalloc{$symbol}" = "$symbol"),
$ordinal{$exportperlmalloc{$symbol}} || ++$sym_ord
if $exportperlmalloc and exists $exportperlmalloc{$symbol};
}
elsif ($PLATFORM eq 'aix' || $PLATFORM eq 'MacOS') {
print "$symbol\n";
}
elsif ($PLATFORM eq 'netware') {
print "\t$symbol,\n";
}
}
1;
__DATA__
Perl_cxinc
perl_alloc
perl_alloc_using
perl_clone
perl_clone_using
perl_construct
perl_destruct
perl_free
perl_parse
perl_run
PerlIO_binmode
PerlIO_getpos
PerlIO_init
PerlIO_setpos
PerlIO_sprintf
PerlIO_sv_dup
PerlIO_tmpfile
PerlIO_vsprintf
