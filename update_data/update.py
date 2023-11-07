import requests
import os
from bs4 import BeautifulSoup
import re
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_folder(folder_name):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        files_directory = os.path.join(script_directory, folder_name)  # Create a 'files' subdirectory
        # Check if the folder already exists
        if not os.path.exists(files_directory):
            os.makedirs(files_directory)  # Create the folder and any necessary parent folders
            return files_directory
        else:
            return f'Folder "{folder_name}" already exists in the "files" directory'
    except Exception as e:
        return f'Error creating folder: {str(e)}'

def create_file(content, path, file_name, file_format):
    try:
        # Combine the provided path and file name with format to create the full file path
        full_file_path = os.path.join(path, f'{file_name}.{file_format}')

        # Write the content to the file
        with open(full_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return f'File "{full_file_path}" created successfully'
    except Exception as e:
        return f'Error creating file: {str(e)}'


def extract_json_data_from_url(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, verify=False)  # Setting verify=False for self-signed certificates
        response.raise_for_status()  # Check for any request errors

        # Parse the HTML content with BeautifulSoup and prettify it
        soup = BeautifulSoup(response.text, 'html.parser').prettify()
        soup = BeautifulSoup(soup, 'html.parser')

        # Initialize an empty dictionary to store the JSON data
        json_data_dict = {}

        # Find all div elements and extract their class names
        class_names = ['top_bar_data', 'top_bar_name_data', 'menu_data','banners_data','article_data','news_data','social_data','about_data','address_data','mobile_data']



        unit_test_data_path = create_folder('unit_test_data')

        # Find all elements with class 'top_bar_data', 'top_bar_name_data', and 'menu_data'
        for class_name in class_names:
            element = soup.find('div', class_=class_name)
            if element:
                test = create_file(element.text, unit_test_data_path, class_name, 'json')
                print(test)


        return true

    except Exception as e:
        return str(e)

# Replace 'https://192.168.1.100/' with your desired URL
url = 'https://192.168.1.100/'
result = extract_json_data_from_url(url)



