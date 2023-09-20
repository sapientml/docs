======================
Training from a corpus
======================

------------------------------------
SapientML local training
------------------------------------

1. Execution Method
===================

Please refer to `this page <https://github.com/sapientml/docs/edit/main/docs/dev/setup.rst>`_ to finish the setup of development environment first.
We assume that at this point, **corpus** is downloaded and stored at the **sapientml_core** location, all the pipelines in the corpus is already clean using program slicing and there exists a label file such as *annotated-notebooks/annotated-notebooks-1140.csv* that has all the components for each pipeline. 

* After successfull setup, the following directory structure should reflect.

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

Create sample main.py
---------------------

* Create a driver code inside sapientml which runs each training step.
* We have to explicitly call the train method from the SapientMLGenerator class in order to train sapientml by considering datasets taken from corpus.

.. code-block:: python

    from sapientml_core.generator import SapientMLGenerator

    print("Training started")
    print("=================")
    cls = SapientMLGenerator()
    cls.train(<tag>, <num_parallelization>)
    print("=================")
    print("Training ended")

* By executing the above driver code, a folder **.cache** is created inside **sapientml_core** and output files from local training are stored here. 
* Argument **tag** is passed to each step to determine the cache folder name. For example, *./.cache/2.5.1-test* is created as the cache folder if *tag* is set as "2.5.1-test", then all artifacts of local training will be stored in that folder. Otherwise if **tag** is not set, all artifacts will be stored in **.cache**.
* Also the argument **num_parallelization** is used for parallellizing the execution process and its default value is 200.

2. Local training process overview 
====================================

* Step-1 : Denoise dataset
* Step-2 : Augment the corpus
* Step-3 : Extract meta-features
* Step-4 : Train the models
* Step-5 : Create dataflow model

3. Explanation of each process in local training
================================================

Step-1 : Denoise Dataset
------------------------

Step-1A : static_analysis_of_columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/denoising/static_analysis_of_columns.py* fetches all project list or pipeline details.
* Parse pipeline and fetch target, dropped, renamed column names.
* We use **libcst** library for parsing the column api details. 

.. note:: This script can traverse an Abstract Syntax Tree (AST) using the LibCST library and retrieve many useful information  such as column names, API names, strings, assignments, and so on.

Output : static_info.json
^^^^^^^^^^^^^^^^^^^^^^^^^

* It will create the directory *.cache/<tag>/static_info.json.*
* It gives informations about pre-processing components operations.

Example:

.. code-block:: json

        {
            "script0011.py": {
                "drop_api": [
                    "Age",
                    "Balance",
                    "CreditScore",
                    "EstimatedSalary",
                    "RowNumber",
                    "CustomerId",
                    "Surname",
                    "Tenure",
                    "HasCrCard"
                ],
                "rename_api": [],
                "target": "Exited"
            },
    
Step-1B : dataset_snapshot_extractor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/denoising/dataset_snapshot_extractor.py* fetches all project list or all pipeline details.
* Parse pipelines and instruments a given pipeline with code snippets to collect snapshots of dataset.
* We use **ast** library for parse and update the code.
* We use **machinery** library for the implementation of the import statement in updated pipeline.
* Execute the instrumented version of the pipeline to store the snapshot of the dataset after each line in the pipeline.

Output : dataset-snapshots
^^^^^^^^^^^^^^^^^^^^^^^^^^
* It will create the directory .cache/<tag>/dataset-snapshots/.
* A JSON file for each pipeline that stores the snapshot of column names of the dataframe after important statements in *.cache/<tag>/dataset-snapshots* as shown below.
* It is a dictionary that contains line number as a key and a list of column names as value.

Example:

    .. code-block:: json

        [
            {
                "4": [
                    [
                        "RowNumber",
                        "CustomerId",
                        "Surname",
                        "CreditScore",
                        "Geography",
                        "Gender",
                        "Age",
                        "Tenure",
                        "Balance",
                        "NumOfProducts",
                        "HasCrCard",
                        "IsActiveMember",
                        "EstimatedSalary",
                        "Exited"
                    ],
                    "data",
                    "<class 'pandas.core.frame.DataFrame'>"
                ]
            }
        ]

Step-1C : determine_used_features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/denoising/determine_used_features.py* takes the outputs of **static_info.json** and **dataset-snapshots** from Step-1A and Step-1B as input.
* Fetch summary for each pipeline from dataset_snapshot(json) created in step 1b.
* The summary consist of following information:
    * pipeline name
    * used_cols
    * unmapped_cols
    * new_cols
    * target
    * deleted
    * status

Output : feature_analysis_summary.json
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* It will create the JSON file *.cache/<tag>/feature_analysis_summary.json*
* It contains summary for all pipelines.

Example:

   .. code-block:: json

    {
     "script0011.py": {
        "pipeline": "script0011.py",
        "used_cols": [
            "EstimatedSalary",
            "Exited",
            "Age",
            "CreditScore",
            "NumOfProducts",
            "Gender",
            "Geography",
            "Balance",
            "IsActiveMember"
        ],
        "unmapped_cols": [],
        "new_cols": [],
        "target": "Exited",
        "deleted": [
            "Tenure",
            "Surname",
            "HasCrCard",
            "RowNumber",
            "CustomerId"
        ],
        "status": "FINALIZED"
    },


Step-2 : Corpus Augmentation
----------------------------

Step-2A : mutation_runner
^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/augmentation/mutation_runner.py* mutates each pipeline in the corpus, runs the mutated version, and store all the details in  *.cache/<tag>/exec_info* directory.
* In the first run, this step is expected to take a long time depending on the number of the pipelines in the corpus. From the subsequent runs, mutation is only run for the new notebooks, i.e., if the mutated results are not found locally for those notebooks.
* We use *ast* library for parsing and analyse the components in pipeline.
* It executes the mutated pipelines and store the results and logs.

Output: exec_info
^^^^^^^^^^^^^^^^^
* It will create the directory *.cache/<tag>/exec_info*
* It will contain the information of all the mutated pipeleines i.e., it replaces the model in the original pipeline with a pre-defined list of models(21 models).

Step-2B : mutation_results
^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/augmentation/mutation_results.py* combines all the results in a CSV file and selects the best model.
* It fetches the accuracy score of mutated corpus for all pipelines.
* And saves it in *.cache/{tag(if any)}/mutation_results.csv* file.

Output : mutation_results.csv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+--------------+------------+----------+---------+----------+-------------------+----------+---------------+-----+------------+----------------------------+-------+-----+-----+----------------+-------------+--------------+----------+------------+
|file_name     |random forest,| extra tree,| lightgbm,| xgboost,| catboost,| gradient boosting,| adaboost,| decision tree,| svm,| linear svm,| logistic/linear regression,| lasso,| sgd,| mlp,| multinomial nb,| gaussian nb,| bernoulli nb,| original,| best_models|
+==============+==============+============+==========+=========+==========+===================+==========+===============+=====+============+============================+=======+=====+=====+================+=============+==============+==========+============+
|script0011.py |0.8275        |0.8315      |0.858     |0.8555   |0.859     |0.86               |0.853     |0.825          |0.856|0.846       |0.85                        |0.0    |0.843|0.852|0.8435          |0.817        |0.813         |0.8555    |['gradient  |
|              |              |            |          |         |          |                   |          |               |     |            |                            |       |     |     |                |             |              |          |boosting']  |
+--------------+--------------+------------+----------+---------+----------+-------------------+----------+---------------+-----+------------+----------------------------+-------+-----+-----+----------------+-------------+--------------+----------+------------+

* From the above we can say that the gradient boosting model is the best model as it has greater accuracy than the rest of the models.

Step-3 : Extraction of Meta-Features and Pipeline Components
-------------------------------------------------------------

* *core/sapientml_core/training/meta_feature_extractor.py* extracts the meta-features for all the projects, In other words it fetches all the pipeline details. This will save all the meta-features at *.cache/<tag>/* in form of two CSV files:
    1. one for pre-processing components (pp_metafeatures_training.csv).
    2. another for the model components (model_metafeatures_training.csv).
* There are two modes of extracting meta-features. "clean" is active in default. This setting can be modified directly in the source code
    1. "as-is" 
    2. "clean"
* **as-is** computes meta-features based on all the meta-features in the dataset.
* **clean** mode only uses the meta-features that are used in the pipeline. Features which are already used in the pipeline are pre-computed and stored in the *.cache/<tag>/feature_analysis_summary.json file*.

Output : pp_metafeatures_training.csv, model_metafeatures_training.csv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Fetch meta features related to model and save to *.cache/<tag>/pp_metafeatures_training.csv*.
* Fetch meta features related to preprocess component and save to *.cache/<tag>/model_meta_features_trainer.csv*.

Step-4 : Training Meta-Models for Skeleton Predictor
----------------------------------------------------

Step-4A: Training of pre-processing components (pp_model_trainer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/pp_model_trainer.py* is in charge of training the meta-models for pre-processing components.
* It takes *.cache/<tag>/pp_metafeatures_training.csv* as input and trains a decision tree for each pre-processing component.

Output : pp_models.pkl
^^^^^^^^^^^^^^^^^^^^^^

* *.cache/<tag>/pp_models.pkl* is a machine learning model pickle file for selecting pre-processing components.

Step-4B: Training of Model components (meta_model_trainer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* *core/sapientml_core/training/meta_model_trainer.py* is in charge of training the meta-model that predicts and ranks the model components for the pipeline. Currently it is an ensemble model that uses **LogisticRegression** and **SVM** as the base classifiers and ranks the predicted model based on the average of their probability scores.

Output: mp_model_1.pkl, mp_model_2.pkl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *.cache/<tag>/mp_model_1.pkl* is a **LogisticRegression** model pickle file for selecting pre-processing components.
* *.cache/<tag>/mp_model_2.pkl* is a **svm** model pickle file for selecting pre-processing components.

Step-5 : Construct the Data Flow Model
--------------------------------------

Step-5A : dependent_api_extractor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/dataflowmodel/dependent_api_extractor.py* will get the API/labels that are dependent on each other. A label is dependent on each other when they are applied on the same column.
* It gets all the annotated pipelines in the corpus.
* It reads Annotated_notebook csv and store the labels with respect to filename and line number
* If same label exists take a count and store as a dictionary data in final_dependency_list i.e {'a b':1, 'c d':3, 'e f':2}
* It sorts the items and store all the list of dependent labels/APIs in dependent_labels.json file.

Output : dependent_labels.json
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* A JSON file stored in *.cache/<tag>/dependent_labels.json* containing the list of dependent APIs.

Example:

.. code-block:: json

    {
    "['PREPROCESS:Category:get_dummies:pandas', 'PREPROCESS:DeleteColumns:drop:pandas']": 79,
    "['PREPROCESS:ConvertStr2Date:to_datetime:pandas', 'PREPROCESS:DeleteColumns:drop:pandas']": 27,
    "['PREPROCESS:MissingValues:fillna:pandas', 'PREPROCESS:DeleteColumns:drop:pandas']": 16,
    "['PREPROCESS:Scaling:log:numpy', 'PREPROCESS:DeleteColumns:drop:pandas']": 12,
    }

* In the above sample json file. The first line shows that they call *get_dummies* preprocessor first and then *DeleteColumns* preprocessor next and this pair is dependent on each other.
* The number denotes the count of this dependent_labels executed as we have multiple pipelines.

Step-5B : determine_label_order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* *core/sapientml_core/training/dataflowmodel/determine_label_order.py* will determine the order of the components.
* If there is any order exists. It will extract the order of two APIs/labels A and B.
* There is an order between A --> B if A and B are dependent on each other based on 'dependent_api_extractor.py' and A is always followed by B in all piplelines and there is NO case in the corpus where B is followed by A.
* Based on the previous step output file *.cache/<tag>/dependent_labels.json*, An output json file *.cache/<tag>/label_orders.json* is created.

Output: label_orders.json
^^^^^^^^^^^^^^^^^^^^^^^^^

* A JSON file stored in *.cache/<tag>/label_orders.json* containing the order of labels in a pair-wise form.

Example:

.. code-block:: json

    [
    "PREPROCESS:MissingValues:fillna:pandas#PREPROCESS:GenerateColumn:groupby:pandas",
    "PREPROCESS:TypeChange:astype:pandas#PREPROCESS:MissingValues:fillna:pandas",
    "PREPROCESS:MissingValues:interpolate:sklearn#PREPROCESS:CONVERT_NUM2NUM:where:numpy",
    "PREPROCESS:TypeChange:astype:pandas#PREPROCESS:GenerateColumn:date:pandas",
    "PREPROCESS:MissingValues:fillna:pandas#PREPROCESS:TypeChange:astype:pandas",
    "PREPROCESS:MissingValues:fillna:pandas#PREPROCESS:Category:get_dummies:pandas",
    ]

4. How to use training output
=============================

* After **label_orders.json** is produced, it is copied into *core/sapientml_core/adaptation/artifacts/label_order.json* so that SapientML can use it. 
* Please note that the **dataflow model** is a very important artifact. So make sure that the updated **dataflow model** is correct before replacing the existing one.
* Generally, it should not be updated unless there is no new pre-processing components.

.. _corpus: https://github.com/sapientml/sapientml/files/12593737/sapientml-corpus-0.1.0.zip
.. _this page: https://github.com/sapientml/docs/edit/main/docs/dev/setup.rst