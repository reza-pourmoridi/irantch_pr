from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs
from modular import helper_functions as helper
from modular import unit_test

complex_items_pattern = re.compile(r'__i_modular_c_item_class_(\d+)')
simple_items_pattern = re.compile(r'__i_modular_nc_item_class_(\d+)')
complex_items_class = "__i_modular_c_item_class_"
simple_items_class = "__i_modular_nc_item_class_"

def initiation_progress():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    if 'project_name' not in request.form:
        return jsonify({"message": "No project name"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})

    lang = 'fa'

    project_path = helper.create_folder(request.form['project_name'])
    copy_repeated_file_folders_massage = helper.copy_repeated_file_folders(request.form['project_name'])
    html_content = file.read()
    # turn string to soup object
    soup = BeautifulSoup(html_content, 'html.parser')
    if not soup:
        return jsonify({"message": "testing html = " + f'{soup}'})



    moduls_array = {
            'blog': {
                'class': 'i_modular_blog',
                'file': 'blog.tpl',
                'name': 'وبلاگ',
                'modular': blog_module,
                'test_function': unit_test.unit_test_blog
            },
            'newsletter': {
                'class': 'i_modular_newsletter',
                'name': 'خبرنامه',
                'file': 'newsletter.tpl',
                'modular': newsletter_module,
                'test_function': unit_test.unit_test_newsletter
            },
            'news': {
                'class': 'i_modular_news',
                'name': 'اخبار',
                'file': 'news.tpl',
                'modular': news_module,
                'test_function': unit_test.unit_test_news
            },
            'menu': {
                'class': 'i_modular_menu',
                'name': 'منو',
                'file': 'menu.tpl',
                'modular': menu_module,
                'test_function': unit_test.unit_test_menu
            },
            'footer': {
                'class': 'i_modular_footer',
                'name': 'فوتر',
                'file': 'footer.tpl',
                'modular': footer_module,
                'test_function': unit_test.unit_test_footer
            },
            'banner_gallery': {
                'class': 'i_modular_banner_gallery',
                'name': 'گالری بنر',
                'file': 'banner.tpl',
                'modular': banner_gallery_module,
                'test_function': unit_test.unit_test_banner_gallery
            },
            'header': {
                'class': 'i_modular_header',
                'name': 'هدر',
                'file': 'header.tpl',
                'modular': header_module,
                'test_function': unit_test.test_unit_test

            },
            'footer_script': {
                'class': 'i_modular_footer_script',
                'name': 'اسکریپت فوتر',
                'file': 'footer-script.tpl',
                'modular': footer_script_module,
                'test_function': unit_test.test_unit_test

            },
            'fast_search_flight': {
                'class': 'i_modular_fast_search_flight',
                'name': 'جستجوی سریع پرواز',
                'file': 'fast_search_flight.tpl',
                'modular': fast_search_flight_module,
                'test_function': unit_test.test_unit_test

            },
        }

    moduls_array = {
            # 'menu': {
            #     'class': 'i_modular_menu',
            #     'name': 'منو',
            #     'file': 'menu.tpl',
            #     'modular': menu_module,
            #     'test_function': unit_test.unit_test_menu
            # },
            # 'header': {
            #     'class': 'i_modular_header',
            #     'name': 'هدر',
            #     'file': 'header.tpl',
            #     'modular': header_module,
            #     'test_function': unit_test.test_unit_test
            #
            # },
            # 'footer_script': {
            #     'class': 'i_modular_footer_script',
            #     'name': 'اسکریپت فوتر',
            #     'file': 'footer-script.tpl',
            #     'modular': footer_script_module,
            #     'test_function': unit_test.test_unit_test
            #
            # },
            # 'fast_search_flight': {
            #     'class': 'i_modular_fast_search_flight',
            #     'name': 'جستجوی سریع پرواز',
            #     'file': 'fast_search_flight.tpl',
            #     'modular': fast_search_flight_module,
            #     'test_function': unit_test.test_unit_test
            #
            # },

            'hotels_webservice': {
                'class': 'i_modular_hotels_webservice',
                'name': 'هتل وب سرویس',
                'file': 'hotels-webservice.tpl',
                'modular': hotels_webservice_module,
                'test_function': unit_test.test_unit_test

            },
        }

    module_messages = []



    main_page_array = {}
    for module_name, module_info in moduls_array.items():
        section = soup.find(class_=module_info['class'])
        if section:
            main_page_array[f'{section}'] = "{" + module_info['name'] + ".tpl}"
            module_messages.append("<br><br> تست ماژول گذاری بخش " + module_info['name'] + " = " + module_info['modular'](section, project_path , lang))

    summary_message = '\n'.join(module_messages)

    return jsonify({"message": f'{summary_message}'
})

    #creation of mainPage
    soup = BeautifulSoup(html_content, 'html.parser')

    for module_key, module_info in moduls_array.items():
        class_name = module_info['class']
        file_name = '{include file="include_files/' + module_info['file'] + '"}'
        elements = soup.find_all(class_=class_name)

        for element in elements:
            # Replace the old element with the 'file' string
            element.replace_with(file_name)

    modified_html_content = str(soup)
    soup_str = f'{modified_html_content}'
    main_page = helper.create_file(soup_str, project_path, 'mainPage2', 'tpl')

    # UNIT TEST
    soup = BeautifulSoup(html_content, 'html.parser')
    if not soup:
        return jsonify({"message": "testing html = " + f'{soup}'})

    soup_online = unit_test.get_online_html()
    if 'خطایی' in soup_online:
        return jsonify({"message": "testing local connection = " + f'{soup_online}'})
    module_test_messages = []

    for module_name, module_info in moduls_array.items():
        section = soup.find(class_=module_info['class'])
        if section:
            module_test_messages.append("<br><br> تست بخش  " + module_info['name'] + " = " + initiation_test(module_info['class'], module_info['name'], module_info['test_function'] , soup, soup_online ,lang))
    summary_test_message = '\n'.join(module_test_messages)

    return jsonify({"message": f'{summary_message}'
           +  '<br><br><br>' 'main_page_creation' + f'{main_page}'
           +  '<br><br><br>' + f'{summary_test_message}'})

def initiation_test(class_name, module_name, module_test_function, soup, soup_online , lang):
    section = soup.find(class_=class_name)
    section_online = soup_online.find(class_=class_name) if section else None

    if section_online:
        return module_test_function(section, section_online , lang)

    return f'ماژول {module_name} بازگذاری نشد'

def initiation_modulation(class_name, module_name, modular_function, soup, soup_online):
    section = soup.find(class_=class_name)
    section_online = soup_online.find(class_=class_name) if section else None

    if section_online:
        return module_test_function(section, section_online)

    return f'ماژول {module_name} بازگذاری نشد'

def banner_gallery_module(banner_gallery_section, project_path , lang = 'fa'):
    try:
        # create regex objects containing patterns of items classes
        complex_items_numbers = helper.item_numbers(banner_gallery_section,complex_items_pattern)
        simple_items_numbers = helper.item_numbers(banner_gallery_section,simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        before_html = '''{assign var="type_data" value=['is_active'=>1 , 'limit' =>10]}
                        {assign var='banners' value=$obj_main_page->galleryBannerMain($type_data)}'''
        after_html = ''

        before_foreach = '''{foreach $banners as $key => $banner}'''
        after_foreach = '''{/foreach}'''

        for num in simple_items_numbers:
            banner_gallery_replacement_data = {
                "__title__": '''{$banner['title']}''',
                "__link__": '''{$banner['link']}'''
            }
            simple_element = banner_gallery_section.find(class_=simple_items_class + num)
            if num == simple_items_numbers[0]:
                helper.add_before_after(banner_gallery_section, simple_items_class + num, before_foreach,after_foreach)
                simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                simple_element = helper.replace_placeholders(simple_element, banner_gallery_replacement_data)
                simple_element = banner_gallery_section.find(class_=simple_items_class + num)
                helper.replace_attribute(simple_element, '__image_class__', 'src','{$banner["pic"]}')
                helper.replace_attribute(simple_element, '__image_class__', 'alt','{$banner["title"]}')

            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            before_if = '''{if banners[{0}] }'''
            before_if = before_if.replace("{0}", num)
            after_if = '''{/if}'''

            banner_gallery_complex_replacement_data = {
                "__link__": '''{{banners[{0}]['link']}}'''.format(num),
                "__title__": '''{{banners[{0}]['title']}}'''.format(num),
            }
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            helper.add_before_after(banner_gallery_section, complex_items_class + num, before_if, after_if)
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            complex_element_final = helper.replace_placeholders(complex_element, banner_gallery_complex_replacement_data)
            complex_element = banner_gallery_section.find(class_=complex_items_class + num)
            helper.replace_attribute(complex_element, '__image_class__', 'src', '''{{banners[{0}]['pic']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title_class__', 'alt', '''{{banners[{0}]['title']}}'''.format(num))


        banner_gallery_final_content = f'{before_html}\n{banner_gallery_section}\n{after_html}'


        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/banner-gallery.tpl'}")
        banner_gallery_final_content = banner_gallery_final_content.replace("&gt;", ">")
        banner_gallery_final_content = banner_gallery_final_content.replace("&lt;", "<")

        return helper.create_file(banner_gallery_final_content, include_files_directory, 'banner_gallery', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def news_module(news_section, project_path , lang = 'fa'):
    try:
        # create regex objects containing patterns of items classes
        complex_items_numbers = helper.item_numbers(news_section,complex_items_pattern)
        simple_items_numbers = helper.item_numbers(news_section,simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        before_html = '''{assign var="main_articles" value=$obj_main_page->getNewsArticles()}
                            {assign var="othe_itmes" value=$main_articles['data']}
                            {assign var="i" value="2"}
                            {assign var='counter' value=0}
                            {if $main_articles['count'] > 0 }'''
        after_html = '{/if}'

        before_foreach = '''{foreach $othe_itmes as $item} {if $counter >= i_modular__min_for_limit and $counter <= i_modular__max_for_limit}'''
        before_foreach = before_foreach.replace("i_modular__min_for_limit", simple_items_numbers_min)
        before_foreach = before_foreach.replace("i_modular__max_for_limit", simple_items_numbers_max)
        after_foreach = '''{/if}{$counter = $counter + 1}{/foreach}'''

        for num in simple_items_numbers:
            news_replacement_data = {
                "__link__": '''{$item['link']}''',
            }
            simple_element = news_section.find(class_=simple_items_class + num)
            if num == simple_items_numbers[0]:
                helper.add_before_after(news_section, simple_items_class + num, before_foreach, after_foreach)
                simple_element = news_section.find(class_=simple_items_class + num)
                simple_element = helper.replace_placeholders(simple_element, news_replacement_data)
                simple_element = news_section.find(class_=simple_items_class + num)
                helper.replace_attribute(simple_element, '__image_class__', 'src','{$item["image"]}')
                helper.replace_attribute(simple_element, '__image_class__', 'alt','{$item["alt"]}')
                helper.replace_attribute(simple_element, '__title_class__', 'string','{$item["title"]}')
                helper.replace_attribute(simple_element, '__heading_class__', 'string','{$item["heading"]}')
                helper.replace_attribute(simple_element, '__description_class__', 'string','{$item["description"]}')

            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            before_if = '''{if $othe_itmes[{0}] }'''
            before_if = before_if.replace("{0}", num)
            after_if = '''{/if}'''

            news_complex_replacement_data = {
                "__link__": '''{{$othe_itmes[{0}]['link']}}'''.format(num),
                "__alt_article__": '''{{$othe_itmes[{0}]['title']}}'''.format(num),
                'images/5497750661271-6.jpg': '''{{$othe_itmes[{0}]['image']}}'''.format(num),
                '<span class="__date__">5 بهمن 1402</span>': '''{{$othe_itmes[{0}]['created_at']}}'''.format(num),
                '<span class="__comments_number__">450</span>': '''{{$othe_itmes[{0}]['comments_count']['comments_count']}}'''.format(num)
            }
            complex_element = news_section.find(class_=complex_items_class + num)
            helper.add_before_after(news_section, complex_items_class + num, before_if, after_if)
            complex_element = news_section.find(class_=complex_items_class + num)
            complex_element_final = helper.replace_placeholders(complex_element, news_complex_replacement_data)
            complex_element = news_section.find(class_=complex_items_class + num)
            helper.replace_attribute(complex_element, '__image_class__', 'src', '''{{$othe_itmes[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__image_class__', 'alt', '''{{$othe_itmes[{0}]['alt']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title_class__', 'string', '''{{$othe_itmes[{0}]['title']}}'''.format(num))
            helper.replace_attribute(complex_element, '__heading_class__', 'string', '''{{$othe_itmes[{0}]['heading']}}'''.format(num))
            helper.replace_attribute(complex_element, '__description_class__', 'string', '''{{$othe_itmes[{0}]['description']}}'''.format(num))


        news_final_content = f'{before_html}\n{news_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/news.tpl'}")
        news_final_content = news_final_content.replace("&gt;", ">")
        news_final_content = news_final_content.replace("&lt;", "<")

        return helper.create_file(news_final_content, include_files_directory, 'news', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def newsletter_module(newsletter_section, project_path , lang = 'fa'):
    try:
        helper.replace_attribute(newsletter_section, '__name_class__', 'name','NameSms')
        helper.replace_attribute(newsletter_section, '__email_class__', 'name','EmailSms')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'name','CellSms')

        helper.replace_attribute(newsletter_section, '__name_class__', 'id','NameSms')
        helper.replace_attribute(newsletter_section, '__email_class__', 'id','EmailSms')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'id','CellSms')

        helper.replace_attribute(newsletter_section, '__name_class__', 'class','full-name-js')
        helper.replace_attribute(newsletter_section, '__email_class__', 'class','email-js')
        helper.replace_attribute(newsletter_section, '__phone_class__', 'class','mobile-js')

        helper.replace_attribute(newsletter_section, '__submit_class__', 'onclick','submitNewsLetter()')


        newsletter_final_content = f'{newsletter_section}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/newsletter.tpl'}")
        newsletter_final_content = newsletter_final_content.replace("&gt;", ">")
        newsletter_final_content = newsletter_final_content.replace("&lt;", "<")

        return helper.create_file(newsletter_final_content, include_files_directory, 'newsletter', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def menu_module(menu_section, project_path , lang = 'fa'):
    try:


        repeatable_links = {
            'fa':{
                'پرواز': '{$smarty.const.ROOT_ADDRESS}/page/flight',
                'هتل': '{$smarty.const.ROOT_ADDRESS}/page/hotel',
                'بیمه': '{$smarty.const.ROOT_ADDRESS}/page/insurance',
                'انتقاد و پیشنهادات': '{$smarty.const.ROOT_ADDRESS}/feedback',
                'نظر سنجی': '{$smarty.const.ROOT_ADDRESS}/vote',
                'باشگاه مسافران': '{$smarty.const.ROOT_ADDRESS}/loginUser',
                'پیگیری خرید': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
                'وبلاگ': '{$smarty.const.ROOT_ADDRESS}/mag',
                'ویدئو ها': '{$smarty.const.ROOT_ADDRESS}/video',
                'نمایندگی ها': '{$smarty.const.ROOT_ADDRESS}/agencyList',
                'همکاری با ما': '{$smarty.const.ROOT_ADDRESS}/همکاری با ما',
                'نرخ ارز': '{$smarty.const.ROOT_ADDRESS}/currency',
                'سفر نامه': '{$smarty.const.ROOT_ADDRESS}/recommendation',
                'سفارت': '{$smarty.const.ROOT_ADDRESS}/embassies',
                'پرسش و پاسخ': '{$smarty.const.ROOT_ADDRESS}/faq',
                'دقیقه 90': '{$smarty.const.ROOT_ADDRESS}/lastMinute',
                'اخبار سایت': '{$smarty.const.ROOT_ADDRESS}/news',
                'معرفی ايران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
                'قوانین و مقررات': '{$smarty.const.ROOT_ADDRESS}/rules',
                'درباره ما': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
                'تماس با ما': '{$smarty.const.ROOT_ADDRESS}/contactUs',
                'پرداخت آنلاین': '{$smarty.const.ROOT_ADDRESS}/pay',
            },
            'ar' : {
                'رحلة جوية': '{$smarty.const.ROOT_ADDRESS}/page/flight',
                'ترتيب المسار': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
                'مدونة': '{$smarty.const.ROOT_ADDRESS}/mag',
                'الخدمات السياحية': '{$smarty.const.ROOT_ADDRESS}/orderServices',
                'مقدمة عن إيران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
                'الفندق إيران': '{$smarty.const.ROOT_ADDRESS}/hotel',
                'تأشيرة إيران': '{$smarty.const.ROOT_ADDRESS}/iran-visa',
                'شبكة': '{$smarty.const.ROOT_ADDRESS}/tour',
                'الأحكام والشروط': '{$smarty.const.ROOT_ADDRESS}/rules',
                'ساعة البلدان': '{$smarty.const.ROOT_ADDRESS}/worldclock',
                'معلومات عنا': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
                'اتصل بنا': '{$smarty.const.ROOT_ADDRESS}/contactUs',
                'علم الارصاد الجوية': '{$smarty.const.ROOT_ADDRESS}/weather',
            }
        }

        repeatable_lists = {
            'fa':{
                'تور داخلی' : ''' <a href="javascript:;"> تور داخلی </a>
                                    <ul class="nav-dropdown submenu-child fadeIn animated">
                                        {foreach key=key_tour item=item_tour from=$objResult->ReservationTourCities('=1', 'return')}
                                            <li>
                                                <a href="{$smarty.const.ROOT_ADDRESS}/resultTourLocal/1-all/1-{$item_tour.id}/{$objDate->jdate("Y-m-d", '', '', '', 'en')}/all">
                                                    {($smarty.const.SOFTWARE_LANG == 'fa') ? $item_tour.name : $item_tour.name_en}
                                                </a>
                                            </li>
                                        {/foreach}


                                    </ul>
                                ''',
                'تور خارجی' : '''<a href="javascript:;"> تور خارجی </a>
                                    <ul class="nav-dropdown submenu-child fadeIn animated">
                                        {foreach key=key_tour item=item_tour from=$objResult->ReservationTourCountries('yes')}
                                            <li>
                                                <a href="{$smarty.const.ROOT_ADDRESS}/resultTourLocal/1-all/{$item_tour.id}-all/{$objDate->jdate("Y-m-d", '', '', '', 'en')}/all">
                                                    {($smarty.const.SOFTWARE_LANG == 'fa') ? $item_tour.name : $item_tour.name_en}
                                                </a>
                                            </li>
                                        {/foreach}
                                    </ul>
                                ''',

            }
        }

        helper.replace_attribute_by_text(menu_section, 'ورود یا ثبت نام' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute_by_text(menu_section, 'الدخول / يسجل' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute(menu_section, '__login_register_class__2', 'class','__login_register_class__2 main-navigation__button2 show-box-login-js')
        helper.replace_attribute(menu_section, '__login_register_class__', 'class','__login_register_class__ main-navigation__button2 show-box-login-js button_header logIn d-flex d-lg-none')


        after_login = '''<div class="main-navigation__sub-menu2 arrow-up show-content-box-login-js" style="display: none">
                            {include file="`$smarty.const.FRONT_CURRENT_THEME`topBar.tpl"}
                        </div>'''

        simple_element = menu_section.find(class_=lambda classes: classes and '__login_register_class__' in classes)
        for tag in menu_section.find_all():
            if tag.decode() == simple_element.decode():
                new_tag = BeautifulSoup(f'{simple_element}\n{after_login}')
                simple_element.replace_with(new_tag)

        # return f'{menu_section}'

        for key, val in repeatable_links[lang].items():
            helper.replace_attribute_by_text(menu_section, key, 'href', val)

        for key, val in repeatable_lists[lang].items():
            helper.replace_attribute_by_text(menu_section, key, 'string', val)



        menu_final_content = f'{menu_section}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/menu.tpl'}")
        menu_final_content = menu_final_content.replace("__main_link__", "https://{$smarty.const.CLIENT_MAIN_DOMAIN}")
        menu_final_content = menu_final_content.replace("&gt;", ">")
        menu_final_content = menu_final_content.replace("&lt;", "<")

        return helper.create_file(menu_final_content, include_files_directory, 'menu', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def footer_module(footer_section, project_path, lang='fa'):
    try:
        return 'lsdfj'
        before_html = '''{load_presentation_object filename="aboutUs" assign="objAbout"}
                            {assign var="about"  value=$objAbout->getData()}
                            {assign var="socialLinks"  value=$about['social_links']|json_decode:true}


                            {if $smarty.session.layout neq 'pwa'}
                                {if $smarty.const.GDS_SWITCH neq $smarty.const.ConstPrintHotel && $smarty.const.GDS_SWITCH neq $smarty.const.ConstPrintTicket && $smarty.const.GDS_SWITCH neq $smarty.const.ConstPrintHotelReservation && $smarty.const.GDS_SWITCH neq $smarty.const.ConstPrintHotelReservationAhuan}
                                   '''
        after_html = '''    {/if}
                            {else}
                                {include file="`$smarty.const.FRONT_CURRENT_CLIENT`pwaFooter.tpl"}
                            {/if}'''

        befor_social_media = '''{assign var="socialLinks"  value=$about['social_links']|json_decode:true}
                                {assign var="socialLinksArray" value=['telegram'=>'telegramHref','whatsapp'=> 'whatsappHref','instagram' => 'instagramHref']}

                                {foreach $socialLinks as $key => $val}
                                        {assign var=$socialLinksArray[$val['social_media']] value=$val['link']}
                                {/foreach}'''
        befor_social_media_soup = BeautifulSoup(befor_social_media, "html.parser")
        social_element = footer_section.find(class_=lambda classes: classes and '__social_class__' in classes)
        social_element.insert_before(befor_social_media_soup)

        social_element = footer_section.find(class_=lambda classes: classes and '__social_class__' in classes)
        repeatable_social_links = {
            '__telegram_class__': '{if $telegramHref}{$telegramHref}{/if}',
            '__whatsapp_class__': '{if $telegramHref}{$whatsappHref}{/if}',
            '__instagram_class__': '{if $telegramHref}{$instagramHref}{/if}',
        }

        for key, val in repeatable_social_links.items():
            helper.replace_attribute(social_element, key, 'href', val)

        repeatable_links = {
            'fa': {
                'پرواز': '{$smarty.const.ROOT_ADDRESS}/page/flight',
                'پیگیری خرید': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
                'وبلاگ': '{$smarty.const.ROOT_ADDRESS}/mag',
                'اخبار سایت': '{$smarty.const.ROOT_ADDRESS}/news',
                'معرفی ايران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
                'قوانین و مقررات': '{$smarty.const.ROOT_ADDRESS}/rules',
                'درباره ما': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
                'تماس با ما': '{$smarty.const.ROOT_ADDRESS}/contactUs',
                'پرداخت آنلاین': '{$smarty.const.ROOT_ADDRESS}/pay',
            },
            'ar': {
                'رحلة جوية': '{$smarty.const.ROOT_ADDRESS}/page/flight',
                'ترتيب المسار': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
                'مدونة': '{$smarty.const.ROOT_ADDRESS}/mag',
                'الخدمات السياحية': '{$smarty.const.ROOT_ADDRESS}/orderServices',
                'مقدمة عن إيران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
                'الفندق إيران': '{$smarty.const.ROOT_ADDRESS}/hotel',
                'تأشيرة إيران': '{$smarty.const.ROOT_ADDRESS}/iran-visa',
                'شبكة': '{$smarty.const.ROOT_ADDRESS}/tour',
                'الأحكام والشروط': '{$smarty.const.ROOT_ADDRESS}/rules',
                'ساعة البلدان': '{$smarty.const.ROOT_ADDRESS}/worldclock',
                'معلومات عنا': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
                'اتصل بنا': '{$smarty.const.ROOT_ADDRESS}/contactUs',
                'علم الارصاد الجوية': '{$smarty.const.ROOT_ADDRESS}/weather',
            }
        }

        for key, val in repeatable_links[lang].items():
            helper.replace_attribute_by_text(footer_section, key, 'href', val)

        helper.replace_attribute(footer_section, '__aboutUs_class__', 'string',
                                 '''{$htmlContent = $about['body']|strip_tags}{$htmlContent|truncate:300}''')
        helper.replace_attribute(footer_section, '__address_class__', 'string',
                                 ''' آدرس :  {$smarty.const.CLIENT_ADDRESS} ''')
        helper.replace_attribute(footer_section, '__mobile_class__', 'string', '''{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(footer_section, '__mobile_class__', 'href', '''tel:{$smarty.const.CLIENT_MOBILE}''')
        footer_section = helper.replace_placeholders(footer_section,
                                                     {'__aboutUsLink__': '{$smarty.const.ROOT_ADDRESS}/aboutUs'})
        footer_final_content = f'{before_html}\n{footer_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/footer.tpl'}")
        footer_final_content = footer_final_content.replace("&gt;", ">")
        footer_final_content = footer_final_content.replace("&lt;", "<")

        return helper.create_file(footer_final_content, include_files_directory, 'footer', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def header_module(header_section, project_path , lang = 'fa'):
    try:
        style_links = [link.get('href') for link in header_section.find_all('link', rel='stylesheet')]


        header_contents = '''
{load_presentation_object filename="avaParvaz" assign="obj_main_page" subName="customers"}
{load_presentation_object filename="Session" assign="objSession" }
{load_presentation_object filename="functions" assign="objFunctions"}
{load_presentation_object filename="frontMaster" assign="obj"}
{load_presentation_object filename="dateTimeSetting" assign="objDate"}
{assign var="objFunctions" value=$objFunctions scope=parent}
{assign var="obj" value=$obj scope=parent}
{assign var="objDate" value=$objDate scope=parent}
{assign var="obj_main_page" value=$obj_main_page scope=parent}
{assign var="info_access_client_to_service" value=$obj_main_page->getInfoAuthClient() scope=parent}

{assign var='StyleSheetMain' value="StyleSheet" }

{*{assign var="testFlightParams" value=['origin'=> null, 'search_for' =>'تهران']}*}
{*{assign var="testFlightParams" value=['origin'=> 'NJF', 'search_for' =>'تهران']}*}

{*{assign var="searchFlights" value=$obj_main_page->searchAirports($testFlightParams)}*}
{*{assign var="allAirports" value=$obj_main_page->allAirports()}*}
{*{$allAirports|var_dump}*}


<!DOCTYPE html>
<html lang="fa-IR" dir="rtl">
<head class="i_modular_header">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    {include file="`$smarty.const.FRONT_CURRENT_CLIENT`modules/rich/pageInfo/main.tpl" obj_main_page=$obj_main_page}

    {if isset($info_page['all_meta_tags']) && $info_page['all_meta_tags']}
        {assign var="meta_tags" value=$info_page['all_meta_tags']}
        {foreach $meta_tags as $key=>$tag}
            {if $tag['name'] neq ''}
                <meta name="{$tag['name']}" content="{$tag['content']}">
            {/if}
        {/foreach}
    {/if}

    <base href="{$smarty.const.CLIENT_DOMAIN}" />
    <link rel="shortcut icon" href="project_files/images/favicon.png" type="image/x-icon">


    {* todo: this use in all page and all of them are necessary*}


    <meta class='__befor_all__' test="test">



    {* todo: this use only in main-page*}
    <script type="text/javascript" src="project_files/js/jquery-3.4.1.min.js"></script>
    {*    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>*}

    {if $smarty.const.GDS_SWITCH eq 'mainPage' || $smarty.const.GDS_SWITCH eq 'page'}
        <link rel="stylesheet" href="assets/main-asset/css/main.css">
        <meta class='__inside_assets__' test="test">

        <link rel="stylesheet" href="assets/css/jquery-confirm.min.css"/>
        <link type="text/css" rel="stylesheet" href="assets/datepicker/jquery-ui.min.css"/>
        <link rel="stylesheet" type="text/css" href="{$smarty.const.ROOT_LIBRARY}/{$StyleSheetMain}.php" media="screen"/>
        <script type="text/javascript">
          var rootMainPath = '{$smarty.const.SERVER_HTTP}{$smarty.const.CLIENT_DOMAIN}';
          var clientMainDomain = '{$smarty.const.SERVER_HTTP}{$smarty.const.CLIENT_MAIN_DOMAIN}';
          var libraryPath = '{$smarty.const.ROOT_LIBRARY}/';
          var gdsSwitch = '{$smarty.const.GDS_SWITCH}';
          var amadeusPath = '{$smarty.const.SERVER_HTTP}{$smarty.const.CLIENT_DOMAIN}/gds/';
          var amadeusPathByLang = '{$smarty.const.SERVER_HTTP}{$smarty.const.CLIENT_DOMAIN}/gds/{$smarty.const.SOFTWARE_LANG}/';
          var lang = '{$smarty.const.SOFTWARE_LANG}';
          var main_color = '{$smarty.const.COLOR_MAIN_BG}';
          var main_dir_customer = '{$smarty.const.FRONT_TEMPLATE_NAME}';
          var refer_url = '{if isset($smarty.session.refer_url)} {$smarty.session.refer_url} {else} "" {/if}';
          var query_param_get = JSON.parse('{$smarty.get|json_encode}');
        </script>

        <script type="text/javascript" src="assets/js/jquery-ui.min.js"></script>

        <!-- datepicker calendar -->
        <script type="text/javascript" src="assets/datepicker/jquery.cookie.min.js"></script>
        <script type="text/javascript" src="assets/datepicker/jquery.ui.core.js"></script>
        <script type="text/javascript" src="assets/datepicker/jquery.ui.datepicker-cc.js"></script>
        <script type="text/javascript" src="assets/datepicker/datepicker-scripts.js"></script>
        <script type="text/javascript" src="assets/datepicker/datepicker-declarations.js"></script>
    {/if}
    <meta class='__between_mainPage_assets__' test="test">



    {if $smarty.const.GDS_SWITCH neq 'mainPage'}
        <meta class='__inside_mainPage__' test="test">

        <link rel="stylesheet" href="project_files/css/{$StyleSheetHeader}">
        {include file="`$smarty.const.FRONT_CURRENT_CLIENT`contentHead.tpl"}
    {/if}

    <meta class='__after__all__' test="test">


</head>


                        '''
        header_section = header_contents

        befor_all = ['css/header.css', 'css/bootstrap.min.css' ]
        between_mainPage_assets = ['css/style.css']
        inside_mainPage = []
        after__all = ['css/all.min.css', 'css/register.css']

        befor_all = helper.comapre_append_list(befor_all, style_links)
        style_links = helper.delete_assames(style_links, befor_all)

        between_mainPage_assets = helper.comapre_append_list(between_mainPage_assets, style_links)
        style_links = helper.delete_assames(style_links, between_mainPage_assets)

        inside_mainPage = helper.comapre_append_list(inside_mainPage, style_links)
        style_links = helper.delete_assames(style_links, inside_mainPage)

        after__all = helper.comapre_append_list(after__all, style_links)
        style_links = helper.delete_assames(style_links, after__all)

        inside_assets = style_links

        after__all = helper.comapre_append_list(after__all, style_links)
        style_links = helper.delete_assames(style_links, after__all)
        header_section = BeautifulSoup(header_section, "html.parser")
        elements = header_section.find_all(class_='__befor_all__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(befor_all))

        elements = header_section.find_all(class_='__between_mainPage_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(between_mainPage_assets))

        elements = header_section.find_all(class_='__inside_mainPage__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(inside_mainPage))

        elements = header_section.find_all(class_='__after__all__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(after__all))

        elements = header_section.find_all(class_='__inside_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(inside_assets))

        header_final_content = f'{header_section}'
        header_final_content = header_final_content.replace("&gt;", ">")
        header_final_content = header_final_content.replace("&lt;", "<")

        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(header_final_content, include_files_directory, 'header', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def footer_script_module(footer_script_section, project_path, lang='fa'):
    try:
        script_links = [link.get('src') for link in footer_script_section.find_all('script')]

        befor_all = [ 'js/bootstrap.min.js', 'js/bootstrap.js', 'js/mega-menu.js' ]
        between_mainPage_assets = []
        inside_mainPage = []
        remove_assets = ['js/jquery-3.4.1.min.js']
        after__all = ['js/mega-menu.js', 'js/script.js']

        footer_script_content = '''
                            <div class='__befor_all__'></div>
                            {if $smarty.const.GDS_SWITCH eq 'mainPage' || $smarty.const.GDS_SWITCH eq 'page'}
                                <div class='__inside_assets__'></div>
                                <script type="text/javascript" src="assets/js/jquery-confirm.min.js"></script>
                                {include file="`$smarty.const.FRONT_CURRENT_CLIENT`content-main-page-footer.tpl" info_access_client_to_service=$info_access_client_to_service}
                            {else}
                                {if $smarty.const.GDS_SWITCH neq 'app'}
                                    {include file="`$smarty.const.FRONT_CURRENT_CLIENT`contentFooter.tpl"}
                                {/if}
                            {/if}
                            <div class='after__all'></div>
                            <script src="project_files/js/mega-menu.js"></script>
                            <script type="text/javascript" src="project_files/js/script.js"></script>
                            
                            <script type="text/javascript" src="assets/main-asset/js/public-main.js"></script>
                        '''
        footer_script_section = footer_script_content


        script_links = helper.delete_assames(script_links, remove_assets)

        befor_all = helper.comapre_append_list(befor_all, script_links)
        script_links = helper.delete_assames(script_links, befor_all)

        between_mainPage_assets = helper.comapre_append_list(between_mainPage_assets, script_links)
        script_links = helper.delete_assames(script_links, between_mainPage_assets)

        inside_mainPage = helper.comapre_append_list(inside_mainPage, script_links)
        script_links = helper.delete_assames(script_links, inside_mainPage)

        after__all = helper.comapre_append_list(after__all, script_links)
        script_links = helper.delete_assames(script_links, after__all)

        inside_assets = script_links

        after__all = helper.comapre_append_list(after__all, script_links)
        script_links = helper.delete_assames(script_links, after__all)

        footer_script_section = BeautifulSoup(footer_script_section, "html.parser")
        elements = footer_script_section.find_all(class_='__befor_all__')
        for element in elements:
            element.replace_with(helper.turn_to_script_links_assames(befor_all))

        elements = footer_script_section.find_all(class_='__between_mainPage_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_script_links_assames(between_mainPage_assets))

        elements = footer_script_section.find_all(class_='__inside_mainPage__')
        for element in elements:
            element.replace_with(helper.turn_to_script_links_assames(inside_mainPage))

        elements = footer_script_section.find_all(class_='__after__all__')
        for element in elements:
            element.replace_with(helper.turn_to_script_links_assames(after__all))

        elements = footer_script_section.find_all(class_='__inside_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_script_links_assames(inside_assets))

        footer_script_final_content = f'{footer_script_section}'
        footer_script_final_content = footer_script_final_content.replace("&gt;", ">")
        footer_script_final_content = footer_script_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(footer_script_final_content, include_files_directory, 'footer_script', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def fast_search_flight_module(fast_search_flight_section, project_path, lang='fa'):
    try:
        return 'True'

        # type  of current functions:

        # replace_placeholders
        # replace_attribute and string
        # add_before_after
        # direct_string
        # final_content.replace
        fast_search_flight_final_content = fast_search_flight_final_content.replace("&gt;", ">")
        fast_search_flight_final_content = fast_search_flight_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(fast_search_flight_final_content, include_files_directory, 'fast_search_flight', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def blog_module(blog_section, project_path , lang = 'fa'):
    try:
        # create regex objects containing patterns of items classes
        complex_items_numbers = helper.item_numbers(blog_section,complex_items_pattern)
        simple_items_numbers = helper.item_numbers(blog_section,simple_items_pattern)
        complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
        max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

        before_html = '''{assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>1i_modular__max_limit]}
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
            }
            simple_element = blog_section.find(class_=simple_items_class + num)
            if num == simple_items_numbers[0]:
                helper.add_before_after(blog_section, simple_items_class + num, before_foreach, after_foreach)

                simple_element = blog_section.find(class_=simple_items_class + num)
                simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)
                simple_element = blog_section.find(class_=simple_items_class + num)
                helper.replace_attribute(simple_element, '__image_class__', 'src','{$article["image"]}')
                helper.replace_attribute(simple_element, '__image_class__', 'src','{$article["image"]}')
                helper.replace_attribute(simple_element, '__title_class__', 'string','{$article["title"]}')
                helper.replace_attribute(simple_element, '__heading_class__', 'string','{$article["heading"]}')

            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            before_if = '''{if $articles[{0}] }'''
            before_if = before_if.replace("{0}", num)
            after_if = '''{/if}'''

            blog_complex_replacement_data = {
                "__link__": '''{{$articles[{0}]['link']}}'''.format(num),
                "__alt_article__": '''{{$articles[{0}]['title']}}'''.format(num),
                'images/5497750661271-6.jpg': '''{{$articles[{0}]['image']}}'''.format(num),
                '<span class="__date__">5 بهمن 1402</span>': '''{{$articles[{0}]['created_at']}}'''.format(num),
                '<span class="__comments_number__">450</span>': '''{{$articles[{0}]['comments_count']['comments_count']}}'''.format(num)
            }
            helper.add_before_after(blog_section, complex_items_class + num, before_if, after_if)


            complex_element = blog_section.find(class_=complex_items_class + num)
            complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)
            complex_element = blog_section.find(class_=complex_items_class + num)
            helper.replace_attribute(complex_element, '__image_class__', 'src', '''{{$articles[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title_class__', 'string', '''{{$articles[{0}]['title']}}'''.format(num))
            helper.replace_attribute(complex_element, '__heading_class__', 'string', '''{{$articles[{0}]['heading']}}'''.format(num))


        blog_final_content = f'{before_html}\n{blog_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        helper.write_text_in_path(project_path, "{inclued 'include_files/blog.tpl'}")
        blog_final_content = blog_final_content.replace("&gt;", ">")
        blog_final_content = blog_final_content.replace("&lt;", "<")

        return helper.create_file(blog_final_content, include_files_directory, 'blog', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def tours_module(tours_section, project_path, lang='fa'):
    try:
        before_html = '''{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}'''


        after_html = '''{/if}'''

        tour_region_array = ['internal', 'external', '']
        tour_type_array = ['', 'special']

        for region in tour_region_array:
            for type in tour_type_array:
                before_html_local = '''{assign var="__params_var__" value=['type'=>'__type__','limit'=> '__local_max_limit__','dateNow' => $dateNow, 'country' =>'__country__']}
                                        {assign var='__tour_var__' value=$obj_main_page->getToursReservation($__params_var__)}
                                        {if $__tour_var__}
                                            {assign var='check_tour' value=true}
                                        {/if}
                                        {assign var="__local_min_var__" value=__local_min__}
                                        {assign var="__local_max_var__" value=__local_max__}
                                    '''
                before_foreach_local = '''
                                        {foreach $__tour_var__ as $item}
                                            {if $__local_min_var__ <= $__local_max_var__}
                                        '''
                after_foreach_local = '''
                                            {$__local_min_var__ = $__local_min_var__ + 1}
                                            {/if}
                                        {/foreach}
                                        '''
                replace_classes_local = {
                    '___price_class__': {'string': '''{$item['min_price']['discountedMinPriceR']|number_format}'''},
                    '__title_class__': {'string': '''{$item['tour_name']}'''},
                    '__night_class__': {'string': '''{$item['night']}'''},
                    '__image_class__': {
                        'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$item['tour_pic']}''',
                        'alt': '''{$item['tour_name']}'''},
                    '__date_class__': {'string': '''{assign var="year" value=substr($item['start_date'], 0, 4)}
                                                {assign var="month" value=substr($item['start_date'], 4, 2)}
                                                {assign var="day" value=substr($item['start_date'], 6)}
                                                {$year}/{$month}/{$day}
                                                '''},
                }

                section_class= '__tour__'
                section_var= 'tour'
                section_params= 'tour_params'
                local_min_var = 'min'
                local_max_var = 'max'
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


                local_section = tours_section.find(class_=section_class)
                if local_section:
                    before_html_local = before_html_local.replace("__type__", type)
                    before_html_local = before_html_local.replace("__country__", region)
                    before_html_local = before_html_local.replace("__tour_var__", section_var)
                    before_html_local = before_html_local.replace("__params_var__", section_params)
                    before_html_local = before_html_local.replace("__local_min_var__", local_min_var)
                    before_html_local = before_html_local.replace("__local_max_var__", local_max_var)
                    before_foreach_local = before_foreach_local.replace("__local_min_var__", local_min_var)
                    before_foreach_local = before_foreach_local.replace("__local_max_var__", local_max_var)
                    before_foreach_local = before_foreach_local.replace("__tour_var__", section_var)
                    after_foreach_local = after_foreach_local.replace("__local_min_var__", local_min_var)

                    before_html = before_html + '\n' + before_html_local
                    complex_items_numbers = helper.item_numbers(local_section, complex_items_pattern)
                    simple_items_numbers = helper.item_numbers(local_section, simple_items_pattern)
                    complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
                    simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
                    simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
                    max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)
                    before_html = before_html.replace("__local_min__", simple_items_numbers_min)
                    before_html = before_html.replace("__local_max__", simple_items_numbers_max)
                    before_html = before_html.replace("__local_max_limit__", max_item_number)
                    for num in simple_items_numbers:
                        tours_simple_replacements = {
                            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailTour/{$item['id']}/{$item['tour_slug']}''',
                        }
                        simple_element = local_section.find(class_=simple_items_class + num)
                        if num == simple_items_numbers[0]:
                            simple_element = helper.replace_placeholders(simple_element, tours_simple_replacements)
                            simple_element = local_section.find(class_=simple_items_class + num)
                            helper.add_before_after(local_section, simple_items_class + num, before_foreach_local, after_foreach_local)
                            simple_element = local_section.find(class_=simple_items_class + num)
                            for class_name, val in replace_classes_local.items():
                                for atr, value in val.items():
                                    helper.replace_attribute(simple_element, class_name, atr, value)
                        else:
                            simple_element.decompose()



                    for num in complex_items_numbers:
                        tours_complex_replacements = {
                            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailTour/{$__tour_var__[{0}]['id']}/{$__tour_var__[{0}]['tour_slug']}'''  ,
                        }
                        replace_comlex_classes_local = {
                            '___price_class__': {'string': '''{$__tour_var__[{0}]['min_price']['discountedMinPriceR']|number_format}'''},
                            '__title_class__': {'string': '''{$__tour_var__[{0}]['tour_name']}'''},
                            '__night_class__': {'string': '''{$__tour_var__[{0}]['night']}'''},
                            '__image_class__': {
                                'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__tour_var__[{0}]['tour_pic']}''',
                                'alt': '''{$__tour_var__[{0}]['tour_name']}'''},
                            '__date_class__': {'string': '''{assign var="year" value=substr($__tour_var__[{0}]['start_date'], 0, 4)}
                                                        {assign var="month" value=substr($__tour_var__[{0}]['start_date'], 4, 2)}
                                                        {assign var="day" value=substr($__tour_var__[{0}]['start_date'], 6)}
                                                        {$year}/{$month}/{$day}
                                                        '''},
                        }
                        before_c_item_local = '''{if $__tour_var__[{0}]}'''
                        after_c_item_local = '''{/if}'''

                        before_c_item_local = before_c_item_local.replace("{0}", f'{num}')
                        before_c_item_local = before_c_item_local.replace("__tour_var__", section_var)
                        tours_complex_replacements['__link__'] = tours_complex_replacements['__link__'].replace("{0}", f'{num}')
                        tours_complex_replacements['__link__'] = tours_complex_replacements['__link__'].replace("__tour_var__", section_var)


                        complex_element = local_section.find(class_=complex_items_class + num)
                        complex_element = helper.replace_placeholders(complex_element, tours_complex_replacements)

                        complex_element = local_section.find(class_=complex_items_class + num)
                        helper.add_before_after(local_section, complex_items_class + num, before_c_item_local, after_c_item_local)
                        complex_element = local_section.find(class_=complex_items_class + num)
                        for class_name, val in replace_comlex_classes_local.items():
                            for atr, value in val.items():
                                value = value.replace("{0}", f'{num}')
                                value = value.replace("__tour_var__", section_var)
                                helper.replace_attribute(complex_element, class_name, atr, value)


        before_html = before_html + '\n' + '''{if $check_tour}'''

        tours_final_content = f'{before_html}\n{tours_section}\n{after_html}'

        tours_final_content = tours_final_content.replace("&gt;", ">")
        tours_final_content = tours_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(tours_final_content, include_files_directory, 'tours', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def hotels_webservice_module(hotels_section, project_path, lang='fa'):
    try:
        before_html = '''{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}'''


        after_html = '''{/if}'''

        hotel_region_array = ['internal', 'external']
        hotel_type_array = ['']

        for region in hotel_region_array:
            for type in hotel_type_array:
                before_html_local = '''
                                        {assign var="__params_var__" value=['Count'=> '__local_max_limit__', 'type' =>'__country__']}
                                        {assign var='__hotel_var__' value=$obj_main_page->getHotelWebservice($__params_var__)}
                                        {if $__hotel_var__}
                                            {assign var='check_hotel' value=true}
                                        {/if}
                                        {assign var="__local_min_var__" value=__local_min__}
                                        {assign var="__local_max_var__" value=__local_max__}
                                    '''
                before_foreach_local = '''
                                        {foreach $__hotel_var__ as $item}
                                            {if $__local_min_var__ <= $__local_max_var__}
                                        '''
                after_foreach_local = '''
                                            {$__local_min_var__ = $__local_min_var__ + 1}
                                            {/if}
                                        {/foreach}
                                        '''
                replace_classes_local = {
                    '__title_class__': {'string': '''{$item['Name']}'''},
                    '__city_class__': {'string': '''{$item['City']}'''},
                    '__image_class__': {
                        'src': '''{$item['Picture']}''',
                        'alt': '''{$item['City']}'''},
                }

                section_class= '__hotel__'
                section_var= 'hotel'
                section_params= 'hotel_params'
                local_min_var = 'min'
                local_max_var = 'max'
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


                local_section = hotels_section.find(class_=section_class)
                if local_section:
                    before_html_local = before_html_local.replace("__type__", type)
                    before_html_local = before_html_local.replace("__country__", region)
                    before_html_local = before_html_local.replace("__hotel_var__", section_var)
                    before_html_local = before_html_local.replace("__params_var__", section_params)
                    before_html_local = before_html_local.replace("__local_min_var__", local_min_var)
                    before_html_local = before_html_local.replace("__local_max_var__", local_max_var)
                    before_foreach_local = before_foreach_local.replace("__local_min_var__", local_min_var)
                    before_foreach_local = before_foreach_local.replace("__local_max_var__", local_max_var)
                    before_foreach_local = before_foreach_local.replace("__hotel_var__", section_var)
                    after_foreach_local = after_foreach_local.replace("__local_min_var__", local_min_var)

                    before_html = before_html + '\n' + before_html_local
                    complex_items_numbers = helper.item_numbers(local_section, complex_items_pattern)
                    simple_items_numbers = helper.item_numbers(local_section, simple_items_pattern)
                    complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
                    simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
                    simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
                    max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)
                    before_html = before_html.replace("__local_min__", simple_items_numbers_min)
                    before_html = before_html.replace("__local_max__", simple_items_numbers_max)
                    before_html = before_html.replace("__local_max_limit__", max_item_number)
                    for num in simple_items_numbers:
                        hotels_simple_replacements = {
                            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailHotel/api/{$item['HotelIndex']}''',
                        }
                        simple_element = local_section.find(class_=simple_items_class + num)
                        if num == simple_items_numbers[0]:
                            simple_element = helper.replace_placeholders(simple_element, hotels_simple_replacements)
                            simple_element = local_section.find(class_=simple_items_class + num)
                            helper.add_before_after(local_section, simple_items_class + num, before_foreach_local, after_foreach_local)
                            simple_element = local_section.find(class_=simple_items_class + num)
                            for class_name, val in replace_classes_local.items():
                                for atr, value in val.items():
                                    helper.replace_attribute(simple_element, class_name, atr, value)

                            for i in range(1, 6):
                                light_star_elements = simple_element.find(class_='__star_class_light__' + str(i))
                                dark_star_elements = simple_element.find(class_='__star_class_dark__' + str(i))
                                if i == 1 and light_star_elements:
                                    new_light_star = '''{for $i = 0; $i < count($item['StarCode']); $i++}''' + str(light_star_elements) + '''{/for}'''
                                    new_light_star = BeautifulSoup(new_light_star, 'html.parser')
                                    light_star_elements.replace_with(new_light_star)
                                else:
                                    if light_star_elements:
                                        light_star_elements.decompose()

                                if i == 1 and dark_star_elements:
                                    new_dark_star = '''{for $i = 0; $i < count($item['StarCode']); $i++}''' + str(dark_star_elements) + '''{/for}'''
                                    new_dark_star = BeautifulSoup(new_light_star, 'html.parser')
                                    dark_star_elements.replace_with(new_dark_star)
                                else:
                                    if dark_star_elements:
                                        dark_star_elements.decompose()







                        else:
                            simple_element.decompose()



                    for num in complex_items_numbers:
                        hotels_complex_replacements = {
                            "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailHotel/api/{$__hotel_var__[4]['HotelIndex']}'''  ,
                        }
                        replace_comlex_classes_local = {
                            '__title_class__': {'string': '''{$internal_hotels[4]['Name']}'''},
                            '__city_class__': {'string': '''{$internal_hotels[4]['City']}'''},
                            '__image_class__': {
                                'src': '''{$internal_hotels[4]['Picture']}''',
                                'alt': '''{$internal_hotels[4]['City']}'''},
                        }
                        before_c_item_local = '''{if $__hotel_var__[{0}]}'''
                        after_c_item_local = '''{/if}'''

                        before_c_item_local = before_c_item_local.replace("{0}", f'{num}')
                        before_c_item_local = before_c_item_local.replace("__hotel_var__", section_var)
                        hotels_complex_replacements['__link__'] = hotels_complex_replacements['__link__'].replace("{0}", f'{num}')
                        hotels_complex_replacements['__link__'] = hotels_complex_replacements['__link__'].replace("__hotel_var__", section_var)


                        complex_element = local_section.find(class_=complex_items_class + num)
                        complex_element = helper.replace_placeholders(complex_element, hotels_complex_replacements)

                        complex_element = local_section.find(class_=complex_items_class + num)
                        helper.add_before_after(local_section, complex_items_class + num, before_c_item_local, after_c_item_local)
                        complex_element = local_section.find(class_=complex_items_class + num)
                        for class_name, val in replace_comlex_classes_local.items():
                            for atr, value in val.items():
                                value = value.replace("{0}", f'{num}')
                                value = value.replace("__hotel_var__", section_var)
                                helper.replace_attribute(complex_element, class_name, atr, value)


        before_html = before_html + '\n' + '''{if $check_hotel}'''

        hotels_final_content = f'{before_html}\n{hotels_section}\n{after_html}'

        hotels_final_content = hotels_final_content.replace("&gt;", ">")
        hotels_final_content = hotels_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(hotels_final_content, include_files_directory, 'hotels', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now

def new_module(new_section, project_path, lang='fa'):
    try:

        # type  of current functions:

        # replace_placeholders
        # replace_attribute and string
        # add_before_after
        # direct_string
        # final_content.replace
        new_final_content = new_final_content.replace("&gt;", ">")
        new_final_content = new_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(new_final_content, include_files_directory, 'new', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now





