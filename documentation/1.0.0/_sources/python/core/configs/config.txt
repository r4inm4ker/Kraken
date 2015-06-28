Configs
*******

Kraken has a concept of configuration files that allow you to control how things
are named, colored, control shapes, and more.

You can create custom config files by sub-classing the core Config class and
redefining the methods within. This makes it easy to configure the builds per
studios, per project or even per character if desired.



.. seealso::

    :py:class:`kraken.core.builder`


.. contents:: Usage Documentation
   :local:


Custom Config Example
=====================

.. code-block:: python
   :linenos:

   # test_config.py

   from kraken.core.configs.config import Config


   class TestConfig(Config):

       def __init__(self):
           super(Config, self).__init__()

       # ======================
       # Color Mapping Methods
       # ======================
       def initColorMap(self):

           # This maps different colors for the locations compared to the
           # default ones.
           colorMap = {
                       "Control": {
                                   "default": "yellow",
                                   "L": "blue",
                                   "M": "orange",
                                   "R": "green"
                                  }
                      }

           return colorMap


.. note::

    When you import your custom config class and use the ''getInstance()'' method
    before the builder, the builder will use your config instead of the built in
    one.

    The config is cleared from the system after each build.


Using A Custom Config
=====================

.. code-block:: python
   :linenos:

   from kraken import plugins
   from kraken_examples.arm_component import ArmComponentGuide, ArmComponentRig

   from test_config import TestConfig

   config = TestConfig.getInstance()

   arm = ArmComponentRig()
   arm.loadData(armGuideData)

   builder = plugins.getBuilder()
   builder.build(arm)


Class Documentation
===================

.. autoclass:: kraken.core.configs.config.Config
    :members:
    :private-members:
    :special-members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: _Config__instance, __dict__, __module__, __weakref__


.. include:: ../../../footer.rst