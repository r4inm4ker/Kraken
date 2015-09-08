##############
User Interface
##############

Kraken comes with a nodal inteface that allows for quickly prototyping rigs and re-using the configuration at a later time.

.. contents:: Table of Contents
   :local:

|

.. image:: /images/Kraken_UI.jpg

|

Menu Bar (1)
============
The menu bar provides items to easily interact with the graph.

File Menu
---------
|

New
   Creates a new graph flushing the current one.

Save
   Saves the current graph to a ``*.krg`` file at the specified location.

Load
   Load a ``*.krg`` file into the graph as a new graph. The current graph will be cleared.

Close
   Closes the UI and asks to save the current rig.

|

Edit Menu
---------
|

Copy
   Copies the selected nodes in the graph.

Paste
   Pastes a copy of the components.

Paste Connected
   Pastes a copy of the components and keeps connections.

Paste Mirrored
   Pastes a mirroried copy of the components.

Paste Mirrored Connected
   Pastes a mirroried copy of the components and keeps connections.

Rig Name
   Allows you to edit the rig name via a modal input box.

|

Build Menu
----------
|

Build Guide
   Builds the guide for the current graph. Each component will have it's guide structure built. From there you can manipulate the guide to match the proportions of your character.

Build Rig
   This builds the rig for the current graph. If you do not have a guide already built in your scene, it will use the default values in each component to build the rig.

   If you do have a guide in your scene it will synchronize the values from the scene back into the graph before building.

|

Panels Menu
-----------
|

Component Library
   Toggles the component library to be visible.

|

Help Menu
---------
|

Online Help
   Opens a browser page to the Kraken web page.

|

Config Drop Down (2)
====================
The config drop down allows the user to specify a configuration to use while building. Configurations allow you to customize naming, colors, and more.

.. seealso:: :doc:`/python/core/configs/config`

|

Rig Name (3)
============
The rig name widget allows you to quickly change the name of the rig that you're currently working in. Double clicking on the widget displays an input box to change the name.

|

Component Library (4)
=====================
The component library is a list of registered components that you can instance into the graph. Using the ``KRAKEN_COMPONENTS`` environment variable will allow you to register your custom components.

.. seealso:: :doc:`installation` for information on how to add custom components.

|

Contextual Node list (5)
========================
The contextual node list reflects the component library but is a floating widget that allows you to type in the name of the component you want and create it without having the component library visible. Type the name select from the list and hit enter.

|

Nodes & Graph (6)
=================
The graph is where you instance components as nodes and create connections. You can only make connections between component ports which are of the same type. Only Vec3's will connect to Vec3 ports for example. You can click and drag from a label or port to another port to connect it.

|


Keyboard Commands
=================
|

============ =========
Key Combo    Function
============ =========
Ctrl+N       New Graph (Clears current graph)
Ctrl+S       Save Graph
Ctrl+L       Load Graph (Clears current graph)
Ctrl+W       Closes the Interface
Ctrl+C       Copy Selected Nodes
Ctrl+V       Paste Copied Nodes
Ctrl+Shift+V Paste Copied Nodes with connections
Ctrl+G       Builds the Guide Rig
Ctrl+B       Builds the Rig
Ctrl+H       Opens the Kraken Page
Ctrl+Tab     Toggles the Component Library
` (Tilde)    Opens the contextual node list over the graph
============ =========



.. include:: footer.rst