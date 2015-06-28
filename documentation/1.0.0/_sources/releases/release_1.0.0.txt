=============
Release 1.0.0
=============


.. release:: 1.0.0
   :date: 2015-08-9

   .. change:: new
      :tags: ui

      Added a PyQt based user interface for building rigs through nodes and connections

   .. change:: changed
      :tags: plugins, maya

      Maya plug-in now fully supported.

   .. change:: changed
      :tags: plugins, softimage

      Softimage plug-in now fully supported.

   .. change:: new
      :tags: kl

      New Kraken Solver KL extension implements the base inteface and object that all Kraken solvers will inherit. Kraken Arg also works hand in hand with this new object.

   .. change:: new
      :tags: core, synchronizer

      :doc:`/python/core/synchronizer` module allows synchronoization from DCC to the Python graph. This allows users to create guides, adjust them, then synch back to the graph to have those changes affect the final rig build.

      Also allows saving guides / graphs out as a preset file.

   .. change:: new
      :tags: core, kraken system

      :doc:`/python/core/kraken_system` module is a singleton object used to provide an interface with the FabricEngine Core and RTVal system.

   .. change:: new
      :tags: profiler

      :doc:`/python/core/profiler` object is for debugging performance issues during builds. Provides timing and labels.

   .. change:: new
      :tags: math

      :doc:`/python/core/maths/maths` library now wraps the KL math library to ensure there is a one to one mapping between the types and that the math evaluates exactly the same way.

   .. change:: new
      :tags: rig

      :doc:`/python/core/objects/rig` object is sub-classed from the *Container* object and is used to load and save out presets of full rigs. Provided additional methods for doing so.

   .. change:: changed
      :tags: control, config

      :doc:`/python/core/objects/control` object now takes a *shape* argument and shapes are stored in the config.

   .. change:: changed
      :tags: control, config

      :doc:`/python/core/configs/config` object now stores the valid colors, sides, mirror mapping, naming template, and control shapes. This object is a singleton and can be sub-classed to provide customized configurations per studio, per project, or even per asset.

   .. change:: changed
      :tags: object 3d, scene item

      Swapped names of Object 3D and Scene Item. Scene Item is now the base object for most simple objects without transforms.

   .. change:: changed
      :tags: srt buffer, ctrl space

      Renamed srt buffer to ctrl space to be more intuitively named.


.. include:: footer.rst