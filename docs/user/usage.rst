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

    sml.fit(train_data)
    y_pred = sml.predict(test_data)

    print(f"F1 score: {f1_score(y_true, y_pred)}")

