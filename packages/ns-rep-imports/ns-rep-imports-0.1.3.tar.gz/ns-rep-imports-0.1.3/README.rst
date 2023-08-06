=================================
Welcome to NS-REL-IMPORTS's docs!
=================================


Simple rel import generator module
==================================

Generates Realitive info with a camel to snake conversion of class name.

.. code-block:: python

    >>> from rel import mod_rel as RelInfo

    >>> obj_str = 'awt.uno.XInterface'
    >>> ns = 'awt.grid'
    >>> rel = RelInfo.get_rel_import(in_str =obj_str, ns=ns)
    >>> print(f"from {rel.frm} import {rel.imp}")
    from ..uno.x_interface import XInterface

