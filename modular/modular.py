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


def initiation_progress():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    if 'project_name' not in request.form:
        return jsonify({"message": "No project name"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})



    project_path = helper.create_folder(request.form['project_name'])
    copy_repeated_file_folders_massage = helper.copy_repeated_file_folders(request.form['project_name'])
    html_content = file.read()
    # turn string to soup object
    soup = BeautifulSoup(html_content, 'html.parser')
    if not soup:
        return jsonify({"message": "testing blog section = " + f'{soup}'})

    soup_online = unit_test.get_online_html()
    if  soup_online == 'خطایی پیش آمده و دیتایی نمایش ندارد.':
        return jsonify({"message": "testing blog section = " + f'{soup_online}'})


    moduls_array = {
            'blog': {
                'class': 'i_modular_blog',
                'name': 'وبلاگ',
                'modular': blog_module,
                'test_function': unit_test.unit_test_blog
            },
            'newsletter': {
                'class': 'i_modular_newsletter',
                'name': 'خبرنامه',
                'modular': newsletter_module,
                'test_function': unit_test.unit_test_newsletter
            },
            'news': {
                'class': 'i_modular_news',
                'name': 'اخبار',
                'modular': news_module,
                'test_function': unit_test.unit_test_news
            },
            'menu': {
                'class': 'i_modular_menu',
                'name': 'منو',
                'modular': menu_module,
                'test_function': unit_test.unit_test_menu
            },
            'footer': {
                'class': 'i_modular_footer',
                'name': 'فوتر',
                'modular': footer_module,
                'test_function': unit_test.unit_test_footer
            },
            'banner_gallery': {
                'class': 'i_modular_banner_gallery',
                'name': 'گالری بنر',
                'modular': banner_gallery_module,
                'test_function': unit_test.unit_test_blog
            },

        }




    # blog module
    blog_section = soup.find(class_="i_modular_blog")
    if blog_section:
        blog_module_massage = blog_module(blog_section,project_path)
    # newsletter module
    newsletter_section = soup.find(class_="i_modular_newsletter")
    if newsletter_section:
        newsletter_module_massage = newsletter_module(newsletter_section,project_path)
    # news module
    news_section = soup.find(class_="i_modular_news")
    if news_section:
        news_module_massage = news_module(news_section,project_path)
    # menu module
    menu_section = soup.find(class_="i_modular_menu")
    if menu_section:
        menu_module_massage = menu_module(menu_section,project_path)
    # footer module
    footer_section = soup.find(class_="i_modular_footer")
    if footer_section:
        footer_module_massage = footer_module(footer_section,project_path)


    # banner gallery module
    banner_gallery_section = soup.find(class_="i_modular_banner_gallery")
    if banner_gallery_section:
        banner_gallery_module_massage = banner_gallery_module(banner_gallery_section,project_path)


    # UNIT TEST
    soup = BeautifulSoup(html_content, 'html.parser')
    if not soup:
        return jsonify({"message": "testing blog section = " + f'{soup}'})

    blog_test_massage = initiation_test('i_modular_blog', ' وبلاگ ', unit_test.unit_test_blog , soup, soup_online)
    newsletter_test_massage = initiation_test('i_modular_newsletter', ' خبرنامه ', unit_test.unit_test_newsletter , soup, soup_online)
    news_test_massage = initiation_test('i_modular_news', ' اخبار ', unit_test.unit_test_news , soup, soup_online)
    menu_test_massage = initiation_test('i_modular_menu', ' منوی هدر ', unit_test.unit_test_menu , soup, soup_online)
    footer_test_massage = initiation_test('i_modular_footer', ' فوتر ', unit_test.unit_test_footer , soup, soup_online)

    return jsonify({"message":  "<br><br> تست ماژول گذاری بخش بلاگ = " + f'{blog_module_massage}' +
                                " <br><br> تست ماژول گذاری بخش خبرنامه = " + f'{newsletter_module_massage}' +
                                " <br><br> تست ماژول گذاری بخش اخبار = " + f'{news_module_massage}' +
                                " <br><br> تست  ماژول گذاریبخش منوی هدر = " + f'{menu_module_massage}' +
                                " <br><br> تست ماژول گذاری بخش فوتر = " + f'{footer_module_massage}' +
                                 "<br><br> تست بخش بلاگ = " + f'{blog_test_massage}' +
                                " <br><br> تست بخش خبرنامه = " + f'{newsletter_test_massage}' +
                                " <br><br> تست بخش اخبار = " + f'{news_test_massage}' +
                                " <br><br> تست بخش منوی هدر = " + f'{menu_test_massage}' +
                                " <br><br> تست بخش فوتر = " + f'{footer_test_massage}'  })


def blog_module(blog_section, project_path):
    try:
        # create regex objects containing patterns of items classes
        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
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
                "__image__": '''{$article['image']}''',
                "__alt_article__": '''{$article['title']}''',
                '<span class="__date__">5 بهمن 1402</span>': '''{$article['created_at']}''',
                '<span class="__comments_number__">450</span>': '''{$article['comments_count']['comments_count']}''',
                'images/5497750661271-6.jpg': '''{$article['image']}'''
            }
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
            if num == simple_items_numbers[0]:
                helper.add_before_after(blog_section, "__i_modular_nc_item_" + num, before_foreach, after_foreach)

                simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
                simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)
                simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
                helper.replace_attribute(simple_element, '__image__', 'src','{$article["image"]}')
                helper.replace_attribute(simple_element, '__image__', 'src','{$article["image"]}')
                helper.replace_attribute(simple_element, '__title__', 'string','{$article["title"]}')
                helper.replace_attribute(simple_element, '__heading__', 'string','{$article["heading"]}')

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
            helper.add_before_after(blog_section, "__i_modular_c_item_" + num, before_if, after_if)


            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)
            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            helper.replace_attribute(complex_element, '__image__', 'src', '''{{$articles[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title__', 'string', '''{{$articles[{0}]['title']}}'''.format(num))
            helper.replace_attribute(complex_element, '__heading__', 'string', '''{{$articles[{0}]['heading']}}'''.format(num))


        blog_final_content = f'{before_html}\n{blog_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/blog.tpl'}")
        blog_final_content = blog_final_content.replace("&gt;", ">")
        blog_final_content = blog_final_content.replace("&lt;", "<")

        return helper.create_file(blog_final_content, include_files_directory, 'blog', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def initiation_test(class_name, module_name, module_test_function, soup, soup_online):
    section = soup.find(class_=class_name)
    section_online = soup_online.find(class_=class_name) if section else None

    if section_online:
        return module_test_function(section, section_online)

    return f'ماژول {module_name} بازگذاری نشد'

def initiation_modulation(class_name, module_name, modular_function, soup, soup_online):
    section = soup.find(class_=class_name)
    section_online = soup_online.find(class_=class_name) if section else None

    if section_online:
        return module_test_function(section, section_online)

    return f'ماژول {module_name} بازگذاری نشد'



def banner_gallery_module(banner_gallery_section, project_path):
    try:
        # create regex objects containing patterns of items classes
        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
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
            simple_element = banner_gallery_section.find(class_="__i_modular_nc_item_" + num)
            if num == simple_items_numbers[0]:
                for tag in banner_gallery_section.find_all():
                    if tag.decode() == simple_element.decode():
                        new_tag = BeautifulSoup(f'{before_foreach}\n{simple_element}\n{after_foreach}')
                        simple_element.replace_with(new_tag)
                simple_element = banner_gallery_section.find(class_="__i_modular_nc_item_" + num)
                simple_element = helper.replace_placeholders(simple_element, banner_gallery_replacement_data)
                simple_element = banner_gallery_section.find(class_="__i_modular_nc_item_" + num)
                helper.replace_attribute(simple_element, '__image__', 'src','{$banner["image"]}')
                helper.replace_attribute(simple_element, '__image__', 'alt','{$banner["title"]}')

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
            complex_element = banner_gallery_section.find(class_="__i_modular_c_item_" + num)
            for tag in banner_gallery_section.find_all():
                if tag.decode() == complex_element.decode():
                    new_tag = BeautifulSoup(f'{before_if}\n{complex_element}\n{after_if}')
                    complex_element.replace_with(new_tag)

            complex_element = banner_gallery_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, banner_gallery_complex_replacement_data)
            complex_element = banner_gallery_section.find(class_="__i_modular_c_item_" + num)
            helper.replace_attribute(complex_element, '__image__', 'src', '''{{banners[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title__', 'alt', '''{{banners[{0}]['title']}}'''.format(num))


        banner_gallery_final_content = f'{before_html}\n{banner_gallery_section}\n{after_html}'


        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/banner-gallery.tpl'}")
        banner_gallery_final_content = banner_gallery_final_content.replace("&gt;", ">")
        banner_gallery_final_content = banner_gallery_final_content.replace("&lt;", "<")
        return banner_gallery_final_content

        return helper.create_file(banner_gallery_final_content, include_files_directory, 'banner_gallery', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def news_module(news_section, project_path):
    try:
        # create regex objects containing patterns of items classes
        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
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
            simple_element = news_section.find(class_="__i_modular_nc_item_" + num)
            if num == simple_items_numbers[0]:
                for tag in news_section.find_all():
                    if tag.decode() == simple_element.decode():
                        new_tag = BeautifulSoup(f'{before_foreach}\n{simple_element}\n{after_foreach}')
                        simple_element.replace_with(new_tag)
                simple_element = news_section.find(class_="__i_modular_nc_item_" + num)
                simple_element = helper.replace_placeholders(simple_element, news_replacement_data)
                simple_element = news_section.find(class_="__i_modular_nc_item_" + num)
                helper.replace_attribute(simple_element, '__image__', 'src','{$item["image"]}')
                helper.replace_attribute(simple_element, '__image__', 'alt','{$item["alt"]}')
                helper.replace_attribute(simple_element, '__title__', 'string','{$item["title"]}')
                helper.replace_attribute(simple_element, '__heading__', 'string','{$item["heading"]}')
                helper.replace_attribute(simple_element, '__description__', 'string','{$item["description"]}')

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
            complex_element = news_section.find(class_="__i_modular_c_item_" + num)
            for tag in news_section.find_all():
                if tag.decode() == complex_element.decode():
                    new_tag = BeautifulSoup(f'{before_if}\n{complex_element}\n{after_if}')
                    complex_element.replace_with(new_tag)

            complex_element = news_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, news_complex_replacement_data)
            complex_element = news_section.find(class_="__i_modular_c_item_" + num)
            helper.replace_attribute(complex_element, '__image__', 'src', '''{{$othe_itmes[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__image__', 'alt', '''{{$othe_itmes[{0}]['alt']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title__', 'string', '''{{$othe_itmes[{0}]['title']}}'''.format(num))
            helper.replace_attribute(complex_element, '__heading__', 'string', '''{{$othe_itmes[{0}]['heading']}}'''.format(num))
            helper.replace_attribute(complex_element, '__description__', 'string', '''{{$othe_itmes[{0}]['description']}}'''.format(num))


        news_final_content = f'{before_html}\n{news_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/news.tpl'}")
        news_final_content = news_final_content.replace("&gt;", ">")
        news_final_content = news_final_content.replace("&lt;", "<")

        return helper.create_file(news_final_content, include_files_directory, 'news', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def newsletter_module(newsletter_section, project_path):
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
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/newsletter.tpl'}")
        newsletter_final_content = newsletter_final_content.replace("&gt;", ">")
        newsletter_final_content = newsletter_final_content.replace("&lt;", "<")

        return helper.create_file(newsletter_final_content, include_files_directory, 'newsletter', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def menu_module(menu_section, project_path):
    try:

        repeatable_links = {
            'پرواز': '{$smarty.const.ROOT_ADDRESS}/page/flight',
            'پیگیری خرید': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
            'وبلاگ': '{$smarty.const.ROOT_ADDRESS}/mag',
            'اخبار سایت': '{$smarty.const.ROOT_ADDRESS}/news',
            'معرفی ايران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
            'قوانین و مقررات': '{$smarty.const.ROOT_ADDRESS}/rules',
            'درباره ما': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
            'تماس با ما': '{$smarty.const.ROOT_ADDRESS}/contactUs',
            'پرداخت آنلاین': '{$smarty.const.ROOT_ADDRESS}/pay',
        }
        helper.replace_attribute_by_text(menu_section, 'ورود یا ثبت نام' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute(menu_section, '__login_register__2', 'class','__login_register__2 main-navigation__button2 show-box-login-js')
        helper.replace_attribute(menu_section, '__login_register__', 'class','__login_register__ main-navigation__button2 show-box-login-js button_header logIn d-flex d-lg-none')


        after_login = '''<div class="main-navigation__sub-menu2 arrow-up show-content-box-login-js" style="display: none">
                            {include file="`$smarty.const.FRONT_CURRENT_THEME`topBar.tpl"}
                        </div>'''

        simple_element = menu_section.find(class_=lambda classes: classes and '__login_register__' in classes)
        for tag in menu_section.find_all():
            if tag.decode() == simple_element.decode():
                new_tag = BeautifulSoup(f'{simple_element}\n{after_login}')
                simple_element.replace_with(new_tag)

        # return f'{menu_section}'

        for key, val in repeatable_links.items():
            helper.replace_attribute_by_text(menu_section, key, 'href', val)


        menu_final_content = f'{menu_section}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/menu.tpl'}")
        menu_final_content = menu_final_content.replace("&gt;", ">")
        menu_final_content = menu_final_content.replace("&lt;", "<")

        return helper.create_file(menu_final_content, include_files_directory, 'menu', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def footer_module(footer_section, project_path):
    try:
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
        social_element = footer_section.find(class_=lambda classes: classes and '__social__' in classes)
        social_element.insert_before(befor_social_media_soup)

        social_element = footer_section.find(class_=lambda classes: classes and '__social__' in classes)
        repeatable_social_links = {
            '__telegram__': '{if $telegramHref}{$telegramHref}{/if}',
            '__whatsapp__': '{if $telegramHref}{$whatsappHref}{/if}',
            '__instagram__': '{if $telegramHref}{$instagramHref}{/if}',
        }

        for key, val in repeatable_social_links.items():
            helper.replace_attribute(social_element, key, 'href', val)



        repeatable_links = {
            'پرواز': '{$smarty.const.ROOT_ADDRESS}/page/flight',
            'پیگیری خرید': '{$smarty.const.ROOT_ADDRESS}/UserTracking',
            'وبلاگ': '{$smarty.const.ROOT_ADDRESS}/mag',
            'اخبار سایت': '{$smarty.const.ROOT_ADDRESS}/news',
            'معرفی ايران': '{$smarty.const.ROOT_ADDRESS}/aboutIran',
            'قوانین و مقررات': '{$smarty.const.ROOT_ADDRESS}/rules',
            'درباره ما': '{$smarty.const.ROOT_ADDRESS}/aboutUs',
            'تماس با ما': '{$smarty.const.ROOT_ADDRESS}/contactUs',
            'پرداخت آنلاین': '{$smarty.const.ROOT_ADDRESS}/pay',
        }
        for key, val in repeatable_links.items():
            helper.replace_attribute_by_text(footer_section, key, 'href', val)

        helper.replace_attribute(footer_section, '__aboutUs__', 'string', '''{$htmlContent = $about['body']|strip_tags}{$htmlContent|truncate:300}''')
        helper.replace_attribute(footer_section, '__address__', 'string', ''' آدرس :  {$smarty.const.CLIENT_ADDRESS} ''')
        helper.replace_attribute(footer_section, '__mobile__', 'string', '''{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(footer_section, '__mobile__', 'href', '''tel:{$smarty.const.CLIENT_MOBILE}''')
        footer_section = helper.replace_placeholders(footer_section, {'__aboutUsLink__':'{$smarty.const.ROOT_ADDRESS}/aboutUs'})
        footer_final_content = f'{before_html}\n{footer_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/footer.tpl'}")
        footer_final_content = footer_final_content.replace("&gt;", ">")
        footer_final_content = footer_final_content.replace("&lt;", "<")


        return helper.create_file(footer_final_content, include_files_directory, 'footer', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now




