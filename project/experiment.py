import os
import pandas as pd

from knn import main_multiple as knn_main_multiple
from random_classifier import main_multiple as random_classifier_main_multiple
from random_forest import main_multiple as random_forest_main_multiple
from decision_tree import main_multiple as decision_tree_main_multiple

def run_experiments(file_path, iterations=2):
    """
    Run experiments for all models, average the metrics over multiple iterations, and store the data.
    
    Args:
    - file_path (str): Directory containing the dataset files.
    - iterations (int): Number of iterations to run for each model.
    """
    model_functions = {
        'Decision Tree': decision_tree_main_multiple,
        'KNN': knn_main_multiple,
        'Random Classifier': random_classifier_main_multiple,
        'Random Forest': random_forest_main_multiple
    }

    model_metrics_sum_full = {model_name: {metric: 0 for metric in ['precision', 'recall', 'f1', 'fmi', 'effect size', 'Statistical significance (p-value)', 'test_accuracy']} for model_name in model_functions.keys()}
    model_metrics_count_full = {model_name: {metric: 0 for metric in ['precision', 'recall', 'f1', 'fmi', 'effect size', 'Statistical significance (p-value)', 'test_accuracy']} for model_name in model_functions.keys()}
    
    model_metrics_sum_small = {model_name: {metric: 0 for metric in ['precision', 'recall', 'f1', 'fmi', 'effect size', 'Statistical significance (p-value)', 'test_accuracy']} for model_name in model_functions.keys()}
    model_metrics_count_small = {model_name: {metric: 0 for metric in ['precision', 'recall', 'f1', 'fmi', 'effect size', 'Statistical significance (p-value)', 'test_accuracy']} for model_name in model_functions.keys()}

   
    for _ in range(iterations):
        print(f"Iteration {_ + 1}/{iterations}")
        for model_name, model_function in model_functions.items():
            print(f"Running experiments for {model_name}...")
            full_metrics_list, smaller_metrics_list = model_function(file_path)
            for full_metrics, smaller_metrics in zip(full_metrics_list, smaller_metrics_list):
                if full_metrics is not None:
                    for metric, value in full_metrics.items():
                        if value is not None:
                            model_metrics_sum_full[model_name][metric] += value
                            model_metrics_count_full[model_name][metric] += 1
                if smaller_metrics is not None:
                    for metric, value in smaller_metrics.items():
                        if value is not None:
                            model_metrics_sum_small[model_name][metric] += value
                            model_metrics_count_small[model_name][metric] += 1

    # Calculate average metrics for full dataset
    model_metrics_avg_full = {}
    for model_name, model_metrics in model_metrics_sum_full.items():
        model_metrics_avg_full[model_name] = {}
        for metric, total in model_metrics.items():
            count = model_metrics_count_full[model_name][metric]
            if count != 0:
                model_metrics_avg_full[model_name][metric] = total / count
            else:
                model_metrics_avg_full[model_name][metric] = 0

    # Calculate average metrics for smaller random chunk
    model_metrics_avg_small = {}
    for model_name, model_metrics in model_metrics_sum_small.items():
        model_metrics_avg_small[model_name] = {}
        for metric, total in model_metrics.items():
            count = model_metrics_count_small[model_name][metric]
            if count != 0:
                model_metrics_avg_small[model_name][metric] = total / count
            else:
                model_metrics_avg_small[model_name][metric] = 0

    # Print and save metrics
    print("\nAverage Metrics:")
    for model_name in model_functions.keys():
        print(f"\n{model_name}:")
        # Print metrics for full dataset
        print(f"{model_name} (Full data):")
        for metric, value in model_metrics_avg_full[model_name].items():
            print(f"{metric}: {value}")

        # Print metrics for smaller random chunk
        print(f"\n{model_name} (Small data):")
        for metric, value in model_metrics_avg_small[model_name].items():
            print(f"{metric}: {value}")

# Main entry point
if __name__ == "__main__":
    file_path = "../project_data/"  # Adjust the path as needed
    run_experiments(file_path)
