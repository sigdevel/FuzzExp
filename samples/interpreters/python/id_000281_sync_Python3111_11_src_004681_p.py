




























































































































import unittest
import pytest

import azure.mgmt.network
from devtools_testutils import AzureMgmtTestCase, RandomNameResourceGroupPreparer, StorageAccountPreparer

AZURE_LOCATION = 'eastus'

@pytest.mark.live_test_only
class MgmtNetworkTest(AzureMgmtTestCase):

    def setUp(self):
        super(MgmtNetworkTest, self).setUp()
        self.mgmt_client = self.create_mgmt_client(
            azure.mgmt.network.NetworkManagementClient
        )
    

        if self.is_live:
            from azure.mgmt.compute import ComputeManagementClient
            self.compute_client = self.create_mgmt_client(
                ComputeManagementClient
            )
            from azure.mgmt.storage import StorageManagementClient
            self.storage_client = self.create_mgmt_client(
                StorageManagementClient
            )

    def create_vm(self, group_name, location, vm_name, nic_id):
        
        BODY = {
          "location": location,
          "hardware_profile": {
            "vm_size": "Standard_D2_v2"
          },
          "storage_profile": {
            "image_reference": {
              "sku": "enterprise",
              "publisher": "microsoftsqlserver",
              "version": "latest",
              "offer": "sql2019-ws2019"
            },
            "os_disk": {
              "caching": "ReadWrite",
              "managed_disk": {
                "storage_account_type": "Standard_LRS"
              },
              "name": "myVMosdisk",
              "create_option": "FromImage"
            },
            "data_disks": [
              {
                "disk_size_gb": "1023",
                "create_option": "Empty",
                "lun": "0"
              },
              {
                "disk_size_gb": "1023",
                "create_option": "Empty",
                "lun": "1"
              }
            ]
          },
          "os_profile": {
            "admin_username": "testuser",
            "admin_password": "Password1!!!",
            "computer_name" : "myvm"
          },
          "network_profile": {
            "network_interfaces": [
              {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NIC_ID + "",
                "id": nic_id,
                "properties": {
                  "primary": True
                }
              }
            ]
          }
        }
        result = self.compute_client.virtual_machines.create_or_update(group_name, vm_name, BODY)
        result = result.result()

    def create_storage_account(self, group_name, location, storage_name):
        BODY = {
          "sku": {
            "name": "Standard_GRS"
          },
          "kind": "StorageV2",
          "location": AZURE_LOCATION,
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          }
        }
        result_create = self.storage_client.storage_accounts.create(
            group_name,
            storage_name,
            BODY
        )
        result = result_create.result()
        print(result)

    def get_storage_key(self, group_name, storage_name):
        result = self.storage_client.storage_accounts.list_keys(group_name, storage_name)
        print(result)
        return result.keys[0].value

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @StorageAccountPreparer(location=AZURE_LOCATION, name_prefix='gentest')
    def test_network(self, resource_group, storage_account):

        SUBSCRIPTION_ID = self.settings.SUBSCRIPTION_ID
        TENANT_ID = self.settings.TENANT_ID
        RESOURCE_GROUP = resource_group.name
        APPLICATION_GATEWAY_NAME = "myApplicationGateway"
        VIRTUAL_NETWORK_NAME = "myVirtualNetwork"
        SUBNET_NAME = "mySubnet"
        FRONTEND_IP_CONFIGURATION_NAME = "myFrontendIpConfiguration"
        PUBLIC_IP_ADDRESS_NAME = "myPublicIpAddress"
        BACKEND_ADDRESS_POOL_NAME = "myBackendAddressPoolName"
        TRUSTED_CLIENT_CERTIFICATE_NAME = "myTrustedClientCertificate"
        FRONTEND_PORT_NAME = "myFrontendPort"
        SSL_CERTIFICATE_NAME = "mySslCertificate"
        SSL_PROFILE_NAME = "mySslProfile"
        BACKEND_HTTP_SETTINGS_COLLECTION_NAME = "myBackendHttpSettingsCollection"
        REWRITE_RULE_SET_NAME = "myRewriteRuleSet"
        HTTP_LISTENER_NAME = "myHttpListener"
        URL_PATH_MAP_NAME = "myUrlPathMap"
        APPLICATION_GATEWAY_AVAILABLE_SSL_OPTION_NAME = "myApplicationGatewayAvailableSslOption"
        PREDEFINED_POLICY_NAME = "myPredefinedPolicy"
        CONNECTION_NAME = "myConnection"
        PRIVATE_ENDPOINT_NAME = "myPrivateEndpoint"
        APPLICATION_SECURITY_GROUP_NAME = "myApplicationSecurityGroup"
        AZURE_FIREWALL_NAME = "myAzureFirewall"
        VIRTUAL_HUB_NAME = "myVirtualHub"
        FIREWALL_POLICY_NAME = "myFirewallPolicy"
        BASTION_HOST_NAME = "myBastionHost"
        VIRTUAL_WAN_NAME = "myVirtualWan"
        CUSTOM_IP_PREFIX_NAME = "myCustomIpPrefix"
        DDOS_CUSTOM_POLICY_NAME = "myDdosCustomPolicy"
        DDOS_PROTECTION_PLAN_NAME = "myDdosProtectionPlan"
        DSCP_CONFIGURATION_NAME = "myDscpConfiguration"
        CIRCUIT_NAME = "myCircuit"
        AUTHORIZATION_NAME = "myAuthorization"
        PEERING_NAME = "AzurePrivatePeering"
        EXPRESS_ROUTE_CIRCUIT_NAME = "myExpressRouteCircuit"
        EXPRESS_ROUTE_PORT_NAME = "myExpressRoutePort"
        DEVICE_PATH = "myDevicePath"
        CROSS_CONNECTION_NAME = "myCrossConnection"
        LOCATION_NAME = "myLocation"
        LINK_NAME = "myLink"
        RULE_COLLECTION_GROUP_NAME = "myRuleCollectionGroup"
        IP_ALLOCATION_NAME = "myIpAllocation"
        IP_GROUPS_NAME = "myIpGroups"
        LOAD_BALANCER_NAME = "myLoadBalancer"
        PROBE_NAME = "myProbe"
        INBOUND_NAT_RULE_NAME = "myInboundNatRuleName"
        INBOUND_NAT_POOL_NAME = "myInboundNatPool"
        LOAD_BALANCING_RULE_NAME = "myLoadBalancingRule"
        OUTBOUND_RULE_NAME = "myOutboundRule"
        NAT_GATEWAY_NAME = "myNatGateway"
        PUBLIC_IP_PREFIX_NAME = "myPublicIpPrefix"
        NETWORK_INTERFACE_NAME = "myNetworkInterface"
        VIRTUAL_MACHINE_SCALE_SET_NAME = "myVirtualMachineScaleSet"
        VIRTUALMACHINE_INDEX = "myVirtualmachineIndex"
        IP_CONFIGURATION_NAME = "myIpConfiguration"
        TAP_CONFIGURATION_NAME = "myTapConfiguration"
        VIRTUAL_NETWORK_TAP_NAME = "myVirtualNetworkTap"
        NETWORK_PROFILE_NAME = "myNetworkProfile"
        NETWORK_SECURITY_GROUP_NAME = "myNetworkSecurityGroup"
        SECURITY_RULE_NAME = "mySecurityRule"
        DEFAULT_SECURITY_RULE_NAME = "myDefaultSecurityRule"
        NETWORK_VIRTUAL_APPLIANCE_NAME = "myNetworkVirtualAppliance"
        SITE_NAME = "mySite"
        SKU_NAME = "mySku"
        RULE_COLLECTION_NAME = "myRuleCollection"
        NETWORK_WATCHER_NAME = "myNetworkWatcher"
        PACKET_CAPTURE_NAME = "myPacketCapture"
        VIRTUAL_MACHINE_NAME = "myVirtualMachine"
        STORAGE_ACCOUNT_NAME = "myStorageAccount"
        CONNECTION_MONITOR_NAME = "myConnectionMonitor"
        WORKSPACE_NAME = "myWorkspace"
        FLOW_LOG_NAME = "myFlowLog"
        PRIVATE_LINK_SERVICE_NAME = "myPrivateLinkService"
        PRIVATE_DNS_ZONE_GROUP_NAME = "myPrivateDnsZoneGroup"
        PRIVATE_DNS_ZONE_NAME = "myPrivateDnsZone"
        SERVICE_NAME = "myService"
        PE_CONNECTION_NAME = "myPeConnection"
        ROUTE_FILTER_NAME = "myRouteFilter"
        RULE_NAME = "myRule"
        ROUTE_TABLE_NAME = "myRouteTable"
        ROUTE_NAME = "myRoute"
        SECURITY_PARTNER_PROVIDER_NAME = "mySecurityPartnerProvider"
        SERVICE_ENDPOINT_POLICY_NAME = "myServiceEndpointPolicy"
        SERVICE_ENDPOINT_POLICY_DEFINITION_NAME = "myServiceEndpointPolicyDefinition"
        VIRTUAL_NETWORK_PEERING_NAME = "myVirtualNetworkPeering"
        VIRTUAL_NETWORK_GATEWAY_NAME = "myVirtualNetworkGateway"
        VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME = "myVirtualNetworkGatewayConnection"
        LOCAL_NETWORK_GATEWAY_NAME = "myLocalNetworkGateway"
        SHAREDKEY_NAME = "mySharedkey"
        TAP_NAME = "myTap"
        VIRTUAL_ROUTER_NAME = "myVirtualRouter"
        VPN_SITE_NAME = "myVpnSite"
        VPN_SITE_LINK_NAME = "myVpnSiteLink"
        VPN_SERVER_CONFIGURATION_NAME = "myVpnServerConfiguration"
        HUB_ROUTE_TABLE_NAME = "myHubRouteTable"
        GATEWAY_NAME = "myGateway"
        VPN_CONNECTION_NAME = "myVpnConnection"
        LINK_CONNECTION_NAME = "myLinkConnection"
        P2S_VPN_GATEWAY_NAME = "myP2sVpnGateway"
        P2S_CONNECTION_CONFIGURATION_NAME = "myP2sConnectionConfiguration"
        EXPRESS_ROUTE_GATEWAY_NAME = "myExpressRouteGateway"
        EXPRESS_ROUTE_CONNECTION_NAME = "myExpressRouteConnection"
        HUB_NAME = "myHub"
        IP_CONFIG_NAME = "myIpConfig"
        POLICY_NAME = "myPolicy"
        STORAGE_ACCOUNT_NAME = storage_account.name


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "virtual_wan": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualWANs/" + VIRTUAL_WAN_NAME
          },
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "is_security_site": False,
          "vpn_site_links": [
            {
              "name": "vpnSiteLink1",
              "ip_address": "50.50.50.56",
              "fqdn": "link1.vpnsite1.contoso.com",
              "link_properties": {
                "link_provider_name": "vendor1",
                "link_speed_in_mbps": "0"
              },
              "bgp_properties": {
                "bgp_peering_address": "192.168.0.0",
                "asn": "1234"
              }
            }
          ],
          "o365policy": {
            "break_out_categories": {
              "allow": True,
              "optimize": True,
              "default": False
            }
          }
        }
        result = self.mgmt_client.vpn_sites.begin_create_or_update(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME, vpn_site_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "ip_addresses": [
            "13.64.39.16/32",
            "40.74.146.80/31",
            "40.74.147.32/28"
          ]
        }
        result = self.mgmt_client.ip_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          },
          "connections": [
            {
              "name": "vpnConnection1",
              "remote_vpn_site": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE_NAME
              },
              "vpn_link_connections": [
                {
                  "name": "Connection-Link1",
                  "vpn_site_link": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE_NAME + "/vpnSiteLinks/" + VPN_SITE_LINK_NAME
                  },
                  "connection_bandwidth": "200",
                  "vpn_connection_protocol_type": "IKEv2",
                  "shared_key": "key"
                }
              ]
            }
          ],
          "bgp_settings": {
            "asn": "65515",
            "peer_weight": "0",
            "bgp_peering_addresses": [
              {
                "ip_configuration_id": "Instance0",
                "custom_bgp_ip_addresses": [
                  "169.254.21.5"
                ]
              },
              {
                "ip_configuration_id": "Instance1",
                "custom_bgp_ip_addresses": [
                  "169.254.21.10"
                ]
              }
            ]
          }
        }
        result = self.mgmt_client.vpn_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, vpn_gateway_parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          },
          "vpn_server_configuration": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnServerConfigurations/" + VPN_SERVER_CONFIGURATION_NAME
          },
          "p2sconnection_configurations": [
            {
              "name": "P2SConnectionConfig1",
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/p2sVpnGateways/" + P2S_VPN_GATEWAY_NAME + "/p2sConnectionConfigurations/" + P2S_CONNECTION_CONFIGURATION_NAME,
              "vpn_client_address_pool": {
                "address_prefixes": [
                  "101.3.0.0/16"
                ]
              }
            }
          ],
          "vpn_gateway_scale_unit": "1",
          "custom_dns_servers": [
            "1.1.1.1",
            "2.2.2.2"
          ]
        }
        result = self.mgmt_client.p2s_vpn_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, p2svpn_gateway_parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "destination_network_interface_ip_configuration": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NETWORK_INTERFACE_NAME + "/ipConfigurations/" + IP_CONFIGURATION_NAME
          }
        }
        result = self.mgmt_client.virtual_network_taps.begin_create_or_update(resource_group_name=RESOURCE_GROUP, tap_name=TAP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "virtual_wan": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualWans/" + VIRTUAL_WAN_NAME
          },
          "address_prefix": "10.168.0.0/24",
          "sku": "Basic"
        }
        result = self.mgmt_client.virtual_hubs.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, virtual_hub_parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "disable_vpn_encryption": False,
          "type": "Basic"
        }
        result = self.mgmt_client.virtual_wans.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, wan_parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "disable_bgp_route_propagation": True,
          "routes": [
            {
              "name": "route1",
              "address_prefix": "10.0.3.0/24",
              "next_hop_type": "VirtualNetworkGateway"
            }
          ]
        }
        result = self.mgmt_client.route_tables.begin_create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.route_tables.begin_create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "public_ip_addresses": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
            }
          ],
          "public_ip_prefixes": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPPrefixes/" + PUBLIC_IP_PREFIX_NAME
            }
          ]
        }
        result = self.mgmt_client.nat_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "rules": [
            {
              "name": "ruleName",
              "access": "Allow",
              "route_filter_rule_type": "Community",
              "communities": [
                "12076:5030",
                "12076:5040"
              ]
            }
          ]
        }
        result = self.mgmt_client.route_filters.begin_create_or_update(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, route_filter_parameters=BODY)
        result = result.result()


        

        BODY = {
          "ip_configurations": [
            {
              "name": "bastionHostIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.bastion_hosts.begin_create_or_update(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "visibility": {
            "subscriptions": [
              "subscription1",
              "subscription2",
              "subscription3"
            ]
          },
          "auto_approval": {
            "subscriptions": [
              "subscription1",
              "subscription2"
            ]
          },
          "fqdns": [
            "fqdn1",
            "fqdn2",
            "fqdn3"
          ],
          "load_balancer_frontend_ip_configurations": [
            {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
            }
          ],
          "ip_configurations": [
            {
              "name": "fe-lb",
              "private_ip_address": "10.0.1.4",
              "private_ipallocation_method": "Static",
              "private_ip_address_version": "IPv4",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.private_link_services.begin_create_or_update(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "backend_address_pools": [
            {
              "name": BACKEND_ADDRESS_POOL_NAME
            }
          ],
          "load_balancing_rules": [
            {
              "name": "rulelb",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "probe": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
              },
              "protocol": "Tcp",
              "load_distribution": "Default",
              "frontend_port": "80",
              "backend_port": "80",
              "idle_timeout_in_minutes": "15",
              "enable_floating_ip": True,
              "disable_outbound_snat": True
            }
          ],
          "probes": [
            {
              "name": PROBE_NAME,
              "protocol": "Http",
              "port": "80",
              "request_path": "healthcheck.aspx",
              "interval_in_seconds": "15",
              "number_of_probes": "2"
            }
          ],
          "inbound_nat_rules": [
            {
              "name": INBOUND_NAT_RULE_NAME,
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "3389",
              "backend_port": "3389",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp"
            }
          ],
          "inbound_nat_pools": [],
          "outbound_rules": [
            {
              "name": "rule1",
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "frontend_ip_configurations": [
                {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
                }
              ],
              "protocol": "All"
            }
          ]
        }
        result = self.mgmt_client.load_balancers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "zones": [],
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME,
              "private_ipallocation_method": "Dynamic",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ],
          "backend_address_pools": [],
          "load_balancing_rules": [],
          "probes": [],
          "inbound_nat_rules": [],
          "outbound_rules": [],
          "inbound_nat_pools": [
            {
              "name": "test",
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/inboundNatPools/" + INBOUND_NAT_POOL_NAME,
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "protocol": "Tcp",
              "frontend_port_range_start": "8080",
              "frontend_port_range_end": "8085",
              "backend_port": "8888",
              "idle_timeout_in_minutes": "10",
              "enable_floating_ip": True,
              "enable_tcp_reset": True
            }
          ]
        }
        result = self.mgmt_client.load_balancers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "zones": [
                "1"
              ],
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ],
          "backend_address_pools": [
            {
              "name": BACKEND_ADDRESS_POOL_NAME
            }
          ],
          "load_balancing_rules": [
            {
              "name": "rulelb",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "80",
              "backend_port": "80",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp",
              "load_distribution": "Default",
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "probe": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
              }
            }
          ],
          "probes": [
            {
              "name": PROBE_NAME,
              "protocol": "Http",
              "port": "80",
              "request_path": "healthcheck.aspx",
              "interval_in_seconds": "15",
              "number_of_probes": "2"
            }
          ],
          "inbound_nat_rules": [
            {
              "name": INBOUND_NAT_RULE_NAME,
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "3389",
              "backend_port": "3389",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp"
            }
          ],
          "inbound_nat_pools": [],
          "outbound_rules": []
        }
        result = self.mgmt_client.load_balancers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ],
          "backend_address_pools": [
            {
              "name": BACKEND_ADDRESS_POOL_NAME
            }
          ],
          "load_balancing_rules": [
            {
              "name": "rulelb",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "80",
              "backend_port": "80",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp",
              "load_distribution": "Default",
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "probe": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
              }
            }
          ],
          "probes": [
            {
              "name": PROBE_NAME,
              "protocol": "Http",
              "port": "80",
              "request_path": "healthcheck.aspx",
              "interval_in_seconds": "15",
              "number_of_probes": "2"
            }
          ],
          "inbound_nat_rules": [
            {
              "name": INBOUND_NAT_RULE_NAME,
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "3389",
              "backend_port": "3389",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp"
            }
          ],
          "inbound_nat_pools": [],
          "outbound_rules": []
        }
        result = self.mgmt_client.load_balancers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ],
          "backend_address_pools": [
            {
              "name": BACKEND_ADDRESS_POOL_NAME
            }
          ],
          "load_balancing_rules": [
            {
              "name": "rulelb",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "80",
              "backend_port": "80",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp",
              "enable_tcp_reset": False,
              "load_distribution": "Default",
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "probe": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/probes/" + PROBE_NAME
              }
            }
          ],
          "probes": [
            {
              "name": PROBE_NAME,
              "protocol": "Http",
              "port": "80",
              "request_path": "healthcheck.aspx",
              "interval_in_seconds": "15",
              "number_of_probes": "2"
            }
          ],
          "inbound_nat_rules": [
            {
              "name": INBOUND_NAT_RULE_NAME,
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": "3389",
              "backend_port": "3389",
              "enable_floating_ip": True,
              "idle_timeout_in_minutes": "15",
              "protocol": "Tcp",
              "enable_tcp_reset": False
            }
          ],
          "inbound_nat_pools": []
        }
        result = self.mgmt_client.load_balancers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "type": "Hypernet",
          "prefix": "3.2.5.0/24",
          "allocation_tags": {
            "vnet_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME
          }
        }
        result = self.mgmt_client.ip_allocations.begin_create_or_update(resource_group_name=RESOURCE_GROUP, ip_allocation_name=IP_ALLOCATION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Premium_MeteredData",
            "tier": "Premium",
            "family": "MeteredData"
          },
          "express_route_port": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRoutePorts/" + EXPRESS_ROUTE_PORT_NAME
          },
          "bandwidth_in_gbps": "10"
        }
        result = self.mgmt_client.express_route_circuits.begin_create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "sku": {
            "name": "Standard_MeteredData",
            "tier": "Standard",
            "family": "MeteredData"
          },
          "location": AZURE_LOCATION,
          "authorizations": [],
          "peerings": [],
          "allow_classic_operations": False,
          "service_provider_properties": {
            "service_provider_name": "Equinix",
            "peering_location": "Silicon Valley",
            "bandwidth_in_mbps": "200"
          }
        }
        result = self.mgmt_client.express_route_circuits.begin_create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "hosted_gateway": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY_NAME
          }
        }
        result = self.mgmt_client.virtual_routers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "zones": [],
          "sku": {
            "name": "AZFW_VNet",
            "tier": "Standard"
          },
          "threat_intel_mode": "Alert",
          "ip_configurations": [
            {
              "name": "azureFirewallIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "application_rule_collections": [
            {
              "name": "apprulecoll",
              "priority": "110",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "rule1",
                  "description": "Deny inbound rule",
                  "protocols": [
                    {
                      "protocol_type": "Https",
                      "port": "443"
                    }
                  ],
                  "target_fqdns": [
                    "www.test.com"
                  ],
                  "source_addresses": [
                    "216.58.216.164",
                    "10.0.0.0/24"
                  ]
                }
              ]
            }
          ],
          "nat_rule_collections": [
            {
              "name": "natrulecoll",
              "priority": "112",
              "action": {
                "type": "Dnat"
              },
              "rules": [
                {
                  "name": "DNAT-HTTPS-traffic",
                  "description": "D-NAT all outbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "443"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_address": "1.2.3.5",
                  "translated_port": "8443"
                },
                {
                  "name": "DNAT-HTTP-traffic-With-FQDN",
                  "description": "D-NAT all inbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "80"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_fqdn": "internalhttpserver",
                  "translated_port": "880"
                }
              ]
            }
          ],
          "network_rule_collections": [
            {
              "name": "netrulecoll",
              "priority": "112",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "L4-traffic",
                  "description": "Block traffic based on source IPs and ports",
                  "source_addresses": [
                    "192.168.1.1-192.168.1.12",
                    "10.1.4.12-10.1.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                },
                {
                  "name": "L4-traffic-with-FQDN",
                  "description": "Block traffic based on source IPs and ports to amazon",
                  "source_addresses": [
                    "10.2.4.12-10.2.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_fqdns": [
                    "www.amazon.com"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "zones": [],
          "sku": {
            "name": "AZFW_VNet",
            "tier": "Standard"
          },
          "threat_intel_mode": "Alert",
          "ip_configurations": [
            {
              "name": "azureFirewallIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "application_rule_collections": [
            {
              "name": "apprulecoll",
              "priority": "110",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "rule1",
                  "description": "Deny inbound rule",
                  "protocols": [
                    {
                      "protocol_type": "Https",
                      "port": "443"
                    }
                  ],
                  "target_fqdns": [
                    "www.test.com"
                  ],
                  "source_addresses": [
                    "216.58.216.164",
                    "10.0.0.0/24"
                  ]
                }
              ]
            }
          ],
          "nat_rule_collections": [
            {
              "name": "natrulecoll",
              "priority": "112",
              "action": {
                "type": "Dnat"
              },
              "rules": [
                {
                  "name": "DNAT-HTTPS-traffic",
                  "description": "D-NAT all outbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "443"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_address": "1.2.3.5",
                  "translated_port": "8443"
                },
                {
                  "name": "DNAT-HTTP-traffic-With-FQDN",
                  "description": "D-NAT all inbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "80"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_fqdn": "internalhttpserver",
                  "translated_port": "880"
                }
              ]
            }
          ],
          "network_rule_collections": [
            {
              "name": "netrulecoll",
              "priority": "112",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "L4-traffic",
                  "description": "Block traffic based on source IPs and ports",
                  "source_addresses": [
                    "192.168.1.1-192.168.1.12",
                    "10.1.4.12-10.1.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                },
                {
                  "name": "L4-traffic-with-FQDN",
                  "description": "Block traffic based on source IPs and ports to amazon",
                  "source_addresses": [
                    "10.2.4.12-10.2.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_fqdns": [
                    "www.amazon.com"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                }
              ]
            }
          ],
          "ip_groups": [],
          "additional_properties": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "zones": [],
          "sku": {
            "name": "AZFW_Hub",
            "tier": "Standard"
          },
          "threat_intel_mode": "Alert",
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          },
          "firewall_policy": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/firewallPolicies/" + FIREWALL_POLICY_NAME
          },
          "hub_ip_addresses": {
            "public_ips": {
              "addresses": [],
              "count": "1"
            }
          }
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "zones": [],
          "sku": {
            "name": "AZFW_VNet",
            "tier": "Standard"
          },
          "threat_intel_mode": "Alert",
          "ip_configurations": [
            {
              "name": "azureFirewallIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "management_ip_configuration": {
            "name": "azureFirewallMgmtIpConfiguration",
            "subnet": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
            },
            "public_ip_address": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
            }
          },
          "application_rule_collections": [
            {
              "name": "apprulecoll",
              "priority": "110",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "rule1",
                  "description": "Deny inbound rule",
                  "protocols": [
                    {
                      "protocol_type": "Https",
                      "port": "443"
                    }
                  ],
                  "target_fqdns": [
                    "www.test.com"
                  ],
                  "source_addresses": [
                    "216.58.216.164",
                    "10.0.0.0/24"
                  ]
                }
              ]
            }
          ],
          "nat_rule_collections": [
            {
              "name": "natrulecoll",
              "priority": "112",
              "action": {
                "type": "Dnat"
              },
              "rules": [
                {
                  "name": "DNAT-HTTPS-traffic",
                  "description": "D-NAT all outbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "443"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_address": "1.2.3.5",
                  "translated_port": "8443"
                },
                {
                  "name": "DNAT-HTTP-traffic-With-FQDN",
                  "description": "D-NAT all inbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "80"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_fqdn": "internalhttpserver",
                  "translated_port": "880"
                }
              ]
            }
          ],
          "network_rule_collections": [
            {
              "name": "netrulecoll",
              "priority": "112",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "L4-traffic",
                  "description": "Block traffic based on source IPs and ports",
                  "source_addresses": [
                    "192.168.1.1-192.168.1.12",
                    "10.1.4.12-10.1.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                },
                {
                  "name": "L4-traffic-with-FQDN",
                  "description": "Block traffic based on source IPs and ports to amazon",
                  "source_addresses": [
                    "10.2.4.12-10.2.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_fqdns": [
                    "www.amazon.com"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "tags": {
            "key1": "value1"
          },
          "zones": [
            "1",
            "2",
            "3"
          ],
          "threat_intel_mode": "Alert",
          "sku": {
            "name": "AZFW_VNet",
            "tier": "Standard"
          },
          "ip_configurations": [
            {
              "name": "azureFirewallIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "application_rule_collections": [
            {
              "name": "apprulecoll",
              "priority": "110",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "rule1",
                  "description": "Deny inbound rule",
                  "protocols": [
                    {
                      "protocol_type": "Https",
                      "port": "443"
                    }
                  ],
                  "target_fqdns": [
                    "www.test.com"
                  ],
                  "source_addresses": [
                    "216.58.216.164",
                    "10.0.0.0/24"
                  ]
                }
              ]
            }
          ],
          "nat_rule_collections": [
            {
              "name": "natrulecoll",
              "priority": "112",
              "action": {
                "type": "Dnat"
              },
              "rules": [
                {
                  "name": "DNAT-HTTPS-traffic",
                  "description": "D-NAT all outbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "443"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_address": "1.2.3.5",
                  "translated_port": "8443"
                },
                {
                  "name": "DNAT-HTTP-traffic-With-FQDN",
                  "description": "D-NAT all inbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "80"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_fqdn": "internalhttpserver",
                  "translated_port": "880"
                }
              ]
            }
          ],
          "network_rule_collections": [
            {
              "name": "netrulecoll",
              "priority": "112",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "L4-traffic",
                  "description": "Block traffic based on source IPs and ports",
                  "source_addresses": [
                    "192.168.1.1-192.168.1.12",
                    "10.1.4.12-10.1.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                },
                {
                  "name": "L4-traffic-with-FQDN",
                  "description": "Block traffic based on source IPs and ports to amazon",
                  "source_addresses": [
                    "10.2.4.12-10.2.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_fqdns": [
                    "www.amazon.com"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "zones": [],
          "sku": {
            "name": "AZFW_VNet",
            "tier": "Standard"
          },
          "threat_intel_mode": "Alert",
          "ip_configurations": [
            {
              "name": "azureFirewallIpConfiguration",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "application_rule_collections": [
            {
              "name": "apprulecoll",
              "priority": "110",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "rule1",
                  "description": "Deny inbound rule",
                  "protocols": [
                    {
                      "protocol_type": "Https",
                      "port": "443"
                    }
                  ],
                  "target_fqdns": [
                    "www.test.com"
                  ],
                  "source_addresses": [
                    "216.58.216.164",
                    "10.0.0.0/24"
                  ]
                }
              ]
            }
          ],
          "nat_rule_collections": [
            {
              "name": "natrulecoll",
              "priority": "112",
              "action": {
                "type": "Dnat"
              },
              "rules": [
                {
                  "name": "DNAT-HTTPS-traffic",
                  "description": "D-NAT all outbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "443"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_address": "1.2.3.5",
                  "translated_port": "8443"
                },
                {
                  "name": "DNAT-HTTP-traffic-With-FQDN",
                  "description": "D-NAT all inbound web traffic for inspection",
                  "source_addresses": [
                    "*"
                  ],
                  "destination_addresses": [
                    "1.2.3.4"
                  ],
                  "destination_ports": [
                    "80"
                  ],
                  "protocols": [
                    "TCP"
                  ],
                  "translated_fqdn": "internalhttpserver",
                  "translated_port": "880"
                }
              ]
            }
          ],
          "network_rule_collections": [
            {
              "name": "netrulecoll",
              "priority": "112",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "name": "L4-traffic",
                  "description": "Block traffic based on source IPs and ports",
                  "source_addresses": [
                    "192.168.1.1-192.168.1.12",
                    "10.1.4.12-10.1.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                },
                {
                  "name": "L4-traffic-with-FQDN",
                  "description": "Block traffic based on source IPs and ports to amazon",
                  "source_addresses": [
                    "10.2.4.12-10.2.4.255"
                  ],
                  "destination_ports": [
                    "443-444",
                    "8443"
                  ],
                  "destination_fqdns": [
                    "www.amazon.com"
                  ],
                  "protocols": [
                    "TCP"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.azure_firewalls.begin_create_or_update(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-1",
              "address_prefix": "10.0.0.0/24",
              "delegations": [
                {
                  "name": "myDelegation",
                  "service_name": "Microsoft.Sql/managedInstances"
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-1",
              "address_prefix": "10.0.0.0/16",
              "service_endpoints": [
                {
                  "service": "Microsoft.Storage"
                }
              ],
              "service_endpoint_policies": [
                {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/serviceEndpointPolicies/" + SERVICE_ENDPOINT_POLICY_NAME
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-1",
              "address_prefix": "10.0.0.0/16",
              "service_endpoints": [
                {
                  "service": "Microsoft.Storage"
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-1",
              "address_prefix": "10.0.0.0/24"
            }
          ],
          "bgp_communities": {
            "virtual_network_community": "12076:20000"
          }
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-2",
              "address_prefixes": [
                "10.0.0.0/28",
                "10.0.1.0/28"
              ]
            }
          ]
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          },
          "subnets": [
            {
              "name": "test-1",
              "address_prefix": "10.0.0.0/24"
            }
          ]
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "address_space": {
            "address_prefixes": [
              "10.0.0.0/16"
            ]
          }
        }
        result = self.mgmt_client.virtual_networks.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.network_watchers.create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


        

        BODY = {
          "location": AZURE_LOCATION,
          "container_network_interface_configurations": [
            {
              "name": "eth1",
              "ip_configurations": [
                {
                  "name": "ipconfig1",
                  "subnet": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
                  }
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.network_profiles.create_or_update(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "threat_intel_mode": "Alert",
          "threat_intel_whitelist": {
            "ip_addresses": [
              "20.3.4.5"
            ],
            "fqdns": [
              "*.microsoft.com"
            ]
          },
          "dns_settings": {
            "servers": [
              "30.3.4.5"
            ],
            "enable_proxy": True,
            "require_proxy_for_network_rules": False
          }
        }
        result = self.mgmt_client.firewall_policies.begin_create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, parameters=BODY)
        result = result.result()


        

        [
          "1"
        ]
        result = self.mgmt_client.public_ip_prefixes.begin_create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, zones=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard"
          },
          "prefix_length": "30"
        }
        result = self.mgmt_client.public_ip_prefixes.begin_create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "manual_private_link_service_connections": [
            {
              "private_link_service_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/privateLinkServices/" + PRIVATE_LINK_SERVICE_NAME,
              "group_ids": [
                "groupIdFromResource"
              ],
              "request_message": "Please manually approve my connection."
            }
          ],
          "subnet": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
          }
        }
        result = self.mgmt_client.private_endpoints.begin_create_or_update(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "private_link_service_connections": [
            {
              "private_link_service_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/privateLinkServices/" + PRIVATE_LINK_SERVICE_NAME,
              "group_ids": [
                "groupIdFromResource"
              ],
              "request_message": "Please approve my connection."
            }
          ],
          "subnet": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
          }
        }
        result = self.mgmt_client.private_endpoints.begin_create_or_update(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME, parameters=BODY)
        result = result.result()


        

        [
          "1"
        ]
        result = self.mgmt_client.custom_ip_prefixes.begin_create_or_update(resource_group_name=RESOURCE_GROUP, custom_ip_prefix_name=CUSTOM_IP_PREFIX_NAME, zones=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "dns_settings": {
            "domain_name_label": "dnslbl"
          }
        }
        result = self.mgmt_client.public_ip_addresses.begin_create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
        result = result.result()


        

        [
          "1"
        ]
        result = self.mgmt_client.public_ip_addresses.begin_create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, zones=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.public_ip_addresses.begin_create_or_update(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "enable_accelerated_networking": True,
          "ip_configurations": [
            {
              "name": "ipconfig1",
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              },
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.network_interfaces.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "peering_location": "peeringLocationName",
          "bandwidth_in_gbps": "100",
          "encapsulation": "QinQ",
          "links": [
            {
              "name": "link1",
              "admin_state": "Enabled"
            }
          ]
        }
        result = self.mgmt_client.express_route_ports.begin_create_or_update(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "peering_location": "peeringLocationName",
          "bandwidth_in_gbps": "100",
          "encapsulation": "QinQ"
        }
        result = self.mgmt_client.express_route_ports.begin_create_or_update(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "markings": [
            "46",
            "10"
          ],
          "source_ip_ranges": [
            {
              "start_ip": "127.0.0.1",
              "end_ip": "127.0.0.2"
            },
            {
              "start_ip": "127.0.1.1",
              "end_ip": "127.0.1.2"
            }
          ],
          "destination_ip_ranges": [
            {
              "start_ip": "127.0.10.1",
              "end_ip": "127.0.10.2"
            },
            {
              "start_ip": "127.0.11.1",
              "end_ip": "127.0.11.2"
            }
          ],
          "source_port_ranges": [
            {
              "start": "10",
              "end": "11"
            },
            {
              "start": "20",
              "end": "21"
            }
          ],
          "destination_port_ranges": [
            {
              "start": "15",
              "end": "15"
            },
            {
              "start": "26",
              "end": "27"
            }
          ],
          "protocol": "Tcp"
        }
        result = self.mgmt_client.dscp_configuration.begin_create_or_update(resource_group_name=RESOURCE_GROUP, dscp_configuration_name=DSCP_CONFIGURATION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "protocol_custom_settings": [
            {
              "protocol": "Tcp"
            }
          ]
        }
        result = self.mgmt_client.ddos_custom_policies.begin_create_or_update(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "identity": {
            "type": "UserAssigned",
            "user_assigned_identities": {}
          },
          "location": AZURE_LOCATION,
          "sku": {
            "name": "Standard_v2",
            "tier": "Standard_v2",
            "capacity": "3"
          },
          "gateway_ip_configurations": [
            {
              "name": "appgwipc",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              }
            }
          ],
          "ssl_certificates": [
            {
              "name": "sslcert",
              "data": "****",
              "password": "****"
            },
            {
              "name": "sslcert2",
              "key_vault_secret_id": "https://kv/secret"
            }
          ],
          "trusted_root_certificates": [
            {
              "name": "rootcert",
              "data": "****"
            },
            {
              "name": "rootcert1",
              "key_vault_secret_id": "https://kv/secret"
            }
          ],
          "trusted_client_certificates": [
            {
              "name": "clientcert",
              "data": "****"
            }
          ],
          "frontend_ip_configurations": [
            {
              "name": FRONTEND_IP_CONFIGURATION_NAME,
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "frontend_ports": [
            {
              "name": "appgwfp",
              "port": "443"
            },
            {
              "name": "appgwfp80",
              "port": "80"
            }
          ],
          "backend_address_pools": [
            {
              "name": BACKEND_ADDRESS_POOL_NAME,
              "backend_addresses": [
                {
                  "ip_address": "10.0.1.1"
                },
                {
                  "ip_address": "10.0.1.2"
                }
              ]
            }
          ],
          "backend_http_settings_collection": [
            {
              "name": "appgwbhs",
              "port": "80",
              "protocol": "Http",
              "cookie_based_affinity": "Disabled",
              "request_timeout": "30"
            }
          ],
          "ssl_profiles": [
            {
              "name": "sslProfile1",
              "ssl_policy": {
                "policy_type": "Custom",
                "min_protocol_version": "TLSv1_1",
                "cipher_suites": [
                  "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"
                ]
              },
              "client_auth_configuration": {
                "verify_client_cert_issuer_dn": True
              },
              "trusted_client_certificates": [
                {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/trustedClientCertificates/" + TRUSTED_CLIENT_CERTIFICATE_NAME
                }
              ]
            }
          ],
          "http_listeners": [
            {
              "name": "appgwhl",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/frontendPorts/" + FRONTEND_PORT_NAME
              },
              "protocol": "Https",
              "ssl_certificate": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/sslCertificates/" + SSL_CERTIFICATE_NAME
              },
              "ssl_profile": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/sslProfiles/" + SSL_PROFILE_NAME
              },
              "require_server_name_indication": False
            },
            {
              "name": "appgwhttplistener",
              "frontend_ip_configuration": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
              },
              "frontend_port": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/frontendPorts/" + FRONTEND_PORT_NAME
              },
              "protocol": "Http"
            }
          ],
          "url_path_maps": [
            {
              "name": "pathMap1",
              "default_backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "default_backend_http_settings": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendHttpSettingsCollection/" + BACKEND_HTTP_SETTINGS_COLLECTION_NAME
              },
              "default_rewrite_rule_set": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/rewriteRuleSets/" + REWRITE_RULE_SET_NAME
              },
              "path_rules": [
                {
                  "name": "apiPaths",
                  "paths": [
                    "/api",
                    "/v1/api"
                  ],
                  "backend_address_pool": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
                  },
                  "backend_http_settings": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendHttpSettingsCollection/" + BACKEND_HTTP_SETTINGS_COLLECTION_NAME
                  },
                  "rewrite_rule_set": {
                    "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/rewriteRuleSets/" + REWRITE_RULE_SET_NAME
                  }
                }
              ]
            }
          ],
          "request_routing_rules": [
            {
              "name": "appgwrule",
              "rule_type": "Basic",
              "priority": "10",
              "http_listener": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/httpListeners/" + HTTP_LISTENER_NAME
              },
              "backend_address_pool": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendAddressPools/" + BACKEND_ADDRESS_POOL_NAME
              },
              "backend_http_settings": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendHttpSettingsCollection/" + BACKEND_HTTP_SETTINGS_COLLECTION_NAME
              },
              "rewrite_rule_set": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/rewriteRuleSets/" + REWRITE_RULE_SET_NAME
              }
            },
            {
              "name": "appgwPathBasedRule",
              "rule_type": "PathBasedRouting",
              "priority": "20",
              "http_listener": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/httpListeners/" + HTTP_LISTENER_NAME
              },
              "url_path_map": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/urlPathMaps/" + URL_PATH_MAP_NAME
              }
            }
          ],
          "rewrite_rule_sets": [
            {
              "name": "rewriteRuleSet1",
              "rewrite_rules": [
                {
                  "name": "Set X-Forwarded-For",
                  "rule_sequence": "102",
                  "conditions": [
                    {
                      "variable": "http_req_Authorization",
                      "pattern": "^Bearer",
                      "ignore_case": True,
                      "negate": False
                    }
                  ],
                  "action_set": {
                    "request_header_configurations": [
                      {
                        "header_name": "X-Forwarded-For",
                        "header_value": "{var_add_x_forwarded_for_proxy}"
                      }
                    ],
                    "response_header_configurations": [
                      {
                        "header_name": "Strict-Transport-Security",
                        "header_value": "max-age=31536000"
                      }
                    ],
                    "url_configuration": {
                      "modified_path": "/abc"
                    }
                  }
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.application_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.ddos_protection_plans.begin_create_or_update(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          },
          "auto_scale_configuration": {
            "bounds": {
              "min": "3"
            }
          }
        }
        result = self.mgmt_client.express_route_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME, put_express_route_gateway_parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "local_network_address_space": {
            "address_prefixes": [
              "10.1.0.0/16"
            ]
          },
          "gateway_ip_address": "11.12.13.14",
          "fqdn": "site1.contoso.com"
        }
        result = self.mgmt_client.local_network_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "security_rules": [
            {
              "name": "rule1",
              "protocol": "*",
              "source_address_prefix": "*",
              "destination_address_prefix": "*",
              "access": "Allow",
              "destination_port_range": "80",
              "source_port_range": "*",
              "priority": "130",
              "direction": "Inbound"
            }
          ]
        }
        result = self.mgmt_client.network_security_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.network_security_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "service_provider_provisioning_state": "NotProvisioned"
        }
        result = self.mgmt_client.express_route_cross_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "virtual_network_gateway1": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY_NAME,
            "location": AZURE_LOCATION,
            "ip_configurations": [
              {
                "name": "gwipconfig1",
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworkGateways/" + VIRTUAL_NETWORK_GATEWAY_NAME + "/ipConfigurations/" + IP_CONFIGURATION_NAME,
                "private_ipallocation_method": "Dynamic",
                "subnet": {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
                },
                "public_ip_address": {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
                }
              }
            ],
            "gateway_type": "Vpn",
            "vpn_type": "RouteBased",
            "enable_bgp": False,
            "active_active": False,
            "sku": {
              "name": "VpnGw1",
              "tier": "VpnGw1"
            },
            "bgp_settings": {
              "asn": "65514",
              "bgp_peering_address": "10.0.1.30",
              "peer_weight": "0"
            }
          },
          "local_network_gateway2": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/localNetworkGateways/" + LOCAL_NETWORK_GATEWAY_NAME,
            "location": AZURE_LOCATION,
            "local_network_address_space": {
              "address_prefixes": [
                "10.1.0.0/16"
              ]
            },
            "gateway_ip_address": "x.x.x.x"
          },
          "connection_type": "IPsec",
          "connection_protocol": "IKEv2",
          "routing_weight": "0",
          "dpd_timeout_seconds": "30",
          "shared_key": "Abc123",
          "enable_bgp": False,
          "use_policy_based_traffic_selectors": False,
          "ipsec_policies": [],
          "traffic_selector_policies": []
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "ip_configurations": [
            {
              "name": "gwipconfig1",
              "private_ipallocation_method": "Dynamic",
              "subnet": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
              },
              "public_ip_address": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/publicIPAddresses/" + PUBLIC_IP_ADDRESS_NAME
              }
            }
          ],
          "gateway_type": "Vpn",
          "vpn_type": "RouteBased",
          "enable_bgp": False,
          "active_active": False,
          "enable_dns_forwarding": True,
          "sku": {
            "name": "VpnGw1",
            "tier": "VpnGw1"
          },
          "vpn_client_configuration": {
            "vpn_client_protocols": [
              "OpenVPN"
            ],
            "vpn_client_root_certificates": [],
            "vpn_client_revoked_certificates": [],
            "radius_servers": [
              {
                "radius_server_address": "10.2.0.0",
                "radius_server_score": "20",
                "radius_server_secret": "radiusServerSecret"
              }
            ]
          },
          "bgp_settings": {
            "asn": "65515",
            "bgp_peering_address": "10.0.1.30",
            "peer_weight": "0"
          },
          "custom_routes": {
            "address_prefixes": [
              "101.168.0.6/32"
            ]
          }
        }
        result = self.mgmt_client.virtual_network_gateways.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "service_endpoint_policy_definitions": [
            {
              "name": "StorageServiceEndpointPolicyDefinition",
              "description": "Storage Service EndpointPolicy Definition",
              "service": "Microsoft.Storage",
              "service_resources": [
                "/subscriptions/subid1",
                "/subscriptions/subid1/resourceGroups/storageRg",
                "/subscriptions/subid1/resourceGroups/storageRg/providers/Microsoft.Storage/storageAccounts/stAccount"
              ]
            }
          ]
        }
        result = self.mgmt_client.service_endpoint_policies.begin_create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.service_endpoint_policies.begin_create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "address_prefix": "10.0.3.0/24",
          "next_hop_type": "VirtualNetworkGateway"
        }
        result = self.mgmt_client.routes.begin_create_or_update(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME, route_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "vpn_protocols": [
            "IkeV2"
          ],
          "vpn_client_ipsec_policies": [
            {
              "sa_life_time_seconds": "86472",
              "sa_data_size_kilobytes": "429497",
              "ipsec_encryption": "AES256",
              "ipsec_integrity": "SHA256",
              "ike_encryption": "AES256",
              "ike_integrity": "SHA384",
              "dh_group": "DHGroup14",
              "pfs_group": "PFS14"
            }
          ],
          "vpn_client_root_certificates": [
            {
              "name": "vpnServerConfigVpnClientRootCert1",
              "public_cert_data": "MIIC5zCCAc+gAwIBAgIQErQ0Hk4aDJxIA+Q5RagB+jANBgkqhkiG9w0BAQsFADAWMRQwEgYDVQQDDAtQMlNSb290Q2VydDAeFw0xNzEyMTQyMTA3MzhaFw0xODEyMTQyMTI3MzhaMBYxFDASBgNVBAMMC1AyU1Jvb3RDZXJ0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArP7/NQXmW7cQ/ZR1mv3Y3I29Lt7HTOqzo/1KUOoVH3NItbQIRAQbwKy3UWrOFz4eGNX2GWtNRMdCyWsKeqy9Ltsdfcm1IbKXkl84DFeU/ZacXu4Dl3xX3gV5du4TLZjEowJELyur11Ea2YcjPRQ/FzAF9/hGuboS1HZQEPLx4FdUs9OxCYOtc0MxBCwLfVTTRqarb0Ne+arNYd4kCzIhAke1nOyKAJBda5ZL+VHy3S5S8qGlD46jm8HXugmAkUygS4oIIXOmj/1O9sNAi3LN60zufSzCmP8Rm/iUGX+DHAGGiXxwZOKQLEDaZXKqoHjMPP0XudmSWwOIbyeQVrLhkwIDAQABozEwLzAOBgNVHQ8BAf8EBAMCAgQwHQYDVR0OBBYEFEfeNU2trYxNLF9ONmuJUsT13pKDMA0GCSqGSIb3DQEBCwUAA4IBAQBmM6RJzsGGipxyMhimHKN2xlkejhVsgBoTAhOU0llW9aUSwINJ9zFUGgI8IzUFy1VG776fchHp0LMRmPSIUYk5btEPxbsrPtumPuMH8EQGrS+Rt4pD+78c8H1fEPkq5CmDl/PKu4JoFGv+aFcE+Od0hlILstIF10Qysf++QXDolKfzJa/56bgMeYKFiju73loiRM57ns8ddXpfLl792UVpRkFU62LNns6Y1LKTwapmUF4IvIuAIzd6LZNOQng64LAKXtKnViJ1JQiXwf4CEzhgvAti3/ejpb3U90hsrUcyZi6wBv9bZLcAJRWpz61JNYliM1d1grSwQDKGXNQE4xuN"
            }
          ],
          "vpn_client_revoked_certificates": [
            {
              "name": "vpnServerConfigVpnClientRevokedCert1",
              "thumbprint": "83FFBFC8848B5A5836C94D0112367E16148A286F"
            }
          ],
          "radius_servers": [
            {
              "radius_server_address": "10.0.0.0",
              "radius_server_score": "25",
              "radius_server_secret": "radiusServerSecret"
            }
          ],
          "radius_server_root_certificates": [
            {
              "name": "vpnServerConfigRadiusServerRootCer1",
              "public_cert_data": "MIIC5zCCAc+gAwIBAgIQErQ0Hk4aDJxIA+Q5RagB+jANBgkqhkiG9w0BAQsFADAWMRQwEgYDVQQDDAtQMlNSb290Q2VydDAeFw0xNzEyMTQyMTA3MzhaFw0xODEyMTQyMTI3MzhaMBYxFDASBgNVBAMMC1AyU1Jvb3RDZXJ0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArP7/NQXmW7cQ/ZR1mv3Y3I29Lt7HTOqzo/1KUOoVH3NItbQIRAQbwKy3UWrOFz4eGNX2GWtNRMdCyWsKeqy9Ltsdfcm1IbKXkl84DFeU/ZacXu4Dl3xX3gV5du4TLZjEowJELyur11Ea2YcjPRQ/FzAF9/hGuboS1HZQEPLx4FdUs9OxCYOtc0MxBCwLfVTTRqarb0Ne+arNYd4kCzIhAke1nOyKAJBda5ZL+VHy3S5S8qGlD46jm8HXugmAkUygS4oIIXOmj/1O9sNAi3LN60zufSzCmP8Rm/iUGX+DHAGGiXxwZOKQLEDaZXKqoHjMPP0XudmSWwOIbyeQVrLhkwIDAQABozEwLzAOBgNVHQ8BAf8EBAMCAgQwHQYDVR0OBBYEFEfeNU2trYxNLF9ONmuJUsT13pKDMA0GCSqGSIb3DQEBCwUAA4IBAQBmM6RJzsGGipxyMhimHKN2xlkejhVsgBoTAhOU0llW9aUSwINJ9zFUGgI8IzUFy1VG776fchHp0LMRmPSIUYk5btEPxbsrPtumPuMH8EQGrS+Rt4pD+78c8H1fEPkq5CmDl/PKu4JoFGv+aFcE+Od0hlILstIF10Qysf++QXDolKfzJa/56bgMeYKFiju73loiRM57ns8ddXpfLl792UVpRkFU62LNns6Y1LKTwapmUF4IvIuAIzd6LZNOQng64LAKXtKnViJ1JQiXwf4CEzhgvAti3/ejpb3U90hsrUcyZi6wBv9bZLcAJRWpz61JNYliM1d1grSwQDKGXNQE4xuM"
            }
          ],
          "radius_client_root_certificates": [
            {
              "name": "vpnServerConfigRadiusClientRootCert1",
              "thumbprint": "83FFBFC8848B5A5836C94D0112367E16148A286F"
            }
          ]
        }
        result = self.mgmt_client.vpn_server_configurations.begin_create_or_update(resource_group_name=RESOURCE_GROUP, vpn_server_configuration_name=VPN_SERVER_CONFIGURATION_NAME, vpn_server_configuration_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "location": AZURE_LOCATION,
          "security_provider_name": "ZScaler",
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          }
        }
        result = self.mgmt_client.security_partner_providers.begin_create_or_update(resource_group_name=RESOURCE_GROUP, security_partner_provider_name=SECURITY_PARTNER_PROVIDER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1"
          },
          "identity": {
            "type": "UserAssigned",
            "user_assigned_identities": {}
          },
          "location": AZURE_LOCATION,
          "nva_sku": {
            "vendor": "Cisco SDWAN",
            "bundled_scale_unit": "1",
            "market_place_version": "12.1"
          },
          "virtual_hub": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME
          },
          "boot_strap_configuration_blobs": [
            "https://csrncvhdstorage1.blob.core.windows.net/csrncvhdstoragecont/csrbootstrapconfig"
          ],
          "cloud_init_configuration_blobs": [
            "https://csrncvhdstorage1.blob.core.windows.net/csrncvhdstoragecont/csrcloudinitconfig"
          ],
          "virtual_appliance_asn": "10000"
        }
        result = self.mgmt_client.network_virtual_appliances.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION
        }
        result = self.mgmt_client.application_security_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "managed_rules": {
            "managed_rule_sets": [
              {
                "rule_set_type": "OWASP",
                "rule_set_version": "3.0"
              }
            ]
          },
          "custom_rules": [
            {
              "name": "Rule1",
              "priority": "1",
              "rule_type": "MatchRule",
              "action": "Block",
              "match_conditions": [
                {
                  "match_variables": [
                    {
                      "variable_name": "RemoteAddr"
                    }
                  ],
                  "operator": "IPMatch",
                  "match_values": [
                    "192.168.1.0/24",
                    "10.0.0.0/24"
                  ]
                }
              ]
            },
            {
              "name": "Rule2",
              "priority": "2",
              "rule_type": "MatchRule",
              "match_conditions": [
                {
                  "match_variables": [
                    {
                      "variable_name": "RemoteAddr"
                    }
                  ],
                  "operator": "IPMatch",
                  "match_values": [
                    "192.168.1.0/24"
                  ]
                },
                {
                  "match_variables": [
                    {
                      "variable_name": "RequestHeaders",
                      "selector": "UserAgent"
                    }
                  ],
                  "operator": "Contains",
                  "match_values": [
                    "Windows"
                  ]
                }
              ],
              "action": "Block"
            }
          ]
        }
        result = self.mgmt_client.web_application_firewall_policies.create_or_update(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME, parameters=BODY)


        

        BODY = {
          "remote_vpn_site": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE_NAME
          },
          "vpn_link_connections": [
            {
              "name": "Connection-Link1",
              "vpn_site_link": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnSites/" + VPN_SITE_NAME + "/vpnSiteLinks/" + VPN_SITE_LINK_NAME
              },
              "connection_bandwidth": "200",
              "vpn_connection_protocol_type": "IKEv2",
              "shared_key": "key"
            }
          ]
        }
        result = self.mgmt_client.vpn_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, connection_name=CONNECTION_NAME, vpn_connection_parameters=BODY)
        result = result.result()


        

        BODY = {
          "value": "AzureAbc123"
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_set_shared_key(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "peer_asn": "200",
          "primary_peer_address_prefix": "192.168.16.252/30",
          "secondary_peer_address_prefix": "192.168.18.252/30",
          "vlan_id": "200"
        }
        result = self.mgmt_client.express_route_circuit_peerings.begin_create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, peering_parameters=BODY)
        result = result.result()


        

        BODY = {
          "peer_ip": "192.168.1.5",
          "peer_asn": "20000"
        }
        result = self.mgmt_client.virtual_router_peerings.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "address_prefix": "10.0.0.0/16"
        }
        result = self.mgmt_client.subnets.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
        result = result.result()


        

        BODY = {
          "address_prefix": "10.0.0.0/16",
          "service_endpoints": [
            {
              "service": "Microsoft.Storage"
            }
          ]
        }
        result = self.mgmt_client.subnets.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
        result = result.result()


        

        BODY = {
          "address_prefix": "10.0.0.0/16"
        }
        result = self.mgmt_client.subnets.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, subnet_parameters=BODY)
        result = result.result()


        

        BODY = {
          "routes": [
            {
              "destination_type": "CIDR",
              "destinations": [
                "20.10.0.0/16",
                "20.20.0.0/16"
              ],
              "next_hop_type": "IPAddress",
              "next_hops": [
                "10.0.0.68"
              ]
            },
            {
              "destination_type": "CIDR",
              "destinations": [
                "0.0.0.0/0"
              ],
              "next_hop_type": "IPAddress",
              "next_hops": [
                "10.0.0.68"
              ]
            }
          ],
          "attached_connections": [
            "All_Vnets"
          ]
        }
        result = self.mgmt_client.virtual_hub_route_table_v2s.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME, virtual_hub_route_table_v2_parameters=BODY)
        result = result.result()


        

        BODY = {
          "access": "Allow",
          "route_filter_rule_type": "Community",
          "communities": [
            "12076:5030",
            "12076:5040"
          ]
        }
        result = self.mgmt_client.route_filter_rules.begin_create_or_update(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, rule_name=RULE_NAME, route_filter_rule_parameters=BODY)
        result = result.result()


        

        BODY = {
          "peer_ip": "192.168.1.5",
          "peer_asn": "20000"
        }
        result = self.mgmt_client.virtual_hub_bgp_connection.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "location": AZURE_LOCATION,
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME,
          "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
          "enabled": True,
          "format": {
            "type": "JSON",
            "version": "1"
          }
        }
        result = self.mgmt_client.flow_logs.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "routes": [
            {
              "name": "route1",
              "destination_type": "CIDR",
              "destinations": [
                "10.0.0.0/8",
                "20.0.0.0/8",
                "30.0.0.0/8"
              ],
              "next_hop_type": "ResourceId",
              "next_hop": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/azureFirewalls/" + AZURE_FIREWALL_NAME
            }
          ],
          "labels": [
            "label1",
            "label2"
          ]
        }
        result = self.mgmt_client.hub_route_tables.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME, route_table_parameters=BODY)
        result = result.result()


        

        BODY = {
          "subnet": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME + "/subnets/" + SUBNET_NAME
          }
        }
        result = self.mgmt_client.virtual_hub_ip_configuration.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, ip_config_name=IP_CONFIG_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {}
        result = self.mgmt_client.express_route_circuit_authorizations.begin_create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME, authorization_parameters=BODY)
        result = result.result()


        

        BODY = {
          "protocol": "Tcp",
          "frontend_ip_configuration": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/loadBalancers/" + LOAD_BALANCER_NAME + "/frontendIPConfigurations/" + FRONTEND_IP_CONFIGURATION_NAME
          },
          "frontend_port": "3390",
          "backend_port": "3389",
          "idle_timeout_in_minutes": "4",
          "enable_tcp_reset": False,
          "enable_floating_ip": False
        }
        result = self.mgmt_client.inbound_nat_rules.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME, inbound_nat_rule_parameters=BODY)
        result = result.result()


        

        BODY = {
          "target": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
          "bytes_to_capture_per_packet": "10000",
          "total_bytes_per_session": "100000",
          "time_limit_in_seconds": "100",
          "storage_location": {
            "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
            "storage_path": "https://mytestaccountname.blob.core.windows.net/capture/pc1.cap",
            "file_path": "D:\\capture\\pc1.cap"
          },
          "filters": [
            {
              "protocol": "TCP",
              "local_ip_address": "10.0.0.4",
              "local_port": "80"
            }
          ]
        }
        result = self.mgmt_client.packet_captures.begin_create(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, packet_capture_name=PACKET_CAPTURE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "peer_asn": "200",
          "primary_peer_address_prefix": "192.168.16.252/30",
          "secondary_peer_address_prefix": "192.168.18.252/30",
          "vlan_id": "200",
          "ipv6peering_config": {
            "primary_peer_address_prefix": "3FFE:FFFF:0:CD30::/126",
            "secondary_peer_address_prefix": "3FFE:FFFF:0:CD30::4/126"
          }
        }
        result = self.mgmt_client.express_route_cross_connection_peerings.begin_create_or_update(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME, peering_parameters=BODY)
        result = result.result()


        

        BODY = {
          "remote_virtual_network": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME
          },
          "enable_internet_security": False,
          "routing_configuration": {
            "associated_route_table": {
              "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME + "/hubRouteTables/" + HUB_ROUTE_TABLE_NAME
            },
            "propagated_route_tables": {
              "labels": [
                "label1",
                "label2"
              ],
              "ids": [
                {
                  "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME + "/hubRouteTables/" + HUB_ROUTE_TABLE_NAME
                }
              ]
            },
            "vnet_routes": {
              "static_routes": [
                {
                  "name": "route1",
                  "address_prefixes": [
                    "10.1.0.0/16",
                    "10.2.0.0/16"
                  ],
                  "next_hop_ip_address": "10.0.0.68"
                },
                {
                  "name": "route2",
                  "address_prefixes": [
                    "10.3.0.0/16",
                    "10.4.0.0/16"
                  ],
                  "next_hop_ip_address": "10.0.0.65"
                }
              ]
            }
          }
        }
        result = self.mgmt_client.hub_virtual_network_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME, hub_virtual_network_connection_parameters=BODY)
        result = result.result()


        

        BODY = {
          "name": "testPlePeConnection",
          "private_endpoint": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/privateEndpoints/" + PRIVATE_ENDPOINT_NAME
          },
          "private_link_service_connection_state": {
            "status": "Approved",
            "description": "approved it for some reason."
          }
        }
        result = self.mgmt_client.private_link_services.update_private_endpoint_connection(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME, pe_connection_name=PE_CONNECTION_NAME, parameters=BODY)


        

        BODY = {
          "load_balancer_backend_addresses": [
            {
              "name": "address1",
              "virtual_network": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME
              },
              "ip_address": "10.0.0.4"
            },
            {
              "name": "address2",
              "virtual_network": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME
              },
              "ip_address": "10.0.0.5"
            }
          ]
        }
        result = self.mgmt_client.load_balancer_backend_address_pools.begin_create_or_update(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, backend_address_pool_name=BACKEND_ADDRESS_POOL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "endpoints": [
            {
              "name": "vm1",
              "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
            },
            {
              "name": "CanaryWorkspaceVamshi",
              "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.OperationalInsights/workspaces/" + WORKSPACE_NAME,
              "filter": {
                "type": "Include",
                "items": [
                  {
                    "type": "AgentAddress",
                    "address": "npmuser"
                  }
                ]
              }
            },
            {
              "name": "bing",
              "address": "bing.com"
            },
            {
              "name": "google",
              "address": "google.com"
            }
          ],
          "test_configurations": [
            {
              "name": "testConfig1",
              "test_frequency_sec": "60",
              "protocol": "Tcp",
              "tcp_configuration": {
                "port": "80",
                "disable_trace_route": False
              }
            }
          ],
          "test_groups": [
            {
              "name": "test1",
              "disable": False,
              "test_configurations": [
                "testConfig1"
              ],
              "sources": [
                "vm1",
                "CanaryWorkspaceVamshi"
              ],
              "destinations": [
                "bing",
                "google"
              ]
            }
          ],
          "outputs": []
        }
        result = self.mgmt_client.connection_monitors.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "source": {
            "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
          },
          "destination": {
            "address": "bing.com",
            "port": "80"
          },
          "monitoring_interval_in_seconds": "60"
        }
        result = self.mgmt_client.connection_monitors.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "virtual_network_tap": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworkTaps/" + VIRTUAL_NETWORK_TAP_NAME
          }
        }
        result = self.mgmt_client.network_interface_tap_configurations.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, tap_configuration_name=TAP_CONFIGURATION_NAME, tap_configuration_parameters=BODY)
        result = result.result()


        

        BODY = {
          "protocol": "*",
          "source_address_prefix": "10.0.0.0/8",
          "destination_address_prefix": "11.0.0.0/8",
          "access": "Deny",
          "destination_port_range": "8080",
          "source_port_range": "*",
          "priority": "100",
          "direction": "Outbound"
        }
        result = self.mgmt_client.security_rules.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME, security_rule_parameters=BODY)
        result = result.result()


        

        BODY = {
          "priority": "110",
          "rule_collections": [
            {
              "rule_collection_type": "FirewallPolicyFilterRuleCollection",
              "name": "Example-Filter-Rule-Collection",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "rule_type": "NetworkRule",
                  "name": "network-1",
                  "ip_protocols": [
                    "TCP"
                  ],
                  "destination_ports": [
                    "*"
                  ],
                  "source_ip_groups": [
                    "/subscriptions/subid/providers/Microsoft.Network/resourceGroup/rg1/ipGroups/ipGroups1"
                  ],
                  "destination_ip_groups": [
                    "/subscriptions/subid/providers/Microsoft.Network/resourceGroup/rg1/ipGroups/ipGroups2"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.firewall_policy_rule_collection_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_collection_group_name=RULE_COLLECTION_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "priority": "110",
          "rule_collections": [
            {
              "rule_collection_type": "FirewallPolicyFilterRuleCollection",
              "name": "Example-Filter-Rule-Collection",
              "action": {
                "type": "Deny"
              },
              "rules": [
                {
                  "rule_type": "NetworkRule",
                  "name": "network-rule1",
                  "source_addresses": [
                    "10.1.25.0/24"
                  ],
                  "destination_addresses": [
                    "*"
                  ],
                  "ip_protocols": [
                    "TCP"
                  ],
                  "destination_ports": [
                    "*"
                  ]
                }
              ]
            }
          ]
        }
        result = self.mgmt_client.firewall_policy_rule_collection_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_collection_group_name=RULE_COLLECTION_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRouteGateways/" + EXPRESS_ROUTE_GATEWAY_NAME + "/expressRouteConnections/" + EXPRESS_ROUTE_CONNECTION_NAME,
          "name": "connectionName",
          "routing_weight": "2",
          "authorization_key": "authorizationKey",
          "express_route_circuit_peering": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRouteCircuits/" + EXPRESS_ROUTE_CIRCUIT_NAME + "/peerings/" + PEERING_NAME
          }
        }
        result = self.mgmt_client.express_route_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME, connection_name=CONNECTION_NAME, put_express_route_connection_parameters=BODY)
        result = result.result()


        

        BODY = {
          "private_dns_zone_configs": [
            {
              "private_dns_zone_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/privateDnsZones/" + PRIVATE_DNS_ZONE_NAME
            }
          ]
        }
        result = self.mgmt_client.private_dns_zone_groups.begin_create_or_update(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME, private_dns_zone_group_name=PRIVATE_DNS_ZONE_GROUP_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "address_prefix": "192.168.1.0/24",
          "o365policy": {
            "break_out_categories": {
              "allow": True,
              "optimize": True,
              "default": True
            }
          }
        }
        result = self.mgmt_client.virtual_appliance_sites.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, site_name=SITE_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "name": "connection1",
          "private_endpoint": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/privateEndpoints/" + PRIVATE_ENDPOINT_NAME
          },
          "private_link_service_connection_state": {
            "status": "Approved",
            "description": "approved it for some reason."
          }
        }
        result = self.mgmt_client.application_gateway_private_endpoint_connections.begin_update(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, connection_name=CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "allow_virtual_network_access": True,
          "allow_forwarded_traffic": True,
          "allow_gateway_transit": False,
          "use_remote_gateways": False,
          "remote_virtual_network": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualNetworks/" + VIRTUAL_NETWORK_NAME
          }
        }
        result = self.mgmt_client.virtual_network_peerings.begin_create_or_update(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME, virtual_network_peering_parameters=BODY)
        result = result.result()


        

        BODY = {
          "express_route_circuit_peering": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRouteCircuits/" + EXPRESS_ROUTE_CIRCUIT_NAME + "/peerings/" + PEERING_NAME
          },
          "peer_express_route_circuit_peering": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRouteCircuits/" + EXPRESS_ROUTE_CIRCUIT_NAME + "/peerings/" + PEERING_NAME
          },
          "authorization_key": "946a1918-b7a2-4917-b43c-8c4cdaee006a",
          "address_prefix": "10.0.0.0/29",
          "ipv6circuit_connection_config": {
            "address_prefix": "aa:bb::/125"
          }
        }
        result = self.mgmt_client.express_route_circuit_connections.begin_create_or_update(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, connection_name=CONNECTION_NAME, express_route_circuit_connection_parameters=BODY)
        result = result.result()


        

        BODY = {
          "rules": [
            {
              "protocol": "TCP",
              "source_address_prefix": "50.20.121.5/32",
              "destination_port_range": "22"
            }
          ]
        }
        result = self.mgmt_client.inbound_security_rule.begin_create_or_update(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, rule_collection_name=RULE_COLLECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "description": "Storage Service EndpointPolicy Definition",
          "service": "Microsoft.Storage",
          "service_resources": [
            "/subscriptions/subid1",
            "/subscriptions/subid1/resourceGroups/storageRg",
            "/subscriptions/subid1/resourceGroups/storageRg/providers/Microsoft.Storage/storageAccounts/stAccount"
          ]
        }
        result = self.mgmt_client.service_endpoint_policy_definitions.begin_create_or_update(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME, service_endpoint_policy_definitions=BODY)
        result = result.result()


        

        result = self.mgmt_client.public_ip_addresses.get_virtual_machine_scale_set_public_ip_address(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME, ip_configuration_name=IP_CONFIGURATION_NAME, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)


        

        result = self.mgmt_client.public_ip_addresses.list_virtual_machine_scale_set_vmpublic_ip_addresses(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME, ip_configuration_name=IP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.network_interfaces.get_virtual_machine_scale_set_network_interface(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.network_interfaces.list_virtual_machine_scale_set_ip_configurations(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.network_interfaces.get_virtual_machine_scale_set_network_interface(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.service_endpoint_policy_definitions.get(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME)


        

        result = self.mgmt_client.network_interfaces.list_virtual_machine_scale_set_vmnetwork_interfaces(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME, virtualmachine_index=VIRTUALMACHINE_INDEX)


        

        result = self.mgmt_client.vpn_site_link_connections.get(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, connection_name=CONNECTION_NAME, link_connection_name=LINK_CONNECTION_NAME)


        

        result = self.mgmt_client.default_security_rules.get(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, default_security_rule_name=DEFAULT_SECURITY_RULE_NAME)


        

        result = self.mgmt_client.peer_express_route_circuit_connections.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.application_gateways.get_ssl_predefined_policy(application_gateway_available_ssl_option_name=APPLICATION_GATEWAY_AVAILABLE_SSL_OPTION_NAME, predefined_policy_name=PREDEFINED_POLICY_NAME)


        

        result = self.mgmt_client.express_route_circuit_connections.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.load_balancer_frontend_ip_configurations.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, frontend_ip_configuration_name=FRONTEND_IP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.virtual_network_peerings.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME)


        

        result = self.mgmt_client.application_gateway_private_endpoint_connections.get(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.virtual_appliance_sites.get(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, site_name=SITE_NAME)


        

        result = self.mgmt_client.private_dns_zone_groups.get(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME, private_dns_zone_group_name=PRIVATE_DNS_ZONE_GROUP_NAME)


        

        result = self.mgmt_client.express_route_connections.get(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.firewall_policy_rule_collection_groups.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_collection_group_name=RULE_COLLECTION_GROUP_NAME)


        

        result = self.mgmt_client.firewall_policy_rule_collection_groups.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_collection_group_name=RULE_COLLECTION_GROUP_NAME)


        

        result = self.mgmt_client.security_rules.get(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME)


        

        result = self.mgmt_client.network_interface_tap_configurations.get(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, tap_configuration_name=TAP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.resource_navigation_links.list(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME)


        

        result = self.mgmt_client.service_association_links.list(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME)


        

        result = self.mgmt_client.network_interface_ip_configurations.get(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, ip_configuration_name=IP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.connection_monitors.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME)


        

        result = self.mgmt_client.service_endpoint_policy_definitions.list_by_resource_group(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)


        

        result = self.mgmt_client.load_balancer_backend_address_pools.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, backend_address_pool_name=BACKEND_ADDRESS_POOL_NAME)


        

        result = self.mgmt_client.load_balancer_backend_address_pools.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, backend_address_pool_name=BACKEND_ADDRESS_POOL_NAME)


        

        result = self.mgmt_client.private_link_services.get_private_endpoint_connection(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME, pe_connection_name=PE_CONNECTION_NAME)


        

        result = self.mgmt_client.load_balancer_load_balancing_rules.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, load_balancing_rule_name=LOAD_BALANCING_RULE_NAME)


        

        result = self.mgmt_client.vpn_link_connections.list_by_vpn_connection(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.hub_virtual_network_connections.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.express_route_cross_connection_peerings.get(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.peer_express_route_circuit_connections.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.virtual_appliance_sites.list(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME)


        

        result = self.mgmt_client.packet_captures.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, packet_capture_name=PACKET_CAPTURE_NAME)


        

        result = self.mgmt_client.inbound_nat_rules.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME)


        

        result = self.mgmt_client.express_route_circuit_authorizations.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME)


        

        result = self.mgmt_client.express_route_circuit_connections.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.network_interfaces.list_virtual_machine_scale_set_network_interfaces(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME)


        

        result = self.mgmt_client.public_ip_addresses.list_virtual_machine_scale_set_public_ip_addresses(resource_group_name=RESOURCE_GROUP, virtual_machine_scale_set_name=VIRTUAL_MACHINE_SCALE_SET_NAME)


        

        result = self.mgmt_client.application_gateway_private_endpoint_connections.list(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)


        

        result = self.mgmt_client.load_balancer_outbound_rules.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, outbound_rule_name=OUTBOUND_RULE_NAME)


        

        result = self.mgmt_client.express_route_connections.list(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME)


        

        result = self.mgmt_client.default_security_rules.list(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)


        

        result = self.mgmt_client.express_route_circuits.get_peering_stats(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.application_gateways.list_available_ssl_predefined_policies(application_gateway_available_ssl_option_name=APPLICATION_GATEWAY_AVAILABLE_SSL_OPTION_NAME)


        

        result = self.mgmt_client.virtual_hub_ip_configuration.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, ip_config_name=IP_CONFIG_NAME)


        

        result = self.mgmt_client.hub_route_tables.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME)


        

        result = self.mgmt_client.application_gateway_private_link_resources.list(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)


        

        result = self.mgmt_client.flow_logs.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME)


        

        result = self.mgmt_client.virtual_hub_bgp_connection.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.express_route_links.get(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, link_name=LINK_NAME)


        

        result = self.mgmt_client.security_rules.list(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)


        

        result = self.mgmt_client.route_filter_rules.get(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, rule_name=RULE_NAME)


        

        result = self.mgmt_client.virtual_networks.check_ip_address_availability(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, ip_address="10.0.1.4")


        

        result = self.mgmt_client.virtual_network_gateways.list_connections(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


        

        result = self.mgmt_client.virtual_hub_route_table_v2s.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME)


        

        result = self.mgmt_client.subnets.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME)


        

        result = self.mgmt_client.subnets.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME)


        

        result = self.mgmt_client.virtual_router_peerings.get(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.express_route_circuit_peerings.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)


        

        result = self.mgmt_client.virtual_network_gateway_connections.get_shared_key(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME)


        

        result = self.mgmt_client.vpn_connections.get(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, connection_name=CONNECTION_NAME)


        

        result = self.mgmt_client.vpn_site_links.get(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME, vpn_site_link_name=VPN_SITE_LINK_NAME)


        

        result = self.mgmt_client.web_application_firewall_policies.get(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME)


        

        result = self.mgmt_client.express_route_cross_connection_peerings.list(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME)


        

        result = self.mgmt_client.private_dns_zone_groups.list(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME)


        

        result = self.mgmt_client.private_link_services.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_network_peerings.list(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.firewall_policy_rule_collection_groups.list(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


        

        result = self.mgmt_client.firewall_policy_rule_collection_groups.list(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


        

        result = self.mgmt_client.network_interface_tap_configurations.list(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.application_security_groups.get(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME)


        

        result = self.mgmt_client.load_balancer_frontend_ip_configurations.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.network_interface_ip_configurations.list(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.hub_virtual_network_connections.list(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.load_balancer_probes.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, probe_name=PROBE_NAME)


        

        result = self.mgmt_client.private_link_services.list_auto_approved_private_link_services(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.supported_security_providers(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME)


        

        result = self.mgmt_client.network_virtual_appliances.get(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME)


        

        result = self.mgmt_client.connection_monitors.list(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


        

        result = self.mgmt_client.security_partner_providers.get(resource_group_name=RESOURCE_GROUP, security_partner_provider_name=SECURITY_PARTNER_PROVIDER_NAME)


        

        result = self.mgmt_client.network_interface_load_balancers.list(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.available_private_endpoint_types.list_by_resource_group(resource_group_name=RESOURCE_GROUP, azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.vpn_server_configurations.get(resource_group_name=RESOURCE_GROUP, vpn_server_configuration_name=VPN_SERVER_CONFIGURATION_NAME)


        

        result = self.mgmt_client.load_balancer_backend_address_pools.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.load_balancer_backend_address_pools.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.routes.get(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME)


        

        result = self.mgmt_client.service_endpoint_policies.get(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)


        

        result = self.mgmt_client.load_balancer_load_balancing_rules.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.packet_captures.list(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


        

        result = self.mgmt_client.virtual_network_gateways.get(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


        

        result = self.mgmt_client.virtual_network_gateway_connections.get(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME)


        

        result = self.mgmt_client.express_route_cross_connections.get(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME)


        

        result = self.mgmt_client.load_balancer_network_interfaces.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.load_balancer_network_interfaces.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.network_security_groups.get(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)


        

        result = self.mgmt_client.available_service_aliases.list_by_resource_group(resource_group_name=RESOURCE_GROUP, azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.express_route_circuit_authorizations.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


        

        result = self.mgmt_client.inbound_nat_rules.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.application_gateways.list_available_ssl_options(application_gateway_available_ssl_option_name=APPLICATION_GATEWAY_AVAILABLE_SSL_OPTION_NAME)


        

        result = self.mgmt_client.express_route_links.get(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, link_name=LINK_NAME)


        

        result = self.mgmt_client.route_filter_rules.list_by_route_filter(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME)


        

        result = self.mgmt_client.local_network_gateways.get(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME)


        

        result = self.mgmt_client.express_route_gateways.get(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME)


        

        result = self.mgmt_client.load_balancer_outbound_rules.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.available_resource_group_delegations.list(resource_group_name=RESOURCE_GROUP, azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.ddos_protection_plans.get(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME)


        

        result = self.mgmt_client.flow_logs.list(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


        

        result = self.mgmt_client.virtual_hub_ip_configuration.list(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.application_gateways.get(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)


        

        result = self.mgmt_client.subnets.list(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.virtual_networks.list_usage(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.virtual_router_peerings.list(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME)


        

        result = self.mgmt_client.virtual_hub_bgp_connections.list(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.hub_route_tables.list(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.ddos_custom_policies.get(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME)


        

        result = self.mgmt_client.dscp_configuration.get(resource_group_name=RESOURCE_GROUP, dscp_configuration_name=DSCP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.express_route_circuit_peerings.list(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


        

        result = self.mgmt_client.web_application_firewall_policies.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.express_route_ports.get(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME)


        

        result = self.mgmt_client.network_interfaces.get(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)


        

        result = self.mgmt_client.public_ip_addresses.get(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)


        

        result = self.mgmt_client.virtual_hub_route_table_v2s.list(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.express_route_circuits.get_stats(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


        

        result = self.mgmt_client.load_balancer_probes.list(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.vpn_connections.list_by_vpn_gateway(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)


        

        result = self.mgmt_client.custom_ip_prefixes.get(resource_group_name=RESOURCE_GROUP, custom_ip_prefix_name=CUSTOM_IP_PREFIX_NAME)


        

        result = self.mgmt_client.private_endpoints.get(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME)


        

        result = self.mgmt_client.private_endpoints.get(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME)


        

        result = self.mgmt_client.public_ip_prefixes.get(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME)


        

        result = self.mgmt_client.firewall_policies.get(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)


        

        result = self.mgmt_client.network_profiles.get(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)


        

        result = self.mgmt_client.network_profiles.get(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)


        

        result = self.mgmt_client.network_watchers.get(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)


        

        result = self.mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.virtual_networks.get(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)


        

        result = self.mgmt_client.routes.list(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)


        

        result = self.mgmt_client.vpn_site_links.list_by_vpn_site(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME)


        

        result = self.mgmt_client.azure_firewalls.get(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)


        

        result = self.mgmt_client.azure_firewalls.get(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)


        

        result = self.mgmt_client.azure_firewalls.get(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)


        

        result = self.mgmt_client.azure_firewalls.get(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)


        

        result = self.mgmt_client.azure_firewalls.get(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)


        

        result = self.mgmt_client.virtual_routers.get(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME)


        

        result = self.mgmt_client.express_route_circuits.get(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)


        

        result = self.mgmt_client.ip_allocations.get(resource_group_name=RESOURCE_GROUP, ip_allocation_name=IP_ALLOCATION_NAME)


        

        result = self.mgmt_client.load_balancers.get(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)


        

        result = self.mgmt_client.private_link_services.get(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME)


        

        result = self.mgmt_client.bastion_hosts.get(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME)


        

        result = self.mgmt_client.route_filters.get(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME)


        

        result = self.mgmt_client.available_endpoint_services.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.nat_gateways.get(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME)


        

        result = self.mgmt_client.route_tables.get(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)


        

        result = self.mgmt_client.virtual_wans.get(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME)


        

        result = self.mgmt_client.virtual_hubs.get(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)


        

        result = self.mgmt_client.virtual_network_taps.get(resource_group_name=RESOURCE_GROUP, tap_name=TAP_NAME)


        

        result = self.mgmt_client.p2s_vpn_gateways.get(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)


        

        result = self.mgmt_client.vpn_gateways.get(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)


        

        result = self.mgmt_client.ip_groups.get(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME)


        

        result = self.mgmt_client.express_route_cross_connections.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.vpn_sites.get(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME)


        

        result = self.mgmt_client.private_link_services.list_auto_approved_private_link_services(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.application_security_groups.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.network_virtual_appliances.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.available_private_endpoint_types.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.security_partner_providers.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.service_endpoint_policies.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.vpn_server_configurations.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_network_gateways.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.network_security_groups.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.express_route_circuits.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.local_network_gateways.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.express_route_gateways.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.application_gateways.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.check_dns_name_availability(azure_location=AZURE_LOCATION, domain_name_label="testdns")


        

        result = self.mgmt_client.ddos_protection_plans.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.private_link_services.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.available_service_aliases.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.dscp_configuration.get(resource_group_name=RESOURCE_GROUP, dscp_configuration_name=DSCP_CONFIGURATION_NAME)


        

        result = self.mgmt_client.virtual_network_taps.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.express_route_ports.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.network_interfaces.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.public_ip_addresses.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.custom_ip_prefixes.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.firewall_policies.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.private_endpoints.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.public_ip_prefixes.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.available_delegations.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.network_profiles.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.network_watchers.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_networks.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.azure_firewalls.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_routers.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.p2s_vpn_gateways.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.ip_allocations.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.load_balancers.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.bastion_hosts.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.route_filters.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.web_application_firewall_policies.list_all()


        

        result = self.mgmt_client.nat_gateways.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.route_tables.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_network_gateway_connections.list(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_wans.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.virtual_hubs.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.vpn_gateways.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.express_route_ports_locations.get(location_name=LOCATION_NAME)


        

        result = self.mgmt_client.ip_groups.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.vpn_sites.list_by_resource_group(resource_group_name=RESOURCE_GROUP)


        

        result = self.mgmt_client.application_gateways.list_available_server_variables()


        

        result = self.mgmt_client.application_gateways.list_available_response_headers()


        

        result = self.mgmt_client.virtual_appliance_skus.get(sku_name=SKU_NAME)


        

        result = self.mgmt_client.service_tags.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.application_gateways.list_available_request_headers()


        

        result = self.mgmt_client.application_gateways.list_available_waf_rule_sets()


        

        result = self.mgmt_client.usages.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.usages.list(azure_location=AZURE_LOCATION)


        

        result = self.mgmt_client.express_route_service_providers.list()


        

        result = self.mgmt_client.express_route_cross_connections.list()


        

        result = self.mgmt_client.virtual_appliance_skus.list()


        

        result = self.mgmt_client.express_route_ports_locations.list()


        

        result = self.mgmt_client.application_security_groups.list_all()


        

        result = self.mgmt_client.network_virtual_appliances.list()


        

        result = self.mgmt_client.security_partner_providers.list()


        

        result = self.mgmt_client.service_endpoint_policies.list()


        

        result = self.mgmt_client.vpn_server_configurations.list()


        

        result = self.mgmt_client.azure_firewall_fqdn_tags.list_all()


        

        result = self.mgmt_client.network_security_groups.list_all()


        

        result = self.mgmt_client.bgp_service_communities.list()


        

        result = self.mgmt_client.express_route_circuits.list_all()


        

        result = self.mgmt_client.express_route_gateways.list_by_subscription()


        

        result = self.mgmt_client.application_gateways.list_all()


        

        result = self.mgmt_client.ddos_protection_plans.list()


        

        result = self.mgmt_client.private_link_services.list_by_subscription()


        

        result = self.mgmt_client.dscp_configuration.list_all()


        

        result = self.mgmt_client.virtual_network_taps.list_all()


        

        result = self.mgmt_client.express_route_ports.list()


        

        result = self.mgmt_client.network_interfaces.list_all()


        

        result = self.mgmt_client.public_ip_addresses.list_all()


        

        result = self.mgmt_client.custom_ip_prefixes.list_all()


        

        result = self.mgmt_client.firewall_policies.list_all()


        

        result = self.mgmt_client.private_endpoints.list_by_subscription()


        

        result = self.mgmt_client.public_ip_prefixes.list_all()


        

        result = self.mgmt_client.network_profiles.list_all()


        

        result = self.mgmt_client.network_watchers.list_all()


        

        result = self.mgmt_client.virtual_networks.list_all()


        

        result = self.mgmt_client.azure_firewalls.list_all()


        

        result = self.mgmt_client.virtual_routers.list()


        

        result = self.mgmt_client.p2s_vpn_gateways.list()


        

        result = self.mgmt_client.ip_allocations.list()


        

        result = self.mgmt_client.load_balancers.list_all()


        

        result = self.mgmt_client.bastion_hosts.list()


        

        result = self.mgmt_client.route_filters.list()


        

        result = self.mgmt_client.nat_gateways.list_all()


        

        result = self.mgmt_client.route_tables.list_all()


        

        result = self.mgmt_client.virtual_wans.list()


        

        result = self.mgmt_client.virtual_hubs.list()


        

        result = self.mgmt_client.vpn_gateways.list()


        

        result = self.mgmt_client.ip_groups.list()


        

        result = self.mgmt_client.vpn_sites.list()


        

        result = self.mgmt_client.operations.list()


        

        result = self.mgmt_client.express_route_cross_connections.begin_list_routes_table_summary(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        result = self.mgmt_client.express_route_cross_connections.begin_list_routes_table(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        result = self.mgmt_client.express_route_cross_connections.begin_list_arp_table(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuits.begin_list_routes_table_summary(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        BODY = {
          "vpn_connection_ids": [
            "vpnconnId1",
            "vpnconnId2"
          ]
        }
        result = self.mgmt_client.virtual_network_gateways.begin_disconnect_virtual_network_gateway_vpn_connections(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, request=BODY)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuits.begin_list_routes_table(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        result = self.mgmt_client.connection_monitors.begin_start(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME)
        result = result.result()


        

        result = self.mgmt_client.connection_monitors.begin_query(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME)
        result = result.result()


        

        result = self.mgmt_client.connection_monitors.begin_stop(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuits.begin_list_arp_table(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, device_path=DEVICE_PATH)
        result = result.result()


        

        result = self.mgmt_client.packet_captures.begin_get_status(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, packet_capture_name=PACKET_CAPTURE_NAME)
        result = result.result()


        

        BODY = {
          "service_name": "Microsoft.Sql/managedInstances"
        }
        result = self.mgmt_client.subnets.begin_unprepare_network_policies(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, unprepare_network_policies_request_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.connection_monitors.update_tags(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME, parameters=BODY)


        

        BODY = {
          "service_name": "Microsoft.Sql/managedInstances"
        }
        result = self.mgmt_client.subnets.begin_prepare_network_policies(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME, prepare_network_policies_request_parameters=BODY)
        result = result.result()


        

        BODY = {
          "link_connection_names": [
            "siteLink1",
            "siteLink2"
          ]
        }
        result = self.mgmt_client.vpn_connections.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, vpn_connection_name=VPN_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "filter_data": "{'TracingFlags': 11,'MaxPacketBufferSize': 120,'MaxFileSize': 200,'Filters': [{'SourceSubnets': ['20.1.1.0/24'],'DestinationSubnets': ['10.1.1.0/24'],'SourcePort': [500],'DestinationPort': [4500],'Protocol': 6,'TcpFlags': 16,'CaptureSingleDirectionTrafficOnly': true}]}",
          "link_connection_names": [
            "siteLink1",
            "siteLink2"
          ]
        }
        result = self.mgmt_client.vpn_connections.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, vpn_connection_name=VPN_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "link_connection_names": [
            "siteLink1",
            "siteLink2"
          ]
        }
        result = self.mgmt_client.vpn_connections.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, vpn_connection_name=VPN_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.packet_captures.begin_stop(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, packet_capture_name=PACKET_CAPTURE_NAME)
        result = result.result()


        

        BODY = {
          "key_length": "128"
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_reset_shared_key(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, sharedkey_name=SHAREDKEY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "vendor": "Cisco",
          "device_family": "ISR",
          "firmware_version": "IOS 15.1 (Preview)"
        }
        result = self.mgmt_client.virtual_network_gateways.vpn_device_configuration_script(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_vpnclient_connection_health(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "sa_life_time_seconds": "86473",
          "sa_data_size_kilobytes": "429497",
          "ipsec_encryption": "AES256",
          "ipsec_integrity": "SHA256",
          "ike_encryption": "AES256",
          "ike_integrity": "SHA384",
          "dh_group": "DHGroup2",
          "pfs_group": "PFS2"
        }
        result = self.mgmt_client.virtual_network_gateways.begin_set_vpnclient_ipsec_parameters(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, vpnclient_ipsec_params=BODY)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_vpnclient_ipsec_parameters(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        BODY = {}
        result = self.mgmt_client.virtual_network_gateways.begin_generatevpnclientpackage(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_reset_vpn_client_shared_key(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_vpn_profile_package_url(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_hub_bgp_connections.begin_list_advertised_routes(resource_group_name=RESOURCE_GROUP, hub_name=HUB_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_interfaces.begin_list_effective_network_security_groups(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.supported_vpn_devices(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_advertised_routes(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, peer="test")
        result = result.result()


        

        result = self.mgmt_client.virtual_hub_bgp_connections.begin_list_learned_routes(resource_group_name=RESOURCE_GROUP, hub_name=HUB_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        BODY = {}
        result = self.mgmt_client.virtual_network_gateways.begin_generate_vpn_profile(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "filter_data": "{'TracingFlags': 11,'MaxPacketBufferSize': 120,'MaxFileSize': 200,'Filters': [{'SourceSubnets': ['20.1.1.0/24'],'DestinationSubnets': ['10.1.1.0/24'],'SourcePort': [500],'DestinationPort': [4500],'Protocol': 6,'TcpFlags': 16,'CaptureSingleDirectionTrafficOnly': true}]}"
        }
        result = self.mgmt_client.virtual_network_gateways.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateway_connections.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME)
        result = result.result()


        

        BODY = {
          "filter_data": "{'TracingFlags': 11,'MaxPacketBufferSize': 120,'MaxFileSize': 200,'Filters': [{'SourceSubnets': ['20.1.1.0/24'],'DestinationSubnets': ['10.1.1.0/24'],'SourcePort': [500],'DestinationPort': [4500],'Protocol': 6,'TcpFlags': 16,'CaptureSingleDirectionTrafficOnly': true}]}"
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "protocol": "Http",
          "pick_host_name_from_backend_http_settings": True,
          "path": "/",
          "timeout": "30",
          "backend_address_pool": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendaddressPools/" + BACKENDADDRESS_POOL_NAME
          },
          "backend_http_settings": {
            "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/applicationGateways/" + APPLICATION_GATEWAY_NAME + "/backendHttpSettingsCollection/" + BACKEND_HTTP_SETTINGS_COLLECTION_NAME
          }
        }
        result = self.mgmt_client.application_gateways.begin_backend_health_on_demand(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, probe_request=BODY)
        result = result.result()


        

        BODY = {
          "sas_url": "https://teststorage.blob.core.windows.net/?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-09-13T07:44:05Z&st=2019-09-06T23:44:05Z&spr=https&sig=V1h9D1riltvZMI69d6ihENnFo%2FrCvTqGgjO2lf%2FVBhE%3D"
        }
        result = self.mgmt_client.virtual_network_gateways.begin_stop_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "sas_url": "https://teststorage.blob.core.windows.net/?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-09-13T07:44:05Z&st=2019-09-06T23:44:05Z&spr=https&sig=V1h9D1riltvZMI69d6ihENnFo%2FrCvTqGgjO2lf%2FVBhE%3D"
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_stop_packet_capture(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_bgp_peer_status(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_get_learned_routes(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
          "profiles": [
            {
              "direction": "Inbound",
              "protocol": "TCP",
              "source": "10.1.0.4",
              "destination": "12.11.12.14",
              "destination_port": "12100"
            }
          ]
        }
        result = self.mgmt_client.network_watchers.begin_get_network_configuration_diagnostic(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.flow_logs.update_tags(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME, parameters=BODY)


        

        BODY = {
          "vpn_connection_ids": [
            "vpnconnId1",
            "vpnconnId2"
          ]
        }
        result = self.mgmt_client.p2s_vpn_gateways.begin_disconnect_p2s_vpn_connections(resource_group_name=RESOURCE_GROUP, p2s_vpn_gateway_name=P2S_VPN_GATEWAY_NAME, request=BODY)
        result = result.result()


        

        BODY = {
          "vpn_user_names_filter": [
            "vpnUser1",
            "vpnUser2"
          ],
          "output_blob_sas_url": "https://blobcortextesturl.blob.core.windows.net/folderforconfig/p2sconnectionhealths?sp=rw&se=2018-01-10T03%3A42%3A04Z&sv=2017-04-17&sig=WvXrT5bDmDFfgHs%2Brz%2BjAu123eRCNE9BO0eQYcPDT7pY%3D&sr=b"
        }
        result = self.mgmt_client.p2s_vpn_gateways.begin_get_p2s_vpn_connection_health_detailed(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, request=BODY)
        result = result.result()


        

        result = self.mgmt_client.network_interfaces.begin_get_effective_route_table(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
        result = result.result()


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
        }
        result = self.mgmt_client.network_watchers.begin_get_troubleshooting_result(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "provider_location": {
            "country": "United States",
            "state": "washington"
          },
          "providers": [
            "Frontier Communications of America, Inc. - ASN 5650"
          ],
          "azure_locations": [
            "West US"
          ],
          "start_time": "2017-09-07T00:00:00Z",
          "end_time": "2017-09-10T00:00:00Z"
        }
        result = self.mgmt_client.network_watchers.begin_get_azure_reachability_report(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "azure_locations": [
            "West US"
          ],
          "country": "United States",
          "state": "washington",
          "city": "seattle"
        }
        result = self.mgmt_client.network_watchers.begin_list_available_providers(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.application_gateways.begin_backend_health(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "private_link_service_alias": "mypls.00000000-0000-0000-0000-000000000000.azure.privatelinkservice"
        }
        result = self.mgmt_client.private_link_services.begin_check_private_link_service_visibility(azure_location=AZURE_LOCATION, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.application_security_groups.update_tags(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME, parameters=BODY)


        

        result = self.mgmt_client.virtual_network_gateways.begin_reset(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        [
          "session1",
          "session2",
          "session3"
        ]
        result = self.mgmt_client.disconnect_active_sessions(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME, session_ids=BODY)


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.network_virtual_appliances.update_tags(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, parameters=BODY)


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME
        }
        result = self.mgmt_client.network_watchers.begin_get_flow_log_status(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.security_partner_providers.update_tags(resource_group_name=RESOURCE_GROUP, security_partner_provider_name=SECURITY_PARTNER_PROVIDER_NAME, parameters=BODY)


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
        }
        result = self.mgmt_client.network_watchers.begin_get_vmsecurity_rules(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "source": {
            "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
          },
          "destination": {
            "address": "192.168.100.4",
            "port": "3389"
          },
          "preferred_ipversion": "IPv4"
        }
        result = self.mgmt_client.network_watchers.begin_check_connectivity(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "customer_name": "customerName"
        }
        result = self.mgmt_client.express_route_ports.generate_loa(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, request=BODY)


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkSecurityGroups/" + NETWORK_SECURITY_GROUP_NAME,
          "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
          "enabled": True
        }
        result = self.mgmt_client.network_watchers.begin_set_flow_log_configuration(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.vpn_server_configurations.update_tags(resource_group_name=RESOURCE_GROUP, vpn_server_configuration_name=VPN_SERVER_CONFIGURATION_NAME, vpn_server_configuration_parameters=BODY)


        

        result = self.mgmt_client.p2s_vpn_gateways.begin_get_p2s_vpn_connection_health(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.service_endpoint_policies.update_tags(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, parameters=BODY)


        

        result = self.mgmt_client.vpn_server_configurations_associated_with_virtual_wan.begin_list(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME)
        result = result.result()


        

        BODY = {
          "vms": [
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            },
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.begin_put_bastion_shareable_link(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME, bsl_request=BODY)
        result = result.result()


        

        BODY = {
          "vms": [
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            },
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.begin_delete_bastion_shareable_link(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME, bsl_request=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.virtual_network_gateways.begin_update_tags(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.virtual_network_gateway_connections.begin_update_tags(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME, parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.application_gateways.begin_start(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.express_route_cross_connections.update_tags(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, cross_connection_parameters=BODY)


        

        result = self.mgmt_client.application_gateways.begin_stop(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.network_security_groups.update_tags(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, parameters=BODY)


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
          "direction": "Outbound",
          "protocol": "TCP",
          "local_port": "80",
          "remote_port": "80",
          "local_ip_address": "10.2.0.4",
          "remote_ip_address": "121.10.1.1"
        }
        result = self.mgmt_client.network_watchers.begin_verify_ipflow(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
          "storage_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT_NAME,
          "storage_path": "https://st1.blob.core.windows.net/cn1"
        }
        result = self.mgmt_client.network_watchers.begin_get_troubleshooting(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "vms": [
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            },
            {
              "vm": {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME
              }
            }
          ]
        }
        result = self.mgmt_client.get_bastion_shareable_link(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME, bsl_request=BODY)


        

        result = self.mgmt_client.begin_get_active_sessions(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME)
        result = result.result()


        

        BODY = {
          "vpn_server_configuration_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/vpnServerConfigurations/" + VPN_SERVER_CONFIGURATION_NAME,
          "authentication_method": "EAPTLS"
        }
        result = self.mgmt_client.begin_generatevirtualwanvpnserverconfigurationvpnprofile(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, vpn_client_params=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.local_network_gateways.update_tags(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME, parameters=BODY)


        

        BODY = {
          "authentication_method": "EAPTLS"
        }
        result = self.mgmt_client.p2s_vpn_gateways.begin_generate_vpn_profile(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.ddos_protection_plans.update_tags(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME, parameters=BODY)


        

        BODY = {
          "target_resource_group_name": "rg2"
        }
        result = self.mgmt_client.network_watchers.get_topology(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


        

        BODY = {
          "vpn_sites": [
            "/subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/vpnSites/abc"
          ],
          "output_blob_sas_url": "https://blobcortextesturl.blob.core.windows.net/folderforconfig/vpnFile?sp=rw&se=2018-01-10T03%3A42%3A04Z&sv=2017-04-17&sig=WvXrT5bDmDFfgHs%2Brz%2BjAu123eRCNE9BO0eQYcPDT7pY%3D&sr=b"
        }
        result = self.mgmt_client.vpn_sites_configuration.begin_download(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, request=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.application_gateways.update_tags(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, parameters=BODY)


        

        BODY = {
          "target_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Compute/virtualMachines/" + VIRTUAL_MACHINE_NAME,
          "source_ip_address": "10.0.0.5",
          "destination_ip_address": "10.0.0.10",
          "target_nic_resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/networkInterfaces/" + NETWORK_INTERFACE_NAME
        }
        result = self.mgmt_client.network_watchers.begin_get_next_hop(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {}
        result = self.mgmt_client.virtual_hubs.begin_get_effective_virtual_hub_routes(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, effective_routes_parameters=BODY)
        result = result.result()


        

        BODY = {
          "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME + "/hubRouteTables/" + HUB_ROUTE_TABLE_NAME,
          "virtual_wan_resource_type": "RouteTable"
        }
        result = self.mgmt_client.virtual_hubs.begin_get_effective_virtual_hub_routes(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, effective_routes_parameters=BODY)
        result = result.result()


        

        BODY = {
          "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/expressRouteGateways/" + EXPRESS_ROUTE_GATEWAY_NAME + "/expressRouteConnections/" + EXPRESS_ROUTE_CONNECTION_NAME,
          "virtual_wan_resource_type": "ExpressRouteConnection"
        }
        result = self.mgmt_client.virtual_hubs.begin_get_effective_virtual_hub_routes(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, effective_routes_parameters=BODY)
        result = result.result()


        

        result = self.mgmt_client.vpn_gateways.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "filter_data": "{'TracingFlags': 11,'MaxPacketBufferSize': 120,'MaxFileSize': 200,'Filters': [{'SourceSubnets': ['20.1.1.0/24'],'DestinationSubnets': ['10.1.1.0/24'],'SourcePort': [500],'DestinationPort': [4500],'Protocol': 6,'TcpFlags': 16,'CaptureSingleDirectionTrafficOnly': true}]}"
        }
        result = self.mgmt_client.vpn_gateways.begin_start_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.ddos_custom_policies.update_tags(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME, parameters=BODY)


        

        BODY = {
          "sas_url": "https://teststorage.blob.core.windows.net/?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-09-13T07:44:05Z&st=2019-09-06T23:44:05Z&spr=https&sig=V1h9D1riltvZMI69d6ihENnFo%2FrCvTqGgjO2lf%2FVBhE%3D"
        }
        result = self.mgmt_client.vpn_gateways.begin_stop_packet_capture(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.express_route_ports.update_tags(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.network_interfaces.update_tags(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.public_ip_addresses.update_tags(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME, parameters=BODY)


        

        [
          "1"
        ]
        result = self.mgmt_client.custom_ip_prefixes.update_tags(resource_group_name=RESOURCE_GROUP, custom_ip_prefix_name=CUSTOM_IP_PREFIX_NAME, zones=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.public_ip_prefixes.update_tags(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.network_profiles.update_tags(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.network_watchers.update_tags(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.virtual_networks.update_tags(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.azure_firewalls.begin_update_tags(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.express_route_circuits.update_tags(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, parameters=BODY)


        

        result = self.mgmt_client.p2s_vpn_gateways.begin_reset(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.ip_allocations.update_tags(resource_group_name=RESOURCE_GROUP, ip_allocation_name=IP_ALLOCATION_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.load_balancers.update_tags(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "key1": "value1"
          }
        }
        result = self.mgmt_client.route_filters.update_tags(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, parameters=BODY)


        

        result = self.mgmt_client.vpn_gateways.begin_reset(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.nat_gateways.update_tags(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.route_tables.update_tags(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, parameters=BODY)


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.virtual_wans.update_tags(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME, wan_parameters=BODY)


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.virtual_hubs.update_tags(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, virtual_hub_parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.virtual_network_taps.update_tags(resource_group_name=RESOURCE_GROUP, tap_name=TAP_NAME, tap_parameters=BODY)


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.p2s_vpn_gateways.begin_update_tags(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, p2svpn_gateway_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
        result = self.mgmt_client.vpn_gateways.begin_update_tags(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, vpn_gateway_parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.ip_groups.update_groups(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME, parameters=BODY)


        

        BODY = {
          "private_link_service_alias": "mypls.00000000-0000-0000-0000-000000000000.azure.privatelinkservice"
        }
        result = self.mgmt_client.private_link_services.begin_check_private_link_service_visibility(azure_location=AZURE_LOCATION, parameters=BODY)
        result = result.result()


        

        BODY = {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
        result = self.mgmt_client.vpn_sites.update_tags(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME, vpn_site_parameters=BODY)


        

        result = self.mgmt_client.service_endpoint_policy_definitions.begin_delete(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME, service_endpoint_policy_definition_name=SERVICE_ENDPOINT_POLICY_DEFINITION_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuit_connections.begin_delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_peerings.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, virtual_network_peering_name=VIRTUAL_NETWORK_PEERING_NAME)
        result = result.result()


        

        result = self.mgmt_client.application_gateway_private_endpoint_connections.begin_delete(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_appliance_sites.begin_delete(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME, site_name=SITE_NAME)
        result = result.result()


        

        result = self.mgmt_client.private_dns_zone_groups.begin_delete(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME, private_dns_zone_group_name=PRIVATE_DNS_ZONE_GROUP_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_connections.begin_delete(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.firewall_policy_rule_collection_groups.begin_delete(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME, rule_collection_group_name=RULE_COLLECTION_GROUP_NAME)
        result = result.result()


        

        result = self.mgmt_client.security_rules.begin_delete(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME, security_rule_name=SECURITY_RULE_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_interface_tap_configurations.begin_delete(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME, tap_configuration_name=TAP_CONFIGURATION_NAME)
        result = result.result()


        

        result = self.mgmt_client.connection_monitors.begin_delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, connection_monitor_name=CONNECTION_MONITOR_NAME)
        result = result.result()


        

        result = self.mgmt_client.load_balancer_backend_address_pools.begin_delete(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, backend_address_pool_name=BACKEND_ADDRESS_POOL_NAME)
        result = result.result()


        

        result = self.mgmt_client.private_link_services.begin_delete_private_endpoint_connection(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME, pe_connection_name=PE_CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.hub_virtual_network_connections.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_cross_connection_peerings.begin_delete(resource_group_name=RESOURCE_GROUP, cross_connection_name=CROSS_CONNECTION_NAME, peering_name=PEERING_NAME)
        result = result.result()


        

        result = self.mgmt_client.packet_captures.begin_delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, packet_capture_name=PACKET_CAPTURE_NAME)
        result = result.result()


        

        result = self.mgmt_client.inbound_nat_rules.begin_delete(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME, inbound_nat_rule_name=INBOUND_NAT_RULE_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuit_authorizations.begin_delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, authorization_name=AUTHORIZATION_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_hub_ip_configuration.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, ip_config_name=IP_CONFIG_NAME)
        result = result.result()


        

        result = self.mgmt_client.hub_route_tables.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME)
        result = result.result()


        

        result = self.mgmt_client.flow_logs.begin_delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME, flow_log_name=FLOW_LOG_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_hub_bgp_connection.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.route_filter_rules.begin_delete(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME, rule_name=RULE_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_hub_route_table_v2s.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME, route_table_name=ROUTE_TABLE_NAME)
        result = result.result()


        

        result = self.mgmt_client.subnets.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME, subnet_name=SUBNET_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_router_peerings.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME, peering_name=PEERING_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuit_peerings.begin_delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME, peering_name=PEERING_NAME)
        result = result.result()


        

        result = self.mgmt_client.vpn_connections.begin_delete(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME, connection_name=CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.web_application_firewall_policies.begin_delete(resource_group_name=RESOURCE_GROUP, policy_name=POLICY_NAME)
        result = result.result()


        

        result = self.mgmt_client.application_security_groups.begin_delete(resource_group_name=RESOURCE_GROUP, application_security_group_name=APPLICATION_SECURITY_GROUP_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_virtual_appliances.begin_delete(resource_group_name=RESOURCE_GROUP, network_virtual_appliance_name=NETWORK_VIRTUAL_APPLIANCE_NAME)
        result = result.result()


        

        result = self.mgmt_client.security_partner_providers.begin_delete(resource_group_name=RESOURCE_GROUP, security_partner_provider_name=SECURITY_PARTNER_PROVIDER_NAME)
        result = result.result()


        

        result = self.mgmt_client.vpn_server_configurations.begin_delete(resource_group_name=RESOURCE_GROUP, vpn_server_configuration_name=VPN_SERVER_CONFIGURATION_NAME)
        result = result.result()


        

        result = self.mgmt_client.routes.begin_delete(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME, route_name=ROUTE_NAME)
        result = result.result()


        

        result = self.mgmt_client.service_endpoint_policies.begin_delete(resource_group_name=RESOURCE_GROUP, service_endpoint_policy_name=SERVICE_ENDPOINT_POLICY_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_name=VIRTUAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_gateway_connections.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_network_gateway_connection_name=VIRTUAL_NETWORK_GATEWAY_CONNECTION_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_security_groups.begin_delete(resource_group_name=RESOURCE_GROUP, network_security_group_name=NETWORK_SECURITY_GROUP_NAME)
        result = result.result()


        

        result = self.mgmt_client.local_network_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, local_network_gateway_name=LOCAL_NETWORK_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, express_route_gateway_name=EXPRESS_ROUTE_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.ddos_protection_plans.begin_delete(resource_group_name=RESOURCE_GROUP, ddos_protection_plan_name=DDOS_PROTECTION_PLAN_NAME)
        result = result.result()


        

        result = self.mgmt_client.application_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, application_gateway_name=APPLICATION_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.ddos_custom_policies.begin_delete(resource_group_name=RESOURCE_GROUP, ddos_custom_policy_name=DDOS_CUSTOM_POLICY_NAME)
        result = result.result()


        

        result = self.mgmt_client.dscp_configuration.begin_delete(resource_group_name=RESOURCE_GROUP, dscp_configuration_name=DSCP_CONFIGURATION_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_ports.begin_delete(resource_group_name=RESOURCE_GROUP, express_route_port_name=EXPRESS_ROUTE_PORT_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_interfaces.begin_delete(resource_group_name=RESOURCE_GROUP, network_interface_name=NETWORK_INTERFACE_NAME)
        result = result.result()


        

        result = self.mgmt_client.public_ip_addresses.begin_delete(resource_group_name=RESOURCE_GROUP, public_ip_address_name=PUBLIC_IP_ADDRESS_NAME)
        result = result.result()


        

        result = self.mgmt_client.custom_ip_prefixes.begin_delete(resource_group_name=RESOURCE_GROUP, custom_ip_prefix_name=CUSTOM_IP_PREFIX_NAME)
        result = result.result()


        

        result = self.mgmt_client.private_endpoints.begin_delete(resource_group_name=RESOURCE_GROUP, private_endpoint_name=PRIVATE_ENDPOINT_NAME)
        result = result.result()


        

        result = self.mgmt_client.public_ip_prefixes.begin_delete(resource_group_name=RESOURCE_GROUP, public_ip_prefix_name=PUBLIC_IP_PREFIX_NAME)
        result = result.result()


        

        result = self.mgmt_client.firewall_policies.begin_delete(resource_group_name=RESOURCE_GROUP, firewall_policy_name=FIREWALL_POLICY_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_profiles.begin_delete(resource_group_name=RESOURCE_GROUP, network_profile_name=NETWORK_PROFILE_NAME)
        result = result.result()


        

        result = self.mgmt_client.network_watchers.begin_delete(resource_group_name=RESOURCE_GROUP, network_watcher_name=NETWORK_WATCHER_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_networks.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_network_name=VIRTUAL_NETWORK_NAME)
        result = result.result()


        

        result = self.mgmt_client.azure_firewalls.begin_delete(resource_group_name=RESOURCE_GROUP, azure_firewall_name=AZURE_FIREWALL_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_routers.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_router_name=VIRTUAL_ROUTER_NAME)
        result = result.result()


        

        result = self.mgmt_client.express_route_circuits.begin_delete(resource_group_name=RESOURCE_GROUP, circuit_name=CIRCUIT_NAME)
        result = result.result()


        

        result = self.mgmt_client.ip_allocations.begin_delete(resource_group_name=RESOURCE_GROUP, ip_allocation_name=IP_ALLOCATION_NAME)
        result = result.result()


        

        result = self.mgmt_client.load_balancers.begin_delete(resource_group_name=RESOURCE_GROUP, load_balancer_name=LOAD_BALANCER_NAME)
        result = result.result()


        

        result = self.mgmt_client.private_link_services.begin_delete(resource_group_name=RESOURCE_GROUP, service_name=SERVICE_NAME)
        result = result.result()


        

        result = self.mgmt_client.bastion_hosts.begin_delete(resource_group_name=RESOURCE_GROUP, bastion_host_name=BASTION_HOST_NAME)
        result = result.result()


        

        result = self.mgmt_client.route_filters.begin_delete(resource_group_name=RESOURCE_GROUP, route_filter_name=ROUTE_FILTER_NAME)
        result = result.result()


        

        result = self.mgmt_client.nat_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, nat_gateway_name=NAT_GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.route_tables.begin_delete(resource_group_name=RESOURCE_GROUP, route_table_name=ROUTE_TABLE_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_wans.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_wan_name=VIRTUAL_WAN_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_hubs.begin_delete(resource_group_name=RESOURCE_GROUP, virtual_hub_name=VIRTUAL_HUB_NAME)
        result = result.result()


        

        result = self.mgmt_client.virtual_network_taps.begin_delete(resource_group_name=RESOURCE_GROUP, tap_name=TAP_NAME)
        result = result.result()


        

        result = self.mgmt_client.p2s_vpn_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.vpn_gateways.begin_delete(resource_group_name=RESOURCE_GROUP, gateway_name=GATEWAY_NAME)
        result = result.result()


        

        result = self.mgmt_client.ip_groups.begin_delete(resource_group_name=RESOURCE_GROUP, ip_groups_name=IP_GROUPS_NAME)
        result = result.result()


        

        result = self.mgmt_client.vpn_sites.begin_delete(resource_group_name=RESOURCE_GROUP, vpn_site_name=VPN_SITE_NAME)
        result = result.result()



if __name__ == '__main__':
    unittest.main()
