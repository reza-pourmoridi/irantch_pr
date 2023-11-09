import requests
import os
from bs4 import BeautifulSoup
import re
import json
import urllib3
import shutil


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

def delete_folder(folder_name):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        folder_path = os.path.join(script_directory, folder_name)

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Recursively delete the folder and its contents
            return f'Folder "{folder_name}" and its contents have been deleted'
        else:
            return f'Folder "{script_directory + "/" + folder_name}" does not exist'

    except Exception as e:
        return f'Error deleting folder: {str(e)}'

def create_file(content, path, file_name, file_format):
    try:
        # Combine the provided path and file name with format to create the full file path
        full_file_path = os.path.join(path, f'{file_name}.{file_format}')

        # Write the content to the file
        with open(full_file_path, 'w') as file:
            file.write(content)

        return f'File "{full_file_path}" created successfully'
    except Exception as e:
        return f'Error creating file: {str(e)}'

def send_request_with_error_handling(class_name,url):
    try:
        data = {'class': class_name}
        response = requests.post(url, data=data, verify=False)  # Disable SSL certificate verification
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response data
        print(f"Successfully posted class: {class_name}")
        return response.text

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for class {class_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred for class {class_name}: {req_err}")

def extract_json_data_from_url(url):
    try:
        # Find all div elements and extract their class names
        class_names = ['top_bar_data', 'top_bar_name_data', 'menu_data','banners_data','article_data','news_data','social_data','about_data','address_data','mobile_data']

        delete_result = delete_folder('unit_test_data')
        print(delete_result)
        # unit_test_data_path = create_folder('unit_test_data')
        # for class_name in class_names:
        #     json = send_request_with_error_handling(class_name,url)
        #     if json is not None and json:
        #
        #         test = create_file(json, unit_test_data_path, class_name, 'json')
        #         print(test)


        return test

    except Exception as e:
        return str(e) + 'sdjfkl2'

extract_json_data_from_url('https://192.168.1.100/')


