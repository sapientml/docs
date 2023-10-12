=====
Setup
=====

Creating a development environment in your host
===============================================

Python `>=3.10,<3.11` is required.

.. code-block:: bash

   $ python -V
   Python 3.10.4

Clone `sapientml <https://github.com/sapientml/sapientml.git>`_ and `core <https://github.com/sapientml/core.git>`_ now.

.. code-block:: bash

   mkdir AutoML
   cd AutoML
   git clone https://github.com/sapientml/sapientml.git
   git clone https://github.com/sapientml/core.git

Setup an environment in the **sapientml** repository folder.

.. code-block:: bash

   cd /path/to/AutoML/sapientml
   python3.10 -m venv venv
   . venv/bin/activate
   pip install poetry
   poetry install
   pre-commit install

As sapientml and core are interdependent. Use below command to integrate.

.. code-block:: bash

   pip install -e /path/to/AutoML/core
   deactivate

Now download `corpus <https://github.com/sapientml/sapientml/files/12593737/sapientml-corpus-0.1.0.zip>`_ inside **sapientml_core**.

.. code-block:: bash

   . venv/bin/activate
   cd /path/to/AutoML/core/sapientml_core
   pip install dvc
   wget https://github.com/sapientml/sapientml/files/12593737/sapientml-corpus-0.1.0.zip
   unzip sapientml-corpus-0.1.0.zip
   mv sapientml-corpus-0.1.0 corpus
   cd corpus
   bash ./scripts/pull.sh
   rm -f sapientml-corpus-0.1.0.zip
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
   │       ├── design
   │       └── training
   │  
   └── sapientml/
       └──sapientml/

.. _sapientml: https://github.com/sapientml/sapientml.git
.. _core: https://github.com/sapientml/core.git
.. _corpus: https://github.com/sapientml/sapientml/files/12593737/sapientml-corpus-0.1.0.zip
