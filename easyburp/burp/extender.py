# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import inspect
import os.path

from burp import IBurpExtender
from burp import IBurpExtenderCallbacks
from burp import IExtensionHelpers
from burp import IExtensionStateListener
from burp import IHttpListener
from burp import IProxyListener
from burp import IScannerListener
from burp import IScopeChangeListener

from easyburp.core import EasyBurp
from easyburp.logger import logger


class Extender:
    def __init__(self, module):
        if not (inspect.ismodule(module) and hasattr(module, 'burp') and isinstance(module.burp, EasyBurp)):
            raise RuntimeError('module %s needs to export EasyBurp instance' % module.__name__)

        self.module = module
        self._mtime = os.path.getmtime(module.__file__)
        self._callbacks = None
        self._helper = None

    def export(self):
        cls = type(b'BurpExtender', (IBurpExtender,), dict(
            registerExtenderCallbacks=self._register_extender_callbacks,
        ))
        return cls

    @property
    def ext(self):  # type: () -> EasyBurp
        return self.module.burp

    @property
    def callbacks(self):  # type: () -> IBurpExtenderCallbacks
        return self._callbacks

    @property
    def helper(self):  # type: () -> IExtensionHelpers
        if self._helper is None:
            self._helper = self.callbacks.getHelpers()
        return self._helper

    def _register_extender_callbacks(self, callbacks):  # type: (IBurpExtenderCallbacks) -> None
        if self.ext.extension_name is not None:
            callbacks.setExtensionName(self.ext.extension_name)

        self._callbacks = callbacks
        self.register_extension_state_listener()
        self.register_http_listener()
        self.register_proxy_listener()
        self.register_scanner_listener()
        self.register_scope_change_listener()

        self.ext.extender = self

    def register_extension_state_listener(self):
        cls = type(b'ExtensionStateListener', (IExtensionStateListener,), dict(
            extensionUnloaded=self.event_handler('extensionUnloaded'),
        ))
        self.callbacks.registerExtensionStateListener(cls())

    def register_http_listener(self):
        cls = type(b'HttpListener', (IHttpListener,), dict(
            processHttpMessage=self.event_handler('processHttpMessage'),
        ))
        self.callbacks.registerHttpListener(cls())

    def register_proxy_listener(self):
        cls = type(b'ProxyListener', (IProxyListener,), dict(
            processProxyMessage=self.event_handler('processProxyMessage'),
        ))
        self.callbacks.registerProxyListener(cls())

    def register_scanner_listener(self):
        cls = type(b'ScannerListener', (IScannerListener,), dict(
            newScanIssue=self.event_handler('newScanIssue'),
        ))
        self.callbacks.registerScannerListener(cls())

    def register_scope_change_listener(self):
        cls = type(b'ScopeChangeListener', (IScopeChangeListener,), dict(
            scopeChanged=self.event_handler('scopeChanged'),
        ))
        self.callbacks.registerScopeChangeListener(cls())

    def event_handler(self, name):
        def _event_handler(_self, *args):
            self.reload_module()
            self.ext.event_handler(name, args)

        return _event_handler

    def reload_module(self):
        mtime = os.path.getmtime(self.module.__file__)
        if self._mtime >= mtime:
            return
        self._mtime = mtime

        logger.debug('reloading module: %s' % self.module.__name__)
        reload(self.module)
        self.ext.extender = self
        logger.debug('reloaded')
