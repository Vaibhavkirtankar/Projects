from dotenv import load_dotenv
load_dotenv()  # Used to load all environment variables
from PIL import Image
import streamlit as st
import os
import google.generativeai as genai
import io
import base64

st.set_page_config(page_title="Image Demo", layout="centered")

# Here I am Using a Simple Blue theme.
st.markdown("""
    <style>
        body {
            background-color: #e0f2f1;  /* Light Blue Background */
        }
        .stButton button {
            background-color: #00796b;  /* Blue Button */
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #004d40;  /* Darker Blue Hover */
        }
        .stTextInput input {
            background-color: #b2dfdb;  /* Light Blue Input */
            border-radius: 8px;
        }
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stHeader {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 32px;
            color: #00796b;
        }
        .stSubheader {
            font-size: 28px;
            color: #004d40;
        }
    </style>
""", unsafe_allow_html=True)

# Loading Our Google API Key from .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  

# Loading Gemini Pro Model and Get responses 
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content({
            "parts": [
                {"text": input},  # Add the input text part
                {"inline_data": {
                    "mime_type": "image/png",  # Assuming the uploaded image is PNG
                    "data": image  # Image data in base64 format
                }}
            ]
        })
    else:
        response = model.generate_content({
            "parts": [
                {"text": ""},  # Empty text if no input is provided
                {"inline_data": {
                    "mime_type": "image/png",  # Assuming the uploaded image is PNG
                    "data": image  # Image data in base64 format
                }}
            ]
        })
    return response.text

# Initialising the StreamLit App
st.header("Gemini LLM Image Demo")

input = st.text_input("Enter description or question:", key="Input")

# Creating an upload button to upload Images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# This block of code is used If image is uploaded and then display it
image = None
if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Display the image with a border and shadow
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Here we Convert image to base64 for passing to the model
def convert_image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")  # or "JPEG" based on the uploaded image format
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

submit = st.button("Tell me about this image")

# If submit button is clicked
if submit:
    if image:  
        image_base64 = convert_image_to_base64(image)
        response = get_gemini_response(input, image_base64)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.error("Please upload an image before submitting.")
