from flask import Flask, render_template, request, session
import pandas as pd
import joblib
from scipy.sparse import csr_matrix
import numpy as np
import os

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session

# Load model and data
model = joblib.load("logistic_regression_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
symptom_names = joblib.load("symptom_names.pkl")
symptom_names = [s.lower() for s in symptom_names]

df = pd.read_csv("disease_symptoms_2023.csv")
disease_symptom_matrix = df.drop("diseases", axis=1).values
disease_names = df["diseases"].values

def extract_symptoms(text):
    text = text.lower()
    return [sym for sym in symptom_names if sym in text]

def get_associated_symptoms(disease_idx, chosen):
    disease_row = disease_symptom_matrix[disease_idx]
    sym_indices = np.where(disease_row == 1)[0]
    related = [symptom_names[i] for i in sym_indices if symptom_names[i] not in chosen]
    return related[:3]

@app.route("/", methods=["GET", "POST"])
def home():
    if "chat_history" not in session:
        session["chat_history"] = [{"sender": "bot", "text": "Hello 👋! Tell me your symptoms and I’ll try to help."}]
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            session["chat_history"].append({"sender": "user", "text": user_input})

            selected_symptoms = extract_symptoms(user_input)
            if not selected_symptoms:
                bot_reply = "Hmm 🤔 I couldn’t detect clear symptoms. Could you rephrase? (e.g., 'I have fever and headache')"
            else:
                vector = [1 if s in selected_symptoms else 0 for s in symptom_names]
                X_new = csr_matrix([vector])
                y_pred_proba = model.predict_proba(X_new)

                top_idx = y_pred_proba[0].argsort()[::-1][:1][0]
                disease = label_encoder.inverse_transform([top_idx])[0]
                related = get_associated_symptoms(top_idx, selected_symptoms)

                bot_reply = (
                    f"It sounds like you might have **{disease}**.\n"
                    f"Other symptoms to check: {', '.join(related) if related else 'None'}.\n"
                    f"If things worsen, please consult a doctor 🩺."
                )

            session["chat_history"].append({"sender": "bot", "text": bot_reply})
    
    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
