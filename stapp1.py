from django.http import JsonResponse
import os
import multiprocessing
from bs4 import BeautifulSoup
import urllib.request
from xhtml2pdf import pisa
import shutil
import streamlit as st
from io import BytesIO
from urllib.error import URLError

def convert_to_pdf(input_file):
    _, file_extension = os.path.splitext(input_file)
    val = file_extension.lower()
    if val == '.mhtml' or val == '.html' or val == '.htm' or val == '.igs':
        url = f"file:///{os.path.abspath(input_file)}"
        try:
            response = urllib.request.urlopen(url)
            soup = BeautifulSoup(response.read(), "html.parser")
            data = soup.find_all()
            output_file = BytesIO()
            html = "<html><head><meta charset='UTF-8'></head><body>"
            for d in data:
                html += str(d)
            html += "</body></html>"
            pisa.CreatePDF(html, dest=output_file)
            print(f"File converted: {input_file}")
            response.close()
            return output_file.getvalue()
        except URLError as e:
            print(f"URLError occurred: {e}")
            return None

    elif val == '.pdf':
        with open(input_file, "rb") as f:
            return f.read()

def main():
    st.title("File Conversion App")

    # Get input file from the user
    uploaded_file = st.file_uploader("Upload File")

    # Convert file to PDF and display download link
    if uploaded_file is not None:
        converted_file = convert_to_pdf(uploaded_file.name)
        if converted_file is not None:
            st.download_button("Download Converted File", converted_file, file_name="converted.pdf")
        else:
            st.warning("Failed to convert the file.")

if __name__ == '__main__':
    main()
