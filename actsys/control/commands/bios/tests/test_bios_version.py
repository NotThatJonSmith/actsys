# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Test the BiosVersion Command.
"""
import unittest

from mock import MagicMock, patch

from .. import BiosVersionCommand
from ....plugin.manager import PluginManager
from datastore import DataStore


class TestBiosVersionCommand(unittest.TestCase):
    """Test case for the BiosVersionCommand class."""

    @patch("datastore.DataStore", spec=DataStore)
    @patch("control.plugin.manager.PluginManager", spec=PluginManager)
    def setUp(self, mock_plugin_manager, mock_logger):
        self.setup_mock_config()
        self.node_name = "knl-123"
        self.mock_plugin_manager = mock_plugin_manager
        self.bios_manager_mock = self.mock_plugin_manager.create_instance.return_value
        self.bios_manager_mock.get_version.return_value = {self.node_name: "Success"}

        self.config = {
                'device_name': [self.node_name],
                'configuration': self.configuration_manager,
                'plugin_manager': mock_plugin_manager,
                'logger': mock_logger
            }
        self.bios_version = BiosVersionCommand(**self.config)

    def setup_mock_config(self):
        self.configuration_manager = MagicMock()
        self.configuration_manager.get_device.return_value = {
            "ip_address": "192.168.1.1",
            "port": 22,
            "user": "user",
            "password": "pass",
            "device_type": "node",
            "access_type": "mock",
            "service_list": []
        }

    def test_execute(self):
        self.assertEqual(self.bios_version.execute()[0].return_code, 0)
        self.bios_manager_mock.get_version.side_effect = Exception("Fail")
        self.assertEqual(self.bios_version.execute()[0].return_code, 255)

    def test_access_type_none(self):
        del self.configuration_manager.get_device.return_value["access_type"]
        self.assertEqual(255, self.bios_version.execute()[0].return_code)

if __name__ == '__main__':
    unittest.main()
