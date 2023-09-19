from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup

import os


def run_app():
    # Add your logic for the '/recom-back-end' route here
    response = {"message": "This is the modular back-end."}
    return jsonify(response)

def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"})

    # Read HTML content from the uploaded file
    html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    replacement_data = {
        "__link__": "https://example.com",
        "__image__": "image_url.jpg",
        "__title__": "Sample Title",
        "__all_article__": "https://example.com/all_articles"
    }

    blog_section = soup.find("section", class_="blog")
    if blog_section:
        # Add the conditional block before and after the <section class="blog"> tag
        blog_section.insert_before('{if !empty($internalTours) || !empty($foreginTours)}')
        blog_section.insert_after('{/if}')

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

