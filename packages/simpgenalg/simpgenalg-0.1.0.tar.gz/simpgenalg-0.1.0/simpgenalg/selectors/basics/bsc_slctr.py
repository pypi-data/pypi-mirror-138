from ...other import basicComponent

class basicSelector(basicComponent):

    __slots__ = ('log')

    def __init__(self, *args, **kargs):
        super().__init__(self, *args, **kargs)

    def select(parents, n_sel=None, **kargs):
        self.log.exception('basicSelector does not implement select',\
                            err=NotImplementedError)

    def clear(self):
        return
