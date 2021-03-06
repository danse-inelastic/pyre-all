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

from BaseParser import BaseParser


class ChemkinParser(BaseParser):


    # the main parsing loop

    def parse(self, mechanism, file):
        # Reset the token counts
        import pyre
        import fuego
        import journal
        from fuego.serialization.chemkin.unpickle.tokens.Token import Token

        Token._constructed = 0
        Token._destructed = 0

        self._mechanism = mechanism
        
        # prepare the parsing machinery
        scanner = fuego.serialization.chemkin.unpickle.scanners.sections()
        tokenizer = pyre.parsing.tokenizer(file)
        tokenizer._info = journal.debug("fuego")
        
        # section parsers
        from Elements import Elements
        self._elementParser = Elements(mechanism, tokenizer)

        from Species import Species
        self._speciesParser = Species(mechanism, tokenizer)

        from Thermo import Thermo
        self._thermoParser = Thermo(mechanism, tokenizer)

        from Reactions import Reactions
        self._reactionParser = Reactions(mechanism, tokenizer)

        # enter the parsing loop

        return BaseParser.parse(self, scanner, tokenizer)


    # handlers for the section headers

    def anElementSection(self, token):
        return self._elementParser.anElementSection(token)


    def aSpeciesSection(self, token):
        return self._speciesParser.aSpeciesSection(token)


    def aThermoSection(self, token):
        return self._thermoParser.aThermoSection(token)


    def aReactionSection(self, token):
        return self._reactionParser.aReactionSection(token)


    # end-of-file handler

    def onEndOfFile(self):
        self._elementParser.onEndOfFile()
        self._speciesParser.onEndOfFile()
        self._thermoParser.onEndOfFile()
        self._reactionParser.onEndOfFile()
        return
        

    # others

    def printStatistics(self):
        print "Chemkin input file: '%s'" % self._filename
        print "    Tokens: %d-%d" % (Token._constructed, Token._destructed)
        return
    

    def __init__(self):
        BaseParser.__init__(self)

        # the table of declared species
        self._species = {}

        # section parsers
        self._elementParser = None
        self._speciesParser = None
        self._thermoParser = None
        self._reactionParser = None

        return


    def _printScanners(self):
        elements = self._elementParser._scanner._pattern()
        print "Element parser (%d): %s" % (len(elements), elements)

        species = self._speciesParser._scanner._pattern()
        print "Species parser (%d): %s" % (len(species), species)

        thermo = self._thermoParser._scanner._pattern()
        print "Thermo parser (%d): %s" % (len(thermo), thermo)

        reaction = self._reactionParser._scanner._pattern()
        print "Reaction parser (%d): %s" % (len(reaction), reaction)

        return


# version
__id__ = "$Id: ChemkinParser.py,v 1.1.1.1 2007-09-13 18:17:31 aivazis Exp $"

#
# End of file
