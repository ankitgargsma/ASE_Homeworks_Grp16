import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import pingouin as pg

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
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - predictions (array-like): Array of randomly generated class labels.
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
    precision = precision_score(y_true, y_pred, pos_label=y_true.unique()[0], zero_division=1)
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

def effect_size(y_true, y_pred):
    """
    Compute Cohen's d as an effect size measure.
    
    Args:
    - y_true (array-like): True class labels.
    - y_pred (array-like): Predicted class labels.
    
    Returns:
    - float: Cohen's d effect size.
    """
    # Compute true positive rate (TPR) and false positive rate (FPR)
    tp = sum((y_true == 1) & (y_pred == 1))
    fp = sum((y_true == 0) & (y_pred == 1))
    tn = sum((y_true == 0) & (y_pred == 0))
    fn = sum((y_true == 1) & (y_pred == 0))
    
    # Check if there are positive instances in y_true
    if (tp + fn) == 0:
        return 0  # Return 0 if there are no positive instances
    
    # Check if fp + tn is not zero to avoid division by zero
    if (fp + tn) == 0:
        return 0  # Return 0 if fp + tn is zero
    
    # Calculate TPR (Sensitivity or Recall) and FPR (Fall-Out)
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    
    # Compute Cohen's d
    cohen_d = (tpr - fpr) / np.sqrt((tp + fn) * (fp + tn) / (tp + fp + tn + fn))
    
    return cohen_d

def drop_nan_values(data):
    """
    Drop rows containing NaN values from the DataFrame.
    
    Args:
    - data (DataFrame): Input DataFrame.
    
    Returns:
    - DataFrame: DataFrame with NaN values dropped.
    """
    cleaned_data = data.dropna()
    return cleaned_data


def main(data):
    """
    Main function to evaluate random classifier on the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics.
    """
    # Perform random classification
    y_true = data.iloc[:, -1]  # True class labels
    y_pred = random_classifier(data)  # Predictions
    
    # Calculate evaluation metrics
    test_accuracy = accuracy_score(y_true, y_pred)
    test_precision, test_recall, test_f1 = evaluate_metrics(y_true, y_pred)
    g_value = gini_impurity(y_true)
    significance_value = statistical_significance(y_true, y_pred)
    effect_size_value = effect_size(y_true, y_pred)

    # Return evaluation metrics
    metrics = {
        'precision': test_precision,
        'recall': test_recall,
        'f1': test_f1,
        'g_value': g_value,
        'effect size': effect_size_value, 
        'Statistical significance (p-value)': significance_value,
        'test_accuracy': test_accuracy
    }
    return metrics



def main_multiple(file_dir):
    """
    Main function to load data from multiple files and print evaluation metrics.
    
    Args:
    - file_dir (str): Directory containing the dataset files.
    
    Returns:
    - full_metrics (list): List of dictionaries containing metrics for the full dataset.
    - smaller_metrics (list): List of dictionaries containing metrics for the smaller random chunk.
    """
    full_metrics = []
    smaller_metrics = []
    
    for file_name in os.listdir(file_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(file_dir, file_name)
            print(f"Processing file: {file_path}")
            

            
            data = read_data(file_path)
            data = drop_nan_values(data)

            # Full dataset
            full_metrics.append(main(data))
            
            # Random smaller chunk
            if data is not None:
                smaller_data = data.sample(frac=0.15, random_state=42)
                print("Processing smaller random chunk of the file...")
                smaller_metrics.append(main(smaller_data))
    
    return full_metrics, smaller_metrics

if __name__ == "__main__":
    file_path = "../project_data/"
    full_metrics, smaller_metrics = main_multiple(file_path)
    print("Full Dataset Metrics:")
    print(full_metrics)
    print("="*50)
    print("Smaller Random Chunk Metrics:")
    print(smaller_metrics)

