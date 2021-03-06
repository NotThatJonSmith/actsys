# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Intel Corp.
#
"""
Defines the interface for remote OS access execution of processes.
"""
from ..plugin import DeclareFramework


@DeclareFramework('os_remote_access')
class OsRemoteAccess(object):
    """Interface for remote process execution."""
    def __init__(self):
        pass

    def execute(self, cmd, remote_access_data, capture=False, other=None):
        """Using address and credentials, execute the cmd remotely."""
        pass

    def test_connection(self, remote_access_data):
        """Test is the OS is currently responding to requests."""
        pass

    def execute_multiple_nodes(self, cmd, remote_access_list, capture=False, other=None):
        """Execute the remote command on multiple nodes"""
        pass
