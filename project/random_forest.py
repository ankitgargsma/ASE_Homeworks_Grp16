import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize the Random Forest classifier
    clf = RandomForestClassifier(random_state=42)

    # Train the classifier
    clf.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = clf.predict(X_test_scaled)

    # Calculate metrics
    g_value = gini_impurity(y_test)
    significance_value = statistical_significance(y_test, y_pred)
    effect_size_value = effect_size(y_test, y_pred)


    # Calculate evaluation metrics
    precision = precision_score(y_test, y_pred, pos_label=y.unique()[0])
    recall = recall_score(y_test, y_pred, pos_label=y.unique()[0])
    f1 = f1_score(y_test, y_pred, pos_label=y.unique()[0])
    
    # Calculate accuracy
    train_accuracy = accuracy_score(y_train, clf.predict(X_train_scaled))
    test_accuracy = accuracy_score(y_test, y_pred)
    
    # Return evaluation metrics
    metrics = {'precision': precision, 'recall': recall, 'f1': f1, 'g_value': g_value, 'effect size': effect_size_value, 'Statistical significance (p-value)': significance_value, 'test_accuracy': test_accuracy}
    return metrics

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
    tp = sum((y_true == 1) & (y_pred == 1))
    fp = sum((y_true == 0) & (y_pred == 1))
    tn = sum((y_true == 0) & (y_pred == 0))
    fn = sum((y_true == 1) & (y_pred == 0))

    n = len(y_true)

    if (tp + fn) == 0 or (tp + fp) == 0 or n == 0:
        return 0

    p1 = (tp + fn) / n
    p2 = (tp + fp) / n
    p = (tp + fn) / n

    return (p1 - p2) / p

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
            data = read_data(file_path)
            if data is not None:
                metrics = random_forest(data)
                print(metrics)
                print("="*50)
            return metrics

if __name__ == "__main__":
    file_path = "../project_data/"
    main_multiple(file_path)
