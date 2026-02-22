import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def classify_domain(complaint_text):
    prompt = f"""
    Classify the following public complaint into one category:
    Water, Road, Sanitation, Electricity, Others.

    Complaint: {complaint_text}

    Only return one word from the list.
    """

    response = model.generate_content(prompt)

    result = response.text.strip()

    allowed = ["Water", "Road", "Sanitation", "Electricity"]

    if result not in allowed:
        return "Others"

    return result
