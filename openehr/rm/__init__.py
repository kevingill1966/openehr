

from functools import wraps

class RMObject(object):
    """
        Root class for all reference model classes.
        
        In Java this inherits from Serializable, which is unnecessary in python.
    """
    serialVersionUID = 1

class Attribute(object):
    """
        This will be used as a function annotation. Don't know how it would be used.
        Values can be read back from func_annotations atribute
    """
    name = required = system = None
    def __init__(self, name=None, required=False, system=False):
        self.name, self.required, self.system = name, required, system

def FullConstructor(f):
    """
        FullConstructor indicates that a constructor can take all attribute both
        required and optional to initialise the object

        Note - I don't use this in Python as there is only one construtor.
    """
    f._rm_FullConstructor = True
    return f
