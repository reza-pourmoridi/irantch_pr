from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup

import os
import shutil


def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"})

    # Read HTML content from the uploaded file
    html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    blog_section = soup.find("section", class_="blog")
    if blog_section:
        # Add the conditional block before and after the <section class="blog"> tag
        blog_section.insert_before('{if !empty($internalTours) || !empty($foreginTours)}')
        blog_section.insert_after('{/if}')

    replacement_data = {
        "__link__": "https://example.com",
        "__image__": "image_url.jpg",
        "__title__": "Sample Title",
        "__all_article__": "https://example.com/all_articles"
    }
    # Iterate through all strings and tag attributes
    for tag in soup.find_all():
        for attr, value in tag.attrs.items():
            if isinstance(value, str):
                for key, new_value in replacement_data.items():
                    tag[attr] = tag[attr].replace(key, new_value)

        for key, value in replacement_data.items():
            if tag.string and key in tag.string:
                tag.string = tag.string.replace(key, value)

    new_html_code = soup.prettify()

    # Save the modified HTML code to a new file with UTF-8 encoding
    modified_file_path = os.path.join('modular/uploads', 'modified5_' + file.filename)
    with open(modified_file_path, 'w', encoding='utf-8') as modified_file:
        modified_file.write(new_html_code)

    return jsonify({"message": "File uploaded and modified successfully"})


def initiation_progress():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    if 'project_name' not in request.form:
        return jsonify({"message": "No project name"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    create_folder_massage = create_folder(request.form['project_name'])
    copy_repeated_file_folders_massage = copy_repeated_file_folders(request.form['project_name'])
    return jsonify({"error": copy_repeated_file_folders_massage})

    # html_content = file.read()
    # soup = BeautifulSoup(html_content, 'html.parser')
    # blog_section = soup.find("section", class_="blog")
    # if blog_section:
    #     # separate blog section for sending to blog_module
    #     blog_module(blog_section)
    #
    # return jsonify({"message": "File uploaded and modified successfully"})


def create_folder(folder_name):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        files_directory = os.path.join(script_directory, 'files')  # Create a 'files' subdirectory
        folder_path = os.path.join(files_directory, folder_name)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder and any necessary parent folders
            return f'Folder "{folder_name}" created successfully in the "files" directory'
        else:
            return f'Folder "{folder_name}" already exists in the "files" directory'
    except Exception as e:
        return f'Error creating folder: {str(e)}'


def copy_repeated_file_folders(target_folder):
    try:
        source_folder = 'repeated_files'
        # Construct the full paths to the source and target directories
        source_directory = os.path.join(os.path.dirname(__file__), 'files', source_folder)
        target_directory = os.path.join(os.path.dirname(__file__), 'files', target_folder)

        # Ensure the source directory exists
        if not os.path.exists(source_directory):
            return f'Source directory "{source_directory}" does not exist.'

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Copy the entire contents of the source directory to the target directory
        shutil.copytree(source_directory, os.path.join(target_directory, os.path.basename(source_directory)))

        return f'Contents of "{source_folder}" copied successfully to "{target_folder}"'
    except Exception as e:
        return f'Error copying directory contents: {str(e)}'

def create_file(folder_file_path):
    # create folders and files and upload fill in target files and folders
    return 'massage'


def blog_module(blog_section):
    # modulation the passed section
    blog_section.insert_before('{if !empty($internalTours) || !empty($foreginTours)}')
    blog_section.insert_after('{/if}')

    blog_replacement_data = {
        "__link1__": "https://example.com",
        "__link__": "https://example.com",
        "__image__": "image_url.jpg",
        "__title__": "Sample Title",
        "__all_article__": "https://example.com/all_articles"
    }
    # Iterate through all strings and tag attributes
    for tag in blog_section.find_all():
        for attr, value in tag.attrs.items():
            if isinstance(value, str):
                for key, new_value in blog_replacement_data.items():
                    tag[attr] = tag[attr].replace(key, new_value)

        for key, value in blog_replacement_data.items():
            if tag.string and key in tag.string:
                tag.string = tag.string.replace(key, value)

    new_html_code = blog_section.prettify()
    create_file(new_html_code)
