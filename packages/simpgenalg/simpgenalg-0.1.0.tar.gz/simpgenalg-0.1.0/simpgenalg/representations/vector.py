from .basics import *
import unittest, random, logging

class fixedVectorChromo(basicChromo):

    __slots__ = ('length')

    def __init__(self, *args, **kargs):

        super().__init__(self, *args, **kargs)

        if 'len_min' in kargs or 'len_max' in kargs:
            raise ValueError('Should not include len_min or len_max for '+\
                             'fixedVectorChromo')

        # if values are none from basicChromo init than use config
        self.length = self.config.get('len',dtype=int, mineq=1)
        self.lenLim = self.lenLim if self.lenLim is not None else \
                        (self.length, self.length)
        self.max = self.max if self.max is not None else \
                        self.config.get('chr_max')
        self.min = self.min if self.min is not None else \
                        self.config.get('chr_min')
        self.dtype = self.dtype if self.dtype is not None else \
                        self.config.get('dtype',int)

        if kargs.get('generate', True):
            self.generate()

    def generate(self):
        ''' Generates a list of random chromosome values '''
        if self.dtype is int:
            self.vals = [random.randint(self.get_min(indx),self.get_max(indx))\
                            for indx in range(self.length)]
        elif self.dtype is float:
            self.vals = [random.uniform(self.get_min(indx),self.get_max(indx))\
                            for indx in range(self.length)]
        else:
            self.log.exception('dtype should be int or float, was '+\
                f'{self.dtype}', err=TypeError)

    def append(self, item):
        self.log.exception('Cannot append to a fixedVectorChromo',\
                           err=NotImplementedError)

    def extend(self, item):
        self.log.exception('Cannot extend to a fixedVectorChromo',\
                           err=NotImplementedError)

    def insert(self, item):
        self.log.exception('Cannot insert to a fixedVectorChromo',\
                           err=NotImplementedError)

    def pop(self, indx):
        self.log.exception('Cannot pop from a fixedVectorChromo',\
                           err=NotImplementedError)

class vectorRepresentation(basicRepresentation):

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        if 'chromo' not in kargs:
            self.chromo = fixedVectorChromo(*args, **kargs)

    def _map(self, chromo):
        return chromo.to_list(return_copy=True)

    def get_mapped(self):
        return self.get_chromo(return_copy=False).to_list(return_copy=True)

    def copy(self, copy_ID=False):
        if copy_ID:
            return vectorRepresentation(log=self.log,\
                                    chromo=self.get_chromo(return_copy=True),\
                                    fit=self.get_fit(),\
                                    attrs=self.get_attrs(return_copy=True),\
                                    len=self.get_chromo().__len__(),\
                                    ID=self.get_ID())
        return vectorRepresentation(log_name=self.log.getLogKey(),\
                                chromo=self.get_chromo(return_copy=True),\
                                fit=self.get_fit(),\
                                attrs=self.get_attrs(return_copy=True),\
                                len=self.get_chromo().__len__())


class fixedVectorChromo_unittest(unittest.TestCase):

    def test_AAA_raises_error(self):

        fvc = fixedVectorChromo(len=10, min=0, max=10, dtype=int)
        logging.disable()
        self.assertRaises(NotImplementedError, fvc.append, 1)
        self.assertRaises(NotImplementedError, fvc.extend,[1])
        self.assertRaises(NotImplementedError, fvc.insert,[1])
        self.assertRaises(NotImplementedError, fvc.pop,1)
        logging.disable(logging.NOTSET)

class vectorRepresentation_unittest(unittest.TestCase):

    def make_indv(self):
        return vectorRepresentation(max=10, \
                                    min=0, \
                                    dtype=int,\
                                    len=10)

    def test_AAA_init(self):
        indv = self.make_indv()

    def test_AAB_map(self):
        indv = vectorRepresentation(max=10, \
                                    min=0, \
                                    dtype=int,\
                                    len=10)

        lst = indv.get_chromo().to_list()

        self.assertEqual(lst, indv.get_mapped(), msg='get_mapped failed')
        self.assertEqual(lst, indv._map(indv.get_chromo()), msg='_map failed')

if __name__ == '__main__':
    unittest.main()
