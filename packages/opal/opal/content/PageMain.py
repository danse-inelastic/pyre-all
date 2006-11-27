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


from PageSection import PageSection


class PageMain(PageSection):


    def document(self, **kwds):
        from Document import Document
        document = Document(**kwds)
        self.contents.append(document)
        return document


    def __init__(self, **kwds):
        PageSection.__init__(self, cls="document-main", **kwds)
        return


# version
__id__ = "$Id: PageMain.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
