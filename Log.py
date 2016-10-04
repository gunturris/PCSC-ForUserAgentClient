import sys, logging
from wsgilog import WsgiLog
import web
import config

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = '%(message)s',
            tofile = True,
            toprint = True,
            file = web.config.log_file,
            interval = web.config.log_interval,
            backups = web.config.log_backups
            )