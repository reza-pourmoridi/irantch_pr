from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs


def item_numbers(section, pattern):
    numbers = []
    elements = section.find_all(class_=pattern)
    for element in elements:
        match = pattern.search(element.get('class')[0])
        if match:
            number = match.group(1)
            numbers.append(number)
    return numbers


def replace_placeholders_recursive(tag, replacement_data):
    # Iterate over the tag's attributes
    for attr, value in tag.attrs.items():
        if isinstance(value, str):
            # Replace keys in attribute values
            for key, new_value in replacement_data.items():
                tag[attr] = tag[attr].replace(key, new_value)

    # Iterate over the replacement_data
    for key, value in replacement_data.items():
        # Replace keys in the tag's string content
        if tag.string and key in tag.string:
            tag.string = tag.string.replace(key, value)

    # Recursively process the parent tags
    if tag.parent:
        replace_placeholders_recursive(tag.parent, replacement_data)

    # Replace entire tag if it's in replacement_data
    if tag.decode() in replacement_data:
        new_tag = BeautifulSoup(replacement_data[tag.decode()], 'html.parser')
        tag.replace_with(new_tag)


def replace_placeholders(section, replacement_data):
    # Iterate over all tags in the section
    for tag in section.find_all():
        replace_placeholders_recursive(tag, replacement_data)

    section_final_content = section.prettify()
    return section_final_content


def create_folder(folder_name):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        files_directory = os.path.join(script_directory, 'files')  # Create a 'files' subdirectory
        folder_path = os.path.join(files_directory, folder_name)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder and any necessary parent folders
            return folder_path
        else:
            return f'Folder "{folder_name}" already exists in the "files" directory'
    except Exception as e:
        return f'Error creating folder: {str(e)}'


def copy_directory_contents(source_directory, target_directory):
    try:
        # Ensure the source directory exists
        if not os.path.exists(source_directory):
            return f'Source directory "{source_directory}" does not exist.'

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Copy the entire contents of the source directory to the target directory
        for item in os.listdir(source_directory):
            source_item = os.path.join(source_directory, item)
            target_item = os.path.join(target_directory, item)

            if os.path.isdir(source_item):
                # Recursively copy subdirectories and their contents
                copy_directory_contents(source_item, target_item)
            else:
                # Copy individual files
                shutil.copy2(source_item, target_item)

        return f'Contents of "{source_directory}" copied successfully to "{target_directory}"'
    except Exception as e:
        return f'Error copying directory contents: {str(e)}'


def copy_repeated_file_folders(target_folder):
    try:
        source_folders = ['repeated_files']

        # Construct the full paths to the source and target directories
        target_directory = os.path.join(os.path.dirname(__file__), 'files', target_folder)

        # Ensure the target directory exists
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        for source_folder in source_folders:
            source_directory = os.path.join(os.path.dirname(__file__), 'files', source_folder)

            # Skip source directories that don't exist
            if not os.path.exists(source_directory):
                continue

            # Copy the entire contents of the source directory to the target directory
            copy_directory_contents(source_directory, target_directory)

        return f'Contents of source folders copied successfully to "{target_folder}"'
    except Exception as e:
        return f'Error copying source folders: {str(e)}'


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


def write_text_in_path(path, text):
    mainpage_tpl_path = os.path.join(path, 'mainPage.tpl')
    with open(mainpage_tpl_path, 'w') as mainPage_tpl_file:
        mainPage_tpl_file.write(text)


def replace_attribute(section, class_name, attr, value):
    for tag in section.find_all():
        if attr != 'string':
            if class_name in tag.get('class', []):
                # Replace the src attribute for tags with class __image__
                tag[attr] = value  # Replace with desired code
        else:
            if class_name in tag.get('class', []):
                # Replace the src attribute for tags with class __image__
                tag.string = value  # Replace with desired code


