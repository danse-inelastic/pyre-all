# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Pickler(object):


    def __init__(self, db, outputdir, chunksize=None):
        self.db = db
        self.outputdir = outputdir
        self.chunksize = chunksize or 10000
        if os.path.exists(outputdir):
            raise RuntimeError, 'output directory %s already exists' % outputdir
        else:
            os.makedirs(outputdir)
        return
    

    def dump(self, table=None, tables=None):
        if tables:
            if table: tables.append(table)
        else:
            tables = [table]

        all = _order(tables)
        all.reverse()
        
        self._saveResolveOrder(all)
        for t in all:
            self._save(t)
            
        return


    def _save(self, table):
        db = self.db
        records = db.query(table).all()
        if not records: return
        
        tuples = self._toTuples(records, table)
        f = os.path.join(self.outputdir, table.getTableName())
        stream = open(f, 'w')
        import pickle
        pickle.dump(tuples, stream)
        return


    def _toTuples(self, records, table):
        from collections import namedtuple as nt
        r0 = records[0]
        names = r0.getColumnNames()
        tname = table.getTableName()
        db = self.db
        def _v(r, name):
            col = r._columnRegistry[name]
            v = r.getColumnValue(name)
            if isinstance(col, Reference):
                return v and v.id
            elif isinstance(col, VersatileReference):
                return v
            return v
        def _T(r):
            l = [_v(r,n) for n in names]
            return tuple(l)
        return tname, tuple(names), map(_T, records)


    def _findDeps(self, table):
        ret = []
        _findDeps(table, ret)
        return ret

    resolve_order_filename = 'resolve-order'
    def _saveResolveOrder(self, tables):
        tables = list(tables)
        f = os.path.join(self.outputdir, self.resolve_order_filename)
        stream = open(f, 'w')
        while tables:
            t = tables.pop()
            name = t.getTableName()
            stream.write(name+'\n')
            continue
        return 


import os
from Reference import Reference
from VersatileReference import VersatileReference

def _findDeps(table, deps):
    colreg = table._columnRegistry
    for k, v in colreg.iteritems():
        if isinstance(v, Reference):
            t = v.referred_table
            _findDeps(t, deps)
            if t not in deps:
                deps.append(t)
        continue
    return                


def _order(tables):
    r = []
    for t in tables:
        if t in r: continue
        _findDeps(t, r)
        r.append(t)
    return r


# version
__id__ = "$Id$"

# End of file 
