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

    if target_page > pdf_document.page_count or target_page <= 0:
        raise ValueError("Invalid page number. Please provide a valid page number within the range of the PDF.")

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
    try:
        # Split the text into sentences
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

        # Translate each sentence individually
        translated_sentences = [EngtoHindi(sentence).convert for sentence in sentences]

        # Join the translated sentences into a single text
        translated_text = ' '.join(translated_sentences)

        return translated_text

    except TypeError as te:
        print(f"TypeError in translate_text_eng_to_hindi: {te}")
        return "Text can't be translated. Please provide valid input."

    except Exception as e:
        print(f"Error in translate_text_eng_to_hindi: {e}")
        traceback.print_exc()
        return "An error occurred during translation."

# Streamlit app
def main():
    st.title("PDF Audiobook with Translation")

    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if pdf_file is not None:
        st.success("PDF file uploaded successfully!")

        page_number = st.number_input("Enter Page Number", value=1, step=1, min_value=1, max_value=10000)

        try:
            lines = extract_text_from_pdf(pdf_file, page_number)
        except ValueError as ve:
            st.error(f"Error: {ve}")
            return

        st.subheader("Translation:")
        source_lang = st.selectbox("Select Source Language", ["en", "hi"])
        target_lang = st.selectbox("Select Target Language", ["en", "hi"])

        text = ' '.join(lines)

        # Translate the entire content of the specified page using EngtoHindi if source is English and target is Hindi
        translated_text = translate_text_eng_to_hindi(text)

        if st.button("Play Audio"):
            try:
                text_to_speech(translated_text, lang=target_lang)

                st.audio('output.mp3', format='audio/mp3')

            except ValueError as e:
                st.warning(f"Unable to generate audio: {e}")

if __name__ == "__main__":
    main()
