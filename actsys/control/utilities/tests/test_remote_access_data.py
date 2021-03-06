# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Tests for the RemoteAccessData class
"""
import unittest
from ..remote_access_data import RemoteAccessData


class TestRemoteAccessData(unittest.TestCase):
    """Simple tests for a simple class."""
    def test_remote_access_data(self):
        """All Tests."""
        data = RemoteAccessData('127.0.0.1', 22, 'some_user', 'some_id')
        self.assertEqual('127.0.0.1', data.address)
        self.assertEqual(22, data.port)
        self.assertEqual('some_user', data.username)
        self.assertEqual('some_id', data.identifier)
        self.assertEqual('127.0.0.1:22', data.get_authority())
        self.assertEqual('some_user:some_id', data.get_credentials())

        data1 = RemoteAccessData('127.0.0.1', 22, 'some_user', 'some_id')
        self.assertEqual(data, data1)

        data2 = RemoteAccessData('127.0.0.2', 22, 'some_user', 'some_id')
        self.assertNotEqual(data, data2)


if __name__ == '__main__':
    unittest.main()
