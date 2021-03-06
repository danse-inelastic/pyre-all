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


import journal
debug = journal.debug('dsaw.model')


class OrmManager(object):

    def __init__(self, db, guid = None, object2record = None, record2object = None, 
                 object2table = None, rules = None):
        if object2record is None:
            from Object2DBRecord import Object2DBRecord
            object2record = Object2DBRecord(object2dbtable=object2table, rules=rules)
        self.object2record = object2record

        if record2object is None:
            from DBRecord2Object import DBRecord2Object
            record2object = DBRecord2Object(object2record, db)
        self.record2object = record2object

        from ObjectFactory import ObjectFactory
        object_inventory_generator = object2record.object2dbtable.object_inventory_generator
        self.objectFactory = ObjectFactory(object_inventory_generator)

        from DeepCopier import DeepCopier
        self.deepcopier = DeepCopier(
            object_inventory_generator = object_inventory_generator,
            object_factory = self.objectFactory,
            )

        self.db = db
        self.guid = guid


        # types that are registered
        self._registered_types = []
        # tables that are registered with db manager
        self._registered_tables = []
        return


    def __call__(self, obj, rules=None):
        if inspect.isclass(obj):
            self.registerObjectType(obj)
            return self.object2record.object2dbtable(obj, rules=rules)
        return self.object2record(obj, rules=rules)


    def createAllTables(self):
        return self.db.createAllTables()


    def destroyAllTables(self):
        return self.db.destroyAllTables()


    def deepcopy(self, obj):
        return self.deepcopier(obj)


    def createInventory(self, obj):
        'create inventory for an data object'
        from dsaw.model.Inventory import establishInventoryFromObject
        i = obj.Inventory()
        return establishInventoryFromObject(i, obj)
    inv = createInventory


    def setObjectAttribute(self, obj, key, value):
        # ! slow !
        assert key in [d.name for d in obj.Inventory.getDescriptors()]
        inv = self.inv(obj)
        setattr(inv, key, value)
        from dsaw.model.Inventory import restoreObjectFromInventory
        restoreObjectFromInventory(obj, inv)
        return


    def registerObjectType(self, type):
        if type in self._registered_types: return
        
        self.object2record.object2dbtable(type)
        self._registerTables()
        self._registered_types.append(type)

        for descriptor in type.Inventory.getDescriptors():
            if descriptor.type in ['reference', 'referenceset']:

                # not polymorphic
                if not descriptor.isPolymorphic():
                    self.registerObjectType(descriptor.targettype)
                    continue

                # polymorphic
                if not descriptor.targettypes: continue
                map(self.registerObjectType, descriptor.targettypes)
                
            continue
        return


    def registerObjectTypes(self, types):
        for type in types: self.registerObjectType(type)
        return


    def getObjectTypeFromName(self, name):
        return self.object2record.object2dbtable.registry.getObjectFromName(name)
    def getObjectTypeFromTableName(self, name):
        return self.object2record.object2dbtable.registry.getObjectFromTableName(name)


    def save(self, object, save_not_owned_referred_object=True, id=None, rules=None):
        if object is None: return
        record = self.object2record(object, rules=rules)
        self._registerTables()

        try:
            self._saveRecordRecursively(
                object, record, 
                save_not_owned_referred_object=save_not_owned_referred_object, id=id)
        except: #self.db.DBEngineError:
            raise
            import traceback
            debug.log('from ormManager: '+traceback.format_exc())
            #pass
            #this is old--tables are now created within saveRecordRecursively()
            # probably this is due to the table is not created. so let us create tables
            # and try again.
#            self.createAllTables()  #this could be much more efficient by only creating the table that is missing...or better yet the table could be created right after a failed insertion instead of here and then inserted
#            self._saveRecordRecursively(
#                object, record, 
#                save_not_owned_referred_object=save_not_owned_referred_object, id=id)
            return


    def load(self, Object, id):
        import __builtin__
        if id is __builtin__.id:
            raise ValueError, "You have supplied builtin function 'id' as id"
        self.registerObjectType(Object)
        Table = self.object2record.object2dbtable(Object)
        record = self.db.query(Table).filter_by(id=id).one()
        self.db.commit()
        obj = self.record2object(record)
        return obj


    def destroy(self, object):
        db = self.db
        record = self.object2record(object)
        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            name = descriptor.name
            if type == 'reference':
                value = getattr(object.inventory, name)
                if value is None:
                    # reference does not have value, skip
                    continue
                setattr(record, name, None)
                self.db.updateRecord(record)
                if descriptor.owned:
                    self.destroy(value)
            if type == 'referenceset':
                value = getattr(object.inventory, name)
                refset = getattr(record, name)
                # the implementation here is not efficient and
                # dictates that no referred items to be referred
                # by other objects. 
                for elem in value:
                    elemrec = self.object2record(elem)
                    # remove the associateion
                    refset.delete(elemrec, db)
                    # destroy the element
                    if descriptor.owned:
                        self.destroy(elem)
                    continue
            continue
        self.db.deleteRecord(record)
        self.object2record.registry.remove(obj=object, rec=record)
        return


    def _findAllOwnedRecords(self, object):
        '''recursively find all db records that are referenced and owned by the
        given object.
        '''
        db = self.db
        record = self.object2record(object)
        for descriptor in object.Inventory.getDescriptors():
            
            # skip any reference that is not owned
            if hasattr(descriptor, 'owned') and not descriptor.owned:
                continue
            
            type = descriptor.type
            name = descriptor.name
            if type == 'reference':
                value = getattr(object.inventory, name)
                if value is None:
                    # reference does not have value, skip
                    continue
                yield self.object2record(value)
                for t in self._findAllOwnedRecords(value): yield t
            if type == 'referenceset':
                value = getattr(object.inventory, name)
                # the implementation here is not efficient and
                # dictates that no referred items to be referred
                # by other objects. 
                for elem in value:
                    elemrec = self.object2record(elem)
                    yield elemrec
                    for t in self._findAllOwnedRecords(elem): yield t
                    continue
            continue
        return


    def _registerTables(self):
        db = self.db
#        print self.object2record.object2dbtable.registry._object2table
#        print self.object2record.object2dbtable.registry._table2object
        for t in self.object2record.object2dbtable.registry.iterTables():
            if t in self._registered_tables: continue
            db.registerTable(t)
            self._registered_tables.append(t)
            continue
        return


    def _getRecordFromDB(self, record, object):
        # an object and its corresponding record are cached in the object2record
        # registry. but this record usually is not the same as the one
        # saved in database
        # this method retrieves the record from the database
        
        #first, get the id from the record or object
        if hasattr(record, 'id') and record.id!=None and len(record.id)>0: 
            id = record.id
        elif hasattr(object, 'id') and object.id!=None and len(object.id)>0: 
            id = object.id
        
        table = record.__class__
        db = self.db
        rs = db.query(table).filter_by(id=id).all()
        db.commit()
        n = len(rs)
        if n>1: raise RuntimeError
        if n==1: return rs[0]
        return 


    def _saveRecordRecursively(self, object, record, save_not_owned_referred_object=True, id=None):
        db = self.db
        #table = self.object2record.object2dbtable(object.__class__)
        
        # the old record in the database
        try:
            oldrecord = self._getRecordFromDB(record, object)
        except:
#            import traceback
#            print traceback.print_exc()
            oldrecord = None

        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            name = descriptor.name
            if type == 'reference':
                value = getattr(object.inventory, name)
                if oldrecord:
                    # convert the new referred object to a db record (not saved yet)
                    record1 = self.object2record(value)
                    # if this referred object is actually owned, more work is needed
                    if descriptor.owned:
                        # find the old referred db record
                        oldreference = getattr(oldrecord, name)
                        oldrecord1 = oldreference and oldreference.dereference(db)
                        # if the old record is the same as the new record,
                        # means the reference has not pointed to a new object,
                        # and we don't need to do extra things. Otherwise,
                        # we need to delete the old record
                        if oldrecord1 is not None and (record1 is None or oldrecord1.id != record1.id):
                            # remove the association
                            setattr(oldrecord, name, None)
                            db.updateRecord(oldrecord)
                            # remove the record
                            self._removeRecordFromDB(oldrecord1)
                if value is not None and (save_not_owned_referred_object or descriptor.owned):
                    self.save(value, save_not_owned_referred_object=save_not_owned_referred_object)
                if value is not None:
                    value = self.object2record(value)
                setattr(record, name, value)
            elif type == 'referenceset':
                if oldrecord:
                    ref = getattr(oldrecord, name)
                    for k,v in ref.dereference(db):
                        # remove item from the refset.
                        # must do this otherwise the record cannot be removed
                        ref.delete(v, db)
                        # remove the record
                        if descriptor.owned:
                            self._removeRecordFromDB(v)
                value = getattr(object.inventory, name)
                if save_not_owned_referred_object or descriptor.owned:
                    for elem in value:
                        self.save(elem, save_not_owned_referred_object=save_not_owned_referred_object)
                # the code to reestablish the reference set is at the end of
                # this method
                
            continue
        # debug.log('object: %s, %s; record: %s, %s' % (
        #   id(object), object, id(record), record.id))
        
        # it needs an id and needs to be inserted in db
        if not oldrecord:
            #first try passed id
            if id: 
                record.id = id
                object.id = id
            #then try obj.id
            elif hasattr(object, 'id'): 
                record.id = object.id
            #then try guid
            elif self.guid: 
                record.id = self.guid()
                object.id = record.id
            #then throw error
            else: raise Exception('no guid supplied')
            try:
                db.insertRow(record)
            except self.db.DBEngineError:
                db._sasession.rollback()
                self.createAllTables()
                db.insertRow(record)
#                import traceback
#                print traceback.format_exc()
               
                # if insertion failed, we should remove id from record (restore)
#                record.id = None
#                import traceback
#                raise self.db.DBEngineError, str(record) + 'not inserted in db; error: \n\n'+traceback.format_exc()
        # it has an id and a previous record
        else:
            db.updateRecord(record)

        for descriptor in object.Inventory.getDescriptors():
            type = descriptor.type
            if type == 'referenceset':
                # need to establish associations after the record is inserted
                name = descriptor.name
                value = getattr(object.inventory, name)
                refset = getattr(self.object2record(object), name)
                for elem in value:
                    elemrecord = self.object2record(elem)
                    refset.add(elemrecord, db)
                    continue
                # may establish global pointer in the process, so let us get it
                if not record.globalpointer:
                    # fetch the record from db
                    r1 = db.query(record.__class__).filter_by(id=record.id).one()
                    db.commit()
                    record.globalpointer = r1.globalpointer
        return


    def _removeRecordFromDB(self, record):
        '''remove a record (recursively) from the data base
        This record must have been saved to db using a orm manager.
        Also remove its trace in the registry managed by this orm manager.
        '''
        # clean up the object-record registry 
        registry = self.object2record.registry
        obj = registry.findObject(record)
        if obj:
            registry.remove(obj=obj, rec=registry.getRecord(obj))
        # also need to clean up the database side
        # this can be done by load the object from the db
        # and then destroy it
        obj = self.load(obj.__class__, id=record.id)
        self.destroy(obj)
        return


import inspect


# version
__id__ = "$Id$"

# End of file 
