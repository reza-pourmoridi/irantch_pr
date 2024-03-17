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
from modular import modular

complex_items_pattern = re.compile(r'__i_modular_c_item_class_(\d+)')
simple_items_pattern = re.compile(r'__i_modular_nc_item_class_(\d+)')
complex_items_class = "__i_modular_c_item_class_"
simple_items_class = "__i_modular_nc_item_class_"
script_directory = os.path.dirname(__file__)  # Get the directory of the script
unit_test_json_files_directory = os.path.join(script_directory, '../update_data/unit_test_data')
menu_data = helper.get_general_data('menu_data')
repeatable_social_links = helper.get_general_data('social_data')
user_data = helper.get_general_data('user_data')
banner_data = helper.get_general_data('banner_data')


def unit_test_banner_gallery(banner_gallery_section, banner_gallery_section_online, lang='fa', modul_data_array = {}):
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
        for num in simple_items_numbers:
            simple_element = banner_gallery_section.find(class_=simple_items_class + num)
            num = int(num)  # Convert 'num' to an integer
            if 0 <= num < len(banner_data) and banner_data[num]:
                num = str(num)
                banner_gallery_replacement_data = {
                    "__title__": banner_data[int(num)]['title'],
                    "__link__": banner_data[int(num)]['link']
                }
                if num == simple_items_numbers[0]:
                    simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                    simple_element = helper.replace_placeholders(simple_element, banner_gallery_replacement_data)
                    simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                    helper.replace_attribute(simple_element, '__image_class__', 'src', banner_data[int(num)]['pic'])
                    helper.replace_attribute(simple_element, '__image_class__', 'alt', banner_data[int(num)]['title'])
                else:
                    simple_element.decompose()
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
            complex_element_final = helper.replace_placeholders(complex_element,banner_gallery_complex_replacement_data)
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            helper.replace_attribute(complex_element, '__image_class__', 'src',banner_data[int(num)]['pic'].format(num))
            helper.replace_attribute(complex_element, '__title_class__', 'alt',banner_data[int(num)]['title'].format(num))

        banner_gallery_section = f'{banner_gallery_section}'
        banner_gallery_section_online = f'{banner_gallery_section_online}'


        # clearing search box
        banner_gallery_section = BeautifulSoup(banner_gallery_section, "html.parser")
        banner_gallery_section_online = BeautifulSoup(banner_gallery_section_online, "html.parser")
        search_box = banner_gallery_section.find(class_='i_modular_searchBox')
        search_box_online = banner_gallery_section_online.find(class_='i_modular_searchBox')
        if search_box and search_box_online:
            search_box.replace_with('')
            search_box_online.replace_with('')
        # clearing search box end

        banner_gallery_section = helper.unit_test_clean_string(f'{banner_gallery_section}')
        banner_gallery_section_online = helper.unit_test_clean_string(f'{banner_gallery_section_online}')

        banner_gallery_section_serialized = helper.serialize_string(banner_gallery_section)
        banner_gallery_section_online_serialized = helper.serialize_string(banner_gallery_section_online)

        if helper.compare_html_strings(banner_gallery_section_online_serialized, banner_gallery_section_serialized):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن  موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">سکشن  خطا دارد..<section class="debug" style="display:none;"><div class="online section" >' + banner_gallery_section_online + '</div><div class="unit-test-section"> ' + banner_gallery_section + '</div></section></div>'
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def unit_test_menu(menu_section, menu_section_online , lang = 'fa', modul_data_array = {}):
    try:


        links = modular.repeatable_links
        repeatable_links = {}
        for key, value in links.items():
            updated_key = key.replace('{$smarty.const.ROOT_ADDRESS}', menu_data['main'])
            updated_key = updated_key.replace('https://{$smarty.const.CLIENT_MAIN_DOMAIN}', menu_data['home'])
            repeatable_links[updated_key] = value


        social_element = menu_section.find(class_=lambda classes: classes and '__social_class__' in classes)
        if social_element:
            for key, val in repeatable_social_links.items():
                helper.replace_attribute(social_element, key, 'href', val)

        helper.replace_attribute_by_text(menu_section, 'ورود  |  ثبت نام' , 'string', "<span class='logined-name'>ورود / ثبت نام</span>")
        helper.replace_attribute_by_text(menu_section, 'ورود یا ثبت نام' , 'string', "<span class='logined-name'>ورود / ثبت نام</span>")
        helper.replace_attribute_by_text(menu_section, 'ورود / ثبت نام' , 'string', "<span class='logined-name'>ورود / ثبت نام</span>")
        helper.replace_attribute_by_text(menu_section, 'الدخول / يسجل' , 'string', "<span class='logined-name'>ورود / ثبت نام</span>")

        helper.replace_attribute(menu_section, '__login_register_class__2', 'href', menu_data['main'] + '''/authenticate''')
        helper.replace_attribute(menu_section, '__login_register_class__', 'href', menu_data['main'] + '''/authenticate''')

        helper.add_class_to_elements(menu_section, '__login_register_class__2','main-navigation__button1')
        helper.add_class_to_elements(menu_section, '__login_register_class__',' main-navigation__button1')
        after_login =  "<div class='main-navigation__sub-menu2 arrow-up show-content-box-login-js' style='display: none'>\r\n    <div class=\"sup-menu-flex\">\r\n        <div class=\"sup-menu-flex-r\">\r\n            <a target=\"_parent\" class=\"log-reg-sub\" href=\"https://192.168.1.100/gds/fa/loginUser\">\r\n                <div>\r\n                    <svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n                    <path d=\"M131.5,472H60.693c-8.538,0-13.689-4.765-15.999-7.606c-3.988-4.906-5.533-11.29-4.236-17.519\r\n                        c20.769-99.761,108.809-172.616,210.445-174.98c1.693,0.063,3.39,0.105,5.097,0.105c1.722,0,3.434-0.043,5.142-0.107\r\n                        c24.853,0.567,49.129,5.24,72.236,13.917c10.34,3.885,21.871-1.352,25.754-11.693c3.883-10.34-1.352-21.871-11.693-25.754\r\n                        c-3.311-1.244-6.645-2.408-9.995-3.512C370.545,220.021,392,180.469,392,136C392,61.01,330.991,0,256,0\r\n                        c-74.991,0-136,61.01-136,136c0,44.509,21.492,84.092,54.643,108.918c-30.371,9.998-58.871,25.546-83.813,46.062\r\n                        c-45.732,37.617-77.529,90.086-89.532,147.743c-3.762,18.066,0.744,36.622,12.363,50.908C25.221,503.847,42.364,512,60.693,512\r\n                        H131.5c11.046,0,20-8.954,20-20C151.5,480.954,142.546,472,131.5,472z M160,136c0-52.935,43.065-96,96-96s96,43.065,96,96\r\n                        c0,51.367-40.554,93.438-91.326,95.885c-1.557-0.028-3.114-0.052-4.674-0.052c-1.564,0-3.127,0.023-4.689,0.051\r\n                        C200.546,229.43,160,187.362,160,136z\"></path>\r\n                        <path d=\"M496.689,344.607c-8.561-19.15-27.845-31.558-49.176-31.607h-62.372c-0.045,0-0.087,0-0.133,0\r\n                        c-22.5,0-42.13,13.26-50.029,33.807c-1.051,2.734-2.336,6.178-3.677,10.193H200.356c-5.407,0-10.583,2.189-14.35,6.068\r\n                        l-34.356,35.388c-7.567,7.794-7.529,20.203,0.085,27.95l35,35.612c3.76,3.826,8.9,5.981,14.264,5.981h65c11.046,0,20-8.954,20-20\r\n                        c0-11.046-8.954-20-20-20h-56.614l-15.428-15.698L208.814,397h137.491c9.214,0,17.235-6.295,19.426-15.244\r\n                        c1.618-6.607,3.648-12.959,6.584-20.596c1.936-5.036,6.798-8.16,12.741-8.16c0.013,0,0.026,0,0.039,0h62.371\r\n                        c5.656,0.013,10.524,3.053,12.705,7.932c5.369,12.012,11.78,30.608,11.828,50.986c0.048,20.529-6.356,39.551-11.739,51.894\r\n                        c-2.17,4.978-7.079,8.188-12.56,8.188c-0.011,0-0.022,0-0.033,0h-63.125c-5.533-0.013-10.716-3.573-12.896-8.858\r\n                        c-2.339-5.671-4.366-12.146-6.197-19.797c-2.571-10.742-13.367-17.366-24.105-14.796c-10.743,2.571-17.367,13.364-14.796,24.106\r\n                        c2.321,9.699,4.978,18.118,8.121,25.738c8.399,20.364,27.939,33.555,49.827,33.606h63.125c0.043,0,0.083,0,0.126,0\r\n                        c21.351-0.001,40.647-12.63,49.18-32.201c6.912-15.851,15.137-40.511,15.072-67.975\r\n                        C511.935,384.434,503.638,360.153,496.689,344.607z\"></path>\r\n                        <circle cx=\"431\" cy=\"412\" r=\"20\"></circle>\r\n                </svg>\r\n\r\n                </div>\r\n                <span>ورود</span>\r\n            </a>\r\n        </div>\r\n        <div class=\"sup-menu-flex-l\">\r\n            <a target=\"_parent\" class=\"log-reg-sub\" href=\"https://192.168.1.100/gds/fa/registerUser\">\r\n                <div>\r\n                    <svg version=\"1.1\" id=\"Capa_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\" viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n                    <circle cx=\"370\" cy=\"346\" r=\"20\"></circle>\r\n                        <path d=\"M460,362c11.046,0,20-8.954,20-20v-74c0-44.112-35.888-80-80-80h-24.037v-70.534C375.963,52.695,322.131,0,255.963,0\r\n                        s-120,52.695-120,117.466V188H112c-44.112,0-80,35.888-80,80v164c0,44.112,35.888,80,80,80h288c44.112,0,80-35.888,80-80\r\n                        c0-11.046-8.954-20-20-20c-11.046,0-20,8.954-20,20c0,22.056-17.944,40-40,40H112c-22.056,0-40-17.944-40-40V268\r\n                        c0-22.056,17.944-40,40-40h288c22.056,0,40,17.944,40,40v74C440,353.046,448.954,362,460,362z M335.963,188h-160v-70.534\r\n                        c0-42.715,35.888-77.466,80-77.466s80,34.751,80,77.466V188z\"></path>\r\n                        <circle cx=\"219\" cy=\"346\" r=\"20\"></circle>\r\n                        <circle cx=\"144\" cy=\"346\" r=\"20\"></circle>\r\n                        <circle cx=\"294\" cy=\"346\" r=\"20\"></circle>\r\n                </svg>\r\n                </div>\r\n                <span>ثبت نام</span>\r\n            </a>\r\n\r\n        </div>\r\n    </div>\r\n    "

        simple_element = menu_section.find(class_=lambda classes: classes and '__login_register_class__' in classes)
        if simple_element is not None:
            for tag in menu_section.find_all():
                if tag is not None and tag.decode() == simple_element.decode():
                    new_tag = BeautifulSoup(f'{simple_element}\n{after_login}')
                    simple_element.replace_with(new_tag)

        for key, val_set in repeatable_links.items():
            for text in val_set:
                helper.replace_attribute_by_text(menu_section, text, 'href', key)

        menu_section_online = menu_section_online.prettify()
        menu_section = menu_section.prettify()
        menu_section = menu_section.replace("__main_link_href__", menu_data['home'])

        menu_section = f'{menu_section}'
        menu_section = menu_section.replace("__main_link__", "http://192.168.1.100")


        menu_section_online = helper.unit_test_clean_string(menu_section_online)
        menu_section = helper.unit_test_clean_string(menu_section)

        menu_section_online_serialized = helper.serialize_string(menu_section_online)
        menu_section_serialized = helper.serialize_string(menu_section)

        if helper.compare_html_strings(menu_section_online_serialized, menu_section_serialized):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن منوی هدر موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="online section" >' + menu_section_online + '</div><div class="unit-test-section"> ' + menu_section +'</div></section></div>'

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def unit_test_footer(footer_section, footer_section_online , lang = 'fa', modul_data_array = {}):
    try:

        social_element = footer_section.find(class_=lambda classes: classes and '__social_class__' in classes)
        if social_element:
            for key, val in repeatable_social_links.items():
                helper.replace_attribute(social_element, key, 'href', val)
        
        links = modular.repeatable_links
        repeatable_links = {}
        for key, value in links.items():
            updated_key = key.replace('{$smarty.const.ROOT_ADDRESS}', menu_data['main'])
            updated_key = updated_key.replace('https://{$smarty.const.CLIENT_MAIN_DOMAIN}', menu_data['home'])
            repeatable_links[updated_key] = value

        for key, val_set in repeatable_links.items():
            for text in val_set:
                helper.replace_attribute_by_text(footer_section, text, 'href', key)

        helper.replace_attribute(footer_section, '__aboutUs_class__', 'string',user_data['about'])
        helper.replace_attribute(footer_section, '__aboutUs_class_href__', 'href', menu_data['main'] + '''/aboutUs''')
        helper.replace_attribute(footer_section, '__address_class__', 'string',user_data['address'])
        helper.replace_attribute(footer_section, '__mobile_class__', 'string', user_data['mobile'])
        helper.replace_attribute(footer_section, '__mobile_class__', 'href', 'tel:' + user_data['mobile'])
        helper.replace_attribute(footer_section, '__phone_class__', 'string', user_data['phone'])
        helper.replace_attribute(footer_section, '__phone_class__', 'href', 'tel:' + user_data['phone'])
        helper.replace_attribute(footer_section, '__email_class__', 'string', user_data['email'])
        helper.replace_attribute(footer_section, '__email_class__', 'href','mailto:' + user_data['email'])
        footer_section = helper.replace_placeholders(footer_section,{'__aboutUsLink__':  menu_data['main'] + '/aboutUs'})

        footer_section = BeautifulSoup(footer_section, "html.parser")

        footer_section_online = footer_section_online.prettify()
        footer_section = footer_section.prettify()

        footer_section_online = f'{footer_section_online}'
        footer_section = f'{footer_section}'

        footer_section_online = helper.unit_test_clean_string(footer_section_online)
        footer_section = helper.unit_test_clean_string(footer_section)

        footer_section_online_serialized = helper.serialize_string(footer_section_online)
        footer_section_serialized = helper.serialize_string(footer_section)

        if helper.compare_html_strings(footer_section_online_serialized, footer_section_serialized):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن  موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="online section" >' + footer_section_online + '</div><div class="unit-test-section"> ' + footer_section +'</div></section></div>'

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def test_unit_test(a, b, c, modul_data_array = {}):
    return 'test'


def unit_test_header(soup, soup_online , lang = 'fa', modul_data_array = {}):
    try:
        header_section = soup.find('head')
        header_section_online = soup_online.find('head')

        css_links = [helper.clean_links(link.get('href')) for link in header_section.find_all('link')]
        css_links_online_initial = [link.get('href') for link in header_section_online.find_all('link')]
        css_links_online = [helper.clean_links(link.get('href')) for link in header_section_online.find_all('link')]

        #deleting additional links
        css_links = [path for path in css_links if 'css' in path]
        css_links_online = [path for path in css_links_online if 'project_files/css' in path]
        css_links_online_initial = [path for path in css_links_online_initial if 'project_files/css' in path]
        final_css_links_online = [path.replace("project_files/", "") for path in css_links_online]

        befor_all = modular.befor_all_css
        between_mainPage_assets = modular.between_mainPage_assets_css
        not_inside_mainPage = modular.not_inside_mainPage_css
        after__all_pags_mainpage = modular.after__all_pags_mainpage_css
        after__all = modular.after__all_css

        final_css_links = []
        final_css_links = final_css_links +  [path for path in befor_all if path in css_links]
        final_css_links = final_css_links +  [path for path in css_links if path not in befor_all and path not in between_mainPage_assets
                                              and path not in not_inside_mainPage and path not in after__all_pags_mainpage  and path not in after__all]
        final_css_links = final_css_links +  [path for path in between_mainPage_assets if path in css_links]
        final_css_links = final_css_links +  [path for path in not_inside_mainPage if path in css_links]
        final_css_links = final_css_links +  [path for path in after__all_pags_mainpage if path in css_links]
        final_css_links = final_css_links +  [path for path in after__all if path in css_links]

        if helper.check_url_real(css_links_online_initial):
            return f'{helper.check_url_real(css_links_online_initial)}'

        if final_css_links_online != final_css_links:
            return '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="online css" >' + f'{final_css_links_online}' + '</div><div class="unit test css"> ' + f'{final_css_links}' + '</div></section></div>'

        return '<div style="background: green;padding: 15px;">' + "تست سکشن  موفقیت آمیز بود." + "</div>"

    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message



def unit_test_script_footer(soup, soup_online , lang = 'fa', modul_data_array = {}):
    try:
        error = False
        error_massage = ''
        script_footer_section = soup
        script_footer_section_online = soup_online

        js_links = [helper.clean_links(link.get('src')) for link in script_footer_section.find_all('script') if link is not None]
        js_links_online_initial = [link.get('src') for link in script_footer_section_online.find_all('script') if link is not None]
        js_links_online = [helper.clean_links_js(link.get('src')) for link in script_footer_section_online.find_all('script') if link is not None]


        #deleting additional links
        js_links = [path for path in js_links if path is not None and 'js' in path]
        js_links_online = [path for path in js_links_online if path is not None and 'project_files/js' in path]
        js_links_online_initial = [path for path in js_links_online_initial if path is not None and 'project_files/js' in path]
        final_js_links_online = [path.replace("project_files/", "") for path in js_links_online if path is not None]


        befor_all = modular.befor_all_js
        between_mainPage_assets = modular.between_mainPage_assets_js
        inside_mainPage = modular.inside_mainPage_js
        remove_assets = modular.remove_assets_js
        after__all = modular.after__all_js

        final_js_links = []
        final_js_links = final_js_links + [path for path in remove_assets if path in js_links]
        final_js_links = final_js_links + [path for path in befor_all if path in js_links]
        final_js_links = final_js_links + [path for path in js_links if  path not in final_js_links and path not in between_mainPage_assets and path not in inside_mainPage and path not in after__all]
        final_js_links = final_js_links + [path for path in between_mainPage_assets if path in js_links]
        final_js_links = final_js_links + [path for path in inside_mainPage if path in js_links]
        final_js_links = final_js_links + [path for path in after__all if path in js_links]


        if helper.check_url_real(js_links_online_initial):
            error = True
            error_massage = error_massage + f'{helper.check_url_real(js_links_online_initial)}'

        if final_js_links_online != final_js_links:
            error = True
            error_massage = error_massage +  '<div style="background: red;padding: 15px;"><section class="debug" style="display:none;"><div class="online js" >' + f'{final_js_links_online}' + '</div><div class="unit test js"> ' + f'{final_js_links}' + '</div></section></div>'


        if error:
            return error_massage
        else:
            return '<div style="background: green;padding: 15px;">' + "تست سکشن  موفقیت آمیز بود." + "</div>"
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message


def unit_test_other(soup, soup_online , lang = 'fa', modul_data_array = {}):
    try:
        error = False
        error_massage = ''

        corrupted_imgs = []
        for img in soup_online.find_all('img'):
            if not img.get('alt'):
                imgg = '<xmp>' + f'{img}' + '</xmp>'
                corrupted_imgs.append(imgg)

        if corrupted_imgs:
            error = True
            error_massage = error_massage + 'this images do not have any alt ' + f'{corrupted_imgs}'


        corrupted_links = []
        links = []
        for link in soup_online.find_all('a'):
            if not link.get('href'):
                linkk = '<xmp>' + f'{link}' + '</xmp>'
                corrupted_links.append(linkk)
            else:
                links.append(link.get('href'))


        if corrupted_links:
            error = True
            error_massage = error_massage + 'this links are empty ' + f'{corrupted_links}'

        if helper.check_url_real(links):
            error = True
            error_massage = error_massage + helper.check_url_real(links)


        if error:
            return error_massage
        else:
            return '<div style="background: green;padding: 15px;">' + "سایر تست ها  موفقیت آمیز بود." + "</div>"
    except requests.exceptions.RequestException as e:
        trace = traceback.format_exc()
        error_message = f"خطایی در ماژول گذار پیش آمد در: {trace}"
        return error_message







def initiate_general_test(general_section, general_section_online , lang = 'fa' , modul_data_array = {}):
    try:
        unit_test = general_test(general_section, general_section_online, lang, modul_data_array)
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
                    general_data = helper.get_general_data(unique_key)
                else:
                    sections = generals_section.find_all(class_=section_class)
                    general_data = helper.get_general_data(section_class)

                if not isinstance(general_data, (dict, list)):
                    return '<div style="background: red;padding: 15px;">data is empty</div>'

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
                                    pattern = r"(.*)\{\$item\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?\}"
                                    output_string = helper.get_element_data_key_by_pattern(general_data[int(numInt)],pattern, item_val)
                                    final_generals_simple_replacements[item_pointer] = output_string

                                simple_element = helper.replace_placeholders(simple_element, final_generals_simple_replacements)
                                simple_element = local_section.find(class_=simple_items_class + num)
                                for class_name, val in replace_classes_local.items():
                                    for atr, value in val.items():
                                        pattern = r"(.*)\{\$item\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?\}"
                                        value = helper.get_element_data_key_by_pattern(general_data[int(numInt)], pattern, value)
                                        helper.replace_attribute(simple_element, class_name, atr, value)

                                for i in range(1, 6):
                                    light_star_elements = simple_element.find(class_='__star_class_light__' + str(i))
                                    dark_star_elements = simple_element.find(class_='__star_class_dark__' + str(i))

                                    # before_star_simple = modul_data_array['before_star_simple']
                                    # before_dark_star_simple = modul_data_array['before_dark_star_simple']
                                    # pattern = r"(.*)\{\$item\[['\"]rate_average['\"]\](?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?\}"
                                    # match_combined = re.search(pattern, before_star_simple)
                                    # return f'{match_combined(1)}'

                                    if i <= 1 and light_star_elements:
                                        new_light_star =  str(light_star_elements)
                                        new_light_star = BeautifulSoup(new_light_star, 'html.parser')
                                        light_star_elements.replace_with(new_light_star)
                                    else:
                                        if light_star_elements:
                                            light_star_elements.decompose()

                                    if i <= 1 and dark_star_elements:
                                        new_dark_star =  str(dark_star_elements)
                                        new_dark_star = BeautifulSoup(new_dark_star, 'html.parser')
                                        dark_star_elements.replace_with(new_dark_star)
                                    else:
                                        if dark_star_elements:
                                            dark_star_elements.decompose()

                            elif simple_element:
                                simple_element.decompose()


                        for num in complex_items_numbers:
                            numInt = int(num)
                            if 0 <= numInt < len(general_data):
                                complex_element = local_section.find(class_=complex_items_class + num)
                                final_gcr = {}
                                for gcr_key, gcr_val in generals_complex_replacements.items():
                                    pattern = r"(.*)\{\$__general_var__\[\{0}\]\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?\}"
                                    valuefinal = helper.get_element_data_key_by_pattern(general_data[int(numInt)],pattern, gcr_val)
                                    final_gcr = {
                                        f'{gcr_key}': f'{valuefinal}'
                                    }

                                complex_element = helper.replace_placeholders(complex_element, final_gcr)

                                complex_element = local_section.find(class_=complex_items_class + num)
                                for class_name, val in replace_comlex_classes_local.items():
                                    for atr, value in val.items():
                                        pattern = r"(.*)\{\$__general_var__\[\{0}\]\[['\"](.+?)['\"]\](?:\[['\"](.+?)['\"]\])?(?:\[['\"](.+?)['\"]\])?\}"
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

                        befor_social_media = ''''''
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

        generals_final_content = generals_final_content.replace("__all_link_href__", menu_data['main'] + "/page/" + special_page)

        general_section_online = helper.unit_test_clean_string(general_section_online)
        generals_final_content = helper.unit_test_clean_string(generals_final_content)

        general_section_online_serialized = helper.serialize_string(general_section_online)
        generals_final_content_serialized = helper.serialize_string(generals_final_content)

        if helper.compare_html_strings(general_section_online_serialized, generals_final_content_serialized):
            return '<div style="background: green;padding: 15px;">' + "تست سکشن  موفقیت آمیز بود." + "</div>"

        return '<div style="background: red;padding: 15px;">طرح و سکشن  ماژول گذاری شده هماهنگ نیستند.<section class="debug" style="display:none;"><div class="online-section" >' + general_section_online + '</div><div class="unit-test-section"> ' + generals_final_content +'</div></section></div>'

    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str
