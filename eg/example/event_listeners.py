# original source code: https://github.com/PortSwigger/example-event-listeners/tree/master/python

import easyburp.ext.example.event_listeners
from easyburp import Extender

BurpExtender = Extender(easyburp.ext.example.event_listeners).export()
