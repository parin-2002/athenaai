# Athena AI - Project README

## Project Overview

During the master’s program, developed an RAG(Retrieval Augmented Generation) app where students
can upload their notes, chat, and learn more with AI.
Build with Python, LangChain, ChromaDB, Gemini, and GPT-3.5 models

## Local Setup Instructions

### Prerequisites

We recommend using Anaconda to manage the virtual environment. If you do not have Anaconda installed, you can download it from the following links:

- [Windows](https://docs.anaconda.com/free/anaconda/install/windows/)
- [MacOS](https://docs.anaconda.com/free/anaconda/install/mac-os/)
- [Linux](https://docs.anaconda.com/free/anaconda/install/linux/)

### Steps to Run the Project Locally

1. **Open Anaconda PowerShell Prompt**

   After installing Anaconda, locate and open the “Anaconda PowerShell Prompt” on your system.

2. **Download and Unzip the Project**

   Download the zip file of our project and unzip it. Locate the folder where you have downloaded and unzipped our project.

3. **Create a Virtual Environment**

   Navigate to the project directory and create a virtual environment using the following commands:
   ```sh
   conda create -p venv python=3.10
   ```

   Type `y` when prompted to proceed.

4. **Activate the Virtual Environment**

   Activate the virtual environment with the following command:
   ```sh
   conda activate .\venv\
   ```

5. **Install Required Modules**

   Install the necessary Python modules using the `requirements.txt` file:
   ```sh
   pip install -r requirements.txt
   ```

6. **Run the Application**

   Finally, run the application using the following command:
   ```sh
   streamlit run .\1_QA.py
   ```

### Test Documents

Test documents are available in the "Test Document" folder within the "project_code" directory for your reference. You can utilize these documents for testing purposes or you may upload additional PDF or Word files as needed.


---

We hope you find our project helpful and easy to use. Thank you for choosing Athena AI!
