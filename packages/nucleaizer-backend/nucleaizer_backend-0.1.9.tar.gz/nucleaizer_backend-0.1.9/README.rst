==================
nucleaizer-backend
==================


.. image:: https://img.shields.io/pypi/v/nucleaizer_backend.svg
        :target: https://pypi.python.org/pypi/nucleaizer_backend

.. image:: https://img.shields.io/travis/etasnadi/nucleaizer_backend.svg
        :target: https://travis-ci.com/etasnadi/nucleaizer_backend

.. image:: https://readthedocs.org/projects/nucleaizer-backend/badge/?version=latest
        :target: https://nucleaizer-backend.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Use in headless mode
-------------------------

* Install MATLAB Runtime v99.
* If ready, do not forget to set the ``LD_LIBRARY_PATH``: the install prints out. OR set the ``MATLAB_RUNTIME_PATHS`` variable: e.g.::

        MATLAB_RUNTIME=/MATLAB/MATLAB_Runtime
        export MATLAB_RUNTIME_PATHS=$MATLAB_RUNTIME/v99/runtime/glnxa64:$MATLAB_RUNTIME/v99/bin/glnxa64:$MATLAB_RUNTIME/v99/sys/os/glnxa64:$MATLAB_RUNTIME/v99/extern/bin/glnxa64

* Install the stuff locally in a virtual environment::

        python -m venv venv
        source venv/bin/activate (or .\Scripts\activate or something on Win)
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        python -m pip install -e .

* If the install is readly, then one should create the ``nucleaizer_backend/cli_config.py`` file and setup the config values needed:

  - ``nucleaizer_dir``: the directory where the models (.h5) files, configs, etc are staying. Prepare this dir first. Example: ``.nucleaizer_data_example`` in the shared distribution.
  - ``workflow_dir``: a directory where the pipeline puts the intermediate results. May be empty or a result of a previous run.
  - ``inputs_dir``: the input should go here with the subdirs ``train``, ``val``, ``test``. Consult the ``training.py`` for the details. Example: ``nucleaizer_dataset`` in the shared distribution.

* Then, call the entry point: ``python -m nucleaizer_backend.run_cli``. See the corresponding script for the details.

* Free software: MIT license
* Documentation: https://nucleaizer-backend.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
