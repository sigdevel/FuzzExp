
import json
from unittest import TestCase

from pcs import settings
from pcs.common import reports
from pcs.common.reports import codes as report_codes
from pcs.lib.commands.sbd import (
    ALLOWED_SBD_OPTION_LIST,
    TIMEOUT_ACTION_ALLOWED_VALUE_LIST,
    enable_sbd,
)
from pcs.lib.corosync.config_parser import Parser

from pcs_test.tools import fixture
from pcs_test.tools.command_env import get_env_tools
from pcs_test.tools.misc import (
    get_test_resource,
    outdent,
)


def _get_corosync_conf_text_with_atb(orig_cfg_file):
    with open(get_test_resource(orig_cfg_file), "rb") as a_file:
        corosync_conf = Parser.parse(a_file.read())
    for quorum in corosync_conf.get_sections(name="quorum"):
        quorum.del_attributes_by_name("two_node")
        quorum.set_attribute("auto_tie_breaker", 1)
    return corosync_conf.export()


def _sbd_enable_successful_report_list_fixture(
    online_node_list, skipped_offline_node_list=(), atb_set=False
):
    report_list = (
        [
            fixture.warn(report_codes.OMITTING_NODE, node=node)
            for node in skipped_offline_node_list
        ]
        + [fixture.info(report_codes.SBD_CHECK_STARTED)]
        + [
            fixture.info(report_codes.SBD_CHECK_SUCCESS, node=node)
            for node in online_node_list
        ]
    )
    if atb_set:
        report_list.append(
            fixture.warn(
                report_codes.COROSYNC_QUORUM_ATB_WILL_BE_ENABLED_DUE_TO_SBD
            )
        )
    return (
        report_list
        + [fixture.info(report_codes.SBD_CONFIG_DISTRIBUTION_STARTED)]
        + [
            fixture.info(report_codes.SBD_CONFIG_ACCEPTED_BY_NODE, node=node)
            for node in online_node_list
        ]
        + [
            fixture.info(
                reports.codes.SERVICE_ACTION_STARTED,
                action=reports.const.SERVICE_ACTION_ENABLE,
                service="sbd",
                instance="",
            )
        ]
        + [
            fixture.info(
                reports.codes.SERVICE_ACTION_SUCCEEDED,
                action=reports.const.SERVICE_ACTION_ENABLE,
                service="sbd",
                node=node,
                instance="",
            )
            for node in online_node_list
        ]
        + [fixture.warn(report_codes.CLUSTER_RESTART_REQUIRED_TO_APPLY_CHANGES)]
    )


class OddNumOfNodesSuccess(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync-3nodes.conf"
        self.node_list = ["rh7-1", "rh7-2", "rh7-3"]
        self.sbd_options = {
            "SBD_WATCHDOG_TIMEOUT": "10",
            "SBD_STARTMODE": "clean",
            "SBD_TIMEOUT_ACTION": "flush,off",
        }
        self.sbd_config_template = outdent(
            """\
        
        SBD_DELAY_START=no
        {devices}SBD_OPTS="-n {node_name}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=clean
        SBD_TIMEOUT_ACTION=flush,off
        SBD_WATCHDOG_DEV={watchdog}
        SBD_WATCHDOG_TIMEOUT=10
        """
        )
        self.watchdog_dict = {
            node: "/dev/watchdog-{0}".format(node) for node in self.node_list
        }
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(node_labels=self.node_list)

    def test_with_devices(self):
        def config_generator(node):
            return self.sbd_config_template.format(
                node_name=node,
                watchdog=self.watchdog_dict[node],
                devices='SBD_DEVICE="{0}"\n'.format(
                    ";".join(device_dict[node])
                ),
            )

        device_dict = {
            node: ["/dev/{0}-sbd{1}".format(node, j) for j in range(i)]
            for i, node in enumerate(self.node_list, start=1)
        }
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    node, self.watchdog_dict[node], device_dict[node]
                )
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=None,
            watchdog_dict=self.watchdog_dict,
            sbd_options=self.sbd_options,
            default_device_list=[],
            node_device_dict=device_dict,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )

    def test_no_device(self):
        def config_generator(node):
            return self.sbd_config_template.format(
                node_name=node,
                watchdog=self.watchdog_dict[node],
                devices="",
            )

        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    node, self.watchdog_dict[node], []
                )
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=None,
            watchdog_dict=self.watchdog_dict,
            sbd_options=self.sbd_options,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )


class OddNumOfNodesDefaultsSuccess(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync-3nodes.conf"
        self.node_list = ["rh7-1", "rh7-2", "rh7-3"]
        self.sbd_config_template = outdent(
            """\
        
        SBD_DELAY_START=no
        {devices}SBD_OPTS="-n {node_name}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        )
        self.watchdog = "/dev/watchdog"
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(node_labels=self.node_list)

    def test_with_device(self):
        def config_generator(node):
            return self.sbd_config_template.format(
                node_name=node,
                devices='SBD_DEVICE="{0}"\n'.format(";".join(device_list)),
            )

        device_list = ["/dev/sdb"]

        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    node, self.watchdog, device_list
                )
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
            default_device_list=device_list,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )

    def test_no_device(self):
        def config_generator(node):
            return self.sbd_config_template.format(node_name=node, devices="")

        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )


class WatchdogValidations(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync-3nodes.conf"
        self.node_list = ["rh7-1", "rh7-2", "rh7-3"]
        self.sbd_config_template = outdent(
            """\
        
        SBD_DELAY_START=no
        SBD_OPTS="-n {node_name}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        )
        self.watchdog = "/dev/watchdog"
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(node_labels=self.node_list)

    def test_watchdog_not_supported(self):
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list[:2]
            ]
            + [
                dict(
                    label=self.node_list[2],
                    output=json.dumps(
                        {
                            "sbd": {
                                "installed": True,
                            },
                            "watchdog": {
                                "exist": True,
                                "path": self.watchdog,
                                "is_supported": False,
                            },
                            "device_list": [],
                        }
                    ),
                    param_list=[
                        ("watchdog", self.watchdog),
                        ("device_list", "[]"),
                    ],
                )
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [fixture.info(report_codes.SBD_CHECK_STARTED)]
            + [
                fixture.error(
                    report_codes.SBD_WATCHDOG_NOT_SUPPORTED,
                    node=self.node_list[2],
                    watchdog=self.watchdog,
                )
            ]
            + [
                fixture.info(report_codes.SBD_CHECK_SUCCESS, node=node)
                for node in self.node_list[:2]
            ]
        )

    def test_no_watchdog_validation(self):
        def config_generator(node):
            return self.sbd_config_template.format(node_name=node)

        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, "", [])
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
            no_watchdog_validation=True,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
            + [fixture.warn(report_codes.SBD_WATCHDOG_VALIDATION_INACTIVE)]
        )


class EvenNumOfNodes(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync.conf"
        self.node_list = ["rh7-1", "rh7-2"]
        self.sbd_config_template = outdent(
            """\
        
        SBD_DELAY_START=no
        {devices}SBD_OPTS="-n {node_name}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        )
        self.watchdog = "/dev/watchdog"
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(node_labels=self.node_list)

    def test_with_device(self):
        def config_generator(node):
            return self.sbd_config_template.format(
                node_name=node,
                devices='SBD_DEVICE="{0}"\n'.format(";".join(device_list)),
            )

        device_list = ["/dev/sdb"]
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    node, self.watchdog, device_list
                )
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
            default_device_list=device_list,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )

    def test_no_device(self):
        def config_generator(node):
            return self.sbd_config_template.format(node_name=node, devices="")

        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list
            ]
        )
        self.config.env.push_corosync_conf(
            corosync_conf_text=_get_corosync_conf_text_with_atb(
                self.corosync_conf_name
            ),
            need_stopped_cluster=True,
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list,
                atb_set=True,
            )
        )

    def test_no_device_auto_tie_breaker_enabled(self):
        def config_generator(node):
            return self.sbd_config_template.format(node_name=node, devices="")

        self.config.corosync_conf.load(
            filename=self.corosync_conf_name,
            auto_tie_breaker=True,
            instead="corosync_conf.load",
        )
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )

    def test_no_device_with_qdevice(self):
        def config_generator(node):
            return self.sbd_config_template.format(node_name=node, devices="")

        self.config.corosync_conf.load(
            filename="corosync-qdevice.conf",
            instead="corosync_conf.load",
        )
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(self.node_list)
        )


class OfflineNodes(TestCase):
    
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync.conf"
        node_list = ["rh7-1", "rh7-2"]
        self.online_node_list = node_list[:-1]
        self.offline_node_list = node_list[-1:]
        self.watchdog = "/dev/watchdog"
        self.err_msg = "error msg"
        self.sbd_config_generator = outdent(
            """\
        
        SBD_DELAY_START=no
        SBD_OPTS="-n {0}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        ).format
        self.offline_communication_list = [
            dict(label=node) for node in self.online_node_list
        ] + [
            dict(
                label=node,
                was_connected=False,
                errno=1,
                error_msg=self.err_msg,
            )
            for node in self.offline_node_list
        ]
        self.config.env.set_known_nodes(node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(
            communication_list=self.offline_communication_list
        )

    def test_no_ignore_offline_nodes(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=None,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    force_code=report_codes.SKIP_OFFLINE_NODES,
                    node=node,
                    command="remote/check_auth",
                    reason=self.err_msg,
                )
                for node in self.offline_node_list
            ]
        )

    def test_ignore_offline_nodes(self):
        self.config.corosync_conf.load(
            filename="corosync-qdevice.conf",
            instead="corosync_conf.load",
        )
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.online_node_list
            ]
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=self.sbd_config_generator,
            node_labels=self.online_node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.online_node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.online_node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=None,
            watchdog_dict={},
            sbd_options={},
            ignore_offline_nodes=True,
        )
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.OMITTING_NODE,
                    node=node,
                )
                for node in self.offline_node_list
            ]
            + _sbd_enable_successful_report_list_fixture(self.online_node_list)
        )

    def test_ignore_offline_nodes_atb_needed(self):
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.online_node_list
            ]
        )
        self.config.env.push_corosync_conf(
            corosync_conf_text=_get_corosync_conf_text_with_atb(
                self.corosync_conf_name
            ),
            skip_offline_targets=True,
            need_stopped_cluster=True,
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=self.sbd_config_generator,
            node_labels=self.online_node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.online_node_list[0]]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.online_node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=None,
            watchdog_dict={},
            sbd_options={},
            ignore_offline_nodes=True,
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.online_node_list,
                skipped_offline_node_list=self.offline_node_list,
                atb_set=True,
            )
        )



class Validations(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync.conf"
        self.node_list = ["rh7-1", "rh7-2"]
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)

    def test_non_existing_node_in_watchdogs(self):
        unknown_node = "unknown_node"
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=None,
                watchdog_dict={
                    node: "/dev/watchdog"
                    for node in (self.node_list + [unknown_node])
                },
                sbd_options={},
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_NOT_FOUND,
                    node=unknown_node,
                    searched_types=[],
                ),
            ]
        )

    def test_non_existing_node_in_devices(self):
        unknown_node = "unknown_node"
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={},
                default_device_list="/device",
                node_device_dict={
                    node: ["/device"]
                    for node in (self.node_list + [unknown_node])
                },
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_NOT_FOUND,
                    node=unknown_node,
                    searched_types=[],
                ),
            ]
        )

    def test_device_not_abs_path(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={},
                default_device_list=["device1"],
                node_device_dict={self.node_list[0]: ["device2"]},
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.SBD_DEVICE_PATH_NOT_ABSOLUTE,
                    node=node,
                    device=dev,
                )
                for node, dev in [
                    (self.node_list[0], "device2"),
                    (self.node_list[1], "device1"),
                ]
            ]
        )

    def test_no_device_for_node(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={},
                default_device_list=[],
                node_device_dict={self.node_list[0]: ["/dev/device1"]},
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.SBD_NO_DEVICE_FOR_NODE,
                    node=self.node_list[1],
                    sbd_enabled_in_cluster=False,
                ),
            ]
        )

    def test_too_many_devices(self):
        max_dev_num = settings.sbd_max_device_num
        dev_list = ["/dev/dev{0}".format(i) for i in range(max_dev_num + 1)]
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={},
                default_device_list=["/dev/dev1"],
                node_device_dict={self.node_list[0]: dev_list},
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.SBD_TOO_MANY_DEVICES_FOR_NODE,
                    node=self.node_list[0],
                    device_list=dev_list,
                    max_devices=max_dev_num,
                ),
            ]
        )

    def test_invalid_opt_values(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={
                    "SBD_TIMEOUT_ACTION": "noflush,flush",
                },
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.INVALID_OPTION_VALUE,
                    force_code=report_codes.FORCE,
                    option_name="SBD_TIMEOUT_ACTION",
                    option_value="noflush,flush",
                    allowed_values=TIMEOUT_ACTION_ALLOWED_VALUE_LIST,
                    cannot_be_empty=False,
                    forbidden_characters=None,
                ),
            ]
        )

    def test_invalid_opt_values_forced(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={
                    "SBD_TIMEOUT_ACTION": "noflush,flush",
                    "UNKNOWN_OPT1": 1,
                },
                allow_invalid_option_values=True,
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.INVALID_OPTION_VALUE,
                    option_name="SBD_TIMEOUT_ACTION",
                    option_value="noflush,flush",
                    allowed_values=TIMEOUT_ACTION_ALLOWED_VALUE_LIST,
                    cannot_be_empty=False,
                    forbidden_characters=None,
                ),
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["UNKNOWN_OPT1"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                    force_code=report_codes.FORCE,
                ),
            ]
        )

    def test_unknown_sbd_opts(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={
                    "UNKNOWN_OPT1": 1,
                    "SBD_STARTMODE": "clean",
                    "UNKNOWN_OPT2": "val",
                    "SBD_WATCHDOG_DEV": "dev",
                },
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["UNKNOWN_OPT1", "UNKNOWN_OPT2"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                    force_code=report_codes.FORCE,
                ),
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["SBD_WATCHDOG_DEV"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                ),
            ]
        )

    def test_unknown_sbd_opts_allowed(self):
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog",
                watchdog_dict={},
                sbd_options={
                    "UNKNOWN_OPT1": 1,
                    "SBD_STARTMODE": "clean",
                    "UNKNOWN_OPT2": "val",
                    "SBD_WATCHDOG_DEV": "dev",
                },
                allow_unknown_opts=True,
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.INVALID_OPTIONS,
                    option_names=["UNKNOWN_OPT1", "UNKNOWN_OPT2"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                ),
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["SBD_WATCHDOG_DEV"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                ),
            ]
        )

    def test_sbd_not_installed(self):
        watchdog = "/dev/watchdog"
        self.config.http.host.check_auth(node_labels=self.node_list)
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    self.node_list[0], watchdog, []
                ),
                dict(
                    label=self.node_list[1],
                    output=json.dumps(
                        {
                            "sbd": {
                                "installed": False,
                            },
                            "watchdog": {
                                "exist": True,
                                "path": watchdog,
                            },
                            "device_list": [],
                        }
                    ),
                    param_list=[
                        ("watchdog", watchdog),
                        ("device_list", "[]"),
                    ],
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [fixture.info(report_codes.SBD_CHECK_STARTED)]
            + [
                fixture.error(
                    report_codes.SERVICE_NOT_INSTALLED,
                    node=self.node_list[1],
                    service_list=["sbd"],
                )
            ]
            + [
                fixture.info(
                    report_codes.SBD_CHECK_SUCCESS, node=self.node_list[0]
                )
            ]
        )

    def test_watchdog_not_found(self):
        watchdog = "/dev/watchdog"
        self.config.http.host.check_auth(node_labels=self.node_list)
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    self.node_list[0], watchdog, []
                ),
                dict(
                    label=self.node_list[1],
                    output=json.dumps(
                        {
                            "sbd": {
                                "installed": True,
                            },
                            "watchdog": {
                                "exist": False,
                                "path": watchdog,
                            },
                            "device_list": [],
                        }
                    ),
                    param_list=[
                        ("watchdog", watchdog),
                        ("device_list", "[]"),
                    ],
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [fixture.info(report_codes.SBD_CHECK_STARTED)]
            + [
                fixture.error(
                    report_codes.WATCHDOG_NOT_FOUND,
                    node=self.node_list[1],
                    watchdog=watchdog,
                )
            ]
            + [
                fixture.info(
                    report_codes.SBD_CHECK_SUCCESS, node=self.node_list[0]
                )
            ]
        )

    def test_device_not_exists_not_block_device(self):
        watchdog = "/dev/watchdog"
        device_list = ["/dev/dev0", "/dev/dev1"]
        self.config.http.host.check_auth(node_labels=self.node_list)
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(
                    self.node_list[0], watchdog, device_list
                ),
                dict(
                    label=self.node_list[1],
                    output=json.dumps(
                        {
                            "sbd": {
                                "installed": True,
                            },
                            "watchdog": {
                                "exist": True,
                                "path": watchdog,
                            },
                            "device_list": [
                                dict(
                                    path=device_list[0],
                                    exist=False,
                                    block_device=False,
                                ),
                                dict(
                                    path=device_list[1],
                                    exist=True,
                                    block_device=False,
                                ),
                            ],
                        }
                    ),
                    param_list=[
                        ("watchdog", watchdog),
                        ("device_list", json.dumps(device_list)),
                    ],
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=watchdog,
                watchdog_dict={},
                sbd_options={},
                default_device_list=device_list,
            ),
            [],
        )
        self.env_assist.assert_reports(
            [fixture.info(report_codes.SBD_CHECK_STARTED)]
            + [
                fixture.error(
                    report_codes.SBD_DEVICE_DOES_NOT_EXIST,
                    node=self.node_list[1],
                    device=device_list[0],
                ),
                fixture.error(
                    report_codes.SBD_DEVICE_IS_NOT_BLOCK_DEVICE,
                    node=self.node_list[1],
                    device=device_list[1],
                ),
            ]
            + [
                fixture.info(
                    report_codes.SBD_CHECK_SUCCESS, node=self.node_list[0]
                )
            ]
        )

    def test_multiple_validation_failures(self):
        unknown_node_list = ["unknown_node{0}".format(i) for i in range(2)]
        max_dev_num = settings.sbd_max_device_num
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog="/dev/watchdog1",
                watchdog_dict={
                    unknown_node_list[0]: "/dev/watchdog",
                    self.node_list[0]: "",
                },
                sbd_options={
                    "UNKNOWN_OPT1": 1,
                    "SBD_STARTMODE": "clean",
                    "UNKNOWN_OPT2": "val",
                    "SBD_WATCHDOG_DEV": "dev",
                },
                default_device_list=[],
                node_device_dict={
                    self.node_list[0]: ["/dev0", "/dev1", "/dev2", "dev"],
                    unknown_node_list[0]: ["/dev/device0"],
                    unknown_node_list[1]: ["/dev/device0"],
                },
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_NOT_FOUND,
                    node=node,
                    searched_types=[],
                )
                for node in unknown_node_list
            ]
            + [
                fixture.error(report_codes.WATCHDOG_INVALID, watchdog=""),
                fixture.error(
                    report_codes.SBD_NO_DEVICE_FOR_NODE,
                    node=self.node_list[1],
                    sbd_enabled_in_cluster=False,
                ),
                fixture.error(
                    report_codes.SBD_TOO_MANY_DEVICES_FOR_NODE,
                    node=self.node_list[0],
                    device_list=["/dev0", "/dev1", "/dev2", "dev"],
                    max_devices=max_dev_num,
                ),
                fixture.error(
                    report_codes.SBD_DEVICE_PATH_NOT_ABSOLUTE,
                    device="dev",
                    node="rh7-1",
                ),
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["SBD_WATCHDOG_DEV"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                ),
                fixture.error(
                    report_codes.INVALID_OPTIONS,
                    option_names=["UNKNOWN_OPT1", "UNKNOWN_OPT2"],
                    option_type=None,
                    allowed=sorted(ALLOWED_SBD_OPTION_LIST),
                    allowed_patterns=[],
                    force_code=report_codes.FORCE,
                ),
            ]
        )


class FailureHandling(TestCase):
    
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.corosync_conf_name = "corosync.conf"
        self.node_list = ["rh7-1", "rh7-2"]
        self.sbd_config_generator = outdent(
            """\
        
        SBD_DELAY_START=no
        SBD_OPTS="-n {0}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        ).format
        self.watchdog = "/dev/watchdog"
        self.reason = "failure reason"
        self.communication_list_failure = [
            dict(
                label=self.node_list[0],
                response_code=400,
                output=self.reason,
            ),
            dict(
                label=self.node_list[1],
            ),
        ]
        self.communication_list_not_connected = [
            dict(
                label=self.node_list[0],
                errno=1,
                error_msg=self.reason,
                was_connected=False,
            ),
            dict(
                label=self.node_list[1],
            ),
        ]
        self.config.env.set_known_nodes(self.node_list)
        self.config.corosync_conf.load(filename=self.corosync_conf_name)
        self.config.http.host.check_auth(node_labels=self.node_list)
        self.config.http.sbd.check_sbd(
            communication_list=[
                fixture.check_sbd_comm_success_fixture(node, self.watchdog, [])
                for node in self.node_list
            ]
        )
        self.config.env.push_corosync_conf(
            corosync_conf_text=_get_corosync_conf_text_with_atb(
                self.corosync_conf_name
            ),
            need_stopped_cluster=True,
        )
        self.config.http.sbd.set_sbd_config(
            config_generator=self.sbd_config_generator,
            node_labels=self.node_list,
        )
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            node_labels=[self.node_list[0]]
        )

    def _remove_calls(self, count):
        for name in self.config.calls.names[-count:]:
            self.config.calls.remove(name)

    def test_enable_failed(self):
        self.config.http.sbd.enable_sbd(
            communication_list=self.communication_list_failure
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )[:-3]
            + [
                fixture.info(
                    reports.codes.SERVICE_ACTION_SUCCEEDED,
                    action=reports.const.SERVICE_ACTION_ENABLE,
                    service="sbd",
                    node=self.node_list[1],
                    instance="",
                ),
                fixture.error(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/sbd_enable",
                ),
            ]
        )

    def test_enable_not_connected(self):
        self.config.http.sbd.enable_sbd(
            communication_list=self.communication_list_not_connected
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )[:-3]
            + [
                fixture.info(
                    reports.codes.SERVICE_ACTION_SUCCEEDED,
                    action=reports.const.SERVICE_ACTION_ENABLE,
                    service="sbd",
                    node=self.node_list[1],
                    instance="",
                ),
                fixture.error(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/sbd_enable",
                ),
            ]
        )

    def test_removing_stonith_wd_timeout_failure(self):
        self._remove_calls(2)
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            communication_list=[
                self.communication_list_failure[:1],
                [dict(label=self.node_list[1])],
            ]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )
            + [
                fixture.warn(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/remove_stonith_watchdog_timeout",
                )
            ]
        )

    def test_removing_stonith_wd_timeout_not_connected(self):
        self._remove_calls(2)
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            communication_list=[
                self.communication_list_not_connected[:1],
                [dict(label=self.node_list[1])],
            ]
        )
        self.config.http.sbd.enable_sbd(node_labels=self.node_list)
        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )
            + [
                fixture.warn(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/remove_stonith_watchdog_timeout",
                )
            ]
        )

    def test_removing_stonith_wd_timeout_complete_failure(self):
        self._remove_calls(2)
        self.config.http.pcmk.remove_stonith_watchdog_timeout(
            communication_list=[
                self.communication_list_not_connected[:1],
                [
                    dict(
                        label=self.node_list[1],
                        response_code=400,
                        output=self.reason,
                    )
                ],
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )[:-4]
            + [
                fixture.warn(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/remove_stonith_watchdog_timeout",
                ),
                fixture.warn(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[1],
                    reason=self.reason,
                    command="remote/remove_stonith_watchdog_timeout",
                ),
                fixture.error(
                    report_codes.UNABLE_TO_PERFORM_OPERATION_ON_ANY_NODE,
                ),
            ]
        )

    def test_set_sbd_config_failure(self):
        self._remove_calls(4)
        self.config.http.sbd.set_sbd_config(
            communication_list=[
                dict(
                    label=self.node_list[0],
                    param_list=[
                        ("config", self.sbd_config_generator(self.node_list[0]))
                    ],
                    response_code=400,
                    output=self.reason,
                ),
                dict(
                    label=self.node_list[1],
                    param_list=[
                        ("config", self.sbd_config_generator(self.node_list[1]))
                    ],
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )[:-6]
            + [
                fixture.error(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/set_sbd_config",
                ),
                fixture.info(
                    report_codes.SBD_CONFIG_ACCEPTED_BY_NODE,
                    node=self.node_list[1],
                ),
            ]
        )

    def test_set_corosync_conf_failed(self):
        self._remove_calls(5)
        self.config.env.push_corosync_conf(
            corosync_conf_text=_get_corosync_conf_text_with_atb(
                self.corosync_conf_name
            ),
            raises=True,
            need_stopped_cluster=True,
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            _sbd_enable_successful_report_list_fixture(
                self.node_list, atb_set=True
            )[:-7]
        )

    def test_check_sbd_invalid_data_format(self):
        self._remove_calls(7)
        self.config.http.sbd.check_sbd(
            communication_list=[
                dict(
                    label=self.node_list[0],
                    param_list=[
                        ("watchdog", self.watchdog),
                        ("device_list", "[]"),
                    ],
                    output="{}",
                ),
                dict(
                    label=self.node_list[1],
                    param_list=[
                        ("watchdog", self.watchdog),
                        ("device_list", "[]"),
                    ],
                    output="not JSON",
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [fixture.info(report_codes.SBD_CHECK_STARTED)]
            + [
                fixture.error(report_codes.INVALID_RESPONSE_FORMAT, node=node)
                for node in self.node_list
            ]
        )

    def test_check_sbd_failure(self):
        self._remove_calls(7)
        self.config.http.sbd.check_sbd(
            communication_list=[
                dict(
                    label=self.node_list[0],
                    param_list=[
                        ("watchdog", self.watchdog),
                        ("device_list", "[]"),
                    ],
                    response_code=400,
                    output=self.reason,
                ),
                fixture.check_sbd_comm_success_fixture(
                    self.node_list[1], self.watchdog, []
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [
                fixture.info(report_codes.SBD_CHECK_STARTED),
                fixture.error(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/check_sbd",
                ),
                fixture.info(
                    report_codes.SBD_CHECK_SUCCESS, node=self.node_list[1]
                ),
            ]
        )

    def test_check_sbd_not_connected(self):
        self._remove_calls(7)
        self.config.http.sbd.check_sbd(
            communication_list=[
                dict(
                    label=self.node_list[0],
                    param_list=[
                        ("watchdog", self.watchdog),
                        ("device_list", "[]"),
                    ],
                    errno=1,
                    error_msg=self.reason,
                    was_connected=False,
                ),
                fixture.check_sbd_comm_success_fixture(
                    self.node_list[1], self.watchdog, []
                ),
            ]
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [
                fixture.info(report_codes.SBD_CHECK_STARTED),
                fixture.error(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/check_sbd",
                ),
                fixture.info(
                    report_codes.SBD_CHECK_SUCCESS, node=self.node_list[1]
                ),
            ]
        )

    def test_get_online_targets_failed(self):
        self._remove_calls(9)
        self.config.http.host.check_auth(
            communication_list=self.communication_list_failure
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_COMMUNICATION_COMMAND_UNSUCCESSFUL,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/check_auth",
                )
            ]
        )

    def test_get_online_targets_not_connected(self):
        self._remove_calls(9)
        self.config.http.host.check_auth(
            communication_list=self.communication_list_not_connected
        )
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            ),
            [],
        )
        self.env_assist.assert_reports(
            [
                fixture.error(
                    report_codes.NODE_COMMUNICATION_ERROR_UNABLE_TO_CONNECT,
                    node=self.node_list[0],
                    reason=self.reason,
                    command="remote/check_auth",
                    force_code=report_codes.SKIP_OFFLINE_NODES,
                )
            ]
        )


class UnknownHosts(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.node_list = ["rh7-1", "rh7-2"]
        self.known_hosts = self.node_list[:-1]
        self.unknown_hosts = self.node_list[-1:]
        self.config.corosync_conf.load()

    def test_one_node_not_auth(self):
        self.config.env.set_known_nodes(self.known_hosts)
        report_list = [
            fixture.error(
                report_codes.HOST_NOT_FOUND,
                force_code=report_codes.SKIP_OFFLINE_NODES,
                host_list=self.unknown_hosts,
            )
        ]
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=None,
                watchdog_dict={},
                sbd_options={},
            )
        )
        self.env_assist.assert_reports(report_list)

    def test_one_node_not_auth_skip_offline(self):
        sbd_config_generator = outdent(
            """\
        
        SBD_DELAY_START=no
        SBD_OPTS="-n {0}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        ).format
        (
            self.config.corosync_conf.load(
                filename="corosync-qdevice.conf", instead="corosync_conf.load"
            )
            .env.set_known_nodes(self.known_hosts)
            .http.host.check_auth(self.known_hosts)
            .http.sbd.check_sbd(
                communication_list=[
                    fixture.check_sbd_comm_success_fixture(
                        node, "/dev/watchdog", []
                    )
                    for node in self.known_hosts
                ]
            )
            .http.sbd.set_sbd_config(
                config_generator=sbd_config_generator,
                node_labels=self.known_hosts,
            )
            .http.pcmk.remove_stonith_watchdog_timeout(
                node_labels=[self.known_hosts[0]]
            )
            .http.sbd.enable_sbd(node_labels=self.known_hosts)
        )

        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=None,
            watchdog_dict={},
            sbd_options={},
            ignore_offline_nodes=True,
        )

        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.HOST_NOT_FOUND,
                    host_list=self.unknown_hosts,
                )
            ]
            + _sbd_enable_successful_report_list_fixture(self.known_hosts)
        )

    def test_all_nodes_not_auth(self):
        report_list = [
            fixture.error(
                report_codes.HOST_NOT_FOUND,
                force_code=report_codes.SKIP_OFFLINE_NODES,
                host_list=self.node_list,
            ),
            fixture.error(report_codes.NONE_HOST_FOUND),
        ]
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=None,
                watchdog_dict={},
                sbd_options={},
            )
        )
        self.env_assist.assert_reports(report_list)

    def test_all_node_not_auth_skip_offline(self):
        report_list = [fixture.error(report_codes.NONE_HOST_FOUND)]
        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=None,
                watchdog_dict={},
                sbd_options={},
                ignore_offline_nodes=True,
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.HOST_NOT_FOUND, host_list=self.node_list
                ),
            ]
            + report_list
        )


class MissingNodeNamesInCorosync(TestCase):
    def setUp(self):
        self.env_assist, self.config = get_env_tools(self)
        self.config.env.set_known_nodes(["rh7-1", "rh7-2", "rh7-3"])
        self.watchdog = "/dev/watchdog"

    def test_some_node_names_missing(self):
        def config_generator(node):
            return sbd_config_template.format(node_name=node, devices="")

        corosync_conf_name = "corosync-some-node-names.conf"
        node_list = ["rh7-2"]
        sbd_config_template = outdent(
            """\
        
        SBD_DELAY_START=no
        {devices}SBD_OPTS="-n {node_name}"
        SBD_PACEMAKER=yes
        SBD_STARTMODE=always
        SBD_WATCHDOG_DEV=/dev/watchdog
        SBD_WATCHDOG_TIMEOUT=5
        """
        )

        (
            self.config.corosync_conf.load(
                filename=corosync_conf_name,
                
                auto_tie_breaker=True,
            )
            .http.host.check_auth(node_labels=node_list)
            .http.sbd.check_sbd(
                communication_list=[
                    fixture.check_sbd_comm_success_fixture(
                        node, self.watchdog, []
                    )
                    for node in node_list
                ]
            )
            .http.sbd.set_sbd_config(
                config_generator=config_generator,
                node_labels=node_list,
            )
            .http.pcmk.remove_stonith_watchdog_timeout(node_labels=node_list)
            .http.sbd.enable_sbd(node_labels=node_list)
        )

        enable_sbd(
            self.env_assist.get_env(),
            default_watchdog=self.watchdog,
            watchdog_dict={},
            sbd_options={},
        )

        
        
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.COROSYNC_CONFIG_MISSING_NAMES_OF_NODES,
                    fatal=False,
                ),
            ]
            + _sbd_enable_successful_report_list_fixture(node_list)
        )

    def test_some_node_names_missing_atb(self):
        corosync_conf_name = "corosync-some-node-names.conf"
        node_list = ["rh7-2"]

        (
            self.config.corosync_conf.load(filename=corosync_conf_name)
            .http.host.check_auth(node_labels=node_list)
            .http.sbd.check_sbd(
                communication_list=[
                    fixture.check_sbd_comm_success_fixture(
                        node, self.watchdog, []
                    )
                    for node in node_list
                ]
            )
        )

        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            )
        )

        self.env_assist.assert_reports(
            [
                
                
                fixture.warn(
                    report_codes.COROSYNC_CONFIG_MISSING_NAMES_OF_NODES,
                    fatal=False,
                ),
                fixture.info(report_codes.SBD_CHECK_STARTED),
                fixture.info(report_codes.SBD_CHECK_SUCCESS, node="rh7-2"),
                fixture.warn(
                    report_codes.COROSYNC_QUORUM_ATB_WILL_BE_ENABLED_DUE_TO_SBD
                ),
                fixture.error(
                    report_codes.COROSYNC_CONFIG_MISSING_NAMES_OF_NODES,
                    fatal=True,
                ),
            ]
        )

    def test_some_node_names_missing_validation(self):
        (
            self.config.corosync_conf.load(
                filename="corosync-some-node-names.conf"
            )
        )

        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={
                    "rh7-1": "/dev/wd1",
                    "rh7-2": "/dev/wd2",
                },
                sbd_options={},
                node_device_dict={
                    "rh7-1": ["/dev/dev1"],
                    "rh7-2": ["/dev/dev2"],
                },
            )
        )
        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.COROSYNC_CONFIG_MISSING_NAMES_OF_NODES,
                    fatal=False,
                ),
                fixture.error(
                    report_codes.NODE_NOT_FOUND,
                    node="rh7-1",
                    searched_types=[],
                ),
            ]
        )

    def test_all_node_names_missing(self):
        (self.config.corosync_conf.load(filename="corosync-no-node-names.conf"))

        self.env_assist.assert_raise_library_error(
            lambda: enable_sbd(
                self.env_assist.get_env(),
                default_watchdog=self.watchdog,
                watchdog_dict={},
                sbd_options={},
            )
        )

        self.env_assist.assert_reports(
            [
                fixture.warn(
                    report_codes.COROSYNC_CONFIG_MISSING_NAMES_OF_NODES,
                    fatal=False,
                ),
                fixture.error(
                    report_codes.COROSYNC_CONFIG_NO_NODES_DEFINED,
                ),
            ]
        )
