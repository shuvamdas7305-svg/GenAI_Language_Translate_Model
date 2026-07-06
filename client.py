import requests
import streamlit as st


def get_groq_response(input_text , language):
    json_body={
        "input": {
            "language": language,
            "text": input_text
        },
        "config": {},
        "kwargs": {}
    }
    

    response= requests.post(
    "http://127.0.0.1:8001/chain/invoke",
    json=json_body

    )
    return response.json()

st.title("AIbot : language model")
# ✅ Language selection zone
language = st.selectbox(
    "Select language to translate into:",
    ["French", "Hindi", "Bengali", "Spanish", "German", "Japanese", "Korean", "Russian", "Italian", "Portuguese", "Arabic", "Turkish", "Dutch", "Swedish", "Norwegian", "Danish", "Finnish", "Polish", "Czech", "Slovak", "Hungarian", "Romanian", "Bulgarian", "Greek", "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay", "Filipino", "Swahili", "Zulu", "Xhosa", "Afrikaans", "Amharic", "Yoruba", "Igbo", "Hausa", "Somali", "Nepali", "Sinhala", "Burmese", "Khmer", "Lao", "Mongolian", "Tibetan", "Pashto", "Urdu", "Punjabi", "Gujarati", "Marathi", "Telugu", "Tamil", "Kannada", "Malayalam", "Odia", "Assamese", "Maithili", "Santali", "Konkani", "Manipuri", "Bodo", "Dogri", "Kashmiri", "Sindhi", "Tulu", "Bhili/Bhilodi", "Gondi", "Kurukh/Oraon", "Mundari", "Ho", "Khasi", "Mizo/Lushai", "Karbi", "Dimasa", "Bishnupriya Manipuri", "Chakma", "Hmar", "Lepcha", "Nicobarese", "Shan/Thai (Myanmar)", "Tangkhul Naga", "Ao Naga", "Angami Naga", "Sema Naga", "Rongmei Naga"]
)
# Text input
input_text = st.text_input("Enter text")

# Output
if input_text:
    result = get_groq_response(input_text, language)

    # cleaner output
    st.subheader("Translated Text:")
    st.write(result["output"])