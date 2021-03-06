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


class Logo(object):


    def identify(self, inspector):
        return inspector.onLogo(self)


    def __init__(self, href):
        self.href = href
        return


# version
__id__ = "$Id: Logo.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
