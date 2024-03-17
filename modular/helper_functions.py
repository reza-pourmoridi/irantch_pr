from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs
import zipfile
from collections import OrderedDict
import traceback
from difflib import SequenceMatcher
import socket

requests.packages.urllib3.disable_warnings()


def item_numbers(section, pattern):
    numbers = []
    elements = section.find_all(class_=pattern)
    for element in elements:
        match = pattern.search(element.get('class')[0])
        if match:
            number = match.group(1)
            numbers.append(number)

    return numbers

def item_strings(section, pattern):
    strings = []
    elements = section.find_all(class_=pattern)
    return f'{section}'
    for element in elements:
        match = pattern.search(element.get('class')[0])
        if match:
            string = element.get('class')[0]
            strings.append(string)

    return strings


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

def unzip_to_folder(folder_path, zip_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        return  f"The folder {folder_path} does not exist."

    # Empty the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return f'Failed to delete {file_path}. Reason: {e}'

    # Unzip the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
       result = zip_ref.extractall(folder_path)
    return result

def is_zip(file_path):
    return zipfile.is_zipfile(file_path)

def create_folder(folder_name , path = False):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        files_directory = os.path.join(script_directory, 'final_files')  # Create a 'final_files' subdirectory
        if path:
            files_directory = path  # Create a 'final_files' subdirectory
        folder_path = os.path.join(files_directory, folder_name)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder and any necessary parent folders
            return folder_path
        else:
            return f'Folder "{folder_name}" already exists in the "final_files" directory'
    except Exception as e:
        return f'Error creating folder: {str(e)}'


def read_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

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
        target_directory = os.path.join(os.path.dirname(__file__), 'final_files', target_folder)

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


def write_text_in_path(path, text):
    mainpage_tpl_path = os.path.join(path, 'mainPage.tpl')
    with open(mainpage_tpl_path, 'w') as mainPage_tpl_file:
        mainPage_tpl_file.write(text)

def replace_attribute(section, class_name, attr, value):
    for tag in section.find_all(class_=class_name):
        if attr != 'string':
            tag[attr] = value
        else:
            tag.string = value

def replace_attribute_by_tag(section, tag_name, attr, value):
    for tag in section.find_all(tag_name):
        if attr != 'string':
            tag[attr] = value
        else:
            tag.string = value


def add_class_to_elements(section, class_name, new_class):
    for tag in section.find_all(class_=class_name):
        # Get the current classes
        current_classes = tag.get('class', [])

        # Add the new class
        if new_class not in current_classes:
            current_classes.append(new_class)

        # Update the class attribute
        tag['class'] = current_classes

def remove_class_from_elements(section, class_name, class_to_remove):
    for tag in section.find_all(class_=class_name):
        # Get the current classes
        current_classes = tag.get('class', [])

        # Remove the class if it exists
        if class_to_remove in current_classes:
            current_classes.remove(class_to_remove)

        # Update the class attribute
        tag['class'] = current_classes


def remove_tag_from_soup_object(content, tag_name):
    tag = content.find(tag_name)
    tag_content = tag.decode_contents() if tag else None
    soup = BeautifulSoup(f'{tag_content}', 'html.parser')
    return soup





def add_value_to_attribute(section, class_name, attr, value):
    for tag in section.find_all(class_=class_name):
        if attr != 'string':
            if tag.get(attr) is not None:
                tag[attr] += value
        else:
            if tag.string is not None:
                tag.string += value

def comapre_append_list(editing_array, compare_array):
    result = []
    for item in editing_array:
        if item in compare_array:
            result.append(item)
    return result

def delete_assames(editing_array, compare_array):
    result = []
    for item in editing_array:
        if item not in compare_array:
            result.append(item)
    return result

def turn_to_styl_links_assames(links):
    result = ''
    for item in links:
        result = result + '<link rel="stylesheet" href="project_files/' + item + '">'
    return result

def turn_to_script_links_assames(links):
    result = ''
    for item in links:
        if item:
            result = result + '<script src="project_files/' + item + '"></script>'
    return result


def replace_attribute_by_text(section, target_text, attr, value):
    for tag in section.find_all(text=lambda text: text and target_text.strip() == text.strip()):
        parent_tag = tag.find_parent()
        if parent_tag:
            if attr == 'href':
                if parent_tag.name == 'a':
                    parent_tag[attr] = value
            elif attr != 'string':
                parent_tag[attr] = value
            else:
                parent_tag.string = value


def changing_numbers_to_array_elements(array, num):
    for key, val in array.items():
        array[key] = val.format(num)
    return array

def add_before_after(section, class_name, before, after):
    complex_element = section.find(class_=class_name)
    if complex_element:
        inner_html = f'{before}\n{complex_element}\n{after}'
        complex_element.replace_with(BeautifulSoup(inner_html, 'html.parser'))


def clean_serialize_string(string):
    string = string.replace("https://192.168.1.100/gds/view/WW12/", "")
    string = string.replace("http://192.168.1.100/gds/view/WW12/", "")
    string = string.replace("http://192.168.1.100/gds/view/WW12/", "")
    string = BeautifulSoup(string, 'html.parser')
    string = string.prettify()
    string = string.replace("https", "")
    string = string.replace("http", "")
    string = string.replace("/>", ">")
    string = string.replace("  ", "")
    string = string.replace("", "")
    string = string.replace("</img>", "")
    string = string.replace("/>", ">")
    string = string.replace("&gt;", ">")
    string = string.replace("&lt;", "<")
    return string


def clean_links(string):
    if string:
        pattern = re.compile(r'192\.168\.1\.100/gds/view/[^/]+/')
        string = pattern.sub('', string)
        string = string.replace("http://", "")
        string = string.replace("https://", "")
    else:
        string = ''
    return string

def clean_links_js(string):
    if string:
        pattern = re.compile(r'192\.168\.1\.100/gds/view/[^/]+/')
        string = pattern.sub('', string)
        string = string.replace("http://", "")
        string = string.replace("https://", "")
    else:
        string = ''
    return string

def unit_test_clean_string(string):
    string = BeautifulSoup(string, 'html.parser')
    string = string.prettify()
    pattern = re.compile(r'__i_modular_nc_item_class_[0-9]+')
    string = pattern.sub('', string)
    pattern = re.compile(r'192\.168\.1\.100/gds/view/[^/]+/project_files')
    string = pattern.sub('', string)
    string = string.replace("https://192.168.1.100/gds/view/WW12/", "")
    string = string.replace("http://192.168.1.100/gds/view/WW12/", "")
    string = string.replace("http://192.168.1.100/gds/view/WW12/", "")
    string = BeautifulSoup(string, 'html.parser')
    string = string.prettify()
    string = string.replace("http://", "")
    string = string.replace("https://", "")
    string = string.replace("project_files", "")
    string = string.replace("None", "")
    string = string.replace("/>", ">")
    string = string.replace("  ", "")
    string = string.replace("</img>", "")
    string = string.replace("/>", ">")
    string = string.replace("&gt;", ">")
    string = string.replace("&lt;", "<")
    return string

def serialize_string(string):
    string = string.replace(" ", "")
    string = string.replace("<html>", " ")
    string = string.replace("</html>", " ")
    string = string.replace("<body>", " ")
    string = string.replace("</body>", " ")
    string = string.replace(" ", "")
    return string

def search_box_clean_serialize_string(string):
    string = string.replace("&gt;", ">")
    string = string.replace("&lt;", "<")
    string = string.replace('''[" ''', "['")
    string = string.replace(''' "="" ''', " ")
    string = string.replace('''}'=">{''', '''}">{''')
    string = string.replace('''}'="">{''', '''}">{''')
    string = string.replace(""""{$country[">""", """"{$country['id']}">""")
    string = string.replace("""id']}'=""""", " ")

    return string

def icons_clean_serialize_string(string):
    string = string.replace(r'\"', "'")
    return string


def value_exists_in_dict_values(dictionary, value ):
    for sub_dict in dictionary.values():
        if value in sub_dict.values():
            return True
    return False

def return_file_in_same_section(classes, moduls_array, index = '1'):
    final_classes = []
    for c in classes:
        if value_exists_in_dict_values(moduls_array, c):
            final_classes.append(c)

    final_names = []
    for key, val in moduls_array.items():
        if val['class'] in final_classes:
            final_names.append(val['file'])

    file_name = ''
    for item in final_names:
        if item != final_names[0]:
            file_name = file_name + '-' + item
        else:
            file_name =  item

    if remove_repeated_words(file_name) == 'search-box':
        return remove_repeated_words(file_name)
    else:
        return remove_repeated_words(file_name) + '-' + index


def remove_repeated_words(s):
    return "-".join(OrderedDict.fromkeys(s.split("-")))

def check_if_section_built(project_path ,file_name ,section):
    if os.path.exists(project_path + '/include_files/' + file_name + '.tpl'):
        section = f"{read_file(project_path + '/include_files/' + file_name + '.tpl')}"
        section = BeautifulSoup(section, 'html.parser')

    return section

def if_dosnt_exist_create_else_add(file_path, file_name ,string):
    if os.path.exists(file_path + '/' + file_name + '.tpl'):
        section = f"{read_file(file_path + '/' + file_name + '.tpl')}"
        return create_file(f'{section}' + string, file_path, file_name, 'tpl')

    return create_file(string, file_path, file_name, 'tpl')

def create_or_replace_file(file_path, new_content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
            return (f"File '{file_path}' created or content replaced successfully.")
    except PermissionError:
        return (f"Permission denied. Check if you have write permissions for '{file_path}'.")
    except Exception as e:
        return (f"An error occurred: {e}")


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


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False



def copy_file(source_file, destination_folder):
    # Check if the source file exists
    if not os.path.exists(source_file):
        return("Source file does not exist:", source_file)


    # Check if the destination folder exists, if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy the file to the destination folder
    try:
        shutil.copy(source_file, destination_folder)
        return ("File copied successfully to:", destination_folder)
    except Exception as e:
        return ("An error occurred while copying the file:", str(e))



def upload():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})


    file = request.files['file']

    if not is_zip(file):
        return jsonify({"message": "file format must be zip"})

    if file.filename == '':
        return jsonify({"message": "No selected file"})

    files_directory = os.path.dirname(__file__)  # Get the directory of the script
    files_directory = os.path.join(files_directory, 'files')  # Create a 'final_files' subdirectory
    files_directory = os.path.join(files_directory, 'repeated_files')  # Create a 'final_files' subdirectory
    files_directory = os.path.join(files_directory, 'project_files')  # Create a 'final_files' subdirectory
    unzip_to_folder(files_directory, file)
    return jsonify({"message": 'استایل های پروژه بارگذاری شدند.'})



def get_online_html():
    url = "http://192.168.1.100/"

    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            html_content_online = response.text
            if "i_modular_modulation" in html_content_online:
                soup = BeautifulSoup(html_content_online, 'html.parser')
                return soup
            else:
                return "خطایی پیش آمده و دیتایی نمایش ندارد1."

        else:
            return f"خطایی در گرفتن اطلاعات پیش آمده2.{response.status_code}"


    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در گرفتن اطلاعات پیش آمده3.: {trace}"
        return error_message



def compare_html_strings(soup1, soup2):
    similarity_percentage = similarity(soup1, soup2)
    if similarity_percentage > 98:
        return True
    return False


def special_items(data, item):
    if item == '''{$item['min_price']['discountedMinPriceR']|number_format}''':
        return format(data['min_price']['discountedMinPriceR'], ',')
    if item == '''{$smarty.const.ROOT_ADDRESS}/detailTour/{$item['id']}/{$item['tour_slug']}''':
        return '192.168.1.100/gds/fa/detailTour/' + data['id'] + '/' + data['tour_slug']

    if item == '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$item['tour_pic']}''':
        return '192.168.1.100/gds/pic/reservationTour/' + data['tour_pic']

    if item == '''{assign var="year" value=substr($item['start_date'], 0, 4)}
                                {assign var="month" value=substr($item['start_date'], 4, 2)}
                                {assign var="day" value=substr($item['start_date'], 6)}
                                {$year}/{$month}/{$day}
                                ''':
        formatted_date = f"{data['start_date'][:4]}/{data['start_date'][4:6]}/{data['start_date'][6:]}"
        return formatted_date

    return False



def get_element_data_key_by_pattern(data,pattern, item):
    valuefinal = ''
    match_combined = re.search(pattern, item)
    special_items_val = special_items(data, item)
    if special_items_val:
        item = str(special_items_val)

    elif match_combined:
        item_key_1 = match_combined.group(2)

        if item_key_1:
            valuefinal = data.get(item_key_1, '')

        item_key_2 = match_combined.group(3)
        if item_key_2:
            valuefinal = data.get(item_key_1, {}).get(item_key_2, '')

        item_key_3 = match_combined.group(4)
        if item_key_3:
            valuefinal = data.get(item_key_1, {}).get(item_key_2, {}).get(item_key_3, '')

        # Convert pattern_str and valuefinal to strings before using them
        pattern_str = str(re.escape(match_combined.group(0)))
        valuefinal = str(valuefinal)

        # Replace the matched pattern with valuefinal
        item = re.sub(pattern_str, valuefinal, item)

    return item


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


def extract_json_data_from_url(class_name, url = 'http://192.168.1.100/gds/fa/modular_data'):
    try:
        json = send_request_with_error_handling(class_name,url)
        return f'{json}'
        if json is not None and json:
            return f'{json}'
        return 'error for updating unit_test_data folder'
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str



def get_general_data(unique_key):
    try:
        general_data = []
        json_html = extract_json_data_from_url(unique_key)
        json_html = BeautifulSoup(json_html, 'html.parser')
        json_element = json_html.find(class_='data_modular')
        if json_element:
            json_string = json_element.get_text()
            general_data = json.loads(json_string)
        else:
            return 'data dosent loaded'
        return general_data
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def check_url_real(urls):
    broken_links = []
    for url in urls:
        if url.startswith('http://') or url.startswith('https://'):
            try:
                response = requests.head(url, verify=False)
                if response.status_code == 200:
                    print(f"{url} exists and is reachable.")
                else:
                    broken_links.append(url)
            except (requests.exceptions.ConnectionError, socket.gaierror) as e:
                print(f"Error occurred while accessing {url}: {e}")
                broken_links.append(url)
    if broken_links:
        return 'These links are corrupted: ' + ', '.join(broken_links)
    return False


def similarity(string1, string2):
    matcher = SequenceMatcher(None, string1, string2)
    return matcher.ratio() * 100