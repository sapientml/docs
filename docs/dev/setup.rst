=====
Setup
=====

Creating a development environment in your host
===============================================

Python `>=3.10,<3.13` is required.

Clone `sapientml <https://github.com/sapientml/sapientml.git>`_ and `core <https://github.com/sapientml/core.git>`_.
If you need to modify `preprocess <https://github.com/sapientml/preprocess.git>`_ and `loaddata <https://github.com/sapientml/loaddata.git>`_, please clone them as well.

.. code-block:: bash

   mkdir AutoML
   cd AutoML
   git clone https://github.com/sapientml/sapientml.git
   git clone https://github.com/sapientml/core.git

   # optional
   git clone https://github.com/sapientml/preprocess.git
   git clone https://github.com/sapientml/loaddata.git

Setup an environment in the **sapientml** repository folder.

.. code-block:: bash

   cd /path/to/AutoML/sapientml
   python -m venv venv
   . venv/bin/activate
   pip install poetry
   poetry install
   pre-commit install
   pip install -e ../core

   # optional
   pip install -e ../preprocess
   pip install -e ../loaddata

For ubuntu, `poetry install` may fail. If so, try the following command:

.. code-block:: bash

   PYTHON_KEYRING_BACKEND="keyring.backends.null.Keyring" poetry install

As sapientml and core are interdependent. Use below command to integrate.

.. code-block:: bash

   pip install -e /path/to/AutoML/core
   deactivate

Now download `corpus <https://github.com/sapientml/docs/files/13290907/sapientml-corpus-0.1.1.zip>`_ inside **sapientml_core**.

.. code-block:: bash

   . venv/bin/activate
   cd /path/to/AutoML/core/sapientml_core
   pip install dvc
   wget https://github.com/sapientml/docs/files/13290907/sapientml-corpus-0.1.1.zip
   unzip sapientml-corpus-0.1.1.zip
   mv sapientml-corpus-0.1.1 corpus
   cd corpus
   bash ./scripts/pull.sh
   rm -f sapientml-corpus-0.1.1.zip
   deactivate

After successfull installation, the following directory structure should reflect.

.. code-block::
   
   AutoML/
   ├── core/
   │   ├── sapientml_core/
   │       ├── corpus/
   │       │   ├── clean-notebooks/
   │       │   ├── annotated-notebooks/
   │       │   └── dataset/
   │       ├── design/
   │       └── training/
   │  
   └── sapientml/
       └──sapientml/

.. _sapientml: https://github.com/sapientml/sapientml.git
.. _core: https://github.com/sapientml/core.git
.. _corpus: https://github.com/sapientml/docs/files/13290907/sapientml-corpus-0.1.1.zip
