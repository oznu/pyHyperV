pyHyperV
========


.. image:: https://img.shields.io/pypi/v/pyHyperV.svg
        :target: https://pypi.python.org/pypi/pyHyperV/0.0.4

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
    
    orchestratorEndpoint = "http://hostname.local:81/Orchestrator2012/Orchestrator.svc"
    username = "domain\\username"
    password = "password"
    
    o = pyHyperV.orchestrator(orchestratorEndpoint, username, password)
    

===============
Execute Runbook
===============

.. code:: python

    pyHyperV.orchestrator.Execute(runbookID, runbookParameters, dictionary=False)


You can send the parameters to orchestrator using the parameter ID or the parameter name.

Using Parameter IDs
-------------------

Example of sending using the parameter ID:

.. code:: python

    runbookID = '285f017e-bc97-4b03-a999-64e08065769e'
    
    runbookParameters = {
         'f90e6468-31d3-4aa8-9d50-f8bf5bf689e2' : 'value',
         'edb8d27d-38ad-4d29-a255-30d8360a3852' : 'value',
         'b61abea1-4001-42fd-99b5-470acc5c1386' : 'value',
         '32725695-0b25-47e0-abbe-b28e22eca8ad' : 'value',
    }
    
    o.Execute(runbookID, runbookParameters)
    
Using Parameter Names
---------------------
    
To send a request using the parameter names indead of the IDs, add the **dictionary=True** flag. The parameter names must match the names for each parameter in orchestrator.

Example:

.. code:: python

    runbookID = '285f017e-bc97-4b03-a999-64e08065769e'
    
    runbookParameters = {
         'HDD'  : '50gb',
         'CPU'  : '2',
         'RAM'  : '2048',
         'OS'   : 'Server2012',
    }
    
    o.Execute(runbookID, runbookParameters, dictionary=True)
    
    
Response
--------

Successfully initiating a runbook execution will return a 201 status code, along with the orchestrator job ID. The job ID returned can be used to check the status of the job using the GetJobStatus function.

Example Response:

.. code:: python

    { 
    'status' : 201,
      'result': {
          'id'               : '3c87fd6c-69f5-41c9-bd55-ec2aa6ec7c64',
          'status'           : 'pending',
          'CreationTime'     : '2014-04-02T12:11:05.617',
          'LastModifiedTime' : '2014-04-02T12:19:08.963',
          }
    }
    
    
============
Get Runbooks
============

.. code:: python

    pyHyperV.orchestrator.GetRunbooks()
    pyHyperV.orchestrator.GetRunbookID(runbookName)
    
Returns a list of runbooks and their IDs from orchestrator.

Example:

.. code:: python
    
    o.GetRunbooks()
    
    { 
    'status' : 200,
    'result' : {
        'Runbook_1' : 'e5944fe0-b600-45d2-a872-0c256594e394'
        'Runbook_2' : 'fd6d6a4b-1e57-40a3-930a-f4eb56394d3f'
        'Runbook_3' : '31451e20-5829-4323-9661-603ff826c852'
        }
    }
    

It is also possible to return a single runbook ID by it's name:

.. code:: python

    o.GetRunbookID('Runbook_1')
    
    'e5944fe0-b600-45d2-a872-0c256594e394'
    
         


======================
Get Runbook Parameters
======================

.. code:: python

    pyHyperV.orchestrator.GetParameters(runbookID)
    
This function returns the parameter names and paramater IDs required by the runbook specified.

Example:

.. code:: python

    runbookID = '285f017e-bc97-4b03-a999-64e08065769e'
    
    o.GetParameters(runbookID)
    
Example Response:

.. code:: python

    { 
    'status' : 200,
      'result': {
          'HDD' : 'f90e6468-31d3-4aa8-9d50-f8bf5bf689e2',
          'CPU' : 'edb8d27d-38ad-4d29-a255-30d8360a3852',
          'RAM' : 'b61abea1-4001-42fd-99b5-470acc5c1386',
          'OS'  : '32725695-0b25-47e0-abbe-b28e22eca8ad',
          }
    }
    
    
==============
Get Job Status
==============

.. code:: python

    pyHyperV.orchestrator.GetJobStatus(jobID)
    
    
This function allows you to check the status of an orchestrator job/task.

Example:

.. code:: python

    jobID = '285f017e-bc97-4b03-a999-64e08065769e'
    
    o.GetParameters(jobID)

Example Response:

.. code:: python

    { 
    'status' : 200,
      'result': {
          'id'               : '3c87fd6c-69f5-41c9-bd55-ec2aa6ec7c64',
          'status'           : 'Complete',
          'CreationTime'     : '2014-04-02T12:11:05.617',
          'LastModifiedTime' : '2014-04-02T12:19:08.963',
          }
    }
    
===================
Get Job Instance ID
===================

.. code:: python

    pyHyperV.orchestrator.GetJobInstance(jobID)
    
Returns the job instance ID. This ID can then be used in other functions such as GetInstanceParameters.

Example:

.. code:: python

    jobID = '3c87fd6c-69f5-41c9-bd55-ec2aa6ec7c64'

    o.GetJobInstance(jobID)
    
    'f4ac97ed-495b-44ae-b547-64611b0d8075'
    

=======================
Get Instance Parameters
=======================

.. code:: python

    pyHyperV.orchestrator.GetInstanceParameters(instanceID)
    
    
Returns the instance parameters from orchestrator. This function can be used to get data returned from orchestrator.

Example:

.. code:: python

    instanceID = 'f4ac97ed-495b-44ae-b547-64611b0d8075'

    o.GetInstanceParameters(instanceID)
    
    {
    'status' : 200,
    'result' : {
        'HDD'   : '50gb',
        'CPU'   : '2',
        'RAM'   : '2048',
        'OS'    : 'Server2012',
        'VM_ID' : 'edb8d27d-38ad-4d29-a255-30d8360a3852',
        'VM_IP' : '127.0.0.1',
        }
    }
