import streamlit as st
import nbformat
from nbconvert import HTMLExporter
import os

def main():
    st.title("Metodos de Analise Pojeto_2")

    # File uploader
    uploaded_file = st.file_uploader("Suba o arquivo Jupiter Notebook para vizualizar o trabalho a seguir", type="ipynb")
    
    if uploaded_file is not None:
        # Read the file
        content = uploaded_file.read()
        
        # Parse the notebook
        notebook = nbformat.reads(content, as_version=4)
        
        # Convert to HTML
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'basic'
        
        (body, _) = html_exporter.from_notebook_node(notebook)
        
        # Display the HTML
        st.components.v1.html(body, scrolling=True, height=600)

if __name__ == "__main__":
    main()