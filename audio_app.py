import streamlit as st
import fitz  # PyMuPDF
from gtts import gTTS
from englisttohindi.englisttohindi import EngtoHindi
import os  # Add this line to import the 'os' module
import traceback  # Add this import for traceback

# Function to extract text from a PDF file for a specific page
def extract_text_from_pdf(uploaded_file, target_page):
    # Save the uploaded PDF file temporarily
    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())

    # Read text from the temporary PDF file for the specified page
    pdf_document = fitz.open(temp_pdf_path)
    
    if target_page > pdf_document.page_count:
        raise ValueError("Invalid page number. The PDF does not have the specified page.")

    page = pdf_document[target_page - 1]
    text = page.get_text()

    # Remove the temporary PDF file
    os.remove(temp_pdf_path)

    return text

# Function to translate text using EngtoHindi
def translate_text_eng_to_hindi(text):
    converter = EngtoHindi(text)
    return converter.convert

# Function to convert text to speech using gTTS
def text_to_speech(text, lang):
    try:
        if not text:
            raise ValueError("No text to speak")

        print(f"Text to be spoken: {text}")  # Add this line for debugging

        # Specify the language for the voice
        tts_lang = lang if lang == 'en' else 'hi'

        tts = gTTS(text, lang=tts_lang)

        print("Saving audio file...")  # Add this line for debugging
        tts.save('output.mp3')
        print("Audio file saved successfully!")  # Add this line for debugging

    except Exception as e:
        print(f"Error in text_to_speech function: {e}")
        traceback.print_exc()  # Print full exception traceback
        raise  # Reraise the exception

# Streamlit app
def main():
    st.title("PDF Audiobook with Translation")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])
    
    if pdf_file is not None:
        st.success("PDF file uploaded successfully!")

        # Get user input for page number
        page_number = st.number_input("Enter Page Number", value=1, step=1, min_value=1, max_value=10000)

        # Extract text from the specified page
        text = extract_text_from_pdf(pdf_file, page_number)

        # Translation options
        st.subheader("Translation:")
        source_lang = st.selectbox("Select Source Language", ["en"])
        target_lang = st.selectbox("Select Target Language", ["hi"])

        # Translate the text using EngtoHindi
        if source_lang == "en" and target_lang == "hi":
            translated_text = translate_text_eng_to_hindi(text)
        else:
            translated_text = text

        # st.subheader("Translated Content:")
        # st.text(translated_text)

        # Play audio button
        if st.button("Play Audio"):
            try:
                # Convert text to speech using gTTS and get the audio stream
                text_to_speech(translated_text, lang=target_lang)  # Adjust the language as needed

                # Play the audio using Streamlit's audio widget
                st.audio('output.mp3', format='audio/mp3')

            except ValueError as e:
                st.warning(f"Unable to generate audio: {e}")

if __name__ == "__main__":
    main()
