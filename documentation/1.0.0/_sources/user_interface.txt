==============
User Interface
==============

Kraken comes with a nodal inteface that allows for quickly prototyping rigs and re-using the configuration at a later time.

.. image:: /images/Kraken_UI.jpg


UI Sections
***********

Component Library
=================
The component library is a list of registered components that you can instance into the graph. Using the ``KRAKEN_COMPONENTS`` environment variable will allow you to register your custom components.
|

Contextual Node list
====================
The contextual node list reflects the component library but is a floating widget that allows you to type in the name of the component you want and create it without having the component library visible. Type the name select from the list and hit enter.
|

Graph
=====
The graph is where you instance components as nodes and create connections. You can only make connections between component ports which are of the same type. Only Vec3's will connect to Vec3 ports for example. You can click and drag from a label or port to another port to connect it.
|

Graph Toolbar
=============
The graph toolbar is where you can interact with the current graph.

New
   Creates a new graph flushing the current one.

Save
   Saves the current graph to a ``*.krig`` file at the specified location.

Load
   Load a ``*.krig`` file into the graph as a new graph. The current graph will be cleared.

Rig Name
   The name of the rig you are going to build. This will be the name that you will see on the top container node and layers.

Build Guide
   Builds the guide for the current graph. Each component will have it's guide structure built. From there you can manipulate the guide to match the proportions of your character.

Build Rig
   This builds the rig for the current graph. If you do not have a guide already built in your scene, it will use the default values in each component to build the rig.

   If you do have a guide in your scene it will synchronize the values from the scene back into the graph before building.

|

Keyboard Commands
*****************
|

============ =========
Key Combo    Function
============ =========
Ctrl+N       New Graph (Clears current graph)
Ctrl+W       Closes the Interface
` (Tilde)    Opens the contextual node list over the graph
Ctrl+Tab     Toggles the Component Library
Ctrl+C       Copy Selected Nodes
Ctrl+V       Paste Copied Nodes
Ctrl+Shift+V Paste Copied Nodes with connections
============ =========



.. include:: footer.rst