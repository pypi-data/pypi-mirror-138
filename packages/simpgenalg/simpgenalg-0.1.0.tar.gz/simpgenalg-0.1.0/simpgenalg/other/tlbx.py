from simptoolbox import toolbox
from ..structures import structures_dct
from ..selectors import selectors_dct
from ..evaluators import evaluators_dct
from ..populations import populations_dct
from ..representations import representations_dct
from ..crossovers import crossovers_dct
from ..mutations import mutations_dct

sga_tb = toolbox('simpgenalg')

total_dct = {}

total_dct.update(structures_dct)
total_dct.update(selectors_dct)
total_dct.update(evaluators_dct)
total_dct.update(populations_dct)
total_dct.update(representations_dct)
total_dct.update(crossovers_dct)
total_dct.update(mutations_dct)

sga_tb.load_dict(total_dct)
