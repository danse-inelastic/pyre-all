#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2007  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Entity(object):

    _FILENAME_LIMIT = 40


    def locator(self,locator):
        self.filename = locator.source
        self.line = locator.line
        self.column = locator.column
        return


    def __init__(self, id, locator):
        self.id = id
        if locator:
            self.filename = locator.source
            self.line = locator.line
            self.column = locator.column
        else:
            self.filename = ""
            self.line = 0
            self.column = 0
        return


    def __str__(self):
        filename = self.filename
        if not filename:
            return "<unknown>"
        
        if len(filename) > self._FILENAME_LIMIT:
            filename = filename[:self._FILENAME_LIMIT/2 - 3] + \
                       "..." + filename[-self._FILENAME_LIMIT/2 + 3:]
        
        return "'%s':(%d, %d)" % (filename, self.line, self.column)


# version
__id__ = "$Id: Entity.py,v 1.1.1.1 2007-09-13 18:17:32 aivazis Exp $"

# End of file
