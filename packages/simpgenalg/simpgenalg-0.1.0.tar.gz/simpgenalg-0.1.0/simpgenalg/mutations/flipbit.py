from ..representations.basics import basicRepresentation
from .basics import basicMutation

class flipbitMutation():

    def mutate_indx(self, indv, indx=None, mut_rate=None):
        chromo = indv.get_chromo(return_copy=False)
        if random.random() < mut_rate if mut_rate is not None else self.mut_rate:
            indv.incr_attr('num_muts')
            if chromo[indx] == 1:
                chromo[indx] = 0
            elif chromo[indx] == 0:
                chromo[indx] = 1
            else:
                self.log.exception(f'flipbitMutation received {chromo[indx]} '+\
                                    'instead of 0 or 1', err=ValueError)

    def mutate_chromo(self, indv, mut_rate=None):
        mut_rate = mut_rate if mut_rate is not None else self.mut_rate
        indv.get_chromo().set_chromo([val if random.random()>=mut_rate else \
                                        0 if val == 1 else 0 \
                                        for indx, val in enumerate(chromo)])

        num_mut = 0
        chromo = indv.get_chromo(return_copy=False)
        random_chance = random.random
        for indx, val in enumerate(chromo.to_list()):
            if random_chance() < mut_rate:
                num_mut += 1
                if val == 1:
                    chromo[indx] = 0
                elif val == 0:
                    chromo[indx] = 1
                else:
                    self.log.exception(f'flipbitMutation received {val} '+\
                                        'instead of 0 or 1', err=ValueError)
        indv.set_attr('num_muts', num_mut)
