"""
IPy - class and tools for handling of IPv4 and IPv6 addresses and networks.
See README file for learn how to use IPy.

Further Information might be available at:
https://github.com/haypo/python-ipy
"""

__version__ = '1.01'

import bisect
import types
try:
    import collections.abc as collections_abc
except ImportError:
    import collections as collections_abc




IPv4ranges = {
    '0':                'PUBLIC',   
    '00000000':         'PRIVATE',  
    '00001010':         'PRIVATE',  
    '0110010001':       'CARRIER_GRADE_NAT', 
    '01111111':         'LOOPBACK', 
    '1':                'PUBLIC',   
    '1010100111111110': 'PRIVATE',  
    '101011000001':     'PRIVATE',  
    '1100000010101000': 'PRIVATE',  
    '111':              'RESERVED', 
    }





IPv6ranges = {
    '00000000'                                      : 'RESERVED',               
    '0' * 96                                        : 'RESERVED',               
    '0' * 128                                       : 'UNSPECIFIED',            
    '0' * 127 + '1'                                 : 'LOOPBACK',               
    '0' * 80 + '1' * 16                             : 'IPV4MAP',                
    '00000000011001001111111110011011' + '0' * 64   : 'WKP46TRANS',             
    '00000001'                                      : 'UNASSIGNED',             
    '0000001'                                       : 'RESERVED',               
    '0000010'                                       : 'RESERVED',               
    '0000011'                                       : 'RESERVED',               
    '00001'                                         : 'RESERVED',               
    '0001'                                          : 'RESERVED',               
    '001'                                           : 'GLOBAL-UNICAST',         
    '00100000000000010000000'                       : 'SPECIALPURPOSE',         
    '00100000000000010000000000000000'              : 'TEREDO',                 
    '00100000000000010000000000000010' + '0' * 16   : 'BMWG',                   
    '0010000000000001000000000001'                  : 'ORCHID',                 
    '00100000000000010000001'                       : 'ALLOCATED APNIC',        
    '00100000000000010000010'                       : 'ALLOCATED ARIN',         
    '00100000000000010000011'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010000100'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010000101'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010000110'                       : 'ALLOCATED APNIC',        
    '00100000000000010000110110111000'              : 'DOCUMENTATION',          
    '00100000000000010000111'                       : 'ALLOCATED APNIC',        
    '00100000000000010001001'                       : 'ALLOCATED LACNIC',       
    '00100000000000010001010'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010001011'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010001100'                       : 'ALLOCATED ARIN',         
    '00100000000000010001101'                       : 'ALLOCATED RIPE NCC',     
    '0010000000000001000111'                        : 'ALLOCATED RIPE NCC',     
    '00100000000000010010'                          : 'ALLOCATED RIPE NCC',     
    '001000000000000100110'                         : 'ALLOCATED RIPE NCC',     
    '0010000000000001001110'                        : 'ALLOCATED RIPE NCC',     
    '0010000000000001001111'                        : 'RESERVED',               
    '00100000000000010100000'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010100001'                       : 'ALLOCATED AFRINIC',      
    '00100000000000010100010'                       : 'ALLOCATED APNIC',        
    '00100000000000010100011'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010100100'                       : 'ALLOCATED ARIN',         
    '00100000000000010100101'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010100110'                       : 'ALLOCATED RIPE NCC',     
    '00100000000000010101'                          : 'ALLOCATED RIPE NCC',     
    '0010000000000001100'                           : 'ALLOCATED APNIC',        
    '00100000000000011010'                          : 'ALLOCATED APNIC',        
    '00100000000000011011'                          : 'ALLOCATED APNIC',        
    '0010000000000010'                              : '6TO4',                   "6to4" [RFC3056]
    '001000000000001100'                            : 'ALLOCATED RIPE NCC',     
    '001001000000'                                  : 'ALLOCATED APNIC',        
    '001001100000'                                  : 'ALLOCATED ARIN',         
    '00100110000100000000000'                       : 'ALLOCATED ARIN',         
    '00100110001000000000000'                       : 'ALLOCATED ARIN',         
    '001010000000'                                  : 'ALLOCATED LACNIC',       
    '001010100000'                                  : 'ALLOCATED RIPE NCC',     
    '001011000000'                                  : 'ALLOCATED AFRINIC',      
    '00101101'                                      : 'RESERVED',               
    '0010111'                                       : 'RESERVED',               
    '0011'                                          : 'RESERVED',               
    '010'                                           : 'RESERVED',               
    '011'                                           : 'RESERVED',               
    '100'                                           : 'RESERVED',               
    '101'                                           : 'RESERVED',               
    '110'                                           : 'RESERVED',               
    '1110'                                          : 'RESERVED',               
    '11110'                                         : 'RESERVED',               
    '111110'                                        : 'RESERVED',               
    '1111110'                                       : 'ULA',                    
    '111111100'                                     : 'RESERVED',               
    '1111111010'                                    : 'LINKLOCAL',              
    '1111111011'                                    : 'RESERVED',               
    '11111111'                                      : 'MULTICAST',              
    '1111111100000001'                              : 'NODE-LOCAL MULTICAST',   
    '1111111100000010'                              : 'LINK-LOCAL MULTICAST',   
    '1111111100000100'                              : 'ADMIN-LOCAL MULTICAST',  
    '1111111100000101'                              : 'SITE-LOCAL MULTICAST',   
    '1111111100001000'                              : 'ORG-LOCAL MULTICAST',    
    '1111111100001110'                              : 'GLOBAL MULTICAST',       
    '1111111100001111'                              : 'RESERVED MULTICAST',     
    '111111110011'                                  : 'PREFIX-BASED MULTICAST', 
    '111111110111'                                  : 'RP-EMBEDDED MULTICAST',  
    }

MAX_IPV4_ADDRESS = 0xffffffff
MAX_IPV6_ADDRESS = 0xffffffffffffffffffffffffffffffff
IPV6_TEST_MAP    = 0xffffffffffffffffffffffff00000000
IPV6_MAP_MASK    = 0x00000000000000000000ffff00000000

try:
    INT_TYPES = (int, long)
    STR_TYPES = (str, unicode)
    xrange
except NameError:
    INT_TYPES = (int,)
    STR_TYPES = (str,)
    xrange = range


class IPint(object):
    """Handling of IP addresses returning integers.

    Use class IP instead because some features are not implemented for
    IPint."""

    def __init__(self, data, ipversion=0, make_net=0):
        """Create an instance of an IP object.

        Data can be a network specification or a single IP. IP
        addresses can be specified in all forms understood by
        parseAddress(). The size of a network can be specified as

        /prefixlen        a.b.c.0/24               2001:658:22a:cafe::/64
        -lastIP           a.b.c.0-a.b.c.255        2001:658:22a:cafe::-2001:658:22a:cafe:ffff:ffff:ffff:ffff
        /decimal netmask  a.b.c.d/255.255.255.0    not supported for IPv6

        If no size specification is given a size of 1 address (/32 for
        IPv4 and /128 for IPv6) is assumed.

        If make_net is True, an IP address will be transformed into the network
        address by applying the specified netmask.

        >>> print(IP('127.0.0.0/8'))
        127.0.0.0/8
        >>> print(IP('127.0.0.0/255.0.0.0'))
        127.0.0.0/8
        >>> print(IP('127.0.0.0-127.255.255.255'))
        127.0.0.0/8
        >>> print(IP('127.0.0.1/255.0.0.0', make_net=True))
        127.0.0.0/8

        See module documentation for more examples.
        """

        
        self.NoPrefixForSingleIp = 1

        
        self.WantPrefixLen = None

        netbits = 0
        prefixlen = -1

        
        if isinstance(data, INT_TYPES):
            self.ip = int(data)
            if ipversion == 0:
                if self.ip <= MAX_IPV4_ADDRESS:
                    ipversion = 4
                else:
                    ipversion = 6
            if ipversion == 4:
                if self.ip > MAX_IPV4_ADDRESS:
                    raise ValueError("IPv4 Address can't be larger than %x: %x" % (MAX_IPV4_ADDRESS, self.ip))
                prefixlen = 32
            elif ipversion == 6:
                if self.ip > MAX_IPV6_ADDRESS:
                    raise ValueError("IPv6 Address can't be larger than %x: %x" % (MAX_IPV6_ADDRESS, self.ip))
                prefixlen = 128
            else:
                raise ValueError("only IPv4 and IPv6 supported")
            self._ipversion = ipversion
            self._prefixlen = prefixlen
        
        elif isinstance(data, IPint):
            self._ipversion = data._ipversion
            self._prefixlen = data._prefixlen
            self.ip = data.ip
        elif isinstance(data, STR_TYPES):
            
            
            x = data.split('-')
            if len(x) == 2:
                
                (ip, last) = x
                (self.ip, parsedVersion) = parseAddress(ip)
                if parsedVersion != 4:
                    raise ValueError("first-last notation only allowed for IPv4")
                (last, lastversion) = parseAddress(last)
                if lastversion != 4:
                    raise ValueError("last address should be IPv4, too")
                if last < self.ip:
                    raise ValueError("last address should be larger than first")
                size = last - self.ip
                netbits = _count1Bits(size)
                
                
                
                if IP('%s/%s' % (ip, 32-netbits)).broadcast().int() != last:
                    raise ValueError("the range %s is not on a network boundary." % data)
            elif len(x) == 1:
                x = data.split('/')
                
                if len(x) == 1:
                    ip = x[0]
                    prefixlen = -1
                elif len(x) > 2:
                    raise ValueError("only one '/' allowed in IP Address")
                else:
                    (ip, prefixlen) = x
                    if prefixlen.find('.') != -1:
                        
                        
                        (netmask, vers) = parseAddress(prefixlen)
                        if vers != 4:
                            raise ValueError("netmask must be IPv4")
                        prefixlen = _netmaskToPrefixlen(netmask)
            elif len(x) > 2:
                raise ValueError("only one '-' allowed in IP Address")
            else:
                raise ValueError("can't parse")

            (self.ip, parsedVersion) = parseAddress(ip, ipversion)
            if ipversion == 0:
                ipversion = parsedVersion
            if prefixlen == -1:
                bits = _ipVersionToLen(ipversion)
                prefixlen = bits - netbits
            self._ipversion = ipversion
            self._prefixlen = int(prefixlen)

            if make_net:
                self.ip = self.ip & _prefixlenToNetmask(self._prefixlen, self._ipversion)

            if not _checkNetaddrWorksWithPrefixlen(self.ip,
            self._prefixlen, self._ipversion):
                raise ValueError("%s has invalid prefix length (%s)" % (repr(self), self._prefixlen))
        else:
            raise TypeError("Unsupported data type: %s" % type(data))

    def int(self):
        """Return the first / base / network addess as an (long) integer.

        The same as IP[0].

        >>> "%X" % IP('10.0.0.0/8').int()
        'A000000'
        """
        return self.ip

    def version(self):
        """Return the IP version of this Object.

        >>> IP('10.0.0.0/8').version()
        4
        >>> IP('::1').version()
        6
        """
        return self._ipversion

    def prefixlen(self):
        """Returns Network Prefixlen.

        >>> IP('10.0.0.0/8').prefixlen()
        8
        """
        return self._prefixlen

    def net(self):
        """
        Return the base (first) address of a network as an (long) integer.
        """
        return self.int()

    def broadcast(self):
        """
        Return the broadcast (last) address of a network as an (long) integer.

        The same as IP[-1]."""
        return self.int() + self.len() - 1

    def _printPrefix(self, want):
        """Prints Prefixlen/Netmask.

        Not really. In fact it is our universal Netmask/Prefixlen printer.
        This is considered an internal function.

        want == 0 / None        don't return anything    1.2.3.0
        want == 1               /prefix                  1.2.3.0/24
        want == 2               /netmask                 1.2.3.0/255.255.255.0
        want == 3               -lastip                  1.2.3.0-1.2.3.255
        """

        if (self._ipversion == 4 and self._prefixlen == 32) or \
           (self._ipversion == 6 and self._prefixlen == 128):
            if self.NoPrefixForSingleIp:
                want = 0
        if want == None:
            want = self.WantPrefixLen
            if want == None:
                want = 1
        if want:
            if want == 2:
                
                netmask = self.netmask()
                if not isinstance(netmask, INT_TYPES):
                    netmask = netmask.int()
                return "/%s" % (intToIp(netmask, self._ipversion))
            elif want == 3:
                return "-%s" % (intToIp(self.ip + self.len() - 1, self._ipversion))
            else:
                
                return "/%d" % (self._prefixlen)
        else:
            return ''

        
        
        
        
        
        

    def strBin(self, wantprefixlen = None):
        """Return a string representation as a binary value.

        >>> print(IP('127.0.0.1').strBin())
        01111111000000000000000000000001
        >>> print(IP('2001:0658:022a:cafe:0200::1').strBin())
        00100000000000010000011001011000000000100010101011001010111111100000001000000000000000000000000000000000000000000000000000000001
        """

        bits = _ipVersionToLen(self._ipversion)
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0
        ret = _intToBin(self.ip)
        return  '0' * (bits - len(ret)) + ret + self._printPrefix(wantprefixlen)

    def strCompressed(self, wantprefixlen = None):
        """Return a string representation in compressed format using '::' Notation.

        >>> IP('127.0.0.1').strCompressed()
        '127.0.0.1'
        >>> IP('2001:0658:022a:cafe:0200::1').strCompressed()
        '2001:658:22a:cafe:200::1'
        >>> IP('ffff:ffff:ffff:ffff:ffff:f:f:fffc/127').strCompressed()
        'ffff:ffff:ffff:ffff:ffff:f:f:fffc/127'
        """

        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1

        if self._ipversion == 4:
            return self.strFullsize(wantprefixlen)
        else:
            if self.ip >> 32 == 0xffff:
                ipv4 = intToIp(self.ip & MAX_IPV4_ADDRESS, 4)
                text = "::ffff:" + ipv4 + self._printPrefix(wantprefixlen)
                return text
            
            hextets = [int(x, 16) for x in self.strFullsize(0).split(':')]
            
            
            followingzeros = [0] * 8
            for i in xrange(len(hextets)):
                followingzeros[i] = _countFollowingZeros(hextets[i:])
            
            compressionpos = followingzeros.index(max(followingzeros))
            if max(followingzeros) > 1:
                
                
                hextets = [x for x in self.strNormal(0).split(':')]
                while compressionpos < len(hextets) and hextets[compressionpos] == '0':
                    del(hextets[compressionpos])
                hextets.insert(compressionpos, '')
                if compressionpos + 1 >= len(hextets):
                    hextets.append('')
                if compressionpos == 0:
                    hextets = [''] + hextets
                return ':'.join(hextets) + self._printPrefix(wantprefixlen)
            else:
                return self.strNormal(0) + self._printPrefix(wantprefixlen)

    def strNormal(self, wantprefixlen = None):
        """Return a string representation in the usual format.

        >>> print(IP('127.0.0.1').strNormal())
        127.0.0.1
        >>> print(IP('2001:0658:022a:cafe:0200::1').strNormal())
        2001:658:22a:cafe:200:0:0:1
        """

        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1

        if self._ipversion == 4:
            ret = self.strFullsize(0)
        elif self._ipversion == 6:
            ret = ':'.join(["%x" % x for x in [int(x, 16) for x in self.strFullsize(0).split(':')]])
        else:
            raise ValueError("only IPv4 and IPv6 supported")



        return ret + self._printPrefix(wantprefixlen)

    def strFullsize(self, wantprefixlen = None):
        """Return a string representation in the non-mangled format.

        >>> print(IP('127.0.0.1').strFullsize())
        127.0.0.1
        >>> print(IP('2001:0658:022a:cafe:0200::1').strFullsize())
        2001:0658:022a:cafe:0200:0000:0000:0001
        """

        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1

        return intToIp(self.ip, self._ipversion) + self._printPrefix(wantprefixlen)

    def strHex(self, wantprefixlen = None):
        """Return a string representation in hex format in lower case.

        >>> print(IP('127.0.0.1').strHex())
        0x7f000001
        >>> print(IP('2001:0658:022a:cafe:0200::1').strHex())
        0x20010658022acafe0200000000000001
        """

        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0

        x = '0x%x' % self.ip
        return x + self._printPrefix(wantprefixlen)

    def strDec(self, wantprefixlen = None):
        """Return a string representation in decimal format.

        >>> print(IP('127.0.0.1').strDec())
        2130706433
        >>> print(IP('2001:0658:022a:cafe:0200::1').strDec())
        42540616829182469433547762482097946625
        """

        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0

        x = '%d' % self.ip
        return x + self._printPrefix(wantprefixlen)

    def iptype(self):
        """Return a description of the IP type ('PRIVATE', 'RESERVED', etc).

        >>> print(IP('127.0.0.1').iptype())
        LOOPBACK
        >>> print(IP('192.168.1.1').iptype())
        PRIVATE
        >>> print(IP('195.185.1.2').iptype())
        PUBLIC
        >>> print(IP('::1').iptype())
        LOOPBACK
        >>> print(IP('2001:0658:022a:cafe:0200::1').iptype())
        ALLOCATED RIPE NCC

        The type information for IPv6 is out of sync with reality.
        """

        

        if self._ipversion == 4:
            iprange = IPv4ranges
        elif self._ipversion == 6:
            iprange = IPv6ranges
        else:
            raise ValueError("only IPv4 and IPv6 supported")

        bits = self.strBin()
        for i in xrange(len(bits), 0, -1):
            if bits[:i] in iprange:
                return iprange[bits[:i]]
        return "unknown"


    def netmask(self):
        """Return netmask as an integer.

        >>> "%X" % IP('195.185.0.0/16').netmask().int()
        'FFFF0000'
        """

        
        bits = _ipVersionToLen(self._ipversion)
        locallen = bits - self._prefixlen

        return ((2 ** self._prefixlen) - 1) << locallen


    def strNetmask(self):
        """Return netmask as an string. Mostly useful for IPv6.

        >>> print(IP('195.185.0.0/16').strNetmask())
        255.255.0.0
        >>> print(IP('2001:0658:022a:cafe::0/64').strNetmask())
        /64
        """

        
        
        bits = _ipVersionToLen(self._ipversion)
        if self._ipversion == 4:
            locallen = bits - self._prefixlen
            return intToIp(((2 ** self._prefixlen) - 1) << locallen, 4)
        elif self._ipversion == 6:
            return "/%d" % self._prefixlen

    def len(self):
        """Return the length of a subnet.

        >>> print(IP('195.185.1.0/28').len())
        16
        >>> print(IP('195.185.1.0/24').len())
        256
        """

        bits = _ipVersionToLen(self._ipversion)
        locallen = bits - self._prefixlen
        return 2 ** locallen


    def __nonzero__(self):
        """All IPy objects should evaluate to true in boolean context.
        Ordinarily they do, but if handling a default route expressed as
        0.0.0.0/0, the __len__() of the object becomes 0, which is used
        as the boolean value of the object.
        """
        return True

    def __bool__(self):
        return self.__nonzero__()

    def __len__(self):
        """
        Return the length of a subnet.

        Called to implement the built-in function len().
        It will break with large IPv6 Networks.
        Use the object's len() instead.
        """
        return self.len()

    def __add__(self, other):
        """Emulate numeric objects through network aggregation"""
        if self._ipversion != other._ipversion:
            raise ValueError("Only networks with the same IP version can be added.")
        if self._prefixlen != other._prefixlen:
            raise ValueError("Only networks with the same prefixlen can be added.")
        if self._prefixlen < 1:
            raise ValueError("Networks with a prefixlen longer than /1 can't be added.")
        if self > other:
            
            return other.__add__(self)
        if other.int() - self[-1].int() != 1:
            raise ValueError("Only adjacent networks can be added together.")
        ret = IP(self.int(), ipversion=self._ipversion)
        ret._prefixlen = self.prefixlen() - 1
        if not _checkNetaddrWorksWithPrefixlen(ret.ip, ret._prefixlen,
                                               ret._ipversion):
            raise ValueError("The resulting %s has invalid prefix length (%s)"
                             % (repr(ret), ret._prefixlen))
        return ret

    def __sub__(self, other):
        """Return the prefixes that are in this IP but not in the other"""
        return _remove_subprefix(self, other)                
        
    def __getitem__(self, key):
        """Called to implement evaluation of self[key].

        >>> ip=IP('127.0.0.0/30')
        >>> for x in ip:
        ...  print(repr(x))
        ...
        IP('127.0.0.0')
        IP('127.0.0.1')
        IP('127.0.0.2')
        IP('127.0.0.3')
        >>> ip[2]
        IP('127.0.0.2')
        >>> ip[-1]
        IP('127.0.0.3')
        """

        if isinstance(key, slice):
            return [self.ip + int(x) for x in xrange(*key.indices(len(self)))]
        if not isinstance(key, INT_TYPES):
            raise TypeError
        if key < 0:
            if abs(key) <= self.len():
                key = self.len() - abs(key)
            else:
                raise IndexError
        else:
            if key >= self.len():
                raise IndexError

        return self.ip + int(key)



    def __contains__(self, item):
        """Called to implement membership test operators.

        Should return true if item is in self, false otherwise. Item
        can be other IP-objects, strings or ints.

        >>> IP('195.185.1.1').strHex()
        '0xc3b90101'
        >>> 0xC3B90101 in IP('195.185.1.0/24')
        True
        >>> '127.0.0.1' in IP('127.0.0.0/24')
        True
        >>> IP('127.0.0.0/24') in IP('127.0.0.0/25')
        False
        """

        if isinstance(item, IP):
            if item._ipversion != self._ipversion:
                return False
        else:
            item = IP(item)
        if item.ip >= self.ip and item.ip < self.ip + self.len() - item.len() + 1:
            return True
        else:
            return False


    def overlaps(self, item):
        """Check if two IP address ranges overlap.

        Returns 0 if the two ranges don't overlap, 1 if the given
        range overlaps at the end and -1 if it does at the beginning.

        >>> IP('192.168.0.0/23').overlaps('192.168.1.0/24')
        1
        >>> IP('192.168.0.0/23').overlaps('192.168.1.255')
        1
        >>> IP('192.168.0.0/23').overlaps('192.168.2.0')
        0
        >>> IP('192.168.1.0/24').overlaps('192.168.0.0/23')
        -1
        """

        if not isinstance(item, IP):
            item = IP(item)
        if item.ip >= self.ip and item.ip < self.ip + self.len():
            return 1
        elif self.ip >= item.ip and self.ip < item.ip + item.len():
            return -1
        else:
            return 0


    def __str__(self):
        """Dispatch to the prefered String Representation.

        Used to implement str(IP)."""

        return self.strCompressed()


    def __repr__(self):
        """Print a representation of the Object.

        Used to implement repr(IP). Returns a string which evaluates
        to an identical Object (without the wantprefixlen stuff - see
        module docstring.

        >>> print(repr(IP('10.0.0.0/24')))
        IP('10.0.0.0/24')
        """

        return("IPint('%s')" % (self.strCompressed(1)))


    def __cmp__(self, other):
        """Called by comparison operations.

        Should return a negative integer if self < other, zero if self
        == other, a positive integer if self > other.
        
        Order is first determined by the address family. IPv4 addresses
        are always smaller than IPv6 addresses:
        
        >>> IP('10.0.0.0') < IP('2001:db8::')
        1
        
        Then the first address is compared. Lower addresses are
        always smaller:
        
        >>> IP('10.0.0.0') > IP('10.0.0.1')
        0
        >>> IP('10.0.0.0/24') > IP('10.0.0.1')
        0
        >>> IP('10.0.1.0') > IP('10.0.0.0/24')
        1
        >>> IP('10.0.1.0/24') > IP('10.0.0.0/24')
        1
        >>> IP('10.0.1.0/24') > IP('10.0.0.0')
        1
        
        Then the prefix length is compared. Shorter prefixes are
        considered smaller than longer prefixes:
        
        >>> IP('10.0.0.0/24') > IP('10.0.0.0')
        0
        >>> IP('10.0.0.0/24') > IP('10.0.0.0/25')
        0
        >>> IP('10.0.0.0/24') > IP('10.0.0.0/23')
        1

        """
        if not isinstance(other, IPint):
            raise TypeError
        
        
        if self._ipversion != other._ipversion:
            return self._ipversion < other._ipversion and -1 or 1
        
        
        if self.ip != other.ip:
            return self.ip < other.ip and -1 or 1
        
        
        if self._prefixlen != other._prefixlen:
            return self._prefixlen < other._prefixlen and -1 or 1
            
        
        return 0

    def __eq__(self, other):
        if not isinstance(other, IPint):
            return False
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __hash__(self):
        """Called for the key object for dictionary operations, and by
        the built-in function hash(). Should return a 32-bit integer
        usable as a hash value for dictionary operations. The only
        required property is that objects which compare equal have the
        same hash value

        >>> IP('10.0.0.0/24').__hash__()
        -167772185
        """

        thehash = int(-1)
        ip = self.ip
        while ip > 0:
            thehash = thehash ^ (ip & 0x7fffffff)
            ip = ip >> 32
        thehash = thehash ^ self._prefixlen
        return int(thehash)


class IP(IPint):
    """Class for handling IP addresses and networks."""

    def net(self):
        """Return the base (first) address of a network as an IP object.

        The same as IP[0].

        >>> IP('10.0.0.0/8').net()
        IP('10.0.0.0')
        """
        return IP(IPint.net(self), ipversion=self._ipversion)

    def broadcast(self):
        """Return the broadcast (last) address of a network as an IP object.

        The same as IP[-1].

        >>> IP('10.0.0.0/8').broadcast()
        IP('10.255.255.255')
        """
        return IP(IPint.broadcast(self))

    def netmask(self):
        """Return netmask as an IP object.

        >>> IP('10.0.0.0/8').netmask()
        IP('255.0.0.0')
         """
        return IP(IPint.netmask(self), ipversion=self._ipversion)

    def _getIPv4Map(self):
        if self._ipversion != 6:
            return None
        if (self.ip >> 32) != 0xffff:
            return None
        ipv4 = self.ip & MAX_IPV4_ADDRESS
        if self._prefixlen != 128:
            ipv4 = '%s/%s' % (ipv4, 32-(128-self._prefixlen))
        return IP(ipv4, ipversion=4)

    def reverseNames(self):
        """Return a list with values forming the reverse lookup.

        >>> IP('213.221.113.87/32').reverseNames()
        ['87.113.221.213.in-addr.arpa.']
        >>> IP('213.221.112.224/30').reverseNames()
        ['224.112.221.213.in-addr.arpa.', '225.112.221.213.in-addr.arpa.', '226.112.221.213.in-addr.arpa.', '227.112.221.213.in-addr.arpa.']
        >>> IP('127.0.0.0/24').reverseNames()
        ['0.0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/23').reverseNames()
        ['0.0.127.in-addr.arpa.', '1.0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/16').reverseNames()
        ['0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/15').reverseNames()
        ['0.127.in-addr.arpa.', '1.127.in-addr.arpa.']
        >>> IP('128.0.0.0/8').reverseNames()
        ['128.in-addr.arpa.']
        >>> IP('128.0.0.0/7').reverseNames()
        ['128.in-addr.arpa.', '129.in-addr.arpa.']
        >>> IP('::1:2').reverseNames()
        ['2.0.0.0.1.ip6.arpa.']
        """

        if self._ipversion == 4:
            ret = []
            
            if self.len() < 2**8:
                for x in self:
                    ret.append(x.reverseName())
            elif self.len() < 2**16:
                for i in xrange(0, self.len(), 2**8):
                    ret.append(self[i].reverseName()[2:])
            elif self.len() < 2**24:
                for i in xrange(0, self.len(), 2**16):
                    ret.append(self[i].reverseName()[4:])
            else:
                for i in xrange(0, self.len(), 2**24):
                    ret.append(self[i].reverseName()[6:])
            return ret
        elif self._ipversion == 6:
            ipv4 = self._getIPv4Map()
            if ipv4 is not None:
                return ipv4.reverseNames()
            s = "%x" % self.ip
            if self._prefixlen % 4 != 0:
                raise NotImplementedError("can't create IPv6 reverse names at sub nibble level")
            s = list(s)
            s.reverse()
            s = '.'.join(s)
            first_nibble_index = int(32 - (self._prefixlen // 4)) * 2
            return ["%s.ip6.arpa." % s[first_nibble_index:]]
        else:
            raise ValueError("only IPv4 and IPv6 supported")

    def reverseName(self):
        """Return the value for reverse lookup/PTR records as RFC 2317 look alike.

        RFC 2317 is an ugly hack which only works for sub-/24 e.g. not
        for /23. Do not use it. Better set up a zone for every
        address. See reverseName for a way to achieve that.

        >>> print(IP('195.185.1.1').reverseName())
        1.1.185.195.in-addr.arpa.
        >>> print(IP('195.185.1.0/28').reverseName())
        0-15.1.185.195.in-addr.arpa.
        >>> IP('::1:2').reverseName()
        '2.0.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa.'
        >>> IP('ff02::/64').reverseName()
        '0.0.0.0.0.0.0.0.0.0.0.0.2.0.f.f.ip6.arpa.'
        """

        if self._ipversion == 4:
            s = self.strFullsize(0)
            s = s.split('.')
            s.reverse()
            first_byte_index = int(4 - (self._prefixlen // 8))
            if self._prefixlen % 8 != 0:
                nibblepart = "%s-%s" % (s[3-(self._prefixlen // 8)], intToIp(self.ip + self.len() - 1, 4).split('.')[-1])
                nibblepart += '.'
            else:
                nibblepart = ""

            s = '.'.join(s[first_byte_index:])
            return "%s%s.in-addr.arpa." % (nibblepart, s)

        elif self._ipversion == 6:
            ipv4 = self._getIPv4Map()
            if ipv4 is not None:
                return ipv4.reverseName()
            s = '%032x' % self.ip
            if self._prefixlen % 4 != 0:
                nibblepart = "%s-%x" % (s[self._prefixlen:], self.ip + self.len() - 1)
                nibblepart += '.'
            else:
                nibblepart = ""
            s = list(s)
            s.reverse()
            s = '.'.join(s)
            first_nibble_index = int(32 - (self._prefixlen // 4)) * 2
            return "%s%s.ip6.arpa." % (nibblepart, s[first_nibble_index:])
        else:
            raise ValueError("only IPv4 and IPv6 supported")

    def make_net(self, netmask):
        """Transform a single IP address into a network specification by
        applying the given netmask.

        Returns a new IP instance.

        >>> print(IP('127.0.0.1').make_net('255.0.0.0'))
        127.0.0.0/8
        """
        if '/' in str(netmask):
            raise ValueError("invalid netmask (%s)" % netmask)
        return IP('%s/%s' % (self, netmask), make_net=True)

    def __getitem__(self, key):
        """Called to implement evaluation of self[key].

        >>> ip=IP('127.0.0.0/30')
        >>> for x in ip:
        ...  print(str(x))
        ...
        127.0.0.0
        127.0.0.1
        127.0.0.2
        127.0.0.3
        >>> print(str(ip[2]))
        127.0.0.2
        >>> print(str(ip[-1]))
        127.0.0.3
        """
        if isinstance(key, slice):
            return [IP(IPint.__getitem__(self, x), ipversion=self._ipversion) for x in xrange(*key.indices(len(self)))]
        return IP(IPint.__getitem__(self, key), ipversion=self._ipversion)

    def __repr__(self):
        """Print a representation of the Object.

        >>> IP('10.0.0.0/8')
        IP('10.0.0.0/8')
        """

        return("IP('%s')" % (self.strCompressed(1)))

    def get_mac(self):
        """
        Get the 802.3 MAC address from IPv6 RFC 2464 address, in lower case.
        Return None if the address is an IPv4 or not a IPv6 RFC 2464 address.

        >>> IP('fe80::f66d:04ff:fe47:2fae').get_mac()
        'f4:6d:04:47:2f:ae'
        """
        if self._ipversion != 6:
            return None
        if (self.ip & 0x20000ffff000000) != 0x20000fffe000000:
            return None
        return '%02x:%02x:%02x:%02x:%02x:%02x' % (
            (((self.ip >> 56) & 0xff) & 0xfd),
            (self.ip >> 48) & 0xff,
            (self.ip >> 40) & 0xff,
            (self.ip >> 16) & 0xff,
            (self.ip >> 8) & 0xff,
            self.ip & 0xff,
        )

    def v46map(self):
        """
        Returns the IPv6 mapped address of an IPv4 address, or the corresponding
        IPv4 address if the IPv6 address is in the appropriate range.
        Raises a ValueError if the IPv6 address is not translatable. See RFC 4291.

        >>> IP('192.168.1.1').v46map()
        IP('::ffff:192.168.1.1')
        >>> IP('::ffff:192.168.1.1').v46map()
        IP('192.168.1.1')
        """
        if self._ipversion == 4:
            return IP(str(IPV6_MAP_MASK + self.ip) + 
                          "/%s" % (self._prefixlen + 96))
        else:
            if self.ip & IPV6_TEST_MAP == IPV6_MAP_MASK:
                return IP(str(self.ip - IPV6_MAP_MASK) +
                          "/%s" % (self._prefixlen - 96))
        raise ValueError("%s cannot be converted to an IPv4 address."
                         % repr(self))

class IPSet(collections_abc.MutableSet):
    def __init__(self, iterable=[]):
        
        if not isinstance(iterable, collections_abc.Iterable):
            raise TypeError("'%s' object is not iterable" % type(iterable).__name__)
        
        
        for prefix in iterable:
            if not isinstance(prefix, IP):
                raise ValueError('Only IP objects can be added to an IPSet')
            
        
        self.prefixes = iterable[:]
        self.optimize()
            
    def __contains__(self, ip):
        valid_masks = self.prefixtable.keys()
        if isinstance(ip, IP):
            
            ip_mask = ip._prefixlen
            valid_masks = [x for x in valid_masks if x <= ip_mask]
        for mask in sorted(valid_masks):
            i = bisect.bisect(self.prefixtable[mask], ip)
            
            
            if i and ip in self.prefixtable[mask][i - 1]:
                return True

    def __iter__(self):
        for prefix in self.prefixes:
            yield prefix
    
    def __len__(self):
        return self.len()
    
    def __add__(self, other):
        return IPSet(self.prefixes + other.prefixes)
    
    def __sub__(self, other):
        new = IPSet(self.prefixes)
        for prefix in other:
            new.discard(prefix)
        return new
    
    def __and__(self, other):
        left = iter(self.prefixes)
        right = iter(other.prefixes)
        result = []
        try:
            l = next(left)
            r = next(right)
            while True:
                
                
                if l in r:
                    result.append(l)
                    l = next(left)
                    continue
                elif r in l:
                    result.append(r)
                    r = next(right)
                    continue
                if l < r:
                    l = next(left)
                else:
                    r = next(right)
        except StopIteration:
            return IPSet(result)

    def __repr__(self):
        return '%s([' % self.__class__.__name__ + ', '.join(map(repr, self.prefixes)) + '])'
    
    def len(self):
        return sum(prefix.len() for prefix in self.prefixes)

    def add(self, value):
        
        if not isinstance(value, collections_abc.Iterable):
            value = [value]
        
        
        for prefix in value:
            if not isinstance(prefix, IP):
                raise ValueError('Only IP objects can be added to an IPSet')
        
        
        self.prefixes.extend(value)
        self.optimize()
    
    def discard(self, value):
        
        if not isinstance(value, collections_abc.Iterable):
            value = [value]
            
        
        if isinstance(value, IPSet):
            value = value.prefixes

        
        for del_prefix in value:
            if not isinstance(del_prefix, IP):
                raise ValueError('Only IP objects can be removed from an IPSet')
            
            
            found = False
            d = 0
            for i in range(len(self.prefixes)):
                if self.prefixes[i - d] in del_prefix:
                    self.prefixes.pop(i - d)
                    d = d + 1
                    found = True
                
            if found:
                
                
                continue
            
            
            found = False
            for i in range(len(self.prefixes)):
                if del_prefix in self.prefixes[i]:
                    self.prefixes[i:i+1] = self.prefixes[i] - del_prefix
                    break
                
        self.optimize()

    def isdisjoint(self, other):
        left = iter(self.prefixes)
        right = iter(other.prefixes)
        try:
            l = next(left)
            r = next(right)
            while True:
                if l in r or r in l:
                    return False
                if l < r:
                    l = next(left)
                else:
                    r = next(right)
        except StopIteration:
            return True

    def optimize(self):
        
        self.prefixes.sort()

        
        addrlen = len(self.prefixes)
        i = 0
        while i < addrlen:
            
            
            j = i+1
            while j < addrlen and self.prefixes[j] in self.prefixes[i]:
                
                self.prefixes[j] = None
                j += 1
            
            
            i = j
            
        
        run_again = True
        while run_again:
            
            
            self.prefixes = [a for a in self.prefixes if a is not None]
        
            
            
            run_again = False

            
            
            addrlen = len(self.prefixes)
            i = 0
            while i < addrlen-1:
                j = i + 1
                
                try:
                    
                    
                    self.prefixes[i] += self.prefixes[j]
                    self.prefixes[j] = None
                    i = j + 1
                    run_again = True
                except ValueError:
                    
                    i = j

        
        
        self.prefixtable = {}
        for address in self.prefixes:
            try:
                self.prefixtable[address._prefixlen].append(address)
            except KeyError:
                self.prefixtable[address._prefixlen] = [address]

def _parseAddressIPv6(ipstr):
    """
    Internal function used by parseAddress() to parse IPv6 address with ':'.

    >>> print(_parseAddressIPv6('::'))
    0
    >>> print(_parseAddressIPv6('::1'))
    1
    >>> print(_parseAddressIPv6('0:0:0:0:0:0:0:1'))
    1
    >>> print(_parseAddressIPv6('0:0:0::0:0:1'))
    1
    >>> print(_parseAddressIPv6('0:0:0:0:0:0:0:0'))
    0
    >>> print(_parseAddressIPv6('0:0:0::0:0:0'))
    0

    >>> print(_parseAddressIPv6('FEDC:BA98:7654:3210:FEDC:BA98:7654:3210'))
    338770000845734292534325025077361652240
    >>> print(_parseAddressIPv6('1080:0000:0000:0000:0008:0800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('1080:0:0:0:8:800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('1080:0::8:800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('1080::8:800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('FF01:0:0:0:0:0:0:43'))
    338958331222012082418099330867817087043
    >>> print(_parseAddressIPv6('FF01:0:0::0:0:43'))
    338958331222012082418099330867817087043
    >>> print(_parseAddressIPv6('FF01::43'))
    338958331222012082418099330867817087043
    >>> print(_parseAddressIPv6('0:0:0:0:0:0:13.1.68.3'))
    218186755
    >>> print(_parseAddressIPv6('::13.1.68.3'))
    218186755
    >>> print(_parseAddressIPv6('0:0:0:0:0:FFFF:129.144.52.38'))
    281472855454758
    >>> print(_parseAddressIPv6('::FFFF:129.144.52.38'))
    281472855454758
    >>> print(_parseAddressIPv6('1080:0:0:0:8:800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('1080::8:800:200C:417A'))
    21932261930451111902915077091070067066
    >>> print(_parseAddressIPv6('::1:2:3:4:5:6'))
    1208962713947218704138246
    >>> print(_parseAddressIPv6('1:2:3:4:5:6::'))
    5192455318486707404433266432802816
    """

    
    
    
    items = []
    index = 0
    fill_pos = None
    while index < len(ipstr):
        text = ipstr[index:]
        if text.startswith("::"):
            if fill_pos is not None:
                
                raise ValueError("%r: Invalid IPv6 address: more than one '::'" % ipstr)
            fill_pos = len(items)
            index += 2
            continue
        pos = text.find(':')
        if pos == 0:
            
            raise ValueError("%r: Invalid IPv6 address" % ipstr)
        if pos != -1:
            items.append(text[:pos])
            if text[pos:pos+2] == "::":
                index += pos
            else:
                index += pos+1

            if index == len(ipstr):
                
                raise ValueError("%r: Invalid IPv6 address" % ipstr)
        else:
            items.append(text)
            break

    if items and '.' in items[-1]:
        
        if (fill_pos is not None) and not (fill_pos <= len(items)-1):
            
            raise ValueError("%r: Invalid IPv6 address: '::' after IPv4" % ipstr)
        value = parseAddress(items[-1])[0]
        items = items[:-1] + ["%04x" % (value >> 16), "%04x" % (value & 0xffff)]

    
    
    if fill_pos is not None:
        diff = 8 - len(items)
        if diff <= 0:
            raise ValueError("%r: Invalid IPv6 address: '::' is not needed" % ipstr)
        items = items[:fill_pos] + ['0']*diff + items[fill_pos:]

    
    if len(items) != 8:
        
        raise ValueError("%r: Invalid IPv6 address: should have 8 hextets" % ipstr)

    
    value = 0
    index = 0
    for item in items:
        try:
            item = int(item, 16)
            error = not(0 <= item <= 0xffff)
        except ValueError:
            error = True
        if error:
            raise ValueError("%r: Invalid IPv6 address: invalid hexlet %r" % (ipstr, item))
        value = (value << 16) + item
        index += 1
    return value

def parseAddress(ipstr, ipversion=0):
    """
    Parse a string and return the corresponding IP address (as integer)
    and a guess of the IP version.

    Following address formats are recognized:

    >>> def testParseAddress(address):
    ...     ip, version = parseAddress(address)
    ...     print(("%s (IPv%s)" % (ip, version)))
    ...
    >>> testParseAddress('0x0123456789abcdef')           
    81985529216486895 (IPv6)
    >>> testParseAddress('123.123.123.123')              
    2071690107 (IPv4)
    >>> testParseAddress('123.123')                      
    2071658496 (IPv4)
    >>> testParseAddress('127')
    2130706432 (IPv4)
    >>> testParseAddress('255')
    4278190080 (IPv4)
    >>> testParseAddress('256')
    256 (IPv4)
    >>> testParseAddress('108000000000000000080800200C417A')
    21932261930451111902915077091070067066 (IPv6)
    >>> testParseAddress('0x108000000000000000080800200C417A')
    21932261930451111902915077091070067066 (IPv6)
    >>> testParseAddress('1080:0000:0000:0000:0008:0800:200C:417A')
    21932261930451111902915077091070067066 (IPv6)
    >>> testParseAddress('1080:0:0:0:8:800:200C:417A')
    21932261930451111902915077091070067066 (IPv6)
    >>> testParseAddress('1080:0::8:800:200C:417A')
    21932261930451111902915077091070067066 (IPv6)
    >>> testParseAddress('::1')
    1 (IPv6)
    >>> testParseAddress('::')
    0 (IPv6)
    >>> testParseAddress('0:0:0:0:0:FFFF:129.144.52.38')
    281472855454758 (IPv6)
    >>> testParseAddress('::13.1.68.3')
    218186755 (IPv6)
    >>> testParseAddress('::FFFF:129.144.52.38')
    281472855454758 (IPv6)
    """

    try:
        hexval = int(ipstr, 16)
    except ValueError:
        hexval = None
    try:
        intval = int(ipstr, 10)
    except ValueError:
        intval = None

    if ipstr.startswith('0x') and hexval is not None:
        if hexval > MAX_IPV6_ADDRESS:
            raise ValueError("IP Address can't be larger than %x: %x" % (MAX_IPV6_ADDRESS, hexval))
        if hexval <= MAX_IPV4_ADDRESS:
            return (hexval, 4)
        else:
            return (hexval, 6)

    if ipstr.find(':') != -1:
        return (_parseAddressIPv6(ipstr), 6)

    elif len(ipstr) == 32 and hexval is not None:
        
        return (hexval, 6)

    elif ipstr.find('.') != -1 or (intval is not None and intval < 256 and ipversion != 6):
        
        bytes = ipstr.split('.')
        if len(bytes) > 4:
            raise ValueError("IPv4 Address with more than 4 bytes")
        bytes += ['0'] * (4 - len(bytes))
        bytes = [int(x) for x in bytes]
        for x in bytes:
            if x > 255 or x < 0:
                raise ValueError("%r: single byte must be 0 <= byte < 256" % (ipstr))
        return ((bytes[0] << 24) + (bytes[1] << 16) + (bytes[2] << 8) + bytes[3], 4)

    elif intval is not None:
        
        
        
        if intval > MAX_IPV6_ADDRESS:
            raise ValueError("IP Address can't be larger than %x: %x" % (MAX_IPV6_ADDRESS, intval))
        if intval <= MAX_IPV4_ADDRESS and ipversion != 6:
            return (intval, 4)
        else:
            return (intval, 6)

    raise ValueError("IP Address format was invalid: %s" % ipstr)


def intToIp(ip, version):
    """Transform an integer string into an IP address."""

    
    ip = int(ip)

    if ip < 0:
        raise ValueError("IPs can't be negative: %d" % (ip))

    ret = ''
    if version == 4:
        if ip > MAX_IPV4_ADDRESS:
            raise ValueError("IPv4 Address can't be larger than %x: %x" % (MAX_IPV4_ADDRESS, ip))
        for l in xrange(4):
            ret = str(ip & 0xff) + '.' + ret
            ip = ip >> 8
        ret = ret[:-1]
    elif version == 6:
        if ip > MAX_IPV6_ADDRESS:
            raise ValueError("IPv6 Address can't be larger than %x: %x" % (MAX_IPV6_ADDRESS, ip))
        l = "%032x" % ip
        for x in xrange(1, 33):
            ret = l[-x] + ret
            if x % 4 == 0:
                ret = ':' + ret
        ret = ret[1:]
    else:
        raise ValueError("only IPv4 and IPv6 supported")

    return ret

def _ipVersionToLen(version):
    """Return number of bits in address for a certain IP version.

    >>> _ipVersionToLen(4)
    32
    >>> _ipVersionToLen(6)
    128
    >>> _ipVersionToLen(5)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "IPy.py", line 1076, in _ipVersionToLen
        raise ValueError("only IPv4 and IPv6 supported")
    ValueError: only IPv4 and IPv6 supported
    """

    if version == 4:
        return 32
    elif version == 6:
        return 128
    else:
        raise ValueError("only IPv4 and IPv6 supported")


def _countFollowingZeros(l):
    """Return number of elements containing 0 at the beginning of the list."""
    if len(l) == 0:
        return 0
    elif l[0] != 0:
        return 0
    else:
        return 1 + _countFollowingZeros(l[1:])


_BitTable = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
            '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
            'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

def _intToBin(val):
    """Return the binary representation of an integer as string."""

    if val < 0:
        raise ValueError("Only positive values allowed")
    s = "%x" % val
    ret = ''
    for x in s:
        ret += _BitTable[x]
    
    while ret[0] == '0' and len(ret) > 1:
        ret = ret[1:]
    return ret

def _count1Bits(num):
    """Find the highest bit set to 1 in an integer."""
    ret = 0
    while num > 0:
        num = num >> 1
        ret += 1
    return ret

def _count0Bits(num):
    """Find the highest bit set to 0 in an integer."""

    
    num = int(num)
    if num < 0:
        raise ValueError("Only positive Numbers please: %s" % (num))
    ret = 0
    while num > 0:
        if num & 1 == 1:
            break
        num = num >> 1
        ret += 1
    return ret


def _checkPrefix(ip, prefixlen, version):
    """Check the validity of a prefix

    Checks if the variant part of a prefix only has 0s, and the length is
    correct.

    >>> _checkPrefix(0x7f000000, 24, 4)
    1
    >>> _checkPrefix(0x7f000001, 24, 4)
    0
    >>> repr(_checkPrefix(0x7f000001, -1, 4))
    'None'
    >>> repr(_checkPrefix(0x7f000001, 33, 4))
    'None'
    """

    
    bits = _ipVersionToLen(version)

    if prefixlen < 0 or prefixlen > bits:
        return None

    if ip == 0:
        zbits = bits + 1
    else:
        zbits = _count0Bits(ip)
    if zbits <  bits - prefixlen:
        return 0
    else:
        return 1


def _checkNetmask(netmask, masklen):
    """Checks if a netmask is expressable as a prefixlen."""

    num = int(netmask)
    bits = masklen

    
    while (num & 1) == 0 and bits != 0:
        num = num >> 1
        bits -= 1
        if bits == 0:
            break
    
    while bits > 0:
        if (num & 1) == 0:
            raise ValueError("Netmask 0x%x can't be expressed as an prefix." % netmask)
        num = num >> 1
        bits -= 1


def _checkNetaddrWorksWithPrefixlen(net, prefixlen, version):
    """Check if a base addess of a network is compatible with a prefixlen"""
    try:
        return (net & _prefixlenToNetmask(prefixlen, version) == net)
    except ValueError:
        return False


def _netmaskToPrefixlen(netmask):
    """Convert an Integer representing a netmask to a prefixlen.

    E.g. 0xffffff00 (255.255.255.0) returns 24
    """

    netlen = _count0Bits(netmask)
    masklen = _count1Bits(netmask)
    _checkNetmask(netmask, masklen)
    return masklen - netlen


def _prefixlenToNetmask(prefixlen, version):
    """Return a mask of n bits as a long integer.

    From 'IP address conversion functions with the builtin socket module'
    by Alex Martelli
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66517
    """
    if prefixlen == 0:
        return 0
    elif prefixlen < 0:
        raise ValueError("Prefixlen must be > 0")
    return ((2<<prefixlen-1)-1) << (_ipVersionToLen(version) - prefixlen)


def _remove_subprefix(prefix, subprefix):
    if prefix in subprefix:
        
        return IPSet()
    
    if subprefix not in prefix:
        
        return IPSet([IP(prefix)])
    
    
    prefixes = [
        IP('%s/%d' % (prefix[0], prefix._prefixlen + 1)),
        IP('%s/%d' % (prefix[int(prefix.len() / 2)], prefix._prefixlen + 1)),
    ]
    if subprefix in prefixes[0]:
        return _remove_subprefix(prefixes[0], subprefix) + IPSet([prefixes[1]])
    else:
        return IPSet([prefixes[0]]) + _remove_subprefix(prefixes[1], subprefix)


if __name__ == "__main__":
    import doctest
    failure, nbtest = doctest.testmod()
    if failure:
        import sys
        sys.exit(1)
