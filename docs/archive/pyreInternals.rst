Pyre Internals
==============

Pyre has a complex internal structure.  Here we discuss some of it's internal workings for the benefit of those who would like to extend it.


.. _pyre-components:

pyre.components
---------------

Here is the class diagram for pyre's component:

.. image:: images/PyreComponentClassDiagram.png




.. _pyre-parsing:

pyre.parsing
------------

Here is the class diagram for pyre's parsing utilities:

.. image:: images/PyreParsingClassDiagram.png

It's classes in turn use locators for the files they parse:

.. image:: images/PyreParsingLocatorsClassDiagram.png



.. _pyre-filesystem:

pyre.filesystem
---------------

Here is the class diagram for pyre's tools for managing filesystems:

.. image:: images/PyreFilesystemClassDiagram.png



.. _weaver-structure:

Struture of pyre's weaver rendering utility
-------------------------------------------

This is a structural discussion of weaver.  See :ref:`<weaver>` for the purpose of weaver and how to extend it.  Here is its class diagram:

.. image:: images/PyreWeaverClassDiagram.png


Here is the class diagram for weaver's componenets:

.. image:: images/PyreWeaverComponentsClassDiagram.png


Here are its internal mills (classes that "render" pyre data structures):

.. image:: images/PyreWeaverMillsClassDiagram.png




.. _opal-structure:

Opal: basic web framework 
-------------------------

Here is the class diagram of opal:





.. _journal-structure:

Journal: structure and architecture 
-----------------------------------


Here is the class diagram of journal:

.. image:: images/JournalTopLevelClassDiagram.png

Here are journal's services:

.. image:: images/JournalServicesClassDiagram.png

Here are journal components:

.. image:: images/JournalComponentsClassDiagram.png

Here are journal's devices:

.. image:: images/JournalComponentsClassDiagram.png

and it's diagnostics tools:

.. image:: images/JournalDiagnosticsClassDiagram.png
