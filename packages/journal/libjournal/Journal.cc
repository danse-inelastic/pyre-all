// -*- C++ -*-
//
//--------------------------------------------------------------------------------
//
//                              Michael A.G. Aivazis
//                       California Institute of Technology
//                       (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
//--------------------------------------------------------------------------------
//

#include <portinfo>
#include <string>
#include <ostream>

#include "Device.h"
#include "Journal.h"

#include "StreamDevice.h"
#include "Console.h"


using namespace journal;

// meta-methods

Journal::Journal() :
    _device(new Console)
{}

Journal::~Journal() {
    delete _device;
}

// version
// $Id: Journal.cc,v 1.1.1.1 2006-11-27 00:09:37 aivazis Exp $

// End of file
