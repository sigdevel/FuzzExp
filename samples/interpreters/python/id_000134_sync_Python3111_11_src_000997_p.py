
import os
import sys
import json
import time
import shutil
import datetime
import logging
import ipaddress
import string
import tempfile
import unittest
import warnings

from pathlib import Path
from collections import deque

import datrie
import pytest

from diskcache import Index

import node_tools.timing_funcs as tf

from node_tools.ctlr_funcs import gen_netobj_queue
from node_tools.ctlr_funcs import handle_net_cfg
from node_tools.ctlr_funcs import ipnet_get_netcfg
from node_tools.ctlr_funcs import is_exit_node
from node_tools.ctlr_funcs import name_generator
from node_tools.ctlr_funcs import netcfg_get_ipnet
from node_tools.ctlr_funcs import set_network_cfg
from node_tools.ctlr_funcs import unset_network_cfg
from node_tools.exceptions import MemberNodeError
from node_tools.helper_funcs import AttrDict
from node_tools.helper_funcs import ENODATA
from node_tools.helper_funcs import NODE_SETTINGS
from node_tools.helper_funcs import find_ipv4_iface
from node_tools.helper_funcs import get_filepath
from node_tools.helper_funcs import get_runtimedir
from node_tools.helper_funcs import json_load_file
from node_tools.helper_funcs import put_state_msg
from node_tools.helper_funcs import send_cfg_handler
from node_tools.helper_funcs import set_initial_role
from node_tools.helper_funcs import startup_handlers
from node_tools.helper_funcs import validate_role
from node_tools.helper_funcs import xform_state_diff
from node_tools.logger_config import setup_logging
from node_tools.msg_queues import handle_wedged_nodes
from node_tools.network_funcs import do_host_check
from node_tools.network_funcs import do_peer_check
from node_tools.network_funcs import get_net_cmds
from node_tools.network_funcs import run_host_check
from node_tools.network_funcs import run_net_check
from node_tools.node_funcs import check_daemon
from node_tools.node_funcs import control_daemon
from node_tools.node_funcs import do_shutdown
from node_tools.node_funcs import handle_moon_data
from node_tools.node_funcs import parse_moon_data
from node_tools.sched_funcs import catch_exceptions
from node_tools.sched_funcs import check_return_status
from node_tools.trie_funcs import cleanup_state_tries
from node_tools.trie_funcs import create_state_trie
from node_tools.trie_funcs import find_exit_net
from node_tools.trie_funcs import find_orphans
from node_tools.trie_funcs import get_active_nodes
from node_tools.trie_funcs import get_bootstrap_list
from node_tools.trie_funcs import get_dangling_net_data
from node_tools.trie_funcs import get_invalid_net_id
from node_tools.trie_funcs import get_neighbor_ids
from node_tools.trie_funcs import get_target_node_id
from node_tools.trie_funcs import get_wedged_node_id
from node_tools.trie_funcs import load_id_trie
from node_tools.trie_funcs import load_state_trie
from node_tools.trie_funcs import save_state_trie
from node_tools.trie_funcs import trie_is_empty


try:
    from datetime import timezone
    utc = timezone.utc
except ImportError:
    from daemon.timezone import UTC
    utc = UTC()


def read_file(filename):
    """
    Quickndirty get the first line of data from a file.
    """
    import codecs

    with codecs.open(filename, 'r', 'utf8') as f:
        return f.readline().strip()


class mock_zt_api_client(object):
    """
    Client API to serve simple GET data endpoints
    """
    def __init__(self):
        self.test_dir = 'test/test_data'
        self.response = '200'

    def get_data(self, endpoint):
        self.endpoint = json_load_file(endpoint, self.test_dir)
        return self.response, self.endpoint

    def load_data(self, endpoint):
        import os
        self.endpoint = read_file(os.path.join(self.test_dir, endpoint))
        return self.response, self.endpoint



class BasicConfigTest(unittest.TestCase):

    """Basic tests for logger_config.py"""

    def setUp(self):
        super(BasicConfigTest, self).setUp()
        self.handlers = logging.root.handlers
        self.saved_handlers = logging._handlers.copy()
        self.saved_handler_list = logging._handlerList[:]
        self.original_logging_level = logging.root.level
        self.addCleanup(self.cleanup)
        self.log = logging.getLogger('test')
        logging.root.handlers = []

    def tearDown(self):
        for h in logging.root.handlers[:]:
            logging.root.removeHandler(h)
            h.close()
        super(BasicConfigTest, self).tearDown()

    def cleanup(self):
        setattr(logging.root, 'handlers', self.handlers)
        logging._handlers.clear()
        logging._handlers.update(self.saved_handlers)
        logging._handlerList[:] = self.saved_handler_list
        logging.root.level = self.original_logging_level

    def test_debug_level(self):
        old_level = logging.root.level
        self.addCleanup(logging.root.setLevel, old_level)

        debug = True
        setup_logging(debug, '/dev/null')
        self.assertEqual(logging.root.level, logging.DEBUG)
        
        logging.basicConfig(level=58)
        self.assertEqual(logging.root.level, logging.DEBUG)

    def test_info_level(self):
        old_level = logging.root.level
        self.addCleanup(logging.root.setLevel, old_level)

        debug = False
        setup_logging(debug, '/dev/null')
        str_level = logging.getLevelName(self.log.getEffectiveLevel())
        
        self.assertEqual(str_level, 'INFO')
        self.assertEqual(logging.root.level, logging.INFO)
        
        logging.basicConfig(level=58)
        self.assertEqual(logging.root.level, logging.INFO)


class CheckReturnsTest(unittest.TestCase):
    """
    Tests for check_return_status().
    """
    def test_bad_returns(self):
        naughty_list = [1, (), '', [], {}, {False: 'blarg'}, False, None]
        for thing in naughty_list:
            
            self.assertFalse(check_return_status(thing))

    def test_int_return(self):
        self.assertTrue(check_return_status(0))
        self.assertFalse(check_return_status(1))

    def test_bool_return(self):
        self.assertTrue(check_return_status(True))
        self.assertFalse(check_return_status(False))

    def test_string_return(self):
        self.assertFalse(check_return_status('blurt'))
        good_list = ['OK', 'Success', 'UP', 'good']
        for thing in good_list:
            self.assertTrue(check_return_status(thing))

    def test_multiple_returns(self):
        self.assertTrue(check_return_status((True, 'Success', 0)))
        self.assertFalse(check_return_status((False, 'blarg', 1)))
        self.assertTrue(check_return_status(['forecast is good', 'some clouds', 0]))


class HandleMoonDataTest(unittest.TestCase):
    """
    Tests for handle_moon_data() state updates.
    """
    def setUp(self):
        super(HandleMoonDataTest, self).setUp()
        from node_tools import state_data as st

        self.saved_state = AttrDict.from_nested_dict(st.fpnState)
        self.default_state = AttrDict.from_nested_dict(st.defState)
        self.state = st.fpnState
        self.client = client = mock_zt_api_client()
        _, moon_data = client.get_data('moon')
        self.data = parse_moon_data(moon_data)
        self.moons = ['deadd738e6']
        NODE_SETTINGS['moon_list'] = self.moons

    def tearDown(self):
        from node_tools import state_data as st

        st.fpnState = self.saved_state
        NODE_SETTINGS['moon_list'] = ['9790eaaea1']
        super(HandleMoonDataTest, self).tearDown()

    def test_handle_empty_list(self):
        """Raise MemberNodeError error"""
        with self.assertRaises(MemberNodeError):
            handle_moon_data([])

    def test_handle_extra_moon(self):
        """Handle a typical case with 2 moons"""
        self.assertIn(self.state.moon_id0, self.moons)
        self.assertEqual(self.state.moon_addr, '192.81.135.59')
        handle_moon_data(self.data)
        self.assertEqual(self.state.moon_addr, '10.0.1.66')

    def test_handle_single_moon(self):
        """Handle a single moon"""
        self.data = [('deadd738e6', '10.0.1.66', '9993')]
        self.assertIn(self.state.moon_id0, self.moons)
        self.assertEqual(self.state.moon_addr, '192.81.135.59')
        handle_moon_data(self.data)
        self.assertEqual(self.state.moon_addr, '10.0.1.66')


class IPv4InterfaceTest(unittest.TestCase):
    """
    Note the input for this test case is the input string for a Python
    ipaddress.IPv4Interface object.
    """
    def test_strip(self):
        """Return IPv4 addr without prefix"""
        strip = find_ipv4_iface('192.168.1.1/24')
        self.assertEqual(strip, '192.168.1.1')

    def test_nostrip(self):
        """Return True if IPv4 addr is valid"""
        nostrip = find_ipv4_iface('172.16.0.241' + '/30', False)
        self.assertTrue(nostrip)

    def test_bogus(self):
        """Return False if IPv4 addr is not valid"""
        bogus_addr = find_ipv4_iface('192.168.1.300/24', False)
        self.assertFalse(bogus_addr)


class IPv4NetObjectTest(unittest.TestCase):
    """
    The input for this test case is a bare IPv4 address string,
    followed by an ipaddress.IPv4Network object.
    """
    def test_get_valid_obj(self):
        """Return IPv4 network object"""
        netobj = netcfg_get_ipnet('172.16.0.241')
        self.assertIsInstance(netobj, ipaddress.IPv4Network)
        self.assertEqual(str(netobj), '172.16.0.240/30')

    def test_get_invalid_obj(self):
        """Raise IPv4 address error"""
        with self.assertRaises(ipaddress.AddressValueError):
            netobj = netcfg_get_ipnet('172.16.0.261')

    def test_get_valid_cfg(self):
        netobj = ipaddress.ip_network('172.16.0.0/30')
        res = ipnet_get_netcfg(netobj)
        self.assertIsInstance(res, AttrDict)
        self.assertEqual(res.host, ['172.16.0.2/30'])
        

    def test_get_invalid_cfg(self):
        """Raise IPv4Network ValueError"""
        with self.assertRaises(ValueError):
            res = ipnet_get_netcfg('172.16.0.0/30')


class NetCmdTest(unittest.TestCase):
    """
    Simple test of find_the_net_script.
    """
    def setUp(self):
        super(NetCmdTest, self).setUp()
        self.bin_dir = os.path.join(os.getcwd(), 'bin')

    def test_bin_path(self):
        
        self.assertTrue(os.path.isdir(self.bin_dir))

    def test_get_net_cmds_false(self):
        bin_path = '/bin'
        self.assertIsNone(get_net_cmds(bin_path))

    def test_get_net_cmds_true(self):
        up0, down0, up1, down1 = get_net_cmds(self.bin_dir)
        
        self.assertTrue(os.path.isfile(up0))
        self.assertTrue(os.path.isfile(down0))
        self.assertTrue(os.path.isfile(up1))
        self.assertTrue(os.path.isfile(down1))

    def test_get_net_cmds_single(self):
        cmd = get_net_cmds(self.bin_dir, 'fpn0')
        path, name = os.path.split(cmd[0])
        self.assertEqual(name, 'fpn0-down.sh')

    def test_get_net_cmds_single_up(self):
        cmd = get_net_cmds(self.bin_dir, 'fpn1', True)
        path, name = os.path.split(cmd[0])
        self.assertEqual(name, 'fpn1-setup.sh')


@pytest.mark.xfail(strict=False)
class NetHostCheckTest(unittest.TestCase):
    """
    Running an actual ``ping`` or geoip lookup in a unittest is somewhat
    problematic...
    """
    def setUp(self):
        super(NetHostCheckTest, self).setUp()
        NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'bin')

    def test_do_host_check(self):
        """Requires live internet in test env"""
        state, res, retcode = do_host_check()

    def test_run_host_check(self):
        """Requires live internet in test env"""
        res = run_host_check()

    def test_run_host_check_exc(self):
        """Test the decorator (should move this to decorator tests)"""
        res = run_host_check('/bin')


class NetPeerCheckTest(unittest.TestCase):
    """
    Running an actual ``ping`` or geoip lookup in a unittest is somewhat
    problematic...
    """
    def setUp(self):
        from node_tools import state_data as st

        super(NetPeerCheckTest, self).setUp()
        st.wait_cache.set('fpn0_UP', True, 1)
        NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'bin')

    @pytest.mark.xfail(strict=False)
    def test_run_net_check_geoip(self):
        """Requires live internet in test env"""
        res = run_net_check()
        

    def test_do_peer_check_bad_addr(self):
        """Raise IPv4 address error"""
        with self.assertRaises(ipaddress.AddressValueError):
            res = do_peer_check('192.168.0.261')

    def test_do_peer_check_good_addr(self):
        """Possible permission error in test env"""
        res = do_peer_check('172.16.0.1')
        self.assertIsInstance(res, tuple)
        self.assertEqual(res, (False, b'', 1))


class SetRolesTest(unittest.TestCase):
    """
    Tests for check_and_set_role() and validate_role().
    """
    def setUp(self):
        super(SetRolesTest, self).setUp()
        from node_tools import state_data as st

        self.saved_state = AttrDict.from_nested_dict(st.fpnState)
        self.default_state = AttrDict.from_nested_dict(st.defState)
        self.state = st.fpnState
        self.state.update(fpn_id='deadbeef00')
        self.role = NODE_SETTINGS['node_role']

    def tearDown(self):
        from node_tools import state_data as st

        st.fpnState = self.saved_state
        NODE_SETTINGS['node_role'] = None
        NODE_SETTINGS['mode'] = 'peer'
        super(SetRolesTest, self).tearDown()

    def test_adhoc_mode(self):
        NODE_SETTINGS['mode'] = 'adhoc'
        self.assertIsNone(self.role)

        set_initial_role()
        validate_role()
        self.assertIsNone(NODE_SETTINGS['node_role'])

    def test_ctlr_role(self):
        self.assertIsNone(self.role)

        set_initial_role()
        validate_role()
        self.assertIsNone(NODE_SETTINGS['node_role'])

        NODE_SETTINGS['ctlr_list'].append(self.state['fpn_id'])

        validate_role()

        self.assertEqual(NODE_SETTINGS['node_role'], 'controller')
        self.assertEqual(self.state['fpn_role'], 'controller')
        self.assertEqual(NODE_SETTINGS['node_runner'], 'netstate.py')
        NODE_SETTINGS['ctlr_list'].remove(self.state['fpn_id'])

    def test_moon_role(self):
        self.assertIsNone(self.role)

        set_initial_role()
        validate_role()
        self.assertIsNone(NODE_SETTINGS['node_role'])

        NODE_SETTINGS['moon_list'].append(self.state['fpn_id'])

        validate_role()

        self.assertEqual(NODE_SETTINGS['node_role'], 'moon')
        self.assertEqual(NODE_SETTINGS['node_runner'], 'peerstate.py')
        self.assertEqual(self.state['fpn_role'], 'moon')
        NODE_SETTINGS['moon_list'].remove(self.state['fpn_id'])


class StateChangeTest(unittest.TestCase):
    """
    Note the input for this test case is a pair of node fpnState
    objects (type is dict).
    """
    def setUp(self):
        super(StateChangeTest, self).setUp()
        from node_tools import state_data as st

        self.saved_state = AttrDict.from_nested_dict(st.defState)
        self.state = self.saved_state

    def tearDown(self):
        from node_tools import state_data as st

        st.fpnState = self.saved_state
        super(StateChangeTest, self).tearDown()

    def show_state(self):
        from node_tools import state_data as st

        print('')
        print(self.saved_state)
        print(self.state)

    def test_change_none(self):
        
        self.assertIsInstance(self.state, dict)
        self.assertFalse(self.state['online'])
        self.assertFalse(self.state['fpn1'])

    def test_change_online(self):
        self.state.update(online=True)
        self.assertTrue(self.state['online'])
        self.assertFalse(self.state['fpn0'])
        self.assertFalse(self.state['fpn1'])

    def test_change_upfpn0(self):
        self.state.update(online=True, fpn0=True)
        self.assertTrue(self.state['online'])
        self.assertTrue(self.state['fpn0'])
        self.assertFalse(self.state['fpn1'])

    def test_change_upfpn1_downfpn0(self):
        self.state.update(online=True, fpn0=False, fpn1=True)
        self.assertTrue(self.state['online'])
        self.assertFalse(self.state['fpn0'])
        self.assertTrue(self.state['fpn1'])

    def test_change_upfpn1_upfpn0(self):
        self.state.update(online=True, fpn0=True, fpn1=True)
        self.assertTrue(self.state['online'])
        self.assertTrue(self.state['fpn0'])
        self.assertTrue(self.state['fpn1'])

    def test_state_string_vars(self):
        self.state.update(online=True, fpn1=True)
        for iface in ['fpn0', 'fpn1']:
            if self.state[iface]:
                self.assertEqual(iface, 'fpn1')
                


class WaitCacheTest(unittest.TestCase):
    """
    Stolen from NTPSec util tests
    """
    def test_wait_cache(self):
        c = tf.Cache

        monodata = []

        def monoclock_jig():
            return monodata.pop(0)

        
        cls = c()
        self.assertEqual(cls._cache, {})
        try:
            monotemp = tf.monoclock
            tf.monoclock = monoclock_jig
            
            monodata = [5, 10, 315, 20]
            cls.set("foo", 42)
            cls.set("bar", 23)
            self.assertEqual(cls._cache, {"foo": (42, 5, 300),
                                          "bar": (23, 10, 300)})
            self.assertEqual(monodata, [315, 20])
            
            result = cls.get("foo")
            self.assertEqual(result, None)
            self.assertEqual(monodata, [20])
            self.assertEqual(cls._cache, {"bar": (23, 10, 300)})
            
            result = cls.get("bar")
            self.assertEqual(result, 23)
            self.assertEqual(monodata, [])
            self.assertEqual(cls._cache, {"bar": (23, 10, 300)})
            
            monodata = [0, 0, 11, 15]
            cls.set("foo", 42, 10)
            cls.set("bar", 23, 20)
            self.assertEqual(cls._cache, {"foo": (42, 0, 10),
                                          "bar": (23, 0, 20)})
            self.assertEqual(monodata, [11, 15])
            
            result = cls.get("foo")
            self.assertEqual(result, None)
            self.assertEqual(monodata, [15])
            self.assertEqual(cls._cache, {"bar": (23, 0, 20)})
            
            result = cls.get("bar")
            self.assertEqual(result, 23)
            self.assertEqual(monodata, [])
            self.assertEqual(cls._cache, {"bar": (23, 0, 20)})
        finally:
            tf.monoclock = monotemp

    def test_monoclock(self):
        a = tf.monoclock()
        b = tf.monoclock()
        self.assertLessEqual(a, b)
        
        
        times = [tf.monoclock() for n in range(100)]
        t1 = times[0]
        for t2 in times[1:]:
            self.assertGreaterEqual(t2, t1, "times=%s" % times)
            t1 = t2

        
        t1 = tf.monoclock()
        time.sleep(0.5)
        t2 = tf.monoclock()
        dt = t2 - t1
        self.assertGreater(t2, t1)
        
        self.assertTrue(0.45 <= dt <= 1.0, dt)

        
        info = time.get_clock_info('monotonic')
        self.assertTrue(info.monotonic)
        self.assertFalse(info.adjustable)


class XformStateDataTest(unittest.TestCase):
    """
    Tests for state data transformation: xform_state_diff()
    """
    def setUp(self):
        super(XformStateDataTest, self).setUp()
        self.one_new = [('fpn1', False)]
        self.old_new = [(('fpn1', True), ('fpn1', False))]
        self.two_new = [('fpn0', True), ('fpn1', True),
                        ('fpn_id0', 'bb8dead3c63cea29'),
                        ('fpn_id1', '7ac4235ec5d3d938')]
        self.none = []

    def test_return_none(self):
        self.assertIsInstance(xform_state_diff(self.none), dict)

    def test_return_old_new(self):
        diff = xform_state_diff(self.old_new)
        self.assertIsInstance(diff, dict)
        self.assertTrue(diff.old_fpn1)
        self.assertFalse(diff.new_fpn1)

    def test_return_one_new(self):
        diff = xform_state_diff(self.one_new)
        self.assertFalse(diff.fpn1)

    def test_return_two_new(self):
        diff = xform_state_diff(self.two_new)
        self.assertTrue(diff.fpn0)
        self.assertEqual(diff.fpn_id0, 'bb8dead3c63cea29')


client = mock_zt_api_client()


def load_ctlr_data():
    nets = []
    for net in ['net1.data', 'net2.data', 'net3.data']:
        _, data = client.load_data(net)
        nets.append(eval(data))

    mbrs = []
    for mbr in ['mbr1net1.data', 'mbr2net1.data', 'mbr2net2.data', 'mbr3net2.data', 'mbr3net3.data']:
        _, data = client.load_data(mbr)
        mbrs.append(eval(data))

    return nets, mbrs


def load_net_trie_data(trie):
    nets, mbrs = load_ctlr_data()
    for net in nets:
        
        net_id = net['id']
        trie[net_id] = net
        for mbr in mbrs:
            mbr_id = mbr['id']
            if net_id == mbr['nwid']:
                trie[net_id + mbr_id] = mbr


def get_state_icon(state):
    """
    Match the state msg and return the icon name.
    """
    state_dict = {
        'CONNECTED': 'network-vpn-symbolic',
        'WAITING': 'network-vpn-acquiring-symbolic',
        'CONFIG': 'network-vpn-no-route-symbolic',
        'ERROR': 'network-error-symbolic',
        'STARTING': 'network-idle-symbolic',
        'UPGRADE': 'network-offline-symbolic',
        'NONE': 'network-offline-symbolic'
    }
    return state_dict.get(state, state_dict['NONE'])


def get_status(filename, n=1):
    """
    Return the last n lines of the status file in a deque
    """
    with open(filename) as f:
        return deque(f, n)


def test_file_is_found():
    """
    Test if we can find the msg_responder daemon.
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = control_daemon('fart')
    assert res is False




def test_check_daemon():
    """
    Test status return from check_daemon().
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = check_daemon()
    
    assert res is None
    res = check_daemon('msg_subscriber.py')
    assert res is None


def test_daemon_can_die():
    """
    Test if we can kill the msg_responder daemon.
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = control_daemon('start')
    assert res.returncode == 0
    assert res.stdout == ''
    
    time.sleep(1)
    pid_file = '/tmp/msg_responder.pid'
    with open(pid_file, 'r') as pf:
        resp_pid = int(pf.read().strip())
    with pytest.raises(SystemExit):
        do_shutdown(pid=resp_pid)


def test_daemon_can_start():
    """
    Test if we can start the msg_responder daemon.
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = control_daemon('start')
    assert res.returncode == 0
    assert res.stdout == ''


def test_daemon_can_stop():
    """
    Test if we can stop the msg_responder daemon.
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = control_daemon('stop')
    assert res.returncode == 0
    assert res.stdout == ''


def test_daemon_has_status():
    """
    Test if we can get status from msg_responder daemon.
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), 'scripts')
    res = control_daemon('status')
    assert res.returncode == 0
    assert 'pidfile' in res.stdout



def test_path_ecxeption():
    """
    Test if we can generate an exception (yes we can, so now we don't
    need to raise it).
    """
    NODE_SETTINGS['home_dir'] = os.path.join(os.getcwd(), '/root')
    res = control_daemon('restart')
    assert not res


def test_get_runtimedir():
    import tempfile

    temp_dir = tempfile.gettempdir()
    NODE_SETTINGS['runas_user'] = False
    res = get_runtimedir()
    assert res == '/run/fpnd' or res == temp_dir
    res = get_runtimedir(user_dirs=True)
    
    assert '/run/user/' in res or 'tmp/portage' in res or res == temp_dir
    NODE_SETTINGS['runas_user'] = True


def test_get_icon_from_state():
    """
    This is really in the gtk indicator source, test it here fr now
    """
    msgs = ['STARTING', 'CONNECTED', 'CONFIG', 'ERROR', 'UPGRADE', 'WAITING', 'NONE', 'FOO']
    for state in msgs:
        res = get_state_icon(state)
        assert 'symbolic' in res


def test_put_state_msg():
    """
    Use get_status() from freepn-gtk3-indicator (replicated above)
    """
    state_path = Path(get_runtimedir(user_dirs=True)).joinpath('fpnd.state')

    msgs = ['STARTING', 'CONNECTED', 'CONFIG', 'ERROR', 'UPGRADE', 'WAITING', 'NONE']
    for msg in msgs:
        put_state_msg(msg)
        status_queue = get_status(str(state_path))
        assert len(list(status_queue)) == 1
        data = status_queue.pop().strip()
        assert data == msg
        assert len(list(status_queue)) == 0

    for msg in msgs:
        put_state_msg(msg)
    status_queue = get_status(str(state_path), 7)
    assert len(list(status_queue)) == 1
    data = status_queue.pop().strip()
    assert data == 'NONE'
    assert len(list(status_queue)) == 0

    state_path.unlink()


def test_put_state_msg_save():
    """
    Same as test_put_state_msg but without cleaning
    """
    state_path = Path(get_runtimedir(user_dirs=True)).joinpath('fpnd.state')

    msgs = ['STARTING', 'CONNECTED', 'CONFIG', 'ERROR', 'UPGRADE', 'WAITING', 'NONE']
    for msg in msgs:
        put_state_msg(msg, clean=False)
        status_queue = get_status(str(state_path))
        assert len(list(status_queue)) == 1
        data = status_queue.pop().strip()
        assert data == msg
        assert len(list(status_queue)) == 0

    for msg in msgs:
        put_state_msg(msg, clean=False)
    status_queue = get_status(str(state_path), 7)
    assert len(list(status_queue)) == 7
    data = status_queue.pop().strip()
    assert data == 'NONE'
    assert len(list(status_queue)) == 6

    state_path.unlink()


def test_state_trie_load_save():
    
    _, fname = create_state_trie()
    trie = load_state_trie(fname)
    trie['f00baf'] = 1
    trie['foobar'] = 2
    trie['baf'] = 3
    trie['fa'] = 4
    trie['Faa'] = 'vasia'
    save_state_trie(trie, fname)
    del trie

    trie2 = load_state_trie(fname)
    assert trie2['f00baf'] == 1
    assert trie2['baf'] == 3
    assert trie2['fa'] == 4
    assert trie2['Faa'] == 'vasia'

    with pytest.raises(KeyError):
        assert trie2['foobar'] == 2


def test_trie_is_empty():
    
    from node_tools import ctlr_data as ct

    res = trie_is_empty(ct.id_trie)
    assert res is True

    ct.id_trie.setdefault(u'f00b', 42)
    with pytest.raises(AssertionError):
        res = trie_is_empty(ct.id_trie)

    ct.id_trie.clear()


def test_is_exit_node():
    NODE_SETTINGS['use_exitnode'].append('beefea68e6')
    res = is_exit_node('beefea68e6')
    assert res is True
    NODE_SETTINGS['use_exitnode'].remove('beefea68e6')
    res = is_exit_node('beefea68e6')
    assert res is False


def test_load_id_from_net_trie():
    from node_tools import ctlr_data as ct

    NODE_SETTINGS['use_exitnode'].append('beefea68e6')
    dead_key = 'dead99dead'

    res = trie_is_empty(ct.net_trie)
    assert res is True

    load_net_trie_data(ct.net_trie)
    assert len(list(ct.net_trie)) == 8

    for net_id in ['beafde52b4296ea5', 'beafde52b4a5f7ba', 'beafde52b4a5e8ab']:
        load_id_trie(ct.net_trie, ct.id_trie, [net_id], [], nw=True)
    for node_id in ['beefea68e6', 'ee2eedb2e1', 'ff2ffdb2e1', dead_key]:
        load_id_trie(ct.net_trie, ct.id_trie, [], [node_id])

    for key in ['beafde52b4296ea5', 'beafde52b4a5f7ba', 'ee2eedb2e1', 'ff2ffdb2e1']:
        links, needs = ct.id_trie[key]
        for item in [links, needs]:
            assert isinstance(item, list)
        assert len(links) == 2
        assert len(needs) == 2

    assert ct.id_trie['beefea68e6'] == (['beafde52b4296ea5'], [False, False])
    assert ct.id_trie['beafde52b4a5f7ba'] == (['ee2eedb2e1', 'ff2ffdb2e1'], [False, False])
    assert ct.id_trie['beafde52b4a5e8ab'] == (['ff2ffdb2e1'], [False, True])

    res = find_exit_net(ct.id_trie)
    assert isinstance(res, list)
    assert res == ['beafde52b4296ea5']
    exit_net = find_exit_net(ct.id_trie)[0]
    assert exit_net == res[0]
    

    node_id = 'beefea68e6'
    with pytest.raises(AssertionError):
        load_id_trie(ct.net_trie, ct.id_trie, [], [node_id], needs=[True])
    with pytest.raises(AssertionError):
        load_id_trie(ct.net_trie, ct.id_trie, [], [node_id, node_id, node_id])
    with pytest.raises(AssertionError):
        load_id_trie(ct.net_trie, ct.id_trie, [], node_id)
    with pytest.raises(AssertionError):
        load_id_trie(ct.net_trie, ct.id_trie, [], [])

    NODE_SETTINGS['use_exitnode'].clear()



def test_find_orphans():
    from node_tools import ctlr_data as ct

    exit_id = 'beefea68e6'
    dead_key = 'dead99dead'
    empty_nets = ['beafde52b4296eee']

    res = find_orphans(ct.net_trie, ct.id_trie)
    assert res == ([('beafde52b4296ea5', exit_id)], [dead_key])

    NODE_SETTINGS['use_exitnode'].append(exit_id)
    res = find_orphans(ct.net_trie, ct.id_trie)
    assert res == ([], [dead_key])

    del ct.id_trie[dead_key]
    load_id_trie(ct.net_trie, ct.id_trie, empty_nets, [], nw=True)
    res = find_orphans(ct.net_trie, ct.id_trie)
    assert res == (empty_nets, [])

    NODE_SETTINGS['use_exitnode'].clear()


def test_get_invalid_net_id():
    from node_tools import ctlr_data as ct

    trie = ct.net_trie
    node_id = 'ee2eedb2e1'
    exit_id = 'beefea68e6'
    tail_id = 'ff2ffdb2e1'

    res = get_invalid_net_id(trie, node_id)
    assert res == 'beafde52b4296ea5'


def test_get_neighbor_ids():
    from node_tools import ctlr_data as ct

    trie = ct.net_trie
    node_id = 'ee2eedb2e1'
    exit_id = 'beefea68e6'
    tail_id = 'ff2ffdb2e1'

    res = get_neighbor_ids(trie, node_id)
    assert res == ('beafde52b4a5f7ba', 'beafde52b4296ea5', 'ff2ffdb2e1', 'beefea68e6')

    res = get_neighbor_ids(trie, tail_id)
    assert res == ('beafde52b4a5e8ab', 'beafde52b4a5f7ba', None, 'ee2eedb2e1')

    with pytest.raises(AssertionError):
        res = get_neighbor_ids(trie, exit_id)

    NODE_SETTINGS['use_exitnode'].append(exit_id)
    res = get_neighbor_ids(trie, exit_id)
    assert res == ('beafde52b4296ea5', None, 'ee2eedb2e1', None)

    NODE_SETTINGS['use_exitnode'].clear()


def test_get_bootstrap_list():
    from node_tools import ctlr_data as ct

    node_id = 'ee2eedb2e1'
    exit_id = 'beefea68e6'
    tail_id = 'ff2ffdb2e1'
    NODE_SETTINGS['use_exitnode'].append(exit_id)

    boot_list = get_bootstrap_list(ct.net_trie, ct.id_trie)
    assert exit_id not in boot_list
    assert node_id == boot_list[-1]
    assert tail_id == boot_list[0]
    
    NODE_SETTINGS['use_exitnode'].clear()


def test_get_target_node_id():
    from node_tools import ctlr_data as ct

    NODE_SETTINGS['use_exitnode'].append('beefea68e6')
    node_list = get_active_nodes(ct.id_trie)
    assert 'beefea68e6' not in node_list
    boot_list = ['deadbeef01', 'deadbeef02', 'deadbeef03']

    res = get_target_node_id(node_list, boot_list)
    assert res in ['ee2eedb2e1', 'ff2ffdb2e1']
    NODE_SETTINGS['use_exitnode'].clear()



def test_get_wedged_node_id():
    from node_tools import ctlr_data as ct
    from node_tools import state_data as st

    node_id = 'ee2eedb2e1'
    exit_id = 'beefea68e6'
    tail_id = 'ff2ffdb2e1'

    res = get_wedged_node_id(ct.net_trie, node_id)
    assert res == exit_id

    res = get_wedged_node_id(ct.net_trie, tail_id)
    assert res == node_id

    st.wait_cache.set(exit_id, True, 1)
    res = get_wedged_node_id(ct.net_trie, node_id)
    assert res is None
    time.sleep(2)
    res = get_wedged_node_id(ct.net_trie, node_id)
    assert res == exit_id


def test_handle_wedged_nodes():
    import diskcache as dc
    from node_tools import ctlr_data as ct

    trie = ct.net_trie
    off_q = dc.Deque(directory='/tmp/test-oq')
    wdg_q = dc.Deque(directory='/tmp/test-wq')
    node_id = 'ee2eedb2e1'
    exit_id = 'beefea68e6'
    tail_id = 'ff2ffdb2e1'

    wdg_q.append(node_id)
    wdg_q.append(node_id)
    handle_wedged_nodes(trie, wdg_q, off_q)
    assert list(wdg_q) == []
    assert list(off_q) == ['beefea68e6']

    wdg_q.append(tail_id)
    wdg_q.append(tail_id)
    handle_wedged_nodes(trie, wdg_q, off_q)
    assert list(wdg_q) == []
    assert list(off_q) == ['beefea68e6', 'ee2eedb2e1']

    wdg_q.append(exit_id)
    wdg_q.append(exit_id)
    with pytest.raises(AssertionError):
        handle_wedged_nodes(trie, wdg_q, off_q)


def test_cleanup_state_tries():
    from node_tools import ctlr_data as ct

    ct.id_trie.clear()
    ct.net_trie.clear()
    load_net_trie_data(ct.net_trie)

    for net_id in ['beafde52b4296ea5', 'beafde52b4a5f7ba', 'beafde52b4a5e8ab']:
        load_id_trie(ct.net_trie, ct.id_trie, [net_id], [], nw=True)
    for node_id in ['beefea68e6', 'ee2eedb2e1', 'ff2ffdb2e1']:
        load_id_trie(ct.net_trie, ct.id_trie, [], [node_id])

    net1 = 'beafde52b4296ea5'
    node1 = 'beefea68e6'
    net2 = 'beafde52b4a5f7ba'
    node2 = 'ee2eedb2e1'
    net3 = 'beafde52b4a5e8ab'
    node3 = 'ff2ffdb2e1'

    assert len(list(ct.net_trie)) == 8
    res = get_active_nodes(ct.id_trie)
    assert len(res) == 3
    assert res == ['beefea68e6', 'ee2eedb2e1', 'ff2ffdb2e1']

    cleanup_state_tries(ct.net_trie, ct.id_trie, net2, node3, mbr_only=True)

    assert len(list(ct.net_trie)) == 7
    assert node3 not in ct.id_trie
    res = get_active_nodes(ct.id_trie)
    assert len(res) == 2
    assert res == ['beefea68e6', 'ee2eedb2e1']

    cleanup_state_tries(ct.net_trie, ct.id_trie, net3, node3)

    assert len(list(ct.net_trie)) == 5
    assert len(list(ct.id_trie)) == 4
    for key in ct.net_trie.keys():
        assert net3 not in key
        assert node3 not in key
    for key in ct.id_trie.keys():
        assert net3 not in key
        assert node3 not in key

    cleanup_state_tries(ct.net_trie, ct.id_trie, net1, node2, mbr_only=True)
    cleanup_state_tries(ct.net_trie, ct.id_trie, net2, node2)
    for key in ct.net_trie.keys():
        assert net2 not in key
        assert node2 not in key
        assert net1 in key
    for key in ct.id_trie.keys():
        assert net2 not in key
        assert node2 not in key
    cleanup_state_tries(ct.net_trie, ct.id_trie, net1, node1)
    assert node1 not in ct.id_trie


def test_get_dangling_net_data():
    from node_tools import ctlr_data as ct

    load_net_trie_data(ct.net_trie)

    net_id = 'beafde52b4a5e8ab'
    res = get_dangling_net_data(ct.net_trie, net_id)
    assert isinstance(res, dict)
    assert res.host == ['172.16.1.150/30']


def test_set_network_cfg():
    host_cfg = ['172.16.0.126/30']
    res = set_network_cfg(host_cfg)
    assert isinstance(res, dict)
    assert res.ipAssignments == ['172.16.0.126/30']
    assert res.authorized is True


def test_unset_network_cfg():
    res = unset_network_cfg()
    assert isinstance(res, dict)
    assert res.ipAssignments == []
    assert res.authorized is False


def test_name_generator():
    name = name_generator()
    assert len(name) == 21
    assert name.isprintable()


def test_name_generator_chars():
    name = name_generator(size=15, char_set=string.hexdigits)
    assert len(name) == 31
    str1, str2 = name.split(sep='_', maxsplit=-1)
    assert all(c in string.hexdigits for c in str1)
    assert all(c in string.hexdigits for c in str2)


def test_set_initial_role():
    set_initial_role()


def test_send_cfg_handler():
    send_cfg_handler()


def test_startup_handlers():
    startup_handlers()


def test_api_warning_msg():
    with pytest.warns(UserWarning):
        warnings.warn("Cannot connect to ZeroTier API", UserWarning)


def test_enodata_warning_msg():
    with pytest.warns(UserWarning):
        warnings.warn("Cache empty and API returned ENODATA", UserWarning)


def test_aging_not_available_warning_msg():
    with pytest.warns(UserWarning):
        warnings.warn("Cache aging not available", UserWarning)


def test_gen_netobj_queue():
    import diskcache as dc

    netobj_q = dc.Deque(directory='/tmp/test-oq')
    netobj_q.clear()

    gen_netobj_queue(netobj_q, ipnet='192.168.0.0/24')
    assert len(netobj_q) == 64
    net = netobj_q.popleft()
    assert isinstance(net, ipaddress.IPv4Network)
    assert len(list(net)) == 4
    assert len(list(net.hosts())) == 2
    gen_netobj_queue(netobj_q)
    assert len(netobj_q) == 63


def test_handle_net_cfg():
    import diskcache as dc

    netobj_q = dc.Deque(directory='/tmp/test-oq')

    net1, mbr1, gw1 = handle_net_cfg(netobj_q)
    for fragment in [net1, mbr1, gw1]:
        assert isinstance(fragment, AttrDict)

    net2, mbr2, gw2 = handle_net_cfg(netobj_q)
    for fragment in [net2, mbr2, gw2]:
        assert isinstance(fragment, AttrDict)

    assert mbr1 != mbr2
    assert mbr1.ipAssignments == ['192.168.0.6/30']
    assert mbr1.authorized is True
    res = handle_net_cfg(netobj_q)
    assert len(res) is 3
    
    netobj_q.clear()
