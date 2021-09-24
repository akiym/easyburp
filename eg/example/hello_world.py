# original source code: https://github.com/PortSwigger/example-hello-world/tree/master/python

from java.io import PrintWriter
from java.lang import RuntimeException

import easyburp.ext.example.hello_world
from easyburp import Extender

_BurpExtender = Extender(easyburp.ext.example.hello_world).export()


class BurpExtender(_BurpExtender):
    def registerExtenderCallbacks(self, callbacks):
        super(BurpExtender, self).registerExtenderCallbacks(callbacks)

        # obtain our output and error streams
        stdout = PrintWriter(callbacks.getStdout(), True)
        stderr = PrintWriter(callbacks.getStderr(), True)

        # write a message to our output stream
        stdout.println("Hello output")

        # write a message to our error stream
        stderr.println("Hello errors")

        # write a message to the Burp alerts tab
        callbacks.issueAlert("Hello alerts")

        # throw an exception that will appear in our error stream
        raise RuntimeException("Hello exception")
