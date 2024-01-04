import streamlit as st
import fitz  # PyMuPDF
from gtts import gTTS
from englisttohindi.englisttohindi import EngtoHindi
import os
import traceback
import re  # Add this line to import the 're' module

# Function to extract text from a PDF file for a specific page
def extract_text_from_pdf(uploaded_file, target_page):
    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    pdf_document = fitz.open(temp_pdf_path)

    if target_page > pdf_document.page_count:
        raise ValueError("Invalid page number. The PDF does not have the specified page.")

    page = pdf_document[target_page - 1]
    lines = page.get_text("text").split('\n')

    os.remove(temp_pdf_path)

    return lines

# Function to convert text to speech using gTTS
def text_to_speech(text, lang):
    try:
        if not text:
            raise ValueError("No text to speak")

        print(f"Text to be spoken: {text}")

        # Specify the language for the voice
        tts_lang = lang if lang == 'en' else 'hi'

        tts = gTTS(text, lang=tts_lang)

        print("Saving audio file...")
        tts.save('output.mp3')
        print("Audio file saved successfully!")

    except Exception as e:
        print(f"Error in text_to_speech function: {e}")
        traceback.print_exc()
        raise

# Function to translate text using EngtoHindi
def translate_text_eng_to_hindi(text):
    # Split the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Translate each sentence individually
    translated_sentences = [EngtoHindi(sentence).convert for sentence in sentences]

    # Join the translated sentences into a single text
    translated_text = ' '.join(translated_sentences)

    return translated_text

# Streamlit app
def main():
    st.title("PDF Audiobook with Translation")

    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if pdf_file is not None:
        st.success("PDF file uploaded successfully!")

        page_number = st.number_input("Enter Page Number", value=1, step=1, min_value=1, max_value=10000)

        lines = extract_text_from_pdf(pdf_file, page_number)

        st.subheader("Translation:")
        source_lang = st.selectbox("Select Source Language", ["en", "hi"])
        target_lang = st.selectbox("Select Target Language", ["en", "hi"])

        text = ' '.join(lines)

        # Translate the entire content of the specified page using EngtoHindi if source is English and target is Hindi
        if source_lang == "en" and target_lang == "hi":
            translated_text = translate_text_eng_to_hindi(text)
        else:
            translated_text = text

        if st.button("Play Audio"):
            try:
                text_to_speech(translated_text, lang=target_lang)

                st.audio('output.mp3', format='audio/mp3')

            except ValueError as e:
                st.warning(f"Unable to generate audio: {e}")

if __name__ == "__main__":
    main()
