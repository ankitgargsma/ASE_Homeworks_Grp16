import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
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
        y_pred_train = random_classifier(pd.concat([X_train, y_train], axis=1))
        y_pred_test = random_classifier(pd.concat([X_test, y_test], axis=1))
        
        # Calculate accuracy
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        print("Train Accuracy:", train_accuracy)
        print("Test Accuracy:", test_accuracy)

# Example usage:
if __name__ == "__main__":
    file_path = "../../data/diabetes.csv"
    main(file_path)
