# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing ControlRestApi """
from unittest import TestCase
from mock import patch
import datastore
from ..rest_api import ControlRestApi

class TestControlRestApi(TestCase):
    """ Class for testing ControlRestApi """
    def setUp(self):
        self.rest_api = ControlRestApi(dfx=True, debug=True)
        self.rest_api.flask_app.config['TESTING'] = True
        self.test_app = self.rest_api.flask_app.test_client()

    def test_load_config(self):
        """ Test for _load_config function """
        self.assertTrue(self.rest_api.flask_app.config['TESTING'])

    def test__init__defaults(self):
        """ Tests init function with default values """
        with patch.object(datastore.DataStoreBuilder, 'build'):
            rest_api = ControlRestApi()
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertFalse(rest_api.debug)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test__init__dfx_and_debug_enabled(self):
        """ Tests init function with debug and dfx enabled """
        rest_api = ControlRestApi(dfx=True, debug=True)
        self.assertIsNotNone(rest_api)
        self.assertTrue(rest_api.dfx)
        self.assertTrue(rest_api.debug)
        self.assertTrue(rest_api.dfx_resource_mgr)

    def test__init__no_dfx_with_dfx_data(self):
        """ Tests init function with global dfx disabled but enabled for resource_mgr """
        with patch.object(datastore.DataStoreBuilder, 'build'):
            rest_api = ControlRestApi(dfx_resource_mgr=True)
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertTrue(rest_api.dfx_resource_mgr)

    def test__init__dfx_with_dfx_data(self):
        """ Tests init function with global dfx enabled but disabled for resource_mgr """
        rest_api = ControlRestApi(dfx=True, dfx_resource_mgr=False)
        self.assertIsNotNone(rest_api)
        self.assertTrue(rest_api.dfx)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test__init__no_dfx_invalid_dfx_data(self):
        """ Tests init function with global dfx disabled and invalid dfx_data """
        with patch.object(datastore.DataStoreBuilder, 'build'):
            rest_api = ControlRestApi(foo=True)
        self.assertIsNotNone(rest_api)
        self.assertFalse(rest_api.dfx)
        self.assertFalse(rest_api.dfx_resource_mgr)

    def test_run(self):
        """ Tests run function """
        with patch.object(self.rest_api.flask_app, 'run') as mock_run:
            self.rest_api.run()
            mock_run.assert_called_once()
            mock_run.assert_called_with(debug=True, host=None, port=None)