# Import necessary libraries
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, top_k_accuracy_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Load preprocessed data
X = pd.read_pickle('X.pkl') if os.path.exists('X.pkl') else None
y_encoded = pd.read_pickle('y_encoded.pkl') if os.path.exists('y_encoded.pkl') else None
label_encoder = joblib.load('label_encoder.pkl') if os.path.exists('label_encoder.pkl') else None
if X is None or y_encoded is None or label_encoder is None:
    print("Error: Preprocessed data (X.pkl, y_encoded.pkl, label_encoder.pkl) not found. Run data_preprocess.py first.")
    exit()

# Convert X to sparse matrix for memory efficiency
X = csr_matrix(X)
print("\nDataset shape (sparse):", X.shape)

# Step 2: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)
print("\nTraining set shape (X_train, y_train):", X_train.shape, y_train.shape)
print("Testing set shape (X_test, y_test):", X_test.shape, y_test.shape)

# Save train-test split (optional)
pd.DataFrame.sparse.from_spmatrix(X_train).to_pickle('X_train.pkl')
pd.DataFrame.sparse.from_spmatrix(X_test).to_pickle('X_test.pkl')
pd.Series(y_train).to_pickle('y_train.pkl')
pd.Series(y_test).to_pickle('y_test.pkl')

# Step 3: Model Choices
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000, n_jobs=-1)
}

# Step 4: Training + Evaluation
results = []
best_model = None
best_f1 = 0
best_model_name = None
best_y_pred = None

for model_name, model in models.items():
    print(f"\nTraining {model_name}...")
    try:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        precision = report['weighted avg']['precision']
        recall = report['weighted avg']['recall']
        f1 = report['weighted avg']['f1-score']
        
        # Top-3 Accuracy
        top3_accuracy = None
        if hasattr(model, 'predict_proba'):
            try:
                y_pred_proba = model.predict_proba(X_test)
                model_classes = model.classes_
                # Filter y_test and corresponding X_test to match model_classes
                mask = np.isin(y_test, model_classes)
                y_test_filtered = y_test[mask]
                X_test_filtered = X_test[mask]
                y_pred_proba_filtered = y_pred_proba[mask]
                if len(y_test_filtered) > 0:
                    # Map indices based on model_classes
                    valid_indices = [np.where(model_classes == c)[0][0] for c in model_classes]
                    y_pred_proba_mapped = y_pred_proba_filtered[:, valid_indices]
                    top3_accuracy = top_k_accuracy_score(y_test_filtered, y_pred_proba_mapped, k=3, labels=model_classes)
                else:
                    print(f"No valid samples for {model_name}: Skipping top-3 accuracy.")
            except Exception as e:
                print(f"Top-3 accuracy failed for {model_name}: {e}")
        
        # Save results
        results.append({
            'Model': model_name,
            'Accuracy': round(accuracy, 3),
            'Precision': round(precision, 3),
            'Recall': round(recall, 3),
            'F1': round(f1, 3),
            'Top-3 Accuracy': round(top3_accuracy, 3) if top3_accuracy is not None else 'N/A'
        })
        
        # Track best model (based on F1-score)
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = model_name
            best_y_pred = y_pred
        
        # Save model
        joblib.dump(model, f'{model_name.lower().replace(" ", "_")}_model.pkl')
        
    except Exception as e:
        print(f"Error training {model_name}: {e}")
        continue

# Step 5: Model Comparison
results_df = pd.DataFrame(results)
print("\nModel Comparison:")
print(results_df)
results_df.to_csv('model_comparison.csv', index=False)

# Generate confusion matrix for best model
if best_model is not None:
    cm = confusion_matrix(y_test, best_y_pred)
    print(f"Confusion matrix shape: {cm.shape}")
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=False, cmap='Blues')
    plt.title(f'Confusion Matrix - {best_model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.savefig(f'confusion_matrix_{best_model_name.lower().replace(" ", "_")}.png')
    plt.close()
    print(f"\nConfusion matrix saved for {best_model_name} as 'confusion_matrix_{best_model_name.lower().replace(' ', '_')}.png'")