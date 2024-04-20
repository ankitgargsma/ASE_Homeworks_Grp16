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

    model_metrics_sum = {model_name: {metric: 0 for metric in ['precision', 'recall', 'f1', 'g_value', 'effect size', 'Statistical significance (p-value)', 'test_accuracy']} for model_name in model_functions.keys()}

    for _ in range(iterations):
        print(f"Iteration {_ + 1}/{iterations}")
        for model_name, model_function in model_functions.items():
            print(f"Running experiments for {model_name}...")
            metrics = model_function(file_path)
            if metrics is not None:
                for metric, value in metrics.items():
                    if value is not None:
                        model_metrics_sum[model_name][metric] += value

    # Calculate average metrics
    model_metrics_avg = {model_name: {metric: total / iterations for metric, total in model_metrics.items()} for model_name, model_metrics in model_metrics_sum.items()}

    # Print average metrics
    print("\nAverage Metrics:")
    for model_name, metrics in model_metrics_avg.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

    # Save metrics to CSV file
    df = pd.DataFrame(model_metrics_avg)
    if not os.path.exists("results"):
        os.makedirs("results")
    file_path = os.path.join("results", "average_metrics.csv")
    df.to_csv(file_path, index=False)
    print("\nAverage metrics saved.")

# Main entry point
if __name__ == "__main__":
    file_path = "../project_data/"  # Adjust the path as needed
    run_experiments(file_path)
