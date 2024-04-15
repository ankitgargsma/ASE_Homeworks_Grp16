import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

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
    # Split the data into features (X) and target variable (y)
    X = data.iloc[:, :-1]  # Features (all columns except the last one)
    y = data.iloc[:, -1]   # Target variable (last column)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Initialize the random forest classifier
    clf = RandomForestClassifier(random_state=42)
    
    # Train the classifier
    clf.fit(X_train, y_train)
    
    # Predict on the testing set
    y_pred = clf.predict(X_test)
    
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
    metrics = random_forest(data)
    print(metrics)


if __name__ == "__main__":
    file_path = "../../data/diabetes.csv"
    main(file_path)
