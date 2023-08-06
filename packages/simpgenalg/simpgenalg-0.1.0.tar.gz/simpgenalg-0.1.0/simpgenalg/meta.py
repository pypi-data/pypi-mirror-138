from .other.tlbx import sga_tb
from .other import basicComponent
from simpcfg import config
from simplogger import simplog
from simptoolbox import toolbox
from .structures.basics import basicStructure
import logging

class geneticAlgorithm():

    __slots__ = ('config', 'toolbox', 'log')

    def __init__(self, *args, **kargs):
        # Get config
        self.config = kargs.pop('config',config(kargs.get('config_name',\
                                                            'simpgenalg')))
        # Get toolbox
        self.toolbox = kargs.pop('toolbox',sga_tb)

        # Any extra kargs will go to updating the config
        self.config.loadDict(kargs, update=True)

        # Create the log
        self.log = simplog(self.config.get('log_name','simpgenalg',dtype=str))
        self.log.setLevel(self.config.get('log_lvl',20,dtype=int))

        if self.config.get('console_log',True, dtype=bool):
            #logging.
            self.log.addHandler(htype='stream', \
                                   h_lvl=self.config.get('console_loglvl',\
                                                self.config.get('log_lvl'),\
                                                dtype=int),\
                                   format=self.config.get('console_format',4))
        #self.log.addHandler(htype='stream')

        self.log.debug('Initializing geneticAlgorithm')

    # Loads the structure of the GA, then runs it and returns results
    def run(self):

        self.log.info(f'Configuration:\n{self.config}')
        self.log.debug('Called run for geneticAlgorithm')

        # Get structure, defaults to generational GA
        self.log.debug('Getting structure for geneticAlgorithm')
        struct = self.config.get('structure','generational', \
                                 dtype=(str, basicStructure))

        # If inputted a string, convert it using toolbox
        if isinstance(struct, str):
            self.log.debug(f'Converting {struct} from str to struct obj')
            struct = self.toolbox[struct]

        # Initialize the structure
        self.log.info('Creating structure for geneticAlgorithm')
        struct = struct(config=self.config, \
                        toolbox=self.toolbox)

        # Run the structure and return the results
        self.log.info('Starting structure')

        return struct.run()

    #  CFG
    def get_config(self):
        return self.config
    def set_config(self, newCFG):
        if isinstance(newCFG, str):
            self.config = config(newCFG)
        elif isinstance(newCFG, config):
            self.config = newCFG
        else:
            self.log.exception('Expected str or simpconfig', err=TypeError)

    #  Toolbox
    def get_toolbox(self):
        return self.toolbox
    def set_toolbox(self, newTB):
        if isinstance(newTB, str):
            self.toolbox = simplog(newTB)
        elif isinstance(newTB, config):
            self.toolbox = newTB
        else:
            self.log.exception('Expected str or toolbox', err=TypeError)

    # Logger
    def get_log(self):
        return self.log
