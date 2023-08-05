Install and run
---------------

- Installing from `pip <https://pypi.org/project/pyRingGW/1.0.0/)>`_:
   
   .. code-block:: bash

      $ pip install pyRingGW
   
- Installing the `source code <https://git.ligo.org/lscsoft/pyring>`_:
   
   In your ``~/.bashrc`` add:  

   .. code-block:: bash

      $ export PYRING_PREFIX=/home/installation_directory/pyring  

   where ``installation_directory`` is the directory where you will be placing the ``pyRing`` source code. This path is needed for advanced functionalities such as QNM interpolation or injection of NR data.

   .. code-block:: bash

         $ git clone git@git.ligo.org:cbc-testinggr/pyring.git  
         $ cd pyring
         $ git lfs install 
         $ git lfs pull  
         $ pip install -r requirements.txt
         $ python setup.py install  
   
   Add ``--user`` to the last command in case you don't have administrator's permissions (for example if you are installing on a cluster).    
   Alternatives to the last command are ``python -m pip install .`` or ``pip install .``  

- Running the code:

   The one-liner you are searching for is:
   
   .. code-block:: bash
   
      $ pyRing --config-file config.ini


- Examples:

   The ``config_files`` directory contains a variety of example files to analyse GW detections and injections (both ringdown templates and IMR injections). There is one example file for each waveform model supported, included all modifications to the Kerr hypothesis.
   
   A fast example to get you up to speed is:
   
   .. code-block:: bash
     
      $ pyRing --config-file repo/config_files/config_gw150914_local_data.ini

   And in ~20 minutes you should be able to roughly reproduce the GW150914 ringodwn measurement on a laptop.
   
   A configuration file for the same run using production settings (hence obtaining publication-level results) is:

   .. code-block:: bash
   
      $ pyRing --config-file repo/config_files/config_gw150914_production.ini
   
   Never forget that the sampler settings may need adjustment based on the problem you want to tackle.
   See the `Usage` section for further discussion.

   The configuration files directory can either be found on the source code `repository <https://git.ligo.org/lscsoft/pyring/-/tree/master/pyRing/config_files)>`_ or under the path ``installation_path/pyRing/config_files``. 
   To discover your ``installation_path``, type on the terminal:

   .. code-block:: bash
   
      $ import pyRing
      $ pyRing.__file__

   that will output the path under which the package was built.

- Explore:

   The software supports a variety of analysis and injection options, all of which can be explored by running:

   .. code-block:: bash

      $ pyRing --help 

- Requirements:
 
   The software requires ``python==3.7`` or ``python>=3.9`` (``cpnest`` has an incompatibility with ``python==3.8``).
