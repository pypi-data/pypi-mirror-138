from ...other import basicComponent
from ...representations.basics import basicRepresentation
from simplogger import simplog
import random
class basicMutation(basicComponent):

    __slots__ = ('mut_rate')

    def __init__(self, *args, **kargs):
        super().__init__(self, *args, **kargs)
        self.mut_rate = self.config.get('mut_rate',dtype=float,mineq=0,maxeq=1)

    def __call__(self, *args, **kargs):
        self.mutate(*args, **kargs)

    # Easy call for mutation that infers based on input which method
    def mutate(self, input, **kargs):

        # See if batch
        if isinstance(input, list):

            if all([isinstance(inp, basicRepresentation) for inp in input]):
                self.mutate_batch(input, **kargs)
            else:
                self.log.exception('If passing list to mutate, must be list '+\
                                    'of individuals', err=TypeError)
        elif isinstance(input, basicRepresentation):
            if 'indx' in kargs:
                self.mutate_indx(input, **kargs)
            else:
                self.mutate_chromo(indv, **kargs)
        else:
            self.log.exception('mutate expected list of indvs or an indv',\
                                    err=TypeError)

    # Mutates singular index of indv
    def mutate_indx(self, indv, *args, **kargs):
        if random.random() < kargs.get('mut_rate',self.mut_rate):
            self._mutate_indx(indv, *args, **kargs)

    # Mutates singular indv
    def mutate_chromo(self, indv, *args, **kargs):
        self.log.exception('mutate_chromo not setup',err=NotImplementedError)

    # Mutates batch of individuals
    def mutate_batch(self, btch, *args, **kargs):
        for indv in btch:
            self.mutate_chromo(indv)

    # Mutates singular index of indv unconditionally
    def _mutate_indx(self, chromo, *args, **kargs):
        self.log.exception('_mutate_indx not setup',err=NotImplementedError)
