# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
""" Module for testing Utils """

from unittest import TestCase
from copy import deepcopy
from mock import patch, call, MagicMock
from datastore import DataStore
from ..utils import split_command_results, print_msg, \
                    append_to_list_in_dictionary, Usage, \
                    debug_info_from_device_name, device_name_from_debug_info
from ....commands import CommandResult

def mock_print_and_test(class_name, msg, exp_class_name, exp_msg):
    """ Mocks the builtin print function and checks for a given message """
    with patch('__builtin__.print') as mock_print:
        print_msg(class_name, msg)
        mock_print.assert_has_calls(
            [
                call(' * {0} - {1}'.format(exp_class_name, exp_msg))
            ]
        )

class TestUtils(TestCase):
    """Class to test utils's functions. """
    def setUp(self):
        self.node = 'node0'
        self.msg = "Some message."
        self.default_class_name = "REST API"
        self.result = CommandResult()
        self.base_none_dic = {self.result.device_name: self.result}
        self.result_device = CommandResult(device_name=self.node)
        self.base_dic = {self.result_device.device_name: self.result_device}
        self.result_success = CommandResult(0, "Success")
        self.base_success_dic = {self.result_success.device_name: self.result_success}
        self.datastore = MagicMock(spec=DataStore)

    def test_print_msg_no_class_no_msg(self):
        """ Tests print_msg without class_name nor message"""
        mock_print_and_test(None, None, self.default_class_name, None)

    def test_print_msg(self):
        """ Tests print_msg function """
        mock_print_and_test(self.__class__, self.msg, self.__class__, self.msg)

    def test_append_to_list_in_dictionary_None_values(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = None
        self.assertEqual(-1, append_to_list_in_dictionary(mydic, None))
        self.assertIsNone(mydic)

    def test_append_to_list_in_dictionary_invalid_types(self):
        """ Tests the append_to_list_in_dictionary function """
        self.assertEqual(-1, append_to_list_in_dictionary(self.msg, self.msg))

    def test_append_to_list_in_dictionary_first_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        self.assertEqual(self.base_none_dic, mydic)

    def test_append_to_list_in_dictionary_second_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = deepcopy(self.base_none_dic)
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        expected = {self.result.device_name: [self.result, self.result]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_third_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {self.result.device_name: [self.result, self.result]}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result))
        expected = {self.result.device_name: [self.result, self.result, self.result]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_first_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        self.assertEqual(self.base_dic, mydic)

    def test_append_to_list_in_dictionary_second_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = deepcopy(self.base_dic)
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        expected = {self.result_device.device_name:[self.result_device,
                                                    self.result_device]}
        self.assertEqual(expected, mydic)

    def test_append_to_list_in_dictionary_third_device_result(self):
        """ Tests the append_to_list_in_dictionary function """
        mydic = {self.result_device.device_name:[self.result_device,
                                                 self.result_device]}
        self.assertFalse(append_to_list_in_dictionary(mydic, self.result_device))
        expected = {self.result_device.device_name:[self.result_device,
                                                    self.result_device,
                                                    self.result_device]}
        self.assertEqual(expected, mydic)

    def test_split_command_None_results(self):
        """ Tests the split_command_results function """
        success, fail = split_command_results(None)
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_split_command_empty_results(self):
        """ Tests the split_command_results function """
        success, fail = split_command_results(list())
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_split_command_invalid_result(self):
        """ Tests the split_command_results function """
        success, fail = split_command_results(self.msg)
        self.assertEqual(success, fail)
        self.assertFalse(success)

    def test_split_command_single_result(self):
        """ Tests the split_command_results function """
        success, fail = split_command_results(self.result)
        self.assertFalse(success)
        self.assertEqual(self.base_none_dic, fail)

    def test_split_command_multiple_results(self):
        """ Tests the split_command_results function """
        results = [self.result, self.result]
        success, fail = split_command_results(results)
        self.assertFalse(success)
        self.assertEqual({self.result.device_name:results}, fail)

    def test_split_command_single_result_success(self):
        """ Tests the split_command_results function """
        success, fail = split_command_results(self.result_success)
        self.assertFalse(fail)
        self.assertEqual(self.base_success_dic, success)

    def test_split_command_multiple_results_success(self):
        """ Tests the split_command_results function """
        results = [self.result_success, self.result_success]
        success, fail = split_command_results(results)
        self.assertFalse(fail)
        self.assertEqual({self.result_success.device_name:results}, success)

    def test_split_command_multiple_results_both(self):
        """ Tests the split_command_results function """
        results = [self.result, self.result_success]
        success, fail = split_command_results(results)
        self.assertEqual(self.base_none_dic, fail)
        self.assertEqual(self.base_success_dic, success)

    def test_split_command_multiple_results_invalid(self):
        """ Tests the split_command_results function """
        results = [self.msg, self.result_success]
        success, fail = split_command_results(results)
        self.assertFalse(fail)
        self.assertEqual(self.base_success_dic, success)

    def test_utils_get_usage_msg(self):
        """ Tests the get_usage_msg from Usage class """
        usage = Usage()
        expected = (usage._literals['title']+
                    usage._literals['description']+
                    usage._literals['usage']+
                    usage._literals['http_method_supported']+
                    usage._literals['http_method']+
                    usage._literals['url']+usage._literals['command']+
                    usage._literals['subcommand']+
                    usage._literals['args_start']+
                    usage._literals['args']+
                    usage._literals['where']+
                    usage._literals['server_desc']+
                    usage._literals['port_desc']+
                    usage._literals['command_desc']+
                    usage._literals['subcommand_desc']+
                    usage._literals['args_desc']
                   )
        ret = usage.get_usage_msg()
        self.assertEqual(expected, ret)
        print (ret)

    def test_debug_info_from_device_name_none_params(self):
        self.assertIsNone(debug_info_from_device_name(None, None))

    def test_debug_info_from_device_name_invalid_DataStore(self):
        self.assertIsNone(debug_info_from_device_name('', None))

    def test_debug_info_from_device_name_not_found(self):
        self._check_debug_info_from_device_name_is_none(None)

    def test_debug_info_from_device_name_found(self):
        device = dict(debug_ip="192.168.20.1", debug_port=0)
        self._check_debug_info_from_device_name_is_eq(device, device)
        self.datastore.get_device.assert_called_once()

    def test_debug_info_from_device_name_found_no_debug_port(self):
        device = dict(debug_ip="192.168.20.1")
        self._check_debug_info_from_device_name_is_none(device)

    def test_debug_info_from_device_name_found_no_debug_ip(self):
        device = dict(debug_port=0)
        self._check_debug_info_from_device_name_is_none(device)

    def _check_debug_info_from_device_name_is_none(self, return_value, device_name='mydevice'):
        self.datastore.get_device.return_value = return_value
        self.assertIsNone(debug_info_from_device_name(self.datastore, device_name))

    def _check_debug_info_from_device_name_is_eq(self, return_value, expected, device_name='mydevice'):
        self.datastore.get_device.return_value = return_value
        self.assertEqual(expected, debug_info_from_device_name(self.datastore, device_name))

    def test_device_name_from_debug_info_none_params(self):
        self.assertIsNone(device_name_from_debug_info(None, None, None))

    def test_device_name_from_debug_info_none_debug_ip(self):
        self.assertIsNone(device_name_from_debug_info(self.datastore, None, None))

    def test_device_name_from_debug_info_none_debug_port(self):
        self.assertIsNone(device_name_from_debug_info(self.datastore, '', None))

    def test_device_name_from_debug_info_invalid_DataStore(self):
        self.assertIsNone(device_name_from_debug_info('', None, None))

    def test_device_name_from_debug_info_not_found(self):
        self._check_device_name_from_debug_info_is_none([])

    def test_device_name_from_debug_info_found_device_id(self):
        device = dict(device_id='mydevice', hostname='mydevice', ip_address='192.168.20.20')
        self._check_device_name_from_debug_info_is_eq([device], 'mydevice')

    def test_device_name_from_debug_info_foun_hostname(self):
        device = dict(hostname='mydevice', ip_address='192.168.20.20')
        self._check_device_name_from_debug_info_is_eq([device], 'mydevice')

    def test_device_name_from_debug_info_found_ip_address(self):
        device = dict(ip_address='192.168.20.20')
        self._check_device_name_from_debug_info_is_eq([device], '192.168.20.20')

    def test_device_name_from_debug_info_found_no_device_name(self):
        device = dict(debug_address='192.168.20.20')
        self._check_device_name_from_debug_info_is_none([device])

    def _check_device_name_from_debug_info_is_none(self, return_value, debug_ip='debug_hostname', debug_port=0):
        self.datastore.list_devices.return_value = return_value
        self.assertIsNone(device_name_from_debug_info(self.datastore, debug_ip, debug_port))

    def _check_device_name_from_debug_info_is_eq(self, return_value, expected, debug_ip='debug_hostname', debug_port=0):
        self.datastore.list_devices.return_value = return_value
        self.assertEqual(expected, device_name_from_debug_info(self.datastore, debug_ip, debug_port))
