=====
Usage
=====

**sapientml** generates source code to train and predict a machine learning model from a CSV-formatted dataset and requirements of a machine learning task to be solved.

SapientML class
===============

**sapientml** provides :code:`SapientML` class that provides the top level API of SapientML. In the constructor of :code:`SapientML`, you firstly need to set :code:`target_columns` as a requirement of the task. :code:`target_columns` specifies which the task is to predict. Second, you can set :code:`task_type` from :code:`classification` or :code:`regression` as a type of machine learning task. You can also skip setting :code:`task_type` and in that case SapientML automatially suggests task type by looking into values of the target columns.

.. code-block:: python

    from sapientml import SapientML

    cls = SapientML(
        target_columns=["survived"],
        task_type=None, # suggested automatically from the target columns
    )

As well as model classes of the other well-known libraries like **scikit-learn**, :code:`SapientML` provides :code:`fit` and :code:`predict` to conduct model training and prediction by using generated code.

.. code-block:: python

    import pandas as pd
    from sklearn.metrics import f1_score
    from sklearn.model_selection import train_test_split

    train_data = pd.read_csv("https://github.com/sapientml/sapientml/files/12481088/titanic.csv")
    train_data, test_data = train_test_split(train_data)
    y_true = test_data["survived"].reset_index(drop=True)
    test_data.drop(["survived"], axis=1, inplace=True)

    cls.fit(train_data, output_dir="./outputs")
    y_pred = cls.predict(test_data)

    print(f"F1 score: {f1_score(y_true, y_pred)}")

Generated source code
=====================

After calling `fit`, you can get generated source code at :code:`./outputs` folder. Here is the example of files generated by :code:`fit`:

.. parsed-literal::

    outputs
    ├── 1_script.py
    ├── 2_script.py
    ├── 3_script.py
    ├── final_predict.py
    ├── final_script.out.json
    ├── final_script.py
    ├── final_train.py
    └── lib
        └── sample_dataset.py

:code:`1_script.py`, :code:`2_script.py`, and :code:`3_script.py` are scripts of the hold-out validation using the preprocessors and the top-3 most plausible models.
:code:`final_script.py` is the script that selects the model actually achieved the highest score of the top-3 models, and :code:`final_script.out.json` contains its score. 
:code:`final_train.py` is the script for training the selected model, and :code:`final_predict.py` is the the script for prediction using the model trained by :code:`final_train.py`.
:code:`lib` folder contains modules that the above scripts uses.

Using generated code as a model
===============================

After calling :code:`fit`, you can also get :code:`cls.model`, which is a :code:`GeneratedModel` instance that contains generated source code and :code:`.pkl` files of preprocessers and a actual machine learning model. The instance also asts a usual model providing :code:`fit` and :code:`predict`.

.. code-block:: python

    cls.fit(train_data)
    model = cls.model # obtains GeneratedModel instance

You can get the set of source code and :code:`.pkl` files by referring :code:`model.files` or by looking into :code:`./outputs` folder after calling :code:`model.save("./model")`. Here is the example of files contained in :code:`GeneratedModel`:

.. parsed-literal::

    model
    ├── final_predict.py
    ├── final_train.py
    ├── lib
    │   └── sample_dataset.py
    ├── model.pkl
    ├── ordinalEncoder.pkl
    ├── simpleimputer-numeric.pkl
    └── simpleimputer-string.pkl

The actual behavior of :code:`model.fit` is a subprocess executing :code:`final_train.py`.
Beware that :code:`model.fit(another_train_data)` is not retraining the existing model but buiding a new one. 
:code:`model.predict` creates a subprocess executing :code:`final_predict.py` as well.

:code:`SapientML` provides a utility function to restore the :code:`SapientML` instance from generated model.

.. code-block:: python

    import pickle
    
    cls.fit(train_data)
    with open("model.pkl", "wb") as f:
        pickle.dump(sml.model, f)
    
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    sml = SapientML.from_pretrained(model)
