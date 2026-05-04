import pickle
import streamlit as st
import nltk
import string
import tempfile
import whisper
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')

# -------- LOAD MODELS --------
@st.cache_resource
def load_models():
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    whisper_model = whisper.load_model("tiny")
    return tfidf, model, whisper_model

tfidf, model, whisper_model = load_models()

# -------- PREPROCESS --------
class PreProcessText:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def clean(self, text):
        text = ''.join([x for x in text if x not in string.punctuation])
        words = [w for w in text.split() if w.lower() not in self.stop_words]
        return " ".join(words)

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Scam Detector", layout="centered")

# -------- UI --------
st.title("🛡️ AI Scam Detector (Text + Voice)")
st.markdown("Detect scam messages using AI + smart fraud logic")

st.markdown("---")

# ✅ ONLY ONE uploader (fixed)
audio_file = st.file_uploader(
    "🎤 Upload Audio",
    type=["wav", "mp3", "m4a"],
    key="audio_input"
)

user_text = st.text_area("📩 Or Enter Message")

# -------- BUTTON --------
if st.button("🔍 Analyze", use_container_width=True):

    # -------- INPUT --------
    if user_text:
        input_message = user_text

    elif audio_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                temp_path = tmp.name

            st.info("Processing audio...")
            transcription = whisper_model.transcribe(temp_path)
            input_message = transcription["text"]

            st.subheader("📝 Transcribed Text")
            st.write(input_message)

            st.audio(audio_file)

        except:
            st.error("Audio processing failed. Try text input.")
            st.stop()

    else:
        st.warning("Please provide text or audio input")
        st.stop()

    # -------- PREPROCESS --------
    processor = PreProcessText()
    clean_text = processor.clean(input_message)

    # -------- ML --------
    vector_input = tfidf.transform([clean_text])
    result = model.predict(vector_input)[0]

    try:
        prob = model.predict_proba(vector_input)[0]
        scam_prob = prob[0]
    except:
        scam_prob = 0.5

    text_lower = clean_text.lower()

    # -------- RULE SYSTEM --------
    safe_patterns = [
        "your otp for login",
        "do not share this otp",
        "order has been shipped",
        "electricity bill",
        "bill generated"
    ]

    scam_patterns = [
        "lottery", "win", "prize",
        "urgent", "immediately", "act now",
        "click", "verify", "link",
        "account blocked", "account suspended",
        "send otp", "share otp",
        "confirm your account"
    ]

    # -------- INTENT --------
    has_otp = "otp" in text_lower

    has_threat = any(word in text_lower for word in [
        "blocked", "suspended", "deactivated"
    ])

    has_urgency = any(word in text_lower for word in [
        "urgent", "immediately", "now"
    ])

    has_account = "account" in text_lower
    has_details = "details" in text_lower or "information" in text_lower
    has_provide = "provide" in text_lower or "share" in text_lower

    has_sensitive = has_account and (has_details or has_provide)

    is_safe = any(p in text_lower for p in safe_patterns)
    is_scam_rule = any(p in text_lower for p in scam_patterns)

    # -------- FINAL DECISION --------
    final_result = result

    if is_safe:
        final_result = 1

    elif has_otp and (has_threat or has_urgency):
        final_result = 0

    elif has_sensitive and has_threat:
        final_result = 0

    elif has_account and has_provide and has_threat:
        final_result = 0

    elif is_scam_rule:
        final_result = 0

    # -------- OUTPUT --------
    st.markdown("---")
    st.subheader("🚨 Result")

    if final_result == 0:
        st.error("⚠️ Scam Detected")
    else:
        st.success("✅ No Scam Detected")

    st.metric("Confidence", f"{scam_prob*100:.2f}%")

    if scam_prob > 0.8:
        st.error("High Risk 🚨")
    elif scam_prob > 0.5:
        st.warning("Medium Risk ⚠️")
    else:
        st.success("Low Risk ✅")

    st.info("Reason: ML + intent-based fraud detection")