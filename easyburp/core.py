import functools
import logging
import sys

from .logger import logger

if False:  # XXX: instead of typing.TYPE_CHECKING
    from .burp.extender import Extender
    from .burp.types import *


def only_when_running(function):
    @functools.wraps(function)
    def _only_when_running(*args, **kwargs):
        if EasyBurp.callbacks is None:
            raise RuntimeError('only_when_running')
        return function(*args, **kwargs)

    return _only_when_running


class EasyBurp:
    extender = None  # type: Extender

    def __init__(self, extension_name=None, level=logging.WARNING):
        self.extension_name = extension_name
        self.logger = logger
        self._event_handlers = {}
        self._helper = None

        logging.basicConfig(
            level=level,
            format=b'[%(asctime)s] %(levelname)s: %(message)s',
            stream=sys.stdout,
        )

    def add_event_handler(self, name, func):
        if name not in self._event_handlers:
            self._event_handlers[name] = []

        self._event_handlers[name].append(func)

    def event_handler(self, name, args):
        if name in self._event_handlers:
            for h in self._event_handlers[name]:
                h(*args)

    @property
    @only_when_running
    def callbacks(self):
        return self.extender.callbacks

    @property
    @only_when_running
    def helper(self):
        return self.extender.helper

    def extension_unloaded(self, _func=None):
        if _func is None:
            return self.extension_unloaded

        self.add_event_handler('extensionUnloaded', _func)

        @functools.wraps(_func)
        def decorator():
            return _func()

        return decorator

    def http(self, _func=None, request=None, response=None, host=None, port=None, protocol=None):
        if _func is None:
            return functools.partial(self.http, request=request, response=response, host=host, port=port,
                                     protocol=protocol)

        def __func(tool_flag, message_is_request, message_info):  # type: (int, bool, IHttpRequestResponse) -> None
            if request is not None and (request and not message_is_request or not request and message_is_request):
                return
            if response is not None and (response and message_is_request or not response and not message_is_request):
                return

            http_service = message_info.getHttpService()  # type: IHttpService

            if host is not None:
                if http_service.getHost() != host:
                    return
            if port is not None:
                if http_service.getPort() != port:
                    return
            if protocol is not None:
                if http_service.getProtocol() != protocol:
                    return

            _func(tool_flag, message_is_request, message_info)

        self.add_event_handler('processHttpMessage', __func)

        @functools.wraps(_func)
        def decorator(*a, **kw):
            return _func(*a, **kw)

        return decorator

    def proxy(self, _func=None):
        if _func is None:
            return self.proxy

        self.add_event_handler('processProxyMessage', _func)

        @functools.wraps(_func)
        def decorator(*a, **kw):
            return _func(*a, **kw)

        return decorator

    def scanner(self, _func=None):
        if _func is None:
            return self.scanner

        self.add_event_handler('newScanIssue', _func)

        @functools.wraps(_func)
        def decorator(*a, **kw):
            return _func(*a, **kw)

        return decorator

    def scope_change(self, _func=None):
        if _func is None:
            return self.scope_change

        self.add_event_handler('scopeChanged', _func)

        @functools.wraps(_func)
        def decorator(*a, **kw):
            return _func(*a, **kw)

        return decorator
