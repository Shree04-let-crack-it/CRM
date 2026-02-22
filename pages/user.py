import streamlit as st
import pandas as pd
import google.generativeai as genai
from database import insert_complaint, get_complaints_by_user
from config import GEMINI_API_KEY
from googletrans import Translator

# --------------------------------------------------
# CONFIGURE GEMINI
# --------------------------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------------------
# GOOGLE TRANSLATE SETUP
# --------------------------------------------------
translator = Translator()

# --------------------------------------------------
# GEMINI DOMAIN CLASSIFIER
# --------------------------------------------------
def classify_domain_with_gemini(text_en):
    """
    Classify complaint domain using Gemini AI.
    Input must be English text.
    """
    prompt = f"""
    You are a government complaint classifier.

    Classify the following complaint into ONLY ONE of these categories:
    Water, Road, Sanitation, Electricity, Others.

    Complaint:
    "{text_en}"

    Return ONLY the category name.
    """
    try:
        response = model.generate_content(prompt)
        domain = response.text.strip()
        allowed_domains = ["Water", "Road", "Sanitation", "Electricity", "Others"]

        for d in allowed_domains:
            if d.lower() in domain.lower():
                return d
        return "Others"
    except Exception:
        return "Others"

# --------------------------------------------------
# USER DASHBOARD
# --------------------------------------------------
def show_user():

    # -------------------------
    # LANGUAGE SELECTION
    # -------------------------
    st.sidebar.subheader("🌐 Select Language")
    indian_languages = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Telugu": "te",
        "Marathi": "mr",
        "Tamil": "ta",
        "Gujarati": "gu",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Odia": "or",
        "Punjabi": "pa",
        "Assamese": "as"
    }
    target_lang = st.sidebar.selectbox("Choose your language", list(indian_languages.keys()))

    def translate_text(text):
        try:
            return translator.translate(text, dest=indian_languages[target_lang]).text
        except Exception:
            return text

    # -------------------------
    # AUTHENTICATION CHECK
    # -------------------------
    username = st.session_state.get("username")
    if not username:
        st.warning(translate_text("Please login first."))
        return

    # -------------------------
    # DASHBOARD TITLE
    # -------------------------
    st.title(translate_text("👤 Citizen Dashboard"))

    # -------------------------
    # RAISE COMPLAINT
    # -------------------------
    st.subheader(translate_text("📝 Raise New Complaint"))
    st.markdown(
        translate_text(
            "💡 You can write your complaint in any Indian regional language. "
            "It will be automatically converted to English for processing."
        )
    )

    complaint_text = st.text_area(
        translate_text("Describe your issue"),
        placeholder=translate_text("Write your issue here...")
    )

    if st.button(translate_text("🚀 Submit Complaint"), use_container_width=True):

        if not complaint_text.strip():
            st.warning(translate_text("Please enter complaint text."))
            return

        with st.spinner(translate_text("🔍 Translating & classifying complaint...")):
            # Translate user input to English before storing
            try:
                complaint_en = translator.translate(complaint_text, dest='en').text
            except Exception:
                complaint_en = complaint_text

            # Classify domain using Gemini
            domain = classify_domain_with_gemini(complaint_en)

        # Insert English complaint into DB
        insert_complaint(
            complaint_en.strip(),
            domain,
            username
        )

        st.success(translate_text(f"Complaint submitted successfully under '{domain}' department."))
        st.rerun()

    st.divider()

    # -------------------------
    # VIEW COMPLAINTS
    # -------------------------
    st.subheader(translate_text("📋 My Complaints & Status"))

    complaints = get_complaints_by_user(username)

    if complaints:
        df = pd.DataFrame(
            complaints,
            columns=["ID", "Text", "Domain", "Priority", "Status", "Timestamp"]
        )

        # Translate complaint text in dashboard if user selected another language
        if target_lang != "English":
            df["Text"] = df["Text"].apply(lambda x: translate_text(x))

        st.dataframe(
            df[["ID", "Text", "Domain", "Priority", "Status", "Timestamp"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(translate_text("You have not raised any complaints yet."))
