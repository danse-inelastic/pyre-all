#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Element import Element


class IncludedStyle(Element):


    def identify(self, inspector):
        return inspector.onIncludedStyle(self)


    def __init__(self, url, **kwds):
        Element.__init__(self, 'style', **kwds)
        self.url = url
        return

# version
__id__ = "$Id: IncludedStyle.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
