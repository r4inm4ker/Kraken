============
Installation
============

.. contents::
   :local:
|

Download
********
Get the latest version of Kraken here:
`Kraken Downloads <http://fabric-engine.github.io/Kraken/#download>`_

|

Environment Variables
*********************
|

.. glossary::

   KRAKEN_DIR
      Base directory where Kraken is installed

   KRAKEN_COMPONENTS
      Root python paths to custom components
|

Example Launcher Scripts
************************
|

Windows Standalone
==================
|

.. highlight:: bash

::

   set FABRIC_DIR=D:\fabric\FabricEngine-1.15.2-Windows-x86_64

   set KRAKEN_PATH=D:\dev\kraken

   set PATH=%FABRIC_DIR%\bin;%PATH%

   set FABRIC_EXTS_PATH=%FABRIC_DIR%\Exts;%FABRIC_EXTS_PATH%;%KRAKEN_PATH%\KLExts;

   set PYTHONPATH=%PYTHONPATH%;%FABRIC_DIR%\Python\2.7;%KRAKEN_PATH%\Python;


   cd /d D:\dev\kraken\Python\kraken

   call cmd


Windows Softimage 2015
======================
|

.. highlight:: bash

::

   set FABRIC_DIR=D:\fabric\FabricEngine-1.15.2-Windows-x86_64

   set KRAKEN_PATH=D:\dev\kraken

   set PATH=%FABRIC_DIR%\bin;%PATH%

   set FABRIC_EXTS_PATH=%FABRIC_DIR%\Exts;%FABRIC_EXTS_PATH%;%KRAKEN_PATH%\KLExts;

   set PYTHONPATH=%PYTHONPATH%;%FABRIC_DIR%\Python\2.7;%KRAKEN_PATH%\Python;


   call "C:\Program Files\Autodesk\Softimage 2015 SP1\Application\bin\XSI.bat"

   echo OFF


Windows Maya 2015
=================
|

.. highlight:: bash

::

   set FABRIC_DIR=D:\fabric\FabricEngine-1.15.2-Windows-x86_64

   set KRAKEN_PATH=D:\dev\kraken

   set PATH=%FABRIC_DIR%\bin;%PATH%

   set FABRIC_EXTS_PATH=%FABRIC_DIR%\Exts;%FABRIC_EXTS_PATH%;%KRAKEN_PATH%\KLExts;

   set PYTHONPATH=%PYTHONPATH%;%FABRIC_DIR%\Python\2.7;%KRAKEN_PATH%\Python;


   set MAYA_MODULE_PATH=%FABRIC_DIR%\SpliceIntegrations\FabricSpliceMaya2015SP2;%KRAKEN_PATH%\DCCIntegrations\maya;

   start /d "C:\Program Files\Autodesk\Maya2015\bin" maya.exe


.. include:: footer.rst