# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Plugin to talk to mock pdu functionality.
"""
import os.path
import json
from ...plugin.manager import PluginMetadataInterface
from ..pdu_interface import PDUInterface


class PluginMetadata(PluginMetadataInterface):
    """Required metadata class for a dynamic plugin."""
    def __init__(self):
        PluginMetadataInterface.__init__(self)

    def category(self):
        """Get the plugin category"""
        return 'pdu'

    def name(self):
        """Get the plugin instance name."""
        return 'mock'

    def priority(self):
        """Get the priority of this name in this category."""
        return 1000

    def create_instance(self, options=None):
        """Create an instance of this named implementation."""
        return PduMock(options)


class PduMock(PDUInterface):
    """Implement pdu contract"""
    def __init__(self, options=None):
        super(PduMock, self).__init__(options=None)
        self.__current_states = {}
        self.__persistent_file = os.path.sep + os.path.join('tmp', 'pdu_file')
        if os.path.exists(self.__persistent_file):
            self._load_pdu_file()

    def get_outlet_state(self, connection, outlet):
        """Get the current power state of the node outlet as a boolean."""
        if outlet in self.__current_states:
            return self.__current_states[outlet]
        else:
            self.__current_states[outlet] = 'On'
            self._save_pdu_file()
            return 'On'

    def set_outlet_state(self, connection, outlet, new_state):
        """Set the outlet to a new state."""
        if new_state not in self.valid_states:
            raise RuntimeError('An illegal PDU state was attempted: %s' %
                               new_state)
        self.__current_states[outlet] = new_state.capitalize()
        self._save_pdu_file()

    def _load_pdu_file(self):
        """Loads the pdu file from disk."""
        file_obj = open(self.__persistent_file, 'r')
        self.__current_states = json.load(file_obj)
        file_obj.close()

    def _save_pdu_file(self):
        """Saves the pdu file to disk."""
        file_obj = open(self.__persistent_file, 'w')
        json.dump(self.__current_states, file_obj)
        file_obj.close()
