from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import traceback
import requests
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


def unit_test_banner_gallery(banner_gallery_section, banner_gallery_section_online, lang='fa'):
    try:
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
        json_file_path = os.path.join(unit_test_json_files_directory, 'banners_data.json')
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()

        banner_data = json.loads(json_string)

        for num in simple_items_numbers:
            num = int(num)  # Convert 'num' to an integer
            if 0 <= num < len(banner_data) and banner_data[num]:
                num = str(num)
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

        if helper.compare_html_strings(banner_gallery_section_online, banner_gallery_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن بنر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">سکشن بنر خطا دارد..<section class="debug" style="display:none;"><div class="unit-test-section" >' + banner_gallery_section + '</div><div class="online section"> ' + banner_gallery_section_online + '</div></section></div>'
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def unit_test_news_old(news_section, news_section_online , lang = 'fa'):
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

        news_section = news_section.replace("__all_link_href__", "://192.168.1.100/gds/fa/news")


        news_section = f'{news_section}'

        for num in simple_items_numbers:
            news_section = news_section.replace(simple_items_class + num,simple_items_class + simple_items_numbers[0])



        news_section_online = news_section_online.replace("https", "")
        news_section_online = news_section_online.replace("http", "")
        news_section = news_section.replace("https", "")
        news_section = news_section.replace("http", "")

        news_section_online = news_section_online.replace("</img>", "")
        news_section = news_section.replace("/>", ">")


        if helper.compare_html_strings(news_section_online, news_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن اخبار موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.<section class="debug" style="display:none;"><div class="unit-test-section" >' + news_section + '</div><div class="online section"> ' + news_section_online +'</div></section></div>'

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


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
        if helper.compare_html_strings(newsletter_section_online, newsletter_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن خبرنامه موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">سکشن خبرنامه خطا دارد..<section class="debug" style="display:none;"><div class="unit-test-section" >' + newsletter_section + '</div><div class="online section"> ' + newsletter_section_online + '</div></section></div>'
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def unit_test_menu(menu_section, menu_section_online , lang = 'fa'):
    try:
        json_file_path = os.path.join(unit_test_json_files_directory, 'menu_data.json')


        # Initialize an empty list to store the data
        menu_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()
        menu_data = json.loads(json_string)

        repeatable_links = {
                'پرواز': 'http://192.168.1.100/gds/'+ lang +'/page/flight',
                'پرواز': 'http://192.168.1.100/gds/'+ lang +'/page/flight',
                'هتل': 'http://192.168.1.100/gds/'+ lang +'/page/hotel',
                'بیمه': 'http://192.168.1.100/gds/'+ lang +'/page/insurance',
                'انتقاد و پیشنهادات': 'http://192.168.1.100/gds/'+ lang +'/feedback',
                'نظر سنجی': 'http://192.168.1.100/gds/'+ lang +'/vote',
                'باشگاه مسافران': 'http://192.168.1.100/gds/'+ lang +'/loginUser',
                'پیگیری خرید': 'http://192.168.1.100/gds/'+ lang +'/UserTracking',
                'وبلاگ': 'http://192.168.1.100/gds/'+ lang +'/mag',
                'ویدئو ها': 'http://192.168.1.100/gds/'+ lang +'/video',
                'نمایندگی ها': 'http://192.168.1.100/gds/'+ lang +'/agencyList',
                'همکاری با ما': 'http://192.168.1.100/gds/'+ lang +'/همکاری با ما',
                'نرخ ارز': 'http://192.168.1.100/gds/'+ lang +'/currency',
                'سفر نامه': 'http://192.168.1.100/gds/'+ lang +'/recommendation',
                'سفارت': 'http://192.168.1.100/gds/'+ lang +'/embassies',
                'پرسش و پاسخ': 'http://192.168.1.100/gds/'+ lang +'/faq',
                'دقیقه 90': 'http://192.168.1.100/gds/'+ lang +'/lastMinute',
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
        if simple_element is not None:
            for tag in menu_section.find_all():
                if tag is not None and tag.decode() == simple_element.decode():
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


        if helper.compare_html_strings(menu_section_online, menu_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن منوی هدر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + menu_section + '</div><div class="online section"> ' + menu_section_online +'</div></section></div>'

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


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



        if helper.compare_html_strings(footer_section_online, footer_section):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن فوتر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="unit-test-section" >' + footer_section + '</div><div class="online section"> ' + footer_section_online +'</div></section></div>'

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def test_unit_test(a, b, c):
    return 'test'


def unit_test_tour(tour_section, tour_section_online , lang = 'fa'):
    try:
        modul_data_array = {
            'general_region_array': ['internal', 'external', ''],
            'general_type_array': ['', 'special'],
            'before_html': '''{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}''',
            'before_html_local': '''{assign var="__params_var__" value=['type'=>'__type__','limit'=> '__local_max_limit__','dateNow' => $dateNow, 'country' =>'__country__','city' => null]}
                                {assign var='__general_var__' value=$obj_main_page->getToursReservation($__params_var__)}
                                {if $__general_var__}
                                    {assign var='check_general' value=true}
                                {/if}
                                {assign var="__local_min_var__" value=__local_min__}
                                {assign var="__local_max_var__" value=__local_max__}
                            ''',
            'after_html': '''{/if}''',
            'before_foreach_local':'''
                                {foreach $__general_var__ as $item}
                                    {if $__local_min_var__ <= $__local_max_var__}
                                ''',
            'after_foreach_local':'''
                                    {$__local_min_var__ = $__local_min_var__ + 1}
                                    {/if}
                                {/foreach}
                                ''',
            'replace_classes_local': {
            '___price_class__': {'string': '''{$item['min_price']['discountedMinPriceR']|number_format}'''},
            '__title_class__': {'string': '''{$item['tour_name']}'''},
            '__airline_class__': {'string': '''{$item['airline_name']}'''},
            '__night_class__': {'string': '''{$item['night']}'''},
            '__day_class__': {'string': '''{$item['night'] + 1}'''},
            '__city_class__': {'string': '''{$item['destination_city_name']}'''},
            '__rate_count_class__': {'string': '''{$item['rate_count']}'''},
            '__description_class__': {'string': '''{$item['description']}'''},
            '__degree_class__': {'string': '''{$item['StarCode']}'''},
            '__image_class__': {
                'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$item['tour_pic']}''',
                'alt': '''{$item['tour_name']}'''},
            '__date_class__': {'string': '''{assign var="year" value=substr($item['start_date'], 0, 4)}
                                        {assign var="month" value=substr($item['start_date'], 4, 2)}
                                        {assign var="day" value=substr($item['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        '''},
        },
            'replace_comlex_classes_local': {
            '___price_class__': {
                'string': '''{$__general_var__[{0}]['min_price']['discountedMinPriceR']|number_format}'''},
            '__title_class__': {'string': '''{$__general_var__[{0}]['tour_name']}'''},
            '__airline_class__': {'string': '''{$__general_var__[{0}]['airline_name']}'''},
            '__night_class__': {'string': '''{$__general_var__[{0}]['night']}'''},
            '__city_class__': {'string': '''{$__general_var__[{0}]['destination_city_name']}'''},
            '__rate_count_class__': {'string': '''{$__general_var__[{0}]['rate_count']}'''},
            '__description_class__': {'string': '''{$__general_var__[{0}]['description']}'''},
            '__day_class__': {'string': '''{$__general_var__[{0}]['night'] + 1}'''},
            '__degree_class__': {'string': '''{$__general_var__[{0}]['StarCode']}'''},
            '__image_class__': {
                'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__general_var__[{0}]['tour_pic']}''',
                'alt': '''{$__general_var__[{0}]['tour_name']}'''},
            '__date_class__': {'string': '''{assign var="year" value=substr($__general_var__[{0}]['start_date'], 0, 4)}
                                        {assign var="month" value=substr($__general_var__[{0}]['start_date'], 4, 2)}
                                        {assign var="day" value=substr($__general_var__[{0}]['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        '''},
        },
            'generals_simple_replacements': {
            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailTour/{$item['id']}/{$item['tour_slug']}''',
        },
            'generals_complex_replacements': {
            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailTour/{$__general_var__[{0}]['id']}/{$__general_var__[{0}]['tour_slug']}''',
        },

            'before_star_simple': '''{for $i = 0; $i < count($item['rate_average']); $i++}''',
            'before_dark_star_simple': '''{for $i = count($item['rate_average']); $i < 6; $i++}''',
            'before_star_complex': '''{for $i = 0; $i < count($__general_var__['rate_average']); $i++}''',
            'before_dark_star_complex': '''{for $i = count($__general_var__['rate_average']); $i < 6; $i++}''',

            'unique_key': 'tour',
            'no_chiled': '',

            'replace_classes_general': {},

        }

        unit_test = general_test(tour_section, tour_section_online, lang, modul_data_array)
        return unit_test
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str





def unit_test_blog(blog_section, blog_section_online , lang = 'fa'):
    try:
        modul_data_array = {
            'general_region_array': [''],
            'general_type_array': [''],
            'before_html': '''''',
            'before_html_local': '''
                        {*with category*}
                        {*{assign var="search_array" value=['section'=>'mag','category'=>1,'limit'=>'__local_max_limit__']}*}
                        {*{assign var='__general_var__' value=$obj_main_page->getCategoryArticles($search_array)}*}
                        {*{assign var='counter' value=0}*}
                        {*{assign var="article_count" value=$__general_var__|count}*}

                        {assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>'__local_max_limit__']}
                        {assign var='__general_var__' value=$obj_main_page->articlesPosition($data_search_blog)}
                        {assign var='counter' value=0}
                        {assign var="article_count" value=$__general_var__|count}
                        {if $__general_var__[0]}
                            {assign var='check_general' value=true}
                        {/if}
                    ''',
            'after_html': '''{/if}''',
            'before_foreach_local':'''
                                {foreach $__general_var__ as $key => $item}
                                    {if $__local_min_var__ <= $__local_max_var__}
                                ''',
            'after_foreach_local':'''
                                    {$__local_min_var__ = $__local_min_var__ + 1}
                                    {/if}
                                {/foreach}
                                ''',

            'replace_classes_local': {
            '__image_class__': {'src': '''{$item["image"]}''', 'alt': '''{$item["alt"]}'''},
            '__title_class__': {'string': '''{$item["title"]}'''},
            '__degree_class__': {'string': '''{$item["rates"]["average"]}'''},
            '__category_class__': {'string': '''{$item['categories_array'][0]['title']}'''},
            '__heading_class__': {'string': '''{$item["heading"]}'''},
            '__date_class__': {'string': '''{$item["created_at"]}'''},
        },
            'replace_comlex_classes_local': {
            '__image_class__': {
                'src': '''{$__general_var__[{0}]['image']}''',
                'alt': '''{$__general_var__[{0}]['alt']}'''},
            '__title_class__': {'string': '''{$__general_var__[{0}]['title']}'''},
            '__degree_class__': {'string': '''{$__general_var__[{0}]["rates"]["average"]}'''},
            '__category_class__': {'string': '''{$__general_var__[{0}]['categories_array'][0]['title']}'''},
            '__heading_class__': {'string': '''{$__general_var__[{0}]['heading']}'''},
            '__date_class__': {'string': '''{$__general_var__[{0}]['created_at']}'''},
        },

            'generals_simple_replacements': {
            "__airline__": '''{$item['link']}''',
            "__link__": '''{$item['link']}''',
                 },
            'generals_complex_replacements': {
            "__link__": '''{$__general_var__[{0}]['link']}''',
        },

            'before_star_simple': '''{for $i = 0; $i < count($item['StarCode']); $i++}''',
            'before_dark_star_simple': '''{for $i = count($item['StarCode']); $i < 6; $i++}''',
            'before_star_complex': '''{for $i = 0; $i < count($__general_var__['StarCode']); $i++}''',
            'before_dark_star_complex': '''{for $i = count($__general_var__['StarCode']); $i < 6; $i++}''',

            'unique_key': 'blog',
            'no_chiled': 'yes',
            'replace_classes_general': {},
        }

        unit_test = general_test(blog_section, blog_section_online, lang, modul_data_array)
        return unit_test
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def unit_test_news(news_section, news_section_online , lang = 'fa'):
    try:
        modul_data_array = {
            'general_region_array': [''],
            'general_type_array': [''],
            'before_html': '''''',
            'before_html_local': '''{assign var="__general_var__" value=$obj_main_page->getNewsArticles()}
                            {assign var="othe_itmes" value=$__general_var__['data']}
                            {assign var="i" value="2"}
                            {assign var='counter' value=0}
                            {if $othe_itmes > 0 }
                            {if $__general_var__[0]}
                                {assign var='check_general' value=true}
                            {/if}
                            ''',
            'after_html': '''{/if}''',
            'before_foreach_local':'''{foreach $__general_var__ as $item} {if $__local_min_var__ <= $__local_max_var__}''',
            'after_foreach_local':'''
                                    {$__local_min_var__ = $__local_min_var__ + 1}
                                    {/if}
                                {/foreach}
                                ''',

            'replace_classes_local': {
            '__image_class__': {'src': '''{$item["image"]}''', 'alt': '''{$item["alt"]}'''},
            '__title_class__': {'string': '''{$item["title"]}'''},
            '__heading_class__': {'string': '''{$item["heading"]}'''},
            '__date_class__': {'string': '''{$item["created_at"]}'''},
            '__description_class__': {'string': '''{$item["description"]}'''},
        },
            'replace_comlex_classes_local': {
            '__image_class__': {
                'src': '''{$__general_var__[{0}]['image']}''',
                'alt': '''{$__general_var__[{0}]['alt']}'''},
            '__title_class__': {'string': '''{$__general_var__[{0}]['title']}'''},
            '__heading_class__': {'string': '''{$__general_var__[{0}]["created_at"]}'''},
            '__date_class__': {'string': '''{$__general_var__[{0}]['heading']}'''},
            '__description_class__': {'string': '''{$__general_var__[{0}]['description']}'''},
        },

            'generals_simple_replacements': {
            "__link__": '''{$item['link']}''',
                 },
            'generals_complex_replacements': {
            "__link__": '''{$__general_var__[{0}]['link']}''',
        },

            'before_star_simple': '''{for $i = 0; $i < count($item['StarCode']); $i++}''',
            'before_dark_star_simple': '''{for $i = count($item['StarCode']); $i < 6; $i++}''',
            'before_star_complex': '''{for $i = 0; $i < count($__general_var__['StarCode']); $i++}''',
            'before_dark_star_complex': '''{for $i = count($__general_var__['StarCode']); $i < 6; $i++}''',

            'unique_key': 'news',
            'no_chiled': 'yes',
            'replace_classes_general': {
                '__all_link_href_class__': {'href': '''{$smarty.const.ROOT_ADDRESS}/news'''},
            },
        }
        unit_test = general_test(news_section, news_section_online, lang, modul_data_array)
        return unit_test
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def general_test(generals_section, general_section_online, lang = 'fa', modul_data_array = {} ):
    try:

        before_html = ''
        after_html = ''

        general_region_array = modul_data_array['general_region_array']
        general_type_array = modul_data_array['general_type_array']
        before_html_local = ''


        before_foreach_local = ''
        after_foreach_local = ''

        replace_classes_local = modul_data_array['replace_classes_local']
        replace_comlex_classes_local = modul_data_array['replace_comlex_classes_local']

        generals_simple_replacements = modul_data_array['generals_simple_replacements']
        generals_complex_replacements = modul_data_array['generals_complex_replacements']

        before_star_simple = modul_data_array['before_star_simple']
        before_dark_star_simple = modul_data_array['before_dark_star_simple']
        before_star_complex = modul_data_array['before_star_complex']
        before_dark_star_complex = ''

        unique_key = modul_data_array['unique_key']
        no_chiled = modul_data_array['no_chiled']
        section_class_init = '__'+ unique_key + '__'
        section_var_init = unique_key
        section_params_init = unique_key + '_params'
        special_page = unique_key

        replace_classes_general = modul_data_array['replace_classes_general']


        local_min_var_init = 'min'
        local_max_var_init = 'max'

        for region in general_region_array:
            for type in general_type_array:

                section_class = section_class_init
                section_var = section_var_init
                section_params = section_params_init
                local_min_var = local_min_var_init
                local_max_var = local_max_var_init
                if region:
                    section_class =  section_class + region + '__'
                    section_var =  section_var + '_' + region
                    section_params =  section_params + '_' + region
                    local_min_var =  local_min_var + '_' + region
                    local_max_var =  local_max_var + '_' + region
                if type:
                    section_class = section_class + type + '__'
                    section_var =  section_var + '_' + type
                    local_min_var =  local_min_var + '_' + region
                    local_max_var =  local_max_var + '_' + region


                if no_chiled == 'yes':
                    sections = [1]
                    json_html = helper.extract_json_data_from_url(unique_key)
                else:
                    sections = generals_section.find_all(class_=section_class)
                    json_html = helper.extract_json_data_from_url(section_class)

                json_html = BeautifulSoup(json_html, 'html.parser')
                json_element = json_html.find(class_='data_modular')
                if json_element:
                    json_string = json_element.get_text()
                    general_data = json.loads(json_string)
                else:
                    general_data = []

                if  sections:
                    for local_section in sections:
                        if no_chiled == 'yes':
                            local_section = generals_section

                        complex_items_numbers = helper.item_numbers(local_section, complex_items_pattern)
                        simple_items_numbers = helper.item_numbers(local_section, simple_items_pattern)
                        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
                        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
                        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
                        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

                        for num in simple_items_numbers:
                            simple_element = local_section.find(class_=simple_items_class + num)
                            numInt = int(num)
                            
                            if num != simple_items_numbers[0]:
                                simple_element_text = local_section.find(class_=simple_items_class + simple_items_numbers[0])
                                simple_element_text = f'{simple_element_text}'
                                simple_element_text = simple_element_text.replace(f'{simple_items_class + simple_items_numbers[0]}', f'{simple_items_class + num}')
                                simple_element_text = BeautifulSoup(simple_element_text, 'html.parser')
                                simple_element.replace_with(simple_element_text)
                                simple_element = local_section.find(class_=simple_items_class + num)
                                helper.replace_attribute(local_section, simple_items_class + num, 'href', '__link__')

                            if 0 <= numInt < len(general_data):
                                final_generals_simple_replacements = {}
                                for item_pointer ,item_val in generals_simple_replacements.items():
                                    pattern = r"\{\$item\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?\}"
                                    output_string = helper.get_element_data_key_by_pattern(general_data[int(numInt)],pattern, item_val)
                                    final_generals_simple_replacements[item_pointer] = output_string

                                simple_element = helper.replace_placeholders(simple_element, final_generals_simple_replacements)
                                simple_element = local_section.find(class_=simple_items_class + num)
                                for class_name, val in replace_classes_local.items():
                                    for atr, value in val.items():
                                        pattern = r"\{\$item\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?\}"
                                        value = helper.get_element_data_key_by_pattern(general_data[int(numInt)], pattern, value)
                                        helper.replace_attribute(simple_element, class_name, atr, value)

                                for i in range(1, 6):
                                    light_star_elements = simple_element.find(class_='__star_class_light__' + str(i))
                                    dark_star_elements = simple_element.find(class_='__star_class_dark__' + str(i))
                                    if i == 1 and light_star_elements:
                                        new_light_star = before_star_simple + str(light_star_elements) + '''{/for}'''
                                        new_light_star = BeautifulSoup(new_light_star, 'html.parser')
                                        light_star_elements.replace_with(new_light_star)
                                    else:
                                        if light_star_elements:
                                            light_star_elements.decompose()

                                    if i == 1 and dark_star_elements:
                                        new_dark_star = before_dark_star_simple + str(dark_star_elements) + '''{/for}'''
                                        new_dark_star = BeautifulSoup(new_dark_star, 'html.parser')
                                        dark_star_elements.replace_with(new_dark_star)
                                    else:
                                        if dark_star_elements:
                                            dark_star_elements.decompose()

                            else:
                                simple_element.decompose()


                        for num in complex_items_numbers:
                            numInt = int(num)
                            if 0 <= numInt < len(general_data):
                                complex_element = local_section.find(class_=complex_items_class + num)
                                final_gcr = {}
                                for gcr_key, gcr_val in generals_complex_replacements.items():
                                    pattern = r"\{\$__general_var__\[\{0}\]\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?\}"
                                    valuefinal = helper.get_element_data_key_by_pattern(general_data[int(numInt)],pattern, gcr_val)
                                    final_gcr = {
                                        f'{gcr_key}': f'{valuefinal}'
                                    }

                                complex_element = helper.replace_placeholders(complex_element, final_gcr)

                                complex_element = local_section.find(class_=complex_items_class + num)
                                for class_name, val in replace_comlex_classes_local.items():
                                    for atr, value in val.items():
                                        pattern = r"\{\$__general_var__\[\{0}\]\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?\}"
                                        valuefinal = helper.get_element_data_key_by_pattern(general_data[int(numInt)], pattern, value )
                                        helper.replace_attribute(complex_element, class_name, atr, valuefinal)

                                    for i in range(1, 6):
                                        light_star_elements = complex_element.find(class_='__star_class_light__' + str(i))
                                        dark_star_elements = complex_element.find(class_='__star_class_dark__' + str(i))
                                        if i == 1 and light_star_elements:
                                            new_light_star = before_star_complex + str(light_star_elements) + '''{/for}'''
                                            new_light_star = new_light_star.replace("{0}", f'{num}')
                                            new_light_star = new_light_star.replace("__general_var__", section_var)
                                            new_light_star = BeautifulSoup(new_light_star, 'html.parser')
                                            light_star_elements.replace_with(new_light_star)
                                        else:
                                            if light_star_elements:
                                                light_star_elements.decompose()

                                        if i == 1 and dark_star_elements:
                                            new_dark_star = str(dark_star_elements)
                                            new_dark_star = new_dark_star.replace("{0}", f'{num}')
                                            new_dark_star = new_dark_star.replace("__general_var__", section_var)
                                            new_dark_star = BeautifulSoup(new_dark_star, 'html.parser')
                                            dark_star_elements.replace_with(new_dark_star)
                                        else:
                                            if dark_star_elements:
                                                dark_star_elements.decompose()

                        befor_social_media = '''{assign var="socialLinks"  value=$about['social_links']|json_decode:true}
                                                {assign var="socialLinksArray" value=['telegram'=>'telegramHref','whatsapp'=> 'whatsappHref','instagram' => 'instagramHref','aparat' => 'aparatHref','youtube' => 'youtubeHref','facebook' => 'facebookHref','linkeDin' => 'linkeDinHref']}

                                                {foreach $socialLinks as $key => $val}
                                                        {assign var=$socialLinksArray[$val['social_media']] value=$val['link']}
                                                {/foreach}'''
                        befor_social_media_soup = BeautifulSoup(befor_social_media, "html.parser")
                        social_element = local_section.find(class_='__social_class__')
                        if social_element:
                            social_element.insert_before(befor_social_media_soup)
                            social_element = local_section.find(
                                class_=lambda classes: classes and '__social_class__' in classes)
                            repeatable_social_links = {
                                '__telegram_class__': '{if $telegramHref}{$telegramHref}{/if}',
                                '__whatsapp_class__': '{if $whatsappHref}{$whatsappHref}{/if}',
                                '__instagram_class__': '{if $instagramHref}{$instagramHref}{/if}',
                                '__linkdin_class__': '{if $linkeDinHref}{$linkeDinHref}{/if}',
                                '__aparat_class__': '{if $aparatHref}{$aparatHref}{/if}',
                                '__youtube_class__': '{if $youTubeHref}{$youTubeHref}{/if}',
                            }
                            for key, val in repeatable_social_links.items():
                                helper.replace_attribute(social_element, key, 'href', val)

                        if replace_classes_general != '':
                            for class_name, val in replace_classes_general.items():
                                for atr, value in val.items():
                                    if atr != 'class':
                                        helper.replace_attribute(local_section, class_name, atr, value)
                                    else:
                                        helper.add_class_to_elements(local_section, class_name,value)


        general_section_online = general_section_online.prettify()
        generals_final_content = f'{before_html}\n{generals_section}\n{after_html}'

        general_section_online = helper.unit_test_clean_string(general_section_online)
        generals_final_content = helper.unit_test_clean_string(generals_final_content)

        general_section_online_serialized = helper.serialize_string(general_section_online)
        generals_final_content_serialized = helper.serialize_string(generals_final_content)

        if helper.compare_html_strings(general_section_online_serialized, generals_final_content_serialized):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن اخبار موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.<section class="debug" style="display:none;"><div class="online-section" >' + general_section_online + '</div><div class="unit-test-section"> ' + generals_final_content +'</div></section></div>'

    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str
