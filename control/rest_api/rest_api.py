# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
This module creates a rest application to execute user commands.
"""
from flask_restful import Api
from flask import Flask
from .resources.resource_mgr import ResourceManager
from .resources.bios import Bios
from ..cli.command_invoker import CommandInvoker

class ControlRestApi(object):
    """ Class that creates a rest application to execute user commands. """
    def __init__(self, **kwargs):
        self._set_flags_from_kwargs(kwargs)
        self.cmd_invoker = CommandInvoker()
        self.flask_app = Flask(__name__)
        self.rest_api = Api(self.flask_app)
        self._load_config()
        self._add_resources()

    def _set_flags_from_kwargs(self, kwargs):
        self.debug = kwargs.get('debug', False)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def _load_config(self):
        self.flask_app.config.from_object(__name__)

    def _add_resources(self):
        self.rest_api.add_resource(ResourceManager, \
            '/resource', '/resource/', '/resource/<string:subcommand>', \
            resource_class_kwargs={'cmd_invoker':self.cmd_invoker, \
            'debug': self.debug})
        self.rest_api.add_resource(Bios, \
            '/bios', '/bios/', '/bios/<string:subcommand>', \
            resource_class_kwargs={'cmd_invoker':self.cmd_invoker, \
            'debug': self.debug})
        self._add_plugins()

    def _add_plugins(self):
        try:
            from ctrl_plugins import ResourceSut
            self.rest_api.add_resource(ResourceSut, \
                '/sut', '/sut/', '/sut/<string:subcommand>', \
                resource_class_kwargs={'cmd_invoker':self.cmd_invoker, \
                'debug': self.debug})
        except ImportError:
            pass

    def run(self):
        """ Runs the rest api application """
        self.flask_app.run(host=self.host, port=self.port, debug=self.debug)