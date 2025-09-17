# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load the dataset from CSV file
file_path = 'disease_symptoms_2023.csv'
if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found!")
    exit()

df = pd.read_csv(file_path)

# Debug: Print column names
print("\nColumn names in the dataset:")
print(df.columns.tolist())

# Explore the data basics
print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nShape of the dataset (rows, columns):")
print(df.shape)

# Use correct column name: 'diseases'
disease_column = 'diseases'
if disease_column not in df.columns:
    print(f"Error: Column '{disease_column}' not found in the dataset!")
    exit()

print("\nUnique diseases:")
print(df[disease_column].nunique())

print("\nMissing values per column:")
print(df.isnull().sum())

# Separate features (X: symptoms) and labels (y: diseases)
symptom_columns = [col for col in df.columns if col != disease_column]
X = df[symptom_columns]
y = df[disease_column]

# Clean: Fill any missing values with 0
X = X.fillna(0)

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save encoded labels and classes
joblib.dump(label_encoder, 'label_encoder.pkl')

# Save preprocessed data
X.to_pickle('X.pkl')
pd.Series(y_encoded).to_pickle('y_encoded.pkl')

# Save symptom names
symptom_names = symptom_columns
joblib.dump(symptom_names, 'symptom_names.pkl')

# Print samples to verify
print("\nSample symptoms (first row):")
print(X.iloc[0])

print("\nSample encoded label (first row):")
print(y_encoded[0])

print("\nDecoded back to disease:")
print(label_encoder.inverse_transform([y_encoded[0]]))

print("\nSample symptom names:")
print(symptom_names[:5])