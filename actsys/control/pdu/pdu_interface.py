# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
This defines the interface for PDU objects.
"""
from abc import ABCMeta, abstractmethod
from ..plugin import DeclareFramework


@DeclareFramework('pdu')
class PDUInterface(object, metaclass=ABCMeta):
    """Interface class for PDU classes."""

    valid_states = ['On', 'Off', 'on', 'off']

    def __init__(self):
        pass

    @abstractmethod
    def get_outlet_state(self, connection, outlet):
        """Get the current outlet state for a pdu outlet."""
        pass

    @abstractmethod
    def set_outlet_state(self, connection, outlet, new_state):
        """Set the target outlet state for a pdu outlet."""
        pass
