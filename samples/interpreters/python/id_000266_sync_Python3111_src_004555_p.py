



















"deanx" Dean for creating the original 'polenum'



"Wh1t3Fox" West for his fork of 'polenum'













""










































from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime
import json
import os
import random
import re
import shutil
import shlex
import socket
from subprocess import check_output, STDOUT, TimeoutExpired
import sys
import tempfile
from impacket import nmb, smb, smbconnection, smb3
from impacket.smbconnection import SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21, SMB2_DIALECT_30, SMB2_DIALECT_311
from impacket.dcerpc.v5.rpcrt import DCERPC_v5
from impacket.dcerpc.v5 import transport, samr
from ldap3 import Server, Connection, DSA
import yaml
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper



"statusq.c".  This file in turn




















NBT_INFO = [
    ["__MSBROWSE__", "01", False, "Master Browser"],
    ["INet~Services", "1C", False, "IIS"],
    ["IS~", "00", True, "IIS"],
    ["", "00", True, "Workstation Service"],
    ["", "01", True, "Messenger Service"],
    ["", "03", True, "Messenger Service"],
    ["", "06", True, "RAS Server Service"],
    ["", "1F", True, "NetDDE Service"],
    ["", "20", True, "File Server Service"],
    ["", "21", True, "RAS Client Service"],
    ["", "22", True, "Microsoft Exchange Interchange(MSMail Connector)"],
    ["", "23", True, "Microsoft Exchange Store"],
    ["", "24", True, "Microsoft Exchange Directory"],
    ["", "30", True, "Modem Sharing Server Service"],
    ["", "31", True, "Modem Sharing Client Service"],
    ["", "43", True, "SMS Clients Remote Control"],
    ["", "44", True, "SMS Administrators Remote Control Tool"],
    ["", "45", True, "SMS Clients Remote Chat"],
    ["", "46", True, "SMS Clients Remote Transfer"],
    ["", "4C", True, "DEC Pathworks TCPIP service on Windows NT"],
    ["", "52", True, "DEC Pathworks TCPIP service on Windows NT"],
    ["", "87", True, "Microsoft Exchange MTA"],
    ["", "6A", True, "Microsoft Exchange IMC"],
    ["", "BE", True, "Network Monitor Agent"],
    ["", "BF", True, "Network Monitor Application"],
    ["", "03", True, "Messenger Service"],
    ["", "00", False, "Domain/Workgroup Name"],
    ["", "1B", True, "Domain Master Browser"],
    ["", "1C", False, "Domain Controllers"],
    ["", "1D", True, "Master Browser"],
    ["", "1E", False, "Browser Service Elections"],
    ["", "2B", True, "Lotus Notes Server Service"],
    ["IRISMULTICAST", "2F", False, "Lotus Notes"],
    ["IRISNAMESERVER", "33", False, "Lotus Notes"],
    ['Forte_$ND800ZA', "20", True, "DCA IrmaLan Gateway Server Service"]
]


ACB_DICT = {
        0x00000001: "Account Disabled",
        0x00000200: "Password not expired",
        0x00000400: "Account locked out",
        0x00020000: "Password expired",
        0x00000040: "Interdomain trust account",
        0x00000080: "Workstation trust account",
        0x00000100: "Server trust account",
        0x00002000: "Trusted for delegation"
        }


DOMAIN_FIELDS = {
        0x00000001: "DOMAIN_PASSWORD_COMPLEX",
        0x00000002: "DOMAIN_PASSWORD_NO_ANON_CHANGE",
        0x00000004: "DOMAIN_PASSWORD_NO_CLEAR_CHANGE",
        0x00000008: "DOMAIN_PASSWORD_LOCKOUT_ADMINS",
        0x00000010: "DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT",
        0x00000020: "DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE"
        }


OS_VERSIONS = {
        "10.0": "Windows 10, Windows Server 2019, Windows Server 2016",
        "6.3": "Windows 8.1, Windows Server 2012 R2",
        "6.2": "Windows 8, Windows Server 2012",
        "6.1": "Windows 7, Windows Server 2008 R2",
        "6.0": "Windows Vista, Windows Server 2008",
        "5.2": "Windows XP 64-Bit Edition, Windows Server 2003, Windows Server 2003 R2",
        "5.1": "Windows XP",
        "5.0": "Windows 2000",
        }


OS_RELEASE = {
        "19045": "22H2",
        "19044": "21H2",
        "19043": "21H1",
        "19042": "20H2",
        "19041": "2004",
        "18363": "1909",
        "18362": "1903",
        "17763": "1809",
        "17134": "1803",
        "16299": "1709",
        "15063": "1703",
        "14393": "1607",
        "10586": "1511",
        "10240": "1507"
        }



SAMBA_CLIENT_ERRORS = [
        "Unable to initialize messaging context",
        "WARNING: no network interfaces found",
        "Can't load /etc/samba/smb.conf - run testparm to debug it"
    ]


SMB_DIALECTS = {
        SMB_DIALECT: "SMB 1.0",
        SMB2_DIALECT_002: "SMB 2.02",
        SMB2_DIALECT_21: "SMB 2.1",
        SMB2_DIALECT_30: "SMB 3.0",
        SMB2_DIALECT_311: "SMB 3.1.1"
    }









NT_STATUS_COMMON_ERRORS = [
        "RPC_S_ACCESS_DENIED",
        "DCERPC_FAULT_ACCESS_DENIED",
        "WERR_ACCESS_DENIED",
        "STATUS_ACCESS_DENIED",
        "STATUS_ACCOUNT_LOCKED_OUT",
        "STATUS_NO_LOGON_SERVERS",
        "STATUS_LOGON_FAILURE",
        "STATUS_IO_TIMEOUT",
        "STATUS_NETWORK_UNREACHABLE",
        "STATUS_INVALID_PARAMETER",
        "STATUS_NOT_SUPPORTED",
        "STATUS_NO_SUCH_FILE",
        "STATUS_PASSWORD_EXPIRED",
        
        
        "ERRSRV:ERRaccess",
        
        
        
        
        
        "STATUS_CONNECTION_DISCONNECTED"
    ]


AUTH_PASSWORD = "password"
AUTH_NTHASH = "nthash"
AUTH_KERBEROS = "kerberos"
AUTH_NULL = "null"


SOCKET_ERRORS = {
        11: "timed out",
        110: "timed out",
        111: "connection refused",
        113: "no route to host"
        }


SERVICE_LDAP = "LDAP"
SERVICE_LDAPS = "LDAPS"
SERVICE_SMB = "SMB"
SERVICE_SMB_NETBIOS = "SMB over NetBIOS"
SERVICES = {
        SERVICE_LDAP: 389,
        SERVICE_LDAPS: 636,
        SERVICE_SMB: 445,
        SERVICE_SMB_NETBIOS: 139
        }


ENUM_LDAP_DOMAIN_INFO = "enum_ldap_domain_info"
ENUM_NETBIOS = "enum_netbios"
ENUM_SMB = "enum_smb"
ENUM_SESSIONS = "enum_sessions"
ENUM_SMB_DOMAIN_INFO = "enum_smb_domain_info"
ENUM_LSAQUERY_DOMAIN_INFO = "enum_lsaquery_domain_info"
ENUM_USERS_RPC = "enum_users_rpc"
ENUM_GROUPS_RPC = "enum_groups_rpc"
ENUM_SHARES = "enum_shares"
ENUM_SERVICES = "enum_services"
ENUM_LISTENERS = "enum_listeners"
ENUM_POLICY = "enum_policy"
ENUM_PRINTERS = "enum_printers"
ENUM_OS_INFO = "enum_os_info"
RID_CYCLING = "rid_cycling"
BRUTE_FORCE_SHARES = "brute_force_shares"

DEPS = ["nmblookup", "net", "rpcclient", "smbclient"]
RID_RANGES = "500-550,1000-1050"
KNOWN_USERNAMES = "administrator,guest,krbtgt,domain admins,root,bin,none"
TIMEOUT = 5

GLOBAL_VERSION = '1.3.0'
GLOBAL_VERBOSE = False
GLOBAL_COLORS = True
GLOBAL_SAMBA_LEGACY = False

class Colors:
    ansi_reset = '\033[0m'
    ansi_red = '\033[91m'
    ansi_green = '\033[92m'
    ansi_yellow = '\033[93m'
    ansi_blue = '\033[94m'

    @classmethod
    def red(cls, msg):
        if GLOBAL_COLORS:
            return f"{cls.ansi_red}{msg}{cls.ansi_reset}"
        return msg

    @classmethod
    def green(cls, msg):
        if GLOBAL_COLORS:
            return f"{cls.ansi_green}{msg}{cls.ansi_reset}"
        return msg

    @classmethod
    def yellow(cls, msg):
        if GLOBAL_COLORS:
            return f"{cls.ansi_yellow}{msg}{cls.ansi_reset}"
        return msg

    @classmethod
    def blue(cls, msg):
        if GLOBAL_COLORS:
            return f"{cls.ansi_blue}{msg}{cls.ansi_reset}"
        return msg

class Result:
    '''
    The idea of the Result class is, that functions can easily return a return value
    as well as a return message. The return message can be further processed or printed
    out by the calling function, while the return value is supposed to be added to the
    output dictionary (contained in class Output), which will be later converted to JSON/YAML.
    '''
    def __init__(self, retval, retmsg):
        self.retval = retval
        self.retmsg = retmsg

class Target:
    '''
    Target encapsulates various target information. The class should only be instantiated once and
    passed during the enumeration to the various modules. This allows to modify/update target information
    during enumeration.
    '''
    def __init__(self, host, credentials, port=None, tls=None, timeout=None, samba_config=None, sessions={}):
        self.host = host
        self.creds = credentials
        self.port = port
        self.timeout = timeout
        self.tls = tls
        self.samba_config = samba_config
        self.sessions = sessions

        self.ip_version = None
        self.smb_ports = []
        self.ldap_ports = []
        self.listeners = []
        self.smb_preferred_dialect = None
        self.smb1_supported = False
        self.smb1_only = False

        result = self.valid_host(host)
        if not result.retval:
            raise Exception(result.retmsg)

    def valid_host(self, host):
        try:
            result = socket.getaddrinfo(host, None)

            
            ip_version = result[0][0]
            if ip_version == socket.AF_INET6:
                self.ip_version = 6
            elif ip_version == socket.AF_INET:
                self.ip_version = 4

            
            ip = result[0][4][0]
            if ip == host and self.creds.auth_method == AUTH_KERBEROS:
                return Result(False, f'Kerberos authentication requires a hostname, but an IPv{self.ip_version} address was given')

            return Result(True,'')
        except Exception as e:
            if isinstance(e, OSError) and e.errno == -2:
                return Result(False, f'Could not resolve host {host}')
        return Result(False, 'No valid host given')

    def as_dict(self):
        return {'target':{'host':self.host}}

class Credentials:
    '''
    Stores usernames and password.
    '''
    def __init__(self, user='', pw='', domain='', ticket_file='', nthash='', local_auth=False):
        
        self.random_user = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(8))
        self.user = user
        self.pw = pw
        self.ticket_file = ticket_file
        self.nthash = nthash
        self.local_auth = local_auth

        
        self.domain = ''
        if domain:
            self.set_domain(domain)

        if ticket_file:
            result = self.valid_ticket(ticket_file)
            if not result.retval:
                raise Exception(result.retmsg)
            self.auth_method = AUTH_KERBEROS
        elif nthash:
            result = self.valid_nthash(nthash)
            if not result.retval:
                raise Exception(result.retmsg)
            if nthash and not user:
                raise Exception("NT hash given (-H) without any user, please provide a username (-u)")
            self.auth_method = AUTH_NTHASH
        elif not user and not pw:
            self.auth_method = AUTH_NULL
        else:
            if pw and not user:
                raise Exception("Password given (-p) without any user, please provide a username (-u)")
            self.auth_method = AUTH_PASSWORD

    def valid_nthash(self, nthash):
        hash_len = len(nthash)
        if hash_len != 32:
            return Result(False, f'The given hash has {hash_len} characters instead of 32 characters')
        if not re.match(r"^[a-fA-F0-9]{32}$", nthash):
            return Result(False, f'The given hash contains invalid characters')
        return Result(True, '')

    def valid_ticket(self, ticket_file):
        return valid_file(ticket_file)

    
    
    
    
    def set_domain(self, domain):
        if self.domain and self.domain.lower() == domain.lower():
            return True
        if not self.domain:
            self.domain = domain
            return True
        return False

    def as_dict(self):
        return {'credentials':OrderedDict({'auth_method':self.auth_method, 'user':self.user, 'password':self.pw, 'domain':self.domain, 'ticket_file':self.ticket_file, 'nthash':self.nthash, 'random_user':self.random_user})}


class SambaTool():
    '''
    Encapsulates various Samba Tools.
    '''

    def __init__(self, command, target, creds):
        self.target = target
        self.creds = creds
        self.env = None

        
        self.exec = []

        
        if self.creds:
            if creds.ticket_file:
                
                
                self.env = os.environ.copy()
                self.env['KRB5CCNAME'] = self.creds.ticket_file
                
                
                if GLOBAL_SAMBA_LEGACY:
                    self.exec += ['-k']
                else:
                    self.exec += ['--use-krb5-ccache', self.creds.ticket_file]
            elif creds.nthash:
                self.exec += ['-W', f'{self.creds.domain}']
                self.exec += ['-U', f'{self.creds.user}%{self.creds.nthash}', '--pw-nt-hash']
            else:
                self.exec += ['-W', f'{self.creds.domain}']
                self.exec += ['-U', f'{self.creds.user}%{self.creds.pw}']

        
        
        
        if target.samba_config:
            self.exec += ['-s', f'{target.samba_config.get_path()}']

        
        
        
        
        
        

    def run(self, log, error_filter=True):
        '''
        Runs a samba client command (net, nmblookup, smbclient or rpcclient) and does some basic output filtering.
        '''

        if GLOBAL_VERBOSE and log:
            print_verbose(f"{log}, running command: {' '.join(shlex.quote(x) for x in self.exec)}")

        try:
            output = check_output(self.exec, env=self.env, shell=False, stderr=STDOUT, timeout=self.target.timeout)
            retval = 0
        except TimeoutExpired:
            return Result(False, "timed out")
        except Exception as e:
            output = e.output
            retval = 1

        output = output.decode()
        for line in output.splitlines(True):
            if any(entry in line for entry in SAMBA_CLIENT_ERRORS):
                output = output.replace(line, "")
        output = output.rstrip('\n')

        if "Cannot find KDC for realm" in output:
            return Result(False, "Cannot find KDC for realm, check DNS settings or setup /etc/krb5.conf")

        if retval == 1 and not output:
            return Result(False, "empty response")

        if error_filter:
            nt_status_error = nt_status_error_filter(output)
            if nt_status_error:
                return Result(False, nt_status_error)

        return Result(True, output)

class SambaSmbclient(SambaTool):
    '''
    Encapsulates a subset of the functionality of the Samba smbclient command.
    '''
    def __init__(self, command, target, creds):
        super().__init__(command, target, creds)

        
        self.exec += ['-t', f'{target.timeout}']

        
        if command[0] == 'list':
            self.exec += ['-L', f'//{target.host}', '-g']
        elif command[0] == 'help':
            self.exec += ['-c','help', f'//{target.host}/ipc$']
        elif command[0] == 'dir' and command[1]:
            self.exec += ['-c','dir', f'//{target.host}/{command[1]}']

        self.exec = ['smbclient'] + self.exec

class SambaRpcclient(SambaTool):
    '''
    Encapsulates a subset of the functionality of the Samba rpcclient command.
    '''
    def __init__(self, command, target, creds):
        super().__init__(command, target, creds)

        
        if command[0] == 'queryuser':
            rid = command[1]
            self.exec += ['-c', f'{command[0]} {rid}']
        elif command[0] == 'querygroup':
            rid = command[1]
            self.exec += ['-c', f'{command[0]} {rid}']
        elif command[0] == 'enumalsgroups':
            group_type = command[1]
            self.exec += ['-c', f'{command[0]} {group_type}']
        elif command[0] == 'lookupnames':
            username = command[1]
            self.exec += ['-c', f'{command[0]} {username}']
        elif command[0] == 'lookupsids':
            sid = command[1]
            self.exec += ['-c', f'{command[0]} {sid}']
        
        
        
        
        
        
        else:
            self.exec += ['-c', f'{command[0]}']

        self.exec += [ target.host ]
        self.exec = ['rpcclient'] + self.exec

class SambaNet(SambaTool):
    '''
    Encapsulates a subset of the functionality of the Samba net command.
    '''
    def __init__(self, command, target, creds):
        super().__init__(command, target, creds)

        
        self.exec += ['-t', f'{target.timeout}']

        
        if command[0] == 'rpc':
            if command[1] == 'group':
                if command[2] == 'members':
                    groupname = command[3]
                    self.exec += [f'{command[0]}', f'{ command[1]}', f'{command[2]}', groupname]
            if command[1] == 'service':
                if command[2] == 'list':
                    self.exec += [f'{command[0]}', f'{ command[1]}', f'{command[2]}']

        self.exec += [ "-S", target.host ]
        self.exec = ['net'] + self.exec

class SambaNmblookup(SambaTool):
    '''
    Encapsulates the nmblookup command. Currently only the -A option is supported.
    '''
    def __init__(self, target):
        super().__init__(None, target, creds=None)

        self.exec += [ "-A", target.host ]
        self.exec = ['nmblookup'] + self.exec

class SambaConfig:
    '''
    Allows to create custom Samba configurations which can be passed via path to the various Samba client tools.
    Currently such a configuration is always created on tool start. This allows to overcome issues with newer
    releases of the Samba client tools where certain features are disabled by default.
    '''
    def __init__(self, entries):
        config = '\n'.join(['[global]']+entries) + '\n'
        with tempfile.NamedTemporaryFile(delete=False) as config_file:
            config_file.write(config.encode())
            self.config_filename = config_file.name

    def get_path(self):
        return self.config_filename

    def add(self, entries):
        try:
            config = '\n'.join(entries) + '\n'
            with open(self.config_filename, 'a') as config_file:
                config_file.write(config)
            return True
        except:
            return False

    def delete(self):
        try:
            os.remove(self.config_filename)
        except OSError:
            return Result(False, f"Could not delete samba configuration file {self.config_filename}")
        return Result(True, "")

class Output:
    '''
    Output stores the output dictionary which will be filled out during the run of
    the tool. The update() function takes a dictionary, which will then be merged
    into the output dictionary (out_dict). In addition, the update() function is
    responsible for writing the JSON/YAML output.
    '''
    def __init__(self, out_file=None, out_file_type=None):
        self.out_file = out_file
        self.out_file_type = out_file_type
        self.out_dict = OrderedDict({"errors":{}})

    def update(self, content):
        
        

        "errors" sub dict. Then update out_dict with the new
        "content" also had an "errors" dict (e.g. if the module run failed),
        "errors" dict from the previous run. Therefore,
        "errors"] with the saved one. A proper merge will
        
        old_errors_dict = self.out_dict["errors"]
        self.out_dict.update(content)
        self.out_dict["errors"] = old_errors_dict

        
        if "errors" in content:
            new_errors_dict = content["errors"]

            for key, value in new_errors_dict.items():
                if key in old_errors_dict:
                    self.out_dict["errors"][key] = {**old_errors_dict[key], **new_errors_dict[key]}
                else:
                    self.out_dict["errors"][key] = value

    def flush(self):
        
        self.out_dict.move_to_end("errors")

        
        if self.out_file is not None:
            if "json" in self.out_file_type and not self._write_json():
                return Result(False, f"Could not write JSON output to {self.out_file}.json")
            if "yaml" in self.out_file_type and not self._write_yaml():
                return Result(False, f"Could not write YAML output to {self.out_file}.yaml")
        return Result(True, "")

    def _write_json(self):
        try:
            with open(f"{self.out_file}.json", 'w') as f:
                f.write(json.dumps(self.out_dict, indent=4))
        except OSError:
            return False
        return True

    def _write_yaml(self):
        try:
            with open(f"{self.out_file}.yaml", 'w') as f:
                f.write(yamlize(self.out_dict, rstrip=False))
        except OSError:
            return False
        return True

    def as_dict(self):
        return self.out_dict



class ListenersScan():
    def __init__(self, target, scan_list):
        self.target = target
        self.scan_list = scan_list
        self.listeners = OrderedDict({})

    def run(self):
        module_name = ENUM_LISTENERS
        output = {}

        print_heading(f"Listener Scan on {self.target.host}")
        for listener, port in SERVICES.items():
            if listener not in self.scan_list:
                continue

            print_info(f"Checking {listener}")
            result = self.check_accessible(listener, port)
            if result.retval:
                print_success(result.retmsg)
            else:
                output = process_error(result.retmsg, ["listeners"], module_name, output)

            self.listeners[listener] = {"port": port, "accessible": result.retval}

        output["listeners"] = self.listeners

        return output

    def check_accessible(self, listener, port):
        if self.target.ip_version == 6:
            address_family = socket.AF_INET6
        elif self.target.ip_version == 4:
            address_family = socket.AF_INET

        try:
            sock = socket.socket(address_family, socket.SOCK_STREAM)
            sock.settimeout(self.target.timeout)
            result = sock.connect_ex((self.target.host, port))
            if result == 0:
                return Result(True, f"{listener} is accessible on {port}/tcp")
            return Result(False, f"Could not connect to {listener} on {port}/tcp: {SOCKET_ERRORS[result]}")
        except Exception:
            return Result(False, f"Could not connect to {listener} on {port}/tcp")

    def get_accessible_listeners(self):
        accessible = []
        for listener, entry in self.listeners.items():
            if entry["accessible"] is True:
                accessible.append(listener)
        return accessible

    def get_accessible_ports_by_pattern(self, pattern):
        accessible = []
        for listener, entry in self.listeners.items():
            if pattern in listener and entry["accessible"] is True:
                accessible.append(entry["port"])
        return accessible



class EnumNetbios():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run NetBIOS module which collects Netbios names and the workgroup/domain.
        '''
        module_name = ENUM_NETBIOS
        print_heading(f"NetBIOS Names and Workgroup/Domain for {self.target.host}")
        output = {"domain":None, "nmblookup":None}

        nmblookup = self.nmblookup()
        if nmblookup.retval:
            result = self.get_domain(nmblookup.retval)
            if result.retval:
                print_success(result.retmsg)
                output["domain"] = result.retval
            else:
                output = process_error(result.retmsg, ["domain"], module_name, output)

            result = self.nmblookup_to_human(nmblookup.retval)
            print_success(result.retmsg)
            output["nmblookup"] = result.retval
        else:
            output = process_error(nmblookup.retmsg, ["nmblookup", "domain"], module_name, output)

        return output

    def nmblookup(self):
        '''
        Runs nmblookup (a NetBIOS over TCP/IP Client) in order to lookup NetBIOS names information.
        '''

        result = SambaNmblookup(self.target).run(log='Trying to get NetBIOS names information')

        if not result.retval:
            return Result(None, f"Could not get NetBIOS names information via 'nmblookup': {result.retmsg}")

        if "No reply from" in result.retmsg:
            return Result(None, "Could not get NetBIOS names information via 'nmblookup': host does not reply")

        return Result(result.retmsg, "")

    def get_domain(self, nmblookup_result):
        '''
        Extract domain from given nmblookoup result.
        '''
        match = re.search(r"^\s+(\S+)\s+<00>\s+-\s+<GROUP>\s+", nmblookup_result, re.MULTILINE)
        if match:
            if valid_domain(match.group(1)):
                domain = match.group(1)
            else:
                return Result(None, f"Workgroup {domain} contains some illegal characters")
        else:
            return Result(None, "Could not find domain/domain")

        if not self.creds.local_auth:
            self.creds.set_domain(domain)
        return Result(domain, f"Got domain/workgroup name: {domain}")

    def nmblookup_to_human(self, nmblookup_result):
        '''
        Map nmblookup output to human readable strings.
        '''
        output = []
        nmblookup_result = nmblookup_result.splitlines()
        for line in nmblookup_result:
            if "Looking up status of" in line or line == "":
                continue

            line = line.replace("\t", "")
            match = re.match(r"^(\S+)\s+<(..)>\s+-\s+?(<GROUP>)?\s+?[A-Z]", line)
            if match:
                line_val = match.group(1)
                line_code = match.group(2).upper()
                line_group = not match.group(3)
                for entry in NBT_INFO:
                    pattern, code, group, desc = entry
                    if pattern:
                        if pattern in line_val and line_code == code and line_group == group:
                            output.append(line + " " + desc)
                            break
                    else:
                        if line_code == code and line_group == group:
                            output.append(line + " " + desc)
                            break
            else:
                output.append(line)
        return Result(output, f"Full NetBIOS names information:\n{yamlize(output)}")



class EnumSmb():
    def __init__(self, target, detailed):
        self.target = target
        self.detailed = detailed

    def run(self):
        '''
        Run SMB module which checks for the supported SMB dialects.
        '''
        module_name = ENUM_SMB
        print_heading(f"SMB Dialect Check on {self.target.host}")
        output = {}

        for port in self.target.smb_ports:
            print_info(f"Trying on {port}/tcp")
            self.target.port = port
            result = self.check_smb_dialects()
            if result.retval is None:
                output = process_error(result.retmsg, ["smb1_only"], module_name, output)
            else:
                output["smb_dialects"] = result.retval
                print_success(result.retmsg)
                break

        
        if result.retval and result.retval["SMB1 only"]:
            print_info("Enforcing legacy SMBv1 for further enumeration")
            result = self.enforce_smb1()
            if not result.retval:
                output = process_error(result.retmsg, ["smb_dialects"], module_name, output)

        output["smb_dialects"] = result.retval
        return output

    def enforce_smb1(self):
        try:
            if self.target.samba_config.add(['client min protocol = NT1']):
                return Result(True, "")
        except:
            pass
        return Result(False, "Could not enforce SMBv1")

    def check_smb_dialects(self):
        '''
        Current implementations of the samba client tools will enforce at least SMBv2 by default. This will give false
        negatives during session checks, if the target only supports SMBv1. Therefore, we try to find out here whether
        the target system only speaks SMBv1.
        '''
        supported = {
                SMB_DIALECTS[SMB_DIALECT]: False,
                SMB_DIALECTS[SMB2_DIALECT_002]: False,
                SMB_DIALECTS[SMB2_DIALECT_21]:False,
                SMB_DIALECTS[SMB2_DIALECT_30]:False,
                SMB_DIALECTS[SMB2_DIALECT_311]:False,
                }

        output = {
                "Supported dialects": None,
                "Preferred dialect": None,
                "SMB1 only": False,
                "SMB signing required": None
        }

        
        smb_dialects = [SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21, SMB2_DIALECT_30, SMB2_DIALECT_311]

        
        last_supported_dialect = None
        for dialect in smb_dialects:
            try:
                smb_conn = smbconnection.SMBConnection(self.target.host, self.target.host, sess_port=self.target.port, timeout=self.target.timeout, preferredDialect=dialect)
                smb_conn.close()
                supported[SMB_DIALECTS[dialect]] = True
                last_supported_dialect = dialect
            except Exception:
                pass

        
        self.target.smb1_supported = supported[SMB_DIALECTS[SMB_DIALECT]]

        
        preferred_dialect = None
        if sum(1 for value in supported.values() if value is True) == 1:
            if last_supported_dialect == SMB_DIALECT:
                output["SMB1 only"] = True
                self.target.smb1_only = True
            preferred_dialect = last_supported_dialect

        try:
            smb_conn = smbconnection.SMBConnection(self.target.host, self.target.host, sess_port=self.target.port, timeout=self.target.timeout, preferredDialect=preferred_dialect)
            preferred_dialect = smb_conn.getDialect()
            
            output["SMB signing required"] = smb_conn.isSigningRequired()
            smb_conn.close()

            output["Preferred dialect"] = SMB_DIALECTS[preferred_dialect]
            self.target.smb_preferred_dialect = preferred_dialect
        except Exception as exc:
            
            if isinstance(exc, (smb3.SessionError)):
                if nt_status_error_filter(str(exc)) == "STATUS_NOT_SUPPORTED":
                    output["Preferred Dialect"] = "> SMB 3.0"

        output["Supported dialects"] = supported

        
        
        if not output["Preferred dialect"]:
            return Result(None, f"No supported dialects found")
        return Result(output, f"Supported dialects and settings:\n{yamlize(output)}")



class EnumSessions():
    SESSION_USER = "user"
    SESSION_RANDOM = "random user"
    SESSION_NULL = "null"
    SESSION_KERBEROS="Kerberos"
    SESSION_NTHASH="NT hash"

    def __init__(self, target, creds):

        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run session check module which tests for user and null sessions.
        '''
        module_name = ENUM_SESSIONS
        print_heading(f"RPC Session Check on {self.target.host}")
        output = { "sessions":None }
        sessions = {"sessions_possible":False,
                  AUTH_NULL:False,
                  AUTH_PASSWORD:False,
                  AUTH_KERBEROS:False,
                  AUTH_NTHASH:False,
                  "random_user":False,
                  }

        
        print_info("Check for null session")
        null_session = self.check_session(Credentials('', '', self.creds.domain), self.SESSION_NULL)
        if null_session.retval:
            sessions[AUTH_NULL] = True
            print_success(null_session.retmsg)
        else:
            output = process_error(null_session.retmsg, ["sessions"], module_name, output)

        
        if self.creds.ticket_file:
            print_info("Check for Kerberos session")
            kerberos_session = self.check_session(self.creds, self.SESSION_KERBEROS)
            if kerberos_session.retval:
                sessions[AUTH_KERBEROS] = True
                print_success(kerberos_session.retmsg)
            else:
                output = process_error(kerberos_session.retmsg, ["sessions"], module_name, output)
        
        elif self.creds.nthash:
            print_info("Check for NT hash session")
            nthash_session = self.check_session(self.creds, self.SESSION_NTHASH)
            if nthash_session.retval:
                sessions[AUTH_NTHASH] = True
                print_success(nthash_session.retmsg)
            else:
                output = process_error(nthash_session.retmsg, ["sessions"], module_name, output)
        
        elif self.creds.user:
            print_info("Check for user session")
            user_session = self.check_session(self.creds, self.SESSION_USER)
            if user_session.retval:
                sessions[AUTH_PASSWORD] = True
                print_success(user_session.retmsg)
            else:
                output = process_error(user_session.retmsg, ["sessions"], module_name, output)

        
        print_info("Check for random user")
        user_session = self.check_session(Credentials(self.creds.random_user, self.creds.pw, self.creds.domain), self.SESSION_RANDOM)
        if user_session.retval:
            sessions["random_user"] = True
            print_success(user_session.retmsg)
            print_hint(f"Rerunning enumeration with user '{self.creds.random_user}' might give more results")
        else:
            output = process_error(user_session.retmsg, ["sessions"], module_name, output)

        if sessions[AUTH_NULL] or \
            sessions[AUTH_PASSWORD] or \
            sessions[AUTH_KERBEROS] or \
            sessions[AUTH_NTHASH] or \
            sessions["random_user"]:
            sessions["sessions_possible"] = True
        else:
            process_error("Sessions failed, neither null nor user sessions were possible", ["sessions"], module_name, output)

        output['sessions'] = sessions
        return output

    def check_session(self, creds, session_type):
        '''
        Tests access to the IPC$ share.

        General explanation:
        The Common Internet File System(CIFS/Server Message Block (SMB) protocol specifies
        mechanisms for interprocess communication over the network. This is called a named pipe.
        In order to be able to "talk" to these named pipes, a special share named "IPC$" is provided.
        SMB clients can access named pipes by using this share. Older Windows versions supported
        anonymous access to this share (empty username and password), which is called a "null sessions".
        This is a security vulnerability since it allows to gain valuable information about the host
        system.

        How the test works:
        In order to test for a null session, the smbclient command is used, by tring to connect to the
        IPC$ share. If that works, smbclient's 'help' command will be run. If the login was successfull,
        the help command will return a list of possible commands. One of these commands is called
        'case_senstive'. We search for this command as an indicator that the IPC session was setup correctly.
        '''

        result = SambaSmbclient(['help'], self.target, creds).run(log='Attempting to make session')

        if not result.retval:
            return Result(False, f"Could not establish {session_type} session: {result.retmsg}")

        if "case_sensitive" in result.retmsg:
            if session_type == self.SESSION_KERBEROS:
                return Result(True, f"Server allows Kerberos session using '{creds.ticket_file}'")
            if session_type == self.SESSION_NTHASH:
                return Result(True, f"Server allows NT hash session using '{creds.nthash}'")
            return Result(True, f"Server allows session using username '{creds.user}', password '{creds.pw}'")
        return Result(False, f"Could not establish session using '{creds.user}', password '{creds.pw}'")



class EnumLdapDomainInfo():
    def __init__(self, target):
        self.target = target

    def run(self):
        '''
        Run ldapsearch module which tries to find out whether host is a parent or
        child DC. Also tries to fetch long domain name. The information are get from
        the LDAP RootDSE.
        '''
        module_name = ENUM_LDAP_DOMAIN_INFO
        print_heading(f"Domain Information via LDAP for {self.target.host}")
        output = {"is_parent_dc":None,
                  "is_child_dc":None,
                  "long_domain":None}

        for with_tls in [False, True]:
            if with_tls:
                if SERVICES[SERVICE_LDAPS] not in self.target.ldap_ports:
                    continue
                print_info('Trying LDAPS')
            else:
                if SERVICES[SERVICE_LDAP] not in self.target.ldap_ports:
                    continue
                print_info('Trying LDAP')
            self.target.tls = with_tls
            namingcontexts = self.get_namingcontexts()
            if namingcontexts.retval is not None:
                break
            output = process_error(namingcontexts.retmsg, ["is_parent_dc", "is_child_dc", "long_domain"], module_name, output)

        if namingcontexts.retval:
            
            result = self.check_parent_dc(namingcontexts.retval)
            if result.retval:
                output["is_parent_dc"] = True
                output["is_child_dc"] = False
            else:
                output["is_parent_dc"] = True
                output["is_child_dc"] = False
            print_success(result.retmsg)

            
            result = self.get_long_domain(namingcontexts.retval)
            if result.retval:
                print_success(result.retmsg)
                output["long_domain"] = result.retval
            else:
                output = process_error(result.retmsg, ["long_domain"], module_name, output)

        return output

    def get_namingcontexts(self):
        '''
        Tries to connect to LDAP/LDAPS. If successful, it tries to get the naming contexts from
        the so called Root Directory Server Agent Service Entry (RootDSE).
        '''
        try:
            server = Server(self.target.host, use_ssl=self.target.tls, get_info=DSA, connect_timeout=self.target.timeout)
            ldap_con = Connection(server, auto_bind=True)
            ldap_con.unbind()
        except Exception as e:
            if len(e.args) == 1:
                error = str(e.args[0])
            else:
                error = str(e.args[1][0][0])
            if "]" in error:
                error = error.split(']', 1)[1]
            elif ":" in error:
                error = error.split(':', 1)[1]
            error = error.lstrip().rstrip()
            if self.target.tls:
                return Result(None, f"LDAPS connect error: {error}")
            return Result(None, f"LDAP connect error: {error}")

        try:
            if not server.info.naming_contexts:
                return Result([], "NamingContexts are not readable")
        except Exception:
            return Result([], "NamingContexts are not readable")

        return Result(server.info.naming_contexts, "")

    def get_long_domain(self, namingcontexts_result):
        '''
        Tries to extract the long domain from the naming contexts.
        '''
        long_domain = ""

        for entry in namingcontexts_result:
            match = re.search("(DC=[^,]+,DC=[^,]+)$", entry)
            if match:
                long_domain = match.group(1)
                long_domain = long_domain.replace("DC=", "")
                long_domain = long_domain.replace(",", ".")
                break
        if long_domain:
            return Result(long_domain, f"Long domain name is: {long_domain}")
        return Result(None, "Could not find long domain")

    def check_parent_dc(self, namingcontexts_result):
        '''
        Checks whether the target is a parent or child domain controller.
        This is done by searching for specific naming contexts.
        '''
        parent = False
        namingcontexts_result = '\n'.join(namingcontexts_result)
        if "DC=DomainDnsZones" in namingcontexts_result or "ForestDnsZones" in namingcontexts_result:
            parent = True
        if parent:
            return Result(True, "Appears to be root/parent DC")
        return Result(False, "Appears to be child DC")



class EnumSmbDomainInfo():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module EnumSmbDomainInfo  which extracts domain information from
        Session Setup Request packets.
        '''
        module_name = ENUM_SMB_DOMAIN_INFO
        print_heading(f"Domain Information via SMB session for {self.target.host}")
        output = {"smb_domain_info":None}

        for port in self.target.smb_ports:
            self.target.port = port
            print_info(f"Enumerating via unauthenticated SMB session on {port}/tcp")
            result_smb = self.enum_from_smb()
            if result_smb.retval:
                print_success(result_smb.retmsg)
                output["smb_domain_info"] = result_smb.retval
                break
            output = process_error(result_smb.retmsg, ["smb_domain_info"], module_name, output)

        return output

    def enum_from_smb(self):
        '''
        Tries to set up an SMB null session. Even if the null session does not succeed, the SMB protocol will transfer
        some information about the remote system in the SMB "Session Setup Response" or the SMB "Session Setup andX Response"
        packet. These are the domain, DNS domain name as well as DNS host name.
        '''
        smb_domain_info = {"NetBIOS computer name":None, "NetBIOS domain name":None, "DNS domain":None, "FQDN":None, "Derived membership":None, "Derived domain":None}

        smb_conn = None
        try:
            smb_conn = smbconnection.SMBConnection(remoteName=self.target.host, remoteHost=self.target.host, sess_port=self.target.port, timeout=self.target.timeout, preferredDialect=self.target.smb_preferred_dialect)
            smb_conn.login("", "", "")
        except Exception as e:
            error_msg = process_impacket_smb_exception(e, self.target)
            
            
            if not "STATUS_ACCESS_DENIED" in error_msg:
                return Result(None, error_msg)

        "Session Setup AndX Response" packet.
        
        try:
            smb_domain_info["NetBIOS domain name"] = smb_conn.getServerDomain()
            smb_domain_info["NetBIOS computer name"] = smb_conn.getServerName()
            smb_domain_info["FQDN"] = smb_conn.getServerDNSHostName().rstrip('\x00')
            smb_domain_info["DNS domain"] = smb_conn.getServerDNSDomainName().rstrip('\x00')
        except:
            pass

        
        
        
        
        
        
        
        

        if (smb_domain_info["NetBIOS computer name"] and
                smb_domain_info["NetBIOS domain name"] and
                smb_domain_info["DNS domain"] and
                smb_domain_info["FQDN"] and
                smb_domain_info["DNS domain"] in smb_domain_info["FQDN"] and
                '.' in smb_domain_info["FQDN"]):

            smb_domain_info["Derived domain"] = smb_domain_info["NetBIOS domain name"]
            smb_domain_info["Derived membership"] = "domain member"

            if not self.creds.local_auth:
                self.creds.set_domain(smb_domain_info["NetBIOS domain name"])
        elif (smb_domain_info["NetBIOS domain name"] and
                not smb_domain_info["NetBIOS computer name"] and
                not smb_domain_info["FQDN"] and
                not smb_domain_info["DNS domain"]):

            smb_domain_info["Derived domain"] = smb_domain_info["NetBIOS domain name"]
            smb_domain_info["Derived membership"] = "workgroup member"

            if not self.creds.local_auth:
                self.creds.set_domain(smb_domain_info["NetBIOS domain name"])
        elif smb_domain_info["NetBIOS computer name"]:

            smb_domain_info["Derived domain"] = "unknown"
            smb_domain_info["Derived membership"] = "workgroup member"

            if self.creds.local_auth:
                self.creds.set_domain(smb_domain_info["NetBIOS computer name"])

        
        if not self.creds.domain:
            self.creds.set_domain('WORKGROUP')

        if not any(smb_domain_info.values()):
            return Result(None, "Could not enumerate domain information via unauthenticated SMB")
        return Result(smb_domain_info, f"Found domain information via SMB\n{yamlize(smb_domain_info)}")



class EnumLsaqueryDomainInfo():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module lsaquery which tries to get domain information like
        the domain/workgroup name, domain SID and the membership type.
        '''
        module_name = ENUM_LSAQUERY_DOMAIN_INFO
        print_heading(f"Domain Information via RPC for {self.target.host}")
        output = {}
        rpc_domain_info = {"Domain":None,
                           "Domain SID":None,
                           "Membership":None}

        lsaquery = self.lsaquery()
        if lsaquery.retval is not None:
            
            result = self.get_domain(lsaquery.retval)
            if result.retval:
                print_success(result.retmsg)
                rpc_domain_info["Domain"] = result.retval

                
                
                
                
                
                if not self.creds.local_auth and not self.creds.set_domain(result.retval):
                    print_hint(f"Found domain/workgroup '{result.retval}' which is different from the currently used one '{self.creds.domain}'.")
            else:
                output = process_error(result.retmsg, ["rpc_domain_info"], module_name, output)

            
            result = self.get_domain_sid(lsaquery.retval)
            if result.retval:
                print_success(result.retmsg)
                rpc_domain_info["Domain SID"] = result.retval
            else:
                output = process_error(result.retmsg, ["rpc_domain_info"], module_name, output)

            
            result = self.check_is_part_of_workgroup_or_domain(lsaquery.retval)
            if result.retval:
                print_success(result.retmsg)
                rpc_domain_info["Membership"] = result.retval
            else:
                output = process_error(result.retmsg, ["rpc_domain_info"], module_name, output)
        else:
            output = process_error(lsaquery.retmsg, ["rpc_domain_info"], module_name, output)

        output["rpc_domain_info"] = rpc_domain_info
        return output

    def lsaquery(self):
        '''
        Uses the rpcclient command to connect to the named pipe LSARPC (Local Security Authority Remote Procedure Call),
        which allows to do remote management of domain security policies. In this specific case, we use rpcclient's lsaquery
        command. This command will do an LSA_QueryInfoPolicy request to get the domain name and the domain service identifier
        (SID).
        '''

        result = SambaRpcclient(['lsaquery'], self.target, self.creds).run(log='Attempting to get domain SID')

        if not result.retval:
            return Result(None, f"Could not get domain information via 'lsaquery': {result.retmsg}")

        if result.retval:
            return Result(result.retmsg, "")
        return Result(None, "Could not get information via 'lsaquery'")

    def get_domain(self, lsaquery_result):
        '''
        Takes the result of rpclient's lsaquery command and tries to extract the workgroup/domain.
        '''
        domain = ""
        if "Domain Name" in lsaquery_result:
            match = re.search("Domain Name: (.*)", lsaquery_result)
            if match:
                domain = match.group(1)

        if domain:
            return Result(domain, f"Domain: {domain}")
        return Result(None, "Could not get workgroup/domain from lsaquery")

    def get_domain_sid(self, lsaquery_result):
        '''
        Takes the result of rpclient's lsaquery command and tries to extract the domain SID.
        '''
        domain_sid = None
        if "Domain Sid: (NULL SID)" in lsaquery_result:
            domain_sid = "NULL SID"
        else:
            match = re.search(r"Domain Sid: (S-\d+-\d+-\d+-\d+-\d+-\d+)", lsaquery_result)
            if match:
                domain_sid = match.group(1)
        if domain_sid:
            return Result(domain_sid, f"Domain SID: {domain_sid}")
        return Result(None, "Could not get domain SID from lsaquery")

    def check_is_part_of_workgroup_or_domain(self, lsaquery_result):
        '''
        Takes the result of rpclient's lsaquery command and tries to determine from the result whether the host
        is part of a domain or workgroup.
        '''
        if "Domain Sid: S-0-0" in lsaquery_result or "Domain Sid: (NULL SID)" in lsaquery_result:
            return Result("workgroup member", "Membership: workgroup member")
        if re.search(r"Domain Sid: S-\d+-\d+-\d+-\d+-\d+-\d+", lsaquery_result):
            return Result("domain member", "Membership: domain member")
        return Result(False, "Could not determine if host is part of domain or part of a workgroup")



class EnumOsInfo():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module OS info which tries to collect OS information. The module supports both authenticated and unauthenticated
        enumeration. This allows to get some target information without having a working session for many systems.
        '''
        module_name = ENUM_OS_INFO
        print_heading(f"OS Information via RPC for {self.target.host}")
        output = {"os_info":None}
        os_info = {"OS":None, "OS version":None, "OS release": None, "OS build": None, "Native OS":None, "Native LAN manager": None, "Platform id":None, "Server type":None, "Server type string":None}

        
        for port in self.target.smb_ports:
            self.target.port = port
            print_info(f"Enumerating via unauthenticated SMB session on {port}/tcp")
            result_smb = self.enum_from_smb()
            if result_smb.retval:
                print_success(result_smb.retmsg)
                break
            output = process_error(result_smb.retmsg, ["os_info"], module_name, output)

        if result_smb.retval:
            os_info = {**os_info, **result_smb.retval}

        
        print_info("Enumerating via 'srvinfo'")
        if self.target.sessions[self.creds.auth_method]:
            result_srvinfo = self.enum_from_srvinfo()
            if result_srvinfo.retval:
                print_success(result_srvinfo.retmsg)
            else:
                output = process_error(result_srvinfo.retmsg, ["os_info"], module_name, output)

            if result_srvinfo.retval is not None:
                os_info = {**os_info, **result_srvinfo.retval}
        else:
            output = process_error("Skipping 'srvinfo' run, not possible with provided credentials", ["os_info"], module_name, output)

        
        if result_smb.retval or (self.target.sessions[self.creds.auth_method] and result_srvinfo.retval):
            os_info = self.os_info_to_human(os_info)
            print_success(f"After merging OS information we have the following result:\n{yamlize(os_info)}")
            output["os_info"] = os_info

        return output

    def srvinfo(self):
        '''
        Uses rpcclient's srvinfo command to connect to the named pipe SRVSVC in order to call
        NetSrvGetInfo() on the target. This will return OS information (OS version, platform id,
        server type).
        '''

        result = SambaRpcclient(['srvinfo'], self.target, self.creds).run(log='Attempting to get OS info with command')

        if not result.retval:
            return Result(None, f"Could not get OS info via 'srvinfo': {result.retmsg}")

        
        
        if "NT_STATUS_REQUEST_NOT_ACCEPTED" in result.retmsg:
            return Result(None, 'Could not get OS information via srvinfo: STATUS_REQUEST_NOT_ACCEPTED - too many RPC sessions open?')

        return Result(result.retmsg, "")

    def enum_from_srvinfo(self):
        '''
        Parses the output of rpcclient's srvinfo command and extracts the various information.
        '''
        result = self.srvinfo()

        if result.retval is None:
            return result

        os_info = {"OS version":None, "Server type":None, "Server type string":None, "Platform id":None}
        search_patterns = {
                "platform_id":"Platform id",
                "os version":"OS version",
                "server type":"Server type"
                }
        first = True
        for line in result.retval.splitlines():

            if first:
                match = re.search(r"\s+[^\s]+\s+(.*)", line)
                if match:
                    os_info['Server type string'] = match.group(1).rstrip()
                first = False

            for search_pattern in search_patterns.keys():
                match = re.search(fr"\s+{search_pattern}\s+:\s+(.*)", line)
                if match:
                    os_info[search_patterns[search_pattern]] = match.group(1)

        if not os_info:
            return Result(None, "Could not parse result of 'srvinfo' command, please open a GitHub issue")
        return Result(os_info, "Found OS information via 'srvinfo'")

    def enum_from_smb(self):
        '''
        Tries to set up an SMB null session. Even if the null session does not succeed, the SMB protocol will transfer
        some information about the remote system in the SMB "Session Setup Response" or the SMB "Session Setup andX Response"
        packet. This is the major and minor OS version as well as the build number. In SMBv1 also the "Native OS" as well as
        the "Native LAN Manager" will be reported.
        '''
        os_info = {"OS version":None, "OS release":None, "OS build":None, "Native LAN manager":None, "Native OS":None}

        os_major = None
        os_minor = None

        "Native OS" (e.g. "Windows 5.1")  and "Native LAN Manager"
        "Windows 2000 LAN Manager") field in the "Session Setup AndX Response" packet.
        "OS Major" (e.g. 5), "OS Minor" (e.g. 1) as well as the
        "OS Build" fields in the "SMB2 Session Setup Response packet".

        if self.target.smb1_supported:
            smb_conn = None
            try:
                smb_conn = smbconnection.SMBConnection(remoteName=self.target.host, remoteHost=self.target.host, sess_port=self.target.port, timeout=self.target.timeout, preferredDialect=SMB_DIALECT)
                smb_conn.login("", "", "")
            except Exception as e:
                error_msg = process_impacket_smb_exception(e, self.target)
                if not "STATUS_ACCESS_DENIED" in error_msg:
                    return Result(None, error_msg)

            if self.target.smb1_only:
                os_info["OS build"] = "not supported"
                os_info["OS release"] = "not supported"

            try:
                native_lanman = smb_conn.getSMBServer().get_server_lanman()
                if native_lanman:
                    os_info["Native LAN manager"] = f"{native_lanman}"

                native_os = smb_conn.getSMBServer().get_server_os()
                if native_os:
                    os_info["Native OS"] = f"{native_os}"
                    match = re.search(r"Windows ([0-9])\.([0-9])", native_os)
                    if match:
                        os_major = match.group(1)
                        os_minor = match.group(2)
            except AttributeError:
                os_info["Native LAN manager"] = "not supported"
                os_info["Native OS"] = "not supported"
            except:
                pass

        if not self.target.smb1_only:
            smb_conn = None
            try:
                smb_conn = smbconnection.SMBConnection(remoteName=self.target.host, remoteHost=self.target.host, sess_port=self.target.port, timeout=self.target.timeout, preferredDialect=self.target.smb_preferred_dialect)
                smb_conn.login("", "", "")
            except Exception as e:
                error_msg = process_impacket_smb_exception(e, self.target)
                if not "STATUS_ACCESS_DENIED" in error_msg:
                    return Result(None, error_msg)

            if not self.target.smb1_supported:
                os_info["Native LAN manager"] = "not supported"
                os_info["Native OS"] = "not supported"

            try:
                os_major = smb_conn.getServerOSMajor()
                os_minor = smb_conn.getServerOSMinor()
            except:
                pass

            try:
                os_build = smb_conn.getServerOSBuild()
                if os_build is not None:
                    os_info["OS build"] = f"{os_build}"
                    if str(os_build) in OS_RELEASE:
                        os_info["OS release"] = OS_RELEASE[f"{os_build}"]
                    else:
                        os_info["OS release"] = ""
                else:
                    os_info["OS build"] = "not supported"
                    os_info["OS release"] = "not supported"
            except:
                pass

        if os_major is not None and os_minor is not None:
            os_info["OS version"] = f"{os_major}.{os_minor}"
        else:
            os_info["OS version"] = "not supported"

        if not any(os_info.values()):
            return Result(None, "Could not enumerate information via unauthenticated SMB")
        return Result(os_info, "Found OS information via SMB")

    def os_info_to_human(self, os_info):
        native_lanman = os_info["Native LAN manager"]
        native_os = os_info["Native OS"]
        version = os_info["OS version"]
        server_type_string = os_info["Server type string"]
        os = "unknown"

        if native_lanman is not None and "Samba" in native_lanman:
            os = f"Linux/Unix ({native_lanman})"
        elif native_os is not None and "Windows" in native_os and not "Windows 5.0" in native_os:
            os = native_os
        elif server_type_string is not None and "Samba" in server_type_string:
            
            
            
            match = re.search(r".*(Samba\s.*[^)])", server_type_string)
            if match:
                os = f"Linux/Unix ({match.group(1)})"
            else:
                os = "Linux/Unix"
        elif version in OS_VERSIONS:
            os = OS_VERSIONS[version]

        os_info["OS"] = os

        return os_info




class EnumUsersRpc():
    def __init__(self, target, creds, detailed):
        self.target = target
        self.creds = creds
        self.detailed = detailed

    def run(self):
        '''
        Run module enum users.
        '''
        module_name = ENUM_USERS_RPC
        print_heading(f"Users via RPC on {self.target.host}")
        output = {}

        
        print_info("Enumerating users via 'querydispinfo'")
        users_qdi = self.enum_from_querydispinfo()
        if users_qdi.retval is None:
            output = process_error(users_qdi.retmsg, ["users"], module_name, output)
            users_qdi_output = None
        else:
            print_success(users_qdi.retmsg)
            users_qdi_output = users_qdi.retval

        
        print_info("Enumerating users via 'enumdomusers'")
        users_edu = self.enum_from_enumdomusers()
        if users_edu.retval is None:
            output = process_error(users_edu.retmsg, ["users"], module_name, output)
            users_edu_output = None
        else:
            print_success(users_edu.retmsg)
            users_edu_output = users_edu.retval

        
        if users_qdi_output is not None and users_edu_output is not None:
            users = {**users_edu_output, **users_qdi_output}
        elif users_edu_output is None:
            users = users_qdi_output
        else:
            users = users_edu_output

        if users:
            if self.detailed:
                print_info("Enumerating users details")
                for rid in users.keys():
                    name = users[rid]['username']
                    user_details = self.get_details_from_rid(rid, name)
                    if user_details.retval:
                        print_success(user_details.retmsg)
                        users[rid]["details"] = user_details.retval
                    else:
                        output = process_error(user_details.retmsg, ["users"], module_name, output)
                        users[rid]["details"] = ""

            print_success(f"After merging user results we have {len(users.keys())} user(s) total:\n{yamlize(users, sort=True)}")

        output["users"] = users
        return output

    def querydispinfo(self):
        '''
        querydispinfo uses the Security Account Manager Remote Protocol (SAMR) named pipe to run the QueryDisplayInfo() request.
        This request will return users with their corresponding Relative ID (RID) as well as multiple account information like a
        description of the account.
        '''

        result = SambaRpcclient(['querydispinfo'], self.target, self.creds).run(log='Attempting to get userlist')

        if not result.retval:
            return Result(None, f"Could not find users via 'querydispinfo': {result.retmsg}")

        return Result(result.retmsg, "")

    def enumdomusers(self):
        '''
        enomdomusers command will again use the SAMR named pipe to run the EnumDomainUsers() request. This will again
        return a list of users with their corresponding RID (see querydispinfo()). This is possible since by default
        the registry key HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\Lsa\\RestrictAnonymous = 0. If this is set to
        1 enumeration is no longer possible.
        '''

        result = SambaRpcclient(['enumdomusers'], self.target, self.creds).run(log='Attempting to get userlist')

        if not result.retval:
            return Result(None, f"Could not find users via 'enumdomusers': {result.retmsg}")

        return Result(result.retmsg, "")

    def enum_from_querydispinfo(self):
        '''
        Takes the result of rpclient's querydispinfo and tries to extract the users from it.
        '''
        users = {}
        querydispinfo = self.querydispinfo()

        if querydispinfo.retval is None:
            return querydispinfo

        
        
        for line in filter(None, querydispinfo.retval.split('\n')):
            match = re.search(r"index:\s+.*\s+RID:\s+(0x[A-F-a-f0-9]+)\s+acb:\s+(.*)\s+Account:\s+(.*)\s+Name:\s+(.*)\s+Desc:\s+(.*)", line)
            if match:
                rid = match.group(1)
                rid = str(int(rid, 16))
                acb = match.group(2)
                username = match.group(3)
                name = match.group(4)
                description = match.group(5)
                users[rid] = OrderedDict({"username":username, "name":name, "acb":acb, "description":description})
            else:
                return Result(None, "Could not extract users from querydispinfo output, please open a GitHub issue")
        return Result(users, f"Found {len(users.keys())} user(s) via 'querydispinfo'")

    def enum_from_enumdomusers(self):
        '''
        Takes the result of rpclient's enumdomusers and tries to extract the users from it.
        '''
        users = {}
        enumdomusers = self.enumdomusers()

        if enumdomusers.retval is None:
            return enumdomusers

        
        
        for line in enumdomusers.retval.splitlines():
            match = re.search(r"user:\[(.*)\]\srid:\[(0x[A-F-a-f0-9]+)\]", line)
            if match:
                username = match.group(1)
                rid = match.group(2)
                rid = str(int(rid, 16))
                users[rid] = {"username":username}
            else:
                return Result(None, "Could not extract users from eumdomusers output, please open a GitHub issue")
        return Result(users, f"Found {len(users.keys())} user(s) via 'enumdomusers'")

    def get_details_from_rid(self, rid, name):
        '''
        Takes an RID and makes use of the SAMR named pipe to call QueryUserInfo() on the given RID.
        The output contains lots of information about the corresponding user account.
        '''
        if not valid_rid(rid):
            return Result(None, f"Invalid rid passed: {rid}")

        details = OrderedDict()

        result = SambaRpcclient(['queryuser', f'{rid}'], self.target, self.creds).run(log='Attempting to get detailed user info')

        if not result.retval:
            return Result(None, f"Could not find details for user '{name}': {result.retmsg}")

        
        if "NT_STATUS_NO_SUCH_USER" in result.retmsg:
            return Result(None, f"Could not find details for user '{name}': STATUS_NO_SUCH_USER")

        match = re.search("([^\n]*User Name.*logon_hrs[^\n]*)", result.retmsg, re.DOTALL)
        if match:
            user_info = match.group(1)

            for line in filter(None, user_info.split('\n')):
                if re.match(r'^\t[A-Za-z][A-Za-z\s_\.0-9]*(:|\[[0-9\.]+\]\.\.\.)(\t|\s)?', line):
                    if ":" in line:
                        key, value = line.split(":", 1)
                    if "..." in line:
                        key, value = line.split("...", 1)

                    
                    if "User Name" in key or "Full Name" in key:
                        continue

                    key = key.strip()
                    value = value.strip()
                    details[key] = value
                else:
                    
                    
                    
                    try:
                        if key not in details:
                            details[key] = line
                        else:
                            details[key] += "\n" + line
                    except:
                        return Result(None, f"Could not parse result of 'rpcclient' command, please open a GitHub issue")

            if "acb_info" in details and valid_hex(details["acb_info"]):
                for key in ACB_DICT:
                    if int(details["acb_info"], 16) & key:
                        details[ACB_DICT[key]] = True
                    else:
                        details[ACB_DICT[key]] = False

            return Result(details, f"Found details for user '{name}' (RID {rid})")
        return Result(None, f"Could not find details for user '{name}' (RID {rid})")



class EnumGroupsRpc():
    def __init__(self, target, creds, with_members, detailed):
        self.target = target
        self.creds = creds
        self.with_members = with_members
        self.detailed = detailed

    def run(self):
        '''
        Run module enum groups.
        '''
        module_name = ENUM_GROUPS_RPC
        print_heading(f"Groups via RPC on {self.target.host}")
        output = {}
        groups = None

        for grouptype in ["local", "builtin", "domain"]:
            print_info(f"Enumerating {grouptype} groups")
            enum = self.enum(grouptype)
            if enum.retval is None:
                output = process_error(enum.retmsg, ["groups"], module_name, output)
            else:
                if groups is None:
                    groups = {}
                print_success(enum.retmsg)
                groups.update(enum.retval)

        
        if groups:
            if self.with_members:
                print_info("Enumerating group members")
                for rid in groups.keys():
                    
                    groupname = groups[rid]['groupname']
                    grouptype = groups[rid]['type']
                    group_members = self.get_members_from_name(groupname, grouptype, rid)
                    if group_members.retval or group_members.retval == '':
                        print_success(group_members.retmsg)
                    else:
                        output = process_error(group_members.retmsg, ["groups"], module_name, output)
                    groups[rid]["members"] = group_members.retval

            if self.detailed:
                print_info("Enumerating group details")
                for rid in groups.keys():
                    groupname = groups[rid]["groupname"]
                    grouptype = groups[rid]["type"]
                    details = self.get_details_from_rid(rid, groupname, grouptype)

                    if details.retval:
                        print_success(details.retmsg)
                    else:
                        output = process_error(details.retmsg, ["groups"], module_name, output)
                    groups[rid]["details"] = details.retval

            print_success(f"After merging groups results we have {len(groups.keys())} group(s) total:\n{yamlize(groups, sort=True)}")
        output["groups"] = groups
        return output

    def enum(self, grouptype):
        '''
        Tries to enumerate all groups by calling rpcclient's 'enumalsgroups builtin', 'enumalsgroups domain' as well
        as 'enumdomgroups'.
        '''
        grouptype_dict = {
            "builtin":['enumalsgroups', 'builtin'],
            "local":['enumalsgroups', 'domain'],
            "domain":['enumdomgroups']
        }

        if grouptype not in ["builtin", "domain", "local"]:
            return Result(None, f"Unsupported grouptype, supported types are: { ','.join(grouptype_dict.keys()) }")

        groups = {}
        enum = self.enum_by_grouptype(grouptype)

        if enum.retval is None:
            return enum

        if not enum.retval:
            return Result({}, f"Found 0 group(s) via '{' '.join(grouptype_dict[grouptype])}'")

        match = re.search("(group:.*)", enum.retval, re.DOTALL)
        if not match:
            return Result(None, f"Could not parse result of '{' '.join(grouptype_dict[grouptype])}' command, please open a GitHub issue")

        
        
        for line in enum.retval.splitlines():
            match = re.search(r"group:\[(.*)\]\srid:\[(0x[A-F-a-f0-9]+)\]", line)
            if match:
                groupname = match.group(1)
                rid = match.group(2)
                rid = str(int(rid, 16))
                groups[rid] = OrderedDict({"groupname":groupname, "type":grouptype})
            else:
                return Result(None, f"Could not extract groups from '{' '.join(grouptype_dict[grouptype])}' output, please open a GitHub issue")
        return Result(groups, f"Found {len(groups.keys())} group(s) via '{' '.join(grouptype_dict[grouptype])}'")

    def enum_by_grouptype(self, grouptype):
        '''
        Tries to fetch groups via rpcclient's enumalsgroups (so called alias groups) and enumdomgroups.
        Grouptype "builtin", "local" and "domain" are supported.
        '''
        grouptype_dict = {
            "builtin":"enumalsgroups builtin",
            "local":"enumalsgroups domain",
            "domain": "enumdomgroups"
        }

        if grouptype not in ["builtin", "domain", "local"]:
            return Result(None, f"Unsupported grouptype, supported types are: { ','.join(grouptype_dict.keys()) }")

        result = SambaRpcclient([grouptype_dict[grouptype]], self.target, self.creds).run(log=f'Attempting to get {grouptype} groups')

        if not result.retval:
            return Result(None, f"Could not get groups via '{grouptype_dict[grouptype]}': {result.retmsg}")

        return Result(result.retmsg, "")

    def get_members_from_name(self, groupname, grouptype, rid):
        '''
        Takes a group name as first argument and tries to enumerate the group members. This is don by using
        the 'net rpc group members' command.
        '''

        result = SambaNet(['rpc', 'group', 'members', groupname], self.target, self.creds).run(log=f"Attempting to get group memberships for {grouptype} group '{groupname}'")

        if not result.retval:
            return Result(None, f"Could not lookup members for {grouptype} group '{groupname}' (RID {rid}): {result.retmsg}")

        members_string = result.retmsg
        members = []
        for member in members_string.splitlines():
            if "Couldn't lookup SIDs" in member:
                return Result(None, f"Could not lookup members for {grouptype} group '{groupname}' (RID {rid}): insufficient user permissions, try a different user")
            if "Couldn't find group" in member:
                return Result(None, f"Could not lookup members for {grouptype} group '{groupname}' (RID {rid}): group not found")
            members.append(member)

        return Result(','.join(members), f"Found {len(members)} member(s) for {grouptype} group '{groupname}' (RID {rid})")

    def get_details_from_rid(self, rid, groupname, grouptype):
        '''
        Takes an RID and makes use of the SAMR named pipe to open the group with OpenGroup() on the given RID.
        '''
        if not valid_rid(rid):
            return Result(None, f"Invalid rid passed: {rid}")

        details = OrderedDict()

        result = SambaRpcclient(['querygroup', f'{rid}'], self.target, self.creds).run(log='Attempting to get detailed group info')

        if not result.retval:
            return Result(None, f"Could not find details for {grouptype} group '{groupname}': {result.retmsg}")

        
        if "NT_STATUS_NO_SUCH_GROUP" in result.retmsg:
            return Result(None, f"Could not get details for {grouptype} group '{groupname}' (RID {rid}): STATUS_NO_SUCH_GROUP")

        match = re.search("([^\n]*Group Name.*Num Members[^\n]*)", result.retmsg, re.DOTALL)
        if match:
            group_info = match.group(1)
            group_info = group_info.replace("\t", "")

            for line in filter(None, group_info.split('\n')):
                if ':' in line:
                    (key, value) = line.split(":", 1)
                    
                    if "Group Name" in key:
                        continue
                    details[key] = value
                else:
                    details[line] = ""

            return Result(details, f"Found details for {grouptype} group '{groupname}' (RID {rid})")
        return Result(None, f"Could not find details for {grouptype} group '{groupname}' (RID {rid})")



class RidCycleParams:
    '''
    Stores the various parameters needed for RID cycling. rid_ranges and known_usernames are mandatory.
    enumerated_input is a dictionary which contains already enumerated input like "users,
    "groups", "machines" and/or a domain sid. By default enumerated_input is an empty dict
    and will be filled up during the tool run.
    '''
    def __init__(self, rid_ranges, batch_size, known_usernames):
        self.rid_ranges = rid_ranges
        self.batch_size = batch_size
        self.known_usernames = known_usernames
        self.enumerated_input = {}

    def set_enumerated_input(self, enum_input):
        for key in ["users", "groups", "machines"]:
            if key in enum_input:
                self.enumerated_input[key] = enum_input[key]
            else:
                self.enumerated_input[key] = None

        if "domain_sid" in enum_input and enum_input["domain_sid"] and "NULL SID" not in enum_input["domain_sid"]:
            self.enumerated_input["domain_sid"] = enum_input["domain_sid"]
        else:
            self.enumerated_input["domain_sid"] = None

class RidCycling():
    def __init__(self, cycle_params, target, creds, detailed):
        self.cycle_params = cycle_params
        self.target = target
        self.creds = creds
        self.detailed = detailed

    def run(self):
        '''
        Run module RID cycling.
        '''
        module_name = RID_CYCLING
        print_heading(f"Users, Groups and Machines on {self.target.host} via RID Cycling")
        output = self.cycle_params.enumerated_input

        
        if output["domain_sid"]:
            sids_list = [output["domain_sid"]]
        else:
            print_info("Trying to enumerate SIDs")
            sids = self.enum_sids(self.cycle_params.known_usernames)
            if sids.retval is None:
                output = process_error(sids.retmsg, ["users", "groups", "machines"], module_name, output)
                return output
            print_success(sids.retmsg)
            sids_list = sids.retval

        
        found_count = {"users": 0, "groups": 0, "machines": 0}

        
        for sid in sids_list:
            print_info(f"Trying SID {sid}")
            rid_cycler = self.rid_cycle(sid)
            for result in rid_cycler:
                
                top_level_key = list(result.retval.keys())[0]

                
                if top_level_key == 'domain_sid':
                    output['domain_sid'] = result.retval['domain_sid']
                    continue

                "users", "groups" or "machines".
                
                rid = list(result.retval[top_level_key])[0]
                entry = result.retval[top_level_key][rid]

                
                if output[top_level_key] is not None and rid in output[top_level_key]:
                    continue

                print_success(result.retmsg)
                found_count[top_level_key] += 1

                
                if output[top_level_key] is None:
                    output[top_level_key] = {}
                output[top_level_key][rid] = entry

                if self.detailed and ("users" in top_level_key or "groups" in top_level_key):
                    if "users" in top_level_key:
                        rid, entry = list(result.retval["users"].items())[0]
                        name = entry["username"]
                        details = EnumUsersRpc(self.target, self.creds, False).get_details_from_rid(rid, name)
                    elif "groups" in top_level_key:
                        rid, entry = list(result.retval["groups"].items())[0]
                        groupname = entry["groupname"]
                        grouptype = entry["type"]
                        details = EnumGroupsRpc(self.target, self.creds, False, False).get_details_from_rid(rid, groupname, grouptype)

                    if details.retval:
                        print_success(details.retmsg)
                    else:
                        output = process_error(details.retmsg, [top_level_key], module_name, output)
                    output[top_level_key][rid]["details"] = details.retval

        if found_count["users"] == 0 and found_count["groups"] == 0 and found_count["machines"] == 0:
            output = process_error("Could not find any (new) users, (new) groups or (new) machines", ["users", "groups", "machines"], module_name, output)
        else:
            print_success(f"Found {found_count['users']} user(s), {found_count['groups']} group(s), {found_count['machines']} machine(s) in total")

        return output

    def enum_sids(self, users):
        '''
        Tries to enumerate SIDs by looking up user names via rpcclient's lookupnames and by using rpcclient's lsaneumsid.
        '''
        sids = []
        sid_patterns_list = [r"(S-1-5-21-[\d-]+)-\d+", r"(S-1-5-[\d-]+)-\d+", r"(S-1-22-[\d-]+)-\d+"]

        
        for known_username in users.split(','):
            result = SambaRpcclient(['lookupnames', f'{known_username}'], self.target, self.creds).run(log=f'Attempting to get SID for user {known_username}', error_filter=False)
            sid_string = result.retmsg

            
            if "NT_STATUS_ACCESS_DENIED" in sid_string or "NT_STATUS_NONE_MAPPED" in sid_string:
                continue

            for pattern in sid_patterns_list:
                match = re.search(pattern, sid_string)
                if match:
                    result = match.group(1)
                    if result not in sids:
                        sids.append(result)

        
        result = SambaRpcclient(['lsaenumsid'], self.target, self.creds).run(log="Attempting to get SIDs via 'lsaenumsid'", error_filter=False)

        
        if "NT_STATUS_ACCESS_DENIED" not in result.retmsg:
            for pattern in sid_patterns_list:
                match_list = re.findall(pattern, result.retmsg)
                for match in match_list:
                    if match not in sids:
                        sids.append(match)

        if sids:
            return Result(sids, f"Found {len(sids)} SID(s)")
        return Result(None, "Could not get any SIDs")

    def rid_cycle(self, sid):
        '''
        Takes a SID as first parameter well as list of RID ranges (as tuples) as second parameter and does RID cycling.
        '''
        for rid_range in self.cycle_params.rid_ranges:
            (start_rid, end_rid) = rid_range

            for rid_base in range(start_rid, end_rid+1, self.cycle_params.batch_size):
                target_sids = " ".join(list(map(lambda x: f'{sid}-{x}', range(rid_base, min(end_rid+1, rid_base+self.cycle_params.batch_size)))))
                
                result = SambaRpcclient(['lookupsids', target_sids], self.target, self.creds).run(log='RID Cycling', error_filter=False)

                for rid_offset, line in enumerate(result.retmsg.splitlines()):
                    
                    match = re.search(r"(S-\d+-\d+-\d+-[\d-]+\s+(.*)\s+[^\)]+\))", line)
                    if match:
                        sid_and_user = match.group(1)
                        entry = match.group(2)
                        rid = rid_base + rid_offset

                        
                        
                        if re.search(r"-(\d+) .*\\\1 \(", sid_and_user):
                            continue

                        "(1)" = User, "(2)" = Domain Group,"(3)" = Domain SID,"(4)" = Local Group
                        "(5)" = Well-known group, "(6)" = Deleted account, "(7)" = Invalid account
                        "(8)" = Unknown, "(9)" = Machine/Computer account
                        if "(1)" in sid_and_user:
                            yield Result({"users":{str(rid):{"username":entry}}}, f"Found user '{entry}' (RID {rid})")
                        elif "(2)" in sid_and_user:
                            yield Result({"groups":{str(rid):{"groupname":entry, "type":"domain"}}}, f"Found domain group '{entry}' (RID {rid})")
                        elif "(3)" in sid_and_user:
                            yield Result({"domain_sid":f"{sid}-{rid}"}, f"Found domain SID {sid}-{rid}")
                        elif "(4)" in sid_and_user:
                            yield Result({"groups":{str(rid):{"groupname":entry, "type":"builtin"}}}, f"Found builtin group '{entry}' (RID {rid})")
                        elif "(9)" in sid_and_user:
                            yield Result({"machines":{str(rid):{"machine":entry}}}, f"Found machine '{entry}' (RID {rid})")



class EnumShares():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module enum shares.
        '''
        module_name = ENUM_SHARES
        print_heading(f"Shares via RPC on {self.target.host}")
        output = {}
        shares = None

        enum = self.enum()
        if enum.retval is None:
            output = process_error(enum.retmsg, ["shares"], module_name, output)
        else:
            print_info("Enumerating shares")
            
            print_success(enum.retmsg)
            shares = enum.retval
            
            if enum.retmsg:
                for share in sorted(shares):
                    print_info(f"Testing share {share}")
                    access = self.check_access(share)
                    if access.retval is None:
                        output = process_error(access.retmsg, ["shares"], module_name, output)
                        continue
                    print_success(access.retmsg)
                    shares[share]['access'] = access.retval

        output["shares"] = shares
        return output

    def enum(self):
        '''
        Tries to enumerate shares with the given username and password. It does this running the smbclient command.
        smbclient will open a connection to the Server Service Remote Protocol named pipe (srvsvc). Once connected
        it calls the NetShareEnumAll() to get a list of shares.
        '''

        result = SambaSmbclient(['list'], self.target, self.creds).run(log='Attempting to get share list using authentication')

        if not result.retval:
            return Result(None, f"Could not list shares: {result.retmsg}")

        shares = {}
        match_list = re.findall(r"^(Device|Disk|IPC|Printer)\|(.*)\|(.*)$", result.retmsg, re.MULTILINE|re.IGNORECASE)
        if match_list:
            for entry in match_list:
                share_type = entry[0]
                share_name = entry[1]
                share_comment = entry[2].rstrip()
                shares[share_name] = {'type':share_type, 'comment':share_comment}

        if shares:
            return Result(shares, f"Found {len(shares.keys())} share(s):\n{yamlize(shares, sort=True)}")
        return Result(shares, f"Found 0 share(s) for user '{self.creds.user}' with password '{self.creds.pw}', try a different user")

    def check_access(self, share):
        '''
        Takes a share as first argument and checks whether the share is accessible.
        The function returns a dictionary with the keys "mapping" and "listing".
        "mapping" can be either OK or DENIED. OK means the share exists and is accessible.
        "listing" can bei either OK, DENIED, N/A, NOT SUPPORTED or WRONG PASSWORD.
        N/A means directory listing is not allowed, while NOT SUPPORTED means the share does
        not support listing at all. This is the case for shares like IPC$ which is used for
        remote procedure calls.

        In order to enumerate access permissions, smbclient is used with the "dir" command.
        In the background this will send an SMB I/O Control (IOCTL) request in order to list the contents of the share.
        '''

        result = SambaSmbclient(['dir', f'{share}'], self.target, self.creds).run(log=f'Attempting to map share //{self.target.host}/{share}', error_filter=False)

        if "NT_STATUS_BAD_NETWORK_NAME" in result.retmsg:
            return Result(None, "Share doesn't exist")

        if "NT_STATUS_ACCESS_DENIED listing" in result.retmsg:
            return Result({"mapping":"ok", "listing":"denied"}, "Mapping: OK, Listing: DENIED")

        if "NT_STATUS_WRONG_PASSWORD" in result.retmsg:
            return Result({"mapping":"ok", "listing":"wrong password"}, "Mapping: OK, Listing: WRONG PASSWORD")

        if "tree connect failed: NT_STATUS_ACCESS_DENIED" in result.retmsg:
            return Result({"mapping":"denied", "listing":"n/a"}, "Mapping: DENIED, Listing: N/A")

        if "NT_STATUS_INVALID_INFO_CLASS" in result.retmsg\
                or "NT_STATUS_NETWORK_ACCESS_DENIED" in result.retmsg\
                or "NT_STATUS_NOT_A_DIRECTORY" in result.retmsg\
                or "NT_STATUS_NO_SUCH_FILE" in result.retmsg:
            return Result({"mapping":"ok", "listing":"not supported"}, "Mapping: OK, Listing: NOT SUPPORTED")

        if "NT_STATUS_OBJECT_NAME_NOT_FOUND" in result.retmsg:
            return Result(None, "Could not check share: STATUS_OBJECT_NAME_NOT_FOUND")

        if "NT_STATUS_INVALID_PARAMETER" in result.retmsg:
            return Result(None, "Could not check share: STATUS_INVALID_PARAMETER")

        if re.search(r"\n\s+\.\.\s+D.*\d{4}\n", result.retmsg) or re.search(r".*blocks\sof\ssize.*blocks\savailable.*", result.retmsg):
            return Result({"mapping":"ok", "listing":"ok"}, "Mapping: OK, Listing: OK")

        return Result(None, "Could not parse result of smbclient command, please open a GitHub issue")



class ShareBruteParams:
    '''
    Stores the various parameters needed for Share Bruteforcing. shares_file is mandatory.
    enumerated_input is a dictionary which contains already enumerated shares. By default
    enumerated_input is an empty dict and will be filled up during the tool run.
    '''
    def __init__(self, shares_file):
        self.shares_file = shares_file
        self.enumerated_input = {}

    def set_enumerated_input(self, enum_input):
        if "shares" in enum_input:
            self.enumerated_input["shares"] = enum_input["shares"]
        else:
            self.enumerated_input["shares"] = None

class BruteForceShares():
    def __init__(self, brute_params, target, creds):
        self.brute_params = brute_params
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module bruteforce shares.
        '''
        module_name = BRUTE_FORCE_SHARES
        print_heading(f"Share Bruteforcing on {self.target.host}")
        output = self.brute_params.enumerated_input

        found_count = 0
        try:
            with open(self.brute_params.shares_file) as f:
                for share in f:
                    share = share.rstrip()

                    
                    if output["shares"] is not None and share in output["shares"].keys():
                        continue

                    result = EnumShares(self.target, self.creds).check_access(share)
                    if result.retval:
                        if output["shares"] is None:
                            output["shares"] = {}
                        print_success(f"Found share: {share}")
                        print_success(result.retmsg)
                        output["shares"][share] = result.retval
                        found_count += 1
        except:
            output = process_error(f"Failed to open {self.brute_params.shares_file}", ["shares"], module_name, output)

        if found_count == 0:
            output = process_error("Could not find any (new) shares", ["shares"], module_name, output)
        else:
            print_success(f"Found {found_count} (new) share(s) in total")

        return output



class EnumPolicy():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module enum policy.
        '''
        module_name = ENUM_POLICY
        print_heading(f"Policies via RPC for {self.target.host}")
        output = {}

        for port in self.target.smb_ports:
            print_info(f"Trying port {port}/tcp")
            self.target.port = port
            enum = self.enum()
            if enum.retval is None:
                output = process_error(enum.retmsg, ["policy"], module_name, output)
                output["policy"] = None
            else:
                print_success(enum.retmsg)
                output["policy"] = enum.retval
                break

        return output

    
    "deanx" Dean: https://labs.portcullis.co.uk/tools/polenum/
    "deanx" Dean and Craig "Wh1t3Fox" West!
    def enum(self):
        '''
        Tries to enum password policy and domain lockout and logoff information by opening a connection to the SAMR
        named pipe and calling SamQueryInformationDomain() as well as SamQueryInformationDomain2().
        '''
        policy = {}

        result = self.samr_init()
        if result.retval[0] is None or result.retval[1] is None:
            return Result(None, result.retmsg)

        dce, domain_handle = result.retval

        
        try:
            domain_passwd = samr.DOMAIN_INFORMATION_CLASS.DomainPasswordInformation
            result = samr.hSamrQueryInformationDomain2(dce, domainHandle=domain_handle, domainInformationClass=domain_passwd)
            policy["Domain password information"] = {}
            policy["Domain password information"]["Password history length"] = result['Buffer']['Password']['PasswordHistoryLength'] or "None"
            policy["Domain password information"]["Minimum password length"] = result['Buffer']['Password']['MinPasswordLength'] or "None"
            policy["Domain password information"]["Maximum password age"] = self.policy_to_human(int(result['Buffer']['Password']['MinPasswordAge']['LowPart']), int(result['Buffer']['Password']['MinPasswordAge']['HighPart']))
            policy["Domain password information"]["Maximum password age"] = self.policy_to_human(int(result['Buffer']['Password']['MaxPasswordAge']['LowPart']), int(result['Buffer']['Password']['MaxPasswordAge']['HighPart']))
            policy["Domain password information"]["Password properties"] = []
            pw_prop = result['Buffer']['Password']['PasswordProperties']
            for bitmask in DOMAIN_FIELDS:
                if pw_prop & bitmask == bitmask:
                    policy["Domain password information"]["Password properties"].append({DOMAIN_FIELDS[bitmask]:True})
                else:
                    policy["Domain password information"]["Password properties"].append({DOMAIN_FIELDS[bitmask]:False})
        except Exception as e:
            nt_status_error = nt_status_error_filter(str(e))
            if nt_status_error:
                return Result(None, f"Could not get domain password policy: {nt_status_error}")
            return Result(None, "Could not get domain password policy")

        
        try:
            domain_lockout = samr.DOMAIN_INFORMATION_CLASS.DomainLockoutInformation
            result = samr.hSamrQueryInformationDomain2(dce, domainHandle=domain_handle, domainInformationClass=domain_lockout)
            policy["Domain lockout information"] = {}
            policy["Domain lockout information"]["Lockout observation window"] = self.policy_to_human(0, result['Buffer']['Lockout']['LockoutObservationWindow'], lockout=True)
            policy["Domain lockout information"]["Lockout duration"] = self.policy_to_human(0, result['Buffer']['Lockout']['LockoutDuration'], lockout=True)
            policy["Domain lockout information"]["Lockout threshold"] = result['Buffer']['Lockout']['LockoutThreshold'] or "None"
        except Exception as e:
            nt_status_error = nt_status_error_filter(str(e))
            if nt_status_error:
                return Result(None, f"Could not get domain_lockout policy: {nt_status_error}")
            return Result(None, "Could not get domain lockout policy")

        
        try:
            domain_logoff = samr.DOMAIN_INFORMATION_CLASS.DomainLogoffInformation
            result = samr.hSamrQueryInformationDomain2(dce, domainHandle=domain_handle, domainInformationClass=domain_logoff)
            policy["Domain logoff information"] = {}
            policy["Domain logoff information"]["Force logoff time"] = self.policy_to_human(result['Buffer']['Logoff']['ForceLogoff']['LowPart'], result['Buffer']['Logoff']['ForceLogoff']['HighPart'])
        except Exception as e:
            nt_status_error = nt_status_error_filter(str(e))
            if nt_status_error:
                return Result(None, f"Could not get domain_lockout policy: {nt_status_error}")
            return Result(None, "Could not get domain lockout policy")

        return Result(policy, f"Found policy:\n{yamlize(policy)}")

    
    "deanx" Dean: https://labs.portcullis.co.uk/tools/polenum/
    "deanx" Dean and Craig "Wh1t3Fox" West!
    def samr_init(self):
        '''
        Tries to connect to the SAMR named pipe and get the domain handle.
        '''

        
        env = os.environ.copy()
        try:
            smb_conn = smbconnection.SMBConnection(remoteName=self.target.host, remoteHost=self.target.host, sess_port=self.target.port, timeout=self.target.timeout)
            if self.creds.ticket_file:
                os.environ['KRB5CCNAME'] = self.creds.ticket_file
                
                smb_conn.kerberosLogin('', self.creds.pw, domain='', useCache=True)
            elif self.creds.nthash:
                smb_conn.login(self.creds.user, self.creds.pw, domain=self.creds.domain, nthash=self.creds.nthash)
            else:
                smb_conn.login(self.creds.user, self.creds.pw, self.creds.domain)

            rpctransport = transport.SMBTransport(smb_connection=smb_conn, filename=r'\samr', remoteName=self.target.host)
            dce = DCERPC_v5(rpctransport)
            dce.connect()
            dce.bind(samr.MSRPC_UUID_SAMR)
        except Exception as e:
            return Result((None, None), process_impacket_smb_exception(e, self.target))
        finally:
            
            os.environ.clear()
            os.environ.update(env)

        try:
            resp = samr.hSamrConnect2(dce)
        except Exception as e:
            return Result((None, None), process_impacket_smb_exception(e, self.target))

        if resp['ErrorCode'] != 0:
            return Result((None, None), f"SamrConnect2 call failed on port {self.target.port}/tcp")

        resp2 = samr.hSamrEnumerateDomainsInSamServer(dce, serverHandle=resp['ServerHandle'], enumerationContext=0, preferedMaximumLength=500)
        if resp2['ErrorCode'] != 0:
            return Result((None, None), "SamrEnumerateDomainsinSamServer failed")

        resp3 = samr.hSamrLookupDomainInSamServer(dce, serverHandle=resp['ServerHandle'], name=resp2['Buffer']['Buffer'][0]['Name'])
        if resp3['ErrorCode'] != 0:
            return Result((None, None), "SamrLookupDomainInSamServer failed")

        resp4 = samr.hSamrOpenDomain(dce, serverHandle=resp['ServerHandle'], desiredAccess=samr.MAXIMUM_ALLOWED, domainId=resp3['DomainId'])
        if resp4['ErrorCode'] != 0:
            return Result((None, None), "SamrOpenDomain failed")

        
        domain_handle = resp4['DomainHandle']

        return Result((dce, domain_handle), "")

    
    "deanx" Dean: https://labs.portcullis.co.uk/tools/polenum/
    "deanx" Dean and Craig "Wh1t3Fox" West!
    def policy_to_human(self, low, high, lockout=False):
        '''
        Converts various values retrieved via the SAMR named pipe into human readable strings.
        '''
        time = ""
        tmp = 0

        if low == 0 and hex(high) == "-0x80000000":
            return "not set"
        if low == 0 and high == 0:
            return "none"

        if not lockout:
            if low != 0:
                high = abs(high+1)
            else:
                high = abs(high)
                low = abs(low)

            tmp = low + (high)*16**8  
            tmp *= (1e-7)  
        else:
            tmp = abs(high) * (1e-7)

        try:
            minutes = datetime.utcfromtimestamp(tmp).minute
            hours = datetime.utcfromtimestamp(tmp).hour
            time_diff = datetime.utcfromtimestamp(tmp) - datetime.utcfromtimestamp(0)
            days = time_diff.days
        except:
            return "invalid time"

        if days > 1:
            time += f"{days} days "
        elif days == 1:
            time += f"{days} day "
        if hours > 1:
            time += f"{hours} hours "
        elif hours == 1:
            time += f"{hours} hour "
        if minutes > 1:
            time += f"{minutes} minutes"
        elif minutes == 1:
            time += f"{minutes} minute"
        return time



class EnumPrinters():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module enum printers.
        '''
        module_name = ENUM_PRINTERS
        print_heading(f"Printers via RPC for {self.target.host}")
        output = {}

        enum = self.enum()
        if enum.retval is None:
            output = process_error(enum.retmsg, ["printers"], module_name, output)
            output["printers"] = None
        else:
            print_success(enum.retmsg)
            output["printers"] = enum.retval
        return output

    def enum(self):
        '''
        Tries to enum printer via rpcclient's enumprinters.
        '''

        result = SambaRpcclient(['enumprinters'], self.target, self.creds).run(log='Attempting to get printer info')
        printers = {}

        if not result.retval:
            return Result(None, f"Could not get printer info via 'enumprinters': {result.retmsg}")

        
        if "NT_STATUS_OBJECT_NAME_NOT_FOUND" in result.retmsg:
            return Result("", "No printers available")
        if "No printers returned." in result.retmsg:
            return Result({}, "No printers returned (this is not an error)")

        nt_status_error = nt_status_error_filter(result.retmsg)
        if nt_status_error:
            return Result(None, f"Could not get printers via 'enumprinters': {nt_status_error}")
        
        if "WERR_INVALID_NAME" in result.retmsg:
            return Result(None, "Could not get printers via 'enumprinters': WERR_INVALID_NAME")

        match_list = re.findall(r"\s*flags:\[([^\n]*)\]\n\s*name:\[([^\n]*)\]\n\s*description:\[([^\n]*)\]\n\s*comment:\[([^\n]*)\]", result.retmsg, re.MULTILINE)
        if not match_list:
            return Result(None, "Could not parse result of enumprinters command, please open a GitHub issue")

        for match in match_list:
            flags = match[0]
            name = match[1]
            description = match[2]
            comment = match[3]
            printers[name] = OrderedDict({"description":description, "comment":comment, "flags":flags})

        return Result(printers, f"Found {len(printers.keys())} printer(s):\n{yamlize(printers, sort=True)}")



class EnumServices():
    def __init__(self, target, creds):
        self.target = target
        self.creds = creds

    def run(self):
        '''
        Run module enum services.
        '''
        module_name = ENUM_SERVICES
        print_heading(f"Services via RPC on {self.target.host}")
        output = {'services':None}

        enum = self.enum()
        if enum.retval is None:
            output = process_error(enum.retmsg, ["services"], module_name, output)
        else:
            print_success(enum.retmsg)
            output['services'] = enum.retval

        return output

    def enum(self):
        '''
        Tries to enum RPC services via net rpc service list.
        '''

        result = SambaNet(['rpc', 'service', 'list'], self.target, self.creds).run(log='Attempting to get RPC services')
        services = {}

        if not result.retval:
            return Result(None, f"Could not get RPC services via 'net rpc service list': {result.retmsg}")

        match_list = re.findall(r"([^\s]*)\s*\"(.*)\"", result.retmsg, re.MULTILINE)
        if not match_list:
            return Result(None, "Could not parse result of 'net rpc service list' command, please open a GitHub issue")

        for match in match_list:
            name = match[0]
            description = match[1]
            services[name] = OrderedDict({"description":description})

        return Result(services, f"Found {len(services.keys())} service(s):\n{yamlize(services, True)}")



class Enumerator():
    def __init__(self, args):

        
        if args.out_json_file:
            output = Output(args.out_json_file, "json")
        elif args.out_yaml_file:
            output = Output(args.out_yaml_file, "yaml")
        elif args.out_file:
            output = Output(args.out_file, "json_yaml")
        else:
            output = Output()

        
        try:
            self.creds = Credentials(args.user, args.pw, args.domain, args.ticket_file, args.nthash, args.local_auth)
            self.target = Target(args.host, self.creds, timeout=args.timeout)
        except Exception as e:
            raise RuntimeError(str(e))

        
        try:
            samba_config = SambaConfig(['client ipc signing = auto'])
            self.target.samba_config = samba_config
        except:
            raise RuntimeError("Could not create default samba configuration")

        
        output.update(self.target.as_dict())
        output.update(self.creds.as_dict())

        self.args = args
        self.output = output
        self.cycle_params = None
        self.share_brute_params = None

    def run(self):
        
        if self.args.R:
            rid_ranges = self.prepare_rid_ranges()
            self.cycle_params = RidCycleParams(rid_ranges, self.args.R, self.args.users)

        
        if self.args.shares_file:
            self.share_brute_params = ShareBruteParams(self.args.shares_file)

        print_heading("Target Information", False)
        print_info(f"Target ........... {self.target.host}")
        print_info(f"Username ......... '{self.creds.user}'")
        print_info(f"Random Username .. '{self.creds.random_user}'")
        print_info(f"Password ......... '{self.creds.pw}'")
        print_info(f"Timeout .......... {self.target.timeout} second(s)")
        if self.args.R:
            print_info(f"RID Range(s) ..... {self.args.ranges}")
            print_info(f"RID Req Size ..... {self.args.R}")
            print_info(f"Known Usernames .. '{self.args.users}'")

        
        
        
        
        listeners = self.service_scan()
        self.target.listeners = listeners
        modules = self.get_modules(listeners)
        self.run_modules(modules)

    def service_scan(self):
        
        
        
        scan_list = [SERVICE_SMB, SERVICE_SMB_NETBIOS]
        if self.args.L:
            scan_list += [SERVICE_LDAP, SERVICE_LDAPS]

        scanner = ListenersScan(self.target, scan_list)
        result = scanner.run()
        self.output.update(result)
        self.target.smb_ports = scanner.get_accessible_ports_by_pattern("SMB")
        self.target.ldap_ports = scanner.get_accessible_ports_by_pattern("LDAP")
        return scanner.get_accessible_listeners()

    def get_modules(self, listeners, session=True):
        modules = []
        if self.args.N:
            modules.append(ENUM_NETBIOS)

        if SERVICE_LDAP in listeners or SERVICE_LDAPS in listeners:
            if self.args.L:
                modules.append(ENUM_LDAP_DOMAIN_INFO)

        if SERVICE_SMB in listeners or SERVICE_SMB_NETBIOS in listeners:
            modules.append(ENUM_SMB)
            modules.append(ENUM_SMB_DOMAIN_INFO)
            modules.append(ENUM_SESSIONS)

            
            
            if self.args.O:
                modules.append(ENUM_OS_INFO)

            
            if session:
                modules.append(ENUM_LSAQUERY_DOMAIN_INFO)
                if self.args.U:
                    modules.append(ENUM_USERS_RPC)
                if self.args.G:
                    modules.append(ENUM_GROUPS_RPC)
                if self.args.Gm:
                    modules.append(ENUM_GROUPS_RPC)
                if self.args.R:
                    modules.append(RID_CYCLING)
                if self.args.S:
                    modules.append(ENUM_SHARES)
                if self.args.shares_file:
                    modules.append(BRUTE_FORCE_SHARES)
                if self.args.P:
                    modules.append(ENUM_POLICY)
                if self.args.I:
                    modules.append(ENUM_PRINTERS)
                if self.args.C:
                    modules.append(ENUM_SERVICES)

        return modules

    def run_modules(self, modules):
        
        if ENUM_LDAP_DOMAIN_INFO in modules:
            result = EnumLdapDomainInfo(self.target).run()
            self.output.update(result)

        
        if ENUM_NETBIOS in modules:
            result = EnumNetbios(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_SMB in modules:
            result = EnumSmb(self.target, self.args.d).run()
            self.output.update(result)

        
        if ENUM_SMB_DOMAIN_INFO in modules:
            result = EnumSmbDomainInfo(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_SESSIONS in modules:
            result = EnumSessions(self.target, self.creds).run()
            self.output.update(result)
            self.target.sessions = self.output.as_dict()['sessions']

        
        
        if self.target.sessions and not self.target.sessions[self.creds.auth_method]:
            modules = self.get_modules(self.target.listeners, session=False)

        
        if ENUM_LSAQUERY_DOMAIN_INFO in modules:
            result = EnumLsaqueryDomainInfo(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_OS_INFO in modules:
            result = EnumOsInfo(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_USERS_RPC in modules:
            result = EnumUsersRpc(self.target, self.creds, self.args.d).run()
            self.output.update(result)

        
        if ENUM_GROUPS_RPC in modules:
            result = EnumGroupsRpc(self.target, self.creds, self.args.Gm, self.args.d).run()
            self.output.update(result)

        
        if ENUM_SERVICES in modules:
            result = EnumServices(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_SHARES in modules:
            result = EnumShares(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_POLICY in modules:
            result = EnumPolicy(self.target, self.creds).run()
            self.output.update(result)

        
        if ENUM_PRINTERS in modules:
            result = EnumPrinters(self.target, self.creds).run()
            self.output.update(result)

        
        if RID_CYCLING in modules:
            self.cycle_params.set_enumerated_input(self.output.as_dict())
            result = RidCycling(self.cycle_params, self.target, self.creds, self.args.d).run()
            self.output.update(result)

        
        if BRUTE_FORCE_SHARES in modules:
            self.share_brute_params.set_enumerated_input(self.output.as_dict())
            result = BruteForceShares(self.share_brute_params, self.target, self.creds).run()
            self.output.update(result)

        if not self.target.listeners:
            warn("Aborting remainder of tests since neither SMB nor LDAP are accessible")
        elif self.target.sessions['sessions_possible'] and not self.target.sessions[self.creds.auth_method]:
            warn("Aborting remainder of tests, sessions are possible, but not with the provided credentials (see session check results)")
        elif not self.target.sessions['sessions_possible']:
            if SERVICE_SMB not in self.target.listeners and SERVICE_SMB_NETBIOS not in self.target.listeners:
                warn("Aborting remainder of tests since SMB is not accessible")
            else:
                warn("Aborting remainder of tests since sessions failed, rerun with valid credentials")

    def prepare_rid_ranges(self):
        '''
        Takes a string containing muliple RID ranges and returns a list of ranges as tuples.
        '''
        rid_ranges = self.args.ranges
        rid_ranges_list = []

        for rid_range in rid_ranges.split(','):
            if rid_range.isdigit():
                start_rid = rid_range
                end_rid = rid_range
            else:
                [start_rid, end_rid] = rid_range.split("-")

            start_rid = int(start_rid)
            end_rid = int(end_rid)

            
            if start_rid > end_rid:
                start_rid, end_rid = end_rid, start_rid

            rid_ranges_list.append((start_rid, end_rid))

        return rid_ranges_list

    def finish(self):
        errors = []

        
        if hasattr(self, 'target'):
            if self.target.samba_config is not None and not self.args.keep:
                result = self.target.samba_config.delete()
                if not result.retval:
                    errors.append(result.retmsg)

        
        if hasattr(self, 'output'):
            result = self.output.flush()
            if not result.retval:
                errors.append(result.retmsg)

        if errors:
            return Result(False, "\n".join(errors))
        return Result(True, "")



def valid_value(value, bounds):
    min_val, max_val = bounds
    try:
        value = int(value)
        if min_val <= value <= max_val:
            return True
    except ValueError:
        pass
    return False

def valid_rid_ranges(rid_ranges):
    if not rid_ranges:
        return False

    for rid_range in rid_ranges.split(','):
        match = re.search(r"^(\d+)-(\d+)$", rid_range)
        if match:
            continue
        if rid_range.isdigit():
            continue
        return False
    return True

def valid_shares_file(shares_file):
    fault_shares = []
    NL = '\n'

    result = valid_file(shares_file)
    if not result.retval:
        return result

    try:
        with open(shares_file) as f:
            line_num = 1
            for share in f:
                share = share.rstrip()
                if not valid_share(share):
                    fault_shares.append(f"line {line_num}:{share}")
                line_num += 1
    except:
        return Result(False, f"Could not open shares file {shares_file}")
    if fault_shares:
        return Result(False, f"Shares with illegal characters found in {shares_file}:\n{NL.join(fault_shares)}")
    return Result(True, "")

def valid_share(share):
    if re.search(r"^[a-zA-Z0-9\._\$-]+$", share):
        return True
    return False

def valid_hex(hexnumber):
    if re.search("^0x[0-9a-f]+$", hexnumber.lower()):
        return True
    return False

def valid_rid(rid):
    if isinstance(rid, int) and rid > 0:
        return True
    if rid.isdigit():
        return True
    return False

def valid_domain(domain):
    if re.match(r"^[A-Za-z0-9_\.-]+$", domain):
        return True
    return False

def valid_file(file, mode=os.R_OK):
    if not os.path.exists(file):
        return Result(False, f'File {file} does not exist')

    if os.stat(file).st_size == 0:
        return Result(False, f'File {file} is empty')

    if not os.access(file, mode):
        if mode == os.R_OK:
            return Result(False, f'Cannot read file {file}')
        if mode == os.W_OK:
            return Result(False, f'Cannot write file {file}')

    return Result(True, '')



def print_banner():
    print(f"{Colors.green(f'ENUM4LINUX - next generation (v{GLOBAL_VERSION})')}\n")

def print_heading(text, leading_newline=True):
    output = f"|    {text}    |"
    length = len(output)

    if leading_newline:
        print()
    print(" " + "="*(length-2))
    print(output)
    print(" " + "="*(length-2))

def print_success(msg):
    print(Colors.green(f"[+] {msg}"))

def print_hint(msg):
    print(Colors.green(f"[H] {msg}"))

def print_error(msg):
    print(Colors.red(f"[-] {msg}"))

def print_info(msg):
    print(Colors.blue(f"[*] {msg}"))

def print_verbose(msg):
    print(f"[V] {msg}")

def process_error(msg, affected_entries, module_name, output_dict):
    '''
    Helper function to print error and update output dictionary at the same time.
    '''
    print_error(msg)

    if not "errors" in output_dict:
        output_dict["errors"] = {}

    for entry in affected_entries:
        if not entry in output_dict["errors"]:
            output_dict["errors"].update({entry: {}})

        if not module_name in output_dict["errors"][entry]:
            output_dict["errors"][entry].update({module_name: []})

        output_dict["errors"][entry][module_name].append(msg)
    return output_dict

def process_impacket_smb_exception(exception, target):
    '''
    Function for handling exceptions during SMB session setup when using the impacket library.
    '''
    if len(exception.args) == 2:
        if isinstance(exception.args[1], ConnectionRefusedError):
            return f"SMB connection error on port {target.port}/tcp: Connection refused"
        if isinstance(exception.args[1], socket.timeout):
            return f"SMB connection error on port {target.port}/tcp: timed out"
    if isinstance(exception, nmb.NetBIOSError):
        return f"SMB connection error on port {target.port}/tcp: session failed"
    if isinstance(exception, (smb.SessionError, smb3.SessionError)):
        nt_status_error = nt_status_error_filter(str(exception))
        if nt_status_error:
            return f"SMB connection error on port {target.port}/tcp: {nt_status_error}"
        return f"SMB connection error on port {target.port}/tcp: session failed"
    if isinstance(exception, AttributeError):
        return f"SMB connection error on port {target.port}/tcp: session failed"
    nt_status_error = nt_status_error_filter(str(exception))
    if nt_status_error:
        return f"SMB connection error on port {target.port}/tcp: {nt_status_error}"
    return f"SMB connection error on port {target.port}/tcp: session failed"

def nt_status_error_filter(msg):
    for error in NT_STATUS_COMMON_ERRORS:
        if error.lower() in msg.lower():
            return error
    return ""

def abort(msg):
    '''
    This function is used to abort the tool run on error.
    The given error message will be printed out and the tool will abort with exit code 1.
    '''
    print(Colors.red(f"[!] {msg}"))
    sys.exit(1)

def warn(msg):
    print("\n"+Colors.yellow(f"[!] {msg}"))

def yamlize(msg, sort=False, rstrip=True):
    try:
        result = yaml.dump(msg, default_flow_style=False, sort_keys=sort, width=160, Dumper=Dumper)
    except TypeError:
        
        result = yaml.dump(msg, default_flow_style=False, width=160, Dumper=Dumper)

    if rstrip:
        return result.rstrip()
    return result



def check_arguments():
    '''
    Takes all arguments from argv and processes them via ArgumentParser. In addition, some basic
    validation of arguments is done.
    '''

    global GLOBAL_VERBOSE
    global GLOBAL_SAMBA_LEGACY

    parser = ArgumentParser(description="""This tool is a rewrite of Mark Lowe's enum4linux.pl, a tool for enumerating information from Windows and Samba systems.
            It is mainly a wrapper around the Samba tools nmblookup, net, rpcclient and smbclient. Other than the original tool it allows to export enumeration results
            as YAML or JSON file, so that it can be further processed with other tools.

            The tool tries to do a 'smart' enumeration. It first checks whether SMB or LDAP is accessible on the target. Depending on the result of this check, it will
            dynamically skip checks (e.g. LDAP checks if LDAP is not running). If SMB is accessible, it will always check whether a session can be set up or not. If no
            session can be set up, the tool will stop enumeration.

            The enumeration process can be interupted with CTRL+C. If the options -oJ or -oY are provided, the tool will write out the current enumeration state to the
            JSON or YAML file, once it receives SIGINT triggered by CTRL+C.

            The tool was made for security professionals and CTF players. Illegal use is prohibited.""")
    parser.add_argument("host")
    parser.add_argument("-A", action="store_true", help="Do all simple enumeration including nmblookup (-U -G -S -P -O -N -I -L). This option is enabled if you don't provide any other option.")
    parser.add_argument("-As", action="store_true", help="Do all simple short enumeration without NetBIOS names lookup (-U -G -S -P -O -I -L)")
    parser.add_argument("-U", action="store_true", help="Get users via RPC")
    parser.add_argument("-G", action="store_true", help="Get groups via RPC")
    parser.add_argument("-Gm", action="store_true", help="Get groups with group members via RPC")
    parser.add_argument("-S", action="store_true", help="Get shares via RPC")
    parser.add_argument("-C", action="store_true", help="Get services via RPC")
    parser.add_argument("-P", action="store_true", help="Get password policy information via RPC")
    parser.add_argument("-O", action="store_true", help="Get OS information via RPC")
    parser.add_argument("-L", action="store_true", help="Get additional domain info via LDAP/LDAPS (for DCs only)")
    parser.add_argument("-I", action="store_true", help="Get printer information via RPC")
    parser.add_argument("-R", default=0, const=1, nargs='?', metavar="BULK_SIZE", type=int, help="Enumerate users via RID cycling. Optionally, specifies lookup request size.")
    parser.add_argument("-N", action="store_true", help="Do an NetBIOS names lookup (similar to nbtstat) and try to retrieve workgroup from output")
    parser.add_argument("-w", dest="domain", default='', type=str, help="Specify workgroup/domain manually (usually found automatically)")
    parser.add_argument("-u", dest="user", default='', type=str, help="Specify username to use (default \"\")")
    auth_methods = parser.add_mutually_exclusive_group()
    auth_methods.add_argument("-p", dest="pw", default='', type=str, help="Specify password to use (default \"\")")
    auth_methods.add_argument("-K", dest="ticket_file", default='', type=str, help="Try to authenticate with Kerberos, only useful in Active Directory environment")
    auth_methods.add_argument("-H", dest="nthash", default='', type=str, help="Try to authenticate with hash")
    parser.add_argument("--local-auth", action="store_true", default=False, help="Authenticate locally to target")
    parser.add_argument("-d", action="store_true", help="Get detailed information for users and groups, applies to -U, -G and -R")
    parser.add_argument("-k", dest="users", default=KNOWN_USERNAMES, type=str, help=f'User(s) that exists on remote system (default: {KNOWN_USERNAMES}).\nUsed to get sid with "lookupsids"')
    parser.add_argument("-r", dest="ranges", default=RID_RANGES, type=str, help=f"RID ranges to enumerate (default: {RID_RANGES})")
    parser.add_argument("-s", dest="shares_file", help="Brute force guessing for shares")
    parser.add_argument("-t", dest="timeout", default=TIMEOUT, help=f"Sets connection timeout in seconds (default: {TIMEOUT}s)")
    parser.add_argument("-v", dest="verbose", action="store_true", help="Verbose, show full samba tools commands being run (net, rpcclient, etc.)")
    parser.add_argument("--keep", action="store_true", help="Don't delete the Samba configuration file created during tool run after enumeration (useful with -v)")
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument("-oJ", dest="out_json_file", help="Writes output to JSON file (extension is added automatically)")
    out_group.add_argument("-oY", dest="out_yaml_file", help="Writes output to YAML file (extension is added automatically)")
    out_group.add_argument("-oA", dest="out_file", help="Writes output to YAML and JSON file (extensions are added automatically)")
    args = parser.parse_args()

    if not (args.A or args.As or args.U or args.G or args.Gm or args.S or args.C or args.P or args.O or args.L or args.I or args.R or args.N or args.shares_file):
        args.A = True

    if args.A or args.As:
        args.G = True
        args.I = True
        args.L = True
        args.O = True
        args.P = True
        args.S = True
        args.U = True

    if args.A:
        args.N = True

    
    GLOBAL_VERBOSE = args.verbose

    
    
    if not args.local_auth and args.domain:
        if not valid_domain(args.domain):
            raise RuntimeError(f"Workgroup/domain '{args.domain}' contains illegal character")

    
    if args.R:
        if not valid_value(args.R, (1,2000)):
            raise RuntimeError("The given RID bulk size must be a valid integer in the range 1-2000")
        if not valid_rid_ranges(args.ranges):
            raise RuntimeError("The given RID ranges should be a range '10-20' or just a single RID like '1199'")

    
    if args.shares_file:
        result = valid_shares_file(args.shares_file)
        if not result.retval:
            raise RuntimeError(result.retmsg)

    
    if args.user and args.user not in args.users.split(","):
        args.users += f",{args.user}"

    
    if not valid_value(args.timeout, (1,600)):
        raise RuntimeError("Timeout must be a valid integer in the range 1-600")
    args.timeout = int(args.timeout)

    
    samba_version = re.match(r".*(\d+\.\d+\.\d+).*", check_output(["smbclient", "--version"]).decode()).group(1)
    samba_version = tuple(int(x) for x in samba_version.split('.'))
    if samba_version < (4, 15, 0):
        GLOBAL_SAMBA_LEGACY = True

    
    
    
    
    if GLOBAL_SAMBA_LEGACY and args.nthash and (args.Gm or args.C):
        raise RuntimeError("The -C and -Gm argument require Samba 4.15 or higher when used in combination with -H")

    return args



def check_dependencies():
    missing = []

    for dep in DEPS:
        if not shutil.which(dep):
            missing.append(dep)

    if missing:
        error_msg = (f"The following dependend tools are missing: {', '.join(missing)}\n"
                     "     For Gentoo, you need to install the 'samba' package.\n"
                     "     For Debian derivates (like Ubuntu) or ArchLinux, you need to install the 'smbclient' package.\n"
                     "     For Fedora derivates (like RHEL, CentOS), you need to install the 'samba-common-tools' and 'samba-client' package.")
        raise RuntimeError(error_msg)



def main():
    
    global GLOBAL_COLORS
    if "NO_COLOR" in os.environ:
        GLOBAL_COLORS = False

    print_banner()

    
    try:
        Dumper.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
        check_dependencies()
        args = check_arguments()
    except Exception as e:
        abort(str(e))

    
    start_time = datetime.now()
    try:
        enum = Enumerator(args)
        enum.run()
    except RuntimeError as e:
        abort(str(e))
    except KeyboardInterrupt:
        warn("Received SIGINT, aborting enumeration")
    finally:
        if 'enum' in locals():
            result = enum.finish()
            if not result.retval:
                abort(result.retmsg)
    elapsed_time = datetime.now() - start_time

    print(f"\nCompleted after {elapsed_time.total_seconds():.2f} seconds")

if __name__ == "__main__":
    main()
