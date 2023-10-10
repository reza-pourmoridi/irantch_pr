from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs



def initiation_progress():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    if 'project_name' not in request.form:
        return jsonify({"message": "No project name"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})



    project_path = create_folder(request.form['project_name'])
    copy_repeated_file_folders_massage = copy_repeated_file_folders(request.form['project_name'])

    # turn html to string
    html_content = file.read()
    # turn string to soup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # blog module
    blog_section = soup.find(class_="i_modular_blog")
    if blog_section:
        blog_module_massage = blog_module(blog_section,project_path)
        soup = BeautifulSoup(html_content, 'html.parser')
        blog_section = soup.find(class_="i_modular_blog")
        intial_blog_test_massage = initial_blog_test(blog_section)

    # tour module

    return jsonify({"message":  "<div style='color:green'> building blog section result =" + blog_module_massage + "- - - - <br><br>- - - - blog test result =" + intial_blog_test_massage + "</div>"})


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


def blog_module(blog_section, project_path):
    try:
        # create regex objects containing patterns of items classes
        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
        complex_items_numbers = []
        simple_items_numbers = []

        elements = blog_section.find_all(class_=complex_items_pattern)
        for element in elements:
            match = complex_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                complex_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")
        elements = blog_section.find_all(class_=simple_items_pattern)
        for element in elements:
            match = simple_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                simple_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")

        complex_items_numbers_max = max(complex_items_numbers)
        simple_items_numbers_max = max(simple_items_numbers)
        simple_items_numbers_min = min(simple_items_numbers)

        # Compare the maximum values and print the larger one
        if complex_items_numbers_max > simple_items_numbers_max:
            max_item_number = complex_items_numbers_max
        elif simple_items_numbers_max > complex_items_numbers_max:
            max_item_number = simple_items_numbers_max
        else:
            max_item_number = complex_items_numbers_max


        before_html = '''{assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>i_modular__max_limit0]}
                        {assign var='articles' value=$obj_main_page->articlesPosition($data_search_blog)}
                        {assign var='counter' value=0}
                        {assign var="article_count" value=$articles|count}
                        {if $articles}'''
        before_html = before_html.replace("i_modular__max_limit", max_item_number)

        after_html = '{/if}'
        before_foreach = '''{foreach $articles as $key => $article} {if $counter >= i_modular__min_for_limit and $counter <= i_modular__max_for_limit}'''
        before_foreach = before_foreach.replace("i_modular__min_for_limit", simple_items_numbers_min)
        before_foreach = before_foreach.replace("i_modular__max_for_limit", simple_items_numbers_max)

        after_foreach = '''{/if}{$counter = $counter + 1}{/foreach}'''

        for num in simple_items_numbers:
            blog_replacement_data = {
                "__airline__": '''{$article['link']}''',
                "__link__": '''{$article['link']}''',
                "__image__": '''{$article['image']}''',
                "__title__": '''{$article['title']}''',
                "__alt_article__": '''{$article['title']}''',
                '<span class="__date__">5 بهمن 1402</span>': '''{$article['created_at']}''',
                '<span class="__comments_number__">450</span>': '''{$article['comments_count']['comments_count']}''',
                'images/5497750661271-6.jpg': '''{$article['image']}''',
                '<span class="__title__">تایتل</span>': '''{$article['title']}'''
            }
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)

            # Check if it's the first simple element
            if num == simple_items_numbers[0]:
                # new_tag = BeautifulSoup(simple_element, 'html.parser')
                # simple_element = replace_placeholders(simple_element, {
                #     new_tag: f'{{if !empty($internalTours) || !empty($foreginTours)}}\n{new_tag}\n{{/if}}'})
                for tag in blog_section.find_all():
                    if tag.decode() == simple_element.decode():
                        new_tag = BeautifulSoup(f'{before_foreach}\n{simple_element}\n{after_foreach}')
                        simple_element.replace_with(new_tag)
                simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
                simple_element = replace_placeholders(simple_element, blog_replacement_data)
            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            blog_complex_replacement_data = {
                "__link__": '''{{$articles[{0}]['link']}}'''.format(num),
                "__image__": '''{{$articles[{0}]['image']}}'''.format(num),
                "__title__": '''{{$articles[{0}]['title']}}'''.format(num),
                "__alt_article__": '''{{$articles[{0}]['title']}}'''.format(num),
                'images/5497750661271-6.jpg': '''{{$articles[{0}]['image']}}'''.format(num),
                '<span class="__date__">5 بهمن 1402</span>': '''{{$articles[{0}]['created_at']}}'''.format(num),
                '<span class="__comments_number__">450</span>': '''{{$articles[{0}]['comments_count']['comments_count']}}'''.format(num),
                '<span class="__title__">تایتل</span>': '''{{$articles[{0}]['title']}}'''.format(num)
            }
            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = replace_placeholders(complex_element, blog_complex_replacement_data)

        blog_final_content = f'{before_html}\n{blog_section}\n{after_html}'
        # blog_final_content = BeautifulSoup(blog_final_content)
        # blog_final_content = blog_final_content.prettify()
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        write_text_in_path(project_path, "{inclued 'include_files/blog.tpl'}")
        blog_final_content = blog_final_content.replace("&gt;", ">")
        blog_final_content = blog_final_content.replace("&lt;", "<")

        #unit test
        # intial_blog_test_massage = initial_blog_test(blog_section)
        # return jsonify({"message": intial_blog_test_massage})

        return create_file(blog_final_content, include_files_directory, 'blog', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


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


def write_text_in_path(path, text):
    mainpage_tpl_path = os.path.join(path, 'mainPage.tpl')
    with open(mainpage_tpl_path, 'w') as mainPage_tpl_file:
        mainPage_tpl_file.write(text)




def initial_blog_test(blog_section):
    # Replace the URL with your local machine's URL
    url = "http://192.168.1.100/"

    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            blog_section_online = soup.find(class_="i_modular_blog")
            blog_unit_test_massage = blog_unit_test(blog_section, blog_section_online)
            return blog_unit_test_massage

            # Check if "i_modular_blog" is present in the HTML content
            if "i_modular_blog" in html_content:
                return "ماژول وبلاگ یافت شد"
            else:
                return "ماژول وبلاگ موجود نیست."
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def blog_unit_test(blog_section, blog_section_online):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        unit_test_files_directory = os.path.join(script_directory, 'unit_test_fles')
        json_file_path = os.path.join(unit_test_files_directory, 'blog_test_data.json')

        # Initialize an empty list to store the data
        blog_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()

        blog_data = json.loads(json_string)

        # for item in blog_data:
        #     testt = (item["title"])

        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
        complex_items_numbers = []
        simple_items_numbers = []

        elements = blog_section.find_all(class_=complex_items_pattern)
        for element in elements:
            match = complex_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                complex_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")
        elements = blog_section.find_all(class_=simple_items_pattern)
        for element in elements:
            match = simple_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                simple_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")


        for num in simple_items_numbers:
            blog_replacement_data = {
                "__i_modular_nc_item_" + num: "__i_modular_nc_item_" + simple_items_numbers[0],
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__title__": blog_data[int(num)]['title'],
                "__alt_article__": blog_data[int(num)]['title'],
                '<span class="__date__">5 بهمن 1402</span>': blog_data[int(num)]['created_at'],
                '<span class="__comments_number__">450</span>': blog_data[int(num)]['comments_count']['comments_count'],
                'images/5497750661271-6.jpg': blog_data[int(num)]['image'],
                '<span class="__title__">تایتل</span>': blog_data[int(num)]['title']
            }
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
            simple_element = replace_placeholders(simple_element, blog_replacement_data)



        for num in complex_items_numbers:
            blog_complex_replacement_data = {
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__title__": blog_data[int(num)]['title'],
                "__alt_article__": blog_data[int(num)]['title'],
                '<span class="__date__">5 بهمن 1402</span>': blog_data[int(num)]['created_at'],
                '<span class="__comments_number__">450</span>': blog_data[int(num)]['comments_count']['comments_count'],
                'images/5497750661271-6.jpg': blog_data[int(num)]['image'],
                '<span class="__title__">تایتل</span>': blog_data[int(num)]['title']
            }

            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = replace_placeholders(complex_element, blog_complex_replacement_data)

        blog_section_online = blog_section_online.prettify()
        # blog_section = blog_section.prettify()

        blog_section = f'{blog_section}'
        for num in simple_items_numbers:
            blog_section = blog_section.replace("__i_modular_nc_item_" + num, "__i_modular_nc_item_" + simple_items_numbers[0])

        for num in complex_items_numbers:
            blog_section = blog_section.replace("__i_modular_c_item_" + num, "__i_modular_c_item_" + complex_items_numbers[0])

        blog_section_online = blog_section_online.replace("</img>", "")
        blog_section = blog_section.replace("/>", ">")

        html_code_1 = re.sub(r'\s+', '', blog_section_online)
        html_code_2 = re.sub(r'\s+', '', blog_section)

        # Compare the two HTML code strings.
        if html_code_1 == html_code_2:
            return "تست سکشن بلاگ موفقیت آمیز بود."

        # return blog_section_online + '   ' + blog_section
        return 'طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.'
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"




