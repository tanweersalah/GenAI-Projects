import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") 


model = ChatGroq(model="llama3-70b-8192")




parser = StrOutputParser()





def translate_text(text_to_translate, source_language, target_language):
    system_message = f"Translate the following sentences from {source_language} to {target_language}"
    prompt = ChatPromptTemplate.from_messages({
    ("system",system_message ),
    ("human", "{input}")
    })

    chain = prompt|model|parser
    return chain.invoke(text_to_translate)


# Streamlit app UI
def main():
    st.title("Language Translation App")
    st.markdown("""
    <style>
    
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stTextInput input {
        background-color: #e8f0fe;
        border: none;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.subheader("Enter Text to Translate")
    text_to_translate = st.text_area("Text", height=150)
    
    st.subheader("Select Source and Target Languages")
    source_language = st.selectbox("Source Language", ["English", "Spanish", "French", "German", "Chinese", "Japanese"])
    target_language = st.selectbox("Target Language", ["German", "Spanish", "French", "English", "Chinese", "Japanese"])
    
    if st.button("Translate"):
        translated_text = translate_text(text_to_translate, source_language, target_language)
        st.subheader("Translated Text")
        st.text_area("", translated_text, height=150)

if __name__ == "__main__":
    main()