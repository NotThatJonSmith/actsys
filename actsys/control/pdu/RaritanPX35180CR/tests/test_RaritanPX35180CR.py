# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Test the RaritanPX35180CR PDU plugin for PDU access/control.
"""

import unittest
import getpass
from mock import MagicMock, patch
from ..RaritanPX35180CR import PduRaritanPX35180CR
from ....utilities.remote_access_data import RemoteAccessData
from ....utilities.utilities import Utilities

class TestPduRaritanPX35180CR(unittest.TestCase):
    """Test the Raritan_PX3-5180CR pdu implementation."""

    def test_get_outlet_state(self):
        pdu = PduRaritanPX35180CR()
        connection = RemoteAccessData('', '', '', None)
        pdu._execute_remote_pdu_command = MagicMock(return_value='Error: Failed to retrieve state')
        with self.assertRaises(RuntimeError):
            pdu.get_outlet_state(connection, 'On')
        pdu._execute_remote_pdu_command.return_value = "Outlet 3: ('Knl-1to4-ps2') Power state: On"
        self.assertEqual('On', pdu.get_outlet_state(connection, '3'))

    def test_set_outlet_state(self):
        pdu = PduRaritanPX35180CR()
        connection = RemoteAccessData('', '', '', None)
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(connection, '', 'invalid_state')
        invalid_connection = RemoteAccessData('', 12, '', None)
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(invalid_connection, '4', 'On')
        pdu._execute_remote_pdu_command = MagicMock(return_value='power outlets 1 On /y')
        pdu.set_outlet_state(connection, '1', 'Off')
        pdu._execute_remote_pdu_command.return_value = 'Error: Invalid outlet number'
        with self.assertRaises(RuntimeError):
            pdu.set_outlet_state(connection, '1', 'On')

    @patch.object(Utilities, 'execute_in_shell')
    def test_execute_remote_pdu_command(self, mock_ssh):
        pdu = PduRaritanPX35180CR()
        connection = RemoteAccessData('127.0.0.1', 22, getpass.getuser(), None)
        mock_ssh.return_value = 0, getpass.getuser() + '\n'
        output = pdu._execute_remote_pdu_command(connection, 'whoami')
        self.assertEqual(getpass.getuser() + '\n', output)
        mock_ssh.return_value = 255, None
        with self.assertRaises(RuntimeError):
            pdu._execute_remote_pdu_command(connection, 'xxx')


