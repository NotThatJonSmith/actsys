# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the Mock plugin for pdu access/control.
"""
import os
import unittest
from ctrl.pdu.mock.mock import PluginMetadata
from ctrl.pdu.mock.mock import PduMock
from ctrl.plugin.manager import PluginManager
from ctrl.utilities.remote_access_data import RemoteAccessData

class TestPduMock(unittest.TestCase):
    def setUp(self):
        self.pdu_file = os.path.sep + os.path.join('tmp', 'pdu_file')

    def test_metadata_mock(self):
        manager = PluginManager()
        metadata = PluginMetadata()
        self.assertEqual('pdu', metadata.category())
        self.assertEqual('mock', metadata.name())
        self.assertEqual(1000, metadata.priority())
        manager.add_provider(metadata)
        pdu = manager.factory_create_instance('pdu', 'mock')
        self.assertIsNotNone(pdu)

    def test_persist_state(self):
        if os.path.exists(self.pdu_file):
            os.unlink(self.pdu_file)
        pdu = PduMock()
        connection = RemoteAccessData('127.0.0.1', 22, 'fsp', None)
        self.assertEqual('On', pdu.get_outlet_state(connection, '3'))
        pdu.set_outlet_state(connection, '3', 'Off')
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(connection, '3', 'invalid_state')
        self.assertEqual('Off', pdu.get_outlet_state(connection, '3'))
        pdu = PduMock()
        self.assertEqual('Off', pdu.get_outlet_state(connection, '3'))