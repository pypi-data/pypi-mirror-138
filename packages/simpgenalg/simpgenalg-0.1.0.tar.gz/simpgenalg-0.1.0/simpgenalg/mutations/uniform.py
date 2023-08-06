from ..representations.basics import basicRepresentation
from .basics import basicMutation
import random

class uniformRandomMutation(basicMutation):

    __slots__ = ('dtype','generate_value')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.dtype = self.config.get('dtype',int)

        if self.dtype is int:
            self.generate_value = random.randint
        elif self.dtype is float:
            self.generate_value = random.uniform
        else:
            self.log.exception('Incorrect dtype for uniformRandomMutation',\
                                err=TypeError)

    def mutate_indx(self, indv, indx=None, mut_rate=None):
        chromo = indv.get_chromo(return_copy=False)
        if random.random() < mut_rate if mut_rate is not None else self.mut_rate:
            indv.incr_attr('num_muts')
            chromo[indx] = self.generate_value(chromo.get_min(indx),\
                                               chromo.get_max(indx))
        return

    def mutate_chromo(self, indv, mut_rate=None):
        mut_rate = mut_rate if mut_rate is not None else self.mut_rate
        chromo = indv.get_chromo(return_copy=False)
        random_chance = random.random
        num_muts = 0
        for indx, indv in enumerate(chromo.to_list()):
            if random_chance() < mut_rate:
                num_muts += 1
                chromo[indx] = self.generate_value(chromo.get_min(indx),\
                                                   chromo.get_max(indx))
        indv.set_attr('num_muts',num_muts)

    def mutate_batch(self, btch, **kargs):
        mut_rate = kargs.get('mut_rate',self.mut_rate)
        random_chance = random.random

        for indv in btch:
            chromo = indv.get_chromo(return_copy=False)
            num_muts = 0
            for indx in range(len(chromo)):
                if random_chance() < mut_rate:
                    num_muts += 1
                    chromo[indx] = self.generate_value(chromo.get_min(indx),\
                                                       chromo.get_max(indx))
            indv.set_attr('num_muts',num_muts)


    def _mutate_indx(self, chromo, indx=None):
        indv.get_chromo()[mut_rate] = self.generate_value(self.get_min(indx),\
                                                          self.get_max(indx))
