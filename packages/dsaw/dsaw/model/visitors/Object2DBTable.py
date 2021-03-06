# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

'''
convert an object type to a db table type.
'''


import journal
warning = journal.warning('object2dbtable')

from dsaw.db.WithID import WithID
from dsaw.db.GloballyReferrable import GloballyReferrable
class GlobalRefBase(GloballyReferrable): pass
class TableBase(WithID, GloballyReferrable): pass

class Object2DBTable(object):

    rules = {
        'str': {
          'max-length': 64,
        },
        'subclassFrom': TableBase,
        }

    def __init__(self, registry=None, rules=None, object_inventory_generator=None):
        if not registry:
            registry = Registry()
        self.registry = registry

        if not object_inventory_generator:
            from InventoryGenerator import InventoryGenerator
            object_inventory_generator = InventoryGenerator()
        self.object_inventory_generator = object_inventory_generator

        self.rules = self.__class__.rules.copy()
        if rules:
            self.rules.update(rules)
        return


    def mapped(self, object):
        return bool(self.registry.getTable(object))


    def __call__(self, object, rules=None):
        return self.registry.getTable(object) or \
               self.createTable(object, rules=rules)
        

    def createTable(self, obj, rules=None):
        if 'Inventory' not in obj.__dict__:
            try:
                Inventory = self.object_inventory_generator(obj)
            except:
                import traceback
                raise RuntimeError, "object type %s not translatable. Please manually add an inventory class to it.\n%s" %  (obj.__name__, traceback.format_exc())

            obj.Inventory = Inventory
        if not rules: rules = self.rules
        else:
            r = self.rules.copy(); r.update(rules); rules = r
        
        Inventory = obj.Inventory

        cols = []
        for descriptor in Inventory.getDescriptors():
            #print descriptor
            col = self._createColumn(descriptor, rules)
            if col:
                cols.append(col)
            continue
            
        # create a table class
        table = self._createTable(obj, cols, rules)

        self.registry.register(obj, table)
        return table


    def _createColumn(self, descriptor, rules):
        type = descriptor.type
        handler = '_on'+type.capitalize()
        handler = getattr(self, handler)
        return handler(descriptor, rules)


    def _createTable(self, object, cols, rules):
        myrules = self.rules.copy()
        myrules.update(rules)

        if 'dbtablename' in myrules:
            tname = myrules['dbtablename']
        elif 'dbtablename' in object.Inventory.__dict__:
            tname = object.Inventory.dbtablename
        else:
            tname = object.__name__.lower()

        subclassFrom = myrules['subclassFrom']
        class _(subclassFrom):
            pyredbtablename = tname

            for col in cols:
                cmd = '%s=col' % col.name
                try:
                    exec cmd
                except:
                    import traceback
                    raise RuntimeError, "failed to exec %s\n%s" % (cmd, traceback.format_exc())
                continue

            try:
                del col
            except:
                pass
        _.__name__ = object.__name__
        return _


    def _onStr(self, descriptor, rules):
        if hasattr(descriptor, 'max_length'):
            length = descriptor.max_length
        else:
            length = rules['str']['max-length']
        if hasattr(descriptor, 'constraints'):
            constraints = descriptor.constraints
        else:
            constraints = None
        return dsaw.db.varchar(name=descriptor.name, length=length, default=descriptor.default, 
                               constraints=constraints, meta=descriptor.meta)


    def _onDate(self, descriptor, rules):
        return dsaw.db.date(name=descriptor.name, default=descriptor.default)


    def _onTimestamp(self, descriptor, rules):
        return dsaw.db.timestamp(name=descriptor.name, default=descriptor.default)


    def _onFloat(self, descriptor, rules):
        return dsaw.db.real(name=descriptor.name, default=descriptor.default)


    def _onInt(self, descriptor, rules):
        return dsaw.db.integer(name=descriptor.name, default=descriptor.default)
    

    def _onBool(self, descriptor, rules):
        return dsaw.db.boolean(name=descriptor.name, default=descriptor.default)


    def _onArray(self, descriptor, rules):
        elementtype = descriptor.elementtype
        handler = '_on%sArray' % elementtype.capitalize()
        if not handler in self.__class__.__dict__:
            raise NotImplementedError
        handler = getattr(self, handler)
        return handler(descriptor, rules)


    def _onFloatArray(self, descriptor, rules):
        return dsaw.db.doubleArray(
            name=descriptor.name, default=descriptor.default,
            shape = descriptor.shape
            )


    def _onIntArray(self, descriptor, rules):
        return dsaw.db.integerArray(
            name=descriptor.name, default=descriptor.default,
            shape = descriptor.shape
            )


    def _onStrArray(self, descriptor, rules):
        if hasattr(descriptor, 'string_max_length'):
            length = descriptor.string_max_length
        else:
            length = rules['str']['max-length']
        return dsaw.db.varcharArray(
            name=descriptor.name, default=descriptor.default,
            #shape=descriptor.shape,
            length=length,
            )
    

    def _onBoolArray(self, descriptor, rules):
        return dsaw.db.booleanArray(
            name=descriptor.name, default=descriptor.default,
            shape=descriptor.shape
            )
    

    def _onReference(self, descriptor, rules):
        targettype = descriptor.targettype
        if descriptor.isPolymorphic():
            return self._onPolymorphicReference(descriptor, rules)

        table = self(targettype)
        return dsaw.db.reference(name=descriptor.name, table=table)


    def _onPolymorphicReference(self, descriptor, rules):
        return dsaw.db.versatileReference(name=descriptor.name)


    def _onReferenceset(self, descriptor, rules):
        return dsaw.db.referenceSet(name=descriptor.name)


    def _onFacility(self, descriptor, rules):
        return


            
import dsaw.db



class Registry(object):

    def __init__(self):
        self._object2table = {}
        self._table2object = {}
        self._name2object = {}
        self._tablename2object = {}
        return


    def iterTables(self):
        return self._table2object.iterkeys()


    def iterObjects(self):
        return self._object2table.iterkeys()


    def getObjectFromName(self, name):
        return self._name2object.get(name)


    def getObjectFromTableName(self, name):
        return self._tablename2object.get(name)


    def getTable(self, object):
        return self._object2table.get(object)


    def getObject(self, table):
        return self._table2object.get(table)


    def register(self, object, table):
        self._object2table[object] = table
        self._table2object[table] = object
        self._name2object[object.__name__] = object
        self._tablename2object[table.getTableName()] = object
        return
    

# version
__id__ = "$Id$"

# End of file 
