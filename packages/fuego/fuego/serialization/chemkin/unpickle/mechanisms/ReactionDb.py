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


class ReactionDb:


    def reaction(self, reaction):
        self._reactions.append(reaction)
        return


    def size(self):
        return len(self._reactions)


    def find(self, symbol=None):
        if not symbol:
            return self._reactions

        candidates = []
        for reaction in self._reactions:
            for species, coefficient in reaction.reactants:
                if species == symbol:
                    candidates.append(reaction)
                continue
            for species, coefficient in reaction.products:
                if species == symbol:
                    candidates.append(reaction)
                continue
                
        return candidates


    def __init__(self):
        self._reactions = []
        return


# version
__id__ = "$Id: ReactionDb.py,v 1.1.1.1 2007-09-13 18:17:31 aivazis Exp $"

# End of file
