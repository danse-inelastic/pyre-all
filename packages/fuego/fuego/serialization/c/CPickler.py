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

from pyre.weaver.mills.CMill import CMill

from pyre.units.pressure import atm
from pyre.units.SI import meter, second, mole, kelvin
from pyre.units.length import cm
from pyre.units.energy import cal, kcal, J, kJ, erg
from pyre.handbook.constants.fundamental import avogadro
from pyre.handbook.constants.fundamental import gas_constant as R

smallnum = 1e-100
R = 8.314e7 * erg/mole/kelvin
Rc = 1.987 * cal/mole/kelvin
Patm = 1013250.0
sym  = "_"

class speciesDb:
    def __init__(self, id, name, mwt):
        self.id = id
        self.symbol = name
        self.weight = mwt
        return


class CPickler(CMill):


    def __init__(self):
        CMill.__init__(self)
        self.species = []
        self.nSpecies = 0
        return


    def _setSpecies(self, mechanism):
        """ For internal use """
        import pyre.handbook
        periodic = pyre.handbook.periodicTable()
        
        nSpecies = len(mechanism.species())
        self.species = [ 0.0 for x in range(nSpecies) ]
        
        for species in mechanism.species():
            weight = 0.0 
            for elem, coef in species.composition:
                aw = mechanism.element(elem).weight
                if not aw:
                    aw = periodic.symbol(elem.capitalize()).atomicWeight
                weight += coef * aw

            tempsp = speciesDb(species.id, species.symbol, weight)
            self.species[species.id] = tempsp

        self.nSpecies = nSpecies
        return


    def _renderDocument(self, mechanism, options=None):

        self._setSpecies(mechanism)
        self._includes()
        self._declarations()

        #self._main(mechanism)

        # chemkin wrappers
        self._ckindx(mechanism)
        self._ckinit(mechanism)
        self._ckxnum(mechanism)
        self._cksnum(mechanism)
        self._cksyms(mechanism)
        self._ckrp(mechanism)
        
        self._ckpx(mechanism)
        self._ckpy(mechanism)
        self._ckpc(mechanism)
        self._ckrhox(mechanism)
        self._ckrhoy(mechanism)
        self._ckrhoc(mechanism)
        self._ckwt(mechanism)
        self._ckmmwy(mechanism)
        self._ckmmwx(mechanism)
        self._ckmmwc(mechanism)
        self._ckytx(mechanism)
        self._ckytcp(mechanism)
        self._ckytcr(mechanism)
        self._ckxty(mechanism)
        self._ckxtcp(mechanism)
        self._ckxtcr(mechanism)
        self._ckctx(mechanism)
        self._ckcty(mechanism)
        
        self._ckcpor(mechanism)
        self._ckhort(mechanism)
        self._cksor(mechanism)
        
        self._ckcvml(mechanism)
        self._ckcpml(mechanism)
        self._ckuml(mechanism)
        self._ckhml(mechanism)
        self._ckgml(mechanism)
        self._ckaml(mechanism)
        self._cksml(mechanism)
        
        self._ckcvms(mechanism)
        self._ckcpms(mechanism)
        self._ckums(mechanism)
        self._ckhms(mechanism)
        self._ckgms(mechanism)
        self._ckams(mechanism)
        self._cksms(mechanism)

        self._ckcpbl(mechanism)
        self._ckcpbs(mechanism)
        self._ckcvbl(mechanism)
        self._ckcvbs(mechanism)
        
        self._ckhbml(mechanism)
        self._ckhbms(mechanism)
        self._ckubml(mechanism)
        self._ckubms(mechanism)
        self._cksbml(mechanism)
        self._cksbms(mechanism)
        self._ckgbml(mechanism)
        self._ckgbms(mechanism)
        self._ckabml(mechanism)
        self._ckabms(mechanism)

        self._ckwc(mechanism)
        self._ckwyp(mechanism)
        self._ckwxp(mechanism)
        self._ckwyr(mechanism)
        self._ckwxr(mechanism)
        
        self._ckqc(mechanism)
        self._ckqyp(mechanism)
        self._ckqxp(mechanism)
        self._ckqyr(mechanism)
        self._ckqxr(mechanism)

        self._cknu(mechanism)
        self._ckncf(mechanism)
        
        self._ckabe(mechanism)
        
        self._ckeqc(mechanism)
        self._ckeqyp(mechanism)
        self._ckeqxp(mechanism)
        self._ckeqyr(mechanism)
        self._ckeqxr(mechanism)
        
        # Fuego Functions
        self._productionRate(mechanism)
        self._progressRate(mechanism)
        self._equilibriumConstants(mechanism)
        self._thermo(mechanism)
        self._molecularWeight(mechanism)

        # Fuego extensions
        self._ck_eytt(mechanism)
        self._ck_eytt2(mechanism)
        self._ck_phity(mechanism)
        self._ck_ytphi(mechanism)
        self._ck_ctyr(mechanism)
        self._ck_cvrhs(mechanism)
        self._ck_cvdim(mechanism)
        self._ck_zndrhs(mechanism)
        self._ck_znddim(mechanism)
        self._ck_mechfile(mechanism)
        self._ck_symnum(mechanism)
        self._ck_symname(mechanism)
        
        # Fuego Symbolic Jacobian
        self._ck_qij(mechanism)
        self._ck_jac(mechanism)
        self._ck_jay(mechanism)
        self._ck_cvjac(mechanism)
        
        return


    def _end(self):
        self._timestamp()
        self._rep += self.footer()
        return


    def _includes(self):
        self._rep += [
            '',
            '#include <math.h>',
            '#include <stdio.h>',
            '#include <string.h>',
            '#include <stdlib.h>'
            ]
        return


    def _declarations(self):
        self._rep += [
            '', '',
            self.line('function declarations'),
            '#ifdef __cplusplus',
            'extern "C" {',
            '#endif',
            'void molecularWeight(double * wt);',
            'void gibbs(double * species, double * tc);',
            'void helmholtz(double * species, double * tc);',
            'void speciesInternalEnergy(double * species, double * tc);',
            'void speciesEnthalpy(double * species, double * tc);',
            'void speciesEntropy(double * species, double * tc);',
            'void cp_R(double * species, double * tc);',
            'void cv_R(double * species, double * tc);',
            'void equilibriumConstants(double * kc, double * g_RT, double T);',
            'void productionRate(double * wdot, double * sc, double T);',
            'void progressRate(double * qdot, double * speciesConc, double T);',
            'void fgindx'+sym+'(int * iwrk, double *rwrk, int * mm, int * kk, int * ii, int * nfit );',
            'void fgxnum'+sym+'(char * line, int * nexp, int * lout, int * nval, double * rval, int * kerr, int lenline);',
            'void fgsnum'+sym+'(char * line, int * nexp, int * lout, char * kray, int * nn, int * knum, int * nval, double * rval, int * kerr, int lenline, int lenkray);',
            'void fgsyms'+sym+'(char * cckwrk, int * lout, char * kname, int * kerr, int lencck, int lenkname);',
            'void fgrp'+sym+'(int * ickwrk, double * rckwrk, double * ru, double * ruc, double * pa);',
            'void fgpx'+sym+'(double * rho, double * T, double * x, int * iwrk, double *rwrk, double * P);',
            'void fgpy'+sym+'(double * rho, double * T, double * y, int * iwrk, double *rwrk, double * P);',
            'void fgpc'+sym+'(double * rho, double * T, double * c, int * iwrk, double *rwrk, double * P);',
            'void fgrhox'+sym+'(double * P, double * T, double * x, int * iwrk, double *rwrk, double * rho);',
            'void fgrhoy'+sym+'(double * P, double * T, double * y, int * iwrk, double *rwrk, double * rho);',
            'void fgrhoc'+sym+'(double * P, double * T, double * c, int * iwrk, double *rwrk, double * rho);',
            'void fgwt'+sym+'(int * iwrk, double *rwrk, double * wt);',
            'void fgmmwy'+sym+'(double * y, int * iwrk, double * rwrk, double * wtm);',
            'void fgmmwx'+sym+'(double * x, int * iwrk, double * rwrk, double * wtm);',
            'void fgmmwc'+sym+'(double * c, int * iwrk, double * rwrk, double * wtm);',
            'void fgytx'+sym+'(double * y, int * iwrk, double * rwrk, double * x);',
            'void fgytcp'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * c);',
            'void fgytcr'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * c);',
            'void fgxty'+sym+'(double * x, int * iwrk, double * rwrk, double * y);',
            'void fgxtcp'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * c);',
            'void fgxtcr'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * c);',
            'void fgctx'+sym+'(double * c, int * iwrk, double * rwrk, double * x);',
            'void fgcty'+sym+'(double * c, int * iwrk, double * rwrk, double * y);',
            'void fgcpor'+sym+'(double * T, int * iwrk, double * rwrk, double * cpor);',
            'void fghort'+sym+'(double * T, int * iwrk, double * rwrk, double * hort);',
            'void fgsor'+sym+'(double * T, int * iwrk, double * rwrk, double * sor);',
            
            'void fgcvml'+sym+'(double * T, int * iwrk, double * rwrk, double * cvml);',
            'void fgcpml'+sym+'(double * T, int * iwrk, double * rwrk, double * cvml);',
            'void fguml'+sym+'(double * T, int * iwrk, double * rwrk, double * uml);',
            'void fghml'+sym+'(double * T, int * iwrk, double * rwrk, double * uml);',
            'void fggml'+sym+'(double * T, int * iwrk, double * rwrk, double * gml);',
            'void fgaml'+sym+'(double * T, int * iwrk, double * rwrk, double * aml);',
            'void fgsml'+sym+'(double * T, int * iwrk, double * rwrk, double * sml);',
            
            'void fgcvms'+sym+'(double * T, int * iwrk, double * rwrk, double * cvms);',
            'void fgcpms'+sym+'(double * T, int * iwrk, double * rwrk, double * cvms);',
            'void fgums'+sym+'(double * T, int * iwrk, double * rwrk, double * ums);',
            'void fghms'+sym+'(double * T, int * iwrk, double * rwrk, double * ums);',
            'void fggms'+sym+'(double * T, int * iwrk, double * rwrk, double * gms);',
            'void fgams'+sym+'(double * T, int * iwrk, double * rwrk, double * ams);',
            'void fgsms'+sym+'(double * T, int * iwrk, double * rwrk, double * sms);',
            
            'void fgcpbl'+sym+'(double * T, double * x, int * iwrk, double * rwrk, double * cpbl);',
            'void fgcpbs'+sym+'(double * T, double * y, int * iwrk, double * rwrk, double * cpbs);',
            'void fgcvbl'+sym+'(double * T, double * x, int * iwrk, double * rwrk, double * cpbl);',
            'void fgcvbs'+sym+'(double * T, double * y, int * iwrk, double * rwrk, double * cpbs);',
            
            'void fghbml'+sym+'(double * T, double * x, int * iwrk, double * rwrk, double * hbml);',
            'void fghbms'+sym+'(double * T, double * y, int * iwrk, double * rwrk, double * hbms);',
            'void fgubml'+sym+'(double * T, double * x, int * iwrk, double * rwrk, double * ubml);',
            'void fgubms'+sym+'(double * T, double * y, int * iwrk, double * rwrk, double * ubms);',
            'void fgsbml'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * sbml);',
            'void fgsbms'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * sbms);',
            'void fggbml'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * gbml);',
            'void fggbms'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * gbms);',
            'void fgabml'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * abml);',
            'void fgabms'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * abms);',

            
            'void fgwc'+sym+'(double * T, double * C, int * iwrk, double *rwrk, double * wdot);',
            'void fgwyp'+sym+'(double * P, double * T, double * y, int * iwrk, double *rwrk, double * wdot);',
            'void fgwxp'+sym+'(double * P, double * T, double * x, int * iwrk, double *rwrk, double * wdot);',
            'void fgwyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double *rwrk, double * wdot);',
            'void fgwxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double *rwrk, double * wdot);',

            
            'void fgqc'+sym+'(double * T, double * C, int * iwrk, double *rwrk, double * qdot);',
            'void fgqyp'+sym+'(double * P, double * T, double * y, int * iwrk, double *rwrk, double * qdot);',
            'void fgqxp'+sym+'(double * P, double * T, double * x, int * iwrk, double *rwrk, double * qdot);',
            'void fgqyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double *rwrk, double * qdot);',
            'void fgqxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double *rwrk, double * qdot);',
            
            'void fgnu'+sym+'(int * kdim, int * iwrk, double *rwrk, int * nuki);',
            'void fgncf'+sym+'(int * mdim, int * iwrk, double *rwrk, int * ncf);',
            
            'void fgabe'+sym+'(int * iwrk, double *rwrk, double * a, double * b, double * e );',
            'void fgeqc'+sym+'(double * T, double * C , int * iwrk, double *rwrk, double * eqcon );',
            'void fgeqyp'+sym+'(double * P, double * T, double * y, int * iwrk, double *rwrk, double * eqcon);',
            'void fgeqxp'+sym+'(double * P, double * T, double * x, int * iwrk, double *rwrk, double * eqcon);',
            'void fgeqyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double *rwrk, double * eqcon);',
            'void fgeqxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double *rwrk, double * eqcon);',
            'int  feeytt'+sym+'(double * e, double * y, int * iwrk, double *rwrk, double * t);',
            'int  feeytt2'+sym+'(double * e, double * y, int * iwrk, double *rwrk, double * t);',
            'void fephity'+sym+'(double * phi, int * iwrk, double *rwrk, double * y);',
            'void feytphi'+sym+'(double * y, int * iwrk, double *rwrk, double * phi);',
            'void fectyr'+sym+'(double * c, double * rho, int * iwrk, double *rwrk, double * y);',

            'void fecvrhs'+sym+'(double * time, double * phi, double * phidot, double * rckwrk, int * ickwrk);',
            'int fecvdim'+sym+'();',
            'void fezndrhs'+sym+'(double * time, double * z, double * zdot, double * rckwrk, int * ickwrk);',
            'int feznddim'+sym+'();',
            'char* femechfile'+sym+'();',
            'char* fesymname'+sym+'(int sn);',
            'int fesymnum'+sym+'(const char* s1);',
            
            'void feqij'+sym+'(int *kdim, double *qij, double *sc, double *T);',
            'void fejac'+sym+'(double *T, double *sc, double *jac);',
            'void fejay'+sym+'(double *rho, double *T, double *y, double *jac);',
            '#ifdef __cplusplus',
            '}',
            '#endif',
            ]
        return


    def _main(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('optional test program'))
        self._write('int main()')
        self._write('{')
        self._indent()

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        # declarations
        self._write('int species;')
        self._write('int reaction;')

        self._write('double T;')
        self._write('double q_dot[%d];' % nReactions)
        self._write('double wdot[%d];' % nSpecies)
        self._write('double sc[%d];' % nSpecies)
        self._write('double uml[%d];' % nSpecies)
        self._write('double rckdummy[%d];' % nSpecies)
        self._write('int    ickdummy[%d];' % nSpecies)

        # set the temperature
        self._write()
        self._write('T = 1000.0;')

        # compute ckuml 
        self._write()
        self._write(self.line('compute the internal energy'))
        self._write('ckuml(&T, ickdummy, rckdummy, uml);')
        
        # print
        self._write()
        self._write('for (species = 0; species < %d; ++species) {' % nSpecies)
        self._indent()
        self._write('printf(" e: %5d   %15.7e\\n", species+1, uml[species]);')
        self._outdent()
        self._write('}')


        # compute the gibbs free energy
        # self._write()
        # self._write(self.line('compute the Gibbs free energy'))
        # self._write('gibbs(g_RT, T);')

        # compute the equilibrium constants
        # self._write()
        # self._write(self.line('compute the equilibrium constants'))
        # self._write('equilibriumConstants(kc, g_RT, T);')

        self._write('for (species = 0; species < %d; ++species) {' % nSpecies)
        self._indent()
        self._write('sc[species] = 1.0e6;')
        self._outdent()
        self._write('}')

        # compute the production rates
        self._write()
        self._write(self.line('compute the production rate'))
        self._write('productionRate(wdot, sc, T);')

        # compute the progress rates
        # self._write()
        # self._write(self.line('compute the progress rates'))
        # self._write('progressRate(q_dot, sc, T);')

        # print
        self._write()
        self._write('for (species = 0; species < %d; ++species) {' % nSpecies)
        self._indent()
        self._write('printf("%5d   %15.7e\\n", species+1, wdot[species]);')
        self._outdent()
        self._write('}')

        # print
        # self._write()
        # self._write('for (reaction = 0; reaction < %d; ++reaction) {' % nReactions)
        # self._indent()
        # self._write('printf("%5d | %15.7e\\n", reaction+1, q_dot[reaction]);')
        # self._write('}')
        # self._outdent()

        # done
        self._write()
        self._write('return 0;')

        self._outdent()
        self._write('}')
        return


    def _thermo(self, mechanism):
        speciesInfo = self._analyzeThermodynamics(mechanism)

        self._gibbs(speciesInfo)
        self._helmholtz(speciesInfo)
        self._cv(speciesInfo)
        self._cp(speciesInfo)
        self._speciesInternalEnergy(speciesInfo)
        self._speciesEnthalpy(speciesInfo)
        self._speciesEntropy(speciesInfo)

        return


    def _ckxnum(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(' ckxnum... for parsing strings '))
        self._write('void fgxnum'+sym+'(char * line, int * nexp, int * lout, int * nval, double * rval, int * kerr, int lenline )')
        self._write('{')
        self._indent()

        self._write('int n,i; ' + self.line('Loop Counters'))
        self._write('char *p; ' + self.line('String Tokens'))
        self._write('char cstr[1000];')

        self._write(self.line(' Strip Comments '))
        self._write('for (i=0; i<lenline; ++i) {')
        self._indent()
        self._write('if (line[i]==\'!\') {')
        self._indent()
        self._write('cstr[i] = \'\\0\';')
        self._write('break;')
        self._outdent()
        self._write('}')
        self._write('cstr[i] = line[i];')
        self._outdent()
        self._write('}')

        self._write()
        self._write('p = strtok(cstr," ");')
        self._write('if (!p) {')
        self._indent()
        self._write('*nval = 0;')
        self._write('*kerr = 1;')
        self._write('return;')
        self._outdent()
        self._write('}')

        self._write('for (n=0; n<*nexp; ++n) {')
        self._indent()
        self._write('rval[n] = atof(p);')
        self._write('p = strtok(NULL, " ");');
        self._write('if (!p) break;')
        self._outdent()
        self._write('}')
        self._write('*nval = n+1;')
        self._write('if (*nval < *nexp) *kerr = 1;')
        self._write('return;')
        
                   
        # done
        self._outdent()
        self._write('}')
        return


    def _cksnum(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(' cksnum... for parsing strings '))
        self._write('void fgsnum'+sym+'(char * line, int * nexp, int * lout, char * kray, int * nn, int * knum, int * nval, double * rval, int * kerr, int lenline, int lenkray)')
        self._write('{')
        self._indent()
        
        self._write(self.line('Not done yet ...'))
        
        # done
        self._outdent()
        self._write('}')
        return

    def _ckrp(self, mechanism):
        self._write()
        self._write()
        self._write(
            self.line(' Returns R, Rc, Patm' ))
        self._write('void fgrp'+sym+'(int * ickwrk, double * rckwrk, double * ru, double * ruc, double * pa)')
        self._write('{')
        self._indent()
        
        self._write(' *ru  = %g; ' % (R * mole * kelvin / erg))
        self._write(' *ruc = %g; ' % (Rc * mole * kelvin / cal))
        self._write(' *pa  = %g; ' % (Patm) )
        
        # done
        self._outdent()
        self._write('}')
        return

    def _cksyms(self, mechanism):

        nSpecies = len(mechanism.species())
        
        self._write()
        self._write()
        self._write(
            self.line(' Returns the char strings of species names'))
        self._write('void fgsyms'+sym+'(char * cckwrk, int * lout, char * kname, int * kerr, int lencck, int lenkname )')
        self._write('{')
        self._indent()
        
        self._write('int i; '+self.line('Loop Counter'))
        self._write(self.line('clear kname'))
        self._write('for (i=0; i<lenkname*%d; i++) {' % nSpecies)
        self._indent()
        self._write('kname[i] = \' \';')
        self._outdent()
        self._write('}')
        self._write()
        for species in mechanism.species():
            self._write(self.line(' %s ' % species.symbol))
            ii = 0
            for char in species.symbol:
                self._write('kname[ %d*lenkname + %d ] = \'%s\';' %
                           (species.id, ii, char.capitalize()))
                ii = ii+1
            self._write('kname[ %d*lenkname + %d ] = \' \';' %
                           (species.id, ii))
            self._write()

        # done
        self._outdent()
        self._write('}')
        return


    def _ckinit(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Dummy ckinit'))
        self._write('void fginit'+sym+'(int * leniwk, int * lenrwk, int * lencwk, int * linc, int * lout, int * ickwrk, double * rckwrk, char * cckwrk )')
        self._write('{')
        self._indent()
        self._write('if ((*lout) != 0) {')
        self._indent()
        self._write('printf(" ***       Congratulations       *** \\n");')
        self._write('printf(" * You are using the Fuego Library * \\n");')
        self._write('printf(" *****    Say NO to cklib.f    ***** \\n");')
        self._outdent()
        self._write('}')
        
        # done
        self._outdent()
        self._write('}')
        return
    

    def _ckindx(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('A few mechanism parameters'))
        self._write('void fgindx'+sym+'(int * iwrk, double * rwrk, int * mm, int * kk, int * ii, int * nfit)')
        self._write('{')
        self._indent()
        self._write('*mm = %d;' % len(mechanism.element()))
        self._write('*kk = %d;' % len(mechanism.species()))
        self._write('*ii = %d;' % len(mechanism.reaction()))
        self._write('*nfit = -1; ' + self.line(
            'Why do you need this anyway ? '))
        
        # done
        self._outdent()
        self._write('}')
        return
        
        
    def _ckpx(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute P = rhoRT/W(x)'))
        self._write('void fgpx'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * P)')
        self._write('{')
        self._indent()

        self._write('double XW = 0;'+
                    self.line(' To hold mean molecular wt'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write(
            '*P = *rho * %g * (*T) / XW; ' % (R*kelvin*mole/erg)
            + self.line('P = rho*R*T/W'))
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')
        return

    def _ckpy(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute P = rhoRT/W(y)'))
        self._write('void fgpy'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * P)')
        self._write('{')
        self._indent()

        self._write('double YOW = 0;'+self.line(' for computing mean MW'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self.line('YOW holds the reciprocal of the mean molecular wt')
        self._write(
            '*P = *rho * %g * (*T) * YOW; ' % (R*kelvin*mole/erg)
            + self.line('P = rho*R*T/W'))
        
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckpc(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute P = rhoRT/W(c)'))
        self._write('void fgpc'+sym+'(double * rho, double * T, double * c, int * iwrk, double * rwrk, double * P)')
        
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write(self.line('See Eq 5 in CK Manual'))
        self._write('double W = 0;')
        self._write('double sumC = 0;')
        
        # molecular weights of all species
        for species in self.species:
            self._write('W += c[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write()
        nSpecies = len(mechanism.species())
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('sumC += c[id];')
        self._outdent()
        self._write('}')

        self.line('W/sumC holds the mean molecular wt')
        self._write(
            '*P = *rho * %g * (*T) * sumC / W; ' % (R*kelvin*mole/erg)
            + self.line('P = rho*R*T/W'))
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 

    def _ckrhox(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute rho = PW(x)/RT'))
        self._write('void fgrhox'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * rho)')
        self._write('{')
        self._indent()

        self._write('double XW = 0;'+
                    self.line(' To hold mean molecular wt'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write(
            '*rho = *P * XW / (%g * (*T)); ' % (R*kelvin*mole/erg)
            + self.line('rho = P*W/(R*T)'))
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')
        return

    def _ckrhoy(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute rho = P*W(y)/RT'))
        self._write('void fgrhoy'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * rho)')
        self._write('{')
        self._indent()

        self._write('double YOW = 0;'+self.line(' for computing mean MW'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self.line('YOW holds the reciprocal of the mean molecular wt')
        self._write(
            '*rho = *P / (%g * (*T) * YOW); ' % (R*kelvin*mole/erg)
            + self.line('rho = P*W/(R*T)'))
        
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckrhoc(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Compute rho = P*W(c)/(R*T)'))
        self._write('void fgrhoc'+sym+'(double * P, double * T, double * c, int * iwrk, double * rwrk, double * rho)')
        
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write(self.line('See Eq 5 in CK Manual'))
        self._write('double W = 0;')
        self._write('double sumC = 0;')
        
        # molecular weights of all species
        for species in self.species:
            self._write('W += c[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write()
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('sumC += c[id];')
        self._outdent()
        self._write('}')

        self.line('W/sumC holds the mean molecular wt')
        self._write(
            '*rho = *P * W / (sumC * (*T) * %g); ' % (R*kelvin*mole/erg)
            + self.line('rho = PW/(R*T)'))
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 

    def _ckwt(self, mechanism):

        self._write()
        self._write()
        self._write(self.line('get molecular weight for all species'))
        self._write('void fgwt'+sym+'(int * iwrk, double * rwrk, double * wt)')
        self._write('{')
        self._indent()

        # call moleuclarWeight
        self._write('molecularWeight(wt);')
        
        self._outdent()

        self._write('}')

        return
      
    def _ckcvml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get specific heat at constant volume as a function '))
        self._write(self.line('of T for all species (molar units)'))
        self._write('void fgcvml'+sym+'(double *T, int * iwrk, double * rwrk, double * cvml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('cv_R(cvml, tc);')
        
        # convert cv/R to cv
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('cvml[id] *= %g;' % (R*kelvin*mole/erg) )
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
       
    def _ckcpml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get specific heat at constant pressure as a '))
        self._write(self.line('function of T for all species (molar units)'))
        self._write('void fgcpml'+sym+'(double *T, int * iwrk, double * rwrk, double * cpml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('cp_R(cpml, tc);')
        
        # convert cp/R to cp
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('cpml[id] *= %g;' % (R*kelvin*mole/erg) )
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
     
    def _ckuml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get internal energy as a function '))
        self._write(self.line('of T for all species (molar units)'))
        self._write('void fguml'+sym+'(double *T, int * iwrk, double * rwrk, double * uml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesInternalEnergy(uml, tc);')
        
        # convert e/RT to e with molar units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('uml[id] *= RT;')
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
      
    def _ckhml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get enthalpy as a function '))
        self._write(self.line('of T for all species (molar units)'))
        self._write('void fghml'+sym+'(double *T, int * iwrk, double * rwrk, double * hml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesEnthalpy(hml, tc);')
        
        # convert h/RT to h with molar units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('hml[id] *= RT;')
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
    
    def _ckgml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get standard-state Gibbs energy as a function '))
        self._write(self.line('of T for all species (molar units)'))
        self._write('void fggml'+sym+'(double *T, int * iwrk, double * rwrk, double * gml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('gibbs(gml, tc);')
        
        # convert g/RT to g with molar units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('gml[id] *= RT;')
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
    
    def _ckaml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get standard-state Helmholtz free energy as a '))
        self._write(self.line('function of T for all species (molar units)'))
        self._write('void fgaml'+sym+'(double *T, int * iwrk, double * rwrk, double * aml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('helmholtz(aml, tc);')
        
        # convert A/RT to A with molar units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('aml[id] *= RT;')
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
   
    def _cksml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the standard-state entropies in molar units'))
        self._write('void fgsml'+sym+'(double *T, int * iwrk, double * rwrk, double * sml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('speciesEntropy(sml, tc);')
        
        # convert s/R to s
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('sml[id] *= %g;' % (R*kelvin*mole/erg) )
        self._outdent()
        self._write('}')
       
        self._outdent()

        self._write('}')

        return
 
    def _ckums(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns internal energy in mass units (Eq 30.)'))
        self._write('void fgums'+sym+'(double *T, int * iwrk, double * rwrk, double * ums)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesInternalEnergy(ums, tc);')
        

        # convert e/RT to e with mass units
        for species in self.species:
            self._write('ums[%d] *= RT/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return
 
    def _ckhms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns enthalpy in mass units (Eq 27.)'))
        self._write('void fghms'+sym+'(double *T, int * iwrk, double * rwrk, double * hms)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesEnthalpy(hms, tc);')
        

        # convert h/RT to h with mass units
        for species in self.species:
            self._write('hms[%d] *= RT/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return

    def _ckams(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns helmholtz in mass units (Eq 32.)'))
        self._write('void fgams'+sym+'(double *T, int * iwrk, double * rwrk, double * ams)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('helmholtz(ams, tc);')
        

        # convert A/RT to A with mass units
        for species in self.species:
            self._write('ams[%d] *= RT/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return

    def _ckgms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns gibbs in mass units (Eq 31.)'))
        self._write('void fggms'+sym+'(double *T, int * iwrk, double * rwrk, double * gms)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('gibbs(gms, tc);')
        

        # convert g/RT to g with mass units
        for species in self.species:
            self._write('gms[%d] *= RT/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return


    def _ckcvms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the specific heats at constant volume'))
        self._write(self.line('in mass units (Eq. 29)'))
        self._write('void fgcvms'+sym+'(double *T, int * iwrk, double * rwrk, double * cvms)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('cv_R(cvms, tc);')

        # convert cv/R to cv with mass units
        self._write(self.line('multiply by R/molecularweight'))
        for species in self.species:
            ROW = (R*kelvin*mole/erg) / species.weight
            self._write('cvms[%d] *= %f; ' % (
                species.id, ROW) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return

    def _ckcpms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the specific heats at constant pressure'))
        self._write(self.line('in mass units (Eq. 26)'))
        self._write('void fgcpms'+sym+'(double *T, int * iwrk, double * rwrk, double * cpms)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('cp_R(cpms, tc);')
        

        # convert cp/R to cp with mass units
        self._write(self.line('multiply by R/molecularweight'))
        for species in self.species:
            ROW = (R*kelvin*mole/erg) / species.weight
            self._write('cpms[%d] *= %f; ' % (
                species.id, ROW) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return

    def _cksms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the entropies in mass units (Eq 28.)'))
        self._write('void fgsms'+sym+'(double *T, int * iwrk, double * rwrk, double * sms)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('speciesEntropy(sms, tc);')
        

        # convert s/R to s with mass units
        self._write(self.line('multiply by R/molecularweight'))
        for species in self.species:
            ROW = (R*kelvin*mole/erg) / species.weight
            self._write('sms[%d] *= %f; ' % (
                species.id, ROW) + self.line('%s' % species.symbol))

       
        self._outdent()

        self._write('}')

        return
    
    def _ckcpbl(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the mean specific heat at CP (Eq. 33)'))
        self._write('void fgcpbl'+sym+'(double *T, double *x, int * iwrk, double * rwrk, double * cpbl)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double cpor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write('cp_R(cpor, tc);')
        
        # dot product
        self._write()
        self._write(self.line('perform dot product'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*cpor[id];')
        self._outdent()
        self._write('}')

        self._write()
        self._write('*cpbl = result * %g;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return
 
    def _ckcpbs(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the mean specific heat at CP (Eq. 34)'))
        self._write('void fgcpbs'+sym+'(double *T, double *y, int * iwrk, double * rwrk, double * cpbs)')
        self._write('{')
        self._indent()

        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double cpor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write('cp_R(cpor, tc);')
        
        # do dot product
        self._write(self.line('multiply by y/molecularweight'))
        for species in self.species:
            self._write('result += cpor[%d]*y[%d]/%g; ' % (
                species.id, species.id, species.weight) + self.line('%s' % species.symbol))

        self._write()
        self._write('*cpbs = result * %g;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return
   
    def _ckcvbl(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the mean specific heat at CV (Eq. 35)'))
        self._write('void fgcvbl'+sym+'(double *T, double *x, int * iwrk, double * rwrk, double * cvbl)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double cvor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write('cv_R(cvor, tc);')
        
        # dot product
        self._write()
        self._write(self.line('perform dot product'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*cvor[id];')
        self._outdent()
        self._write('}')

        self._write()
        self._write('*cvbl = result * %g;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return

    def _ckcvbs(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the mean specific heat at CV (Eq. 36)'))
        self._write('void fgcvbs'+sym+'(double *T, double *y, int * iwrk, double * rwrk, double * cvbs)')
        self._write('{')
        self._indent()

        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double cvor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write('cv_R(cvor, tc);')
        
        # do dot product
        self._write(self.line('multiply by y/molecularweight'))
        for species in self.species:
            self._write('result += cvor[%d]*y[%d]/%g; ' % (
                species.id, species.id, species.weight) + self.line('%s' % species.symbol))

        self._write()
        self._write('*cvbs = result * %g;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return
    
    def _ckhbml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the mean enthalpy of the mixture in molar units'))
        self._write('void fghbml'+sym+'(double *T, double *x, int * iwrk, double * rwrk, double * hbml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double hml[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesEnthalpy(hml, tc);')
        
        # dot product
        self._write()
        self._write(self.line('perform dot product'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*hml[id];')
        self._outdent()
        self._write('}')

        self._write()
        self._write('*hbml = result * RT;')
        
        self._outdent()

        self._write('}')

        return
 
 
    def _ckhbms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns mean enthalpy of mixture in mass units'))
        self._write('void fghbms'+sym+'(double *T, double *y, int * iwrk, double * rwrk, double * hbms)')
        self._write('{')
        self._indent()

        self._write('double result = 0;')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double hml[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesEnthalpy(hml, tc);')

        # convert e/RT to e with mass units
        self._write(self.line('perform dot product + scaling by wt'))
        for species in self.species:
            self._write('result += y[%d]*hml[%d]/%f; ' % (
                species.id, species.id, species.weight)
                        + self.line('%s' % species.symbol))

        
        self._write()
        # finally, multiply by RT
        self._write('*hbms = result * RT;')
        
        self._outdent()

        self._write('}')
        
        return
    
    def _ckubml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get mean internal energy in molar units'))
        self._write('void fgubml'+sym+'(double *T, double *x, int * iwrk, double * rwrk, double * ubml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double uml[%d]; ' % self.nSpecies + self.line(' temporary energy array'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesInternalEnergy(uml, tc);')
        
        # dot product
        self._write()
        self._write(self.line('perform dot product'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*uml[id];')
        self._outdent()
        self._write('}')

        self._write()
        self._write('*ubml = result * RT;')
        
        self._outdent()

        self._write('}')

        return
 
    def _ckubms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get mean internal energy in mass units'))
        self._write('void fgubms'+sym+'(double *T, double *y, int * iwrk, double * rwrk, double * ubms)')
        self._write('{')
        self._indent()

        self._write('double result = 0;')
        
        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double ums[%d]; ' % self.nSpecies + self.line(' temporary energy array'))
        
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        
        # call routine
        self._write('speciesInternalEnergy(ums, tc);')

        # convert e/RT to e with mass units
        self._write(self.line('perform dot product + scaling by wt'))
        for species in self.species:
            self._write('result += y[%d]*ums[%d]/%f; ' % (
                species.id, species.id, species.weight)
                        + self.line('%s' % species.symbol))

        
        self._write()
        # finally, multiply by RT
        self._write('*ubms = result * RT;')
        
        self._outdent()

        self._write('}')
        
        return
 
    def _cksbml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get mixture entropy in molar units'))
        self._write('void fgsbml'+sym+'(double *P, double *T, double *x, int * iwrk, double * rwrk, double * sbml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double sor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        
        # call routine
        self._write('speciesEntropy(sor, tc);')
        
        # Equation 42
        self._write()
        self._write(self.line('Compute Eq 42'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*(sor[id]-log((x[id]+%g))-logPratio);' %
                    smallnum )
        self._outdent()
        self._write('}')

        self._write()
        
        self._write('*sbml = result * %g;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return

    def _cksbms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get mixture entropy in mass units'))
        self._write('void fgsbms'+sym+'(double *P, double *T, double *y, int * iwrk, double * rwrk, double * sbms)')
        self._write('{')
        self._indent()

        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double sor[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        self._write(
            'double x[%d]; ' % self.nSpecies + self.line(' need a ytx conversion'))

        self._write('double YOW = 0; '+self.line('See Eq 4, 6 in CK Manual'))
        
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        # now to ytx
        self._write(self.line('Now compute y to x conversion'))
        for species in self.species:
            self._write('x[%d] = y[%d]/(%f*YOW); ' % (
                species.id, species.id, species.weight) )
            
        # call routine
        self._write('speciesEntropy(sor, tc);')
        
        # Equation 42 and 43
        self._write(self.line('Perform computation in Eq 42 and 43'))
        for species in self.species:
            self._write('result += x[%d]*(sor[%d]-log((x[%d]+%g))-logPratio);' %
                        (species.id, species.id, species.id, smallnum) )

        self._write(self.line('Scale by R/W'))
        self._write('*sbms = result * %g * YOW;' % (R*kelvin*mole/erg) )
        
        self._outdent()

        self._write('}')

        return

    def _ckgbml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns mean gibbs free energy in molar units'))
        self._write('void fggbml'+sym+'(double *P, double *T, double *x, int * iwrk, double * rwrk, double * gbml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        self._write(
            'double gort[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write(self.line('Compute g/RT'))
        self._write('gibbs(gort, tc);')
        
        # Equation 44
        self._write()
        self._write(self.line('Compute Eq 44'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*(gort[id]+log((x[id]+%g))+logPratio);' %
                    smallnum )
        self._outdent()
        self._write('}')

        self._write()
        
        self._write('*gbml = result * RT;')
        
        self._outdent()

        self._write('}')

        return


    def _ckgbms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns mixture gibbs free energy in mass units'))
        self._write('void fggbms'+sym+'(double *P, double *T, double *y, int * iwrk, double * rwrk, double * gbms)')
        self._write('{')
        self._indent()

        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        self._write(
            'double gort[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        self._write(
            'double x[%d]; ' % self.nSpecies + self.line(' need a ytx conversion'))

        self._write(
            'double YOW = 0; '
            + self.line('To hold 1/molecularweight'))
        
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        # now to ytx
        self._write(self.line('Now compute y to x conversion'))
        for species in self.species:
            self._write('x[%d] = y[%d]/(%f*YOW); ' % (
                species.id, species.id, species.weight) )
            
        # call routine
        self._write('gibbs(gort, tc);')
        
        # Equation 42 and 43
        self._write(self.line('Perform computation in Eq 44'))
        for species in self.species:
            self._write('result += x[%d]*(gort[%d]+log((x[%d]+%g))+logPratio);' %
                        (species.id, species.id, species.id, smallnum) )

        self._write(self.line('Scale by RT/W'))
        self._write('*gbms = result * RT * YOW;')
        
        self._outdent()

        self._write('}')

        return
    

    def _ckabml(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns mean helmholtz free energy in molar units'))
        self._write('void fgabml'+sym+'(double *P, double *T, double *x, int * iwrk, double * rwrk, double * abml)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        self._write(
            'double aort[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        
        # call routine
        self._write(self.line('Compute g/RT'))
        self._write('helmholtz(aort, tc);')
        
        # Equation 44
        self._write()
        self._write(self.line('Compute Eq 44'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('result += x[id]*(aort[id]+log((x[id]+%g))+logPratio);' %
                    smallnum )
        self._outdent()
        self._write('}')

        self._write()
        
        self._write('*abml = result * RT;')
        
        self._outdent()

        self._write('}')

        return
    

    def _ckabms(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns mixture helmholtz free energy in mass units'))
        self._write('void fgabms'+sym+'(double *P, double *T, double *y, int * iwrk, double * rwrk, double * abms)')
        self._write('{')
        self._indent()

        self._write('double result = 0; ')
        
        # get temperature cache
        self._write(self.line('Log of normalized pressure in cgs units dynes/cm^2 by Patm'))
        self._write( 'double logPratio = log ( *P / 1013250.0 ); ')
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double RT = %g*tT; ' % (R*kelvin*mole/erg)
            + self.line('R*T'))
        self._write(
            'double aort[%d]; ' % self.nSpecies + self.line(' temporary storage'))
        self._write(
            'double x[%d]; ' % self.nSpecies + self.line(' need a ytx conversion'))

        self._write(
            'double YOW = 0; '
            + self.line('To hold 1/molecularweight'))
        
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        # now to ytx
        self._write(self.line('Now compute y to x conversion'))
        for species in self.species:
            self._write('x[%d] = y[%d]/(%f*YOW); ' % (
                species.id, species.id, species.weight) )
            
        # call routine
        self._write('helmholtz(aort, tc);')
        
        # Equation 42 and 43
        self._write(self.line('Perform computation in Eq 44'))
        for species in self.species:
            self._write('result += x[%d]*(aort[%d]+log((x[%d]+%g))+logPratio);' %
                        (species.id, species.id, species.id, smallnum) )

        self._write(self.line('Scale by RT/W'))
        self._write('*abms = result * RT * YOW;')
        
        self._outdent()

        self._write('}')

        return
    

    def _ckwc(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('compute the production rate for each species'))
        self._write('void fgwc'+sym+'(double * T, double * C, int * iwrk, double * rwrk, double * wdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        # convert C to SI units
        self._write()
        self._write(self.line('convert to SI'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('C[id] *= 1.0e6;')
        self._outdent()
        self._write('}')
        
        # call productionRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('productionRate(wdot, C, *T);')

        # convert C and wdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('C[id] *= 1.0e-6;')
        self._write('wdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return

    def _ckwyp(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the molar production rate of species'))
        self._write(self.line('Given P, T, and mass fractions'))
        self._write('void fgwyp'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * wdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % self.nSpecies + self.line('temporary storage'))
        self._write('double YOW = 0; ')
        self._write('double PWORT; ')
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        self._write(self.line('PW/RT (see Eq. 7)'))
        self._write('PWORT = (*P)/(YOW * %g * (*T)); ' % (R*kelvin*mole/erg) )
        
        self._write(self.line('multiply by 1e6 so c goes to SI'))
        self._write('PWORT *= 1e6; ')

        # now compute conversion
        self._write(self.line('Now compute conversion (and go to SI)'))
        for species in self.species:
            self._write('c[%d] = PWORT * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        # call productionRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('productionRate(wdot, c, *T);')

        # convert wdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('wdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckwxp(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the molar production rate of species'))
        self._write(self.line('Given P, T, and mole fractions'))
        self._write('void fgwxp'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * wdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % self.nSpecies + self.line('temporary storage'))
        
        self._write('double PORT = 1e6 * (*P)/(%g * (*T)); ' % (R*kelvin*mole/erg) +
                    self.line('1e6 * P/RT so c goes to SI units'))
        
        # now compute conversion
        self._write()
        self._write(self.line('Compute conversion, see Eq 10'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('c[id] = x[id]*PORT;')
        self._outdent()
        self._write('}')
        
        # call productionRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('productionRate(wdot, c, *T);')

        # convert wdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('wdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckwyr(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the molar production rate of species'))
        self._write(self.line('Given rho, T, and mass fractions'))
        self._write('void fgwyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * wdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % self.nSpecies + self.line('temporary storage'))

        # now compute conversion
        self._write(self.line('See Eq 8 with an extra 1e6 so c goes to SI'))
        for species in self.species:
            self._write('c[%d] = 1e6 * (*rho) * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )
            
        # call productionRate
        self._write()
        self._write(self.line('call productionRate'))
        self._write('productionRate(wdot, c, *T);')

        # convert wdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('wdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckwxr(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Returns the molar production rate of species'))
        self._write(self.line('Given rho, T, and mole fractions'))
        self._write('void fgwxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * wdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % self.nSpecies + self.line('temporary storage'))
        
        self._write('double XW = 0; '+self.line('See Eq 4, 11 in CK Manual'))
        self._write('double ROW; ')
        
        # compute mean molecular weight first (eq 3)
        self._write(self.line('Compute mean molecular wt first'))
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        # now compute conversion
        self._write(self.line('Extra 1e6 factor to take c to SI'))
        self._write('ROW = 1e6*(*rho) / XW;')
        self._write()
        self._write(self.line('Compute conversion, see Eq 11'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('c[id] = x[id]*ROW;')
        self._outdent()
        self._write('}')
        
        # call productionRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('productionRate(wdot, c, *T);')

        # convert wdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('wdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _cknu(self, mechanism):

        nSpecies  = len(mechanism.species())
        nReaction = len(mechanism.reaction())

        self._write()
        self._write()
        self._write(self.line('Returns the stoichiometric coefficients'))
        self._write(self.line('of the reaction mechanism. (Eq 50)'))
        self._write('void fgnu'+sym+'(int * kdim, int * iwrk, double * rwrk, int * nuki)')
        self._write('{')
        self._indent()

 
        self._write('int id; ' + self.line('loop counter'))
        self._write('int kd = (*kdim); ')
        self._write(self.line('Zero nuki'))
        self._write('for (id = 0; id < %d * %d; ++ id) {' % (nSpecies, nReaction) )
        self._indent()
        self._write(' nuki[id] = 0; ')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():

            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            for symbol, coefficient in reaction.reactants:
                self._write(
                    "nuki[ %d * kd + %d ] += -%d ;"
                    % (mechanism.species(symbol).id, reaction.id-1, coefficient))

            for symbol, coefficient in reaction.products:
                self._write(
                    "nuki[ %d * kd + %d ] += +%d ;"
                    % (mechanism.species(symbol).id, reaction.id-1, coefficient))
       
        # done
        self._outdent()
        self._write('}')

        return


    def _ckncf(self, mechanism):

        nSpecies  = len(mechanism.species())
        nElement  = len(mechanism.element())

        self._write()
        self._write()
        self._write(self.line('Returns the elemental composition '))
        self._write(self.line('of the speciesi (mdim is num of elements)'))
        self._write('void fgncf'+sym+'(int * mdim, int * iwrk, double * rwrk, int * ncf)')
        self._write('{')
        self._indent()

 
        self._write('int id; ' + self.line('loop counter'))
        self._write('int kd = (*mdim); ')
        self._write(self.line('Zero ncf'))
        self._write('for (id = 0; id < %d * %d; ++ id) {' % (nElement, self.nSpecies) )
        self._indent()
        self._write(' ncf[id] = 0; ')
        self._outdent()
        self._write('}')
        
        self._write()
        for species in mechanism.species():
           self._write(self.line('%s' % species.symbol))
           for elem, coef in species.composition:
               self._write('ncf[ %d * kd + %d ] = %d; ' % (
                   species.id, mechanism.element(elem).id, coef) +
                       self.line('%s' % elem) )
                           
           self._write()
                            
        # done
        self._outdent()

        self._write('}')

        return


    def _ckabe(self, mechanism):

        nElement  = len(mechanism.element())

        self._write()
        self._write()
        self._write(self.line('Returns the arrehenius coefficients '))
        self._write(self.line('for all reactions'))
        self._write('void fgabe'+sym+'(int * iwrk, double * rwrk, double * a, double * b, double * e)')
        self._write('{')
        self._indent()

 
        for reaction in mechanism.reaction():

            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            # store the progress rate
            self._write("a[%d] = %g;" % (reaction.id-1 , reaction.arrhenius[0]))
            self._write("b[%d] = %g;" % (reaction.id-1 , reaction.arrhenius[1]))
            self._write("e[%d] = %g;" % (reaction.id-1 , reaction.arrhenius[2]))

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return
                            
        # done
        self._outdent()

        self._write('}')

        return

    
    def _ckmmwy(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('given y[species]: mass fractions'))
        self._write(self.line('returns mean molecular weight (gm/mole)'))
        self._write('void fgmmwy'+sym+'(double *y, int * iwrk, double * rwrk, double * wtm)')
        self._write('{')
        self._indent()

        self._write('double YOW = 0;'+self.line(' see Eq 3 in CK Manual'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write('*wtm = 1.0 / YOW;')
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckmmwx(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('given x[species]: mole fractions'))
        self._write(self.line('returns mean molecular weight (gm/mole)'))
        self._write('void fgmmwx'+sym+'(double *x, int * iwrk, double * rwrk, double * wtm)')
        self._write('{')
        self._indent()

        self._write('double XW = 0;'+self.line(' see Eq 4 in CK Manual'))
        
        # molecular weights of all species
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write('*wtm = XW;')
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckmmwc(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('given c[species]: molar concentration'))
        self._write(self.line('returns mean molecular weight (gm/mole)'))
        self._write('void fgmmwc'+sym+'(double *c, int * iwrk, double * rwrk, double * wtm)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write(self.line('See Eq 5 in CK Manual'))
        self._write('double W = 0;')
        self._write('double sumC = 0;')
        
        # molecular weights of all species
        for species in self.species:
            self._write('W += c[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        self._write()
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('sumC += c[id];')
        self._outdent()
        self._write('}')

        self._write(self.line(' CK provides no guard against divison by zero'))
        self._write('*wtm = W/sumC;')
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckytx(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert y[species] (mass fracs) to x[species] (mole fracs)'))
        self._write('void fgytx'+sym+'(double * y, int * iwrk, double * rwrk, double * x)')
        self._write('{')
        self._indent()

        self._write('double YOW = 0; '+self.line('See Eq 4, 6 in CK Manual'))
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        # now compute conversion
        self._write(self.line('Now compute conversion'))
        for species in self.species:
            self._write('x[%d] = y[%d]/(%f*YOW); ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckytcp(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert y[species] (mass fracs) to c[species] (molar conc)'))
        self._write('void fgytcp'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * c)')
        self._write('{')
        self._indent()

        self._write('double YOW = 0; ')
        self._write('double PWORT; ')
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        self._write(self.line('PW/RT (see Eq. 7)'))
        self._write('PWORT = (*P)/(YOW * %g * (*T)); ' % (R*kelvin*mole/erg) )

        # now compute conversion
        self._write(self.line('Now compute conversion'))
        for species in self.species:
            self._write('c[%d] = PWORT * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckytcr(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert y[species] (mass fracs) to c[species] (molar conc)'))
        self._write('void fgytcr'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * c)')
        self._write('{')
        self._indent()

        # now compute conversion
        self._write(self.line('See Eq 8 (Temperature not used)'))
        for species in self.species:
            self._write('c[%d] = (*rho) * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckxty(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert x[species] (mole fracs) to y[species] (mass fracs)'))
        self._write('void fgxty'+sym+'(double * x, int * iwrk, double * rwrk, double * y)')
        self._write('{')
        self._indent()

        self._write('double XW = 0; '+self.line('See Eq 4, 9 in CK Manual'))
        
        # compute mean molecular weight first (eq 3)
        self._write(self.line('Compute mean molecular wt first'))
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        # now compute conversion
        self._write(self.line('Now compute conversion'))
        for species in self.species:
            self._write('y[%d] = x[%d]*%f/XW; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckxtcp(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert x[species] (mole fracs) to c[species] (molar conc)'))
        self._write('void fgxtcp'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * c)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double PORT = (*P)/(%g * (*T)); ' % (R*kelvin*mole/erg) +
                    self.line('P/RT'))
        # now compute conversion
        self._write()
        self._write(self.line('Compute conversion, see Eq 10'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('c[id] = x[id]*PORT;')
        self._outdent()
        self._write('}')

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckxtcr(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert x[species] (mole fracs) to c[species] (molar conc)'))
        self._write('void fgxtcr'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * c)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double XW = 0; '+self.line('See Eq 4, 11 in CK Manual'))
        self._write('double ROW; ')
        
        # compute mean molecular weight first (eq 3)
        self._write(self.line('Compute mean molecular wt first'))
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        # now compute conversion
        self._write('ROW = (*rho) / XW;')
        self._write()
        self._write(self.line('Compute conversion, see Eq 11'))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('c[id] = x[id]*ROW;')
        self._outdent()
        self._write('}')

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckctx(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert c[species] (molar conc) to x[species] (mole fracs)'))
        self._write('void fgctx'+sym+'(double * c, int * iwrk, double * rwrk, double * x)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))
        self._write('double sumC = 0; ')

        self._write()
        self._write(self.line('compute sum of c '))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('sumC += c[id];')
        self._outdent()
        self._write('}')

        # now compute conversion
        self._write()
        self._write(self.line(' See Eq 13 '))
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('x[id] = c[id]/sumC;')
        self._outdent()
        self._write('}')

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckcty(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert c[species] (molar conc) to y[species] (mass fracs)'))
        self._write('void fgcty'+sym+'(double * c, int * iwrk, double * rwrk, double * y)')
        self._write('{')
        self._indent()

        self._write('double CW = 0; '+self.line('See Eq 12 in CK Manual'))
        
        # compute denominator in eq 12
        self._write(self.line('compute denominator in eq 12 first'))
        for species in self.species:
            self._write('CW += c[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        # now compute conversion
        self._write(self.line('Now compute conversion'))
        for species in self.species:
            self._write('y[%d] = c[%d]*%f/CW; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
    def _ckcpor(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get Cp/R as a function of T '))
        self._write(self.line('for all species (Eq 19)'))
        self._write('void fgcpor'+sym+'(double *T, int * iwrk, double * rwrk, double * cpor)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('cp_R(cpor, tc);')
        
        self._outdent()

        self._write('}')

        return
    
    def _ckhort(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get H/RT as a function of T '))
        self._write(self.line('for all species (Eq 20)'))
        self._write('void fghort'+sym+'(double *T, int * iwrk, double * rwrk, double * hort)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('speciesEnthalpy(hort, tc);')
        
        self._outdent()

        self._write('}')

        return
 
    def _cksor(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('get S/R as a function of T '))
        self._write(self.line('for all species (Eq 21)'))
        self._write('void fgsor'+sym+'(double *T, int * iwrk, double * rwrk, double * sor)')
        self._write('{')
        self._indent()

        # get temperature cache
        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        
        # call routine
        self._write('speciesEntropy(sor, tc);')
        
        self._outdent()

        self._write('}')

        return


    def _ckqc(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        self._write()
        self._write()
        self._write(self.line('Returns the rate of progress for each reaction'))
        self._write('void fgqc'+sym+'(double * T, double * C, int * iwrk, double * rwrk, double * qdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        # convert C to SI units
        self._write()
        self._write(self.line('convert to SI'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('C[id] *= 1.0e6;')
        self._outdent()
        self._write('}')
        
        # call productionRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('progressRate(qdot, C, *T);')

        # convert C to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('C[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')

        # convert qdot to chemkin units
        self._write()
        self._write('for (id = 0; id < %d; ++id) {' % nReactions)
        self._indent()
        self._write('qdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return

    
    def _ckqyp(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())
        
        self._write()
        self._write()
        self._write(self.line('Returns the progress rates of each reactions'))
        self._write(self.line('Given P, T, and mass fractions'))
        self._write('void fgqyp'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * qdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % nSpecies + self.line('temporary storage'))
        self._write('double YOW = 0; ')
        self._write('double PWORT; ')
        
        # compute inverse of mean molecular weight first (eq 3)
        self._write(self.line('Compute inverse of mean molecular wt first'))
        for species in self.species:
            self._write('YOW += y[%d]/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
 
        self._write(self.line('PW/RT (see Eq. 7)'))
        self._write('PWORT = (*P)/(YOW * %g * (*T)); ' % (R*kelvin*mole/erg) )
        
        self._write(self.line('multiply by 1e6 so c goes to SI'))
        self._write('PWORT *= 1e6; ')

        # now compute conversion
        self._write(self.line('Now compute conversion (and go to SI)'))
        for species in self.species:
            self._write('c[%d] = PWORT * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        # call progressRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('progressRate(qdot, c, *T);')

        # convert qdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % nReactions )
        self._indent()
        self._write('qdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckqxp(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())
        
        self._write()
        self._write()
        self._write(self.line('Returns the progress rates of each reactions'))
        self._write(self.line('Given P, T, and mole fractions'))
        self._write('void fgqxp'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * qdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % nSpecies + self.line('temporary storage'))
        
        self._write('double PORT = 1e6 * (*P)/(%g * (*T)); ' % (R*kelvin*mole/erg) +
                    self.line('1e6 * P/RT so c goes to SI units'))
        
        # now compute conversion
        self._write()
        self._write(self.line('Compute conversion, see Eq 10'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('c[id] = x[id]*PORT;')
        self._outdent()
        self._write('}')
        
        # call progressRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('progressRate(qdot, c, *T);')

        # convert qdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % nReactions )
        self._indent()
        self._write('qdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckqyr(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())
        
        self._write()
        self._write()
        self._write(self.line('Returns the progress rates of each reactions'))
        self._write(self.line('Given rho, T, and mass fractions'))
        self._write('void fgqyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * qdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % nSpecies + self.line('temporary storage'))

        # now compute conversion
        self._write(self.line('See Eq 8 with an extra 1e6 so c goes to SI'))
        for species in self.species:
            self._write('c[%d] = 1e6 * (*rho) * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )
            
        # call progressRate
        self._write()
        self._write(self.line('call progressRate'))
        self._write('progressRate(qdot, c, *T);')

        # convert qdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % nReactions )
        self._indent()
        self._write('qdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return


    def _ckqxr(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())
        
        self._write()
        self._write()
        self._write(self.line('Returns the progress rates of each reactions'))
        self._write(self.line('Given rho, T, and mole fractions'))
        self._write('void fgqxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * qdot)')
        self._write('{')
        self._indent()

        self._write('int id; ' + self.line('loop counter'))

        self._write('double c[%d]; ' % nSpecies + self.line('temporary storage'))
        
        self._write('double XW = 0; '+self.line('See Eq 4, 11 in CK Manual'))
        self._write('double ROW; ')
        
        # compute mean molecular weight first (eq 3)
        self._write(self.line('Compute mean molecular wt first'))
        for species in self.species:
            self._write('XW += x[%d]*%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))

        # now compute conversion
        self._write(self.line('Extra 1e6 factor to take c to SI'))
        self._write('ROW = 1e6*(*rho) / XW;')
        self._write()
        self._write(self.line('Compute conversion, see Eq 11'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('c[id] = x[id]*ROW;')
        self._outdent()
        self._write('}')
        
        # call progressRate
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('progressRate(qdot, c, *T);')

        # convert qdot to chemkin units
        self._write()
        self._write(self.line('convert to chemkin units'))
        self._write('for (id = 0; id < %d; ++id) {' % nReactions )
        self._indent()
        self._write('qdot[id] *= 1.0e-6;')
        self._outdent()
        self._write('}')
        
        self._outdent()

        self._write('}')

        return

    
    def __ckeqcontent(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        self._write(
            'double tT = *T; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(tT), tT, tT*tT, tT*tT*tT, tT*tT*tT*tT }; '
            + self.line('temperature cache'))
        self._write(
            'double gort[%d]; ' % nSpecies + self.line(' temporary storage'))

        # compute the gibbs free energy
        self._write()
        self._write(self.line('compute the Gibbs free energy'))
        self._write('gibbs(gort, tc);')

        # compute the equilibrium constants
        self._write()
        self._write(self.line('compute the equilibrium constants'))
        self._write('equilibriumConstants(eqcon, gort, tT);')

        for reaction in mechanism.reaction():

            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            somepow = 0
            for symbol, coefficient in reaction.reactants:
                somepow = somepow - coefficient

            for symbol, coefficient in reaction.products:
                somepow = somepow + coefficient

            if somepow == 0:
                self._write(self.line(
                    'eqcon[%d] *= %g; ' % (reaction.id-1, (1e-6)**somepow) ) )
                
            else:
                self._write( 'eqcon[%d] *= %g; ' % (reaction.id-1, (1e-6)**somepow) ) 
                    



    def _ckeqc(self, mechanism):

        self._write()
        self._write()
        self._write(self.line('Returns the equil constants for each reaction'))
        self._write('void fgeqc'+sym+'(double * T, double * C, int * iwrk, double * rwrk, double * eqcon)')
        self._write('{')
        self._indent()

        self.__ckeqcontent(mechanism)
                
        self._outdent()

        self._write('}')

        return

    
    def _ckeqyp(self, mechanism):

        import pyre.handbook
        periodic = pyre.handbook.periodicTable()

        self._write()
        self._write()
        self._write(self.line('Returns the equil constants for each reaction'))
        self._write(self.line('Given P, T, and mass fractions'))
        self._write('void fgeqyp'+sym+'(double * P, double * T, double * y, int * iwrk, double * rwrk, double * eqcon)')
        self._write('{')
        self._indent()

        self.__ckeqcontent(mechanism)
        
        self._outdent()

        self._write('}')

        return


    def _ckeqxp(self, mechanism):

        import pyre.handbook
        periodic = pyre.handbook.periodicTable()

        self._write()
        self._write()
        self._write(self.line('Returns the equil constants for each reaction'))
        self._write(self.line('Given P, T, and mole fractions'))
        self._write('void fgeqxp'+sym+'(double * P, double * T, double * x, int * iwrk, double * rwrk, double * eqcon)')
        self._write('{')
        self._indent()

        self.__ckeqcontent(mechanism)
        
        self._outdent()

        self._write('}')

        return


    def _ckeqyr(self, mechanism):

        import pyre.handbook
        periodic = pyre.handbook.periodicTable()

        self._write()
        self._write()
        self._write(self.line('Returns the equil constants for each reaction'))
        self._write(self.line('Given rho, T, and mass fractions'))
        self._write('void fgeqyr'+sym+'(double * rho, double * T, double * y, int * iwrk, double * rwrk, double * eqcon)')
        self._write('{')
        self._indent()

        self.__ckeqcontent(mechanism)
        
        self._outdent()

        self._write('}')

        return


    def _ckeqxr(self, mechanism):

        import pyre.handbook
        periodic = pyre.handbook.periodicTable()

        self._write()
        self._write()
        self._write(self.line('Returns the equil constants for each reaction'))
        self._write(self.line('Given rho, T, and mole fractions'))
        self._write('void fgeqxr'+sym+'(double * rho, double * T, double * x, int * iwrk, double * rwrk, double * eqcon)')
        self._write('{')
        self._indent()

        self.__ckeqcontent(mechanism)
        
        self._outdent()

        self._write('}')

        return


# Fuego Extensions. All functions in this section has the fe prefix
# All fuctions in this section uses the standard fuego chemkin functions
    def _ck_eytt(self, mechanism):

        nSpecies = len(mechanism.species())
        lowT,highT,dummy = self._analyzeThermodynamics(mechanism)
        
        self._write()
        self._write()
        self._write(self.line(
            'get temperature given internal energy in mass units and mass fracs'))
        self._write('int feeytt'+sym+'(double * e, double * y, int * iwrk, double * rwrk, double * t)')
        self._write('{')
        self._indent()

        self._write('const int maxiter = 50;')
        self._write('const double tol  = 0.001;')
        self._write('double ein  = *e;')
        self._write('double tmin = %g; // max lower bound for thermo def' % lowT)
        self._write('double tmax = %g; // min upper bound for thermo def' % highT)
        self._write('double e1,emin,emax,cv,t1,dt;')
        self._write('int i; // loop counter')
        self._write('fgubms'+sym+'(&tmin, y, iwrk, rwrk, &emin);')
        self._write('fgubms'+sym+'(&tmax, y, iwrk, rwrk, &emax);')
        self._write('if (ein < emin) {')
        self._indent()
        self._write(self.line('Linear Extrapolation below tmin'))
        self._write('fgcvbs'+sym+'(&tmin, y, iwrk, rwrk, &cv);')
        self._write('*t = tmin - (emin-ein)/cv;')
        self._write('return 1;')
        self._outdent()
        self._write('}')
        
        self._write('if (ein > emax) {')
        self._indent()
        self._write(self.line('Linear Extrapolation above tmax'))
        self._write('fgcvbs'+sym+'(&tmax, y, iwrk, rwrk, &cv);')
        self._write('*t = tmax - (emax-ein)/cv;')
        self._write('return 1;')
        self._outdent()
        self._write('}')

        self._write('t1 = tmin + (tmax-tmin)/(emax-emin)*(ein-emin);')
        self._write('for (i = 0; i < maxiter; ++i) {')
        self._indent()
        self._write('fgubms'+sym+'(&t1,y,iwrk,rwrk,&e1);')
        self._write('fgcvbs'+sym+'(&t1,y,iwrk,rwrk,&cv);')
        self._write('dt = (ein - e1) / cv;')
        self._write('if (dt > 100) { dt = 100; }')
        self._write('else if (dt < -100) { dt = -100; }')
        self._write('else if (fabs(dt) < tol) break;')
        self._write('t1 += dt;')
        self._outdent()
        self._write('}')
        
        self._write('*t = t1;')
        self._write('return 0;')
        
        self._outdent()

        self._write('}')

        return

    def _ck_eytt2(self, mechanism):

        nSpecies = len(mechanism.species())
        lowT,highT,dummy = self._analyzeThermodynamics(mechanism)
        
        self._write()
        self._write()
        self._write(self.line(
            'get temperature given internal energy in mass units and mass fracs'))
        self._write(self.line( '(*t) must contain initial guess on input!'))
        self._write('int feeytt2'+sym+'(double * e, double * y, int * iwrk, double * rwrk, double * t)')
        self._write('{')
        self._indent()

        self._write('const int maxiter = 50;')
        self._write('const double tol  = 0.001;')
        self._write('double ein  = *e;')
        self._write('double e1,cv,t1,dt;')
        self._write('int i; // loop counter')

        self._write('t1 = (*t);')
        self._write('for (i = 0; i < maxiter; ++i) {')
        self._indent()
        self._write('fgubms'+sym+'(&t1,y,iwrk,rwrk,&e1);')
        self._write('fgcvbs'+sym+'(&t1,y,iwrk,rwrk,&cv);')
        self._write('dt = (ein - e1) / cv;')
        self._write('if (dt > 100) { dt = 100; }')
        self._write('else if (dt < -100) { dt = -100; }')
        self._write('else if (fabs(dt) < tol) break;')
        self._write('t1 += dt;')
        self._outdent()
        self._write('}')
        
        self._write('*t = t1;')
        self._write('return 0;')
        
        self._outdent()

        self._write('}')

        return
 
    def _ck_phity(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert phi[species] (specific mole nums) to y[species] (mass fracs)'))
        self._write('void fephity'+sym+'(double * phi, int * iwrk, double * rwrk, double * y)')
        self._write('{')
        self._indent()

        self._write('double XW  = 0; ')
        self._write('int id; ' + self.line('loop counter'))
        
        # compute mean molecular weight first (eq 3)
        self._write(self.line('Compute mean molecular wt first'))
        for species in self.species:
            self._write('y[%d] = phi[%d]*%f;   XW += y[%d]; ' % (
                species.id, species.id, species.weight, species.id) +
                        self.line('%s' % species.symbol))
 
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('y[id] = y[id]/XW;')
        self._outdent()
        self._write('}')
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
 
    def _ck_ytphi(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'convert y[species] (mass fracs) to phi[species] (specific mole num)'))
        self._write('void feytphi'+sym+'(double * y, int * iwrk, double * rwrk, double * phi)')
        self._write('{')
        self._indent()

        for species in self.species:
            self._write('phi[%d] = y[%d]/%15.8e; ' % (
                species.id, species.id, species.weight/1000.0) +
                        self.line('%s (wt in kg)' % species.symbol))
 
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return


    def _ck_ctyr(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'reverse of ytcr, useful for rate computations'))
        self._write('void fectyr'+sym+'(double * c, double * rho, int * iwrk, double * rwrk, double * y)')
        self._write('{')
        self._indent()

        # now compute conversion
        for species in self.species:
            self._write('y[%d] = c[%d] * %f / (*rho); ' % (
                species.id, species.id, species.weight) )
        
        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 
 
 
    def _ck_cvrhs(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'ddebdf compatible right hand side of CV burner'))
        self._write(self.line(
            'rwrk[0] and rwrk[1] should contain rho and ene respectively'))
        self._write(self.line(
            'working variable phi contains specific mole numbers'))
        self._write('void fecvrhs'+sym+'(double * time, double * phi, double * phidot, double * rwrk, int * iwrk)')

	self._write('{')
	self._indent()
	# main body
        self._write('double rho,ene; ' + self.line('CV Parameters'))
        self._write('double y[%s], wdot[%s]; ' % (self.nSpecies, self.nSpecies) +
                    self.line('temporary storage'))
        self._write('int i; ' + self.line('Loop counter'))
        self._write('double temperature,pressure; ' + self.line('temporary var'))
        self._write('rho = rwrk[0];')
        self._write('ene = rwrk[1];')
        self._write('fephity'+sym+'(phi, iwrk, rwrk, y);')
        self._write('feeytt'+sym+'(&ene, y, iwrk, rwrk, &temperature);')
        self._write('fgpy'+sym+'(&rho, &temperature,  y, iwrk, rwrk, &pressure);')
        self._write('fgwyp'+sym+'(&pressure, &temperature,  y, iwrk, rwrk, wdot);')
        self._write('for (i=0; i<%s; ++i) phidot[i] = wdot[i] / (rho/1000.0); ' % self.nSpecies)
        self._write()
        self._write('return;')

	self._outdent()
	self._write('}')
	return


    def _ck_cvdim(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'returns the dimensionality of the cv burner (number of species)'))
        self._write('int fecvdim'+sym+'()')

	self._write('{')
	self._indent()
	# main body
        self._write('return %d;' % self.nSpecies)

	self._outdent()
	self._write('}')
	return

 
    def _ck_zndrhs(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'ddebdf compatible right hand side of ZND solver'))
        self._write(self.line( 'rwrk[0] : scaling factor for pressure'))
        self._write(self.line( 'rwrk[1] : preshock density (g/cc) '))
        self._write(self.line( 'rwrk[2] : detonation velocity (cm/s) '))
        self._write(self.line( 'solution vector: [P; rho; y0 ... ylast] '))
        self._write('void fezndrhs'+sym+'(double * time, double * z, double * zdot, double * rwrk, int * iwrk)')

	self._write('{')
	self._indent()
	# main body
        self._write('double psc,rho1,udet; ' + self.line('ZND Parameters'))
        self._write('double wt[%s], hms[%s], wdot[%s]; ' %
                    (self.nSpecies, self.nSpecies, self.nSpecies) +
                    self.line('temporary storage'))
        self._write('int i; ' + self.line('Loop counter'))
        self._write(self.line('temporary variables'))
        self._write('double ru, T, uvel, wtm, p, rho, gam, son, xm, sum, drdy, eta, cp, cv ;')
        self._write('double *y; ' + self.line('mass frac pointer'))
        self._write()
        self._write('ru = %g;' % (R * mole * kelvin / erg))
        self._write()
        self._write('psc = rwrk[0];')
        self._write('rho1 = rwrk[1];')
        self._write('udet = rwrk[2];')
        self._write()
        self._write('p = z[0] * psc;')
        self._write('rho = z[1];')
        self._write()
        self._write('y = &z[3];')
        self._write()
        self._write('fgmmwy'+sym+'(y, 0, 0, &wtm);')
        self._write()
        self._write('T = p * wtm / rho / ru;')
        self._write()
        self._write('uvel = (rho1 * udet)/ rho;')
        self._write()
        self._write('fgcpbs'+sym+'(&T, y, 0, 0, &cp);')
        self._write('fgcvbs'+sym+'(&T, y, 0, 0, &cv);')
        self._write('gam = cp/cv;')
        self._write()
        self._write('son = sqrt(fabs(gam*ru*T/wtm));')
        self._write('xm = uvel/son;')
        self._write()
        self._write('fghms'+sym+'(&T, 0, 0, hms);')
        self._write('fgwt'+sym+'(0, 0, wt);')
        self._write('fgwyp'+sym+'(&p, &T, y, 0, 0, wdot);')
        self._write()
        self._write('sum = 0.0;')
        self._write('for (i=0; i<%s; ++i) {' % self.nSpecies)
        self._indent()
        self._write('zdot[i+3] = wdot[i] * wt[i] / rho;')
        self._write('drdy = -rho * wtm / wt[i];')
        self._write('sum += -( drdy + rho * hms[i]/ (cp*T) ) * zdot[i+3];')
        self._outdent()
        self._write('}')
        self._write()
        self._write('eta = 1.0 - xm*xm;')
        self._write('zdot[0] = -(uvel*uvel/eta/psc)*sum;')
        self._write('zdot[1] = -sum/eta;')
        self._write('zdot[2] = uvel;')
        self._write()
        self._write('return;')

	self._outdent()
	self._write('}')
	return


    def _ck_znddim(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'returns the dimensionality of the ZND solver (3+number of species)'))
        self._write('int feznddim'+sym+'()')

	self._write('{')
	self._indent()
	# main body
        self._write('return %d;' % (self.nSpecies + 3) )

	self._outdent()
	self._write('}')
	return
    
    def _ck_mechfile(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'returns the name of the source mechanism file '))
        self._write('char* femechfile'+sym+'()')

	self._write('{')
	self._indent()
	# main body
        self._write('return "%s";' % mechanism.name())

	self._outdent()
	self._write('}')
	return

    def _ck_symnum(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'returns the species number'))
        self._write('int fesymnum'+sym+'(const char* s1)')

	self._write('{')
	self._indent()
        
        for species in self.species:
            self._write('if (strcmp(s1, "%s")==0) return %d; ' % (
                species.symbol, species.id))
 
        self._write(self.line( 'species name not found' ))
        self._write('return -1;')

	self._outdent()
	self._write('}')
	return
    
    def _ck_symname(self, mechanism):
        self._write()
        self._write()
        self._write(self.line(
            'returns the species name'))
        self._write('char* fesymname'+sym+'(int sn)')

	self._write('{')
	self._indent()

        for species in self.species:
            self._write('if (sn==%d) return "%s"; ' % (
                species.id, species.symbol))
 
        self._write(self.line( 'species name not found' ))
        self._write('return "NOTFOUND";')

	self._outdent()
	self._write('}')
	return
    
# Fuego's core routines section begins here
    def _molecularWeight(self, mechanism):

        import pyre.handbook
        periodic = pyre.handbook.periodicTable()
        
        nSpecies = len(mechanism.species())
        self._write()
        self._write()
        self._write(self.line('save molecular weights into array'))
        self._write('void molecularWeight(double * wt)')
        self._write('{')
        self._indent()

        # molecular weights of all species
        for species in mechanism.species():

            weight = 0.0 #species.molecularWeight()
            for elem, coef in species.composition:
                aw = mechanism.element(elem).weight
                if not aw:
                    aw = periodic.symbol(elem.capitalize()).atomicWeight
                weight += coef * aw

            self._write('wt[%d] = %f; ' % (
                species.id, weight) + self.line('%s' % species.symbol))

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return 

    def _productionRate(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        self._write()
        self._write()
        self._write(self.line('compute the production rate for each species'))
        self._write('void productionRate(double * wdot, double * sc, double T)')
        self._write('{')
        self._indent()

        # declarations
        self._write('double qdot;')
        self._initializeRateCalculation(mechanism)

        # clear out wdot
        self._write()
        self._write(self.line('zero out wdot'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('wdot[id] = 0.0;')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():

            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            # compute the rates
            self._forwardRate(mechanism, reaction)
            self._reverseRate(mechanism, reaction)

            # store the progress rate
            self._write("qdot = q_f - q_r;")

            for symbol, coefficient in reaction.reactants:
                self._write(
                    "wdot[%d] -= %d * qdot;" % (mechanism.species(symbol).id, coefficient))

            for symbol, coefficient in reaction.products:
                self._write(
                    "wdot[%d] += %d * qdot;" % (mechanism.species(symbol).id, coefficient))

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return


    def _progressRate(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        self._write()
        self._write()
        self._write(self.line('compute the progress rate for each reaction'))
        self._write('void progressRate(double * qdot, double * sc, double T)')
        self._write('{')
        self._indent()

        # declarations
        self._initializeRateCalculation(mechanism)
        
        for reaction in mechanism.reaction():

            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            # compute the rates
            self._forwardRate(mechanism, reaction)
            self._reverseRate(mechanism, reaction)

            # store the progress rate
            self._write("qdot[%d] = q_f - q_r;" % (reaction.id - 1))

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return


    def _initializeRateCalculation(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        # declarations
        self._write()
        self._write('int id; ' + self.line('loop counter'))

        self._write('double mixture;                 '
                    + self.line('mixture concentration'))
        self._write('double g_RT[%d];                ' % nSpecies
                    + self.line('Gibbs free energy'))

        self._write('double Kc;                      ' + self.line('equilibrium constant'))
        self._write('double k_f;                     ' + self.line('forward reaction rate'))
        self._write('double k_r;                     ' + self.line('reverse reaction rate'))
        self._write('double q_f;                     ' + self.line('forward progress rate'))
        self._write('double q_r;                     ' + self.line('reverse progress rate'))
        self._write('double phi_f;                   '
                    + self.line('forward phase space factor'))
        self._write('double phi_r;                   '
                    + self.line('reverse phase space factor'))
        self._write('double alpha;                   ' + self.line('enhancement'))


        self._write('double redP;                    ' + self.line('reduced pressure'))
        self._write('double logPred;                 ' + self.line('log of above'))
        self._write('double F;                       '
                    + self.line('fallof rate enhancement'))
        self._write()
        self._write('double F_troe;                  ' + self.line('TROE intermediate'))
        self._write('double logFcent;                ' + self.line('TROE intermediate'))
        self._write('double troe;                    ' + self.line('TROE intermediate'))
        self._write('double troe_c;                  ' + self.line('TROE intermediate'))
        self._write('double troe_n;                  ' + self.line('TROE intermediate'))

        self._write()
        self._write('double X;                       ' + self.line('SRI intermediate'))
        self._write('double F_sri;                   ' + self.line('SRI intermediate'))

        self._write(
            'double tc[] = { log(T), T, T*T, T*T*T, T*T*T*T }; '
            + self.line('temperature cache'))

        # compute the reference concentration
        self._write()
        self._write(self.line('reference concentration: P_atm / (RT) in inverse mol/m^3'))
        self._write('double refC = %g / %g / T;' % (atm.value, R.value))

        # compute the mixture concentration
        self._write()
        self._write(self.line('compute the mixture concentration'))
        self._write('mixture = 0.0;')
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('mixture += sc[id];')
        self._outdent()
        self._write('}')

        # compute the Gibbs free energies
        self._write()
        self._write(self.line('compute the Gibbs free energy'))
        self._write('gibbs(g_RT, tc);')
        
        return


    def _forwardRate(self, mechanism, reaction):

        lt = reaction.lt
        if lt:
            import journal
            journal.firewall("fuego").log("Landau-Teller reactions are not supported yet")
            return self._landau(reaction)

        dim = self._phaseSpaceUnits(reaction.reactants)

        phi_f = self._phaseSpace(mechanism, reaction.reactants)
        self._write("phi_f = %s;" % phi_f)

        arrhenius = self._arrhenius(reaction, reaction.arrhenius)

        thirdBody = reaction.thirdBody
        if not thirdBody:
            uc = self._prefactorUnits(reaction.units["prefactor"], 1-dim)
            self._write("k_f = %g * %s;" % (uc.value, arrhenius))
            self._write("q_f = phi_f * k_f;")
            return
            
        alpha = self._enhancement(mechanism, reaction)
        self._write("alpha = %s;" % alpha)

        sri = reaction.sri
        low = reaction.low
        troe = reaction.troe

        if not low:
            uc = self._prefactorUnits(reaction.units["prefactor"], -dim)
            self._write("k_f = %g * alpha * %s;" % (uc.value, arrhenius))
            self._write("q_f = phi_f * k_f;")
            return

        uc = self._prefactorUnits(reaction.units["prefactor"], 1-dim)
        self._write("k_f = %g * %s;" % (uc.value, arrhenius))
        k_0 = self._arrhenius(reaction, reaction.low)
        redP = "alpha / k_f * " + k_0
        self._write("redP = 1e-12 * %s;" % redP)
        self._write("F = redP / (1 + redP);")

        if sri:
            self._write("logPred = log10(redP);")

            self._write("X = 1.0 / (1.0 + logPred*logPred);")

            SRI = "exp(X * log(%g*exp(%g/T) + exp(T/%g))" % (sri[0], -sri[1], -sri[2])
            if len(sri) > 3:
                SRI += " * %g * exp(%g*tc[0])" % (sri[3], sri[4])

            self._write("F_sri = %s;" % SRI)
            self._write("F *= Ftroe;")

        elif troe:
            self._write("logPred = log10(redP);")

            logF_cent = "logFcent = log10("
            logF_cent += "(%g*exp(T/%g))" % (1-troe[0], -troe[1])
            logF_cent += "+ (%g*exp(T/%g))" % (troe[0], -troe[2])
            if len(troe) == 4:
                logF_cent += "+ (exp(%g/T))" % (-troe[3])
            logF_cent += ');'
            self._write(logF_cent)
            
            d = .14
            self._write("troe_c = -.4 - .67 * logFcent;")
            self._write("troe_n = .75 - 1.27 * logFcent;")
            self._write("troe = (troe_c + logPred) / (troe_n - .14*(troe_c + logPred));")
            self._write("F_troe = pow(10, logFcent / (1.0 + troe*troe));")
            self._write("F *= F_troe;")

        self._write("k_f *= F;")
        self._write("q_f = phi_f * k_f;")
        return
        

    def _reverseRate(self, mechanism, reaction):
        if not reaction.reversible:
            self._write("q_r = 0.0;")
            return

        phi_r = self._phaseSpace(mechanism, reaction.products)
        self._write("phi_r = %s;" % phi_r)

        if reaction.rlt:
            import journal
            journal.firewall("fuego").log("Landau-Teller reactions are not supported yet")
            return

        if reaction.rev:
            arrhenius = self._arrhenius(reaction, reaction.rev)
            thirdBody = reaction.thirdBody
            if thirdBody:
                uc = self._prefactorUnits(reaction.units["prefactor"], -dim)
                self._write("k_r = %g * alpha * %s;" % (uc.value, arrhenius))
            else:
                uc = self._prefactorUnits(reaction.units["prefactor"], 1-dim)
                self._write("k_r = %g * %s;" % (uc.value, arrhenius))

            self._write("q_f = phi_r * k_r;")
            return
        
        K_c = self._Kc(mechanism, reaction)
        self._write("Kc = %s;" % K_c)

        self._write("k_r = k_f / Kc;")
        self._write("q_r = phi_r * k_r;")

        return


    def _arrhenius(self, reaction, parameters):
        A, beta, E = parameters
        if A == 0:
            return "0.0"
        expr = "%g" % A
        if beta == 0 and E == 0:
            return expr
        expr +="*exp("
        if beta != 0:
            expr += "%g*tc[0]" % beta
        if E != 0:
            uc = self._activationEnergyUnits(reaction.units["activation"])
            expr += "%+g/tc[1]" % (- uc * E / Rc / kelvin) # catch unit conversion errors!
        expr += ')'
        
        return expr


    def _prefactorUnits(self, code, exponent):

        if code == "mole/cm**3":
            units = mole / cm**3
        elif code == "moles":
            units = mole / cm**3
        elif code == "molecules":
            from pyre.hadbook.constants.fundamental import avogadro
            units = 1.0 / avogadro / cm**3
        else:
            import journal
            journal.firewall("fuego").log("unknown prefactor units '%s'" % code)
            return 1

        return units ** exponent / second


    def _activationEnergyUnits(self, code):
        if code == "cal/mole":
            units = cal / mole
        elif code == "kcal/mole":
            units = kcal /mole
        elif code == "joules/mole":
            units = J / mole
        elif code == "kjoules/mole":
            units = kJ / mole
        elif code == "kelvins":
            units = Rc * kelvin
        else:
            import journal
            journal.firewall("fuego").log("unknown activation energy units '%s'" % code)
            return 1

        return units


    def _equilibriumConstants(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('compute the equilibrium constants for each reaction'))
        self._write('void equilibriumConstants(double *kc, double * g_RT, double T)')
        self._write('{')
        self._indent()

        # compute the reference concentration
        self._write(self.line('reference concentration: P_atm / (RT) in inverse mol/m^3'))
        self._write('double refC = %g / %g / T;' % (atm.value, R.value))

        # compute the equilibrium constants
        for reaction in mechanism.reaction():
            self._write()
            self._write(self.line('reaction %d: %s' % (reaction.id, reaction.equation())))

            K_c = self._Kc(mechanism, reaction)
            self._write("kc[%d] = %s;" % (reaction.id - 1, K_c))

        self._write()
        self._write('return;')
        self._outdent()

        self._write('}')

        return


    def _phaseSpace(self, mechanism, reagents):

        phi = []

        for symbol, coefficient in reagents:
            conc = "sc[%d]" % mechanism.species(symbol).id
            phi += [conc] * coefficient

        return "*".join(phi)


    def _phaseSpaceUnits(self, reagents):
        dim = 0
        for symbol, coefficient in reagents:
            dim += coefficient

        return dim


    def _enhancement(self, mechanism, reaction):
        thirdBody = reaction.thirdBody
        if not thirdBody:
            import journal
            journal.firewall("fuego").log("_enhancement called for a reaction without a third body")
            return

        species, coefficient = thirdBody
        efficiencies = reaction.efficiencies

        if not efficiencies:
            if species == "<mixture>":
                return "mixture"
            return "sc[%d]" % mechanism.species(species).id

        alpha = ["mixture"]
        for symbol, efficiency in efficiencies:
            factor = efficiency - 1
            conc = "sc[%d]" % mechanism.species(symbol).id
            if factor == 1:
                alpha.append(conc)
            else:
                alpha.append("%g*%s" % (factor, conc))

        return " + ".join(alpha)


    def _cv(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute Cv/R at the given temperature'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("cv_R", self._cvNASA, speciesInfo)

        return
    
    def _cp(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute Cp/R at the given temperature'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("cp_R", self._cpNASA, speciesInfo)

        return


    def _gibbs(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute the g/(RT) at the given temperature'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("gibbs", self._gibbsNASA, speciesInfo)

        return

    def _helmholtz(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute the a/(RT) at the given temperature'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("helmholtz", self._helmholtzNASA, speciesInfo)

        return

    def _speciesEntropy(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute the S/R at the given temperature (Eq 21)'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("speciesEntropy", self._entropyNASA, speciesInfo)

        return

    def _speciesInternalEnergy(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute the e/(RT) at the given temperature'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("speciesInternalEnergy", self._internalEnergy, speciesInfo)

        return

    def _speciesEnthalpy(self, speciesInfo):

        self._write()
        self._write()
        self._write(self.line('compute the h/(RT) at the given temperature (Eq 20)'))
        self._write(self.line('tc contains precomputed powers of T, tc[0] = log(T)'))
        self._generateThermoRoutine("speciesEnthalpy", self._enthalpyNASA, speciesInfo)

        return

    

    def _generateThermoRoutine(self, name, expressionGenerator, speciesInfo):

        lowT, highT, midpoints = speciesInfo
        
        self._write('void %s(double * species, double * tc)' % name)
        self._write('{')

        self._indent()

        # declarations
        self._write()
        self._write(self.line('temperature'))
        self._write('double T = tc[1];')

        # temperature check
        # self._write()
        # self._write(self.line('check the temperature value'))
        # self._write('if (T < %g || T > %g) {' % (lowT, highT))
        # self._indent()
        # self._write(
        #     'fprintf(stderr, "temperature %%g is outside the range (%g, %g)", T);'
        #     % (lowT, highT))
        # self._write('return;')
        # self._outdent()
        # self._write('}')
                    
        for midT, speciesList in midpoints.items():

            self._write('')
            self._write(self.line('species with midpoint at T=%g kelvin' % midT))
            self._write('if (T < %g) {' % midT)
            self._indent()

            for species, lowRange, highRange in speciesList:
                self._write(self.line('species %d: %s' % (species.id, species.symbol)))
                self._write('species[%d] =' % species.id)
                self._indent()
                expressionGenerator(lowRange.parameters)
                self._outdent()

            self._outdent()
            self._write('} else {')
            self._indent()

            for species, lowRange, highRange in speciesList:
                self._write(self.line('species %d: %s' % (species.id, species.symbol)))
                self._write('species[%d] =' % species.id)
                self._indent()
                expressionGenerator(highRange.parameters)
                self._outdent()

            self._outdent()
            self._write('}')
            
        self._write('return;')
        self._outdent()

        self._write('}')

        return


    def _analyzeThermodynamics(self, mechanism):
        lowT = 0.0
        highT = 1000000.0

        midpoints = {}

        for species in mechanism.species():
            models = species.thermo
            if len(models) > 2:
                import journal
                print models
                journal.firewall("fuego").log(
                    "species '%s' has more than two thermo regions" % species.symbol)
                return
            
            m1 = models[0]
            m2 = models[1]

            if m1.lowT < m2.lowT:
                lowRange = m1
                highRange = m2
            else:
                lowRange = m2
                highRange = m1

            low = lowRange.lowT
            mid = lowRange.highT
            high = highRange.highT

            if low > lowT:
                lowT = low
            if high < highT:
                highT = high

            midpoints.setdefault(mid, []).append((species, lowRange, highRange))
            
        return lowT, highT, midpoints


    def _Kc(self, mechanism, reaction):

        dim = 0
        dG = ""

        terms = []
        for symbol, coefficient in reaction.reactants:
            if coefficient == 1:
                factor = ""
            else:
                factor = "%d * " % coefficient
                    
            terms.append("%sg_RT[%d]" % (factor, mechanism.species(symbol).id))
            dim -= coefficient
        dG += '(' + ' + '.join(terms) + ')'

        # flip the signs
        terms = []
        for symbol, coefficient in reaction.products:
            if coefficient == 1:
                factor = ""
            else:
                factor = "%d * " % coefficient
            terms.append("%sg_RT[%d]" % (factor, mechanism.species(symbol).id))
            dim += coefficient
        dG += ' - (' + ' + '.join(terms) + ')'

        K_p = 'exp(' + dG + ')'

        if dim == 0:
            conversion = ""
        elif dim > 0:
            conversion = "*".join(["refC"] * dim) + ' * '
        else:
            conversion = "1.0 / (" + "*".join(["refC"] * abs(dim)) + ') * '

        K_c = conversion + K_p

        return K_c


    def _cpNASA(self, parameters):
        self._write('%+15.8e' % parameters[0])
        self._write('%+15.8e * tc[1]' % parameters[1])
        self._write('%+15.8e * tc[2]' % parameters[2])
        self._write('%+15.8e * tc[3]' % parameters[3])
        self._write('%+15.8e * tc[4];' % parameters[4])
        return


    def _cvNASA(self, parameters):
        self._write('%+15.8e' % (parameters[0] - 1.0))
        self._write('%+15.8e * tc[1]' % parameters[1])
        self._write('%+15.8e * tc[2]' % parameters[2])
        self._write('%+15.8e * tc[3]' % parameters[3])
        self._write('%+15.8e * tc[4];' % parameters[4])
        return


    def _enthalpyNASA(self, parameters):
        self._write('%+15.8e' % parameters[0])
        self._write('%+15.8e * tc[1]' % (parameters[1]/2))
        self._write('%+15.8e * tc[2]' % (parameters[2]/3))
        self._write('%+15.8e * tc[3]' % (parameters[3]/4))
        self._write('%+15.8e * tc[4]' % (parameters[4]/5))
        self._write('%+15.8e / tc[1];' % (parameters[5]))
        return


    def _internalEnergy(self, parameters):
        self._write('%+15.8e' % (parameters[0] - 1.0))
        self._write('%+15.8e * tc[1]' % (parameters[1]/2))
        self._write('%+15.8e * tc[2]' % (parameters[2]/3))
        self._write('%+15.8e * tc[3]' % (parameters[3]/4))
        self._write('%+15.8e * tc[4]' % (parameters[4]/5))
        self._write('%+15.8e / tc[1];' % (parameters[5]))
        return

    
    def _gibbsNASA(self, parameters):
        self._write('%+15.8e / tc[1]' % parameters[5])
        self._write('%+15.8e' % (parameters[0] - parameters[6]))
        self._write('%+15.8e * tc[0]' % (-parameters[0]))
        self._write('%+15.8e * tc[1]' % (-parameters[1]/2))
        self._write('%+15.8e * tc[2]' % (-parameters[2]/6))
        self._write('%+15.8e * tc[3]' % (-parameters[3]/12))
        self._write('%+15.8e * tc[4];' % (-parameters[4]/20))
        return
    
    def _helmholtzNASA(self, parameters):
        self._write('%+15.8e / tc[1]' % parameters[5])
        self._write('%+15.8e' % (parameters[0] - parameters[6] - 1.0))
        self._write('%+15.8e * tc[0]' % (-parameters[0]))
        self._write('%+15.8e * tc[1]' % (-parameters[1]/2))
        self._write('%+15.8e * tc[2]' % (-parameters[2]/6))
        self._write('%+15.8e * tc[3]' % (-parameters[3]/12))
        self._write('%+15.8e * tc[4];' % (-parameters[4]/20))
        return

    def _entropyNASA(self, parameters):
        self._write('%+15.8e * tc[0]' % parameters[0])
        self._write('%+15.8e * tc[1]' % (parameters[1]))
        self._write('%+15.8e * tc[2]' % (parameters[2]/2))
        self._write('%+15.8e * tc[3]' % (parameters[3]/3))
        self._write('%+15.8e * tc[4]' % (parameters[4]/4))
        self._write('%+15.8e ;' % (parameters[6]))
        return


    # Fuego Symbolic Jacobian and helpers
    def _ck_qij(self, mechanism):
        self._write()
        self._write()
        self._write(self.line('Computes partial derivatives of reaction progress'))
        self._write(self.line('Remember to zero qij before calling !!'))
        self._write(self.line('qij in row major: (nreactions by nspecies)'))
        self._write('void feqij'+sym+'(int *kdim, double *qij, double *sc, double *pT)')

	self._write('{')
	self._indent()
        
        # declarations
        self._write('int kd = (*kdim);               ' + self.line('for indexing output matrix qij'))
        self._initializeJacobianCalculation(mechanism)
        
        # compute the mixture concentration
        self._write()
        self._write(self.line('compute the mixture concentration'))
        self._write('mixture = 0.0;')
        self._write('for (id = 0; id < %d; ++id) {' % self.nSpecies)
        self._indent()
        self._write('mixture += sc[id];')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():
            self._write()
            self._boxedReaction(reaction)

            dqf = self._dForwardRate(mechanism, reaction)
            dqr = self._dReverseRate(mechanism, reaction)
            for i in range(len(dqf)):
                term1 = dqf[i]
                term2 = dqr[i]
                if len(term1) > 0:
                    if len(term2) == 0:
                        self._write("qij[%d * kd + %d] = %s;" % (reaction.id-1, i,term1) )
                    else:
                        self._write("qij[%d * kd + %d] = %s - %s;" % (reaction.id-1, i,term1, term2) )
                else:
                    if len(term2) == 0:
                        pass
                    else:
                        self._write("qij[%d * kd + %d] = -%s;" % (reaction.id-1, i, term2) )
                        
        self._write('return;')

	self._outdent()
	self._write('}')
	return
    
    def _ck_jac(self, mechanism):
        nSpecies = self.nSpecies
        
        self._write()
        self._write()
        self._write(self.line('Computes symbolic jacobian with molar concentrations'))
        self._write(self.line('Jac in column major'))
        self._write('void fejac'+sym+'(double *pT, double *sc, double *jac)')

	self._write('{')
	self._indent()
        
        # declarations
	self._write('double qij;                 /* temporary */ ')
        self._initializeJacobianCalculation(mechanism)
        
        # Convert input to SI units
        self._write()
        self._write(self.line('Convert input conc. from CGS to SI for internal use, and sum'))
        self._write('mixture = 0.0;')
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('sc[id] *= 1e6;')
        self._write('mixture += sc[id];')
        self._outdent()
        self._write('}')

        # clear out jacobian
        self._write()
        self._write(self.line('zero out jac'))
        self._write('for (id = 0; id < %d; ++id) {' % (nSpecies*nSpecies) )
        self._indent()
        self._write('jac[id] = 0.0;')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():
            self._write()
            self._boxedReaction(reaction)

            dqf = self._dForwardRate(mechanism, reaction)
            dqr = self._dReverseRate(mechanism, reaction)
            i = reaction.id - 1
            for j in range(len(dqf)):
                term1 = dqf[j]
                term2 = dqr[j]
                qiszero = 0
                if len(term1) > 0:
                    if len(term2) == 0:
                        self._write("qij = %s;" % (term1) )
                    else:
                        self._write("qij = %s - %s;" % (term1, term2) )
                else:
                    if len(term2) == 0:
                        #self._write(self.line(" qij = 0;"))
                        qiszero = 1
                    else:
                        self._write("qij = -%s;" % (term2) )

                if not qiszero:
                    for symbol, coefficient in reaction.reactants:
                        self._write(
                            "jac[%d * %d + %d] -= %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))
                        
                    for symbol, coefficient in reaction.products:
                        self._write(
                            "jac[%d * %d + %d] += %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))
                        
        # Jacobian has units of 1/s, no converstion needed
        self._write()
        self._write(self.line('Restoring input vector sc back to CGS'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('sc[id] *= 1e-6;')
        self._outdent()
        self._write('}')
        self._write('return;')

	self._outdent()
	self._write('}')
	return
    
    def _ck_jay(self, mechanism):
        nSpecies = self.nSpecies
        
        self._write()
        self._write()
        self._write(self.line('Computes symbolic jacobian for mass-fractions'))
        self._write(self.line('Jac in column major'))
        self._write('void fejay'+sym+'(double *rho, double *pT, double *y, double *jac)')

	self._write('{')
	self._indent()
        
        # declarations
	self._write('double qij;                     ' + self.line('temporary'))
	self._write('double sc[%d];                  ' % nSpecies + self.line('to hold concentrations in SI'))
        self._initializeJacobianCalculation(mechanism)

        self._write()
        self._write(self.line('Convert y to concentrations in SI units'))
        for species in self.species:
            self._write('sc[%d] = 1e6 * (*rho) * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write(self.line('Compute total concentrations'))
        self._write('mixture = 0.0;')
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('mixture += sc[id];')
        self._outdent()
        self._write('}')

        # clear out jacobian
        self._write()
        self._write(self.line('zero out jac'))
        self._write('for (id = 0; id < %d; ++id) {' % (nSpecies*nSpecies) )
        self._indent()
        self._write('jac[id] = 0.0;')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():
            self._write()
            self._boxedReaction(reaction)

            dqf = self._dForwardRate(mechanism, reaction)
            dqr = self._dReverseRate(mechanism, reaction)
            i = reaction.id - 1
            for j in range(len(dqf)):
                term1 = dqf[j]
                term2 = dqr[j]
                qiszero = 0
                if len(term1) > 0:
                    if len(term2) == 0:
                        self._write("qij = %s;" % (term1) )
                    else:
                        self._write("qij = %s - %s;" % (term1, term2) )
                else:
                    if len(term2) == 0:
                        #self._write(self.line(" qij = 0;"))
                        qiszero = 1
                    else:
                        self._write("qij = -%s;" % (term2) )

                if not qiszero:
                    for symbol, coefficient in reaction.reactants:
                        self._write(
                            "jac[%d * %d + %d] -= %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))
                        
                    for symbol, coefficient in reaction.products:
                        self._write(
                            "jac[%d * %d + %d] += %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))
                        
        # Convert concentration jacobian to mass-fractions jacobian
        self._write()
        self._write(self.line('Convert Concentration J to mass-fractions J'))
        knt = 0;
        for speciesj in self.species:
            wtj =  speciesj.weight
            for speciesi in self.species:
                wti = speciesi.weight
                self._write('jac[%d] *= %r;' % (knt, wti/wtj))
                knt = knt + 1

        self._write()
        self._write(self.line('Restoring input vector sc back to CGS'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('sc[id] *= 1e-6;')
        self._outdent()
        self._write('}')
        self._write('return;')

	self._outdent()
	self._write('}')
	return
    
    def _ck_cvjac(self, mechanism):
        nSpecies = self.nSpecies
        
        self._write()
        self._write()
        self._write(self.line('Computes adiabatic constant-volume jacobian for mass-fractions'))
        self._write(self.line('   Jac in column major, this is a rank-1 correction to fejay'))
        self._write(self.line('   see Eq 2.43 of Patrick Hung''s Ph.D. thesis'))
        self._write('void fecvjac'+sym+'(double *rho, double *pT, double *y, double *beta, double *jac)')

	self._write('{')
	self._indent()
        
        # declarations
	self._write('double qij;                     '  + self.line('temporary'))
	self._write('double sc[%d];                  ' % nSpecies + self.line('to hold concentrations in SI'))
	self._write('double uj[%d], RTocv, cv;       ' % (nSpecies) + self.line('temporaries for rank-1 mod'))
        self._initializeJacobianCalculation(mechanism)

        self._write()
        self._write(self.line('Convert y to concentrations in SI units'))
        for species in self.species:
            self._write('sc[%d] = 1e6 * (*rho) * y[%d]/%f; ' % (
                species.id, species.id, species.weight) )

        self._write()
        self._write(self.line('Compute total concentrations'))
        self._write('mixture = 0.0;')
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('mixture += sc[id];')
        self._outdent()
        self._write('}')

        # clear out jacobian
        self._write()
        self._write(self.line('zero out jac'))
        self._write('for (id = 0; id < %d; ++id) {' % (nSpecies*nSpecies) )
        self._indent()
        self._write('jac[id] = 0.0;')
        self._outdent()
        self._write('}')
        
        for reaction in mechanism.reaction():
            self._write()
            self._boxedReaction(reaction)

            dqf = self._dForwardRate(mechanism, reaction)
            dqr = self._dReverseRate(mechanism, reaction)
            i = reaction.id - 1
            for j in range(len(dqf)):
                term1 = dqf[j]
                term2 = dqr[j]
                qiszero = 0
                if len(term1) > 0:
                    if len(term2) == 0:
                        self._write("qij = %s;" % (term1) )
                    else:
                        self._write("qij = %s - %s;" % (term1, term2) )
                else:
                    if len(term2) == 0:
                        #self._write(self.line(" qij = 0;"))
                        qiszero = 1
                    else:
                        self._write("qij = -%s;" % (term2) )

                if not qiszero:
                    for symbol, coefficient in reaction.reactants:
                        self._write(
                            "jac[%d * %d + %d] -= %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))
                        
                    for symbol, coefficient in reaction.products:
                        self._write(
                            "jac[%d * %d + %d] += %d * qij;" % (j, nSpecies, mechanism.species(symbol).id, coefficient))

                        
        # Now, need specific heats and species internal energies (mass units)
        self._write()
        self._write()
        self._write(self.line('Begin computations of some of the terms needed for the rank-1 correction'))
        self._write()
        # now compute mass averaged specific heats apple
        self._write(self.line('Compute mixture-averaged specific heats first, using uj temporarily for CV/R'))
        self._write('cv_R(uj, tc);')
        self._write('cv = 0;')
        for species in self.species:
            self._write('cv += uj[%d]*y[%d]/%g; ' % (
                species.id, species.id, species.weight) + self.line('%s' % species.symbol))
            
        self._write('cv *= %g;' % (R*kelvin*mole/erg) )
        
        self._write()
        self._write(self.line('Compute internal energies for each species in mass units'))
        self._write( 'RTocv = %g*T/cv; ' % (R*kelvin*mole/erg) + self.line('R*T'))
        self._write('speciesInternalEnergy(uj, tc);')
        # convert e/RT to e with mass units
        for species in self.species:
            self._write('uj[%d] *= RTocv/%f; ' % (
                species.id, species.weight) + self.line('%s' % species.symbol))
        
        # Convert concentration jacobian to mass-fractions jacobian
        self._write()
        self._write(self.line('Convert Concentration J to mass-fractions J and add rank one correction'))
        knt = 0;
        for speciesj in self.species:
            wtj =  speciesj.weight
            j = speciesj.id
            for speciesi in self.species:
                wti = speciesi.weight
                i = speciesi.id
                line = 'jac[%d] = jac[%d]*%r' % (knt, knt, wti/wtj)
                if len(line) < 50:
                    line = line + ' '*(50 - len(line))
                self._write('%s - beta[%d]*uj[%d] ;' % (line, i, j))
                knt = knt + 1

        self._write()
        self._write(self.line('Restoring input vector sc back to CGS'))
        self._write('for (id = 0; id < %d; ++id) {' % nSpecies)
        self._indent()
        self._write('sc[id] *= 1e-6;')
        self._outdent()
        self._write('}')
        self._write('return;')

	self._outdent()
	self._write('}')
	return
    
    
    def _forwardCoefficients(self, mechanism, reaction):
        reaVect = {}
        
        for symbol, coefficient in reaction.reactants:
            key = mechanism.species(symbol).id
            if not reaVect.has_key(key):
                reaVect[ key ] = 0
            reaVect[key] += coefficient
            
        return reaVect
    
    def _reverseCoefficients(self, mechanism, reaction):
        reaVect = {}
        
        for symbol, coefficient in reaction.products:
            key = mechanism.species(symbol).id
            if not reaVect.has_key(key):
                reaVect[ key ] = 0
            reaVect[key] += coefficient
            
        return reaVect
    
    def _dReactionVector(self, mechanism, reactionCoefficients):

        dRV = {}
        for key in reactionCoefficients:
            term = []
            for key2 in reactionCoefficients:
                n = reactionCoefficients[key2]
                if key == key2:
                    n -= 1
                conc = "sc[%d]" % key2
                term += [conc] * n

            a1 = reactionCoefficients[key]
            a2 = "*".join(term)
            if len(a2) > 1:
                if a1 > 1:
                    a2 = "%s*" % a1 + a2
            else:
                a2 = "%s" % a1
                
            dRV[key] = a2
            
        return dRV
    
    def _dAlpha(self, mechanism, reaction):
        thirdBody = reaction.thirdBody
        if not thirdBody:
            import journal
            journal.firewall("fuego").log(
                "_enhancement called for a reaction without a third body")
            return

        nSpecies =  self.nSpecies
        
        species, coefficient = thirdBody
        efficiencies = reaction.efficiencies

        if not efficiencies:
            if species == "<mixture>":
                return [1 for x in range(nSpecies)]
            dalpha = [0 for x in range(nSpecies)]
            dalpha[ mechanism.species(species).id ] = 1;
            return dalpha

        dalpha   = [ 1 for x in range(nSpecies) ]
        for symbol, efficiency in efficiencies:
            factor = efficiency - 1
            dalpha[ mechanism.species(symbol).id ] += factor

        return dalpha

    def _hasPressureDependentReactions(self, mechanism):
        for reaction in mechanism.reaction():
            if reaction.low:
                return True
        return False

    def _hasThreeBodyReactions(self, mechanism):
        for reaction in mechanism.reaction():
            if reaction.thirdBody:
                return True
        return False
                
    def _hasSRIReactions(self, mechanism):
        for reaction in mechanism.reaction():
            if reaction.sri:
                return True
        return False
    
    def _hasTroeReactions(self, mechanism):
        for reaction in mechanism.reaction():
            if reaction.troe:
                return True
        return False
        
    def _dForwardRate(self, mechanism, reaction):
        
        dq = ["" for x in range(self.nSpecies)]
        
        lt = reaction.lt
        if lt:
            import journal
            journal.firewall("fuego").log("Landau-Teller reactions are not supported yet")
            return dq

        dim = self._phaseSpaceUnits(reaction.reactants)
        arrhenius = self._arrhenius(reaction, reaction.arrhenius)
        
        phi_f = self._phaseSpace(mechanism, reaction.reactants)
        forward = self._forwardCoefficients(mechanism, reaction)
        dphi_f = self._dReactionVector(mechanism, forward)
        self._write("phi_f = %s;" % phi_f)

        thirdBody = reaction.thirdBody
        if not thirdBody:
            uc = self._prefactorUnits(reaction.units["prefactor"], 1-dim)
            self._write("k_f = %g * %s;" % (uc.value, arrhenius))
            #self._write("q_f = phi_f * k_f;")
            for key in dphi_f:
                #self._write("dq_f_%d = %s * k_f;" % (key, dphi_f[key]) )
                dq[key] = "%s * k_f" % (dphi_f[key])
                
            return dq
            
        alpha = self._enhancement(mechanism, reaction)
        self._write("alpha = %s;" % alpha)

        dalpha = self._dAlpha(mechanism, reaction)

        sri = reaction.sri
        low = reaction.low
        troe = reaction.troe

        if not low:
            uc = self._prefactorUnits(reaction.units["prefactor"], -dim)
            self._write("k_fc = %g * %s;" % (uc.value, arrhenius))
            self._write("k_f  = k_fc * alpha;")
            #self._write("q_fc = phi_f * k_fc;")
            #self._write("q_f  = phi_f * k_fc * alpha;")
            for key in range(self.nSpecies):
                if dalpha[key] == 1:
                    if dphi_f.has_key(key):
                        #self._write("dq_f_%d = dq_c + %s * k_f;" % (key, dphi_f[key]) )
                        dq[key] = "dq_c + %s * k_f" % (dphi_f[key])
                    else:
                        #self._write("dq_f_%d = dq_c;" % (key) )
                        dq[key] = "dq_c"
                        
                elif dalpha[key] == 0:
                    if dphi_f.has_key(key):
                        #self._write("dq_f_%d = %s * k_f ;" % (key, dphi_f[key]) )
                        dq[key] = "%s * k_f" % dphi_f[key]
                else:
                    if dphi_f.has_key(key):
                        #self._write("dq_f_%d = dq_c * %f + %s * k_f;" % (key, dalpha[key], dphi_f[key]) )
                        dq[key] = "dq_c * %f + %s * k_f" % (dalpha[key], dphi_f[key])
                    else:
                        #self._write("dq_f_%d = dq_c * %f;" % (key, dalpha[key]) )
                        dq[key] = "dq_c * %f" % dalpha[key]
                        
            return dq

        self._write(self.line(" Begin block -- shared by all falloff reactions"))
        uc = self._prefactorUnits(reaction.units["prefactor"], 1-dim)
        self._write("k_high = %g * %s;" % (uc.value, arrhenius))
        k_0 = self._arrhenius(reaction, reaction.low)
        self._write("k_low = %g * %s;" % (uc.value, k_0))
        redP = "alpha *  k_low / k_high" 
        self._write("redP = 1e-6 * %s;  /* redP has units of concentration CGS */" % redP)
        self._write("F = redP / (1 + redP);")
        self._write("dFdP = 1 / (1 + redP) - redP / ((1+redP)*(1+redP));")
        self._write("k_f = k_high; " + self.line("forward coefficient for now..."))
        self._write(self.line(" End block -- shared by all falloff reactions"))
        
        if not sri and not troe:
            # Lindemann
            #self._write("chain1 = phi_f * k_f * dFdP * redP / alpha;")
            self._write(self.line(" Begin block -- Lindemann form !"))
            self._indent()
            self._write("chain2 = k_f * F;")
            self._write("k_fc   = k_f * dFdP * redP / alpha;")
            self._write("k_f *= F;")
            self._outdent()
            self._write(self.line(" End block -- Lindemann form !"))
            
        if sri:
            self._write(self.line("SRI form not implemented properly yet"))
            self._write("k_f *= F;")
            self._write("k_fc   = k_f * dFdP * redP / alpha;")

        elif troe:
            self._write(self.line(" Begin block -- Troe form !"))
            self._indent()
            self._write("logPred = log10(redP);")

            logF_cent = "logFcent = log10("
            logF_cent += "(%g*exp(T/%g))" % (1-troe[0], -troe[1])
            logF_cent += "+ (%g*exp(T/%g))" % (troe[0], -troe[2])
            if len(troe) == 4:
                logF_cent += "+ (exp(%g/T))" % (-troe[3])
            logF_cent += ');'
            self._write(logF_cent)
            
            d = .14
            self._write("troe_c = -.4 - .67 * logFcent;")
            self._write("troe_n = .75 - 1.27 * logFcent;")
            self._write("troe = (troe_c + logPred) / (troe_n - .14*(troe_c + logPred));")
            self._write("F_troe = pow(10, logFcent / (1.0 + troe*troe));")
            
            self._write(self.line(" begin -- difference approximation of dF_troe/dP"))
            self._indent();
            self._write("redPP  = redP*1.001+1e-8;")
            self._write("logPred = log10(redPP);")
            self._write("troe = (troe_c + logPred) / (troe_n - .14*(troe_c + logPred));")
            self._write("F_troe2 = pow(10, logFcent / (1.0 + troe*troe));")
            self._write("dF_troe = (F_troe2 - F_troe) / (redPP - redP) ;")
            self._outdent();
            self._write(self.line(" end -- difference approximation of dF_troe/dP"))
            self._write("dFdP = dFdP * F_troe + (redP/(1+redP)) * dF_troe ;")
            self._write("k_fc   = k_low * dFdP * 1e-6;")
            #self._write("chain1 = phi_f * k_low * dFdP * 1e-6;")
            self._write("chain2 = k_f * F * F_troe;")
            self._write("k_f *= F * F_troe;")
            self._outdent()
            self._write(self.line(" End block -- Troe form !"))
            
            
        for key in range(self.nSpecies):
            if dalpha[key] == 1:
                if dphi_f.has_key(key):
                    #self._write("dq_f_%d = chain1 + %s * chain2;" % (key, dphi_f[key]) )
                    dq[key] = "dq_c + %s * chain2" % dphi_f[key]
                else:
                    #self._write("dq_f_%d = chain1;" % (key) )
                    dq[key] = "dq_c"
                        
            elif dalpha[key] == 0:
                if dphi_f.has_key(key):
                    #self._write("dq_f_%d = %s * chain2 ;" % (key, dphi_f[key]) )
                    dq[key] = "%s * chain2" % dphi_f[key]
            else:
                if dphi_f.has_key(key):
                    #self._write("dq_f_%d = chain1 * %f + %s * chain2;" % (key, dalpha[key], dphi_f[key]) )
                    dq[key] = "dq_c * %f + %s * chain2" % (dalpha[key], dphi_f[key])
                else:
                    #self._write("dq_f_%d = chain1 * %f;" % (key, dalpha[key]) )
                    dq[key] = "dq_c * %f" % dalpha[key]
                    
                    
        return dq

    
    def _dReverseRate(self, mechanism, reaction):
        
        dq = ["" for x in range(self.nSpecies)]
        
        if not reaction.reversible:
            self._write(self.line("q_r = 0.0;"))
            return dq

        phi_r = self._phaseSpace(mechanism, reaction.products)
        reverse = self._reverseCoefficients(mechanism, reaction)
        dphi_r = self._dReactionVector(mechanism, reverse)
        
        self._write(self.line(" Begin block -- shared by all reversible reactions"))
        self._indent()
        self._write("phi_r = %s;" % phi_r)

        if reaction.rlt:
            import journal
            journal.firewall("fuego").log("Landau-Teller reactions are not supported yet")
            return dq

        if reaction.rev:
            self._write(self.line("reaction.rev is true in dReverseRate ..."))
            return dq
        
        K_c = self._Kc(mechanism, reaction)
        self._write("Kc = %s;" % K_c)
        self._write("k_r = k_f / Kc;")
        self._outdent()
        self._write(self.line(" End block -- shared by all reversible reactions"))
        #if reaction.thirdBody and not reaction.low:
        if reaction.thirdBody:
            #self._write("k_rc  = k_fc / Kc;     /* k_r = k_rc * alpha */ ")
            #self._write("q_rc = phi_r * k_rc;")
            self._write("dq_c = k_fc * (phi_f - phi_r / Kc);   " + 
                        self.line(" for all rxns with a thirdbody"))
        
        self._write()
        self._write(self.line(" Ready!"))
        for key in dphi_r:
            #self._write("dq_r_%d = %s * k_r;" % (key, dphi_r[key]) )
            dq[key] = "%s * k_r" % (dphi_r[key])
           
        return dq
    
    def _initializeJacobianCalculation(self, mechanism):

        nSpecies = len(mechanism.species())
        nReactions = len(mechanism.reaction())

        # declarations
        self._write()
        self._write('int id; ' + self.line('loop counter'))

        self._write('double mixture;                 '
                    + self.line('mixture concentration'))
        self._write('double g_RT[%d];                ' % nSpecies
                    + self.line('Gibbs free energy'))

        self._write('double Kc;                      ' + self.line('equilibrium constant'))
        self._write('double k_f;                     ' + self.line('forward reaction rate'))
        self._write('double k_r;                     ' + self.line('reverse reaction rate'))
        #self._write('double q_f;                     ' + self.line('forward progress rate'))
        #self._write('double q_r;                     ' + self.line('reverse progress rate'))
        self._write('double phi_f;                   '
                    + self.line('forward phase space factor'))
        self._write('double phi_r;                   '
                    + self.line('reverse phase space factor'))

        if self._hasThreeBodyReactions(mechanism):
            self._write('double alpha;                   ' + self.line('enhancement'))
            self._write('double dq_c, k_fc;              ' + self.line('intermediates for thirdbody rxns'))

        if self._hasPressureDependentReactions(mechanism):
            self._write('double redP;                    ' + self.line('reduced pressure'))
            self._write('double logPred;                 ' + self.line('log of above'))
            self._write('double F;                       '
                        + self.line('fallof rate enhancement'))
            self._write('double dFdP, chain2;            ' + self.line('intermediates for pressure dep. fall-off rxns'))

            
        if self._hasTroeReactions(mechanism):
            self._write()
            self._write('double F_troe;                  ' + self.line('TROE intermediate'))
            self._write('double logFcent;                ' + self.line('TROE intermediate'))
            self._write('double troe;                    ' + self.line('TROE intermediate'))
            self._write('double troe_c;                  ' + self.line('TROE intermediate'))
            self._write('double troe_n;                  ' + self.line('TROE intermediate'))
            self._write('double redPP, F_troe2, dF_troe; ' + self.line('d F_troe / d Pr'))
            self._write('double k_low, k_high;           ')

        if self._hasSRIReactions(mechanism):
            self._write()
            self._write('double X;                       ' + self.line('SRI intermediate'))
            self._write('double F_sri;                   ' + self.line('SRI intermediate'))
        
        self._write()

        self._write(
            'double T = *pT; '
            + self.line('temporary temperature'))
        self._write(
            'double tc[] = { log(T), T, T*T, T*T*T, T*T*T*T }; '
            + self.line('temperature cache'))

        # compute the reference concentration
        self._write()
        self._write(self.line('reference concentration: P_atm / (RT) in inverse mol/m^3'))
        self._write('double refC = %g / %g / T;' % (atm.value, R.value))

        # compute the Gibbs free energies
        self._write()
        self._write(self.line('compute the Gibbs free energy'))
        self._write('gibbs(g_RT, tc);')
        
        return
    
    def _boxedReaction(self, reaction):
        self._write(self.line('*'*80))
        kind = 'Standard form'
        if reaction.lt:
            kind = '(Landau-Teller)'
        elif reaction.low:
            if reaction.sri:
                kind = '(SRI)'
            elif reaction.troe:
                kind = '(Troe)'
            else:
                kind = '(Lindemann)'
        elif reaction.thirdBody:
            kind = '(Three-Body Reactions)'
        
        rxnstring = '        reaction %d: %s -- %s' % (reaction.id, reaction.equation(), kind)
        if len(rxnstring) < 80:
            rxnstring = rxnstring + ' '*(80 - len(rxnstring))
        self._write(self.line(rxnstring))
        self._write(self.line('*'*80))
        return
        

# version
__id__ = "$Id: CPickler.py,v 1.1.1.1 2007-09-13 18:17:30 aivazis Exp $"

#  End of file 
