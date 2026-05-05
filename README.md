🛡️ AI Scam Detector (Text + Voice)
A multimodal scam detection system that analyzes both text messages and voice recordings to identify potential fraud using Machine Learning + NLP + Speech Recognition.

🚀 Live Demo
👉https://scam-deploy-sahil.streamlit.app/

📌 Features
📝 Text Scam Detection Analyze SMS / WhatsApp messages for fraud detection

🎤 Voice Scam Detection Upload audio → converts to text → detects scam

🧠 Machine Learning Model Trained using TF-IDF + Logistic Regression

⚠️ Intent-Based Detection Detects scams using:

OTP requests
Account threats
Sensitive data requests
📊 Confidence Score + Risk Level

Low Risk ✅
Medium Risk ⚠️
High Risk 🚨
🧠 How It Works
Input

User enters text OR uploads audio
Speech-to-Text (if audio)

Uses OpenAI Whisper model
Text Preprocessing

Remove punctuation
Remove stopwords
Vectorization

TF-IDF transformation
Prediction

Logistic Regression model
Rule-Based Enhancement

Detects intent:

OTP + urgency
Account + threat
Sensitive data request
🛠️ Tech Stack
Frontend: Streamlit
Machine Learning: Scikit-learn
NLP: NLTK
Speech Recognition: Whisper
Language: Python
📂 Project Structure
SCAM-DETECTOR/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── packages.txt
⚙️ Installation & Setup
1. Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
2. Install dependencies
pip install -r requirements.txt
3. Run the app
streamlit run app.py
📦 Requirements
streamlit
scikit-learn
nltk
openai-whisper
torch
ffmpeg-python
⚠️ Limitations
Audio processing may be slow on cloud deployment
Model may not detect all regional language scams
Accuracy depends on training dataset
🚀 Future Improvements
🔥 Add Hinglish / multilingual support
📊 Improve model with deep learning (BERT)
🧠 Add explainable AI (why message is scam)
💾 Save user history
