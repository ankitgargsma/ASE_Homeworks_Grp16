# Import necessary libraries
import os
import pandas as pd

# Import the main functions from each module
from project.decision_tree.decision_tree import main_multiple as decision_tree_main_multiple
from project.knn.knn import main_multiple as knn_main_multiple
from project.random_classifier.random_classifier import main_multiple as random_classifier_main_multiple
from project.random_forest.random_forest import main_multiple as random_forest_main_multiple

# Define the main function to run all experiments
def run_experiments(file_path):
    """
    Run experiments for all models and store the data.
    
    Args:
    - file_path (str): Directory containing the dataset files.
    """
    print("Running experiments for Decision Tree...")
    decision_tree_metrics = decision_tree_main_multiple(file_path)
    save_metrics("Decision_Tree", decision_tree_metrics)
    
    print("Running experiments for KNN...")
    knn_metrics = knn_main_multiple(file_path)
    save_metrics("KNN", knn_metrics)
    
    print("Running experiments for Random Classifier...")
    random_classifier_metrics = random_classifier_main_multiple(file_path)
    save_metrics("Random_Classifier", random_classifier_metrics)
    
    print("Running experiments for Random Forest...")
    random_forest_metrics = random_forest_main_multiple(file_path)
    save_metrics("Random_Forest", random_forest_metrics)

def save_metrics(model_name, metrics):
    """
    Save the evaluation metrics for a model to a CSV file.
    
    Args:
    - model_name (str): Name of the model.
    - metrics (dict): Dictionary containing the evaluation metrics.
    """
    if metrics is not None:
        # Convert metrics to DataFrame
        df = pd.DataFrame(metrics)
        
        # Create directory to store results if it doesn't exist
        if not os.path.exists("results"):
            os.makedirs("results")
        
        # Save metrics to CSV file
        file_path = os.path.join("results", f"{model_name}_metrics.csv")
        df.to_csv(file_path, index=False)
        print(f"Metrics saved for {model_name} model.")

# Main entry point
if __name__ == "__main__":
    file_path = "../project_data/"  # Adjust the path as needed
    run_experiments(file_path)
