# -*- coding: utf-8 -*-
# original source code: https://github.com/PortSwigger/example-traffic-redirector/tree/master/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from easyburp import EasyBurp

HOST_FROM = "host1.example.org"
HOST_TO = "host2.example.org"

burp = EasyBurp(extension_name='Traffic redirector')


# only process requests and if the host is HOST_FROM
@burp.http(request=True, host=HOST_FROM)
def http(tool_flag, message_is_request, message_info):
    # get the HTTP service for the request
    http_service = message_info.getHttpService()

    # change it to HOST_TO
    message_info.setHttpService(
        burp.helper.buildHttpService(HOST_TO, http_service.getPort(), http_service.getProtocol()))
