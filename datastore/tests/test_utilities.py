# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Tests for the FileStore class
"""
from __future__ import print_function
import unittest
from random import randint
import tempfile
import os
from ..utilities import DataStoreUtilities, JsonParser, FileNotFound, NonParsableFile, DeviceUtilities


class TestUtilities(unittest.TestCase):

    def setUp(self):
        pass

    def test_tail_file(self):
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write("""aligator
bat
cat
dog
elephant
flamingo
gorilla""")
        temp_file.close()
        result = DataStoreUtilities.tail_file(temp_file.name, 100)
        self.assertEqual(7, len(result))

        result = DataStoreUtilities.tail_file(temp_file.name, 5)
        self.assertEqual(5, len(result))

        result = DataStoreUtilities.tail_file(temp_file.name, 0)
        self.assertEqual(0, len(result))

        def only_dogs(line):
            print(line)
            return str(line) == "dog" or str(line) == "Dog"

        result = DataStoreUtilities.tail_file(temp_file.name, 100, None, only_dogs)
        self.assertEqual(1, len(result))

        def change_to_capitalized(line):
            return line.capitalize()

        result = DataStoreUtilities.tail_file(temp_file.name, 100, change_to_capitalized, only_dogs)
        self.assertEqual(1, len(result))

        os.remove(temp_file.name)

    def test_json_read_file(self):
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write("""{}""")
        temp_file.close()
        result = JsonParser.read_file(temp_file.name)
        self.assertEqual(result, {})
        os.remove(temp_file.name)

        with self.assertRaises(FileNotFound):
            temp_file = tempfile.NamedTemporaryFile("w", delete=True)
            temp_file.close()
            JsonParser.read_file(temp_file.name)

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.write("""foo""")
        temp_file.close()
        with self.assertRaises(NonParsableFile):
            JsonParser.read_file(temp_file.name)
        os.remove(temp_file.name)

    def test_json_write(self):
        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.close()
        JsonParser.write_file(temp_file.name, "{}")
        os.remove(temp_file.name)

        temp_file = tempfile.NamedTemporaryFile("w", delete=False)
        temp_file.close()
        # with self.assertRaises(NonParsableFile):
        #     JsonParser.write_file(temp_file.name, "{[")
        os.remove(temp_file.name)

        with self.assertRaises(FileNotFound):
            JsonParser.write_file('/root/not-allowed', "")

        try:
            JsonParser.write_file('/root/not-allowed', "")
        except FileNotFound as fnf:
            self.assertEqual(str(fnf), "'File /root/not-allowed not found.'")

    def test_json_get_string(self):
        result = JsonParser.get_file_content_string({"one": 1, "two": "two"})
        self.assertEqual('{\n  "one": 1,\n  "two": "two"\n}', result)


expansion_tests = {
    "accept_lists": ["node1,node2,node3", ["node1", "node2", "node3"]],
    "sequential_numbers": ["node[1-3]", ["node1", "node2", "node3"]],
    "accept_lists2": ["node1,node3", ["node1", "node3"]],
    "comma_seperated_numbers": ["node[1,3]", ["node1", "node3"]],
    "zero_padded_numbers": ["node[01-03]", ["node01", "node02", "node03"]],
    "comma_seperated_lists": ["node[1,45-46,990]", ["node1", "node45", "node46", "node990"]],
}

fold_tests = {
    "lists": ["node1,node2", "node[1-2]"],
    "nosequential_lists": ["node1,node5", "node[1,5]"],
    "nosequential_lists2": ["node1,node12", "node[1,12]"],
    "nosequential_lists3": ["node3,node1", "node[1,3]"],
    "strange_lists": ["node001,node4,node94", "node[001,004,094]"],
    "mutiple_names": ["nhl1,nfl1,nhl2,nfl2", "nfl[1-2],nhl[1-2]"]

}


class TestNodeExpand(unittest.TestCase):
    def test_expand(self):
        for test_key in expansion_tests.keys():
            test = expansion_tests.get(test_key)
            self.assertEqual(DeviceUtilities.expand_devicelist(test[0]), test[1])

    def test_fold(self):
        for test_key in fold_tests.keys():
            test = fold_tests.get(test_key)
            self.assertEqual(DeviceUtilities.fold_devices(test[0]), test[1])

