# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.db.Table import Table as base

class Table(base):

    from Schemer import Schemer
    __metaclass__ = Schemer


    @classmethod
    def tablenameIsDefined(cls):
        '''check if this table has a user-defined name

        XXX: for backward compatibility, this also checks attribute "name".
        '''
        return hasattr(cls, 'pyredbtablename') or hasattr(cls, 'name')


    @classmethod
    def addColumn(cls, col):
        """add a new column to the table
        """
        # cf. pyre.db.Schemer

        #
        setattr(cls, col.name, col)
        
        # the registry
        colreg = cls._columnRegistry
        colreg[col.name] = col

        col.parent_table = weakref.ref(cls)

        # the writables
        if not col.auto:
            writeable = cls._writeable
            writeable.append(col.name)
        return



    def __str__(self):
        t = []
        for name, col in self._columnRegistry.iteritems():
            val = col.__get__(self)
            t.append('%s=%s' % (name, val))
            continue
        return '%s %s(%s)'% (self.getTableName(), self.id, ', '.join(t))
    

import weakref

# version
__id__ = "$Id$"

# End of file 
