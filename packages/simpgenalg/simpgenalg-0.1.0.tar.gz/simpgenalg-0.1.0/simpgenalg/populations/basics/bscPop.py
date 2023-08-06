from simplogger import simplog
from ...other import basicComponent
from ...representations.basics import basicChromo, basicRepresentation
from statistics import mean, stdev
import sys

# Optional dependencies
try:
    from scipy.spatial.distance import pdist, squareform
except:
    pass


class basicPopulation(basicComponent):

    __slots__ = ('rep', 'pop_size_lim', 'poplst', 'indv_attrs',\
                 'pop_stats')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        # Setup representation
        self.rep = self.config.get('representation','vector',\
                                    dtype=(str,basicRepresentation))
        self._setup_rep(self.rep)
        self.pop_size_lim = None
        self.poplst = None
        self.indv_attrs = []
        self.pop_stats = {}

    # Allows getting an individual from the population
    def __getitem__(self, indx):
        return self.poplst.__getitem__(indx)

    # Allows setting an individual in the population
    def __setitem__(self, indx, new_indv):
        if isinstance(new_indv, self.rep):
            self.poplst.__setitem__(indx, new_indv)
        else:
            self.log.exception(f'Tried putting {type(new_indv)} in pop',\
                                err=TypeError)

    # Returns an individual, allows multiple search options like searching
    #   by index
    def get(self, *args, **kargs):
        # If we only have one argument, it should be the index
        if len(args) == 1:
            return self.__getitem__(args[0])
        elif len(args) == 0: # Otherwise check the kargs
            if 'id' in kargs or 'ID' in kargs:
                ID = kargs.get('id', kargs.get('ID'))
                for indv in self.poplst:
                    if indv.get_ID() == ID:
                        return indv
            elif 'indx' in kargs:
                return self.__getitem__(kargs.get('indx'))
        # Raise error if we have gotten to this point
        self.log.exception('Expected an int for the indx or a karg '+\
            'for \'indx\' or \'ID\' to search', err=ValueError)

    # General access to the population list
    def append(self, item):
        if len(self.poplst)+1 > self.get_max():
            self.log.exception('Cannot append past the max', err=IndexError)
        self.poplst.append(item)
    def extend(self, iterable):
        if len(self.poplst)+len(iterable) > self.get_max():
            self.log.exception('Cannot extend past the max', err=IndexError)
        self.poplst.extend(iterable)
    def insert(self, indx, item):
        if len(self.poplst)+1 > self.get_max():
            self.log.exception('Cannot insert past the max', err=IndexError)
        self.poplst.insert(indx, item)
    def pop(self, indx):
        if len(self.poplst)-1 < self.get_min():
            self.log.exception('Cannot pop if it will make it below the min',\
                                err=IndexError)
    def reverse(self):
        self.poplst.reverse()
    def sort(self, **kargs):
        self.poplst.sort(**kargs)

    # Generates a population
    def generate(self, *args, **kargs):
        # Get minimum and maximum
        min, max = self.get_min(), self.get_max()

        # Determine pop_size
        if min == max:
            pop_size = min
        elif min < max:
            pop_size = random.randint(min,max)
        elif min > max:
            self.log.exception('Population minimum cannot be greater than '+\
                                'maximum', err=ValueError)

        # Generate pop_size number of individuals
        rep, config, toolbox = self.rep, self.config, self.toolbox
        self.poplst = [self.rep(config=self.config,\
                                toolbox=self.toolbox)\
                        for x in range(pop_size)]

        return

    def clear(self):
        self.poplst,self.indv_attrs,self.pop_stats = None, [], {}

    # Returns the length (or number of indvs) in the population
    def __len__(self):
        return self.poplst.__len__()

    # Returns the iterater for the population
    def __iter__(self):
        return self.poplst.__iter__()

    # pop stats
    def get_indv_attrs(self):
        return [indv.get_attrs() for indv in self.poplst]
    def set_popstat(self, stat_name, value):
        self.pop_stats.__setitem__(stat_name, value)
    def get_popstat(self, stat_name):
        self.pop_stats.__getitem__(stat_name)
    def get_popstats(self, return_copy=True, compile_indv_attrs=True):
        if return_copy:
            dct = self.pop_stats.copy()
            if compile_indv_attrs:
                dct.update(self.compile_indv_attrs())
            return dct
        elif compile_indv_attrs:
            return self.pop_stats.update(self.compile_indv_attrs())
        else:
            return self.pop_stats
    def update_popstats(self, dct):
        self.pop_stats.update(**dct)
    def incr_popstat(self, *args):
        if len(args) == 1:
            self.pop_stats.__setitem__(args[0],\
                                        self.pop_stats.__getitem__(args[0])+1)
        elif len(args) == 2:
            self.pop_stats.__setitem__(args[0],\
                                    self.pop_stats.__getitem__(args[0])+args[1])
        else:
            self.log.exception('Expected 1-2 arguments for incr_popstats',\
                                    err=ValueError)
    # Compiles all individuals' attributes into mean,stdev,max,min
    #   Values that are in one indv but not another are ignored
    #       ^ this means if tracking something, it should be initialized to
    #       a default value while tracking, not just not attributed
    def compile_indv_attrs(self):

        # Get individual attribute dicts
        attrs = [indv.get_attrs() for indv in self.poplst]

        # Track all keys used
        all_keys = set()

        for indv_attr in attrs:
            all_keys.update(indv_attr.keys())

        compiled_dct = {}
        for key in all_keys:
            # Checks first instance to see if int or float
            if not isinstance(attrs[0].get(key, None), (int, float)):
                continue

            # Get all the vals (as long as they are not None)
            vals = [attr.get(key,None) for attr in attrs \
                        if attr.get(key,None) is not None]


            # Try to summarize the data, if fails send a warning
            try:
                compiled_dct[key+'_mean'] = mean(vals)
                compiled_dct[key+'_stdev'] = stdev(vals)
                compiled_dct[key+'_min'] = min(vals)
                compiled_dct[key+'_max'] = max(vals)
            except:
                self.log.warn(f'Tried to compile {key} indv attrs, but failed.')
                continue

        return compiled_dct

    def compare_mapped_distance(self, **kargs):
        # Makes sure Scipy is installed, otherwise raise error
        if 'scipy' not in sys.modules:
            self.log.exception('Cannot call compare_mapped_distance if scipy'+\
                                ' is not installed', err=ModuleNotFoundError)

        # Calculate distance between everything
        dist_mat = squareform(pdist([indv.get_mapped() for indv in self.poplst],\
                                    metric=kargs.get('dist_meth','euclidean')))
        # Add the average, stdev, min, and max of distances to other indvs
        for indx, indv in enumerate(self.poplst):
            indv.set_attr('avg_dist', mean(dist_mat[indx]))
            indv.set_attr('stdev_dist', stdev(dist_mat[indx]))
            indv.set_attr('min_dist', min(dist_mat[indx]))
            indv.set_attr('max_dist', max(dist_mat[indx]))

    # Returns maximum or minimum population
    def get_max(self):
        return self.pop_size_lim[1]
    def get_min(self):
        return self.pop_size_lim[0]

    # Sets up the appropriate value for the representation
    def _setup_rep(self, rep_in):
        if isinstance(self.rep, str):
            try:
                self.rep = self.toolbox[self.rep]
            except KeyError:
                self.log.exception(f'{self.rep} is not a valid representation',\
                                    err=KeyError)
        elif isinstance(self.rep, basicRepresentation):
            return
