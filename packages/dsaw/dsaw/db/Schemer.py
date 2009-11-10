#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# Modified from pyre.db.Schemer
# 


from Column import Column
import weakref


from pyre.db.Schemer import Schemer as base

class Schemer(base):
    """scan the class record for implied attributes 
    and put those in columnRegistry.
    
    if the attribute has a value, assign it a column type appropriate for that value:
    str goes to varChar in multiples of 256 (i.e. if str type atributes has length between 1-256,
    the varChar will be of 256, if it is 474 length, the varChar will be of length 512, etc.
    int goes to 
    
    todo: add possibility of getting table name from the class name.lower()
    """

    def __init__(cls, name, bases, dict):
        # the base class will get all the publicly declared columns and make them
        # part of the registry
        base.__init__(cls, name, bases, dict)
        # TODO: when this Schemer and pyre.db Schemer are combined, this registering
        # of classes should be combined
        
        #now we get the 'implied columns' (those without an explicit declaration)
        #impliedTypes = {}
        for name, item in cls.__dict__.iteritems():

            # disregard entries that are already in the column registry
            if name in cls._columnRegistry.keys():
                continue
            # disregard metadata
            if name[:2]=='__' and name[-2:]=='__':
                continue
            # disregard functions
            if type(item).__name__=='function':
                continue

            # register it and apply automatic type detector
            cls.columnRegistry[item.name] = assignType(item)
            
            if not item.auto:
                cls.writeable.append(item.name)
        
        # now get each column and add a weak reference to it's table
        for name, item in cls._columnRegistry:
            # XXX: Jiao Lin:
            # added so that the column descriptor knows
            # the table it belongs to
            item.parent_table = weakref.ref(cls)

        return
    
    def assignType(self, item):
        # this could obviously be expanded
        import dsaw.db
        attributeType = dir(item).__name__
        if attributeType=='int':
            return dsaw.db.integer(name=item.name, default=item)
        elif attributeType=='float':
            return dsaw.db.double(name=item.name, default=item)
        elif attributeType=='list' or attributeType=='tuple':
            return dsaw.db.varcharArray(name=item.name, length=64, default=item)
        else:
            return dsaw.db.varchar(name=item.name, length=64, default=item)

            
            
            


# version
__id__ = "$Id$"

# End of file 
