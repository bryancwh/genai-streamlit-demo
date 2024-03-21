import streamlit as st #all streamlit commands will be available through the "st" alias
import text_lib as glib #reference to local lib script
from io import StringIO

#
st.set_page_config(page_title="AWS Document GenAI Audit Checker") #HTML title
st.title("AWS Document GenAI Audit Checker") #page title

from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

#pdf
uploaded_file = st.file_uploader("Choose a file")
uploaded_file_string = ""

if uploaded_file is not None:
    # reader = PdfReader(uploaded_file.getvalue())
    pdfReader = PdfReader(BytesIO(uploaded_file.getvalue()))
    # printing number of pages in pdf file
    count = len(pdfReader.pages)
    uploaded_file_string = ""
    
    for i in range(count):
        page = pdfReader.pages[i]
        text = page.extract_text()
        uploaded_file_string += text
        # st.write(page)
        
    print("upload pdf complete!")
    st.write(f"Scanned {count} document pages")

#
prompt_template_default_string = """The following is a friendly conversation between a human and an AI.

The AI is a compliance agent and checks the a word document to see if it meets the compliance requirements."""

with st.expander("Prompt Engineering Template"):
    prompt_template = st.text_area("Prompt Template",prompt_template_default_string, label_visibility="visible",height = 150)

input_text = st.text_area("Input text", label_visibility="collapsed") #display a multiline text box with no label
go_button = st.button("Go", type="primary") #display a primary button

#
if go_button: #code in this if block will be run when the button is clicked
    
    with st.spinner("Working..."): #show a spinner while the code in this with block runs
        response_content = glib.get_text_response(prompt_content = prompt_template, uploaded_content = uploaded_file_string,input_content=input_text) #call the model through the supporting library
        
        st.write(response_content) #display the response content
