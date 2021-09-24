# original source code: https://github.com/PortSwigger/example-traffic-redirector/tree/master/python

import easyburp.ext.example.traffic_redirector
from easyburp import Extender

BurpExtender = Extender(easyburp.ext.example.traffic_redirector).export()
