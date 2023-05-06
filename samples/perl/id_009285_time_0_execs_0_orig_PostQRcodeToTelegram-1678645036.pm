package Mojo::Webqq::Plugin::PostQRcodeToTelegram;
our $PRIORITY = 0;
our $CALL_ON_LOAD = 1;
my @qrcode_message_ids;
sub call{
my $client = shift;
my $data = shift;
$client->on(input_qrcode=>sub{
my($client,$qrcode_path) = @_;
my $telegram_api = 'https://api.telegram.org/bot' . $data->{api_key} .'/sendPhoto';
my $response = $client->http_post($telegram_api,{json=>1},form=>{
chat_id => $data->{chat_id},
caption => 'QQ帐号' .(defined $client->uid?$client->uid:$client->account) .'登录二维码',
photo=>{file=>$qrcode_path}
});
if(not defined $response){
$client->warn("插件[".__PACKAGE__ . "]发送登录二维码失败，响应数据异常");
return
}
if (not $response->{"ok"}) {
$client->warn("插件[".__PACKAGE__ . "]发送登录二维码失败，错误原因：". $response->{"description"});
return
}
push @qrcode_message_ids, $response->{"result"}->{"message_id"};
my $chat = $response->{"result"}->{"chat"};
my $chat_type = $chat->{"type"};
if ($chat_type eq "private") {
$client->info("插件[".__PACKAGE__ . "]二维码已发送给Telegram用户[ ". $chat->{"username"} . " ]");
}
elsif ($chat_type eq "group" or $chat_type eq "supergroup") {
$client->info("插件[".__PACKAGE__ . "]二维码已发送至Telegram群组[ ". $chat->{"title"} . " ]");
}
elsif ($chat_type eq "channel") {
$client->info("插件[".__PACKAGE__ . "]二维码已发送至Telegram频道[ ". $chat->{"title"} . " ]");
} else {
$client->info("插件[".__PACKAGE__ . "]二维码已发送，目标未知");
}
});
$client->on(qrcode_expire=>sub{
my $last_id = $qrcode_message_ids[-1];
my $telegram_api = 'https://api.telegram.org/bot' . $data->{api_key};
my $response = $client->http_post($telegram_api . '/editMessageCaption',{json=>1},form=>{
chat_id => $data->{chat_id},
message_id => $last_id,
caption => '二维码已过期',
});
if(not defined $response){
$client->warn("插件[".__PACKAGE__ . "]提示二维码过期失败，响应数据异常");
return
}
if (not $response->{"ok"}) {
$client->warn("插件[".__PACKAGE__ . "]提示二维码过期失败，错误原因：". $response->{"description"});
return
}
});
$client->on(login=>sub{
my $telegram_api = 'https://api.telegram.org/bot' . $data->{api_key};
foreach my $message_id (@qrcode_message_ids) {
$client->http_post($telegram_api . '/deleteMessage',{json=>1},form=>{
chat_id => $data->{chat_id},
message_id => $message_id,
});
}
@qrcode_message_ids = ();
$client->http_post($telegram_api . '/sendMessage',{json=>1},form=>{
chat_id => $data->{chat_id},
text => "登录成功",
});
});
}
1;
