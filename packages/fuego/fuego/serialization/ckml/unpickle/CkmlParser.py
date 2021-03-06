#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2007 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

from pyre.xml.Parser import Parser


class CkmlParser(Parser):


    def parse(self, mechanism, file):
        # create the document root to hand to the xml Parser
        from Document import Document
        root = Document(mechanism, file.name)
        
        # parse
        return Parser.parse(self, file, root)


    def __init__(self):
        Parser.__init__(self)
        return


# version
__id__ = "$Id: CkmlParser.py,v 1.1.1.1 2007-09-13 18:17:30 aivazis Exp $"

#  End of file 
