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


def KeyboardAttributes(object):


    def identify(self, inspector):
        return inspector.onKeyboardAttributes(self)


    def __init__(self):
        self.accesskey = ''
        self.tabindex = ''
        return


# version
__id__ = "$Id: KeyboardAttributes.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
