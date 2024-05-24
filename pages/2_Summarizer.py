# Import required modules
import streamlit as st
from modules.class_manager import getManager

def summarizer():
    manager=getManager()
    summary=""

    st.title("Generate a Summary for Your Document 📄")

    st.info("""
            
            
            Follow these steps to generate a summary for your selected file:
            
            1. Select the File on the Left Side:
            Choose one file from the list provided on the left sidebar to summarize. 
            2. Confirm Selection:
            Ensure the selected file is displayed under "Selected file:".
            3. Generate Summary:
            Once the file is selected, the summarizer will automatically process the document and generate a summary.

            """)

    with st.sidebar:
        st.title("Select one file:")
        if manager!=None:
            file_name=st.sidebar.radio("Select one file to summarize",manager.file_names,index=None)
            st.write("Selected file: ", file_name)
            if file_name:
                with st.spinner("Processing..."):
                    summary=manager.write_summary(file_name)
                # Success message
                st.success("Done")
        else:
            st.warning("Please upload a file before proceeding!")

    if summary:
        st.write(summary['output_text'])


summarizer()