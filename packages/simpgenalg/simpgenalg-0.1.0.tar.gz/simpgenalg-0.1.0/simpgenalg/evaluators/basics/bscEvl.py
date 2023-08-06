from ...other import basicComponent
import sys

class basicEvaluator(basicComponent):

    __slots__ = ('maximize','dynamic','sCache', 'cache', 'max_indv', \
                 'min_indv', 'smax_indv', 'smin_indv','use_cache',\
                 'use_super_cache', 'get_cache', 'set_cache')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        # Load some parameters
        self.maximize = self.config.get('maximize', True, dtype=bool)
        self.dynamic = self.config.get('dynamic', False, dtype=bool)
        self.use_cache = self.config.get('use_cache',not self.dynamic, \
                                            dtype=bool)
        self.use_super_cache = self.config.get('use_super_cache', \
                                                self.use_cache, dtype=bool)

        # Raise error if trying to use caches on dynamic problem
        if (self.dynamic) and (use_cache or use_super_cache):
            self.log.exception('Cannot use caches with dynamic problems', \
                                    err=ValueError)

        # Set up mins and maxes
        self.max_indv, self.min_indv, self.smax_indv, self.smin_indv = \
                None,None,None,None

        self._setup_caches()

    def clear(self, clear_super=False):
        if self.cache is not None:
            self.cache = {}
        self.min_indv, self.max_indv = None, None

        if clear_super:
            if self.sCache is not None:
                self.sCache = {}
            self.smax_indv, self.smax_indv = None, None

    def evaluate(self, indv, **kargs):
        self.log.exception('Not Implemented', err=NotImplementedError)

    def evaluate_batch(self, btch, **kargs):
        for indv in btch:
            self.evaluate(btch, **kargs)

    def compare_mapped_distance(self, pop):
        if 'scipy' not in sys.modules:
            self.log.exception('Scipy needed to find distance between '+\
                                'individuals.', err=ModuleNotFoundError)

        indv_maps = [(indv, indv.get_mapped()) for indv in pop]

        dist_mat = squareform(pdist)




    # Returns maximum or minimum individual
    def get_max(self):
        return self.max_indv
    def get_smax(self):
        return self.smax_indv
    def get_min(self):
        return self.min_indv
    def get_smin(self):
        return self.smin_indv

    # Returns numbe rof unique solutions
    def get_n_unique_solutions(self, super=False):
        if super:
            if self.sCache is None:
                return None
            return self.sCache.__len__()
        if self.cache is None:
            return None
        return self.cache.__len__()

    # Returns stats
    def get_stats(self):
        dct = {}

        max = self.get_max()
        if max is not None:
            dct['run_max'] = max

        min = self.get_min()
        if min is not None:
            dct['run_min'] = min

        smax = self.get_smax()
        if smax is not None:
            dct['overall_max'] = smax

        smin = self.get_smin()
        if smin is not None:
            dct['overall_min'] = smin

        n_unique = self.get_n_unique_solutions()
        if n_unique is not None:
            dct['n_unique_solutions'] = n_unique

        s_unique = self.get_n_unique_solutions(super=True)
        if s_unique is not None:
            dct['s_unique_solutions'] = s_unique

        return dct

    # See if min or max, replaces if so
    def _replace_if_best(self, indv):
        if self.min_indv is None or indv < self.min_indv:
            self.min_indv = indv.copy(copy_ID=True)
            if  self.smin_indv is None or indv < self.smin_indv:
                self.smin_indv = indv.copy(copy_ID=True)
        if self.max_indv is None or indv > self.max_indv:
            self.max_indv = indv.copy(copy_ID=True)
            if self.smax_indv is None or indv > self.smax_indv:
                self.smax_indv = indv.copy(copy_ID=True)
        return


    # Different cache functions
    def _get_none(self, indv):
        return None
    def _get_bcache(self, indv):
        return self.cache.get(indv, self.sCache.get(indv,None))
    def _get_scache(self, indv):
        return self.sCache.get(indv, None)
    def _get_ncache(self, indv):
        return self.cache.get(indv, None)
    def _set_none(self, indv, fit):
        return
    def _set_bcache(self, indv, fit):
        return self.cache.get(indv, self.sCache.get(indv,None))
    def _set_scache(self, indv, fit):
        return self.sCache.get(indv, None)
    def _set_ncache(self, indv, fit):
        return self.cache.get(indv, None)

    # Sets up cache functions and caches
    def _setup_caches(self):
        # Set up caches
        if self.use_cache and self.use_super_cache:
            # Sets up two caches, a run cache and a super cache
            self.cache, self.sCache = {}, {}
            self.get_cache = self._get_bcache
            self.set_cache = self._set_bcache
        elif self.use_cache:
            # Sets up just a run cache, cleared every run
            self.cache, self.sCache = {}, None
            self.get_cache = self._get_ncache
            self.set_cache = self._set_ncache
        elif self.use_super_cache :
            # Sets up a super cache only, never cleared
            self.cache, self.sCache = None, {}
            self.get_cache = self._get_scache
            self.set_cache = self._set_scache
        else:
            # Sets up no cache (good for dynamic problems)
            self.cache, self.sCache = None, None
            self.get_cache = self._get_none
            self.set_cache = self._set_none

    # Creates a competitive template using a greedy algorithm inspired by the
    #   Messy Genetic Algorithm [1].  Creates a chromosome, runs through it
    #   in random ordering per sweep, and applies mutations.  Keeps if it is
    #   was a positive change
    def make_template(self, **kargs):
        self.log.exception('make_template Not Implemented yet', \
                                err=NotImplementedError)

'''
[1]  Goldberg, David E., Bradley Korb, and Kalyanmoy Deb. "Messy genetic
algorithms: Motivation, analysis, and first results." Complex systems
3.5 (1989): 493-530.
'''
