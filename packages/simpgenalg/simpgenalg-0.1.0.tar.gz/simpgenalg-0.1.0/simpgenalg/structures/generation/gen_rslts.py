from ...other import basicComponent

class allResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.runs = []

    def append_run(self, run):
        self.runs.append(run)

class runResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.gens = []

    def __getitem__(self, key):
        return self.gens.__getitem__(key)

    def append(self, *args, **kargs):
        if len(args) == 1:
            if not isinstance(gen, genResults):
                self.log.exception('Can only append genResults to runResults',\
                                    err=TypeError)
            self.gens.append(gen)
        elif 'pop_stats' in kargs and 'indv_attrs' in kargs:
            self.gens.append(genResults(config=self.config,\
                                        log=self.log,\
                                        toolbox=self.toolbox,\
                                        indv_attrs=kargs.get('indv_attrs'),\
                                        pop_stats=kargs.get('pop_stats')))
        else:
            self.log.exception('Must either pass a genResults or the pop_stats'+\
                                ' and indv_attrs as kargs', err=TypeError)


class genResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.indv_attrs = kargs.get('indv_attrs',None)
        self.pop_stats = kargs.get('pop_stats',None)

    def get_gen_strs(self, *args, **kargs):
        string = ''
        if 'round' in kargs:
            rnd = kargs.get('round')
            if isinstance(rnd, bool):
                rnd = 3
            for key in args:
                string += f'\t{key}:{round(self.pop_stats.get(key,None),rnd)}'
        else:
            for key in args:
                string += f'\t{key}:{self.pop_stats.get(key,None)}'
        return string
