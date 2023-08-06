from ...other import basicComponent
from .bscChromo import basicChromo
from simplogger import simplog
from statistics import mean, stdev
import unittest
import logging

class basicRepresentation(basicComponent):

    last_ID = 0

    __slots__ = ('chromo', 'mapped', 'ID', 'attrs', 'hsh')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.chromo = kargs.get('chromo', None)
        self.mapped = kargs.get('mapped', None)

        self.ID = kargs.get('ID', self.__get_next_ID())

        self.attrs = kargs.get('attrs', {})

        self.hsh = kargs.get('hsh', None)

    ''' chromosome '''
    # Returns chromosome
    def get_chromo(self, return_copy=True):
        if return_copy:
            return self.chromo.copy()
        return self.chromo

    def __len__(self):
        return self.get_chromo(return_copy=False).__len__()
    # Applies maps
    def _map(self, chromo):
        self.log.exception('_map not implemented', err=NotImplementedError)

    # Returns chromosome mapped
    def get_mapped(self):
        if self.mapped is None or self.get_chromo().get_fit() is None:
            self.mapped = self._map(self.get_chromo())
        return self.mapped

    ''' Inheritance '''
    # Sets chromosome
    def set_chromo(self, new_chromo, set_copy=False):
        if isinstance(new_chromo, list):
            self.get_chromo(return_copy=False).set_chromo(new_chromo)
        elif isinstance(new_chromo, basicChromo):
            if not set_copy:
                self.chromo = new_chromo
            else:
                self.chromo = new_chromo.copy()
        else:
            self.log.exception('Attempted to set a chromo without a proper '+\
                               'chromosome', err=TypeError)

        self.clear_attrs()
        self.set_fit(None)


    # Fancy inheriting, accepts new chromo and then compiles information from
    #   parents
    def inherit(self, new_chromo, *parents):
        # Set new chromo
        self.set_chromo(new_chromo)

        # Adds informatoin about the parents
        if len(parents) == 1:
            pfit = parents[0].get_fit()
            p_ID = parents[0].get_ID()
            plen = len(parents[0])
            self.update_attrs({'pfits':[pfit],\
                               'avg_pfit':pfit,\
                               'stdev_pfit':0,\
                               'range_pfit':0,\
                               'max_pfit':pfit,\
                               'min_pfit':pfit,\
                               'pIDs':[p_ID],\
                               'plens':[plen],\
                               'avg_plen':plen,\
                               'stdev_plen':0,\
                               'range_plen':0,\
                               'min_plen':plen,\
                               'max_plen':plen})
        elif len(parents) > 1:
            # Get some values from parents
            pfits = [parent.get_fit() for parent in parents]
            plens = [len(parent.get_chromo()) for parent in parents]
            min_pfit, max_pfit = min(pfits), max(pfits)
            min_plen, max_plen = min(plens), max(plens)
            self.update_attrs({'pfits':pfits,\
                               'avg_pfit':mean(pfits),\
                               'stdev_pfit':stdev(pfits),\
                               'range_pfit':max_pfit-min_pfit,\
                               'max_pfit':max_pfit,\
                               'min_pfit':min_pfit,\
                               'pIDs':[parent.get_ID() for parent in parents],\
                               'plens':plens,\
                               'avg_plen':mean(plens),\
                               'stdev_plen':stdev(plens),\
                               'range_plen':max_plen-min_plen,\
                               'min_plen':min_plen,\
                               'max_plen':max_plen})

    ''' Fitness '''
    # Returns fitness
    def get_fit(self):
        return self.get_chromo(return_copy=False).get_fit()
    # Sets the fitness, also places it in attrs for easy info compilation
    def set_fit(self, new_fit):
        self.set_attr('fit', new_fit)
        self.get_chromo(return_copy=False).set_fit(new_fit)
    # Clears fitness
    def clear_fit(self):
        self.get_chromo(return_copy=False).set_fit(None)
        try:
            self.del_attr('fit')
        except:
            pass
        return
    # If comparing against another individual, will check if mapped chromosome
    #    is the same.  if given a chromosome, will check if chromsome is the same
    #   if given an integer or a float, will check if int/float is the same
    def __eq__(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_mapped().__eq__(other.get_mapped()))
        if isinstance(other, basicChromo):
            retrurn (self.get_chromo().__eq__(other))
        elif isinstance(other, (int, float)):
            return self.get_fit().__eq__(other)
        else:
            try:
                return self.get_fit().__eq__(float(other))
            except:
                pass
        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)
    # Sees if fitnesses are equal to, can take int, float, or individual
    def eq_fit(self, other):
        if isinstance(other, (basicRepresentation, basicChromo)):
            return (self.get_fit().__eq__(other.get_fit()))
        elif isinstance(other, (int, float)):
            return self.get_fit().__eq__(other)
        else:
            try:
                return self.get_fit().__eq__(float(other))
            except:
                pass
        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)
    # Sees if two chromosomes are equal
    def eq_chromo(self, other):
        if isinstance(other, (basicRepresentation, basicChromo)):
            return (self.get_chromo(return_copy=False).\
                        __eq__(other.get_chromo(return_copy=False)))
        self.log.exception('Must compare another indv to another indv or chromo')
    # Sees if two mapped solutions are equal
    def eq_mapped(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_mapped().__eq__(other.get_mapped()))
        self.log.exception('Must compare another indv to another indv')

    # Sees if fitnesses are greater than, can take int, float, or individual
    def __gt__(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_fit().__gt__(other.get_fit()))
        elif isinstance(other, (int, float)):
            return (self.get_fit().__gt__(other))
        else:
            try:
                return self.get_fit().__gt__(float(other))
            except:
                pass
        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)
    # Sees if fitnesses are greater or equal to, can take int, float, or individual
    def __ge__(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_fit().__ge__(other.get_fit()))
        elif isinstance(other, (int, float)):
            return (self.get_fit().__ge__(other))
        else:
            try:
                return self.get_fit().__ge__(float(other))
            except:
                pass
        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)
    # Sees if fitnesses are less than, can take int, float, or individual
    def __lt__(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_fit().__lt__(other.get_fit()))
        elif isinstance(other, (int, float)):
            return (self.get_fit().__lt__(other))
        else:
            try:
                return self.get_fit().__lt__(float(other))
            except:
                pass

        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)
    # Sees if fitnesses are less or equal to, can take int, float, or individual
    def __le__(self, other):
        if isinstance(other, basicRepresentation):
            return (self.get_fit().__le__(other.get_fit()))
        elif isinstance(other, (int, float)):
            return (self.get_fit().__le__(other))
        else:
            try:
                return self.get_fit().__le__(float(other))
            except:
                pass
        self.log.exception('Must compare another individual or an int/float',\
                           err=TypeError)

    ''' Utility '''
    # Returns hash of contained mapped chromosome
    def __hash__(self):
        if self.mapped is None or self.get_chromo().get_fit() is None:
            self.hsh = tuple(self.get_mapped()).__hash__()
        return self.hsh
    def set_hash(self, new_hash):
        self.hsh = new_hash
    def get_hash(self):
        return self.__hash__()

    # Returns copy of the individual
    def copy(self, copy_ID=False):
        if copy_ID:
            return basicRepresentation(log_name=self.log.getLogKey(),\
                                      chromo=self.get_chromo(return_copy=True),\
                                      fit=self.get_fit(),\
                                      attrs=self.get_attrs(return_copy=True),\
                                      ID=self.get_ID())
        return basicRepresentation(log_name=self.log.getLogKey(),\
                                   chromo=self.get_chromo(return_copy=True),\
                                   fit=self.get_fit(),\
                                   attrs=self.get_attrs(return_copy=True))
    def __copy__(self):
        return self.copy()

    ''' attrs '''

    def clear_attrs(self):
        self.attrs = {}

    def set_attr(self, attr_name, value):
        self.attrs.__setitem__(attr_name, value)

    def get_attr(self, attr_name):
        return self.attrs.__getitem__(attr_name)

    def get_attrs(self, return_copy=True, add_len=True):
        if add_len:
            self.add_len_to_attrs()
        if return_copy:
            return self.attrs.copy()
        return self.attrs

    def update_attrs(self, dct):
        if not isinstance(dct, dict):
            self.log.exception('update_attrs takes a dictionary', err=TypeError)
        self.attrs.update(dct)

    def incr_attr(self, *args):
        if len(args) == 2:
            self.attrs.__setitem__(args[0], self.attrs.get(args[0], 0) + \
                                    args[1])
        elif len(args) == 1:
            self.attrs.__setitem__(args[0], self.attrs.get(args[0], 0) + 1)
        else:
            self.log.exception('Should be 1-2 arguments for incr_attr',\
                               err=ValueError)

    def add_len_to_attrs(self):
        self.set_attr('chromo_len', self.get_chromo().__len__())

    def del_attr(self, attr_name):
        del self.attrs[attr_name]

    ''' ID '''

    def get_ID(self):
        return self.ID

    @classmethod
    def __get_next_ID(self):
        ''' Returns next ID '''
        basicRepresentation.last_ID += 1
        return basicRepresentation.last_ID-1

class basicRepresentation_unittest(unittest.TestCase):

    def test_AAA_init(self):
        brep = basicRepresentation()

    def test_AAB_setchromo(self):
        logging.disable()
        brep = basicRepresentation()
        chromo = basicChromo(len=10, min=0, max=1, dtype=int)
        self.assertEqual(brep.get_chromo(return_copy=False), None, \
                         msg='failed to get chromo')
        brep.set_chromo(chromo)
        self.assertEqual(brep.get_chromo(return_copy=False), chromo, \
                         msg='failed to get chromo')
        logging.disable(logging.NOTSET)

    def test_AAC_map(self):
        logging.disable()
        brep = basicRepresentation()
        chromo = basicChromo(len=10, min=0, max=1, dtype=int)
        brep.set_chromo(chromo)
        self.assertEqual(brep.get_chromo(), chromo, msg='failed to get_chromo')
        self.assertRaises(NotImplementedError, brep.get_mapped)
        logging.disable(logging.NOTSET)


    def test_AAD_fit(self):
        logging.disable()
        brep = basicRepresentation()
        self.assertEqual(brep.get_fit(), None, msg='failed to get_fit')
        brep.set_fit(4)
        self.assertEqual(brep.get_fit(), 4, msg='failed to get_fit')
        logging.disable(logging.NOTSET)

    def test_AAE_copy(self):
        logging.disable()
        brep = basicRepresentation()
        brep.set_chromo(basicChromo(len=10, min=0, max=100, dtype=int))
        brep2 = brep.copy()
        logging.disable(logging.NOTSET)

    def test_AAF_comparison(self):
        logging.disable()
        brep = basicRepresentation()
        brep2 = basicRepresentation()
        brep.set_fit(10)
        brep2.set_fit(20)

        self.assertFalse(brep>brep2, msg='> failed')
        self.assertFalse(brep>=brep2, msg='>= failed')
        self.assertFalse(brep2<brep, msg='> failed')
        self.assertFalse(brep2<=brep, msg='>= failed')

        self.assertTrue(brep<brep2, msg='< failed')
        self.assertTrue(brep<=brep2, msg='<= failed')
        self.assertTrue(brep2>brep, msg='< failed')
        self.assertTrue(brep2>=brep, msg='<= failed')

        self.assertFalse(brep.eq_fit(brep2), msg='eq_fit failed')
        brep2.set_fit(10)
        self.assertTrue(brep.eq_fit(brep2), msg='eq_fit failed')

    def test_AAG_attrs(self):
        brep = basicRepresentation()
        self.assertTrue(brep.get_attrs(add_len=False) == {}, \
                        msg='Either get_attrs failed or started with attrs')
        brep.set_attr('x', 10)
        self.assertEqual(brep.get_attr('x'),10, msg='Failed to get_attr')
        brep.clear_attrs()
        self.assertEqual(brep.get_attrs(add_len=False),{}, msg='Failed to clear')
        brep.set_attr('x', 100)
        brep.del_attr('x')
        self.assertEqual(brep.get_attrs(add_len=False),{}, msg='Failed to del')
        brep.set_fit(10)
        self.assertEqual(brep.get_attrs(add_len=False),{'fit':10}, \
                         msg='Failed to add fit to attrs')
        brep.incr_attr('fit', 10)
        self.assertEqual(brep.get_attr('fit'),20, \
                         msg='incr_attr or get_attrs failed')
        brep.clear_attrs()
        brep.update_attrs({'test':4})
        self.assertEqual(brep.get_attrs(add_len=False), {'test':4}, msg='Failed to update')




if __name__ == '__main__':
    unittest.main()
