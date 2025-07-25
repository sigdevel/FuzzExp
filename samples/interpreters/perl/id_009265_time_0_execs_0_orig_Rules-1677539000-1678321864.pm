package FML::Merge::FML4::Rules;
sub translate
{
my ($self, $dispatch, $config, $diff, $key, $value) = @_;
my $fp_rule_convert             = $dispatch->{ rule_convert };
my $fp_rule_prefer_fml4_value   = $dispatch->{ rule_prefer_fml4_value };
my $fp_rule_prefer_fml8_value   = $dispatch->{ rule_prefer_fml8_value };
my $fp_rule_ignore              = $dispatch->{ rule_ignore };
my $fp_rule_not_yet_implemented = $dispatch->{ rule_not_yet_implemented };
my $s = undef;
$s = undef;
if (($key eq 'CFVersion' && $diff->{ CFVersion })) {
if ($config->{ CFVersion }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'debug' && $diff->{ debug })) {
if ($config->{ debug } >= 1) {
$s .= sprintf("use_debug = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'debug' && $diff->{ debug })) {
if ($config->{ debug } == 0) {
$s .= sprintf("use_debug = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LANGUAGE' && $diff->{ LANGUAGE })) {
if ($config->{ LANGUAGE } eq 'Japanese') {
$s .= sprintf("language_preference_order = ja en", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LANGUAGE' && $diff->{ LANGUAGE })) {
if ($config->{ LANGUAGE } eq 'English') {
$s .= sprintf("language_preference_order = en ja", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MESSAGE_LANGUAGE' && $diff->{ MESSAGE_LANGUAGE })) {
if ($config->{ MESSAGE_LANGUAGE } eq 'Japanese') {
$s .= sprintf("language_preference_order = ja en", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MESSAGE_LANGUAGE' && $diff->{ MESSAGE_LANGUAGE })) {
if ($config->{ MESSAGE_LANGUAGE } eq 'English') {
$s .= sprintf("language_preference_order = en ja", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DOMAINNAME' && $diff->{ DOMAINNAME })) {
if ($config->{ DOMAINNAME }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FQDN' && $diff->{ FQDN })) {
if ($config->{ FQDN }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAIL_LIST' && $diff->{ MAIL_LIST })) {
if ($config->{ MAIL_LIST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PERMIT_POST_FROM' && $diff->{ PERMIT_POST_FROM })) {
if ($config->{ PERMIT_POST_FROM }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REJECT_POST_HANDLER' && $diff->{ REJECT_POST_HANDLER })) {
if ($config->{ REJECT_POST_HANDLER }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONTROL_ADDRESS' && $diff->{ CONTROL_ADDRESS })) {
if ($config->{ CONTROL_ADDRESS }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PERMIT_COMMAND_FROM' && $diff->{ PERMIT_COMMAND_FROM })) {
if ($config->{ PERMIT_COMMAND_FROM }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REJECT_COMMAND_HANDLER' && $diff->{ REJECT_COMMAND_HANDLER })) {
if ($config->{ REJECT_COMMAND_HANDLER }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAIL_LIST_ACCEPT_COMMAND' && $diff->{ MAIL_LIST_ACCEPT_COMMAND })) {
if ($config->{ MAIL_LIST_ACCEPT_COMMAND }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAINTAINER' && $diff->{ MAINTAINER })) {
if ($config->{ MAINTAINER }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAINTAINER_SIGNATURE' && $diff->{ MAINTAINER_SIGNATURE })) {
if ($config->{ MAINTAINER_SIGNATURE }) {
$s .= sprintf("maintainer_signature = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ML_FN' && $diff->{ ML_FN })) {
if ($config->{ ML_FN }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SPOOL_DIR' && $diff->{ SPOOL_DIR })) {
if ($config->{ SPOOL_DIR }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TMP_DIR' && $diff->{ TMP_DIR })) {
if ($config->{ TMP_DIR }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'VAR_DIR' && $diff->{ VAR_DIR })) {
if ($config->{ VAR_DIR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'VARLOG_DIR' && $diff->{ VARLOG_DIR })) {
if ($config->{ VARLOG_DIR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'VARRUN_DIR' && $diff->{ VARRUN_DIR })) {
if ($config->{ VARRUN_DIR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'VARDB_DIR' && $diff->{ VARDB_DIR })) {
if ($config->{ VARDB_DIR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MANUAL_REGISTRATION_TYPE' && $diff->{ MANUAL_REGISTRATION_TYPE })) {
if ($config->{ MANUAL_REGISTRATION_TYPE } eq 'confirmation') {
$s .= sprintf("subscribe_command_auth_type = confirmation", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MANUAL_REGISTRATION_TYPE' && $diff->{ MANUAL_REGISTRATION_TYPE })) {
if ($config->{ MANUAL_REGISTRATION_TYPE } eq 'forward_to_admin') {
$s .= sprintf("subscribe_command_auth_type = manual", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MANUAL_REGISTRATION_CONFIRMATION_FILE' && $diff->{ MANUAL_REGISTRATION_CONFIRMATION_FILE })) {
if ($config->{ MANUAL_REGISTRATION_CONFIRMATION_FILE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_TYPE' && $diff->{ AUTO_REGISTRATION_TYPE })) {
if ($config->{ AUTO_REGISTRATION_TYPE } eq 'confirmation') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_TYPE' && $diff->{ AUTO_REGISTRATION_TYPE })) {
if ($config->{ AUTO_REGISTRATION_TYPE } eq 'subject') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_TYPE' && $diff->{ AUTO_REGISTRATION_TYPE })) {
if ($config->{ AUTO_REGISTRATION_TYPE } eq 'body') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_TYPE' && $diff->{ AUTO_REGISTRATION_TYPE })) {
if ($config->{ AUTO_REGISTRATION_TYPE } eq 'no-keyword') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_KEYWORD' && $diff->{ AUTO_REGISTRATION_KEYWORD })) {
if ($config->{ AUTO_REGISTRATION_KEYWORD } eq 'subscribe') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_KEYWORD' && $diff->{ AUTO_REGISTRATION_KEYWORD })) {
if ($config->{ AUTO_REGISTRATION_KEYWORD } ne 'subscribe') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_DEFAULT_MODE' && $diff->{ AUTO_REGISTRATION_DEFAULT_MODE })) {
if ($config->{ AUTO_REGISTRATION_DEFAULT_MODE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_ADDRESS' && $diff->{ CONFIRMATION_ADDRESS })) {
if ($config->{ CONFIRMATION_ADDRESS } eq 'CONTROL_ADDRESS') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_ADDRESS' && $diff->{ CONFIRMATION_ADDRESS })) {
if ($config->{ CONFIRMATION_ADDRESS } ne 'CONTROL_ADDRESS') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_SUBSCRIBE' && $diff->{ CONFIRMATION_SUBSCRIBE })) {
if ($config->{ CONFIRMATION_SUBSCRIBE } eq 'subscribe') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_SUBSCRIBE' && $diff->{ CONFIRMATION_SUBSCRIBE })) {
if ($config->{ CONFIRMATION_SUBSCRIBE } ne 'subscribe') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_KEYWORD' && $diff->{ CONFIRMATION_KEYWORD })) {
if ($config->{ CONFIRMATION_KEYWORD } eq 'confirm') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_KEYWORD' && $diff->{ CONFIRMATION_KEYWORD })) {
if ($config->{ CONFIRMATION_KEYWORD } ne 'confirm') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_WELCOME_STATEMENT' && $diff->{ CONFIRMATION_WELCOME_STATEMENT })) {
if ($config->{ CONFIRMATION_WELCOME_STATEMENT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME' && $diff->{ CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME })) {
if ($config->{ CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME' && $diff->{ CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME })) {
if ($config->{ CONFIRMATION_SUBSCRIBE_NEED_YOUR_NAME } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_FILE' && $diff->{ CONFIRMATION_FILE })) {
if ($config->{ CONFIRMATION_FILE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_EXPIRE' && $diff->{ CONFIRMATION_EXPIRE })) {
if ($config->{ CONFIRMATION_EXPIRE } == 168) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMATION_LIST' && $diff->{ CONFIRMATION_LIST })) {
if ($config->{ CONFIRMATION_LIST }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_SUBSCRIBE' && $diff->{ DEFAULT_SUBSCRIBE })) {
if ($config->{ DEFAULT_SUBSCRIBE } eq 'subscribe') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_SUBSCRIBE' && $diff->{ DEFAULT_SUBSCRIBE })) {
if ($config->{ DEFAULT_SUBSCRIBE } ne 'subscribe') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'WELCOME_FILE' && $diff->{ WELCOME_FILE })) {
if ($config->{ WELCOME_FILE }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'WELCOME_STATEMENT' && $diff->{ WELCOME_STATEMENT })) {
if ($config->{ WELCOME_STATEMENT } eq 'Welcome') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILE_TO_REGIST' && $diff->{ FILE_TO_REGIST })) {
if ($config->{ FILE_TO_REGIST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTERED_UNDELIVER_P' && $diff->{ AUTO_REGISTERED_UNDELIVER_P })) {
if ($config->{ AUTO_REGISTERED_UNDELIVER_P } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTERED_UNDELIVER_P' && $diff->{ AUTO_REGISTERED_UNDELIVER_P })) {
if ($config->{ AUTO_REGISTERED_UNDELIVER_P } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTERD_UNDELIVER_P' && $diff->{ AUTO_REGISTERD_UNDELIVER_P })) {
if ($config->{ AUTO_REGISTERD_UNDELIVER_P } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_LINES_LIMIT' && $diff->{ AUTO_REGISTRATION_LINES_LIMIT })) {
if ($config->{ AUTO_REGISTRATION_LINES_LIMIT } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_REGISTRATION_LINES_LIMIT' && $diff->{ AUTO_REGISTRATION_LINES_LIMIT })) {
if ($config->{ AUTO_REGISTRATION_LINES_LIMIT } > 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMD_ACK_REQ_FILE' && $diff->{ CONFIRMD_ACK_REQ_FILE })) {
if ($config->{ CONFIRMD_ACK_REQ_FILE } eq '$DIR/confirmd.ackreq') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMD_ACK_LOGFILE' && $diff->{ CONFIRMD_ACK_LOGFILE })) {
if ($config->{ CONFIRMD_ACK_LOGFILE } eq '$VARLOG_DIR/confirmd.ack') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMD_ACK_EXPIRE_UNIT' && $diff->{ CONFIRMD_ACK_EXPIRE_UNIT })) {
if ($config->{ CONFIRMD_ACK_EXPIRE_UNIT } eq '1month') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONFIRMD_ACK_WAIT_UNIT' && $diff->{ CONFIRMD_ACK_WAIT_UNIT })) {
if ($config->{ CONFIRMD_ACK_WAIT_UNIT } eq '2weeks') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION' && $diff->{ REMOTE_ADMINISTRATION })) {
if ($config->{ REMOTE_ADMINISTRATION } == 0) {
$s .= sprintf("use_admin_command_mail_function = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION' && $diff->{ REMOTE_ADMINISTRATION })) {
if ($config->{ REMOTE_ADMINISTRATION } == 1) {
$s .= sprintf("use_admin_command_mail_function = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_REQUIRE_PASSWORD' && $diff->{ REMOTE_ADMINISTRATION_REQUIRE_PASSWORD })) {
if ($config->{ REMOTE_ADMINISTRATION_REQUIRE_PASSWORD } == 1) {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_admin_member_password reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_REQUIRE_PASSWORD' && $diff->{ REMOTE_ADMINISTRATION_REQUIRE_PASSWORD })) {
if ($config->{ REMOTE_ADMINISTRATION_REQUIRE_PASSWORD } == 0) {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts permit_admin_member_maps reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'crypt') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_admin_member_password reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'address') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts permit_admin_member_maps reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'md5') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_admin_member_password reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'pgp') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_pgp_signature reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'pgp2') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_pgp_signature reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'pgp5') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_pgp_signature reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REMOTE_ADMINISTRATION_AUTH_TYPE' && $diff->{ REMOTE_ADMINISTRATION_AUTH_TYPE })) {
if ($config->{ REMOTE_ADMINISTRATION_AUTH_TYPE } eq 'gpg') {
$s .= sprintf("admin_command_mail_restrictions = reject_system_special_accounts check_pgp_signature reject", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_MEMBER_LIST' && $diff->{ ADMIN_MEMBER_LIST })) {
if ($config->{ ADMIN_MEMBER_LIST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_HELP_FILE' && $diff->{ ADMIN_HELP_FILE })) {
if ($config->{ ADMIN_HELP_FILE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PASSWD_FILE' && $diff->{ PASSWD_FILE })) {
if ($config->{ PASSWD_FILE }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_ADD_SEND_WELCOME_FILE' && $diff->{ ADMIN_ADD_SEND_WELCOME_FILE })) {
if ($config->{ ADMIN_ADD_SEND_WELCOME_FILE } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_ADD_SEND_WELCOME_FILE' && $diff->{ ADMIN_ADD_SEND_WELCOME_FILE })) {
if ($config->{ ADMIN_ADD_SEND_WELCOME_FILE } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_LOG_DEFAULT_LINE_LIMIT' && $diff->{ ADMIN_LOG_DEFAULT_LINE_LIMIT })) {
if ($config->{ ADMIN_LOG_DEFAULT_LINE_LIMIT }) {
$s .= sprintf("log_command_tail_starting_location = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGP_PATH' && $diff->{ PGP_PATH })) {
if ($config->{ PGP_PATH } eq '$DIR/etc/pgp') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_FML40_PGP_PATH' && $diff->{ USE_FML40_PGP_PATH })) {
if ($config->{ USE_FML40_PGP_PATH } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DIST_AUTH_KEYRING_DIR' && $diff->{ DIST_AUTH_KEYRING_DIR })) {
if ($config->{ DIST_AUTH_KEYRING_DIR } eq '$DIR/etc/dist-auth') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DIST_ENCRYPT_KEYRING_DIR' && $diff->{ DIST_ENCRYPT_KEYRING_DIR })) {
if ($config->{ DIST_ENCRYPT_KEYRING_DIR } eq '$DIR/etc/dist-encrypt') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_AUTH_KEYRING_DIR' && $diff->{ ADMIN_AUTH_KEYRING_DIR })) {
if ($config->{ ADMIN_AUTH_KEYRING_DIR } eq '$DIR/etc/admin-auth') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_ENCRYPT_KEYRING_DIR' && $diff->{ ADMIN_ENCRYPT_KEYRING_DIR })) {
if ($config->{ ADMIN_ENCRYPT_KEYRING_DIR } eq '$DIR/etc/admin-encrypt') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MODERATOR_MEMBER_LIST' && $diff->{ MODERATOR_MEMBER_LIST })) {
if ($config->{ MODERATOR_MEMBER_LIST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MODERATOR_EXPIRE_LIMIT' && $diff->{ MODERATOR_EXPIRE_LIMIT })) {
if ($config->{ MODERATOR_EXPIRE_LIMIT } == 14) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REJECT_ADDR' && $diff->{ REJECT_ADDR })) {
if ($config->{ REJECT_ADDR }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REJECT_ADDR_LIST' && $diff->{ REJECT_ADDR_LIST })) {
if ($config->{ REJECT_ADDR_LIST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_UNIX_FROM_LOOP_CHECK' && $diff->{ NOT_USE_UNIX_FROM_LOOP_CHECK })) {
if ($config->{ NOT_USE_UNIX_FROM_LOOP_CHECK } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_UNIX_FROM_LOOP_CHECK' && $diff->{ NOT_USE_UNIX_FROM_LOOP_CHECK })) {
if ($config->{ NOT_USE_UNIX_FROM_LOOP_CHECK } == 1) {
$s .= sprintf("incoming_mail_envelope_loop_check_rules -= check_envelope_sender", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHECK_MESSAGE_ID' && $diff->{ CHECK_MESSAGE_ID })) {
if ($config->{ CHECK_MESSAGE_ID } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHECK_MESSAGE_ID' && $diff->{ CHECK_MESSAGE_ID })) {
if ($config->{ CHECK_MESSAGE_ID } == 0) {
$s .= sprintf("incoming_mail_header_loop_check_rules -= check_message_id", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHECK_MAILBODY_CKSUM' && $diff->{ CHECK_MAILBODY_CKSUM })) {
if ($config->{ CHECK_MAILBODY_CKSUM } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHECK_MAILBODY_CKSUM' && $diff->{ CHECK_MAILBODY_CKSUM })) {
if ($config->{ CHECK_MAILBODY_CKSUM } == 0) {
$s .= sprintf("incoming_mail_body_loop_check_rules -= check_body_checksum", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_CONNECTION' && $diff->{ LOG_CONNECTION })) {
if ($config->{ LOG_CONNECTION }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADDR_CHECK_MAX' && $diff->{ ADDR_CHECK_MAX })) {
if ($config->{ ADDR_CHECK_MAX }) {
$s .= sprintf("address_compare_function_domain_matching_level = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'INCOMING_MAIL_SIZE_LIMIT' && $diff->{ INCOMING_MAIL_SIZE_LIMIT })) {
if ($config->{ INCOMING_MAIL_SIZE_LIMIT } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'INCOMING_MAIL_SIZE_LIMIT' && $diff->{ INCOMING_MAIL_SIZE_LIMIT })) {
if ($config->{ INCOMING_MAIL_SIZE_LIMIT } != 0) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOTIFY_MAIL_SIZE_OVERFLOW' && $diff->{ NOTIFY_MAIL_SIZE_OVERFLOW })) {
if ($config->{ NOTIFY_MAIL_SIZE_OVERFLOW } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOTIFY_MAIL_SIZE_OVERFLOW' && $diff->{ NOTIFY_MAIL_SIZE_OVERFLOW })) {
if ($config->{ NOTIFY_MAIL_SIZE_OVERFLOW } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ANNOUNCE_MAIL_SIZE_OVERFLOW' && $diff->{ ANNOUNCE_MAIL_SIZE_OVERFLOW })) {
if ($config->{ ANNOUNCE_MAIL_SIZE_OVERFLOW } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ANNOUNCE_MAIL_SIZE_OVERFLOW' && $diff->{ ANNOUNCE_MAIL_SIZE_OVERFLOW })) {
if ($config->{ ANNOUNCE_MAIL_SIZE_OVERFLOW } == 1) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAX_MEMBER_LIMIT' && $diff->{ MAX_MEMBER_LIMIT })) {
if ($config->{ MAX_MEMBER_LIMIT }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_DISTRIBUTE_FILTER' && $diff->{ USE_DISTRIBUTE_FILTER })) {
if ($config->{ USE_DISTRIBUTE_FILTER } == 1) {
$s .= sprintf("use_article_filter = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_DISTRIBUTE_FILTER' && $diff->{ USE_DISTRIBUTE_FILTER })) {
if ($config->{ USE_DISTRIBUTE_FILTER } == 0) {
$s .= sprintf("use_article_filter = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DISTRIBUTE_FILTER_HOOK' && $diff->{ DISTRIBUTE_FILTER_HOOK })) {
if ($config->{ DISTRIBUTE_FILTER_HOOK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_NOTIFY_REJECTION' && $diff->{ FILTER_NOTIFY_REJECTION })) {
if ($config->{ FILTER_NOTIFY_REJECTION } == 1) {
$s .= sprintf("use_article_filter_reject_notice = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_NOTIFY_REJECTION' && $diff->{ FILTER_NOTIFY_REJECTION })) {
if ($config->{ FILTER_NOTIFY_REJECTION } == 0) {
$s .= sprintf("use_article_filter_reject_notice = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_NULL_BODY' && $diff->{ FILTER_ATTR_REJECT_NULL_BODY })) {
if ($config->{ FILTER_ATTR_REJECT_NULL_BODY } == 1) {
$s .= sprintf("article_text_plain_filter_rules += reject_null_mail_body", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_NULL_BODY' && $diff->{ FILTER_ATTR_REJECT_NULL_BODY })) {
if ($config->{ FILTER_ATTR_REJECT_NULL_BODY } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_null_mail_body", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_COMMAND' && $diff->{ FILTER_ATTR_REJECT_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_COMMAND } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_COMMAND' && $diff->{ FILTER_ATTR_REJECT_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_COMMAND } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_old_fml_command_syntax", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_2BYTES_COMMAND' && $diff->{ FILTER_ATTR_REJECT_2BYTES_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_2BYTES_COMMAND } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_2BYTES_COMMAND' && $diff->{ FILTER_ATTR_REJECT_2BYTES_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_2BYTES_COMMAND } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_japanese_command_syntax", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_INVALID_COMMAND' && $diff->{ FILTER_ATTR_REJECT_INVALID_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_INVALID_COMMAND } == 1) {
$s .= sprintf("article_text_plain_filter_rules += reject_invalid_fml_command_syntax", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_INVALID_COMMAND' && $diff->{ FILTER_ATTR_REJECT_INVALID_COMMAND })) {
if ($config->{ FILTER_ATTR_REJECT_INVALID_COMMAND } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_invalid_fml_command_syntax", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_ONE_LINE_BODY' && $diff->{ FILTER_ATTR_REJECT_ONE_LINE_BODY })) {
if ($config->{ FILTER_ATTR_REJECT_ONE_LINE_BODY } == 1) {
$s .= sprintf("article_text_plain_filter_rules += reject_one_line_message", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_ONE_LINE_BODY' && $diff->{ FILTER_ATTR_REJECT_ONE_LINE_BODY })) {
if ($config->{ FILTER_ATTR_REJECT_ONE_LINE_BODY } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_one_line_message", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_MS_GUID' && $diff->{ FILTER_ATTR_REJECT_MS_GUID })) {
if ($config->{ FILTER_ATTR_REJECT_MS_GUID } == 1) {
$s .= sprintf("article_text_plain_filter_rules += reject_ms_guid", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_MS_GUID' && $diff->{ FILTER_ATTR_REJECT_MS_GUID })) {
if ($config->{ FILTER_ATTR_REJECT_MS_GUID } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_ms_guid", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_INVALID_JAPANESE' && $diff->{ FILTER_ATTR_REJECT_INVALID_JAPANESE })) {
if ($config->{ FILTER_ATTR_REJECT_INVALID_JAPANESE } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FILTER_ATTR_REJECT_INVALID_JAPANESE' && $diff->{ FILTER_ATTR_REJECT_INVALID_JAPANESE })) {
if ($config->{ FILTER_ATTR_REJECT_INVALID_JAPANESE } == 0) {
$s .= sprintf("article_text_plain_filter_rules -= reject_not_iso2022jp_japanese_string", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONTENT_HANDLER_CUTOFF_EMPTY_MESSAGE' && $diff->{ CONTENT_HANDLER_CUTOFF_EMPTY_MESSAGE })) {
if ($config->{ CONTENT_HANDLER_CUTOFF_EMPTY_MESSAGE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CONTENT_HANDLER_REJECT_EMPTY_MESSAGE' && $diff->{ CONTENT_HANDLER_REJECT_EMPTY_MESSAGE })) {
if ($config->{ CONTENT_HANDLER_REJECT_EMPTY_MESSAGE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_HANKAKU_CONVERTER' && $diff->{ USE_HANKAKU_CONVERTER })) {
if ($config->{ USE_HANKAKU_CONVERTER } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_HANKAKU_CONVERTER' && $diff->{ USE_HANKAKU_CONVERTER })) {
if ($config->{ USE_HANKAKU_CONVERTER } == 1) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_MAIL_DEFAULT_HANDLER' && $diff->{ HTML_MAIL_DEFAULT_HANDLER })) {
if ($config->{ HTML_MAIL_DEFAULT_HANDLER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_MTI' && $diff->{ USE_MTI })) {
if ($config->{ USE_MTI }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_WARN_INTERVAL' && $diff->{ MTI_WARN_INTERVAL })) {
if ($config->{ MTI_WARN_INTERVAL }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_WARN_LASTLOG' && $diff->{ MTI_WARN_LASTLOG })) {
if ($config->{ MTI_WARN_LASTLOG }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_EXPIRE_UNIT' && $diff->{ MTI_EXPIRE_UNIT }) || ($key eq 'MTI_BURST_SOFT_LIMIT' && $diff->{ MTI_BURST_SOFT_LIMIT })) {
if ($config->{ MTI_EXPIRE_UNIT }) {
if ($config->{ MTI_BURST_SOFT_LIMIT }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_BURST_HARD_LIMIT' && $diff->{ MTI_BURST_HARD_LIMIT })) {
if ($config->{ MTI_BURST_HARD_LIMIT }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_COST_EVAL_FUNCTION' && $diff->{ MTI_COST_EVAL_FUNCTION })) {
if ($config->{ MTI_COST_EVAL_FUNCTION }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MTI_MAIL_FROM_HINT_LIST' && $diff->{ MTI_MAIL_FROM_HINT_LIST })) {
if ($config->{ MTI_MAIL_FROM_HINT_LIST }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBSCRIBE_ANNOUNCE_FORWARD_TYPE' && $diff->{ SUBSCRIBE_ANNOUNCE_FORWARD_TYPE })) {
if ($config->{ SUBSCRIBE_ANNOUNCE_FORWARD_TYPE } eq 'prepend_info') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBSCRIBE_ANNOUNCE_FORWARD_TYPE' && $diff->{ SUBSCRIBE_ANNOUNCE_FORWARD_TYPE })) {
if ($config->{ SUBSCRIBE_ANNOUNCE_FORWARD_TYPE } eq 'raw') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'UNSUBSCRIBE_AUTH_TYPE' && $diff->{ UNSUBSCRIBE_AUTH_TYPE })) {
if ($config->{ UNSUBSCRIBE_AUTH_TYPE } eq 'confirmation') {
$s .= sprintf("unsubscribe_command_auth_type = confirmation", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'UNSUBSCRIBE_AUTH_TYPE' && $diff->{ UNSUBSCRIBE_AUTH_TYPE })) {
if ($config->{ UNSUBSCRIBE_AUTH_TYPE } ne 'confirmation') {
$s .= sprintf("unsubscribe_command_auth_type = confirmation", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHADDR_AUTH_TYPE' && $diff->{ CHADDR_AUTH_TYPE })) {
if ($config->{ CHADDR_AUTH_TYPE } eq 'confirmation') {
$s .= sprintf("chaddr_command_auth_type = confirmation", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHADDR_AUTH_TYPE' && $diff->{ CHADDR_AUTH_TYPE })) {
if ($config->{ CHADDR_AUTH_TYPE } ne 'confirmation') {
$s .= sprintf("unsubscribe_command_auth_type = confirmation", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_LOG_MAIL' && $diff->{ USE_LOG_MAIL })) {
if ($config->{ USE_LOG_MAIL } == 0) {
$s .= sprintf("use_incoming_mail_cache = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_LOG_MAIL' && $diff->{ USE_LOG_MAIL })) {
if ($config->{ USE_LOG_MAIL } == 1) {
$s .= sprintf("use_incoming_mail_cache = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_MAIL_DIR' && $diff->{ LOG_MAIL_DIR })) {
if ($config->{ LOG_MAIL_DIR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_MAIL_SEQ' && $diff->{ LOG_MAIL_SEQ })) {
if ($config->{ LOG_MAIL_SEQ }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NUM_LOG_MAIL' && $diff->{ NUM_LOG_MAIL })) {
if ($config->{ NUM_LOG_MAIL }) {
$s .= sprintf("incoming_mail_cache_size = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_MAIL_FILE_SIZE_MAX' && $diff->{ LOG_MAIL_FILE_SIZE_MAX })) {
if ($config->{ LOG_MAIL_FILE_SIZE_MAX }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ENCRYPTED_DISTRIBUTION' && $diff->{ USE_ENCRYPTED_DISTRIBUTION })) {
if ($config->{ USE_ENCRYPTED_DISTRIBUTION } == 1) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ENCRYPTED_DISTRIBUTION' && $diff->{ USE_ENCRYPTED_DISTRIBUTION })) {
if ($config->{ USE_ENCRYPTED_DISTRIBUTION } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ENCRYPTED_DISTRIBUTION_TYPE' && $diff->{ ENCRYPTED_DISTRIBUTION_TYPE })) {
if ($config->{ ENCRYPTED_DISTRIBUTION_TYPE } eq 'pgp') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ENCRYPTED_DISTRIBUTION_TYPE' && $diff->{ ENCRYPTED_DISTRIBUTION_TYPE })) {
if ($config->{ ENCRYPTED_DISTRIBUTION_TYPE } eq 'pgp2') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ENCRYPTED_DISTRIBUTION_TYPE' && $diff->{ ENCRYPTED_DISTRIBUTION_TYPE })) {
if ($config->{ ENCRYPTED_DISTRIBUTION_TYPE } eq 'pgp5') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ENCRYPTED_DISTRIBUTION_TYPE' && $diff->{ ENCRYPTED_DISTRIBUTION_TYPE })) {
if ($config->{ ENCRYPTED_DISTRIBUTION_TYPE } eq 'gpg') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATE_TYPE' && $diff->{ DATE_TYPE })) {
if ($config->{ DATE_TYPE } eq 'original-date') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATE_TYPE' && $diff->{ DATE_TYPE })) {
if ($config->{ DATE_TYPE } ne 'original-date') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'XMLNAME' && $diff->{ XMLNAME })) {
if ($config->{ XMLNAME } eq 'X-ML-Name:') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'XMLNAME' && $diff->{ XMLNAME })) {
if ($config->{ XMLNAME } ne 'X-ML-Name:') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'XMLCOUNT' && $diff->{ XMLCOUNT })) {
if ($config->{ XMLCOUNT } eq 'X-Mail-Count') {
$s .= sprintf("article_header_rewrite_rules += add_fml_traditional_article_id", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'XMLCOUNT' && $diff->{ XMLCOUNT })) {
if ($config->{ XMLCOUNT } ne 'X-Mail-Count') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBJECT_TAG_TYPE' && $diff->{ SUBJECT_TAG_TYPE })) {
if ($config->{ SUBJECT_TAG_TYPE }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'BRACKET' && $diff->{ BRACKET })) {
if ($config->{ BRACKET } eq 'Elena') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'STRIP_BRACKETS' && $diff->{ STRIP_BRACKETS })) {
if ($config->{ STRIP_BRACKETS } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'BRACKET_SEPARATOR' && $diff->{ BRACKET_SEPARATOR })) {
if ($config->{ BRACKET_SEPARATOR }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBJECT_FREE_FORM' && $diff->{ SUBJECT_FREE_FORM })) {
if ($config->{ SUBJECT_FREE_FORM }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBJECT_FREE_FORM_REGEXP' && $diff->{ SUBJECT_FREE_FORM_REGEXP })) {
if ($config->{ SUBJECT_FREE_FORM_REGEXP }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBJECT_FORM_LONG_ID' && $diff->{ SUBJECT_FORM_LONG_ID })) {
if ($config->{ SUBJECT_FORM_LONG_ID }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ERRORS_TO' && $diff->{ USE_ERRORS_TO })) {
if ($config->{ USE_ERRORS_TO } == 1) {
$s .= sprintf("article_header_rewrite_rules += rewrite_errors_to", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ERRORS_TO' && $diff->{ USE_ERRORS_TO })) {
if ($config->{ USE_ERRORS_TO } == 0) {
$s .= sprintf("article_header_rewrite_rules -= rewrite_errors_to", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ERRORS_TO' && $diff->{ ERRORS_TO })) {
if ($config->{ ERRORS_TO }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ORIGINAL_MESSAGE_ID' && $diff->{ USE_ORIGINAL_MESSAGE_ID })) {
if ($config->{ USE_ORIGINAL_MESSAGE_ID } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ORIGINAL_MESSAGE_ID' && $diff->{ USE_ORIGINAL_MESSAGE_ID })) {
if ($config->{ USE_ORIGINAL_MESSAGE_ID } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PRECEDENCE' && $diff->{ PRECEDENCE })) {
if ($config->{ PRECEDENCE }) {
$s .= sprintf("mail_header_default_precedence = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'APPEND_STARDATE' && $diff->{ APPEND_STARDATE })) {
if ($config->{ APPEND_STARDATE } == 1) {
$s .= sprintf("article_header_rewrite_rules += rewrite_stardate", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'APPEND_STARDATE' && $diff->{ APPEND_STARDATE })) {
if ($config->{ APPEND_STARDATE } == 0) {
$s .= sprintf("article_header_rewrite_rules -= rewrite_stardate", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_RFC2369' && $diff->{ USE_RFC2369 })) {
if ($config->{ USE_RFC2369 } == 1) {
$s .= sprintf("article_header_rewrite_rules += add_rfc2369", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_RFC2369' && $diff->{ USE_RFC2369 })) {
if ($config->{ USE_RFC2369 } == 0) {
$s .= sprintf("article_header_rewrite_rules -= add_rfc2369", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_SOFTWARE' && $diff->{ LIST_SOFTWARE })) {
if ($config->{ LIST_SOFTWARE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_POST' && $diff->{ LIST_POST })) {
if ($config->{ LIST_POST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_OWNER' && $diff->{ LIST_OWNER })) {
if ($config->{ LIST_OWNER }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_HELP' && $diff->{ LIST_HELP })) {
if ($config->{ LIST_HELP }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_SUBSCRIBE' && $diff->{ LIST_SUBSCRIBE })) {
if ($config->{ LIST_SUBSCRIBE }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_UNSUBSCRIBE' && $diff->{ LIST_UNSUBSCRIBE })) {
if ($config->{ LIST_UNSUBSCRIBE }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIST_ID' && $diff->{ LIST_ID })) {
if ($config->{ LIST_ID }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REWRITE_TO' && $diff->{ REWRITE_TO })) {
if ($config->{ REWRITE_TO } == 2) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REWRITE_TO' && $diff->{ REWRITE_TO })) {
if ($config->{ REWRITE_TO } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'REWRITE_TO' && $diff->{ REWRITE_TO })) {
if ($config->{ REWRITE_TO } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'Subject' && $diff->{ Subject })) {
if ($config->{ Subject }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'From_address' && $diff->{ From_address })) {
if ($config->{ From_address }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'User' && $diff->{ User })) {
if ($config->{ User }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'Date' && $diff->{ Date })) {
if ($config->{ Date }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TZone' && $diff->{ TZone })) {
if ($config->{ TZone }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TZONE_DST' && $diff->{ TZONE_DST })) {
if ($config->{ TZONE_DST }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PASS_ALL_FIELDS_IN_HEADER' && $diff->{ PASS_ALL_FIELDS_IN_HEADER })) {
if ($config->{ PASS_ALL_FIELDS_IN_HEADER } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PASS_ALL_FIELDS_IN_HEADER' && $diff->{ PASS_ALL_FIELDS_IN_HEADER })) {
if ($config->{ PASS_ALL_FIELDS_IN_HEADER } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUPERFLUOUS_HEADERS' && $diff->{ SUPERFLUOUS_HEADERS })) {
if ($config->{ SUPERFLUOUS_HEADERS } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUPERFLUOUS_HEADERS' && $diff->{ SUPERFLUOUS_HEADERS })) {
if ($config->{ SUPERFLUOUS_HEADERS } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SKIP_FIELDS' && $diff->{ SKIP_FIELDS })) {
if ($config->{ SKIP_FIELDS }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ALLOW_WRONG_LINES_IN_HEADER' && $diff->{ ALLOW_WRONG_LINES_IN_HEADER })) {
if ($config->{ ALLOW_WRONG_LINES_IN_HEADER } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMMAND_SYNTAX_EXTENSION' && $diff->{ COMMAND_SYNTAX_EXTENSION })) {
if ($config->{ COMMAND_SYNTAX_EXTENSION } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SUBJECT_AS_COMMANDS' && $diff->{ USE_SUBJECT_AS_COMMANDS })) {
if ($config->{ USE_SUBJECT_AS_COMMANDS }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_WARNING' && $diff->{ USE_WARNING })) {
if ($config->{ USE_WARNING } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_WARNING' && $diff->{ USE_WARNING })) {
if ($config->{ USE_WARNING } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMMAND_ONLY_SERVER' && $diff->{ COMMAND_ONLY_SERVER })) {
if ($config->{ COMMAND_ONLY_SERVER }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMMAND_CHECK_LIMIT' && $diff->{ COMMAND_CHECK_LIMIT })) {
if ($config->{ COMMAND_CHECK_LIMIT } == 3) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'GUIDE_CHECK_LIMIT' && $diff->{ GUIDE_CHECK_LIMIT })) {
if ($config->{ GUIDE_CHECK_LIMIT } == 3) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'GUIDE_KEYWORD' && $diff->{ GUIDE_KEYWORD })) {
if ($config->{ GUIDE_KEYWORD } eq 'guide') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAXLEN_COMMAND_INPUT' && $diff->{ MAXLEN_COMMAND_INPUT }) || ($key eq 'MAXLEN_COMMAND_INPUT' && $diff->{ MAXLEN_COMMAND_INPUT })) {
if ($config->{ MAXLEN_COMMAND_INPUT } > 0) {
if ($config->{ MAXLEN_COMMAND_INPUT } != 128) {
$s .= sprintf("command_mail_line_length_limit = %s", $value);
}
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAXNUM_COMMAND_INPUT' && $diff->{ MAXNUM_COMMAND_INPUT })) {
if ($config->{ MAXNUM_COMMAND_INPUT } > 0) {
$s .= sprintf("command_mail_valid_command_limit = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHADDR_KEYWORD' && $diff->{ CHADDR_KEYWORD })) {
if ($config->{ CHADDR_KEYWORD } eq 'chaddr|change\-address|change') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CHADDR_REPLY_TO' && $diff->{ CHADDR_REPLY_TO })) {
if ($config->{ CHADDR_REPLY_TO } eq 'newaddr') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ADMIN_CHADDR_REPLY_TO' && $diff->{ ADMIN_CHADDR_REPLY_TO })) {
if ($config->{ ADMIN_CHADDR_REPLY_TO } eq 'newaddr') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MGET_MODE_DEFAULT' && $diff->{ MGET_MODE_DEFAULT })) {
if ($config->{ MGET_MODE_DEFAULT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MGET_TEXT_MODE_DEFAULT' && $diff->{ MGET_TEXT_MODE_DEFAULT })) {
if ($config->{ MGET_TEXT_MODE_DEFAULT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAIL_LENGTH_LIMIT' && $diff->{ MAIL_LENGTH_LIMIT })) {
if ($config->{ MAIL_LENGTH_LIMIT } == 1000) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SLEEPTIME' && $diff->{ SLEEPTIME })) {
if ($config->{ SLEEPTIME }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_VERSION' && $diff->{ MIME_VERSION })) {
if ($config->{ MIME_VERSION }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_CONTENT_TYPE' && $diff->{ MIME_CONTENT_TYPE })) {
if ($config->{ MIME_CONTENT_TYPE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_MULTIPART_BOUNDARY' && $diff->{ MIME_MULTIPART_BOUNDARY })) {
if ($config->{ MIME_MULTIPART_BOUNDARY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_MULTIPART_CLOSE_DELIMITER' && $diff->{ MIME_MULTIPART_CLOSE_DELIMITER })) {
if ($config->{ MIME_MULTIPART_CLOSE_DELIMITER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_MULTIPART_DELIMITER' && $diff->{ MIME_MULTIPART_DELIMITER })) {
if ($config->{ MIME_MULTIPART_DELIMITER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_MULTIPART_PREAMBLE' && $diff->{ MIME_MULTIPART_PREAMBLE })) {
if ($config->{ MIME_MULTIPART_PREAMBLE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_MULTIPART_TRAILER' && $diff->{ MIME_MULTIPART_TRAILER })) {
if ($config->{ MIME_MULTIPART_TRAILER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SJIS_IN_ISH' && $diff->{ USE_SJIS_IN_ISH })) {
if ($config->{ USE_SJIS_IN_ISH }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RFC1153_ISSUE' && $diff->{ RFC1153_ISSUE })) {
if ($config->{ RFC1153_ISSUE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RFC1153_VOL' && $diff->{ RFC1153_VOL })) {
if ($config->{ RFC1153_VOL }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RFC1153_SEQUENCE_FILE' && $diff->{ RFC1153_SEQUENCE_FILE })) {
if ($config->{ RFC1153_SEQUENCE_FILE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_DOT_QMAIL_EXT' && $diff->{ USE_DOT_QMAIL_EXT })) {
if ($config->{ USE_DOT_QMAIL_EXT } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FORCE_COMMAND_REPLY_TO' && $diff->{ FORCE_COMMAND_REPLY_TO })) {
if ($config->{ FORCE_COMMAND_REPLY_TO }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MGET_SUBJECT_TEMPLATE' && $diff->{ MGET_SUBJECT_TEMPLATE })) {
if ($config->{ MGET_SUBJECT_TEMPLATE } eq 'result') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MESSAGE_RETURN_ADDR_POLICY' && $diff->{ MESSAGE_RETURN_ADDR_POLICY })) {
if ($config->{ MESSAGE_RETURN_ADDR_POLICY } eq 'reply-to') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_SUBJECT_TEMPLATE' && $diff->{ MSEND_SUBJECT_TEMPLATE })) {
if ($config->{ MSEND_SUBJECT_TEMPLATE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_RC' && $diff->{ MSEND_RC })) {
if ($config->{ MSEND_RC }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_MODE_DEFAULT' && $diff->{ MSEND_MODE_DEFAULT })) {
if ($config->{ MSEND_MODE_DEFAULT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_DEFAULT_SUBJECT' && $diff->{ MSEND_DEFAULT_SUBJECT })) {
if ($config->{ MSEND_DEFAULT_SUBJECT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_NOTIFICATION' && $diff->{ MSEND_NOTIFICATION })) {
if ($config->{ MSEND_NOTIFICATION }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_NOTIFICATION_SUBJECT' && $diff->{ MSEND_NOTIFICATION_SUBJECT })) {
if ($config->{ MSEND_NOTIFICATION_SUBJECT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_NOT_USE_X_ML_INFO' && $diff->{ MSEND_NOT_USE_X_ML_INFO })) {
if ($config->{ MSEND_NOT_USE_X_ML_INFO } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_NOT_USE_X_ML_INFO' && $diff->{ MSEND_NOT_USE_X_ML_INFO })) {
if ($config->{ MSEND_NOT_USE_X_ML_INFO } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MSEND_NOT_USE_NEWSYSLOG' && $diff->{ MSEND_NOT_USE_NEWSYSLOG })) {
if ($config->{ MSEND_NOT_USE_NEWSYSLOG } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_MESSAGE_ID' && $diff->{ LOG_MESSAGE_ID })) {
if ($config->{ LOG_MESSAGE_ID } eq '$VARRUN_DIR/msgidcache') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MESSAGE_ID_CACHE_BUFSIZE' && $diff->{ MESSAGE_ID_CACHE_BUFSIZE })) {
if ($config->{ MESSAGE_ID_CACHE_BUFSIZE } == 6000) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOG_MAILBODY_CKSUM' && $diff->{ LOG_MAILBODY_CKSUM })) {
if ($config->{ LOG_MAILBODY_CKSUM } ne '$VARRUN_DIR/bodycksumcache') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MEMBER_LIST' && $diff->{ MEMBER_LIST })) {
if ($config->{ MEMBER_LIST } ne '$DIR/members') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ACTIVE_LIST' && $diff->{ ACTIVE_LIST })) {
if ($config->{ ACTIVE_LIST } ne '$DIR/actives') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'GUIDE_FILE' && $diff->{ GUIDE_FILE })) {
if ($config->{ GUIDE_FILE } ne '$DIR/guide') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'OBJECTIVE_FILE' && $diff->{ OBJECTIVE_FILE })) {
if ($config->{ OBJECTIVE_FILE } ne '$DIR/objective') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HELP_FILE' && $diff->{ HELP_FILE })) {
if ($config->{ HELP_FILE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DENY_FILE' && $diff->{ DENY_FILE })) {
if ($config->{ DENY_FILE } ne '$DIR/deny') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOGFILE' && $diff->{ LOGFILE })) {
if ($config->{ LOGFILE } ne '$DIR/log') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MGET_LOGFILE' && $diff->{ MGET_LOGFILE })) {
if ($config->{ MGET_LOGFILE } ne '$DIR/log') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOGFILE_SUFFIX' && $diff->{ LOGFILE_SUFFIX })) {
if ($config->{ LOGFILE_SUFFIX }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEBUG_LOGFILE' && $diff->{ DEBUG_LOGFILE })) {
if ($config->{ DEBUG_LOGFILE } eq '$DIR/log.debug') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUMMARY_FILE' && $diff->{ SUMMARY_FILE })) {
if ($config->{ SUMMARY_FILE } ne '$DIR/summary') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SEQUENCE_FILE' && $diff->{ SEQUENCE_FILE })) {
if ($config->{ SEQUENCE_FILE } ne '$DIR/seq') {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_FILE' && $diff->{ LOCK_FILE })) {
if ($config->{ LOCK_FILE } eq '$VARRUN_DIR/lockfile.v7') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_DIR' && $diff->{ LOCK_DIR })) {
if ($config->{ LOCK_DIR }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCKDIR' && $diff->{ LOCKDIR })) {
if ($config->{ LOCKDIR }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCKFILE' && $diff->{ LOCKFILE })) {
if ($config->{ LOCKFILE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_INET6' && $diff->{ USE_INET6 })) {
if ($config->{ USE_INET6 } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_INET6' && $diff->{ USE_INET6 })) {
if ($config->{ USE_INET6 } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HOST' && $diff->{ HOST })) {
if ($config->{ HOST }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PORT' && $diff->{ PORT })) {
if ($config->{ PORT }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_SENDER' && $diff->{ SMTP_SENDER })) {
if ($config->{ SMTP_SENDER }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_LOG' && $diff->{ SMTP_LOG })) {
if ($config->{ SMTP_LOG }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SMTP_LOG_ROTATE' && $diff->{ USE_SMTP_LOG_ROTATE })) {
if ($config->{ USE_SMTP_LOG_ROTATE } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SMTP_LOG_ROTATE' && $diff->{ USE_SMTP_LOG_ROTATE })) {
if ($config->{ USE_SMTP_LOG_ROTATE } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_LOG_ROTATE_EXPIRE_LIMIT' && $diff->{ SMTP_LOG_ROTATE_EXPIRE_LIMIT })) {
if ($config->{ SMTP_LOG_ROTATE_EXPIRE_LIMIT } == 90) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_LOG_ROTATE_EXPIRE_LIMIT' && $diff->{ SMTP_LOG_ROTATE_EXPIRE_LIMIT })) {
if ($config->{ SMTP_LOG_ROTATE_EXPIRE_LIMIT } != 90) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NUM_SMTP_LOG_ROTATE' && $diff->{ NUM_SMTP_LOG_ROTATE })) {
if ($config->{ NUM_SMTP_LOG_ROTATE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_LOG_ROTATE_TYPE' && $diff->{ SMTP_LOG_ROTATE_TYPE })) {
if ($config->{ SMTP_LOG_ROTATE_TYPE } eq 'day') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTP_LOG_ROTATE_TYPE' && $diff->{ SMTP_LOG_ROTATE_TYPE })) {
if ($config->{ SMTP_LOG_ROTATE_TYPE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_TRACE_SMTP' && $diff->{ NOT_TRACE_SMTP })) {
if ($config->{ NOT_TRACE_SMTP } == 0) {
$s .= sprintf("use_smtp_log = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_TRACE_SMTP' && $diff->{ NOT_TRACE_SMTP })) {
if ($config->{ NOT_TRACE_SMTP } == 1) {
$s .= sprintf("use_smtp_log = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TRACE_SMTP_DELAY' && $diff->{ TRACE_SMTP_DELAY })) {
if ($config->{ TRACE_SMTP_DELAY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SMTP_PROFILE' && $diff->{ USE_SMTP_PROFILE })) {
if ($config->{ USE_SMTP_PROFILE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MCI_SMTP_HOSTS' && $diff->{ MCI_SMTP_HOSTS })) {
if ($config->{ MCI_SMTP_HOSTS }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_RELAY_SERVER' && $diff->{ DEFAULT_RELAY_SERVER })) {
if ($config->{ DEFAULT_RELAY_SERVER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RELAY_HACK' && $diff->{ RELAY_HACK })) {
if ($config->{ RELAY_HACK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CF_DEF' && $diff->{ CF_DEF })) {
if ($config->{ CF_DEF }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_OUTGOING_ADDRESS' && $diff->{ USE_OUTGOING_ADDRESS })) {
if ($config->{ USE_OUTGOING_ADDRESS }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'OUTGOING_ADDRESS' && $diff->{ OUTGOING_ADDRESS })) {
if ($config->{ OUTGOING_ADDRESS }) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_VERP' && $diff->{ USE_VERP })) {
if ($config->{ USE_VERP }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'POSTFIX_VERP_DELIMITERS' && $diff->{ POSTFIX_VERP_DELIMITERS })) {
if ($config->{ POSTFIX_VERP_DELIMITERS }) {
$s .= sprintf("postfix_verp_delimiters = %s", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TRY_VERP_PER_DAY' && $diff->{ TRY_VERP_PER_DAY })) {
if ($config->{ TRY_VERP_PER_DAY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_ESMTP_PIPELINING' && $diff->{ NOT_USE_ESMTP_PIPELINING })) {
if ($config->{ NOT_USE_ESMTP_PIPELINING } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_SMTPFEED_F_OPTION' && $diff->{ USE_SMTPFEED_F_OPTION })) {
if ($config->{ USE_SMTPFEED_F_OPTION }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_MIME' && $diff->{ USE_MIME })) {
if ($config->{ USE_MIME } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_MIME' && $diff->{ USE_MIME })) {
if ($config->{ USE_MIME } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_BROKEN_ENCODING_FIXUP' && $diff->{ MIME_BROKEN_ENCODING_FIXUP })) {
if ($config->{ MIME_BROKEN_ENCODING_FIXUP } == 0) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MIME_DECODED_ARTICLE' && $diff->{ MIME_DECODED_ARTICLE })) {
if ($config->{ MIME_DECODED_ARTICLE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PREAMBLE_MAILBODY' && $diff->{ PREAMBLE_MAILBODY })) {
if ($config->{ PREAMBLE_MAILBODY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TRAILER_MAILBODY' && $diff->{ TRAILER_MAILBODY })) {
if ($config->{ TRAILER_MAILBODY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'GOOD_BYE_PHRASE' && $diff->{ GOOD_BYE_PHRASE })) {
if ($config->{ GOOD_BYE_PHRASE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FACE_MARK' && $diff->{ FACE_MARK })) {
if ($config->{ FACE_MARK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PROC_GEN_INFO' && $diff->{ PROC_GEN_INFO })) {
if ($config->{ PROC_GEN_INFO }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_FLOCK' && $diff->{ USE_FLOCK })) {
if ($config->{ USE_FLOCK } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_FLOCK' && $diff->{ USE_FLOCK })) {
if ($config->{ USE_FLOCK } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MAX_TIMEOUT' && $diff->{ MAX_TIMEOUT })) {
if ($config->{ MAX_TIMEOUT } == 200) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_SPOOL' && $diff->{ NOT_USE_SPOOL })) {
if ($config->{ NOT_USE_SPOOL } == 1) {
$s .= sprintf("use_article_spool = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_SPOOL' && $diff->{ NOT_USE_SPOOL })) {
if ($config->{ NOT_USE_SPOOL } == 0) {
$s .= sprintf("use_article_spool = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMPAT_FML15' && $diff->{ COMPAT_FML15 })) {
if ($config->{ COMPAT_FML15 } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NEWSYSLOG_MAX' && $diff->{ NEWSYSLOG_MAX })) {
if ($config->{ NEWSYSLOG_MAX } == 4) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CRONTAB' && $diff->{ CRONTAB })) {
if ($config->{ CRONTAB } eq 'etc/crontab') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CRON_PIDFILE' && $diff->{ CRON_PIDFILE })) {
if ($config->{ CRON_PIDFILE } eq 'var/run/cron.pid') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CRON_NOTIFY' && $diff->{ CRON_NOTIFY })) {
if ($config->{ CRON_NOTIFY } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_CROSSPOST' && $diff->{ USE_CROSSPOST })) {
if ($config->{ USE_CROSSPOST }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_MEMBER_NAME' && $diff->{ USE_MEMBER_NAME })) {
if ($config->{ USE_MEMBER_NAME }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_EXPIRE' && $diff->{ USE_EXPIRE })) {
if ($config->{ USE_EXPIRE } == 0) {
$s .= sprintf("use_article_expire = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_EXPIRE' && $diff->{ USE_EXPIRE })) {
if ($config->{ USE_EXPIRE } == 1) {
$s .= sprintf("use_article_expire = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'EXPIRE_SUMMARY' && $diff->{ EXPIRE_SUMMARY })) {
if ($config->{ EXPIRE_SUMMARY } == 0) {
$s .= sprintf("use_article_summary_file_expire = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'EXPIRE_SUMMARY' && $diff->{ EXPIRE_SUMMARY })) {
if ($config->{ EXPIRE_SUMMARY } == 1) {
$s .= sprintf("use_article_summary_file_expire = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'EXPIRE_LIMIT' && $diff->{ EXPIRE_LIMIT })) {
if ($config->{ EXPIRE_LIMIT } eq '7days') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_ARCHIVE' && $diff->{ USE_ARCHIVE })) {
if ($config->{ USE_ARCHIVE } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ARCHIVE_UNIT' && $diff->{ ARCHIVE_UNIT })) {
if ($config->{ ARCHIVE_UNIT } == 100) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_ARCHIVE_UNIT' && $diff->{ DEFAULT_ARCHIVE_UNIT })) {
if ($config->{ DEFAULT_ARCHIVE_UNIT } == 100) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ARCHIVE_DIR' && $diff->{ ARCHIVE_DIR })) {
if ($config->{ ARCHIVE_DIR } eq 'var/archive') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'INDEX_FILE' && $diff->{ INDEX_FILE })) {
if ($config->{ INDEX_FILE } eq '$DIR/index') {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'INDEX_SHOW_DIRNAME' && $diff->{ INDEX_SHOW_DIRNAME })) {
if ($config->{ INDEX_SHOW_DIRNAME } == 0) {
$s .= &$fp_rule_not_yet_implemented($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIBRARY_DIR' && $diff->{ LIBRARY_DIR })) {
if ($config->{ LIBRARY_DIR } eq 'var/library') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIBRARY_ARCHIVE_DIR' && $diff->{ LIBRARY_ARCHIVE_DIR })) {
if ($config->{ LIBRARY_ARCHIVE_DIR } eq 'archive') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOGFILE_NEWSYSLOG_LIMIT' && $diff->{ LOGFILE_NEWSYSLOG_LIMIT })) {
if ($config->{ LOGFILE_NEWSYSLOG_LIMIT }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AMLIST_NEWSYSLOG_LIMIT' && $diff->{ AMLIST_NEWSYSLOG_LIMIT })) {
if ($config->{ AMLIST_NEWSYSLOG_LIMIT } eq '150K') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_HTML_GEN' && $diff->{ AUTO_HTML_GEN })) {
if ($config->{ AUTO_HTML_GEN } == 1) {
$s .= sprintf("use_html_archive = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AUTO_HTML_GEN' && $diff->{ AUTO_HTML_GEN })) {
if ($config->{ AUTO_HTML_GEN } == 0) {
$s .= sprintf("use_html_archive = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_NEW_HTML_GEN' && $diff->{ USE_NEW_HTML_GEN })) {
if ($config->{ USE_NEW_HTML_GEN } == 1) {
$s .= sprintf("use_html_archive = yes", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_NEW_HTML_GEN' && $diff->{ USE_NEW_HTML_GEN })) {
if ($config->{ USE_NEW_HTML_GEN } == 0) {
$s .= sprintf("use_html_archive = no", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD' && $diff->{ HTML_THREAD })) {
if ($config->{ HTML_THREAD } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD' && $diff->{ HTML_THREAD })) {
if ($config->{ HTML_THREAD } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_INDEX_REVERSE_ORDER' && $diff->{ HTML_INDEX_REVERSE_ORDER })) {
if ($config->{ HTML_INDEX_REVERSE_ORDER } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_INDEX_REVERSE_ORDER' && $diff->{ HTML_INDEX_REVERSE_ORDER })) {
if ($config->{ HTML_INDEX_REVERSE_ORDER } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_DIR' && $diff->{ HTML_DIR })) {
if ($config->{ HTML_DIR } eq 'htdocs') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_EXPIRE_LIMIT' && $diff->{ HTML_EXPIRE_LIMIT })) {
if ($config->{ HTML_EXPIRE_LIMIT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_INDEX_TITLE' && $diff->{ HTML_INDEX_TITLE })) {
if ($config->{ HTML_INDEX_TITLE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_DATA_CACHE' && $diff->{ HTML_DATA_CACHE })) {
if ($config->{ HTML_DATA_CACHE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_DATA_THREAD' && $diff->{ HTML_DATA_THREAD })) {
if ($config->{ HTML_DATA_THREAD }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_OUTPUT_FILTER' && $diff->{ HTML_OUTPUT_FILTER })) {
if ($config->{ HTML_OUTPUT_FILTER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_STYLESHEET_BASENAME' && $diff->{ HTML_STYLESHEET_BASENAME })) {
if ($config->{ HTML_STYLESHEET_BASENAME }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD_REF_TYPE' && $diff->{ HTML_THREAD_REF_TYPE })) {
if ($config->{ HTML_THREAD_REF_TYPE } eq 'prefer-in-reply-to') {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD_REF_TYPE' && $diff->{ HTML_THREAD_REF_TYPE })) {
if ($config->{ HTML_THREAD_REF_TYPE } eq 'default') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD_SORT_TYPE' && $diff->{ HTML_THREAD_SORT_TYPE })) {
if ($config->{ HTML_THREAD_SORT_TYPE } eq 'reverse-number') {
$s .= sprintf("html_archive_index_order_type = reverse", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_THREAD_SORT_TYPE' && $diff->{ HTML_THREAD_SORT_TYPE })) {
if ($config->{ HTML_THREAD_SORT_TYPE } eq 'NULL') {
$s .= sprintf("html_archive_index_order_type = normal", $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_INDEX_UNIT' && $diff->{ HTML_INDEX_UNIT })) {
if ($config->{ HTML_INDEX_UNIT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_INDENT_STYLE' && $diff->{ HTML_INDENT_STYLE })) {
if ($config->{ HTML_INDENT_STYLE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_MULTIPART_IMAGE_REF_TYPE' && $diff->{ HTML_MULTIPART_IMAGE_REF_TYPE })) {
if ($config->{ HTML_MULTIPART_IMAGE_REF_TYPE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_DEFAULT_UMASK' && $diff->{ HTML_DEFAULT_UMASK })) {
if ($config->{ HTML_DEFAULT_UMASK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HTML_WRITE_UMASK' && $diff->{ HTML_WRITE_UMASK })) {
if ($config->{ HTML_WRITE_UMASK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_DATABASE' && $diff->{ USE_DATABASE })) {
if ($config->{ USE_DATABASE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATABASE_METHOD' && $diff->{ DATABASE_METHOD })) {
if ($config->{ DATABASE_METHOD }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATABASE_CACHE_FILE_SUFFIX' && $diff->{ DATABASE_CACHE_FILE_SUFFIX })) {
if ($config->{ DATABASE_CACHE_FILE_SUFFIX }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATABASE_DRIVER' && $diff->{ DATABASE_DRIVER })) {
if ($config->{ DATABASE_DRIVER } eq 'toymodel.pl') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DATABASE_DRIVER_ATTRIBUTES' && $diff->{ DATABASE_DRIVER_ATTRIBUTES })) {
if ($config->{ DATABASE_DRIVER_ATTRIBUTES } eq 'always_lower_domain') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_SERVER_HOST' && $diff->{ SQL_SERVER_HOST })) {
if ($config->{ SQL_SERVER_HOST }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_SERVER_PORT' && $diff->{ SQL_SERVER_PORT })) {
if ($config->{ SQL_SERVER_PORT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_SERVER_USER' && $diff->{ SQL_SERVER_USER })) {
if ($config->{ SQL_SERVER_USER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_DATABASE_NAME' && $diff->{ SQL_DATABASE_NAME })) {
if ($config->{ SQL_DATABASE_NAME }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_SERVER_PASSWORD' && $diff->{ SQL_SERVER_PASSWORD })) {
if ($config->{ SQL_SERVER_PASSWORD }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SQL_DATABASE_NAME' && $diff->{ SQL_DATABASE_NAME })) {
if ($config->{ SQL_DATABASE_NAME }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LDAP_SERVER_HOST' && $diff->{ LDAP_SERVER_HOST })) {
if ($config->{ LDAP_SERVER_HOST }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LDAP_SERVER_PASSWORD' && $diff->{ LDAP_SERVER_PASSWORD })) {
if ($config->{ LDAP_SERVER_PASSWORD }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LDAP_SEARCH_BASE' && $diff->{ LDAP_SEARCH_BASE })) {
if ($config->{ LDAP_SEARCH_BASE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LDAP_SERVER_BIND' && $diff->{ LDAP_SERVER_BIND })) {
if ($config->{ LDAP_SERVER_BIND }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LDAP_QUERY_FILTER' && $diff->{ LDAP_QUERY_FILTER })) {
if ($config->{ LDAP_QUERY_FILTER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_WHOIS' && $diff->{ USE_WHOIS })) {
if ($config->{ USE_WHOIS }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_WHOIS_SERVER' && $diff->{ DEFAULT_WHOIS_SERVER })) {
if ($config->{ DEFAULT_WHOIS_SERVER }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'WHOIS_DB' && $diff->{ WHOIS_DB })) {
if ($config->{ WHOIS_DB } eq '$VARDB_DIR/whoisdb') {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'WHOIS_HELP_FILE' && $diff->{ WHOIS_HELP_FILE })) {
if ($config->{ WHOIS_HELP_FILE }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'WHOIS_JCODE_P' && $diff->{ WHOIS_JCODE_P })) {
if ($config->{ WHOIS_JCODE_P } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CPU_TYPE_MANUFACTURER_OS' && $diff->{ CPU_TYPE_MANUFACTURER_OS })) {
if ($config->{ CPU_TYPE_MANUFACTURER_OS }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'STRUCT_SOCKADDR' && $diff->{ STRUCT_SOCKADDR })) {
if ($config->{ STRUCT_SOCKADDR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_SH' && $diff->{ LOCK_SH })) {
if ($config->{ LOCK_SH }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_EX' && $diff->{ LOCK_EX })) {
if ($config->{ LOCK_EX }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_NB' && $diff->{ LOCK_NB })) {
if ($config->{ LOCK_NB }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOCK_UN' && $diff->{ LOCK_UN })) {
if ($config->{ LOCK_UN }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMPAT_SOLARIS2' && $diff->{ COMPAT_SOLARIS2 })) {
if ($config->{ COMPAT_SOLARIS2 }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'NOT_USE_TIOCNOTTY' && $diff->{ NOT_USE_TIOCNOTTY })) {
if ($config->{ NOT_USE_TIOCNOTTY }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HAS_GETPWUID' && $diff->{ HAS_GETPWUID })) {
if ($config->{ HAS_GETPWUID }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HAS_GETPWGID' && $diff->{ HAS_GETPWGID })) {
if ($config->{ HAS_GETPWGID }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HAS_ALARM' && $diff->{ HAS_ALARM })) {
if ($config->{ HAS_ALARM }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'UNISTD' && $diff->{ UNISTD })) {
if ($config->{ UNISTD }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SENDMAIL' && $diff->{ SENDMAIL })) {
if ($config->{ SENDMAIL }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'TAR' && $diff->{ TAR })) {
if ($config->{ TAR }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'UUENCODE' && $diff->{ UUENCODE })) {
if ($config->{ UUENCODE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'COMPRESS' && $diff->{ COMPRESS })) {
if ($config->{ COMPRESS }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ZCAT' && $diff->{ ZCAT })) {
if ($config->{ ZCAT }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LHA' && $diff->{ LHA })) {
if ($config->{ LHA }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ISH' && $diff->{ ISH })) {
if ($config->{ ISH }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ZIP' && $diff->{ ZIP })) {
if ($config->{ ZIP }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'BZIP2' && $diff->{ BZIP2 })) {
if ($config->{ BZIP2 }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGP' && $diff->{ PGP })) {
if ($config->{ PGP }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGP5' && $diff->{ PGP5 })) {
if ($config->{ PGP5 }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGPE' && $diff->{ PGPE })) {
if ($config->{ PGPE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGPK' && $diff->{ PGPK })) {
if ($config->{ PGPK }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGPS' && $diff->{ PGPS })) {
if ($config->{ PGPS }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PGPV' && $diff->{ PGPV })) {
if ($config->{ PGPV }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'GPG' && $diff->{ GPG })) {
if ($config->{ GPG }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RCS' && $diff->{ RCS })) {
if ($config->{ RCS }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CI' && $diff->{ CI })) {
if ($config->{ CI }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'BASE64_DECODE' && $diff->{ BASE64_DECODE })) {
if ($config->{ BASE64_DECODE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'BASE64_ENCODE' && $diff->{ BASE64_ENCODE })) {
if ($config->{ BASE64_ENCODE }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'MD5' && $diff->{ MD5 })) {
if ($config->{ MD5 }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SMTPLOG' && $diff->{ SMTPLOG })) {
if ($config->{ SMTPLOG }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'PROHIBIT_COMMAND_FOR_STRANGER' && $diff->{ PROHIBIT_COMMAND_FOR_STRANGER })) {
if ($config->{ PROHIBIT_COMMAND_FOR_STRANGER }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_LIBMIME' && $diff->{ USE_LIBMIME })) {
if ($config->{ USE_LIBMIME } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'USE_LIBMIME' && $diff->{ USE_LIBMIME })) {
if ($config->{ USE_LIBMIME } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LIBMIMEDIR' && $diff->{ LIBMIMEDIR })) {
if ($config->{ LIBMIMEDIR }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RPG_ML_FORM_FLAG' && $diff->{ RPG_ML_FORM_FLAG })) {
if ($config->{ RPG_ML_FORM_FLAG } == 1) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RPG_ML_FORM_FLAG' && $diff->{ RPG_ML_FORM_FLAG })) {
if ($config->{ RPG_ML_FORM_FLAG } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUN_OS_413' && $diff->{ SUN_OS_413 })) {
if ($config->{ SUN_OS_413 } == 1) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUN_OS_413' && $diff->{ SUN_OS_413 })) {
if ($config->{ SUN_OS_413 } == 0) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'SUBJECT_HML_FORM' && $diff->{ SUBJECT_HML_FORM })) {
if ($config->{ SUBJECT_HML_FORM }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'HML_FORM_LONG_ID' && $diff->{ HML_FORM_LONG_ID })) {
if ($config->{ HML_FORM_LONG_ID }) {
$s .= &$fp_rule_convert($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'ML_MEMBER_CHECK' && $diff->{ ML_MEMBER_CHECK })) {
if ($config->{ ML_MEMBER_CHECK }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_HTTP_PORT' && $diff->{ DEFAULT_HTTP_PORT })) {
if ($config->{ DEFAULT_HTTP_PORT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_GOPHER_PORT' && $diff->{ DEFAULT_GOPHER_PORT })) {
if ($config->{ DEFAULT_GOPHER_PORT }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'DEFAULT_HTML_FIELD' && $diff->{ DEFAULT_HTML_FIELD })) {
if ($config->{ DEFAULT_HTML_FIELD }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'CP' && $diff->{ CP })) {
if ($config->{ CP }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'RM' && $diff->{ RM })) {
if ($config->{ RM }) {
$s .= &$fp_rule_prefer_fml8_value($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'FML' && $diff->{ FML })) {
if ($config->{ FML }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'LOAD_LIBRARY' && $diff->{ LOAD_LIBRARY })) {
if ($config->{ LOAD_LIBRARY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'STORED_BOUNDARY' && $diff->{ STORED_BOUNDARY })) {
if ($config->{ STORED_BOUNDARY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq 'AGAINST_NIFTY' && $diff->{ AGAINST_NIFTY })) {
if ($config->{ AGAINST_NIFTY }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq '_Ds' && $diff->{ _Ds })) {
if ($config->{ _Ds }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
$s = undef;
if (($key eq '_Dm' && $diff->{ _Dm })) {
if ($config->{ _Dm }) {
$s .= &$fp_rule_ignore($self, $config, $diff, $key, $value);
}
}
return $s if defined $s;
return '';
}
1;
