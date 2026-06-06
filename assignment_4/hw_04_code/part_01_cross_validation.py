
"""
# ===============================================
#  Created by: Kenny Davila Castellanos
#              for CSC 480
#
#  MODIFIED BY: [Your NAME]
# ===============================================
"""

import sys
import time

import numpy as np
import pickle

from auxiliary_functions import *

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from helper_classes import SubMetrics, Metrics, GlobalInputs, BothMetrics


# =======================================================================
#    This is an optional function that you can use to print your metrics
#    in a format that makes it easier to tabulate
#
#    This one is up to you. It won't be evaluated!
# =======================================================================
def custom_metric_print(metrics_dict):
    pass


# =======================================================================================================
# wh
#     {
#         "train": sub_metrics_dict,
#         "validation": sub_metrics_dict
#     }
#
#   Where each sub_metrics_dict follows this format:
#     {
#           "class 1 name": group_metrics,
#           "class 2 name": group_metrics,
#              ...
#           "class N name": group_metrics,
#           "accuracy": [AVG accuracy value],
#           "macro avg": group_metrics,
#           "weighted avg": group_metrics
#     }
#
#   Where each group_metrics follows this format:
#     {
#           "precision": [AVG value for this metric],
#           "recall":    [AVG value for this metric],
#           "f1-score":  [AVG value for this metric],
#           "support":   [SUM value for this metric]
#     }
#
#   Note that this is a modified of the dictionary returned by classification_report
# =======================================================================================================
def cross_validation(raw_x: np.ndarray, raw_y: np.ndarray, n_folds: int, classifier_name: str, hyper_params: Dict) -> BothMetrics:
    # DONE: 1) split the dataset ....
    x_y_chunk_pairs = split_dataset(raw_x, raw_y, n_folds)
    # TODO: 2) for each split ...
    total_training_metrics = []
    total_validation_metrics = []
    total_train_time = 0.0
    total_validate_time = 0.0
    for i, current_validation_chunk in enumerate(x_y_chunk_pairs):
        current_train_chunks = x_y_chunk_pairs[:i] + x_y_chunk_pairs[i + 1:]

        concatenate_x = []
        concatenate_y = []
        # 2.1) prepare the split training dataset (concatenate and normalize)
        for current_test_chunk in current_train_chunks:
            # put training chunks together
            concatenate_x.append(current_test_chunk[0])
            concatenate_y.append(current_test_chunk[1])

        current_training_y = np.concatenate(concatenate_y)
        current_training_x, training_scaler = apply_normalization(np.concatenate(concatenate_x), None)

        #  2.2) prepare the split validation dataset (normalize)
        current_validation_y = current_validation_chunk[1]
        current_validation_x, validation_scaler = apply_normalization(current_validation_chunk[0], None)


        #  2.3) train your classifier on the training split
        start = time.time()
        current_trained_classifier = train_classifier(classifier_name, hyper_params, current_training_x, current_training_y)
        total_train_time += time.time() - start
        #  2.4) evaluate your classifier on the training split (compute and print metrics)
        training_predictions = current_trained_classifier.predict(current_training_x)

        # 2.5) evaluate your classifier on the validationx split (compute and print metrics)
        start = time.time()
        validation_predictions =  current_trained_classifier.predict(current_validation_x)
        total_validate_time += time.time() - start

        #  2.6) collect your metrics
        current_training_metrics = classification_report(current_training_y, training_predictions, output_dict=True)
        total_training_metrics.append(current_training_metrics)
        # add time it too for this train chunks to train

        current_validation_metrics = classification_report(current_validation_y, validation_predictions, output_dict=True)
        total_validation_metrics.append(current_validation_metrics)
        # add time it too for this test chunk to validate


    # TODO: 3) compute the averaged metrics
    # 5.1) compute and print training metrics
    training_final_metrics = total_metrics(total_training_metrics, total_train_time)

    #  5.2) compute and print validation metrics
    validation_final_metrics = total_metrics(total_validation_metrics, total_validate_time)

    results = BothMetrics(training_final_metrics, validation_final_metrics)

    print(json.dumps(results.to_dict(), indent=4))
    return results


def total_metrics(metrics, time_to_run):

    total_accuracy = 0
    java_metrics = SubMetrics()
    python_metrics = SubMetrics()
    macro_avg_metrics = SubMetrics()
    weighted_avg_metrics = SubMetrics()

    for metric in metrics:
        # java
        java_metrics.precision += metric['0']['precision']
        java_metrics.recall += metric['0']['recall']
        java_metrics.f1 += metric['0']['f1-score']
        java_metrics.support += metric['0']['support']

        # python
        python_metrics.precision += metric['1']['precision']
        python_metrics.recall += metric['1']['recall']
        python_metrics.f1 += metric['1']['f1-score']
        python_metrics.support += metric['1']['support']

        total_accuracy += metric['accuracy']

        # macro_avg
        macro_avg_metrics.precision += metric['macro avg']['precision']
        macro_avg_metrics.recall += metric['macro avg']['recall']
        macro_avg_metrics.f1 += metric['macro avg']['f1-score']
        macro_avg_metrics.support += metric['macro avg']['support']

       # weighted_avg
        weighted_avg_metrics.precision += metric['weighted avg']['precision']
        weighted_avg_metrics.recall += metric['weighted avg']['recall']
        weighted_avg_metrics.f1 += metric['weighted avg']['f1-score']
        weighted_avg_metrics.support += metric['weighted avg']['support']


    final_metrics = Metrics(java_metrics, python_metrics, total_accuracy, macro_avg_metrics, weighted_avg_metrics, time_to_run)
    final_metrics.average(len(metrics))
    return final_metrics




def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print(f"\tpython {sys.argv[0]} in_config in_raw_data n_folds")
        return

    in_config_filename =  sys.argv[1]
    in_raw_data_filename =  sys.argv[2]
    try:
        n_folds =  int(sys.argv[3])
        if n_folds < 2:
            print("Invalid value for n_folds. Must be an integer >= 2")
            return
    except:
        print("invalid value for n_folds. Must be an integer >= 2")
        return

    # DONE: 1) Load your (cross-validation) hyper-parameters
    (classifier_name, class_config) = load_hyperparameters(in_config_filename, "cross_validation" )

    # DONE: 2) Load your data
    X, Y = load_raw_dataset(in_raw_data_filename)

    # DONE: 3) Run cross-validation
    result = cross_validation(X, Y, n_folds, classifier_name, class_config)
    # custom_metric_print(result)
    # FINISHED!


if __name__ == "__main__":
    main()
