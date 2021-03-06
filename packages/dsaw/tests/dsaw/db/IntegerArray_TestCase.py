#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

class TestCase(unittest.TestCase):


    def dbManager(self):
        from dsaw.db import connect
        db = connect(db ='postgres:///test')
        db.autocommit(True)
        return db
    

    def test1(self):
        'dsaw.db.Psycopg2: integer array type'

        db = self.dbManager()

        # declare tables
        from dsaw.db.WithID import WithID
        class IntegerArrayTest(WithID):
            name = 'integerarraytest'
            import dsaw.db
            arr = dsaw.db.integerArray(name='arr')

        db.registerTable(IntegerArrayTest)
        db.createAllTables()

        t1 = IntegerArrayTest()
        t1.id = 't1'
        t1.arr = [1,2]
        db.insertRow(t1)

        t1.arr = [3,4]
        db.updateRecord(t1)
        
        db.destroyAllTables()
        return
    

    pass # end of TestCase


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
