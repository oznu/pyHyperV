pyHyperV
========


.. image:: https://pypip.in/v/pyHyperV/badge.png
        :target: https://crate.io/packages/pyHyperV

.. image:: https://pypip.in/d/pyHyperV/badge.png
        :target: https://crate.io/packages/pyHyperV

Simple client for calling HyperV orchestrator runbooks in python.

.. contents::
    :local:
    
.. _installation:

============
Installation
============

Using pip::

    $ pip install pyHyperV
    
    
============================
Import & Initialize pyHyperV
============================

.. code:: python

    import pyHyperV
    
    orchestratorEndpoint = "http://hostname.local:81/Orchestrator2012/Orchestrator.svc/Jobs"
    username = "domain\\username"
    password = "password"
    
    o = pyHyperV.orchestrator(orchestratorEndpoint, username, password)
    

===============
Execute Runbook
===============

.. code:: python

    runbookID = '285f017e-bc97-4b03-a999-64e08065769e'
    
    runbookParamaters = {
         'f90e6468-31d3-4aa8-9d50-f8bf5bf689e2' : 'value',
         'edb8d27d-38ad-4d29-a255-30d8360a3852' : 'value',
         'b61abea1-4001-42fd-99b5-470acc5c1386' : 'value',
         '32725695-0b25-47e0-abbe-b28e22eca8ad' : 'value',
    }
    
    o.Execute(runbookID, runbookParamaters)
    
    
    


    
