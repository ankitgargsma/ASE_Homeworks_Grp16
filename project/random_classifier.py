import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

def read_data(file_path):
    """
    Read data from a CSV file.
    
    Args:
    - file_path (str): Path to the CSV file.
    
    Returns:
    - DataFrame: Pandas DataFrame containing the data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print("Error occurred while reading the data:", e)
        return None
    
def random_classifier(data):
    """
    Randomly classify data.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the data.
    
    Returns:
    - predictions (list): List of randomly generated class labels.
    """
    # Get the name of the last column
    last_column_name = data.columns[-1]

    # Get the class labels
    class_labels = data[last_column_name].unique()
    
    # Generate random predictions
    predictions = np.random.choice(class_labels, size=len(data))
    
    return predictions

def evaluate_metrics(y_true, y_pred):
    """
    Calculate precision, recall, and F1 score.
    
    Args:
    - y_true (array-like): True class labels.
    - y_pred (array-like): Predicted class labels.
    
    Returns:
    - precision (float): Precision score.
    - recall (float): Recall score.
    - f1 (float): F1 score.
    """
    precision = precision_score(y_true, y_pred, pos_label=y_true.unique()[0])
    recall = recall_score(y_true, y_pred, pos_label=y_true.unique()[0])
    f1 = f1_score(y_true, y_pred, pos_label=y_true.unique()[0])
    return precision, recall, f1

def gini_impurity(y):
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    gini = 1 - np.sum(probabilities**2)
    return gini

def statistical_significance(y_true, y_pred):
    contingency_table = pd.crosstab(y_true, y_pred)
    _, p, _, _ = chi2_contingency(contingency_table)
    return p

def main(file_path):
    # Read the data
    data = read_data(file_path)

    if data is not None:
        print("Data loaded successfully!")
        
        # Split the data into features and target
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        
        # Perform random classification
        y_pred_test = random_classifier(pd.concat([X_test, y_test], axis=1))
        
        # Calculate accuracy for the test set
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        # Calculate evaluation metrics for the test set
        test_precision, test_recall, test_f1 = evaluate_metrics(y_test, y_pred_test)
        
        # Calculate gini impurity and statistical significance (p-value)
        g_value = gini_impurity(y_test)
        significance_value = statistical_significance(y_test, y_pred_test)
        
        # Return evaluation metrics
        metrics = {
            'precision': test_precision,
            'recall': test_recall,
            'f1': test_f1,
            'g_value': g_value,
            'Statistical significance (p-value)': significance_value,
            'train_accuracy': None,  # No training accuracy for random classifier
            'test_accuracy': test_accuracy
        }
        return metrics

def main_multiple(file_dir):
    """
    Main function to load data from multiple files and print evaluation metrics.
    
    Args:
    - file_dir (str): Directory containing the dataset files.
    """
    for file_name in os.listdir(file_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(file_dir, file_name)
            print(f"Processing file: {file_path}")
            metrics = main(file_path)
            if metrics is not None:
                print(metrics)
                print("="*50)

if __name__ == "__main__":
    file_path = "../../project_data/"
    main_multiple(file_path)
