.. _installation:

Basic Installation
==================

Pyre is the base package in a larger group of software packages built upon it and collectively called pythia-0.8.  However, we frequently use the word pyre to represent pythia as well, especially when discussing installation.  Pythia can either be installed as a python-only set of modules as discussed below, or as a group of python modules with some c extensions discussed :ref:`later<advancedInstall>`. 


Prerequisites
-------------

Currently pythia-0.8 has only been well-tested with python 2.5, and has recently been shown to have some metaclass incompatibilities with python 2.6.  Although pythia-1.0 will be completely compatible with python 3.0, for now we recommend using python 2.5 until the incompatibilties can be removed.


.. _pure-python-distrib:

Python-only distribution
-------------------------

The python-only version of pyre is a good starting point to try out pyre.

From an egg
^^^^^^^^^^^

Assuming you have the `easy install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_   package already on your system::

  $ easy_install -f http://dev.danse.us/packages pythia


From a zip file
^^^^^^^^^^^^^^^

First, download the `zip file <http://www.cacr.caltech.edu/projects/danse/pyre/pythia-0.8-patches.zip>`_. Second, add the zipfile to your $PYTHONPATH. For example, if you are using bash::

  $ export PYTHONPATH=/path/to/downloadedzip:$PYTHONPATH


.. _pyre-tutorials:

10-minute Tutorial
==================

If you have not done so, please :ref:`install <installation>` pythia-0.8 before you try out the following examples.

This is the pyre version of hello world. It introduces some structures into the simple one-liner ::

    print "Hello World!"

In this tutorial we build a pyre application step-by-step, gradually adding structure and explaining why those structures are needed.


.. _helloworld1:

The simplest pyre application
-----------------------------

Open your favorite editor and type in the following (or download it: `hello1.py <tutorials/hello1.py>`_)::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class HelloApp(base):

      def main(self):
	  print "Hello World!"
	  return

      def __init__(self, name='hello1'):
	  super(HelloApp, self).__init__(name=name)
	  return

  # main
  if __name__ == "__main__":
      app = HelloApp()
      app.run()

  # End of file


Save it as hello1.py and run it::

  $ python hello1.py
  Hello World!

Here are a few things to note:

 * A pyre application needs to inherit from pyre.applications.Script.Script.
 * It needs a method named "main". This method will be executed when the application is launched.
 * The application's constructor has a keyword argument "name", and this name 
   is the key the pyre framework will use to find the application's
   configuration items.

You may wonder why we need this larger pyre application instead of
just using the python one-liner to achieve the same effect::

  >>> print "Hello World!"

This will become apparent in the next few sections.  The next step is to make this application a little more configurable
and interesting.


Say hello to someone
--------------------

Please create a new python file "hello2.py" and type in the following code 
(or download it: `hello2.py <tutorials/hello2.py>`_)::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class HelloApp(base):

      class Inventory(base.Inventory):

	  import pyre.inventory

	  name = pyre.inventory.str(name='name', default='World')


      def main(self):
	  print "Hello " + self.name + "!"
	  return


      def _configure(self):
	  super(HelloApp, self)._configure()
	  self.name = self.inventory.name
	  return


      def __init__(self, name='hello2'):
	  super(HelloApp, self).__init__(name=name)
	  return


  # main
  if __name__ == "__main__":
      app = HelloApp()
      app.run()

  # End of file

To try it out, please type in the following command::

  $ python hello2.py
  Hello World!

And you can change the person you want to say hello::

  $ python hello2.py --name=Bob
  Hello Bob!

Comparing this to the :ref:`previous example <helloworld1>`, we note a few things 
are added or modified:

* Inventory

  There is an inner class called Inventory, where publicly cofigurable items are listed.
  In the simple application above, Inventory has one item,
  "name", which is the name of the person to whom we say hello::

    name = pyre.inventory.str(name='name', default='World')

  This statement declares there is a public property for
  this application, its type is a string, its name is "name",
  and its default value is "World".
  Pyre instantiates Inventory with the lower case name "inventory", looks
  for user inputs for its properties when the application is
  launched, parses user inputs to appropriate data types,
  and feeds the value to::

    self.inventory.name

  where self is the application.


* _configure()

  Here we create a local variable and pass it the value of the property
  "name", which is managed by the pyre framework::

    self.name = self.inventory.name


* main()

  Here we change the print message so that we
  will say hello to the person defined by the variable "name"::

    print "Hello "+self.name+"!"


* __init__()

  In the constructor, we give this application the name "hello2".
  This name is a identifier that pyre framework will use to
  look for configurations.  


Although it is useful to have a system to manage commandline inputs, both to an application and to its components,
wouldn't it be useful to have alternative ways to configure a program? Pyre allows xml input through the use of :ref:`pml files <pml-files>`, which are given the .pml ending. 

.. None of the following works because the user has not installed templates yet

..For example, we can use pml files
  to configure this demo pyre application.  Let us create a pml file by using one of the pyre :ref:`templates <templates>`::

    $ inventory.py --name=hello2
    creating inventory template in 'hello2.pml'

.. Now we edit the hello2.pml to look like ::

To try this feature out, create the following xml file and save it as hello2.pml::

  <!DOCTYPE inventory>

  <inventory>

    <component name='hello2'>
      <property name='name'>Alice</property>
    </component>

  </inventory>

With this file in your current directory, you will see something different::

  $ python hello2.py
  Hello Alice!

Pyre looks for pml files by looking for the
names of pyre components/applications, which in this case is "hello2".
If you change the name of the pml file, for example, to hello2a.pml,
you will end up with ::

  $ python hello2.py
  Hello World!

because there is no component named hello2a.


.. _helloworld-greet.py:

Greet someone in different ways
-------------------------------
In this example we need the following python modules (or you can download them: 
`greet.py <tutorials/greet.py>`_ ,
`Greeter.py <tutorials/Greeter.py>`_ 
). The first one is a
pyre application "greet.py"::

  #!/usr/bin/env python

  from pyre.applications.Script import Script as base

  class GreetApp(base):

      class Inventory(base.Inventory):

	  import pyre.inventory

	  from Greeter import Greeter
	  greeter = pyre.inventory.facility(name='greeter', factory=Greeter)
	  name = pyre.inventory.str(name='name', default='World')


      def main(self):
	  self.greeter.greet(self.name)
	  return


      def _configure(self):
	  super(GreetApp, self)._configure()
	  self.name = self.inventory.name
	  self.greeter = self.inventory.greeter
	  return


      def __init__(self, name='greet'):
	  super(GreetApp, self).__init__(name=name)
	  return


  # main
  if __name__ == "__main__":
      app = GreetApp()
      app.run()

  # End of file

and the second one is a pyre component "Greeter.py"::

  # -*- Python -*-

  from pyre.components.Component import Component


  class Greeter(Component):


      class Inventory(Component.Inventory):

	  import pyre.inventory

	  greetings = pyre.inventory.str('greetings', default='Hello')


      def greet(self, name):
	  print self.greetings + ' ' + name + '!'
	  return


      def __init__(self, name='greeter'):
	  Component.__init__(self, name, facility='greeter')
	  return


      def _configure(self):
	  super(Greeter, self)._configure()
	  self.greetings = self.inventory.greetings
	  return


  # End of file 

Let's try it out::
   
  $ python greet.py
  Hello World!

  $ python greet.py --name=Bob
  Hello Bob!

  $ python greet.py --name=Bob --greeter.greetings=Hi
  Hi Bob!

You see we can now not only configure the target of the greetings,
but also the content of the greetings.  There are a few things to note:

* facility()

  A facility is a way a component can declare it needs 
  another component to do some work for it.
  This is a useful feature of pyre, enabling developers
  to construct software in layers and keep each component
  small, dedicated and manageable.

  This "greet" application now delegates its functionality to
  "greeter". It may look unecessary at first glance, but the benefit of this delegation will become obvious for larger, more complex applications. To declare a subcomponent one needs::

    greeter = pyre.inventory.facility(name='greeter', factory=Greeter)

  in the inventory, which means the app "greet" needs a component
  "greeter" to work correctly. The "name" keyword in this declaration
  tells pyre it needs to look for the name "greeter"
  in order to configure this facility. The "factory" keyword tells
  pyre it can use the assigned factory method
  to create a pyre component and use that component as the default
  component for this greeter facility.

Now let's look at Greeter. The Greeter component
is similar to hello1.py, hello2.py, and greet.py. 
It inherits from pyre.components.Component.Component, adds a publicly settable 
property, "greetings", to its inventory, and alters _configure()
and __init__() slightly to accomodate its new behavior. 

* One extra thing worth mentioning is we create a method "greet", which takes an argument "name"
  which is the target of greetings. This method
  is called by the pyre app "greet" in its method "main".

* We also notice in the commandline argument::

    --greeter.greetings=Hi

  how the string "greeter" denotes the "greeter" component,
  and the string "greeter.greetings" denotes the property
  "greetings" of the component "greeter".


Greeting someone in dynamically-loaded different ways
-----------------------------------------------------

Now we demo another component to show the benefit
of using facilities. Please create `fancy-greeter.odb <tutorials/fancy-greeter.odb>`_
with the following content::

  # -*- Python -*-

  from pyre.components.Component import Component


  class Greeter(Component):


      class Inventory(Component.Inventory):

	  import pyre.inventory

	  decoration = pyre.inventory.str('decoration', default='*')
	  greetings = pyre.inventory.str('greetings', default='Hello')


      def greet(self, name):
	  s = self.greetings + ' ' + name + '!'
	  s = ' '.join([self.decoration, s, self.decoration])

	  print self.decoration*(len(s))
	  print s
	  print self.decoration*(len(s))
	  return


      def __init__(self, name='fancy-greeter'):
	  Component.__init__(self, name, facility='greeter')
	  return


      def _configure(self):
	  super(Greeter, self)._configure()
	  self.greetings = self.inventory.greetings
	  self.decoration = self.inventory.decoration
	  return


  def greeter(): return Greeter()

  # End of file 


Try the following command::

  $ python greet.py --name=Bob --greeter.greetings=Hi --greeter=fancy-greeter
  ***********
  * Hi Bob! *
  ***********

The extra command line option ::

  --greeter=fancy-greeter

tells pyre to use the component named "fancy-greeter" instead
of the default component for the facility "greeter". 
Pyre then looks for fancy-greeter by looking for "fancy-greeter.odb" in :ref:`various directories<where-to-put-pml-odb>`, including the current one. The module fancy-greeter.odb must contain a "def greeter()" method which
is the *facility name* this component will plug into.
Thus the method "greeter" returns a pyre component which will 
be used as the "greeter" subcomponent of the main application.

Although the above examples are primitive, their features are useful to scientific development as shown in the :ref:`science use cases <indexScienceUseCases>`.  They help automate tasks such as switching computational engines at runtime, coupling different time/length scale physics engines, abstracting parallelism, and more. Pyre is extremely versatile.  It can also be used to create `web and desktop user interfaces <http://dev.danse.us/trac/luban>`_ to such engines. 

Where to go from here?  You could continue in the :ref:`first section<pyre-basics>` of the user's guide, which reviews much of what is taught here and illustrates it with a :ref:`science tutorial<mmtk>`, or you could jump straight into a discussion of :ref:`available pyre libraries<pyrePackages>` for use in your code, finishing with a tutorial about :ref:`how to create your own pyre project<createPyreProject>`, and another tutorial showing :ref:`how to create a virtual neutron experiment<mcvine>`. 

.. For example, if you have an application that does parametric fitting and this application makes use of a optimizer, you can declare an "optimizer" facility and use pyre's internal component-handling machinery to tell the application to switch optimizers from the command line.

