from ...other import basicComponent
from ...mutations.basics import basicMutation
from ...crossovers.basics import basicCrossover


class operatorApplicator(basicComponent):

    __slots__ = ('mut', 'xov')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        # Read in from config
        self.mut = self.config.get('mut_op', dtype=(str,basicMutation))
        self.xov = self.config.get('xov_op', dtype=(str,basicCrossover))

        # Create the mutation operator
        if isinstance(self.mut, str):
            self.mut = self.toolbox[self.mut](*args, **kargs)
        elif isinstance(self.mut, basicMutation):
            self.mut = self.mut(*args, **kargs)
        else:
            self.log.exception('Expected str or mutation class',err=TypeError)

        # Create the crossover operator
        if isinstance(self.xov, str):
            self.xov = self.toolbox[self.xov](*args, **kargs)
        elif isinstance(self.xov, basicCrossover):
            self.xov = self.xov(*args, **kargs)
        else:
            self.log.exception('Expected str or crossover class',err=TypeError)



    def apply_operators(self, sel_parents, child_pop, **kargs):
        self.xov.cross_batch(parents=sel_parents, children=child_pop)
        self.mut.mutate_batch(child_pop)
