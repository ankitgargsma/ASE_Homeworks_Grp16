import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # statistical data visualization
import warnings
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

warnings.filterwarnings('ignore')

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
    
    
def decision_tree(data):
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

    # Initialize the Decision Tree classifier
    clf = DecisionTreeClassifier()

    # Train the classifier
    clf.fit(X_train_scaled, y_train)

    # Make predictions
    #y_pred = knn.predict(X_test)
    y_pred = clf.predict(X_test_scaled)

    # Calculate metrics
    effect_size_value = effect_size(y_test, y_pred)
    significance_value = statistical_significance(y_test, y_pred)
    g_value = gini_impurity(y_test)
    #recall_value = recall_score(y_test, y_pred, average='macro')
    accuracy_value = accuracy_score(y_test, y_pred)
    #precision_value = precision_score(y_test, y_pred, average='macro')
    
    # Calculate evaluation metrics
    precision = precision_score(y_test, y_pred, pos_label=y.unique()[0])
    recall = recall_score(y_test, y_pred, pos_label=y.unique()[0])
    f1 = f1_score(y_test, y_pred, pos_label=y.unique()[0])
    
    # Perform random classification
    y_pred_train = decisiontree_classifier(pd.concat([X_train, y_train], axis=1))
    y_pred_test = decisiontree_classifier(pd.concat([X_test, y_test], axis=1))
        
    # Calculate accuracy
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    # Return evaluation metrics
    metrics = {'precision': precision, 'recall': recall, 'f1': f1, 'g_value': g_value, 'Statistical significance (p-value)': significance_value, 'train_accuracy': train_accuracy, 'test_accuracy': train_accuracy}
    return metrics

def decisiontree_classifier(data):
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

def statistical_significance(y_true, y_pred):
    contingency_table = pd.crosstab(y_true, y_pred)
    _, p, _, _ = chi2_contingency(contingency_table)
    return p

def gini_impurity(y):
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / len(y)
    gini = 1 - np.sum(probabilities**2)
    return gini


def main(file_path):
    """
    Main function to load data and print the first few rows.
    
    Args:
    - file_path (str): Path to the CSV file.
    """
    data = read_data(file_path)
    # if data is not None:
    #     print("Data loaded successfully!")
    #     print(data.head())  # Print the first few rows to verify
    metrics = decision_tree(data)
    print(metrics)

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
                metrics = decision_tree(data)
                print(metrics)
                print("="*50)

if __name__ == "__main__":
    file_path = "../../project_data/"
    main_multiple(file_path)