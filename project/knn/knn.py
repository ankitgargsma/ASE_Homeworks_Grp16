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
    
def KNN(data):
    """
    Train and test a random forest classifier on the given dataset.
    
    Args:
    - data (DataFrame): Pandas DataFrame containing the dataset.
    
    Returns:
    - dict: Dictionary containing the evaluation metrics.
    """
    # Split the data into features (X) and target variable (y)
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
    #knn.fit(X_train, y_train)
    knn.fit(X_train_scaled,y_train)

    # Make predictions
    #y_pred = knn.predict(X_test)
    y_pred = knn.predict(X_test_scaled)
    
    # Calculate evaluation metrics
    precision = precision_score(y_test, y_pred, pos_label=y.unique()[0])
    recall = recall_score(y_test, y_pred, pos_label=y.unique()[0])
    f1 = f1_score(y_test, y_pred, pos_label=y.unique()[0])
    
    # Return evaluation metrics
    metrics = {'precision': precision, 'recall': recall, 'f1': f1}
    return metrics

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
    metrics = KNN(data)
    print(metrics)


if __name__ == "__main__":
    file_path = "../../data/diabetes.csv"
    main(file_path)
