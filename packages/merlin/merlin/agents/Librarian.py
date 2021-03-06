#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Agent import Agent


class Librarian(Agent):


    def __init__(self, name=None):
        if name is None:
            name = "librarian"

        Agent.__init__(self, name, "librarian")

        return

# version
__id__ = "$Id: Librarian.py,v 1.1.1.1 2006-11-27 00:09:42 aivazis Exp $"

# End of file 
