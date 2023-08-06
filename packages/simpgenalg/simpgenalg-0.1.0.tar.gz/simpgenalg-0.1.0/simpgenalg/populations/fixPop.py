from .basics import basicPopulation


class fixedPopulation(basicPopulation):

    __slots__ = 'pop_size'

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.log.info('Initializing fixedPopulation')
        self.pop_size = self.config.get('pop_size',100,divisible_by=2)
        self.pop_size_lim = (self.pop_size, self.pop_size)

        if kargs.get('generate',True):
            self.generate()


    def append(self, *args, **kargs):
        self.log.exception('Cannot append with fixed population')
    def extend(self, *args, **kargs):
        self.log.exception('Cannot extend with fixed population')
    def insert(self, *args, **kargs):
        self.log.exception('insert append with fixed population')
    def pop(self, *args, **kargs):
        self.log.exception('pop append with fixed population')

    def generate(self, *args, **kargs):
        # Generate pop_size number of individuals
        # Generate pop_size number of individuals
        rep, config, toolbox = self.rep, self.config, self.toolbox
        self.poplst = [self.rep(config=self.config,\
                                toolbox=self.toolbox)\
                        for x in range(self.pop_size)]
        return
