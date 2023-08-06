from .basics import basicEvaluator
import csv

import tensorflow as tf

class regressionEvaluator(basicEvaluator):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.log.info('Initializing regressionEvaluator')

        self.training_data = self.config.get('train_data')
        self.testing_data = self.config.get('test_data')

        if self.lib_use == 'tensorflow':
            if 'tensorflow' in sys.modules:
                self.log.exception('tensorflow is not imported', err=ImportError)

            self.log.exception('tensorflow for regression not implemented yet',\
                                err=NotImplementedError)
        elif self.lib_use == 'numpy':
            if 'numpy' in sys.modules:
                self.log.exception('numpy is not imported', err=ImportError)
            self.log.exception('numpy for regression not implemented yet',\
                                err=NotImplementedError)
        elif self.lib_use == 'python':
            self.log.exception('python for regression not implemented yet',\
                                err=NotImplementedError)
        else:
            self.log.exception('lib_use should be tensorflow, numpy, or python',\
                                err=ValueError)


        self.input_files()


    def input_files(self):
        pass

    def _input_file(self, inp):

        if isinstance(inp, str):
            pass
        elif isinstance(inp, list):
            pass
        elif 'pandas' in sys.modules and isinstance(inp, pd.DataFrame):
            pass
        elif 'tensorflow' in sys.modules and
