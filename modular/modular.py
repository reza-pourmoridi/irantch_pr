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
from modular.searchBox import sb
import traceback



complex_items_pattern = re.compile(r'__i_modular_c_item_class_(\d+)')
simple_items_pattern = re.compile(r'__i_modular_nc_item_class_(\d+)')
complex_items_class = "__i_modular_c_item_class_"
simple_items_class = "__i_modular_nc_item_class_"
repeatable_links = {
        '{$smarty.const.ROOT_ADDRESS}/page/flight':
            {
                'پرواز', 'رحلة جوية', 'flight', 'بلیط هواپیما'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/flight-hotel':
            {
                'پرواز+هتل', 'flight-hotel'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/train':
            {
                'قطار', 'train', 'بلیط قطار'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/bus':
            {
                'اتوبوس', 'bus', 'بلیط اتوبوس'
            },
        '{$smarty.const.ROOT_ADDRESS}/embassies':
            {
                'سفارت'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/entertainment':
            {
                'تفریحات'
            },
        '{$smarty.const.ROOT_ADDRESS}/lastMinute':
            {
                'دقیقه 90'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/insurance':
            {
                'بیمه'
            },
        '{$smarty.const.ROOT_ADDRESS}/currency':
            {
                'نرخ ارز', 'ارز'
            },
        '{$smarty.const.ROOT_ADDRESS}/mag':
            {
                'وبلاگ'
            },
        '{$smarty.const.ROOT_ADDRESS}/iranVisa':
            {
                'تأشيرة إيران'
            },
        'https://{$smarty.const.CLIENT_MAIN_DOMAIN}':
            {
                'خانه', 'home', 'صفحه اصلی'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/tour':
            {
                'تور', 'شبكة', 'Iran Tour', 'tour', 'تور لحظه آخری'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/visa':
            {
                'ویزا', 'Iran visa', 'Iran visa form'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/hotel':
            {
                'الفندق', 'Iran Hotel', 'Hotel', 'هتل', 'هتل ها', 'رزرو هتل '
            },
        '{$smarty.const.ROOT_ADDRESS}/news':
            {
                'اخبار سایت', 'news', 'اخبار'
            },
        '{$smarty.const.ROOT_ADDRESS}/loginUser':
            {
                'باشگاه مسافران', 'باشگاه مشتریان'
            },
        '{$smarty.const.ROOT_ADDRESS}/agencyList':
            {
                'نمایندگی ها'
            },
        '{$smarty.const.ROOT_ADDRESS}/vote':
            {
                'نظر سنجی', 'نظرسنجی'
            },
        '{$smarty.const.ROOT_ADDRESS}/employment':
            {
                'استخدام', 'فرم استخدام',
            },
        '{$smarty.const.ROOT_ADDRESS}/signRequest':
            {
                'درخواست ساین'
            },
        '{$smarty.const.ROOT_ADDRESS}/feedback':
            {
                'انتقاد و پیشنهادات'
            },
        '{$smarty.const.ROOT_ADDRESS}/UserTracking':
            {
                'پیگیری خرید', 'ترتيب المسار', 'Track order'
            },
        '{$smarty.const.ROOT_ADDRESS}/video':
            {
                'ویدئو ها'
            },
        '{$smarty.const.ROOT_ADDRESS}/page/visa':
            {
                'اطلاعات ویزا', 'ویزا'
            },
        '{$smarty.const.ROOT_ADDRESS}/aboutCountry':
            {
                'معرفی کشورها'
            },
        '{$smarty.const.ROOT_ADDRESS}/aboutIran':
            {
                'مقدمة عن إيران', 'Introduction to Iran', 'info of Iran', 'Introduction of Iran', 'معرفی ايران', 'معرفی ایران', 'درباره ایران'
            },
        '{$smarty.const.ROOT_ADDRESS}/rules':
            {
                'قوانین و مقررات', 'الأحكام والشروط', 'terms and conditions', 'rules'
            },
        '{$smarty.const.ROOT_ADDRESS}/aboutUs':
            {
                'درباره ما', 'معلومات عنا', 'about us'
            },
        '{$smarty.const.ROOT_ADDRESS}/contactUs':
            {
                'تماس با ما', 'اتصل بنا', 'call us', 'contacts', 'ارتباط با ما'
            },
        '{$smarty.const.ROOT_ADDRESS}/faq':
            {
                'پرسشهای متداول', 'Faq', 'پرسش و پاسخ', 'سوالات متداول'
            },
        '{$smarty.const.ROOT_ADDRESS}/pay':
            {
                'پرداخت آنلاین', 'درگاه پرداخت'
            },
        '{$smarty.const.ROOT_ADDRESS}/gallery':
            {
                'گالری عکس'
            },
        '{$smarty.const.ROOT_ADDRESS}/recommendation':
            {
                'recommendation', 'Travelogue', 'سفر نامه', 'نظر مشتریان'
            },
        '{$smarty.const.ROOT_ADDRESS}/orderServices':
            {
                'الخدمات السياحية', 'Tourism services'
            },
        '{$smarty.const.ROOT_ADDRESS}/clock':
            {
                'ساعة البلدان', 'Countries clock', 'ساعت کشورها'
            },
        '{$smarty.const.ROOT_ADDRESS}/convertDate':
            {
                'تبدیل تاریخ'
            },
        '{$smarty.const.ROOT_ADDRESS}/weather':
            {
                'علم الارصاد الجوية', 'meteorology', 'weather', 'هواشناسی'
            }

    }
view_folder_path = 'z:/gds/view/'
controller_folder_path = 'z:/gds/controller/customers/'
repeatable_social_links = {
    '__telegram_class__': '{if $telegramHref}{$telegramHref}{/if}',
    '__whatsapp_class__': '{if $whatsappHref}{$whatsappHref}{/if}',
    '__instagram_class__': '{if $instagramHref}{$instagramHref}{/if}',
    '__linkdin_class__': '{if $linkeDinHref}{$linkeDinHref}{/if}',
    '__aparat_class__': '{if $aparatHref}{$aparatHref}{/if}',
    '__youtube_class__': '{if $youTubeHref}{$youTubeHref}{/if}',
}

def initiation_progress():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})

    if 'project_name' not in request.form or not request.form['project_name']:
        return jsonify({"message": "No project name"})

    if bool(re.match('^[a-zA-Z]+(?:[A-Z][a-z0-9]*)*$', request.form['project_name'])) != True:
        return jsonify({"message": "text must folows camelCase ."})


    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"})


    lang = request.form['project_lang']
    test_checked = request.form['project_test']
    upload_checked = request.form['project_upload']
    modulation_checked = request.form['project_modulation']


    project_path = helper.create_folder(request.form['project_name'])
    copy_repeated_file_folders_massage = helper.copy_repeated_file_folders(request.form['project_name'])
    html_content = file.read()
    html_content = html_content.replace(b'"images/', b'"project_files/images/')
    html_content = html_content.replace(b"'images/'", b"'project_files/images/'")
    # turn string to soup object
    soup = BeautifulSoup(html_content, 'html.parser')
    if not soup:
        return jsonify({"message": "testing html = " + f'{soup}'})

    moduls_array = {
        'blog': {
            'class': 'i_modular_blog',
            'file': 'blog',
            'name': 'وبلاگ',
            'array': blog_data_array,
            'modular': False,
        },
        'newsletter': {
            'class': 'i_modular_newsletter',
            'name': 'خبرنامه',
            'file': 'newsletter',
            'array': newsletter_data_array,
            'modular': False,
        },
        'advertisement': {
            'class': 'i_modular_adds',
            'name': 'تبلیغات',
            'file': 'advertisement',
            'array': advertisment_data_array,
            'modular': False,
        },
        'news': {
            'class': 'i_modular_news',
            'name': 'اخبار',
            'file': 'news',
            'array': news_data_array,
            'modular': False,
        },
        'menu': {
            'class': 'i_modular_menu',
            'name': 'منو',
            'file': 'menu',
            'modular': menu_module,
            'test_function': unit_test.unit_test_menu
        },
        'footer': {
            'class': 'i_modular_footer',
            'name': 'فوتر',
            'file': 'footer',
            'modular': footer_module,
            'test_function': unit_test.unit_test_footer
        },
        'about_us': {
            'class': 'i_modular_about_us',
            'name': 'درباره ما',
            'file': 'about-us',
            'array': about_us_data_array,
            'modular': False,
        },
        'banner_gallery': {
                'class': 'i_modular_banner_gallery',
            'name': 'گالری بنر و سرچ باکس',
            'file': 'search-box',
            'modular': banner_gallery_module,
            'test_function': unit_test.unit_test_banner_gallery
        },
        'header': {
            'class': False,
            'name': 'هدر',
            'file': 'header',
            'modular': header_module,
            'test_function': unit_test.test_unit_test,
            'tag': 'head'

        },
        'footer_script': {
            'class': False,
            'name': 'اسکریپت فوتر',
            'file': 'footer_script',
            'modular': footer_script_module,
            'test_function': unit_test.test_unit_test,
            'tag': 'script'

        },
        'tours': {
            'class': 'i_modular_tours',
            'name': 'تور',
            'file': 'tours',
            'array': tours_data_array,
            'modular': False,

         },
        'hotels_webservice': {
            'class': 'i_modular_hotels_webservice',
            'name': 'هتل وب سرویس',
            'file': 'hotels-webservice',
            'array': hotels_webservice_data_array,
            'modular': False,

        },
        'hotels__external_cities': {
            'class': 'i_modular_hotels_external_cities',
            'name': 'هتل , شهرهای خارجی',
            'file': 'hotels-external_cities',
            'array': hotels_external_cities_data_array,
            'modular': False,

        },
        'club_weather_section': {
            'class': 'i_modular_club_weather',
            'name': 'باشگاه, نرخ ارز, تبدیل تاریخ و هواشناسی',
            'file': 'club_weather',
            'modular': club_weather_module,

        },
        'fast_flight_search_section': {
            'class': 'i_modular_fast_search_flight',
            'name': 'جستجوی سریع پرواز',
            'file': 'fast_flight_search',
            'modular': fast_flight_search_module,
            'test_function': unit_test.test_unit_test

        }
    }

    moduls_array = {
        'banner_gallery': {
                'class': 'i_modular_banner_gallery',
            'name': 'گالری بنر و سرچ باکس',
            'file': 'search-box',
            'modular': banner_gallery_module,
            'test_function': unit_test.unit_test_banner_gallery
        },
    }

    final_massage = '--'
    if modulation_checked == '1':
        modulation_summary_message = modulation(soup, moduls_array, project_path, lang)
        final_massage = f'{modulation_summary_message}'

        main_page = creating_main_page(html_content, moduls_array, project_path)
        final_massage = final_massage +  '<br><br><br>' 'main_page_creation evaluation_c' + f'{main_page}'

    if test_checked == '1':
        summary_test_message = unit_test_process(html_content, moduls_array, lang)
        final_massage = final_massage  +  ' <br><br><br> test_massage' + f'{summary_test_message}'

    if upload_checked == '1':
        upload_on_gds_massage = upload_on_gds(final_massage, project_path)
        final_massage = final_massage + ' <br><br><br> upload_massage : ' + f'{upload_on_gds_massage}'

    return jsonify({"message": final_massage})


def upload_on_gds(final_massage, project_path):
    try:
        count_modulation = final_massage.count('evaluation_c')
        count_success = final_massage.count('successfully')

        upload_massage = 'not successful'
        copy_controller = 'not successful'
        if count_success >= count_modulation:
            controller_path = project_path + '/' + request.form['project_name'] + '.php'
            copy_controller = helper.copy_file(controller_path , controller_folder_path)
            helper.remove_file(controller_path)
            create_final_folder = helper.create_folder(request.form['project_name'], view_folder_path)
            if create_final_folder:
                upload_massage = helper.copy_directory_contents(project_path, create_final_folder)

        upload_on_gds_massage = f'{upload_massage}' + 'copy controller ' + f'{copy_controller}'
        return upload_on_gds_massage
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def creating_main_page(html_content, moduls_array, project_path):
    try:

        soup = BeautifulSoup(html_content, 'html.parser')
        classes = []
        for module_key, module_info in moduls_array.items():
            if module_info['class']:
                sections = soup.find_all(class_=module_info['class'])
            elif module_info['tag']:
                sections = soup.find_all(module_info['tag'])
                tags_length = len(sections)

            index = 1
            for element in sections:
                first_tag = sections[0]  # Get the first tag
                classes = first_tag.get('class')  # Get all classes of the first tag
                if module_info['class']:
                    if index == 1:
                        file_name = module_info['file']
                    elif index == 2:
                        file_name = module_info['file'] + '-second'
                    else:
                        file_name = module_info['file'] + '-third'

                    file_name = '{include file="include_files/' + file_name + '.tpl' + '"}'
                    if 'menu' in file_name:
                        file_name = '''{if $smarty.session.layout neq 'pwa' }''' + file_name + '''{/if}'''
                    element.replace_with(file_name)
                elif module_info['tag']:
                    if index == tags_length:
                        file_name = module_info['file']
                        file_name = '{include file="include_files/' + file_name + '.tpl' + '"}'
                        element.replace_with(file_name)
                    else:
                        element.replace_with('')

                index = index + 1

        modified_html_content = str(soup)
        soup_str = f'{modified_html_content}'
        main_page = helper.create_file(soup_str, project_path, 'mainPage', 'tpl')
        return main_page
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def modulation(soup, moduls_array, project_path, lang):
    try:

        module_messages = []
        classes = []
        for module_name, module_info in moduls_array.items():
            if module_info['class']:
                sections = soup.find_all(class_=module_info['class'])
            elif module_info['tag']:
                sections = soup.find_all(module_info['tag'])
                tags_length = len(sections)

            index = 1
            for section in sections:
                if section:
                    first_tag = sections[0]  # Get the first tag
                    classes = first_tag.get('class')  # Get all classes of the first tag
                    if module_info['class']:
                        if index == 1:
                            file_name = module_info['file']
                        elif index == 2:
                            file_name = module_info['file'] + '-second'
                        else:
                            file_name = module_info['file'] + '-third'

                        if module_info['modular']:
                            module_messages.append("<br><br> تست ماژول گذاری بخش evaluation_c " + module_info['name'] + str(index) + " = " + module_info['modular'](section, project_path, lang, file_name))
                        elif module_info['array']:
                            module_messages.append("<br><br> تست ماژول گذاری بخش evaluation_c " + module_info['name'] + str(index) + " = " + general_module(section, project_path, lang, file_name, module_info['array']))

                    elif module_info['tag']:
                        if index == tags_length:
                            file_name = module_info['file']
                            section = soup
                            module_messages.append("<br><br> تست ماژول گذاری بخش evaluation_c " + module_info['name']  + " = " + module_info['modular'](section, project_path , lang , file_name))
                    index = index + 1
        modulation_summary_message = '\n'.join(module_messages)
        return modulation_summary_message
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def initiation_test(class_name, module_name, module_test_function, soup, soup_online , lang , online_index, modul_data_array):
    try:
        section = soup.find(class_=class_name)
        sections_online = soup_online.find_all(class_=class_name) if section else None
        sections_online_length = len(sections_online)

        if online_index <= sections_online_length - 1:
            section_online = sections_online[online_index]
            if section_online:
                return module_test_function(section, section_online , lang, modul_data_array)

        return f'ماژول {module_name} بازگذاری نشد'
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def unit_test_process(html_content, moduls_array, lang):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        if not soup:
            return jsonify({"message": "testing html = " + f'{soup}'})

        soup_online = helper.get_online_html()
        if 'خطایی' in soup_online:
            return jsonify({"message": "testing local connection = " + f'{soup_online}'})
        module_test_messages = []

        for module_name, module_info in moduls_array.items():
            sections = soup.find_all(class_=module_info['class'])
            i = 0
            for section in sections:
                if section:
                    if module_info['modular']:
                        module_test_messages.append("<br><br> تست بخش  " + module_info['name'] + " = " + initiation_test(module_info['class'], module_info['name'], module_info['test_function'] , soup, soup_online ,lang , i , {}))
                    elif module_info['array']:
                        module_test_messages.append("<br><br> تست بخش  " + module_info['name'] + " = " + initiation_test(module_info['class'], module_info['name'], unit_test.initiate_general_test , soup, soup_online ,lang , i , module_info['array']))

                    i = i + 1
        summary_test_message = '\n'.join(module_test_messages)
        return summary_test_message
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def create_controller(main_array_string, project_path, contrller_name='test'):
    try:
        contrller_code = '''
        <?php
    //todo: ********************* CREATE ACCESS CLIENT FOR ((FLIGHT + HOTEL)) *********************
    //if(  $_SERVER['REMOTE_ADDR']=='84.241.4.20'  ) {
    //    error_reporting(1);
    //    error_reporting(E_ALL | E_STRICT);
    //    @ini_set('display_errors', 1);
    //    @ini_set('display_errors', 'on');
    //}

    class __controller_name__ extends mainPage {

        public function __construct() {

            parent::__construct();
        }

        public $icons_json = '__main_array_string__';



        public function classTabsSearchBox($service_name) {
            switch ($service_name) {
                case 'Flight_internal':
                    return 'fa-light fa-plane-circle-check';
                    break;
                case 'Flight_external':
                    return 'fa-light fa-plane-circle-check';
                    break;
                case 'Hotel_internal':
                    return 'fa-light fa-bell-concierge';
                    break;
                case 'Hotel_external':
                    return 'fa-light fa-bell-concierge';
                    break;
                case 'Bus':
                    return 'fa-light fa-bus';
                    break;
                case 'Tour_internal':
                    return 'fa-light fa-suitcase-rolling';
                    break;
                case 'Tour_external':
                    return 'fa-light fa-suitcase-rolling';
                    break;
                case 'Visa':
                    return 'fa-light fa-book-atlas';
                    break;
                default:
                    return '';


            }
        }

        public function newClassTabsSearchBox($service_name) {
            return $this->getServicesFromIds($this->icons_json)[$service_name];
        }

        public function getServicesFromIds($json_array) {
            $icon_array = $this->getItemsBykeyFromJsonServicesArray($json_array, 'icon');
            $new_array = [];
            foreach ($icon_array as $id => $icon) {
                $service = str_replace(['_internal', '_external'], '', $id);
                $new_array[$service][$id] = $icon;
            }
            return $new_array;
        }

        public function getItemsBykeyFromJsonServicesArray($json_array, $key) {
            $array = json_decode($json_array, true);
            $new_array = [];
            foreach ($array as $service => $val) {
                $new_array[$service] = $val[$key];
            }
            return $new_array;
        }


        public function nameTabsSearchBox($service_name) {
            $result_array = $this->getItemsBykeyFromJsonServicesArray($this->icons_json, 'name');
            return $result_array[$service_name];
        }


        public function nameBoxSearchBox($service_name) {
            $result_array = $this->getItemsBykeyFromJsonServicesArray($this->icons_json, 'name');
            return $result_array[$service_name];
        }

    }'''

        contrller_code = contrller_code.replace("__controller_name__", contrller_name)
        contrller_code = contrller_code.replace("__main_array_string__", main_array_string)
        final_file_massage = helper.create_file(contrller_code, project_path, contrller_name, 'php')
        return 'contrller name evaluation_c: ' + final_file_massage
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str









def header_module(header_section, project_path, lang='fa', file_name=''):
    try:
        style_links = [link.get('href') for link in header_section.find_all('link', rel='stylesheet')]

        header_contents = '''
{load_presentation_object filename="__controller_name__" assign="obj_main_page" subName="customers"}
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



<head >
    <meta charset="UTF-8">
    <meta test="i_modular_modulation">
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



    {if $smarty.const.GDS_SWITCH neq 'mainPage' }
        <meta class='__not_inside_mainPage__' test="test">

        <link rel="stylesheet" href="project_files/css/{$StyleSheetHeader}">
        {include file="`$smarty.const.FRONT_CURRENT_CLIENT`contentHead.tpl"}
    {/if}

    {if $smarty.const.GDS_SWITCH eq 'mainPage' || $smarty.const.GDS_SWITCH eq 'page'}
        <meta class='__after__all_pags_mainpage__' test="test">

    {/if}

    <meta class='__after__all__' test="test">


</head>


                        '''
        header_section = header_contents

        befor_all = ['css/header.css', 'css/bootstrap.min.css', 'css/header.css']
        between_mainPage_assets = []
        not_inside_mainPage = []
        after__all_pags_mainpage = ['select2.css', 'select2.min.css']
        after__all = ['css/tabs.css', 'css/all.min.css', 'css/register.css', 'css/style.css']

        befor_all = helper.comapre_append_list(befor_all, style_links)
        style_links = helper.delete_assames(style_links, befor_all)

        between_mainPage_assets = helper.comapre_append_list(between_mainPage_assets, style_links)
        style_links = helper.delete_assames(style_links, between_mainPage_assets)

        not_inside_mainPage = helper.comapre_append_list(not_inside_mainPage, style_links)
        style_links = helper.delete_assames(style_links, not_inside_mainPage)

        after__all_pags_mainpage = helper.comapre_append_list(after__all_pags_mainpage, style_links)
        style_links = helper.delete_assames(style_links, after__all_pags_mainpage)

        after__all = helper.comapre_append_list(after__all, style_links)
        style_links = helper.delete_assames(style_links, after__all)

        inside_assets = style_links

        header_section = BeautifulSoup(header_section, "html.parser")
        elements = header_section.find_all(class_='__befor_all__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(befor_all))

        elements = header_section.find_all(class_='__between_mainPage_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(between_mainPage_assets))

        elements = header_section.find_all(class_='__not_inside_mainPage__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(not_inside_mainPage))

        elements = header_section.find_all(class_='__after__all_pags_mainpage__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(after__all_pags_mainpage))

        elements = header_section.find_all(class_='__after__all__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(after__all))

        elements = header_section.find_all(class_='__inside_assets__')
        for element in elements:
            element.replace_with(helper.turn_to_styl_links_assames(inside_assets))

        header_final_content = f'{header_section}'
        header_final_content = header_final_content.replace("__controller_name__", request.form['project_name'])
        header_final_content = header_final_content.replace("</link></link>", "")
        header_final_content = header_final_content.replace("&gt;", ">")
        header_final_content = header_final_content.replace("&gt;", ">")
        header_final_content = header_final_content.replace("&lt;", "<")
        header_final_content = header_final_content.replace("&amp;", "&")

        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(header_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def footer_module(footer_section, project_path, lang='fa', file_name=''):
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
                                {assign var="socialLinksArray" value=['telegram'=>'telegramHref','whatsapp'=> 'whatsappHref','instagram' => 'instagramHref','aparat' => 'aparatHref','youtube' => 'youtubeHref','facebook' => 'facebookHref','linkeDin' => 'linkeDinHref']}

                                {foreach $socialLinks as $key => $val}
                                        {assign var=$socialLinksArray[$val['social_media']] value=$val['link']}
                                {/foreach}'''
        befor_social_media_soup = BeautifulSoup(befor_social_media, "html.parser")
        social_elements = footer_section.find_all(class_=lambda classes: classes and '__social_class__' in classes)
        for social_element in social_elements:
            if social_element:
                social_element.insert_before(befor_social_media_soup)
                for key, val in repeatable_social_links.items():
                    helper.replace_attribute(social_element, key, 'href', val)

        for key, val in repeatable_links.items():
            for item in val:
                helper.replace_attribute_by_text(footer_section, item, 'href', key)

        helper.replace_attribute(footer_section, '__aboutUs_class__', 'string','''{$htmlContent = $about['body']|strip_tags}{$htmlContent|truncate:300}''')
        helper.replace_attribute(footer_section, '__aboutUs_class_href__', 'href','''{$smarty.const.ROOT_ADDRESS}/mag''')
        helper.replace_attribute(footer_section, '__address_class__', 'string','''  {$smarty.const.CLIENT_ADDRESS} ''')
        helper.replace_attribute(footer_section, '__mobile_class__', 'string', '''{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(footer_section, '__mobile_class__', 'href', '''tel:{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(footer_section, '__phone_class__', 'string', '''{$smarty.const.CLIENT_PHONE}''')
        helper.replace_attribute(footer_section, '__phone_class__', 'href', '''tel:{$smarty.const.CLIENT_PHONE}''')
        helper.replace_attribute(footer_section, '__email_class__', 'string', '''{$smarty.const.CLIENT_EMAIL}''')
        helper.replace_attribute(footer_section, '__email_class__', 'href', '''mailto:{$smarty.const.CLIENT_EMAIL}''')
        footer_section = helper.replace_placeholders(footer_section,
                                                     {'__aboutUsLink__': '{$smarty.const.ROOT_ADDRESS}/aboutUs'})
        footer_final_content = f'{before_html}\n{footer_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        footer_final_content = footer_final_content.replace("&gt;", ">")
        footer_final_content = footer_final_content.replace("&lt;", "<")

        return helper.create_file(footer_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def footer_script_module(footer_script_section, project_path, lang='fa', file_name=''):
    try:
        script_links = [link.get('src') for link in footer_script_section.find_all('script')]

        befor_all = ['js/bootstrap.min.js', 'bootstrap.bundle.min.js', 'js/bootstrap.js', 'bootstrap.bundle.min.js',
                     'js/select2.min.js', 'js/select2.js', 'js/header.js']
        between_mainPage_assets = []
        inside_mainPage = []
        remove_assets = ['js/jquery-3.4.1.min.js']
        after__all = ['js/header.js', 'js/mega-menu.js', 'js/script.js']

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
                            </html>
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

        elements = footer_script_section.find_all(class_='__not_inside_mainPage__')
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
        footer_script_final_content = footer_script_final_content.replace("</html>", " ")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(footer_script_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def banner_gallery_module(banner_gallery_section, project_path , lang = 'fa',  file_name = ''):
    try:
        banner_tab = banner_gallery_section.find(class_='__banner_tabs__')
        if banner_tab:
            before_html = ''''''
            after_html = '''{include file="include_files/banner-slider.tpl" }'''
            banner_gallery_final_content = f'{banner_gallery_section}\n{after_html}'
        else:
            # create regex objects containing patterns of items classes
            complex_items_numbers = helper.item_numbers(banner_gallery_section,complex_items_pattern)
            simple_items_numbers = helper.item_numbers(banner_gallery_section,simple_items_pattern)
            complex_items_numbers_max = max(complex_items_numbers) if complex_items_numbers else '0'
            simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
            simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
            max_item_number = max(complex_items_numbers_max, simple_items_numbers_max)

            before_html = '''{assign var="type_data" value=['is_active'=>1 , 'limit' =>10]}
                            {assign var='banners' value=$obj_main_page->galleryBannerMain($type_data)}
                            {if $page.files.main_file}
                                {$banners = [0 => ['pic' => $page.files.main_file.src , 'title' => 'page']]}
                            {/if}
                            <style>
                                .banner-slider-display {
                                    display: none !important;
                                }
                            </style>
                            '''
            after_html = ''

            before_foreach = '''
                            {foreach $banners as $key => $banner}'''
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
                    helper.replace_attribute(simple_element, '__title_class__', 'string', '''{{$banner['title']}}'''.format(num))

                else:
                    simple_element.decompose()
            for num in complex_items_numbers:
                before_if = '''{if $banners[{0}] }'''
                before_if = before_if.replace("{0}", num)
                after_if = '''{/if}'''

                banner_gallery_complex_replacement_data = {
                    "__link__": '''{{$banners[{0}]['link']}}'''.format(num),
                    "__title__": '''{{$banners[{0}]['title']}}'''.format(num),
                }
                complex_element = banner_gallery_section.find(class_=complex_items_class + num)
                helper.add_before_after(banner_gallery_section, complex_items_class + num, before_if, after_if)
                complex_element = banner_gallery_section.find(class_=complex_items_class + num)
                complex_element_final = helper.replace_placeholders(complex_element, banner_gallery_complex_replacement_data)
                complex_element = banner_gallery_section.find(class_=complex_items_class + num)
                complex_element = banner_gallery_section.find(class_=complex_items_class + str(num))

                helper.replace_attribute(complex_element, '__image_class__', 'src', '''{{$banners[{0}]['pic']}}'''.format(num))
                helper.replace_attribute(complex_element, '__image_class__', 'alt', '''{{$banners[{0}]['title']}}'''.format(num))
                helper.replace_attribute(complex_element, '__title_class__', 'string', '''{{$banners[{0}]['title']}}'''.format(num))




        search_box = banner_gallery_section.find(class_='i_modular_searchBox')
        if search_box:
            search_box_modulation = sb.search_box(search_box, project_path)
            search_box_massage = search_box_modulation[0]
            if isinstance(search_box_modulation, str):
                search_box_massage = search_box_modulation
            tab_icons = search_box_modulation[1]
            services_json = json.dumps(tab_icons , ensure_ascii=False)
            creat_controller = create_controller(f'{services_json}', project_path, request.form['project_name'])
            search_box = banner_gallery_section.find(class_='i_modular_searchBox')
            helper.replace_attribute(search_box, '__search_box_tabs__', 'string','''{include file="./search-box/tabs-search-box.tpl"}''')
            helper.replace_attribute(search_box, '__search_boxes__', 'string','''{include file="./search-box/boxs-search.tpl"}''')




        banner_gallery_final_content = f'{before_html}\n{banner_gallery_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        banner_gallery_final_content = banner_gallery_final_content.replace("&gt;", ">")
        banner_gallery_final_content = banner_gallery_final_content.replace("&lt;", "<")

        final_file_massage = helper.create_file(banner_gallery_final_content, include_files_directory, 'search-box', 'tpl')
        return 'searh box : ' + search_box_massage + ' <br><br> banner : ' + final_file_massage + ' <br><br> controller : ' + creat_controller
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str

#dont dare touch this function...you'll regret that
def fast_flight_search_module(fast_flight_search_section, project_path, lang = 'fa',  file_name = ''):
    try:
        fast_flight_search_section = helper.check_if_section_built(project_path ,file_name ,fast_flight_search_section)

        before_html = '''
                        {assign var="params" value=['limit'=>'7','is_group'=>true]}
                        {assign var="cities" value=$obj_main_page->dataFastSearchInternalFlight($params)}
                        {assign var="foreign_cities" value=['IKA','DXBALL','ISTALL','KUL', 'MOWALL' , 'NJF' , 'TBS']}
                        {assign var="__local_max_var__" value=__local_max__}
                      '''


        fast_flight_search_region_array = ['internal', 'external']
        fast_flight_search_type_array = ['multi_city', 'single_city']
        ii = 0
        for region in fast_flight_search_region_array:
            for type in fast_flight_search_type_array:
                befor_cities_html_array_multy = {
                    'internal': '''{assign var="i" value="1"}
                                                {foreach $cities['cities_flight'] as $city}
                                                {if $i < $__local_max_var__ }
                                                ''',
                    'external': ''' {assign var="i" value="1"}
                                                {foreach $foreign_cities as $city_code}
                                                {assign var="params" value=['use_customer_db'=>true,'origin_city'=>$city_code,'destination_city'=>$foreign_cities]}
                                                {assign var="cities" value=$obj_main_page->dataFastSearchInternationalFlight($params)}
                                                {if $i < $__local_max_var__  and {$cities['main']['DepartureCityFa']}}
                                                 ''',
                }
                befor_cities_html_array_single = {
                    'internal': '''{foreach $cities['cities_flight'] as $city} ''',
                    'external': ''' {foreach $cities['sub_cities'] as $sub_city}''',
                }
                after_cities_html = '''
                                         {/if}
                                            {$i =  $i + 1}
                                        {/foreach}
                                         '''
                after_cities_html_single = '''
                                        {/foreach}
                                         '''
                befor_flights_html = {   'internal':   '''
                                                {foreach $city['sub_cities'] as $sub_city}
                                            ''' ,
                                         'external':   '''
                                                {foreach $cities['sub_cities'] as $sub_city}
                                            ''' ,
                                         }
                after_flights_html = '''
                                            {/foreach}
                                         '''

                section_class= '__fast_flight_search__'
                section_var= 'fast_flight_search'
                section_params= 'fast_flight_search_params'
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

                sections = fast_flight_search_section.find(class_=section_class)

                if sections:
                    if type == 'multi_city':
                        origin__cities = sections.find(class_='__origin__cities__')
                        destination__cities = sections.find(class_='__destination__cities__')
                        simple_items_numbers = helper.item_numbers(origin__cities, simple_items_pattern)
                        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
                        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
                        simple_items_numbers_max = int(simple_items_numbers_max)
                        simple_items_numbers_max = simple_items_numbers_max + 2
                        simple_items_numbers_max = f'{simple_items_numbers_max}'
                        before_html = before_html.replace("__local_max__", simple_items_numbers_max)

                        if origin__cities:
                            for num in simple_items_numbers:
                                simple_element = origin__cities.find(class_=simple_items_class + num)
                                if num == simple_items_numbers[0]:
                                    if region == 'internal':
                                        helper.replace_attribute(simple_element, '__button__', 'string','''{$city['main']['Departure_CityFa']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'aria-controls','''{$city['main']['Departure_CityEn']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'data-target','''#{$city['main']['Departure_CityEn']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'id','''{$city['main']['Departure_CityEn']}-tab''')
                                    else:
                                        helper.replace_attribute(simple_element, '__button__', 'string','''{$cities['main']['DepartureCityFa']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'aria-controls','''{$cities['main']['DepartureCityEn']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'data-target','''#{$cities['main']['DepartureCityEn']}''')
                                        helper.replace_attribute(simple_element, '__button__', 'id','''{$cities['main']['DepartureCityEn']}-tab''')

                                    helper.remove_class_from_elements(simple_element, '__button__','show')
                                    helper.remove_class_from_elements(simple_element, '__button__','active')
                                    helper.add_class_to_elements(simple_element, '__button__',' {if $i==1} show active {/if} ')

                                    helper.add_before_after(origin__cities, simple_items_class + num, befor_cities_html_array_multy[region], after_cities_html)
                                else:
                                    simple_element.decompose()

                        simple_items_numbers = helper.item_numbers(destination__cities, simple_items_pattern)
                        if destination__cities:
                            for num in simple_items_numbers:
                                simple_element = destination__cities.find(class_=simple_items_class + num)
                                if num == simple_items_numbers[0]:
                                    if region == 'internal':
                                        helper.replace_attribute(destination__cities, simple_items_class + num, 'aria-labelledby','''{$city['main']['Departure_CityEn']}-tab''')
                                        helper.replace_attribute(destination__cities, simple_items_class + num, 'id','''{$city['main']['Departure_CityEn']}''')
                                    else:
                                        helper.replace_attribute(destination__cities, simple_items_class + num, 'aria-labelledby','''{$cities['main']['DepartureCityEn']}-tab''')
                                        helper.replace_attribute(destination__cities, simple_items_class + num, 'id','''{$cities['main']['DepartureCityEn']}''')

                                    helper.replace_attribute(destination__cities, simple_items_class + num, 'role','''tabpanel''')
                                    helper.remove_class_from_elements(destination__cities, simple_items_class + num,'show')
                                    helper.remove_class_from_elements(destination__cities, simple_items_class + num,'active')
                                    helper.add_class_to_elements(destination__cities, simple_items_class + num,' {if $i==1} show active {/if} ')

                                    ii = ii + 1
                                    helper.add_before_after(destination__cities, simple_items_class + num, befor_cities_html_array_multy[region], after_cities_html)
                                    final_items_pattern = re.compile(r'__final_destination_(\d+)')
                                    final_items_numbers = helper.item_numbers(destination__cities, final_items_pattern)
                                    if final_items_pattern:
                                        for num in final_items_numbers:
                                            final_simple_element = destination__cities.find(class_='__final_destination_' + num)
                                            if num == final_items_numbers[0]:

                                                helper.replace_attribute(destination__cities, '__final_destination_' + num, 'data-target','''#calenderBox''')
                                                helper.replace_attribute(destination__cities, '__final_destination_' + num, 'data-toggle','''modal''')
                                                if region == 'internal':
                                                    helper.replace_attribute(destination__cities, '__final_destination_' + num, 'onclick','''calenderFlightSearch('{$city['main']['Departure_Code']}','{$sub_city['Departure_Code']}')''')
                                                    helper.replace_attribute(destination__cities, '__origin__', 'string','''{$city['main']['Departure_CityFa']}''')
                                                    helper.replace_attribute(destination__cities, '__destination__', 'string','''{$sub_city['Departure_CityFa']}''')
                                                else:
                                                    helper.replace_attribute(destination__cities, '__final_destination_' + num, 'onclick','''calenderFlightSearch('{$cities['main']['DepartureCode']}','{$sub_city['DepartureCode']}')''')
                                                    helper.replace_attribute(destination__cities, '__origin__', 'string','''{$cities['main']['DepartureCityFa']}''')
                                                    helper.replace_attribute(destination__cities, '__destination__', 'string','''{$sub_city['DepartureCityFa']}''')

                                                helper.add_class_to_elements(destination__cities, '__final_destination_' + num,' flightSearchBox ')
                                                helper.add_before_after(destination__cities, '__final_destination_' + num,befor_flights_html[region],after_flights_html)
                                            else:
                                                final_simple_element.decompose()

                                else:
                                    simple_element.decompose()

                    elif type == 'single_city':
                        destination__cities = sections.find(class_='__destination__cities__')
                        simple_items_numbers = helper.item_numbers(destination__cities, simple_items_pattern)
                        simple_items_numbers_max = max(simple_items_numbers) if simple_items_numbers else '0'
                        simple_items_numbers_min = min(simple_items_numbers) if simple_items_numbers else '0'
                        simple_items_numbers_max = int(simple_items_numbers_max)
                        simple_items_numbers_max = simple_items_numbers_max + 2
                        simple_items_numbers_max = f'{simple_items_numbers_max}'
                        before_html = before_html.replace("__local_max__", simple_items_numbers_max)


                        for num in simple_items_numbers:
                            simple_element = sections.find(class_=simple_items_class + num)
                            if num == simple_items_numbers[0]:
                                helper.add_before_after(destination__cities, simple_items_class + num,befor_cities_html_array_multy[region], after_cities_html)
                                final_items_pattern = re.compile(r'__final_destination_(\d+)')
                                final_items_numbers = helper.item_numbers(destination__cities, final_items_pattern)
                                for num in final_items_numbers:
                                    final_simple_element = destination__cities.find(class_='__final_destination_' + num)
                                    if num == final_items_numbers[0]:
                                        if region == 'internal':
                                            helper.replace_attribute(destination__cities, '__final_destination_' + num,'onclick','''calenderFlightSearch('{$city['main']['Departure_Code']}','{$sub_city['Departure_Code']}')''')
                                            helper.replace_attribute(destination__cities, '__origin__', 'string','''{$city['main']['Departure_CityFa']}''')
                                            helper.replace_attribute(destination__cities, '__destination__', 'string','''{$sub_city['Departure_CityFa']}''')
                                        else:
                                            helper.replace_attribute(destination__cities, '__final_destination_' + num,'onclick','''calenderFlightSearch('{$cities['main']['DepartureCode']}','{$sub_city['DepartureCode']}')''')
                                            helper.replace_attribute(destination__cities, '__origin__', 'string','''{$cities['main']['DepartureCityFa']}''')
                                            helper.replace_attribute(destination__cities, '__destination__', 'string','''{$sub_city['DepartureCityFa']}''')

                                        helper.add_before_after(destination__cities, '__final_destination_' + num,befor_flights_html[region], after_flights_html)
                                    else:
                                        final_simple_element.decompose()
                            else:
                                simple_element.decompose()







        fast_flight_search_final_content = f'{before_html}\n{fast_flight_search_section}'

        fast_flight_search_final_content = fast_flight_search_final_content.replace("&gt;", ">")
        fast_flight_search_final_content = fast_flight_search_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(fast_flight_search_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def menu_module(menu_section, project_path , lang = 'fa',  file_name = ''):
    try:

        before_html  = '''{load_presentation_object filename="reservationBasicInformation" assign="objResult"}'''

        helper.replace_attribute_by_text(menu_section, 'ورود  |  ثبت نام' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute_by_text(menu_section, 'ورود یا ثبت نام' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute_by_text(menu_section, 'ورود / ثبت نام' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')
        helper.replace_attribute_by_text(menu_section, 'الدخول / يسجل' , 'string', '{include file="`$smarty.const.FRONT_CURRENT_THEME`topBarName.tpl"}')

        helper.replace_attribute(menu_section, '__login_register_class__2', 'href', '''{if $obj_main_page->isLogin()}javascript:{else}{$smarty.const.ROOT_ADDRESS}/authenticate{/if}''')
        helper.replace_attribute(menu_section, '__login_register_class__', 'href', '''{if $obj_main_page->isLogin()}javascript:{else}{$smarty.const.ROOT_ADDRESS}/authenticate{/if}''')

        helper.add_class_to_elements(menu_section, '__login_register_class__2',' {if $obj_main_page->isLogin()}show-box-login-js main-navigation__button2{else}main-navigation__button1{/if} ')
        helper.add_class_to_elements(menu_section, '__login_register_class__',' {if $obj_main_page->isLogin()}show-box-login-js main-navigation__button2{else}main-navigation__button1{/if} ')
        after_login = '''<div class="main-navigation__sub-menu2 arrow-up show-content-box-login-js" style="display: none">
                            {include file="`$smarty.const.FRONT_CURRENT_THEME`topBar.tpl"}
                        </div>'''
        helper.add_before_after(menu_section, '__login_register_class__', '', after_login)

        # return f'{menu_section}'

        for key, val_set in repeatable_links.items():
            for text in val_set:
                helper.replace_attribute_by_text(menu_section, text, 'href', key)



        helper.replace_attribute(menu_section, '__mobile_class__', 'string', '''{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(menu_section, '__mobile_class__', 'href', '''tel:{$smarty.const.CLIENT_MOBILE}''')
        helper.replace_attribute(menu_section, '__phone_class__', 'string', '''{$smarty.const.CLIENT_PHONE}''')
        helper.replace_attribute(menu_section, '__phone_class__', 'href', '''tel:{$smarty.const.CLIENT_PHONE}''')
        helper.replace_attribute(menu_section, '__email_class__', 'string', '''{$smarty.const.CLIENT_EMAIL}''')
        helper.replace_attribute(menu_section, '__email_class__', 'href', '''mailto:{$smarty.const.CLIENT_EMAIL}''')
        helper.replace_attribute(menu_section, '__logo_class__', 'alt', '''{$obj->Title_head()}''')

        befor_social_media = '''{assign var="socialLinks"  value=$about['social_links']|json_decode:true}
                                {assign var="socialLinksArray" value=['telegram'=>'telegramHref','whatsapp'=> 'whatsappHref','instagram' => 'instagramHref','aparat' => 'aparatHref','youtube' => 'youtubeHref','facebook' => 'facebookHref','linkeDin' => 'linkeDinHref']}

                                {foreach $socialLinks as $key => $val}
                                        {assign var=$socialLinksArray[$val['social_media']] value=$val['link']}
                                {/foreach}'''
        befor_social_media_soup = BeautifulSoup(befor_social_media, "html.parser")
        social_element = menu_section.find(class_='__social_class__')
        if social_element:
            social_element.insert_before(befor_social_media_soup)
            social_element = menu_section.find(
                class_=lambda classes: classes and '__social_class__' in classes)

            for key, val in repeatable_social_links.items():
                helper.replace_attribute(social_element, key, 'href', val)


        menu_final_content = f'{menu_section}'
        menu_final_content = f'{before_html}\n{menu_section}'

        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        # helper.write_text_in_path(project_path, "{inclued 'include_files/menu.tpl'}")
        menu_final_content = menu_final_content.replace("__main_link_href__", "https://{$smarty.const.CLIENT_MAIN_DOMAIN}")
        menu_final_content = menu_final_content.replace("&gt;", ">")
        menu_final_content = menu_final_content.replace("&lt;", "<")

        return helper.create_file(menu_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def club_weather_module(club_weather_section, project_path, lang = 'fa',  file_name = ''):
    try:
        repeatable_links_club = {
        '{$smarty.const.ROOT_ADDRESS}/loginUser':
            {
                'ورود'
            },
        '{$smarty.const.ROOT_ADDRESS}/weather':
            {
                'علم الارصاد الجوية', 'meteorology', 'weather', 'هواشناسی'
            },
        '{$smarty.const.ROOT_ADDRESS}/currency':
            {
                'نرخ ارز'
            },
        }

        helper.replace_attribute(club_weather_section, '__JalaliToMiladi_button__', 'onclick', '''convertJalaliToMiladi()''')
        helper.replace_attribute(club_weather_section, '__MiladiToJalali_button__', 'onclick', '''convertMiladiToJalali()''')

        helper.add_class_to_elements(club_weather_section, '__JalaliToMiladi_input__','convertShamsiMiladiCalendar')
        helper.add_class_to_elements(club_weather_section, '__MiladiToJalali_input__','convertMiladiShamsiCalendar')

        helper.replace_attribute(club_weather_section, '__JalaliToMiladi_input__', 'name', '''txtShamsiCalendar''')
        helper.replace_attribute(club_weather_section, '__JalaliToMiladi_input__', 'id', '''txtShamsiCalendar''')

        helper.replace_attribute(club_weather_section, '__MiladiToJalali_input__', 'name', '''txtMiladiCalendar''')
        helper.replace_attribute(club_weather_section, '__MiladiToJalali_input__', 'id', '''txtMiladiCalendar''')



        helper.replace_attribute(club_weather_section, '__email_class__', 'string', '''{$smarty.const.CLIENT_EMAIL}''')
        helper.replace_attribute(club_weather_section, '__email_class__', 'href', '''mailto:{$smarty.const.CLIENT_EMAIL}''')

        for key, val in repeatable_links.items():
            for item in val:
                helper.replace_attribute_by_text(club_weather_section, item, 'href', key)

        club_weather_final_content = f'{club_weather_section}'
        club_weather_final_content = club_weather_final_content.replace("&gt;", ">")
        club_weather_final_content = club_weather_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(club_weather_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


advertisment_data_array = {
    'general_region_array': [''],
    'general_type_array': [''],
    'before_html': '''''',
    'before_html_local': '''{load_presentation_object filename="functions" assign="objFunctions"}
                            {assign var="advertises" value=$objFunctions->getConfigContentByTitle('home_page_advertise')}
                    ''',
    'after_html': '''{/if}''',
    'before_foreach_local':'''{foreach $__general_var__ as $item} {if $__local_min_var__ <= $__local_max_var__}''',
    'after_foreach_local':'''
                            {$__local_min_var__ = $__local_min_var__ + 1}
                            {/if}
                        {/foreach}
                        ''',

    'replace_classes_local': {
    '__image_class__': {'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/{$item['image']}''', 'alt': '''{$item['title']}'''},
    '__title_class__': {'string': '''{$item['title']}'''},
},
    'replace_comlex_classes_local': {
    '__image_class__': {
        'src': '''{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/{$__general_var__[{0}]['image']}''',
        'alt': '''{$__general_var__[{0}]['alt']}'''},
    '__title_class__': {'string': '''{$__general_var__[{0}]['title']}'''},
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

    'unique_key': 'advertisement',
    'no_chiled': 'yes',
    'replace_classes_general': {
    },
}

news_data_array = {
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
    'before_foreach_local': '''{foreach $__general_var__ as $item} {if $__local_min_var__ <= $__local_max_var__}''',
    'after_foreach_local': '''
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

about_us_data_array = {
    'general_region_array': [''],
    'general_type_array': [''],
    'before_html': '''{$check_general = true}''',
    'before_html_local': '''''',
    'after_html': '''{/if}''',
    'before_foreach_local': '''''',
    'after_foreach_local': '''''',

    'replace_classes_local': {},
    'replace_comlex_classes_local': {},

    'generals_simple_replacements': {},
    'generals_complex_replacements': {},

    'before_star_simple': '''''',
    'before_dark_star_simple': '',
    'before_star_complex': '''''',
    'before_dark_star_complex': '''''',

    'unique_key': 'about_us',
    'no_chiled': 'yes',
    'replace_classes_general': {
        '__aboutUs_class__': {'string': '''{$htmlContent = $about['body']|strip_tags}{$htmlContent|truncate:300}'''},
        '__aboutUs_class_href__': {'href': '''{$smarty.const.ROOT_ADDRESS}/aboutUs'''},
        '__mobile_class__': {'string': '''{$smarty.const.CLIENT_MOBILE}''',
                             'href': '''tel:{$smarty.const.CLIENT_MOBILE}'''},
        '__phone_class__': {'string': '''{$smarty.const.CLIENT_PHONE}''',
                            'href': '''tel:{$smarty.const.CLIENT_PHONE}'''},
        '__email_class__': {'string': '''{$smarty.const.CLIENT_EMAIL}''',
                            'href': '''mailto:{$smarty.const.CLIENT_EMAIL}'''},
    },
}

newsletter_data_array = {
    'general_region_array': [''],
    'general_type_array': [''],
    'before_html': '''{$check_general = true}''',
    'before_html_local': '''''',
    'after_html': '''{/if}''',
    'before_foreach_local': '''''',
    'after_foreach_local': '''''',

    'replace_classes_local': {},
    'replace_comlex_classes_local': {},

    'generals_simple_replacements': {},
    'generals_complex_replacements': {},

    'before_star_simple': '''''',
    'before_dark_star_simple': '',
    'before_star_complex': '''''',
    'before_dark_star_complex': '''''',

    'unique_key': 'newsletter',
    'no_chiled': 'yes',
    'replace_classes_general': {
        '__name_class__': {'name': '''NameSms''', 'id': '''NameSms''', 'class': '''full-name-js'''},
        '__email_class__': {'name': '''EmailSms''', 'name': '''EmailSms''', 'class': '''email-js'''},
        '__phone_class__': {'name': '''CellSms''', 'id': '''CellSms''', 'class': '''mobile-js'''},
        '__submit_class__': {'onclick': 'submitNewsLetter()'},
    },
}

blog_data_array = {
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
    'before_foreach_local': '''
                        {foreach $__general_var__ as $key => $item}
                            {if $__local_min_var__ <= $__local_max_var__}
                        ''',
    'after_foreach_local': '''
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

tours_data_array = {
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
    'before_foreach_local': '''
                        {foreach $__general_var__ as $item}
                            {if $__local_min_var__ <= $__local_max_var__}
                        ''',
    'after_foreach_local': '''
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

hotels_webservice_data_array = {
    'general_region_array': ['internal', 'external'],
    'general_type_array': [''],
    'before_html': '''{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}''',
    'before_html_local': '''
                        {assign var="__params_var__" value=['Count'=> '__local_max_limit__', 'type' =>'__country__']}
                        {assign var='__general_var__' value=$obj_main_page->getHotelWebservice($__params_var__)}
                        {if $__general_var__}
                            {assign var='check_general' value=true}
                        {/if}
                        {assign var="__local_min_var__" value=__local_min__}
                        {assign var="__local_max_var__" value=__local_max__}
                    ''',
    'after_html': '''{/if}''',
    'before_foreach_local': '''
                        {foreach $__general_var__ as $item}
                            {if $__local_min_var__ <= $__local_max_var__}
                        ''',
    'after_foreach_local': '''
                            {$__local_min_var__ = $__local_min_var__ + 1}
                            {/if}
                        {/foreach}
                        ''',
    'replace_classes_local': {
        '__title_class__': {'string': '''{$item['Name']}'''},
        '__city_class__': {'string': '''{$item['City']}'''},
        '__degree_class__': {'string': '''{$item['StarCode']}'''},
        # '___price_class__': {'string': '''{$item['StarCode']}'''},
        '__description_class__': {'string': '''{$item['comment']|truncate:300}'''},
        '__image_class__': {
            'src': '''{$item['Picture']}''',
            'alt': '''{$item['City']}'''},
    },
    'replace_comlex_classes_local': {
        '__title_class__': {'string': '''{$__general_var__[{0}]['Name']}'''},
        '__city_class__': {'string': '''{$__general_var__[{0}]['City']}'''},
        '__degree_class__': {'string': '''{$__general_var__[{0}]['StarCode']}'''},
        # '___price_class__': {'string': '''{$__general_var__[{0}]['StarCode']}'''},
        '__description_class__': {'string': '''{$__general_var__[{0}]['comment']|truncate:300}'''},
        '__image_class__': {
            'src': '''{$__general_var__[{0}]['Picture']}''',
            'alt': '''{$__general_var__[{0}]['City']}'''},
    },
    'generals_simple_replacements': {
        "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailHotel/api/{$item['HotelIndex']}''',
    },
    'generals_complex_replacements': {
        "__link__": '''{$smarty.const.ROOT_ADDRESS}/detailHotel/api/{$__general_var__[{0}]['HotelIndex']}''',
    },

    'before_star_simple': '''{for $i = 0; $i < count($item['StarCode']); $i++}''',
    'before_dark_star_simple': '''{for $i = count($item['StarCode']); $i < 6; $i++}''',
    'before_star_complex': '''{for $i = 0; $i < count($__general_var__['StarCode']); $i++}''',
    'before_dark_star_complex': '''{for $i = count($__general_var__['StarCode']); $i < 6; $i++}''',
    'unique_key': 'hotel',
    'no_chiled': '',

    'replace_classes_general': {},

}

hotels_external_cities_data_array = {
    'general_region_array': ['external'],
    'general_type_array': ['city'],
    'before_html': '''''',
    'before_html_local': '''                                        
                        {assign var='__general_var__' value=$obj_main_page->getExternalHotelCity()}
                        {if $__general_var__}
                            {assign var='check_general' value=true}
                        {/if}
                        {assign var="__local_min_var__" value=__local_min__}
                        {assign var="__local_max_var__" value=__local_max__}
                    ''',
    'after_html': '''{/if}''',
    'before_foreach_local': '''
                        {foreach $__general_var__ as $item}
                            {if $__local_min_var__ <= $__local_max_var__}
                        ''',
    'after_foreach_local': '''
                            {$__local_min_var__ = $__local_min_var__ + 1}
                            {/if}
                        {/foreach}
                        ''',
    'replace_classes_local': {
        '__title_class__': {'string': '''{$item['DepartureCityFa']}'''},
        '__city_class__': {'string': '''{$item['City']}'''},
        '__image_class__': {
            'src': '''assets/images/hotel/{$item['DepartureCode']}.jpg''',
            'alt': '''{$item['DepartureCityFa']}'''},
    },
    'replace_comlex_classes_local': {
        '__title_class__': {'string': '''{$__general_var__[{0}]['Name']}'''},
        '__city_class__': {'string': '''{$__general_var__[{0}]['City']}'''},
        '__image_class__': {
            'src': '''assets/images/hotel/{$__general_var__[{0}]['DepartureCode']}.jpg''',
            'alt': '''{$__general_var__[{0}]['DepartureCityFa']}'''},
    },
    'generals_simple_replacements': {
        "__link__": '''{$smarty.const.ROOT_ADDRESS}/resultExternalHotel/{$item['CountryEn']}/{$item['DepartureCityEn']}/{$objDate->daysAfterToday('7')}/{$objDate->daysAfterToday('8')}/1/R:2-0-0''',
    },
    'generals_complex_replacements': {
        "__link__": '''{$smarty.const.ROOT_ADDRESS}/resultExternalHotel/{$__general_var__[{0}]['CountryEn']}/{$__general_var__[{0}]['DepartureCityEn']}/{$objDate->daysAfterToday('7')}/{$objDate->daysAfterToday('8')}/1/R:2-0-0''',
    },

    'before_star_simple': '''{for $i = 0; $i < count($item['StarCode']); $i++}''',
    'before_dark_star_simple': '''{for $i = count($item['StarCode']); $i < 6; $i++}''',
    'before_star_complex': '''{for $i = 0; $i < count($__general_var__['StarCode']); $i++}''',
    'before_dark_star_complex': '''{for $i = count($__general_var__['StarCode']); $i < 6; $i++}''',
    'unique_key': 'hotel_function',
    'no_chiled': '',

    'replace_classes_general': {},

}


def general_module(generals_section, project_path, lang = 'fa',  file_name = '', modul_data_array = {} ):
    try:
        generals_section = helper.check_if_section_built(project_path ,file_name ,generals_section)

        before_html = modul_data_array['before_html']
        after_html = modul_data_array['after_html']

        general_region_array = modul_data_array['general_region_array']
        general_type_array = modul_data_array['general_type_array']
        before_html_local = modul_data_array['before_html_local']


        before_foreach_local = modul_data_array['before_foreach_local']
        after_foreach_local = modul_data_array['after_foreach_local']

        replace_classes_local = modul_data_array['replace_classes_local']
        replace_comlex_classes_local = modul_data_array['replace_comlex_classes_local']

        generals_simple_replacements = modul_data_array['generals_simple_replacements']
        generals_complex_replacements = modul_data_array['generals_complex_replacements']

        before_star_simple = modul_data_array['before_star_simple']
        before_dark_star_simple = modul_data_array['before_dark_star_simple']
        before_star_complex = modul_data_array['before_star_complex']
        before_dark_star_complex = modul_data_array['before_dark_star_complex']

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
                else:
                    sections = generals_section.find_all(class_=section_class)

                if sections:
                    for local_section in sections:
                        if no_chiled == 'yes':
                            local_section = generals_section
                        before_html_local = before_html_local.replace("__type__", type)
                        before_html_local = before_html_local.replace("__country__", region)
                        before_html_local = before_html_local.replace("__general_var__", section_var)
                        before_html_local = before_html_local.replace("__params_var__", section_params)
                        before_html_local = before_html_local.replace("__local_min_var__", local_min_var)
                        before_html_local = before_html_local.replace("__local_max_var__", local_max_var)
                        before_foreach_local = before_foreach_local.replace("__local_min_var__", local_min_var)
                        before_foreach_local = before_foreach_local.replace("__local_max_var__", local_max_var)
                        before_foreach_local = before_foreach_local.replace("__general_var__", section_var)
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
                            simple_element = local_section.find(class_=simple_items_class + num)
                            if num == simple_items_numbers[0]:
                                simple_element = helper.replace_placeholders(simple_element, generals_simple_replacements)
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
                            before_c_item_local = '''{if $__general_var__[{0}]}'''
                            after_c_item_local = '''{/if}'''
                            before_c_item_local = before_c_item_local.replace("__general_var__", section_var)
                            before_c_item_local = before_c_item_local.replace("{0}", f"{num}")
                            after_c_item_local = after_c_item_local.replace("__general_var__", section_var)
                            after_c_item_local = after_c_item_local.replace("{0}", f"{num}")

                            complex_element = local_section.find(class_=complex_items_class + num)
                            for gcr_key, gcr_val in generals_complex_replacements.items():
                                gcr_val = gcr_val.replace("__general_var__", section_var)
                                gcr_val = gcr_val.replace("{0}", f"{num}")
                                final_gcr = {
                                    f'{gcr_key}': f'{gcr_val}'
                                }
                                complex_element = helper.replace_placeholders(complex_element, final_gcr)

                            complex_element = local_section.find(class_=complex_items_class + num)
                            helper.add_before_after(local_section, complex_items_class + num, before_c_item_local, after_c_item_local)
                            complex_element = local_section.find(class_=complex_items_class + num)
                            for class_name, val in replace_comlex_classes_local.items():
                                for atr, value in val.items():
                                    value = value.replace("{0}", f'{num}')
                                    value = value.replace("__general_var__", section_var)
                                    helper.replace_attribute(complex_element, class_name, atr, value)

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
                                        new_dark_star = before_dark_star_complex + str(dark_star_elements) + '''{/for}'''
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

                            for key, val in repeatable_social_links.items():
                                helper.replace_attribute(social_element, key, 'href', val)

                        if replace_classes_general != '':
                            for class_name, val in replace_classes_general.items():
                                for atr, value in val.items():
                                    if atr != 'class':
                                        helper.replace_attribute(local_section, class_name, atr, value)
                                    else:
                                        helper.add_class_to_elements(local_section, class_name,value)


        if not os.path.exists(project_path + '/include_files/' + file_name + '.tpl'):
            before_html = before_html + '\n' + '''{if $check_general}'''
        else:
            before_html = before_html + '\n' + '''{if 1 == 1}'''



        generals_final_content = f'{before_html}\n{generals_section}\n{after_html}'

        generals_final_content = generals_final_content.replace("__all_link_href__", "{$smarty.const.ROOT_ADDRESS}/page/" + special_page)
        generals_final_content = generals_final_content.replace("&gt;", ">")
        generals_final_content = generals_final_content.replace("&lt;", "<")
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        return helper.create_file(generals_final_content, include_files_directory, file_name, 'tpl')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str



