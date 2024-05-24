# Import required modules
# import sqlite3
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
import google.generativeai as genai
from modules.class_manager import getManager, setManager

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI model
openai_model = OpenAI(api_key=openai_api_key)

# Retrieve the Google API key from the environment variables
os.getenv("GOOGLE_API_KEY")
# Configure the Generative AI module with the retrieved Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def main():
    # Set the page configuration
    st.set_page_config("Athena")

    # Display the title and header
    st.title("Hi, I am Athena. How can I help you?  🤖")
    st.header("Ask Athena questions about your uploaded course materials (PDF and Word documents) 📚.")

    # Display information message
    st.info(""" Athena allows you to ask questions based on the content of your PDF and WORD files and get a concise response from Athena. Here's how to use it:
            
    1. Select Model: Default model is Gemini. We recommend using Gemini. If it doesn't work well, you can switch to the OpenAI model from the side menu. 
    2. Upload Your Files:
            Drop your PDF and/or Word files into the designated area on the left sidebar. 
    3. Submit and Process:
            Click the "Submit & Process" button to start processing your uploaded files.
    4. Ask Your Question:
            Enter your question in the text input field below.
    5. Get Your Answer:
            Click the "Get Answer" button to receive a response generated from the content of your files.
            
    Additionally, you can:
    - Click on the "Summarizer" on the left sidebar to generate a summary of the uploaded files.
    - Click on the "MCQs Generator" on the left sidebar to generate a set of multiple-choice questions based on the content of the files.
    """)
    # Display an information message
    st.warning("""Note: The Gemini and OPENAI response may provide more general information and inaccurate, while the response based on your files will be specific to the content you uploaded. 
               Additionally, include notes to enhance learning and outcomes for better understanding!""")
    st.warning("""You can switch the model while uploading a file. After the file is uploaded, switching is not possible. Since the OpenAI model is not our primary model, we haven't implemented dynamic switching throughout the app.""",icon="⚠️")
    

    # Input field for the user to ask a question
    user_question = st.text_input("Ask a Question: What is ...")

    #get answer
    if st.button("Get Answer"):
        # If the user has asked a question
        if user_question:
           manager=getManager()
           if manager!=None:
            #    ans= manager.answer_question(user_question)
               ans=manager.ensemble_qa(user_question)
               # Process the user's question and display the response
            #    st.write("### **Reply**:  \n" + ans['result'])
               st.write("### **Ensemble Reply**:  \n" + ans['result'])
           else:
               st.warning("Please upload a file before proceeding!")
            
    # Sidebar section
    with st.sidebar:

        #select model
        model_name = st.selectbox("Which model do you want to use?",
                              ("gemini-pro", "gpt-3.5-turbo-1106"))
        st.write("You selected:", model_name)

        # Display the sidebar title
        st.title("Menu:")
        # File uploader for uploading files
        docs = st.file_uploader("Upload your PDF Files or Word documents and Click on the Submit & Process Button", type=['pdf','docx'], accept_multiple_files=True)
        # Button to trigger processing of uploaded files
        if st.button("Submit & Process", disabled=not bool(docs)):
            # Processing indicator
            with st.spinner("Processing..."):
                # Process Documents:  
                manager=setManager()
                manager.manage_document_extractor(docs)
                manager.manage_chroma_vector_store()
                manager.manage_question_answer_chain(model_name)

            # Success message
            st.success("Done")
                

if __name__ == "__main__":
    main()



# chromadb==0.3.29
# chromadb==0.5.0

        