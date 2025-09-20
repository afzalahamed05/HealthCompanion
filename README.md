# 🩺 HealthMate – AI-Powered Healthcare Assistant
HealthMate Chatbot


HealthMate is an **AI-powered healthcare assistant** designed to help users track their health, diagnose mild symptoms, find nearby hospitals, and manage medical history.  
It combines **Machine Learning**, **Generative AI**, and **real-time APIs** to deliver an intelligent, cross-platform healthcare experience.


## Features

- **🧑‍💼 User Authentication:** Secure sign-up and login (name, age, email, phone, username/password).
- **🎙️ Symptom Input:** Enter symptoms via **voice** or **text**.
- **💬 Chatbot:** Get instant health advice powered by:
  - Machine Learning (Naive Bayes & Logistic Regression models)
  - GPT-based medical conversational assistant
- **🩺 Doctor Recommendations:** Find nearby doctors.
- **📜 Medical History:** Save user health records securely in Firebase Firestore.
- **🗺️ Quick Actions Dashboard:**
  - Check Symptoms
  - Track Vitals
  - Schedule Appointments
  - Manage Medications
  - Get Daily Health Tips


## 🛠️ Tech Stack

| Layer          | Technology Used |
|----------------|----------------|
| **Frontend**   | Flutter (Dart) |
| **Backend**    | Node.js + Express.js |
| **Database**   | Firebase Firestore |
| **Machine Learning** | Python (Naive Bayes & Logistic Regression) |
| **Generative AI** | OpenAI GPT API |
| **Hosting/Deployment** | Firebase / Localhost (Dev) |

## 📂 Folder Structure

HealthMate/
│
├── frontend/ # Flutter app (UI)
│ ├── lib/ # Main Dart source files
│ └── assets/ # Images, icons, etc.
│
├── backend/ # Node.js + Express backend
│ ├── routes/ # API routes
│ ├── models/ # ML model integration
│ └── app.js # Main backend entry
│
├── ml-models/ # Python scripts for training ML models
│ ├── naive_bayes.py
│ ├── logistic_regression.py
│ └── dataset/ # Training datasets
Backend Setup (Node.js)

Navigate to the backend folder:

cd backend


Install dependencies:

npm install


Create a .env file and add:

PORT=5000
FIREBASE_API_KEY=your_firebase_api_key
OPENAI_API_KEY=your_openai_api_key


Start the backend server:

npm run dev


The backend will run on: http://localhost:5000

3️⃣ Machine Learning Model Setup (Python)

Go to the ML models folder:

cd ml-models


Create a virtual environment:

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install required Python packages:

pip install -r requirements.txt


Run training scripts:

python naive_bayes.py
python logistic_regression.py

4️⃣ Frontend Setup (Flutter)

Navigate to the Flutter folder:

cd frontend
Install dependencies:
flutter pub get
Run the app:
flutter run

| Method   | Endpoint               | Description                        |
| -------- | ---------------------- | ---------------------------------- |
| **POST** | `/api/auth/signup`     | Register a new user                |
| **POST** | `/api/auth/login`      | User login                         |
| **POST** | `/api/symptoms`        | Submit symptoms for AI/ML analysis |
| **GET**  | `/api/doctors`         | Fetch nearby doctors               |
| **GET**  | `/api/history/:userId` | Retrieve user's medical history    |


