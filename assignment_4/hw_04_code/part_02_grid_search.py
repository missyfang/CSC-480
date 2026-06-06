
"""
# ===============================================
#  Created by: Kenny Davila Castellanos
#              for CSC 480
#
#  MODIFIED BY: [Your NAME]
# ===============================================
"""
import csv
import sys
import itertools
from logging import config

from auxiliary_functions import *
from helper_classes import GlobalInputs
from part_01_cross_validation import cross_validation, custom_metric_print

def main_all():
    # create CSV header
    with open("grid_search_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "config_1", "config_2", "train_accuracy", "val_accuracy",
                         "avg_recall", "avg_precision", "avg_f1", "train_time", "val_time"])

    n_folds = 4
    in_config_filename = "hyperparameters.json"
    # DONE: 1) Load your (cross-validation) hyper-parameters
    (classifier_name, class_config) = load_hyperparameters(in_config_filename, "grid_search")

    for file_name in GlobalInputs.all_datasets:
        # DONE: 2) Load your data
        X, Y = load_raw_dataset(file_name)

        # DONE: 3) generate a combination of parameters (check itertools.product)
        #          https://docs.python.org/3/library/itertools.html#itertools.product
        keys, combos = create_combinations(class_config)

        # DONE: 4) Use the combinations of parameters to run a grid search
        #       For each combination of parameters
        total_results_by_combo = run_all_combinations(combos, keys, X, Y, n_folds, classifier_name)


        # DONE: 4) print the best parameters found (based on highest validation macro f-1 score)
       # determine_and_print_best_config_for_file(total_results_by_combo)
        for_csv(file_name, total_results_by_combo)



    #
    #custom_metric_print(result)
    # FINISHED!

def for_csv(file_name, total_results_by_config):
    for curr_config, metrics in total_results_by_config:
        #  Accuracy(training and validation)
        training_accuracy = metrics.training.accuracy
        validation_accuracy = metrics.validation.accuracy
        # Average Recall(validation)
        validation_average_recall =( metrics.validation.java.recall + metrics.validation.python.recall +
              metrics.validation.macro_avg.recall + metrics.validation.weighted_avg.recall) / 4
        #  Average Precision (validation)
        validation_average_precision = ( metrics.validation.java.precision + metrics.validation.python.precision +
              metrics.validation.macro_avg.precision + metrics.validation.weighted_avg.precision) / 4
        # average F - 1(Validation)
        validation_average_f1 =  ( metrics.validation.java.f1 + metrics.validation.python.f1 +
              metrics.validation.macro_avg.f1 + metrics.validation.weighted_avg.f1) / 4
        #config 1
        config_1 = list(list(curr_config.values())[0].values())[0]
        # config 2
        config_2 = list(list(curr_config.values())[0].values())[1]
        # validation time
        validation_time = metrics.validation.time_to_run
        # training time
        training_time = metrics.training.time_to_run


        with open("grid_search_results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([file_name, config_1, config_2, training_accuracy, validation_accuracy, validation_average_recall,
                             validation_average_precision, validation_average_f1, training_time, validation_time])



def main_input():
    if len(sys.argv) < 4:
        print("Usage:")
        print(f"\tpython {sys.argv[0]} in_config in_raw_data n_folds")
        return

    in_config_filename = sys.argv[1]
    in_raw_data_filename = sys.argv[2]
    try:
        n_folds = int(sys.argv[3])
        if n_folds < 2:
            print("Invalid value for n_folds. Must be an integer >= 2")
            return
    except:
        print("invalid value for n_folds. Must be an integer >= 2")
        return

    # TODO: 1) Load your (grid-search) hyper-parameters
    (classifier_name, class_config) = load_hyperparameters(in_config_filename, "grid_search")

    # TODO: 2) Load your data
    X, Y = load_raw_dataset(in_raw_data_filename)

    # TODO: 3) generate a combination of parameters (check itertools.product)
    #          https://docs.python.org/3/library/itertools.html#itertools.product
    keys, combos = create_combinations(class_config)

    # TODO: 4) Use the combinations of parameters to run a grid search
    run_all_combinations(combos, keys, X, Y, n_folds, classifier_name)

    # TODO: 4) print the best parameters found (based on highest validation macro f-1 score)
    # FINISHED!


def create_combinations(class_config):
    values = list(class_config['logistic_classifier'].values())
    keys = list(class_config['logistic_classifier'].keys())
    # random combos of the config values
    combos = list(itertools.product(*values))
    return keys, combos

def run_all_combinations(combos, keys, X, Y, n_folds, classifier_name):
    total_results_by_config = []
    for combo in combos:

        # 3.1) create a custom config for this combination
        combo_config = {}
        for i in range(len(keys)):
            combo_config[keys[i]] = combo[i]
        config = {classifier_name: combo_config}

        #  3.2) run full cross-validation for this combination of parameters (re-use function from part 01)
        result = cross_validation(X, Y, n_folds, classifier_name, config)

        #   3.3) collect results
        total_results_by_config.append((config, result))

    return total_results_by_config

def determine_and_print_best_config_for_file(total_results_by_combo):
    max_f1 = 0
    best_config = None
    best_config_results = None
    for config, result in total_results_by_combo:
        f1 = result.validation.macro_avg.f1  # use class attribute instead of dict key
        if f1 > max_f1:
            max_f1 = f1
            best_config = config
            best_config_results = result


    print("\n\nBest configuration:")
    print(json.dumps(best_config, indent=2))

    print("\n\nBest parameters found")
    print(f"\t-> Best configuration: ???")
    print(json.dumps(best_config, indent=2))
    print(f"\t-> Best configuration Results (Training):")
    print(json.dumps(best_config_results.validation.to_dict(), indent=2))
    print(f"\t-> Best configuration Results (Validation):")
    print(json.dumps(best_config_results.training.to_dict(), indent=2))

def main():
    main_all()
    #main_input()


if __name__ == "__main__":
    main()
