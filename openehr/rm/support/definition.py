
"""
The definition package, illustrated in FIGURE 8, defines symbolic definitions used by the
openEHR models. Only a small number are currently defined.
"""

class BASIC_DEFINITIONS:
    """
        Inheritance class to provide access to constants defined in other packages.
    """
    CR = '\015'
    LF = '\012'

class OPENEHR_DEFINITIONS(BASIC_DEFINITIONS):
    """
        Defines globally used constant values.
    """
    pass
