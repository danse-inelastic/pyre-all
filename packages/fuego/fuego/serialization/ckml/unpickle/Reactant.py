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

from AbstractNode import AbstractNode
 

class Reactant(AbstractNode):


    tag = "reactant"


    def notify(self, parent):
        parent.onReactant(self._species, self._coefficient)
        return


    def __init__(self, root, attributes):
        AbstractNode.__init__(self, root, attributes)

        self._species = attributes["species"]
        self._coefficient = int(attributes.get("coefficient", "1"))

        return
            

# version
__id__ = "$Id: Reactant.py,v 1.1.1.1 2007-09-13 18:17:30 aivazis Exp $"

#  End of file 
