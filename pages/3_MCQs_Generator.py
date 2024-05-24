import os
import json
import streamlit as st
from modules.class_manager import getManager
import traceback

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]

        #iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            options=[{"option": option, "value": option_value} for option, option_value in value["options"].items()]
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

with open(r"Response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)
    response_json= json.dumps(RESPONSE_JSON)

st.title("Real-Time MCQ Generator")

manager=getManager()
if manager!=None:
    st.info("""
            Follow these steps to create multiple-choice questions (MCQs) based on your selected file:
            
            1. Select a File:
            Click on the "Choose an option" dropdown menu under "Select one file" to select the document you want to generate MCQs from (e.g., TestDocument.pdf).
            2. Specify the Number of MCQs:
            Adjust the number of MCQs you want to create using the "+" or "-" buttons under "No. of MCQs."
            3. Insert Subject:
            Enter the subject or topic for the MCQs in the "Insert Subject" field.
            4. Select Complexity Level:
            Choose the desired complexity level for the questions from the "Complexity Level of Questions" dropdown menu.
            5. Create MCQs:
            After filling out all the required fields, click the "Create MCQs" button to generate the questions.
            """)
    
    st.warning("""Ensure all fields are filled in correctly before creating MCQs. Incomplete or incorrect information may result in errors or inaccurate question generation.""")

    with st.form("user_inputs"):
        file_name=st.multiselect("Select one file",manager.file_names, max_selections=1)
        mcq_count=st.number_input("No. of MCQs", min_value=1, max_value=10)
        subject=st.text_input("Insert Subject", max_chars=50)
        # tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")
        tone=st.multiselect("Complexity Level of Questions",["Simple","Median","Hard"], max_selections=1)
        button = st.form_submit_button("Create MCQs")

        if button and file_name and mcq_count and subject and tone:
            with st.spinner("Processing..."):
                try:
                    response=manager.mcq_generator(file_name[0],mcq_count,subject,tone[0],response_json)
                except Exception as e:
                    print(e)
                    st.info("try again something went wrong!")
                else:
                    if isinstance(response,dict):
                        quiz_json_start = response['quiz'].find('{')
                        quiz_json_end = response['quiz'].rfind('}') + 1
                        quiz = response['quiz'][quiz_json_start:quiz_json_end]
                        if quiz is not None:
                            table_data=get_table_data(quiz)
                            if table_data is not None:
                                manager.mcqs=table_data
                            else:
                                st.error("Error in table data")
                        
                        else:
                            st.write(response)
                        
        else:
            st.warning("fill all info!")

else:
    st.warning("Please upload a file before proceeding!")

if manager!=None:
    if manager.mcqs!=None:
        for mcq in manager.mcqs:
            if st.radio(mcq['MCQ'],[val['value'] for val in mcq['Choices']],index=None , key=mcq['MCQ']):
                st.write("Correct :",mcq["Correct"])
    else:
        st.info("Fill above form to get quiz!")



    