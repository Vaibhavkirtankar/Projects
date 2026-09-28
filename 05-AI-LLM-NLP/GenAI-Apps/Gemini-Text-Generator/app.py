from dotenv import load_dotenv
load_dotenv()#Used to load all environment variables

import streamlit as st 
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))#Loading Google API Key

# Function to load Gemini Pro Model and Get responses 

model=genai.GenerativeModel("gemini-1.5-pro")

def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

# Initialize Streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

input=st.text_input("Input: ",key="Input")
submit=st.button("Ask the Question")
    
    
#When Submit button is clicked    

if submit:
    response=get_gemini_response(input)
    st.write(response)