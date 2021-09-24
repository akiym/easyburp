# -*- coding: utf-8 -*-
# original source code: https://github.com/PortSwigger/example-hello-world/tree/master/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from easyburp import EasyBurp

burp = EasyBurp(extension_name='Hello world extension')
