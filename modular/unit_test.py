from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs
from modular import helper_functions as helper
import difflib
from html_text import extract_text



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
                return "خطایی پیش آمده و دیتایی نمایش ندارد."

        else:
            return f"خطایی در گرفتن اطلاعات پیش آمده.{response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"خطایی در گرفتن اطلاعات پیش آمده.: {e}"


def unit_test_blog(blog_section, blog_section_online):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        unit_test_files_directory = os.path.join(script_directory, 'unit_test_fles')
        json_file_path = os.path.join(unit_test_files_directory, 'blog_test_data.json')

        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
        complex_items_numbers = []
        simple_items_numbers = []

        complex_items_numbers = helper.item_numbers(blog_section, complex_items_pattern)
        simple_items_numbers = helper.item_numbers(blog_section, simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        # Initialize an empty list to store the data
        blog_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()
        blog_data = json.loads(json_string)

        for num in simple_items_numbers:
            blog_replacement_data = {
                "__i_modular_nc_item_" + num: "__i_modular_nc_item_" + simple_items_numbers[0],
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__alt_article__": blog_data[int(num)]['title']
            }
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
            helper.replace_attribute(simple_element, '__image__', 'src', blog_data[int(num)]['image'])
            helper.replace_attribute(simple_element, '__title__', 'string', blog_data[int(num)]['title'])
            helper.replace_attribute(simple_element, '__heading__', 'string', blog_data[int(num)]['heading'])
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
            simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)


        for num in complex_items_numbers:
            blog_complex_replacement_data = {
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__alt_article__": blog_data[int(num)]['title']
            }

            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            helper.replace_attribute(complex_element, '__image__', 'src', blog_data[int(num)]['image'])
            helper.replace_attribute(complex_element, '__title__', 'string', blog_data[int(num)]['title'])
            helper.replace_attribute(complex_element, '__heading__', 'string', blog_data[int(num)]['heading'])
            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)


        blog_section_online = blog_section_online.prettify()
        blog_section = blog_section.prettify()

        blog_section = f'{blog_section}'


        for num in simple_items_numbers:
            blog_section = blog_section.replace("__i_modular_nc_item_" + num,"__i_modular_nc_item_" + simple_items_numbers[0])



        blog_section_online = blog_section_online.replace("</img>", "")
        blog_section = blog_section.replace("/>", ">")


        if compare_html_strings(blog_section_online, blog_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن خبرنامه موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + blog_section + '</div><div class="online section"> ' + blog_section_online +'</div></section></div>'
        return 'طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"


def unit_test_newsletter(newsletter_section, newsletter_section_online):
    try:
        helper.replace_attribute(newsletter_section, '__name__', 'name','NameSms')
        helper.replace_attribute(newsletter_section, '__email__', 'name','EmailSms')
        helper.replace_attribute(newsletter_section, '__phone__', 'name','CellSms')

        helper.replace_attribute(newsletter_section, '__name__', 'id','NameSms')
        helper.replace_attribute(newsletter_section, '__email__', 'id','EmailSms')
        helper.replace_attribute(newsletter_section, '__phone__', 'id','CellSms')

        helper.replace_attribute(newsletter_section, '__name__', 'class','full-name-js')
        helper.replace_attribute(newsletter_section, '__email__', 'class','email-js')
        helper.replace_attribute(newsletter_section, '__phone__', 'class','mobile-js')

        helper.replace_attribute(newsletter_section, '__submit__', 'onclick','submitNewsLetter()')


        newsletter_final_content = f'{newsletter_section}'
        newsletter_final_content = newsletter_final_content.replace("&gt;", ">")
        newsletter_final_content = newsletter_final_content.replace("&lt;", "<")


        newsletter_section_online = newsletter_section_online.prettify()
        newsletter_section = newsletter_section.prettify()
        newsletter_section = f'{newsletter_section}'
        newsletter_section_online = newsletter_section_online.replace("</img>", "")
        newsletter_section = newsletter_section.replace("/>", ">")

        # Usage
        if compare_html_strings(newsletter_section_online, newsletter_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن خبرنامه موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">سکشن خبرنامه خطا دارد..<section class="debug" style="display:none;"><div class="unit-test-section" >' + newsletter_section + '</div><div class="online section"> ' + newsletter_section_online +'</div></section></div>'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"


def compare_html_strings(html1, html2):
    # Parse the HTML strings
    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')


    # Normalize the HTML by converting it back to strings
    cleaned_html1 = soup1.prettify()
    cleaned_html2 = soup2.prettify()

    # Compare the cleaned HTML strings
    return cleaned_html1 == cleaned_html2