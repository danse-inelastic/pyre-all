Advanced topics
===============

.. _pyre-directory-structure:

Pyre project structure
------------------------

A pyre project typically contains a number of directories.  For example, supposing one wishes to create a pyre module wrapping several molecular dynamics codes.  The pyre application directory structure would be configured with the following subdirectories, assuming the project name (and top-level directory) is named moldyn:

applications/
^^^^^^^^^^^^^
Pyre applications typically are put in this directory with a :ref:`Make.mm <make-mm>` that exports them to the pythia-0.8/bin directory.  :ref:`Pyre convention <pyre-style>` appends a "d" to the app name if it is a service daemon.  

etc/
^^^^
This directory stores facility factory method files, called :ref:`odb files <odb-pml-files>`, for switching facilities at run time.  The internal structure of etc/ mirrors the structure of the application and its components.  For example suppose the application is called MdApp with the inventory::

    class MdApp(Script):
    
        class Inventory(Script.Inventory):
            import pyre.inventory as inv 
            mdEngine = inv.facility('mdEngine', default='gulp')
            mdEngine.meta['known_plugins'] = ['gulp','mmtk']
            mdEngine.meta['tip'] = 'which md engine to use'

Then etc/ would have the structure::

    $ ls etc
    Make.mm MdApp
    $ ls etc/MdApp
    gulp.odb mmtk.odb lammps.odb cp2k.odb
    
<package>/
^^^^^^^^^^
This is the top level directory for python source.

lib<package>/
^^^^^^^^^^^^^
This contains possible c extensions.

<package>module/
^^^^^^^^^^^^^^^^
This contains python bindings to the c extensions.

tests/
^^^^^^
Tests for all parts of the project.

Although this directory structure is not mandatory, it is somewhat conventional.  Much of this structure can be generated automatically by using the :ref:`package utility<create-a-pyre-project>`. 


.. _pyre-inventory-implementation:

Inventory, Trait, and Notary
----------------------------

Inventory has descriptors as its static members. 
Descriptors are special python objects that defines __get__ (and __set__) methods. 
(Note: they are not instances of pyre.inventory.Descriptor.Descriptor. 
class pyre.inventory.Descriptor.Descriptor is not really a Descriptor class meant by
http://users.rcn.com/python/download/Descriptor.htm. 
In pyre, pyre.inventory.Trait.Trait is the real Descriptor class.) 
An instance of descriptor describe a property of his parent, but does not hold the
value of this property. 
This is why you can inherit Inventory but its static members do not conflict in 
different instances of Inventory classes.

For example ::

  class Inventory(Component.Inventory):
  
      import pyre
  
      a = pyre.inventory.str('a', default="" )

Here pyre.inventory.str makes a Str instance. Str is a subclass of Trait. 
So the instance Inventory.a is a descriptor that says the instance of 
Inventory class will have a property called a. 
This property is a string, and it defaults to be empty.

When Inventory class is instantiated, ::

  inventory = Inventory(...)

and when we are asking for its property, ::

  inventory.a

The __set__ and __get__ functions of Trait class will get called and which, 
in turn, calls getTraitValue and setTraitValue of the Inventory class. 

So you can see the class Trait and Inventory have to cooperate to
implement this idea of Descriptor.

Notary
^^^^^^
Inventory has its metaclass pyre.inventory.Notary.Notary. 
The metaclass's __init__ will be called when the object of the class 
(Note: the class object != the class instance) is built. 
In Notary's __init__, all traits of an Inventory class will be 
collected to two registries, one for properties, and one for facilities.


Class Diagrams
^^^^^^^^^^^^^^


Here is how it handles internally inventory items:

.. image:: images/PyreInventoryClassDiagram.png

Here is how it handles the common parts of odb and db-type files:

.. image:: images/PyreOdbCommonClassDiagram.png

Here is how it handles odb files:

.. image:: images/PyreOdbFsClassDiagram.png

and db-type "files":

.. image:: images/PyreOdbDbmClassDiagram.png


.. This appears to be a stub.  Real db interaction is managed by :ref:`pyre.db <pyre-db>`.



Listing of reserved methods for pyre components and scripts
-----------------------------------------------------------

In reality, any method of a used by Component is "reserved", but here are some of the more obvious ones to avoid overriding (but instead use in your application):

* _configure()
* _defaults()
* _init()
* _fini()
* configureComponent()
* 

(give some examples of how each of these may be used--start with vnf's redirect)


.. _weaver:

Pyre rendering: Weaver
----------------------

A typical pyre pattern is to move rendering methods to a class under the generic name "weaver", which makes use of the visitor pattern while traversing structure and data objects using a number of underlying mills.  Examples include generating html pages in opal or gemetrical pml files in pyre.geometry. (give example of pattern and postulate how to use it when basing one's code on pyre)



