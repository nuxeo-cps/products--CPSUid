=============
CPSUid README
=============

:Author: Anahide Tchertchian
:Revision: $Id$


CPSUid provides a unique identifier implementation for CPS documents.


Features
========

CPSUid provides :

- identification profiles registration: profiles are declared to be used
  for a list of given portal types.
- unique id registration: unique ids are stored on the object, and
  incremented given the last unique id used.
- unique id handling: given a uid, objects using this id can be found.


Install
=======

CPSUid comes with an extension profile definition.
Go into portal_setup at the root of the site, choose the 'import' tab, and
import the CPSUid profile.



More information
================

See the doc subsection



.. Emacs
.. Local Variables:
.. mode: rst
.. End:
.. Vim
.. vim: set filetype=rst:
