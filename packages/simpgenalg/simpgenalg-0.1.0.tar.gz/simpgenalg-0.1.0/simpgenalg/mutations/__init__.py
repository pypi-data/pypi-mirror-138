#__name__ = 'simpgenalg.mutations'

from .flipbit import flipbitMutation
from .uniform import uniformRandomMutation

mutations_dct = {'flipbit':flipbitMutation,\
                 'uniform_mutation':uniformRandomMutation}
