.. _pyre-basics:

Pyre basics: Inventory, Component, and Application
==================================================

.. The pyre framework is a Python-based system for constructing applications. Applications consist of a top level application component and a set of lower level components. The framework performs services such as instantiating components, configuring them, and cleaning up. A pyre component is the basic chunk of code managed by the pyre framework.  A component contains a "unit of functionality", whether one class or many, which requires certain settings before runtime.  A component may in turn pass settings to a subcomponent and so on.  The power of pyre is in taking an arbitrarily long, complex, interrelated set of configurations and being able to sort them out and pass them to all the underlying subcomponents so that they are configured in the correct order and dependencies are satisfied.

.. As the component "unit of functionality" is left undefined, it is up to the pyre architect to decide at what level they would like to divide their code into components.  Some may choose to create entire computational engines as components that can be swapped in and out based on a user's preferences.  Others may elect to fine-grain the component nature of their engines, such as creating components for a forcefield within a physics engine that can be altered at configuration time, or even the individual forcefield components.

.. Pyre is one package of pythia, a larger collection of related systems such as a distributed communication system (journal), code-generators (weaver), GUI generators (blade), and a build system (merlin).

If you have not read :ref:`the tutorial <pyre-tutorials>`, you may want to read it and try out the examples to get a feel for pyre components and applications. Here, we cover in more depth these key concepts:

 * Inventory

   * Trait(Descriptor)
   * Property
   * Facility

 * Component
 * Application
 

.. _pyre-inventory:

Inventory: properties and facilities
------------------------------------

In pyre, a component's inventory is the place where user inputs are 
connected to a pyre component.  In the inventory of a pyre component, all publicly configurable items
are declared using `descriptors <http://users.rcn.com/python/download/Descriptor.htm>`_ (traits), are special python objects that describe attributes of a python instance.


There are two kinds of descriptors for a pyre inventory: properties or facilities.
All properties are instances of pyre.inventory.Property.Property, and usually they are instances of a property subclass, such as int, float, str, etc. 

A full list of all inventory properties is shown below:

.. autofunction:: pyre.inventory.array
.. autofunction:: pyre.inventory.bool
.. autofunction:: pyre.inventory.dimensional
.. autofunction:: pyre.inventory.float
.. autofunction:: pyre.inventory.inputFile
.. autofunction:: pyre.inventory.int
.. autofunction:: pyre.inventory.list
.. autofunction:: pyre.inventory.outputFile
.. autofunction:: pyre.inventory.preformatted
.. autofunction:: pyre.inventory.slice
.. autofunction:: pyre.inventory.str

.. .. automodule:: pyre.inventory
   :members: array bool dimensional float inputFile int list outputFile preformatted slice str
   :undoc-members:

The programmer can specify the public name of a property, a default value, and a validator. For example::

  import pyre.units.energy
  energy = pyre.inventory.dimensional(
      name='energy', 
      default=50*pyre.units.energy.meV, 
      validator=pyre.inventory.less(1*pyre.units.energy.eV))

Here pyre.inventory.dimensional is a factory method creating a property of dimensional type, and all user inputs
for this property will be casted into this type.  Keyword "name" specifies the name of the property, and this name will be the key that pyre framework will use to find its user configuration.
Keyword "default" specifies the default value;
Keyword "validator" specifies a method that validate the user input. The following is a complete list of validators:

.. autofunction:: pyre.inventory.less
.. autofunction:: pyre.inventory.lessEqual
.. autofunction:: pyre.inventory.greater
.. autofunction:: pyre.inventory.greaterEqual
.. autofunction:: pyre.inventory.range
.. autofunction:: pyre.inventory.choice


In the above example, a pyre built-in validator pyre.inventory.less is used. Another useful validator is choice, which allows users to input only certain type of property::

  mdEngine = pyre.inventory.facility("mdEngine")
  mdEngine.validator = pyre.inventory.choice('mmtk','gulp')

and will throw an error if another is input. The above snippet also demonstrates the attribute method of specifying property information.

Facility and other factory functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are also factory functions which produce pyre objects themselves.  Here is a complete listing:

.. autofunction:: pyre.inventory.facility
.. autofunction:: pyre.inventory.curator
.. autofunction:: pyre.inventory.registry

.. .. automodule:: pyre.inventory.__init__
     :members: facility curator registry
     :undoc-members:

A facility is how one component (let's call it A) specifies that it would like another 
component to do some work for it. It's a bit like a help-wanted ad. The curator looks through the :ref:`depositories <where-to-put-pml-odb>` where :ref:`xml data<pml-files>` about pyre components are kept in order to populate the inventory.   and tries to wherekeeps track of the inventory items.  The registry is simply the list of inventory items themselves. 


Difference between factory and default keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As part of the facility declaration, A gets to recommend a default component to do the job,
or it can recommend a way to build a component to do the job. 
Users get the final decision: they can direct that a different component be used, 
specifying that on the command line or through a configuration file (.pml).

In this example::

   greeter = pyre.inventory.facility(name='greeter', factory=Greeter)

A factory method is given and the default component is to be used is created from
calling the factory method

In this example::

   greeter = pyre.inventory.facility(name='greeter', default=Greeter())

A default component is specified.

The difference between this two approaches is that in the second case
the default component is one single instance, like a singleton.
This could lead to some strange behavior of your application if you
don't design your application carefully. 
On the other hand, using the first approach is a safe choice.

For more details of how pyre inventory works, please consult
:ref:`pyre-inventory-implementation`.


.. _pyre-component:

Components
---------------

Pyre component structure is relatively straightforward.  The component class is inherited from pyre.inventory.Component.  It should contain an inner class called Inventory, which usually subclasses the Inventory class of the parent.  It may also override a number of methods which are hooks in the framework to do certain tasks.  Some of the more frequently-used methods include:

__init__(): the constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The constructor must call the parent's constructor::

  super(Sentry, self).__init__(name)

Here the name argument specifies the name of this component (i.e. 'sentry'). 


_defaults(): setting default values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each command-line configurable item in the inventory may be given a default value when declared in the Inventory.  If you need to give them a new default for whatever reason, use the _defaults() method:: 

  self.inventory.username = 'bob'

and this will override the default value. However, if users specify another value
for this property through command line or configuration files, it will be overriden.


_configure(): transfer user inputs to local variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
During component configuration, external command-line or configuration file inputs are parsed by the framework,
checked for errors and stored in the object "self.inventory".
Any property or component is accessed as the attribute of this object.
For example, if you declare a string-type property in the inventory::

  filename = pyre.inventory.str('filename')

self.inventory.filename now contains the value of "filename" provided by the user.
In the _configure method, you can transfer this value to local variables of the component::

  self.filename = self.inventory.filename

allowing the component to use these external application-level inputs.


_init(): initialization of computing engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method will be called after every component is configured. 
The method _configure() will already have been called at this time for all components.
This is the place where the computing engine should be constructed.
Usually, in _init() one will want to prepare everything so that the
component is ready to run; for example, you may want to allocate memory,
open input/output files, initiate c/c++/fortran engines that this
component is depending on, etc.

.. todo:: discuss the order in which component methods are called by the framework

The class structure for Components is relatively simple:

.. inheritance-diagram:: pyre.components.Component 
   :parts: 4

Frequently users would like to know which parts of their code to componentize.  The answer is that components represent a "unit of functionality" and so do not have to "wrap each class", but should wrap parts of the code which one would like to interchange or develop separately.




Applications
------------
A pyre application is simply the top-level component that can also be "executed".  
As such it can be run from the command line or started as a daemon.

The body of a pyre application is exactly the same as that of a component, except for the presence of a main() method which is called when the user instantiates the application and calls its run() method::

 myApp = MyApp()
 myApp.run()

Although there are a variety of applications in pyre:

.. inheritance-diagram:: pyre.applications.Application pyre.applications.ClientServer pyre.applications.CommandlineParser pyre.applications.ComponentHarness pyre.applications.Daemon pyre.applications.DynamicComponentHarness pyre.applications.Executive pyre.applications.Script pyre.applications.ServiceDaemon pyre.applications.ServiceHarness pyre.applications.Stager
   :parts: 1

most users subclass pyre.applications.Script.Script.  This allows users to leverage one of the strengths of pyre, which is a systematic way to configure and distribute from the command line all inventory items at run time by simply passing them at the commandline of the application::

  MyApp.py --property=value1 --facility=value2

Although properties can be changed easily, for the above to work for facilities, an odb file must also be present, as discussed in the next section.

.. _odb-files:

Odb files: Swapping subcomponents
---------------------------------

To swap subcomponents one must have a factory function in a python file ending in odb.  This factory returns an instance of the subcomponent to be swapped.  For example, suppose we have a greeter component in :ref:`GreetApp <helloworld-greet.py>` from the tutorial::

     class GreetApp(Script):
     
         class Inventory(Script.Inventory):
     
             greeter = pyre.inventory.facility( 'greeter', default = Greeter('greeter') )
     
             ...

And we want to change the default choice of greeter to an odb file called morning.odb::

     # morning.odb

     from Greeter import Greeter
     
     def greeter():
         from Greeter import Greeter
         class Morning (Greeter):
             def _defaults(self): self.inventory.greetings = "Good morning"
         return Morning('morning')

By specifying a different greeter::

  $ python greet.py --greeter=morning
  Good morning World!

We can swap subcomponents dynamically.  A user may also configure the application using xml input files.  These are called pml files, discussed next.

.. _pml-files:

Pyre pml files
--------------

A pml file is an xml file that assigns values to properties, components, and facilities in an application, allowing a user to override the default values assigned in the respective inventories.

To change the values of a property simply hand-edit the value, which has the general form::

    <property name='key'>value</property>

The name of the pml file must be <component_name>.pml. Facilities may also be configured in a  similar manner::

    <facility name='greeter'>morning</facility>

Pml files and odb files may be placed in a number of locations called depositories.

.. _where-to-put-pml-odb:

Depositories
------------

There are several places to put pml and odb files, depending on the scope you'd like them to have.

   1. Files meant to override variables system-wide should be put in the :ref:`pyre installation root<advancedInstall>`, in <pyre root>/etc/<application name>/<component name>.pml, where <application name> is the name of the pyre app, and <component name> is the name of the component. For example, system-wide pml files for myApp.py should be in <pyre root>/etc/myApp.  To do this one must :ref:`compile and install pyre from source<advancedInstall>`.

   2. Files meant to override variables for just one user should be in a directory called .pyre immediately beneath the user's home directory. Example: /home/user/.pyre/myApp

   3. Files meant to be local overrides should go in the local directory.  For example, for myApp.py one should have myApp.pml in that directory. 

The order of precedence is: 3 beats the others, 2 beats 1, and 1 beats whatever the default is. 


.. _mmtk:

Science example: swapping molecular dynamics engines
-----------------------------------------------------

To understand more about how pyre is useful, we illustrate component swapping with a small `molecular dynamics code <http://docs.danse.us/MolDyn/sphinx>`_ which uses pyre to dynamically change md engine components at run time.


..  also The inventory stores all the settings for the component as properties, as well as additional subcomponents as facilities.  Each of these may have multiple options.  For example, in the 

.. By having an explicit place to interact with the component, components gain the ability to control whether they accept a given change, and what to do with that setting.   External inputs such as those from the command line, a higher-level component, or a GUI, are stored in inventory items.    






