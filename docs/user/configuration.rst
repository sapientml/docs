=============
Configuration
=============

The constructor of :code:`SapientML` class consumes various parameters depending on plugin installation.
Here we show the parameters you can assign at the constructor of :code:`SapientML` in cases of each :code:`model_type` assigned.

Model types
===========

**sapientml** provides the plugin mechanism for generating source code that is different from the original algorithm of **sapientml** in utilizing machine learning models and preprocessing components.
Each plugin has a unique :code:`model_type`, and users can choose one of them as a parameter of the constructor of :code:`SapientML` class.
The default value of :code:`model_type` is :code:`sapientml`, which is provided by **sapientml_core** plugin.

Parameters for :code:`sapientml`
--------------------------------

target_columns (list[str])
    Names of target columns.
task_type (classification', 'regression', or None) = None
    Identifies the task type from classification or regression, or automatically suggests it if set to :code:`None`
adaptation_metric (str) = 'f1' if task_type is 'classification', 'r2' if 'regression'
    Metric for evaluation. :code:`f1`, :code:`auc`, :code:`ROC_AUC`, :code:`accuracy`, :code:`Gini`, :code:`LogLoss`, :code:`MCC` (Matthews correlation coefficient), :code:`QWK` (Quadratic weighted kappa) are available for classification. :code:`r2`, :code:`RMSLE`, :code:`RMSE`, :code:`MAE` are available for regression.
split_method ('random', 'time', or 'group') = 'random'
    Method of train-test split. :code:`random` uses random split. :code:`time` requires :code:`split_column_name`. This sorts the data rows based on the column, and then splits data. :code:`group` requires :code:`split_column_name`. This splits the data so that rows with the same value of :code:`split_column_name` are not placed in both training and test data.
split_seed (int) = 17
    Random seed for train-test split. Ignored when :code:`split_method='time'`.
split_train_size (float) = 0.75
    The ratio of training size to input data. Ignored when :code:`split_method='time'`.
split_column_name (str or None) = None
    Name of the column used to split. Ignored when :code:`split_method='random'`
time_split_num (int) = 5
    Passed to :code:`n_splits` of :code:`TimeSeriesSplit`. Valid only when :code:`split_method='time'`.
time_split_index (int) = 4
    The index of the split from :code:`TimeSeriesSplit`. Valid only when :code:`split_method='time'`.
split_stratification (bool or None) = None
    To perform stratification in train-test split. Valid only when :code:`task_type='classification'`.
initial_timeout (int) = 600
    Timelimit to execute each generated script.
    Ignored when :code:`hyperparameter_tuning=True` and :code:`hyperparameter_tuning_timeout` is set.
timeout_for_test (int) = 0
    Timelimit to execute test script (final_script) and Visualization.
cancel (CancellationToken or None) = None
    Object to interrupt evaluations.
project_name (str or None) = None
    Project name.
debug (bool) = False
    Debug mode or not.
use_pos_list (list[str]) = ["名詞", "動詞", "助動詞", "形容詞", "副詞"]
    List of parts-of-speech to be used during text analysis.
    This variable is used for japanese texts analysis.
    Select the part of speech below.
    "名詞", "動詞", "形容詞", "形容動詞", "副詞".
use_word_stemming (bool) = True
    Specify whether or not word stemming is used.
    This variable is used for japanese texts analysis.
n_models (int) = 3
    Number of output models to be tried.
seed_for_model (int) = 42
    Random seed for models such as :code:`RandomForestClassifier`.
id_columns_for_prediction (list[str] or None) = None
    Name of the dataframe columns that outputs the prediction result.
use_word_list (list[str], dict[str, list[str]], or None) = None
    List of words to be used as features when generating explanatory variables from text.
    If dict type is specified, key must be a column name and value must be a list of words.
hyperparameter_tuning (bool) = False
    On/Off of hyperparameter tuning.
hyperparameter_tuning_n_trials (int) = 10
    The number of trials of hyperparameter tuning.
hyperparameter_tuning_timeout (int) = 0
    Time limit for hyperparameter tuning in each generated script.
    Ignored when :code:`hyperparameter_tuning` is :code:`False`.
hyperparameter_tuning_random_state (int) = 1023
    Random seed for hyperparameter tuning.
predict_option ('default' or 'probability') = 'default'
    Specify predict method (default: :code:`predict()`, probability: :code:`predict_proba()`.)
permutation_importance (bool) = True
    On/Off of outputting permutation importance calculation code.
add_explanation (bool) = False
    If :code:`True`, outputs ipynb files including EDA and explanation.
