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


from AuthenticatingActor import AuthenticatingActor


class NYI(AuthenticatingActor):


    def createDocument(self, app, main):
        # populate the main column
        document = main.document(title="Not Yet Implemented")

        p = document.paragraph()
        p.text = [
            "This page is displayed whenever the user requests application functionality",
            "that is not yet implemented"
            ]

        return document


    def __init__(self, name=None):
        if name is None:
            name = "nyi"

        AuthenticatingActor.__init__(self, name)

        return


# version
__id__ = "$Id: NYI.py,v 1.1.1.1 2006-11-27 00:09:47 aivazis Exp $"

# End of file 
