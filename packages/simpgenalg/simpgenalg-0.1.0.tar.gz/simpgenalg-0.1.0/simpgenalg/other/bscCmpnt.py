from simplogger import simplog
from simpcfg import config
from simptoolbox import toolbox

class basicComponent():

    __slots__ = ('config', 'toolbox', 'log', 'runsafe')

    def __init__(self, *args, **kargs):
        self.log = kargs.get('log',\
                        simplog(kargs.get('log_name','simpgenalg')))
        self.config = kargs.get('config',\
                        config(kargs.get('config_name','simpgenalg')))
        self.toolbox = kargs.get('toolbox',\
                        toolbox(kargs.get('toolbox_name','simpgenalg')))
        self.runsafe = kargs.get('runsafe', None)

        if self.runsafe is None:
            try:
                self.runsafe = self.config.get('runsafe', True, dtype=bool)
            except:
                self.runsafe = True



    def _is_iter(self, obj):
        try:
            iter(obj)
            return True
        except:
            return False

    def _is_hash(self, obj):
        try:
            hash(obj)
            return True
        except:
            return False

    def get_log(self):
        return self.log

    def get_toolbox(self):
        return self.toolbox

    def get_config(self):
        return self.config

    def get_runsafe(self):
        return self.runsafe
