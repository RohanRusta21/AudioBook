import streamlit as st
import PyPDF2
from translate import Translator
import pyttsx3
import os

# Function to extract text from a PDF file starting from a specific page
def extract_text_from_pdf(uploaded_file, start_page):
    # Save the uploaded PDF file temporarily
    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Read text from the temporary PDF file starting from the specified page
    with open(temp_pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(start_page - 1, len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

    # Remove the temporary PDF file
    os.remove(temp_pdf_path)

    return text

# Function to translate text
def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translation = translator.translate(text)
    return translation

# Function to convert text to speech using pyttsx3
def text_to_speech(text, lang):
    if not text:
        raise ValueError("No text to speak")

    engine = pyttsx3.init()
    engine.say(text)
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

# Streamlit app
def main():
    st.title("PDF Audiobook with Translation")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if pdf_file is not None:
        st.success("PDF file uploaded successfully!")

        # Get user input for page number
        page_number = st.number_input("Enter Page Number", value=1, step=1, min_value=1, max_value=10000)

        # Translation options
        st.subheader("Translation:")
        source_lang = st.selectbox("Select Source Language", ["en", "hi"])
        target_lang = st.selectbox("Select Target Language", ["en", "hi"])

        # Extract text from the specified page
        text = extract_text_from_pdf(pdf_file, page_number)
        #st.subheader("Page Content:")
        #st.text(text)

        # Translate the text
        translated_text = translate_text(text, source_lang, target_lang)

        #st.subheader("Translated Content:")
        #st.text(translated_text)

        # Play audio button
        if st.button("Play Audio"):
            try:
                # Convert text to speech using pyttsx3
                text_to_speech(translated_text, lang='en')  # You can adjust the language as needed

                # Play the audio using Streamlit's audio widget
                st.audio('output.mp3', format='audio/mp3')

            except ValueError as e:
                st.warning(f"Unable to generate audio: {e}")

if __name__ == "__main__":
    main()
