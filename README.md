🛡️ PhishGuard - Phishing URL Detection
PhishGuard is an AI-powered web application that detects whether a given URL is legitimate or a phishing attempt.
It combines machine learning, feature extraction, and a simple web interface to make internet browsing safer.

✨ Features
🔍 Detect Phishing URLs: Predict if a URL is malicious in real-time.

🧠 ML-Based Detection: Trained with real-world phishing and legitimate URLs.

🎨 Simple UI: Clean frontend with dark/light mode toggle.

📋 Feature Extraction: Extracts over 20+ URL-based features.

📱 Responsive Design: Works well across devices.

📬 Contact Modal: Easy way for users to get in touch.

🚀 Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: FastAPI (Python)

Machine Learning: XGBoost Classifier

Tools: Pandas, Scikit-learn

📂 Project Structure
graphql
Copy
Edit
PhishGuard/
├── backend/                  # FastAPI backend server
│   └── (backend code files)
├── frontend/                 # Frontend files (HTML/CSS/JS)
│   └── (index.html, etc.)
├── DataFiles/                 # Dataset and supporting files
│   ├── legitimate.csv
│   ├── phishing_urls.csv
├── Phishing_detection_app/    # Feature extraction scripts
│   └── URLFeatureExtraction.py
├── __pycache__/               # Python cache files
├── app.py                     # Main FastAPI app entry point
├── phishing_classifier.pkl    # Trained phishing detection model
├── XGBoostClassifier.pickle.dat # Alternative trained model
├── URL Feature Extraction.ipynb # Notebook for feature extraction
├── Phishing Website Detection_Models & Training.ipynb # Training notebook
├── Phishing Website Detection.pdf # Project report
├── NLP+PR.docx                 # Related documentation
├── requirements.txt           # Python dependencies
├── README.md                  # This file
🛠 How to Run Locally
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/phishguard.git
cd phishguard
Install backend dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the FastAPI server

bash
Copy
Edit
uvicorn app:app --reload
The server will start at: http://127.0.0.1:8000/

Open the frontend

Navigate to the frontend/ folder.

Open index.html in your browser.

It will interact with the backend API for predictions.

🧠 Model Details
Training Dataset: phishing_urls.csv, legitimate.csv

Model Used: XGBoost Classifier

Saved Models: phishing_classifier.pkl, XGBoostClassifier.pickle.dat

Feature Extraction: Custom Python script (URLFeatureExtraction.py) extracts features like:

URL length

Number of dots (.) in the URL

Presence of @ symbol

Domain registration length

and many more!

📸 Screenshots

frontend\Image\brave_screenshot.png

🚀 How to Run the Project
1. Clone the repository:
```bash git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

📬 Contact
Created with ❤️ by Shreyansh Sahu

LinkedIn | GitHub

