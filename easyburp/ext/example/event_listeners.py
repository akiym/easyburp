# -*- coding: utf-8 -*-
# original source code: https://github.com/PortSwigger/example-event-listeners/tree/master/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from easyburp import EasyBurp

burp = EasyBurp(extension_name='Event listeners', level=logging.INFO)


@burp.http
def http(tool_flag, message_is_request, message_info):
    burp.logger.info(
        'HTTP %s %s [%s]' % ('request to' if message_is_request else 'response from',
                             message_info.getHttpService().toString(), burp.callbacks.getToolName(tool_flag)))


@burp.proxy
def proxy(message_is_request, message):
    burp.logger.info(
        'Proxy %s %s' % ('request to' if message_is_request else 'response from',
                         message.getMessageInfo().getHttpService().toString()))


@burp.scanner
def scanner(issue):
    burp.logger.info('New scan issue: %s' % (issue.getIssueName()))


@burp.extension_unloaded
def extension_unloaded():
    burp.logger.info('Extension was unloaded')
