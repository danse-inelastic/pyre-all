# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

include local.def

PROJECT = nttcp
PACKAGE = libnttcp

PROJ_SAR = $(BLD_LIBDIR)/$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_BINDIR)/$(PACKAGE).$(EXT_SO)
PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_CLEAN += $(PROJ_SAR) $(PROJ_DLL)

PROJ_SRCS = \

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# build the library

all: $(PROJ_SAR) export

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ifeq (Win32, ${findstring Win32, $(PLATFORM_ID)})

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_DLL) \
	-Wl,--out-implib=$(PROJ_SAR) $(PROJ_OBJS)

# export
export:: export-headers export-libraries export-binaries

else

# build the shared object
$(PROJ_SAR): product_dirs $(PROJ_OBJS)
	$(CXX) $(LCXXFLAGS) -o $(PROJ_SAR) $(PROJ_OBJS)

# export
export:: export-headers export-libraries

endif

EXPORT_HEADERS = \

EXPORT_LIBS = $(PROJ_SAR)
EXPORT_BINS = $(PROJ_DLL)


# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:45 aivazis Exp $

#
# End of file
