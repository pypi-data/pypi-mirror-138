from ...other import basicComponent
from simplogger import simplog
import logging
from collections import Counter
import unittest
import random

class basicChromo(basicComponent):

    __slots__ = ('max','min','dtype','lenLim','vals','fit', 'hsh')

    def __init__(self, *args, **kargs):
        # Initialize basicComponent
        super().__init__(*args, **kargs)

        ''' Initializes basic chromo '''
        # Creates log
        self.max = kargs.get('max',None)
        self.min = kargs.get('min',None)
        self.dtype = kargs.get('dtype',None)

        self.lenLim = kargs.get('lenLim', None)
        if 'len' in kargs:
            self.lenLim = (kargs.get('len'), kargs.get('len'))
        self.vals = kargs.get('vals',None)
        self.fit = kargs.get('fit',None)
        self.hsh = kargs.get('hsh',None)

    ''' Chromosome Generation '''
    ''' Generates a list of random chromosome values '''
    def generate(self):
        self.set_fit(None)
        self.set_hash(None)
        if self.lenLim[0] is None or self.lenLim[1] is None:
            self.log.exception('Tried to generate chromosome without length '+\
                                'limited', err=ValueError)
        elif self.lenLim[0] == self.lenLim[1]:
            length = self.lenLim[0]
        elif self.lenLim[0] > self.lenLim[1]:
            self.log.exception('Minimum is larger than maximum for chrlen',\
                                    err=ValueError)
        elif self.lenLim[0] != self.lenLim[1]:
            length = random.randint(self.lenLim[0], self.lenLim[1])


        if self.dtype is int:
            self.vals = [random.randint(self.get_min(indx),self.get_max(indx))\
                            for indx in range(self.lenLim[0])]
        elif self.dtype is float:
            self.vals = [random.uniform(self.get_min(indx),self.get_max(indx))\
                            for indx in range(self.lenLim[0])]
        else:
            self.log.exception('dtype should be int or float, was '+\
                f'{self.dtype}', err=TypeError)

    def _validate(self, vals=None):
        ''' Validates chromosome has vals of correct dtype, min, and max '''
        vals = vals if vals is not None else self.vals

        if self.lenLim[0] is None or self.lenLim[1] is None:
            self.log.exception('Need to provide lenLim tuple of min/max or a'+\
                                ' len', err=ValueError)
        if self.dtype is None:
            self.log.exception('Need to provide a dtype', err=ValueError)

        if len(vals) < self.lenLim[0] or len(vals) > self.lenLim[1]:
            self.log.exception('Either above or below min/max len', \
                                    err=ValueError)

        for indx, val in enumerate(vals):
            if not isinstance(val, self.dtype):
                self.log.exception('Incorrrect dtype found in chromo at indx'+\
                    f' {indx}, item {val} is {type(val)}', err=TypeError)
            if not (val >= self.get_min(indx)):
                self.log.exception('Below min val found in chromo at indx'+\
                    f' {indx}, item {val} is less than {self.get_min(indx)}',\
                    err=ValueError)
            if not (val <= self.get_max(indx)):
                self.log.exception('Above max val found in chromo at indx'+\
                                   f' {indx}, item {val} is greater than '+\
                                   f'{self.get_max(indx)}',err=ValueError)
        return

    def set_chromo(self, lst, validate=True):
        self.set_fit(None)
        self.set_hash(None)
        if validate:
            self._validate(vals=lst)
        self.vals = lst.copy()

    ''' Chromosome Value Access '''
    def to_list(self, return_copy=True):
        if return_copy:
            return self.vals.copy()
        return self.vals

    ''' Returns chromo val at indx '''
    def __getitem__(self, indx):
        return self.vals.__getitem__(indx)

    ''' Verifies correct value is being placed, then places it in chromo '''
    def __setitem__(self, indx, item):
        self.set_fit(None)
        self.set_hash(None)
        if not isinstance(item, self.dtype):
            self.log.exception(f'{item} not the correct dtype ({self.dtype}'+\
                               f'for this chromo at index {indx}', \
                               err=TypeError)
        if item < self.get_min(indx) or item > self.get_max(indx):
            self.log.exception(f'{item} out of range ({self.getRange(indx)}) '+\
                               f'for this chromo at index {indx}', \
                               err=ValueError)
        return self.vals.__setitem__(indx, item)

    ''' Alais for __getitem__ '''
    def get(self, indx):
        return self.vals.__getitem__(indx)

    ''' Allows appending to the end of the chromosome '''
    def append(self, item):
        # Raise exception if tried appending past max length
        self.set_fit(None)
        self.set_hash(None)
        if len(self.vals) >= self.lenLim[1]:
            self.log.exception('Tried appending past max length', \
                               err=IndexError)
        self.vals.append(item)


    ''' Allows extending an iterable to the end of a chromo '''
    def extend(self, lst):
        self.set_fit(None)
        self.set_hash(None)
        if len(self.vals) + len(lst) >= self.lenLim[1]:
            self.log.exception('Tried extending past max length', \
                               err=IndexError)
        self.vals.extend(lst)

    ''' Allows inserting values at a spot in the chromosome '''
    def insert(self, indx, item):
        self.set_fit(None)
        self.set_hash(None)
        if len(self.vals) >= self.lenLim[1]:
            self.log.exception('Tried inserting past max length', \
                               err=IndexError)
        self.vals.insert(indx, item)

    ''' Allows replacing a value in the chromosome '''
    def replace(self, oldItem, newItem, n=None):
        self.set_fit(None)
        self.set_hash(None)
        vals = self.vals
        if n is None:
            for indx in range(len(self.vals)):
                if vals[indx] == oldItem:
                    vals[indx] = newItem
        else:
            cnt = 0
            for indx in range(len(self.vals)):
                if vals[indx] == oldItem:
                    vals[indx] = newItem
                    cnt += 1
                    if cnt == n:
                        return

    ''' Evaluation Status '''

    ''' Search '''
    ''' Returns a count of specified item '''
    def count(self, item):
        return self.vals.count(item)

    ''' Returns a Counter object of all the items in the chromosome '''
    def returnCounter(self):
        return Counter(self.vals)

    ''' Returns the first index value of specified object '''
    def index(self, item):
        return self.vals.index(item)

    ''' Returns index of a sublist occuring inside a chromosome '''
    def find_sublist_index(self, subLst):
        vals, firstItem, subLstLen = self.vals, subLst[0], len(subLst)
        if isinstance(subLst, list):
            subLst = list(subLst)
        return [indx for indx, val in enumerate(vals[:-subLstLen]) if \
            (firstItem == val and \
             subLst == vals[indx+subLstLen])]

    # Returns True if a sublist exists inside a chromosome
    def contains_sublist(self, subList):
        vals, firstItem, subLstLen = self.vals, subLst[0], len(subLst)
        if isinstance(subLst, tuple):
            subLst = list(subLst)
        for indx, val in enumerate(vals[:-subLstLen]):
            if (firstItem == val and \
                subLst == vals[indx+subLstLen]):
                return True
        return False

    # Returns true if an object (or sublst) exists inside of chromo
    def __contains__(self, item):
        if isinstance(item, (list,tuple)) and self.contains_sublist(item):
            return True
        else:
            return self.vals.__contains__(item)

    # Returns a copy of this chromosome
    def copy(self):
        return basicChromo(vals = self.to_list(return_copy=True),\
                            max = self.max,\
                            min = self.min,\
                            dtype = self.dtype, \
                            lenLim = self.lenLim, \
                            fit = self.fit, \
                            hsh = self.hsh)

        self.max = kargs.get('max',None)
        self.min = kargs.get('min',None)
        self.dtype = kargs.get('dtype',None)

        self.lenLim = kargs.get('lenLim', None)
        if 'len' in kargs:
            self.lenLim = (kargs.get('len'), kargs.get('len'))
        self.vals = kargs.get('vals',None)
        self.fit = kargs.get('fit',None)
        self.hsh = kargs.get('hsh',None)

    def __copy__(self):
        return self.copy()

    ''' Removal '''
    ''' Resets the chromosome '''
    def clear(self):
        self.vals.clear()

    ''' Pops a value out of the chromoosome '''
    def pop(self, indx):
        return self.vals.pop(indx)

    ''' Removes a value from the chromosome '''
    def remove(self, item):
        self.vals.remove(item)

    ''' Sorting '''
    ''' Reverses the ordering of the chromosome '''
    def reverse(self):
        self.vals.reverse()

    ''' Allows sorting the chromosome '''
    def sort(self, reverse=False, key=None):
        if key is None:
            self.vals.sort(reverse=reverse)
        else:
            self.vals.sort(reverse=reverse, key=key)

    ''' min/max '''
    ''' Returns the minimum accepted value at an index '''
    def get_min(self, indx):
        if isinstance(self.min, int):
            return self.min
        elif isinstance(self.min, list):
            return self.min[indx]
        elif callable(self.min):
            return self.min(indx)
    ''' Returns the maximum accepted value at an index '''
    def get_max(self, indx):
        if isinstance(self.max, int):
            return self.max
        elif isinstance(self.max, list):
            return self.max[indx]
        elif callable(self.max):
            return self.max(indx)
    def getRange(self, indx):
        return (self.get_min(indx), self.get_max(indx))

    ''' Hash '''
    # Note that the hash functions provided are only useful for hashing the
    #   values inside the chromosome at a given momment, meaning if the chromo
    #   changes, it will not reflect the same hash value.  This is useful for
    #   hashing chromosomes' and their respective solutions, however it is not
    #   useful for hashing chromosome objects that may be undergoing changes
    ''' Returns a unique hash for this chromosome '''
    def __hash__(self):
        if self.hsh is None:
            self.hsh = tuple(self.vals).__hash__()
        return self.hsh
    def get_hash(self):
        return self.__hash__()
    def set_hash(self, new_hash):
        self.hsh = new_hash

    ''' Sees if this equals another in terms of values, accepts lists'''
    def __eq__(self, other):
        if isinstance(other, list):
            return (self.vals == other)
        elif isinstance(other, basicChromo):
            return (self.vals == other.vals)
        else:
            return (self.vals == list(other))

    ''' Other utility '''
    ''' Returns list of values as string '''
    def __str__(self):
        return self.vals.__str__()
    ''' Returns length of chromosome '''
    def __len__(self):
        return self.vals.__len__()
    # Returns iterator
    def __iter__(self):
        return self.vals.__iter__()
    ''' Sets/Gets fitness '''
    def set_fit(self, new_fit):
        self.fit = new_fit
    def get_fit(self):
        return self.fit


''' Test '''
class basicChromo_UnitTest(unittest.TestCase):

    def test_AAA_init(self):
        logging.disable()
        chromo = basicChromo(max=1, min=0, len=10, dtype=int)
        self.assertEqual(len(chromo),10, msg='len function failed')
        self.assertEqual(max([chromo.get_max(indx) for indx in \
                         range(len(chromo))]), 1, msg='Bad max value returned')
        self.assertEqual(min([chromo.get_min(indx) for indx in \
                         range(len(chromo))]), 0, msg='Bad min value returned')
        logging.disable(logging.NOTSET)

    def testAAB_Access(self):
        logging.disable()
        chromo = basicChromo(max=10, min=0, len=10, dtype=int)

        chromo[3] = 9
        self.assertEqual(chromo[3], 9, msg='Did not save or return val correct')
        self.assertRaises(IndexError, chromo.__setitem__, 100, 3)
        self.assertRaises(ValueError, chromo.__setitem__, 3, 100)
        self.assertRaises(TypeError, chromo.__setitem__, 3, 3.4)
        logging.disable(logging.NOTSET)


    def test_AAC_copy(self):
        logging.disable()
        chromoA = basicChromo(max=1, min=0, len=10, dtype=int)
        chromoB = chromoA.copy()
        self.assertTrue((chromoA==chromoB), msg='Copy or equal failed')
        logging.disable(logging.NOTSET)


    def test_AAD_hash_and_eq(self):
        logging.disable()

        chromoA = basicChromo(max=10, min=0, len=10, dtype=int)
        hashA = chromoA.__hash__()
        dct = {}
        self.assertEqual(chromoA.__hash__(),hashA, msg='hash failed')
        if chromoA[3] == 5:
            chromoA[3] = 6
        else:
            chromoA[3] = 5
        self.assertNotEqual(chromoA.__hash__(), hashA, \
                            msg='hash did not change')
        logging.disable(logging.NOTSET)





if __name__ == '__main__':
    unittest.main()
