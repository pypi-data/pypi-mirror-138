from .basics import basicEvaluator

class functionEvaluator(basicEvaluator):

    __slots__ = ('function', 'send_list')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.log.info('Initializing functionEvaluator')
        # Get evaluation function
        self.function = self.config.get('function', callable=True)
        self.send_list = self.config.get('send_list',True, dtype=bool)

    def evaluate(self, indv, **kargs):

        # Try reading the cache
        fit = self.get_cache(indv)

        # If fit is none, apply to function
        if fit is None:
            # send list or indv depending on confing
            if self.send_list:
                fit = self.function(\
                            indv.get_chromo(return_copy=False).to_list())
            else:
                fit = self.function(indv)
            # Save in cache
            self.set_cache(indv, fit)
        # Set fitness in individual
        indv.set_fit(fit)
        # Replace the current tracked best if so
        self._replace_if_best(indv)
        return

    def evaluate_batch(self, btch, **kargs):
        for indv in btch:
            self.evaluate(indv)
