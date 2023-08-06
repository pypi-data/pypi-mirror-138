from simplogger import simplog
from ...representations.basics import basicChromo
from ...other import basicComponent
import random, unittest

class basicCrossover(basicComponent):

    __slots__ = 'xov_rate'

    def __init__(self, *args, **kargs):
        # Initialize basicComponent
        super().__init__(*args, **kargs)
        # Initialize crossover values
        self.xov_rate = kargs.get('xov_rate',\
                self.config.get('xov_rate',0.8, dtype=float, mineq=0, maxeq=1))

    def set_xov_rate(self, new_rate):
        self.xov_rate = new_rate

    def get_xov_rate(self):
        return self.xov_rate

    def __call__(self, *args, **kargs):
        self.crossover(*args, **kargs)

    def crossover(self, *parents, **kargs):
        if len(parents) == 0:
            self.log.exception('passed nothing to crossover', err=ValueError)
        elif len(parents) == 1 and isinstance(parents[0], list):
            self.cross_batch(parents[0], **kargs)
        elif all([isinstance(parent, basicChromo) for parent in parents]):
            self.cross_parents(parents, **kargs)
        else:
            self.log.exception('could not infer method with crossover', \
                                err=TypeError)

    def cross_parents(self, *parents, **kargs):
        if random.random() < xov_rate if kargs.get('xov_rate',None) is not None \
                                                            else self.xov_rate:
            return self._cross_parents(*parents, **kargs)


    def _cross_parents(self, *parents, **kargs):
        self.log.exception('_cross_parents not implemented', \
                            err=NotImplementedError)

    def cross_batch(self, *parents, **kargs):
        xov_rate = kargs.get('xov_rate',self.xov_rate)
        children = []
        for p1, p2 in zip(parents[::2], parents[1::2]):
            if random.random() >= xov_rate:
                continue
            cur_children = cross_parents(p1, p2, **kargs)
            children.extend(cur_children)

        return children

class basicCrossver_unittest(unittest.TestCase):

    def test_AAA_errors(self):
        bscxov = basicCrossover(xov_rate=0.7)
        with self.assertRaises(NotImplementedError):
            bscxov._cross_parents([10],[10])
        with self.assertRaises(NotImplementedError):
            bscxov.cross_batch([10],[10])
