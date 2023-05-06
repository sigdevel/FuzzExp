my $ip = '10.0.0.2/24';
my $gw = '10.0.0.1';
my $ip6 = 'fc05::1:2/112';
my $gw6 = 'fc05::1:1';
r(load('base'));
new_iface('vmbr0', 'bridge', [{ family => 'inet' }], autostart => 1, bridge_ports => 'eth0');
expect load('base') . <<"EOF";
auto vmbr0
iface vmbr0 inet manual
bridge-ports eth0
bridge-stp off
bridge-fd 0
EOF
update_iface('vmbr0',
[ { family => 'inet',
address => $ip,
gateway => $gw } ],
autostart => 0);
expect load('base') . <<"EOF";
iface vmbr0 inet static
address $ip
gateway $gw
bridge-ports eth0
bridge-stp off
bridge-fd 0
EOF
save('with-ipv4', w());
update_iface('vmbr0',
[ { family => 'inet6',
address => $ip6,
gateway => $gw6 } ]);
expect load('with-ipv4') . <<"EOF";
iface vmbr0 inet6 static
address $ip6
gateway $gw6
EOF
save('idem', w());
r(load('idem'));
expect load('idem');
delete_iface('vmbr0', 'inet');
expect load('base') . <<"EOF";
iface vmbr0 inet6 static
address $ip6
gateway $gw6
bridge-ports eth0
bridge-stp off
bridge-fd 0
EOF
save('idem', w());
r(load('idem'));
expect load('idem');
delete_iface('vmbr0');
expect load('base');
1;
