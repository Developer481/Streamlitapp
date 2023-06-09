import streamlit as st
from pdfgen import Topdftool
from django.http import JsonResponse


@st.cache(show_spinner=False)
def scrape_files(input_folder_path, output_folder_path):
    # Call the scrape_files function with the input and output folder paths
    Topdftool.scrape_files(input_folder_path, output_folder_path)

@st.cache(show_spinner=False)
def scrape_api():
    input_folder_path = st.text_input("Input Folder Path")
    output_folder_path = st.text_input("Output Folder Path")

    if st.button("Scrape"):
        scrape_files(input_folder_path, output_folder_path)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'waiting'})


def main():
    st.header("API Demo")
    response = scrape_api()
    st.json(response)

if __name__ == "__main__":
    main()
