from ...other import basicComponent

class basicStructure(basicComponent):

    # Initialize the log
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    # Run the structure
    def run(self):
        raise NotImplementedError

    # Clears the components of the structure to redo
    def clear(self):
        raise NotImplementedError
