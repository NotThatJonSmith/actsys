# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Class used to hold username, password, address, and port for remote access.
"""


class RemoteAccessData(object):
    """Class to store common data for remote OS access."""
    def __init__(self, address, port, user, identifier):
        self.address = address
        self.port = port
        self.username = user
        self.identifier = identifier

    def get_authority(self):
        """Return the network authority for this object."""
        return '{}:{}'.format(self.address, self.port)

    def get_credentials(self):
        """Return the username:identifier for this object."""
        return '{}:{}'.format(self.username, self.identifier)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.address == other.address and
                self.port == other.port and
                self.username == other.username and
                self.identifier == other.identifier)

    def __ne__(self, other):
        return not self.__eq__(other)
