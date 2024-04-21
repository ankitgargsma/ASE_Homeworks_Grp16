import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder, StandardScaler

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
    
def KNN(data):
    """
    Train and test a KNN classifier on the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics.
    """
    label_encoders = {}
    for column in data.select_dtypes(include=['object']):
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column])
    X = data.iloc[:, :-1]  # Features (all columns except the last one)
    y = data.iloc[:, -1]   # Target variable (last column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the KNN classifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = knn.predict(X_test_scaled)

    # Calculate evaluation metrics
    precision = precision_score(y_test, y_pred, pos_label=y_test.unique()[0], zero_division=1)
    recall = recall_score(y_test, y_pred, pos_label=y.unique()[0])
    f1 = f1_score(y_test, y_pred, pos_label=y.unique()[0])
    accuracy = accuracy_score(y_test, y_pred)
    g_value = gini_impurity(y_test)
    significance_value = statistical_significance(y_test, y_pred)
    effect_size_value = effect_size(y_test, y_pred)

    # Return evaluation metrics
    metrics = {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'g_value': g_value,
        'effect size': effect_size_value,
        'Statistical significance (p-value)': significance_value,
        'test_accuracy': accuracy
    }
    return metrics

def KNN_small(data):
    """
    Train and test a KNN classifier on a smaller random chunk of the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics for the smaller random chunk.
    """
    # Take a smaller random chunk of the data
    smaller_data = data.sample(frac=0.15, random_state=42)
    
    # Call KNN function to evaluate metrics on the smaller chunk
    return KNN(smaller_data)

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
    
    # Calculate TPR (Sensitivity or Recall) and FPR (Fall-Out)
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    
    # Compute Cohen's d
    cohen_d = (tpr - fpr) / np.sqrt((tp + fn) * (fp + tn) / (tp + fp + tn + fn))
    
    return cohen_d


def main(file_path):
    """
    Main function to load data and return evaluation metrics.
    
    Args:
    - file_path (str): Path to the CSV file.
    
    Returns:
    - metrics_full (dict): Dictionary containing metrics for the full dataset.
    - metrics_small (dict): Dictionary containing metrics for the smaller random chunk.
    """
    data = read_data(file_path)
    if data is not None:
        print("Data loaded successfully!")
        metrics_full = KNN(data)
        print("Metrics for the full dataset:")
        print(metrics_full)
        print("=" * 50)
        metrics_small = KNN_small(data)
        print("Metrics for the smaller random chunk:")
        print(metrics_small)
        
        return metrics_full, metrics_small  # Return the metrics instead of printing them

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
            
            # Full dataset
            metrics_full, metrics_small = main(file_path)  # Call main and get both metrics
            full_metrics.append(metrics_full)  # Append metrics_full
            smaller_metrics.append(metrics_small)  # Append metrics_small
    
    return full_metrics, smaller_metrics


if __name__ == "__main__":
    file_path = "../project_data/"
    main_multiple(file_path)