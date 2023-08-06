"""Settings file for Classifier"""
from sklearn.cluster import KMeans, MiniBatchKMeans
from classifier.models import RandomForest, XGBoost, SingleClass

WORKSPACE = '/workspace/'

RASTER_EXTENSIONS = frozenset(['.tif', '.vrt', '.jp2'])

US_ALGORITHMS = ['us_kmeans', 'us_kmeans_minibatch']

# ##----THE ALGORITHMS---###
ALGORITHMS = ["randomforest",
              "xgboost",
              "singleclass",
              "us_kmeans",
              "us_kmeans_minibatch"
             ]
CLASSIFIERS = [
    RandomForest,
    XGBoost,
    SingleClass,
    KMeans,
    MiniBatchKMeans
    ]
ALGORITHM_DICT = dict(zip(ALGORITHMS, CLASSIFIERS))

PARAMETERS = {
    'app_algorithm': 'randomforest',
    # randomforest, xgboost, singleclass,us_kmeans
    'app_window': 1024,  # Any int, preferably within 2^x
    'app_model': None, # Model File location
    'app_samples': None,  # Samples file location (csv)
    'app_log_level': 'INFO',  # Logging level
    'app_threads': -1,  # #of threads
    'app_imputation': False,  # Use simple imputation for missing values
    'app_imputation_strategy': 'mean',  # Strategy for imputation. mean,
    'app_rasters_are_timeseries': False,  # Whether or not the input rasters
    # are TS
    # median, most_frequent, constant or randomforest
    'app_imputation_constant': -9999,  # imputation constant
    'su_probability': False,  # Output Probability Map
    'su_all_probabilities': False,
    'su_optimize': False,  # Optimize the model parameters
    'su_optimize_number': 10,  # Number of iterations for optimization
    'su_search_max_features': ['auto', 'sqrt', 'log2'],
    'su_search_max_leaf_nodes': [3, 5, 7],
    'su_search_max_depth': [None, 1, 3, 10, 20000],
    'su_search_n_estimators': [10, 50, 100],
    'su_single_class_treshold': 0,  # Treshold to use for single class
    'su_boxplots': False,  # Plot Boxplots for samples
    'su_remove_outliers': True,  # Remove outliers from the training data
    'su_rf_tree_depth': None,  # Depth of the trees in RF model.
    'us_nclasses': 2,  # Number of classes for unsupervised
    'us_trainfraction': 1.0,  # Fraction of raster used for training
    'acc_perform_assesment': True,  # Perform accuracy assessment
    'acc_testfraction': 0.25,  # Fraction of data to use for training
    'model_save': False,  # Save a model file which can be re-used
}
