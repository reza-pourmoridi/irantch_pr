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

complex_items_pattern = re.compile(r'__i_modular_c_item_class_(\d+)')
simple_items_pattern = re.compile(r'__i_modular_nc_item_class_(\d+)')
complex_items_class = "__i_modular_c_item_class_"
simple_items_class = "__i_modular_nc_item_class_"
script_directory = os.path.dirname(__file__)  # Get the directory of the script
unit_test_json_files_directory = os.path.join(script_directory, '../update_data/unit_test_data')


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


def unit_test_blog(blog_section, blog_section_online , lang = 'fa'):
    try:
        json_file_path = os.path.join(unit_test_json_files_directory, 'article_data.json')


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
                simple_items_class + num: simple_items_class + simple_items_numbers[0],
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__alt_article__": blog_data[int(num)]['title']
            }
            simple_element = blog_section.find(class_=simple_items_class + num)
            helper.replace_attribute(simple_element, '__image_class__', 'src', blog_data[int(num)]['image'])
            helper.replace_attribute(simple_element, '__title_class__', 'string', blog_data[int(num)]['title'])
            helper.replace_attribute(simple_element, '__heading_class__', 'string', blog_data[int(num)]['heading'])
            simple_element = blog_section.find(class_=simple_items_class + num)
            simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)


        for num in complex_items_numbers:
            complex_element = blog_section.find(class_=complex_items_class + num)
            num = int(num)  # Convert 'num' to an integer
            if 0 <= num < len(blog_data) and blog_data[num]:
                blog_complex_replacement_data = {
                    "__airline__": blog_data[int(num)]['link'],
                    "__link__": blog_data[int(num)]['link'],
                    "__image__": blog_data[int(num)]['image'],
                    "__alt_article__": blog_data[int(num)]['title']
                }
                num = str(num)
                helper.replace_attribute(complex_element, '__image_class__', 'src', blog_data[int(num)]['image'])
                helper.replace_attribute(complex_element, '__title_class__', 'string', blog_data[int(num)]['title'])
                helper.replace_attribute(complex_element, '__heading_class__', 'string', blog_data[int(num)]['heading'])
                complex_element = blog_section.find(class_=complex_items_class + num)
                complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)
            else:
                complex_element.decompose()



        blog_section_online = blog_section_online.prettify()
        blog_section = blog_section.prettify()

        blog_section = f'{blog_section}'
        blog_section_online = f'{blog_section_online}'


        for num in simple_items_numbers:
            blog_section = blog_section.replace(simple_items_class + num,simple_items_class + simple_items_numbers[0])

        blog_section_online = helper.clean_serialize_string(blog_section_online)
        blog_section = helper.clean_serialize_string(blog_section)

        if compare_html_strings(blog_section_online, blog_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن خبرنامه موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" > ' + blog_section + ' </div><div class="online section"> ' + blog_section_online +' </div></section></div>'
        return 'طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def unit_test_banner_gallery(banner_gallery_section, banner_gallery_section_online, lang='fa'):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        unit_test_files_directory = os.path.join(script_directory, 'unit_test_fles')
        json_file_path = os.path.join(unit_test_files_directory, 'banner_test_data.json')

        complex_items_numbers = []
        simple_items_numbers = []

        complex_items_numbers = helper.item_numbers(banner_gallery_section, complex_items_pattern)
        simple_items_numbers = helper.item_numbers(banner_gallery_section, simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        # Initialize an empty list to store the data
        banner_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()
        banner_data = json.loads(json_string)

        for num in simple_items_numbers:
            banner_gallery_replacement_data = {
                "__title__": banner_data[int(num)]['title'],
                "__link__": banner_data[int(num)]['link']
            }
            simple_element = banner_gallery_section.find(class_=simple_items_class + num)
            if num == simple_items_numbers[0]:
                simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                simple_element = helper.replace_placeholders(simple_element, banner_gallery_replacement_data)
                simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                helper.replace_attribute(simple_element, '__image_class__', 'src', banner_data[int(num)]['pic'])
                helper.replace_attribute(simple_element, '__image_class__', 'alt', banner_data[int(num)]['title'])

            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            before_if = '''{if banners[{0}] }'''
            before_if = before_if.replace("{0}", num)
            after_if = '''{/if}'''

            banner_gallery_complex_replacement_data = {
                "__link__": banner_data[int(num)]['link'],
                "__title__": banner_data[int(num)]['title'],
            }
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            complex_element_final = helper.replace_placeholders(complex_element,
                                                                banner_gallery_complex_replacement_data)
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            helper.replace_attribute(complex_element, '__image_class__', 'src',
                                     banner_data[int(num)]['pic'].format(num))
            helper.replace_attribute(complex_element, '__title_class__', 'alt',
                                     banner_data[int(num)]['title'].format(num))

        banner_gallery_section = f'{banner_gallery_section}'
        banner_gallery_section_online = f'{banner_gallery_section_online}'

        if compare_html_strings(banner_gallery_section_online, banner_gallery_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن بنر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">سکشن بنر خطا دارد..<section class="debug" style="display:none;"><div class="unit-test-section" >' + banner_gallery_section + '</div><div class="online section"> ' + banner_gallery_section_online + '</div></section></div>'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def unit_test_news(news_section, news_section_online , lang = 'fa'):
    try:
        json_file_path = os.path.join(unit_test_json_files_directory, 'news_data.json')

        complex_items_numbers = []
        simple_items_numbers = []

        complex_items_numbers = helper.item_numbers(news_section, complex_items_pattern)
        simple_items_numbers = helper.item_numbers(news_section, simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        # Initialize an empty list to store the data
        news_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()
        news_data = json.loads(json_string)

        for num in simple_items_numbers:
            simple_element = news_section.find(class_=simple_items_class + num)
            numInt = int(num)  # Convert the string to an integer
            if 0 <= numInt < len(news_data):
                news_complex_replacement_data = {
                    "__link__": news_data[numInt]['link'],
                }
                news_replacement_data = {
                    simple_items_class + num: simple_items_class + simple_items_numbers[0],
                    "__link__": news_data[int(numInt)]['link'],
                }
                helper.replace_attribute(simple_element, '__image_class__', 'src', news_data[int(numInt)]['image'])
                helper.replace_attribute(simple_element, '__image_class__', 'alt', news_data[int(numInt)]['title'])
                helper.replace_attribute(simple_element, '__title_class__', 'string', news_data[int(numInt)]['title'])
                helper.replace_attribute(simple_element, '__heading_class__', 'string', news_data[int(numInt)]['heading'])
                helper.replace_attribute(simple_element, '__description_class__', 'string', news_data[int(numInt)]['description'])
                simple_element = news_section.find(class_=simple_items_class + num)
                simple_element = helper.replace_placeholders(simple_element, news_replacement_data)
            else:
                simple_element.decompose()

        for num in complex_items_numbers:
            complex_element = news_section.find(class_=complex_items_class + num)
            numInt = int(num)  # Convert the string to an integer
            if 0 <= numInt < len(news_data):
                news_complex_replacement_data = {
                    "__link__": news_data[numInt]['link'],
                }
                helper.replace_attribute(complex_element, '__image_class__', 'src', news_data[int(numInt)]['image'])
                helper.replace_attribute(complex_element, '__image_class__', 'alt', news_data[int(numInt)]['alt'])
                helper.replace_attribute(complex_element, '__title_class__', 'string', news_data[int(numInt)]['title'])
                helper.replace_attribute(complex_element, '__heading_class__', 'string', news_data[int(numInt)]['heading'])
                helper.replace_attribute(complex_element, '__description_class__', 'string', news_data[int(numInt)]['description'])
                complex_element = news_section.find(class_=complex_items_class + num)
                complex_element_final = helper.replace_placeholders(complex_element, news_complex_replacement_data)
            else:
                complex_element.decompose()



        news_section_online = news_section_online.prettify()
        news_section = news_section.prettify()

        news_section = f'{news_section}'

        for num in simple_items_numbers:
            news_section = news_section.replace(simple_items_class + num,simple_items_class + simple_items_numbers[0])



        news_section_online = news_section_online.replace("https", "")
        news_section_online = news_section_online.replace("http", "")
        news_section = news_section.replace("https", "")
        news_section = news_section.replace("http", "")

        news_section_online = news_section_online.replace("</img>", "")
        news_section = news_section.replace("/>", ">")


        if compare_html_strings(news_section_online, news_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن اخبار موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + news_section + '</div><div class="online section"> ' + news_section_online +'</div></section></div>'
        return 'طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def unit_test_newsletter(newsletter_section, newsletter_section_online, lang='fa'):
    try:
        helper.replace_attribute(newsletter_section, '__name_class__', 'name', 'NameSms')
        helper.replace_attribute(newsletter_section, '__email_class__', 'name', 'EmailSms')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'name', 'CellSms')

        helper.replace_attribute(newsletter_section, '__name_class__', 'id', 'NameSms')
        helper.replace_attribute(newsletter_section, '__email_class__', 'id', 'EmailSms')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'id', 'CellSms')

        helper.replace_attribute(newsletter_section, '__name_class__', 'class', 'full-name-js')
        helper.replace_attribute(newsletter_section, '__email_class__', 'class', 'email-js')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'class', 'mobile-js')

        helper.replace_attribute(newsletter_section, '__submit_class__', 'onclick', 'submitNewsLetter()')

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

        return '<div style="background: red;padding: 15px;">سکشن خبرنامه خطا دارد..<section class="debug" style="display:none;"><div class="unit-test-section" >' + newsletter_section + '</div><div class="online section"> ' + newsletter_section_online + '</div></section></div>'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def unit_test_menu(menu_section, menu_section_online , lang = 'fa'):
    try:
        json_file_path = os.path.join(unit_test_json_files_directory, 'menu_data.json')


        # Initialize an empty list to store the data
        menu_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()
        menu_data = json.loads(json_string)

        repeatable_links = {
                'پرواز': 'http://192.168.1.100/gds/'+ lang +'/page/flight',
                'پیگیری خرید': 'http://192.168.1.100/gds/'+ lang +'/UserTracking',
                'وبلاگ': 'http://192.168.1.100/gds/'+ lang +'/mag',
                'اخبار سایت': 'http://192.168.1.100/gds/'+ lang +'/news',
                'معرفی ايران': 'http://192.168.1.100/gds/'+ lang +'/aboutIran',
                'قوانین و مقررات': 'http://192.168.1.100/gds/'+ lang +'/rules',
                'درباره ما': 'http://192.168.1.100/gds/'+ lang +'/aboutUs',
                'تماس با ما': 'http://192.168.1.100/gds/'+ lang +'/contactUs',
                'پرداخت آنلاین': 'http://192.168.1.100/gds/'+ lang +'/pay',
        }

        helper.replace_attribute_by_text(menu_section, 'ورود یا ثبت نام' , 'string', "<span class='logined-name'>ورود / ثبت نام</span>")
        helper.replace_attribute_by_text(menu_section, 'الدخول / يسجل' , 'string', "<span class='logined-name'>الدخول / يسجل</span>")
        helper.replace_attribute(menu_section, '__login_register_class__', 'class','__login_register_class__ main-navigation__button2 show-box-login-js button_header logIn d-flex d-lg-none')
        helper.replace_attribute(menu_section, '__login_register_class__2', 'class','__login_register_class__2 main-navigation__button2 show-box-login-js')


        after_login =  "<div class='main-navigation__sub-menu2 arrow-up show-content-box-login-js' style='display: none'>\r\n    <div class=\"sup-menu-flex\">\r\n        <div class=\"sup-menu-flex-r\">\r\n            <a target=\"_parent\" class=\"log-reg-sub\" href=\"https://192.168.1.100/gds/fa/loginUser\">\r\n                <div>\r\n                    <svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n                    <path d=\"M131.5,472H60.693c-8.538,0-13.689-4.765-15.999-7.606c-3.988-4.906-5.533-11.29-4.236-17.519\r\n                        c20.769-99.761,108.809-172.616,210.445-174.98c1.693,0.063,3.39,0.105,5.097,0.105c1.722,0,3.434-0.043,5.142-0.107\r\n                        c24.853,0.567,49.129,5.24,72.236,13.917c10.34,3.885,21.871-1.352,25.754-11.693c3.883-10.34-1.352-21.871-11.693-25.754\r\n                        c-3.311-1.244-6.645-2.408-9.995-3.512C370.545,220.021,392,180.469,392,136C392,61.01,330.991,0,256,0\r\n                        c-74.991,0-136,61.01-136,136c0,44.509,21.492,84.092,54.643,108.918c-30.371,9.998-58.871,25.546-83.813,46.062\r\n                        c-45.732,37.617-77.529,90.086-89.532,147.743c-3.762,18.066,0.744,36.622,12.363,50.908C25.221,503.847,42.364,512,60.693,512\r\n                        H131.5c11.046,0,20-8.954,20-20C151.5,480.954,142.546,472,131.5,472z M160,136c0-52.935,43.065-96,96-96s96,43.065,96,96\r\n                        c0,51.367-40.554,93.438-91.326,95.885c-1.557-0.028-3.114-0.052-4.674-0.052c-1.564,0-3.127,0.023-4.689,0.051\r\n                        C200.546,229.43,160,187.362,160,136z\"></path>\r\n                        <path d=\"M496.689,344.607c-8.561-19.15-27.845-31.558-49.176-31.607h-62.372c-0.045,0-0.087,0-0.133,0\r\n                        c-22.5,0-42.13,13.26-50.029,33.807c-1.051,2.734-2.336,6.178-3.677,10.193H200.356c-5.407,0-10.583,2.189-14.35,6.068\r\n                        l-34.356,35.388c-7.567,7.794-7.529,20.203,0.085,27.95l35,35.612c3.76,3.826,8.9,5.981,14.264,5.981h65c11.046,0,20-8.954,20-20\r\n                        c0-11.046-8.954-20-20-20h-56.614l-15.428-15.698L208.814,397h137.491c9.214,0,17.235-6.295,19.426-15.244\r\n                        c1.618-6.607,3.648-12.959,6.584-20.596c1.936-5.036,6.798-8.16,12.741-8.16c0.013,0,0.026,0,0.039,0h62.371\r\n                        c5.656,0.013,10.524,3.053,12.705,7.932c5.369,12.012,11.78,30.608,11.828,50.986c0.048,20.529-6.356,39.551-11.739,51.894\r\n                        c-2.17,4.978-7.079,8.188-12.56,8.188c-0.011,0-0.022,0-0.033,0h-63.125c-5.533-0.013-10.716-3.573-12.896-8.858\r\n                        c-2.339-5.671-4.366-12.146-6.197-19.797c-2.571-10.742-13.367-17.366-24.105-14.796c-10.743,2.571-17.367,13.364-14.796,24.106\r\n                        c2.321,9.699,4.978,18.118,8.121,25.738c8.399,20.364,27.939,33.555,49.827,33.606h63.125c0.043,0,0.083,0,0.126,0\r\n                        c21.351-0.001,40.647-12.63,49.18-32.201c6.912-15.851,15.137-40.511,15.072-67.975\r\n                        C511.935,384.434,503.638,360.153,496.689,344.607z\"></path>\r\n                        <circle cx=\"431\" cy=\"412\" r=\"20\"></circle>\r\n                </svg>\r\n\r\n                </div>\r\n                <span>ورود</span>\r\n            </a>\r\n        </div>\r\n        <div class=\"sup-menu-flex-l\">\r\n            <a target=\"_parent\" class=\"log-reg-sub\" href=\"https://192.168.1.100/gds/fa/registerUser\">\r\n                <div>\r\n                    <svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n                    <circle cx=\"370\" cy=\"346\" r=\"20\"></circle>\r\n                        <path d=\"M460,362c11.046,0,20-8.954,20-20v-74c0-44.112-35.888-80-80-80h-24.037v-70.534C375.963,52.695,322.131,0,255.963,0\r\n                        s-120,52.695-120,117.466V188H112c-44.112,0-80,35.888-80,80v164c0,44.112,35.888,80,80,80h288c44.112,0,80-35.888,80-80\r\n                        c0-11.046-8.954-20-20-20c-11.046,0-20,8.954-20,20c0,22.056-17.944,40-40,40H112c-22.056,0-40-17.944-40-40V268\r\n                        c0-22.056,17.944-40,40-40h288c22.056,0,40,17.944,40,40v74C440,353.046,448.954,362,460,362z M335.963,188h-160v-70.534\r\n                        c0-42.715,35.888-77.466,80-77.466s80,34.751,80,77.466V188z\"></path>\r\n                        <circle cx=\"219\" cy=\"346\" r=\"20\"></circle>\r\n                        <circle cx=\"144\" cy=\"346\" r=\"20\"></circle>\r\n                        <circle cx=\"294\" cy=\"346\" r=\"20\"></circle>\r\n                </svg>\r\n                </div>\r\n                <span>ثبت نام</span>\r\n            </a>\r\n\r\n        </div>\r\n    </div>\r\n    "


        simple_element = menu_section.find(class_=lambda classes: classes and '__login_register_class__' in classes)
        for tag in menu_section.find_all():
            if tag.decode() == simple_element.decode():
                new_tag = BeautifulSoup(f'{simple_element}\n{after_login}')
                simple_element.replace_with(new_tag)

        # return f'{menu_section}'

        for key, val in repeatable_links.items():
            helper.replace_attribute_by_text(menu_section, key, 'href', val)


        menu_section_online = menu_section_online.prettify()
        menu_section = menu_section.prettify()

        menu_section = f'{menu_section}'
        menu_section = menu_section.replace("__main_link__", "http://192.168.1.100")

        menu_section_online = helper.clean_serialize_string(menu_section_online)
        menu_section = helper.clean_serialize_string(menu_section)


        if compare_html_strings(menu_section_online, menu_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن منوی هدر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + menu_section + '</div><div class="online section"> ' + menu_section_online +'</div></section></div>'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def unit_test_footer(footer_section, footer_section_online , lang = 'fa'):
    try:

        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        unit_test_files_directory = os.path.join(script_directory, 'unit_test_fles')



        social_element = footer_section.find(class_=lambda classes: classes and '__social_class__' in classes)
        repeatable_social_links = {
            '__telegram_class__': 'ssssss',
            '__whatsapp_class__': 'https://web.whatsapp.com/send?phone=09195972979',
            '__instagram_class__': 'https://instagram.com/mizbanfly',
        }
        if social_element:
            for key, val in repeatable_social_links.items():
                helper.replace_attribute(social_element, key, 'href', val)

        repeatable_links = {
                'پرواز': 'http://192.168.1.100/gds/'+ lang + '/page/flight',
                'پیگیری خرید': 'http://192.168.1.100/gds/'+ lang + '/UserTracking',
                'وبلاگ': 'http://192.168.1.100/gds/'+ lang + '/mag',
                'اخبار سایت': 'http://192.168.1.100/gds/'+ lang + '/news',
                'معرفی ايران': 'http://192.168.1.100/gds/'+ lang + '/aboutIran',
                'قوانین و مقررات': 'http://192.168.1.100/gds/'+ lang + '/rules',
                'درباره ما': 'http://192.168.1.100/gds/'+ lang + '/aboutUs',
                'تماس با ما': 'http://192.168.1.100/gds/'+ lang + '/contactUs',
                'پرداخت آنلاین': 'http://192.168.1.100/gds/'+ lang + '/pay',

        }

        for key, val in repeatable_links.items():
            helper.replace_attribute_by_text(footer_section, key, 'href', val)

        helper.replace_attribute(footer_section, '__aboutUs_class__', 'string',"تست میکنیم 1 2 3")
        helper.replace_attribute(footer_section, '__address_class__', 'string',            " آدرس :  تهران، خیابان کارگر شمالی، کوچه چهارم، پلاک ۸ ،ساختمان پلاتین، طبقه سوم، واحدجنوبی")
        helper.replace_attribute(footer_section, '__mobile_class__', 'string', '''09353834714''')
        helper.replace_attribute(footer_section, '__mobile_class__', 'href', '''tel:09353834714''')
        footer_section = helper.replace_placeholders(footer_section,{'__aboutUsLink__': 'https://192.168.1.100/gds/fa/aboutUs'})

        footer_section = BeautifulSoup(footer_section, "html.parser")

        footer_section_online = footer_section_online.prettify()
        footer_section = footer_section.prettify()

        footer_section_online = f'{footer_section_online}'
        footer_section = f'{footer_section}'

        footer_section_online = helper.clean_serialize_string(footer_section_online)
        footer_section = helper.clean_serialize_string(footer_section)



        if compare_html_strings(footer_section_online, footer_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن فوتر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + footer_section + '</div><div class="online section"> ' + footer_section_online +'</div></section></div>'
    except requests.exceptions.RequestException as e:
        return f"خطایی در ماژول گذار پیش آمد.: {e}"

def compare_html_strings(html1, html2):
    # Parse the HTML strings
    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')

    soup1 = soup1.prettify()
    soup2 = soup2.prettify()

    # Compare the serialized HTML strings
    return soup1 == soup2

