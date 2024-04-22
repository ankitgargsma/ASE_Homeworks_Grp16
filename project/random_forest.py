import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder



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
    
def calculate_metrics(y_true, y_pred):
    """
    Calculate precision, recall, F1-score, and statistical significance.
    
    Args:
    - y_true (array-like): True class labels.
    - y_pred (array-like): Predicted class labels.
    
    Returns:
    - metrics (dict): Dictionary containing evaluation metrics.
    """
    precision = precision_score(y_true, y_pred, pos_label=y_true.unique()[0], zero_division=1)
    recall = recall_score(y_true, y_pred, pos_label=y_true.unique()[0])
    f1 = f1_score(y_true, y_pred, pos_label=y_true.unique()[0])
    fmi = fowlkes_mallows_index(y_true, y_pred)
    significance_value = statistical_significance(y_true, y_pred)
    effect_size_value = effect_size(y_true, y_pred)
    
    metrics = {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'fmi': fmi,
        'effect size': effect_size_value,
        'Statistical significance (p-value)': significance_value,
    }
    return metrics

def fowlkes_mallows_index(y_true, y_pred):
    """
    Compute the Fowlkes-Mallows index.
    
    Args:
    - y_true (array-like): True class labels.
    - y_pred (array-like): Predicted class labels.
    
    Returns:
    - float: Fowlkes-Mallows index.
    """
    tp = sum((y_true == 1) & (y_pred == 1))
    fp = sum((y_true == 0) & (y_pred == 1))
    fn = sum((y_true == 1) & (y_pred == 0))
    
    if tp == 0:
        return 0
    
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    fmi = np.sqrt(precision * recall)
    return fmi

def random_forest(data):
    """
    Train and test a random forest classifier on the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics.
    """
    label_encoders = {}
    for column in data.select_dtypes(include=['object']):
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column])
    
    # Split the data into features (X) and target variable (y)
    X = data.iloc[:, :-1]  # Features (all columns except the last one)
    y = data.iloc[:, -1]   # Target variable (last column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    
    # Initialize the Random Forest classifier
    clf = RandomForestClassifier()

    # Train the classifier
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Calculate evaluation metrics
    metrics = calculate_metrics(y_test, y_pred)
    
    # Calculate test accuracy separately and add it to the metrics dictionary
    accuracy = accuracy_score(y_test, y_pred)
    metrics['test_accuracy'] = accuracy
    
    return metrics


def random_forest_small(data):
    """
    Train and test a random forest classifier on a smaller random chunk of the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics for the smaller random chunk.
    """
    if data is None:
        return {}
    
    # Take a smaller random chunk of the data
    smaller_data = data.sample(frac=0.15)
    
    # Call random_forest function to evaluate metrics on the smaller chunk
    return random_forest(smaller_data)


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


def main(file_path):
    """
    Main function to load data and print evaluation metrics.
    
    Args:
    - file_path (str): Path to the CSV file.
    """
    data = read_data(file_path)
    if data is not None:
        data = drop_nan_values(data)
        print("Data loaded successfully!")
        metrics_full = random_forest(data)
        print("Metrics for the full dataset:")
        print(metrics_full)
        print("=" * 50)
        metrics_small = random_forest_small(data)
        print("Metrics for the smaller random chunk:")
        print(metrics_small)

def main_multiple(file_dir):
    """
    Main function to load data from multiple files and print evaluation metrics.
    
    Args:
    - file_dir (str): Directory containing the dataset files.
    
    Returns:
    - tuple: Tuple containing dictionaries of evaluation metrics for the full dataset and the smaller random chunk.
    """
    full_metrics_list = []
    smaller_metrics_list = []
    
    for file_name in os.listdir(file_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(file_dir, file_name)
            print(f"Processing file: {file_path}")
            data = read_data(file_path)
            if data is not None:
                full_metrics = random_forest(data)
                print("Metrics for the full dataset:")
                print(full_metrics)
                full_metrics_list.append(full_metrics)
                
                smaller_metrics = random_forest_small(data)
                print("Metrics for the smaller random chunk:")
                print(smaller_metrics)
                smaller_metrics_list.append(smaller_metrics)
                
                print("="*50)
    
    return full_metrics_list, smaller_metrics_list

if __name__ == "__main__":
    file_path = "../project_data/"
    main_multiple(file_path)

