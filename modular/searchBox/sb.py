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
import zipfile
import traceback


def search_box(searchBox_section, project_path, lang = 'fa',  file_name = ''):
    try:
        tabs_section = searchBox_section.find(class_='__search_box_tabs__')
        boxes_section = searchBox_section.find(class_='__search_boxes__')
        has_tpl_services = {'Tour': Tour,
                            'Visa': Visa,'Train': Train,'Insurance': Insurance,'Bus': Bus,'GashtTransfer': GashtTransfer,'Entertainment': Entertainment,'Europcar': Europcar
                            }

        # getting the tabs and put them in array adn tab.tpl file in searchbox directory
        hrefs_list = []
        tab_icons = {}
        if tabs_section:
            all_a_tags = tabs_section.find_all('a')
            boxes_path = helper.create_folder('boxes', project_path + '/include_files/search-box')
            sections_path = helper.create_folder('sections', project_path + '/include_files/search-box/boxes')

            for a in all_a_tags:
                if a.get('href'):
                    item = a.get('href').lstrip('#')
                    parent_li = a.find_parent('li')
                    parent_li = f'{parent_li}'
                    parent_li = parent_li.replace("nav-link", 'nav-link {if $active} active {/if}')
                    hrefs_list.append(item)
                    modified_id = item.replace('_internal', '').replace('_external', '')
                    item_path = helper.create_folder(modified_id, sections_path)

                    check_svg = a.find('svg')
                    check_i = a.find('i')
                    check_h4 = a.find('h4')
                    temprary = {}
                    if check_i:
                        temprary['icon'] = helper.icons_clean_serialize_string(f'{check_i}')
                    if check_h4:
                        temprary['name'] = helper.icons_clean_serialize_string(f'{check_h4.text.strip()}')

                    tab_icons[item] = temprary

            testTabs = modulationSearchBoxTabs(project_path + '/include_files/search-box', parent_li)
            testBoxes = modulationSearchBoxBoxes(project_path + '/include_files/search-box')


        # getting the ids of boxes and add them to href array. and put them in searchbox dierctory
        id_lists = hrefs_list
        boxs = boxes_section.find_all(class_='__box__')
        items_massages = []
        ##modulation of boxes
        for b in boxs:
            box_id = b.get('id')
            modified_id = box_id.replace('_internal', '').replace('_external', '')
            if box_id:
                if box_id not in hrefs_list:
                    item_path = helper.create_folder(box_id, sections_path)
                    id_lists.append(box_id)
                if modified_id in has_tpl_services:
                    has_tpl_massage = has_tpl_services[modified_id](f'{b}' ,boxes_path, modified_id, box_id)
                else:
                    helper.if_dosnt_exist_create_else_add(boxes_path, modified_id, f'{b}')

        ##separation of codes
        for b in boxs:
            box_id = b.get('id')
            modified_id = box_id.replace('_internal', '').replace('_external', '')
            if box_id:
                final_massage = seprate_search_box_codes(project_path,modified_id)
                item_massage = box_id + " : " + final_massage
                items_massages.append(item_massage + '<br><br> evaluation_c')



        # # creating relational services array
        # services_array = {}
        # for item in id_lists:
        #     modified_item = item.replace('_internal', '').replace('_external', '')
        #     if item in services_array:
        #         services_array[item].append(modified_item)
        #     else:
        #         services_array[item] = modified_item


        return [f'{items_massages}', tab_icons]
    except Exception as e:
        return 'search_box()' + str(e)  # Return the exception message for now


def seprate_search_box_codes(project_path, box_name):
    try:
        form_detection_array = {
            'Flight': {
                'internal': {'switch-input-js': 'btn_radio_internal_external.tpl',
                             'internal-one-way-js': 'btn_type_way.tpl',
                             'departure-date-internal-js': 'date_flight.tpl',
                             'internal-arrival-date-js': 'date_flight.tpl',
                             'route_destination_internal-js': 'destination_selection.tpl',
                             'route_origin_internal-js': 'origin_selection.tpl',
                             'box-of-count-passenger-js': 'passenger_count.tpl'},
                'international': {'select-type-way-js': 'btn_type_way.tpl',
                                  'departure-date-international-js': 'date_flight.tpl',
                                  'destination-international-js': 'destination_search_box.tpl',
                                  'iata-origin-international-js': 'origin_search_box.tpl',
                                  'international-adult-js': 'passenger_count.tpl', },
                'multi-way': {'newAdditionalExternal($(this))': 'add_flight_multy_way.tpl',
                              'click_flight_multiTrack': 'btn_type_way.tpl',
                              'multi-adult-js': 'count_passenger_multi_way.tpl',
                              'date-multi-0-js': 'date_first_multi_way.tpl',
                              'list-multi-0-origin-airport-international-js': 'departure_first_multy_way.tpl',
                              'iata-multi-0-destination-international-js': 'destination_first_multi_way.tpl',
                              # additional way
                              'multi-1-origin-international-js': 'departure_secend_multi_way.tpl',
                              'iata-multi-1-destination-international-js': 'destination_second_multi_way.tpl',
                              'date-multi-1-js': 'date_second_multi_way.tpl',
                              'nclick="removeAdditionalExternal($(this))"': 'remove_additional_multi_way.tpl',
                              # end of additional way

                              },

            },
            'Tour': {
                'internal': {'switch-input-tour-js': 'btn_radio_internal_external.tpl',
                             'internal-date-travel-tour-js': 'date_teravel.tpl',
                             'internal-destination-tour-js': 'destination_city_tour.tpl',
                             'internal-origin-tour-js': 'origin_city_tour.tpl', },
                'international': {'international-destination-city-tour-js': 'city_destination.tpl',
                                  'international-tour-origin-city-js': 'city_origin.tpl',
                                  'international-destination-tour-js': 'country_destination.tpl',
                                  'tourOriginCountryPortal': 'country_origin.tpl',
                                  'international-date-travel-tour-js': 'date_travel.tpl', },
            },
            'Hotel': {
                'internal': {
                    '''check-in-date-js''': 'check_in_date.tpl',
                    '''endDateForHotelLocal''': 'check_out_date.tpl',
                    '''internal-hotel-passenger-picker-js''': 'count_passenger_room.tpl',
                    '''searchCity''': 'destination_city.tpl',
                },
                'international': {
                    'switch-input-hotel-js': 'btn_radio_internal_external.tpl',
                    '''check-in-date-international-js''': 'check_in_date.tpl',
                    '''endDateForExternalHotelInternational''': 'check_out_date.tpl',
                    '''international-hotel-passenger-picker-js''': 'count_passenger_room.tpl',
                    '''searchCity''': 'destination_city.tpl',
                },
            },
            'Train': {
                'main': {
                    '''select-type-way-js''': 'btn-type-way.tpl',
                    '''train-departure-date-js''': 'date_train.tpl',
                    '''destination-train-js''': 'destination_selection.tpl',
                    '''origin-train-js''': 'origin_selection.tpl',
                    '''box-of-count-passenger-boxes-js''': 'passenger_count.tpl',
                }
            },
            'Package': {
                'main': {
                    '''departure-date-package-js''': 'date_package.tpl',
                    '''destination-package-js''': 'destination_search_box.tpl',
                    '''origin-package-js''': 'origin_search_box.tpl',
                    '''cbox-package-count-passenger-js''': 'passenger_count.tpl',
                }
            },
            'Bus': {
                'main': {
                    'departure_date_bus': 'date_bus.tpl',
                    'select-destination-route-bus-js': 'destination_selection.tpl',
                    'select-origin-route-bus-js': 'origin_selection.tpl',
                }
            },
            'Insurance': {
                'main': {
                }
            },
            'GashtTransfer': {
                'gasht': {
                    'gasht-date-js': 'date_gasht.tpl',
                    'gasht_destination': 'destination.tpl',
                    'gasht-type-js': 'type_gasht.tpl',
                },
                'transfer': {
                    'transfer-date-js': 'date_transfer.tpl',
                    'transfer-destination-js': 'destination.tpl',
                    'transfer-type-js': 'type_accept.tpl',
                    'transfer-location-js': 'type_destination.tpl',
                    'transfer-vehicle-type-js': 'type_device.tpl',
                },
            },
            'Europcar': {
                'main': {
                    'type_rent_car-js': 'carType.tpl',
                    'delivery_rent-car-date-js': 'deliveryDate.tpl',
                    'select-delivery-place-rent-car-js': 'deliveryPlace.tpl',
                    'rent-start-date-js': 'rentDate.tpl',
                    'select-city-rent-car-js': 'rentPlace.tpl',
                }
            },
            'Entertainment': {
                'main': {
                    'category-entertainment-js': 'category_entertainment.tpl',
                    'getEntertainmentCategoriesSearchBox': 'city_destination.tpl',
                    'getEntertainmentCities': 'country_destination.tpl',
                    'sub-category-entertainment-js': 'sub_category_entertainment.tpl',
                }
            },
            'Visa': {
                'main': {
                    'continent-visa-js': 'continent_visa.tpl',
                    'country-visa-js': 'country_visa.tpl',
                    'box-of-count-passenger-boxes-js': 'passenger_count.tpl',
                    'visa-type-js': 'type_visa.tpl',
                }
            }
        }
        section = f"{helper.read_file(project_path + '/include_files/search-box/boxes/' + box_name + '.tpl')}"
        soup = BeautifulSoup(section, 'html.parser')
        boxes = soup.find_all(class_='__box__')
        for box in boxes:
            forms = box.find_all('form')
            specific_elements = box.find_all(class_='radios')
            all_main_elements = forms + specific_elements


            main_folder_path = project_path + '/include_files/search-box/boxes/sections/' + box_name + '/'
            for element in all_main_elements:
                compere_dic = check_how_much_class_contains_soup(element, form_detection_array[box_name])
                sub_folder_name = max(compere_dic, key=compere_dic.get)
                if sub_folder_name != 'main':
                    sub_folder_path = helper.create_folder(sub_folder_name, main_folder_path)
                    if 'exists' in sub_folder_path:
                        sub_folder_path = main_folder_path + '/' + sub_folder_name + '/'
                else:
                    sub_folder_path = main_folder_path


                for pattern, file_name in form_detection_array[box_name][sub_folder_name].items():
                    modified_file_name = file_name.replace('.tpl', '')
                    file_path = helper.if_dosnt_exist_create_else_add(sub_folder_path, modified_file_name, '')
                tag_replace = continues_tag_rplacment(element, form_detection_array[box_name][sub_folder_name].items(), sub_folder_path, box_name, sub_folder_name)

        final_string = helper.search_box_clean_serialize_string(f'{soup}')
        result = helper.create_or_replace_file(project_path + '/include_files/search-box/boxes/' + box_name + '.tpl', f'{final_string}')
        return f'{result}'

    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def continues_tag_rplacment(tag, patterns, folder_path, box_name, sub_folder_name):
    try:
        count = 0
        tag_string = f'{tag}'
        modified_file_name = False
        for pattern, file_name in patterns:
            if pattern in tag_string:
                modified_file_name = file_name.replace('.tpl', '')
                count = count + 1
        if modified_file_name and count <= 2:
            tag_string = helper.search_box_clean_serialize_string(tag_string)
            file_path = helper.if_dosnt_exist_create_else_add(folder_path, modified_file_name, tag_string)
            if 'main' != sub_folder_name:
                tag.replace_with('''{include file="./sections/''' + box_name + '/' + sub_folder_name + '/' + modified_file_name + '.tpl' + '''"}''')
            else:
                tag.replace_with('''{include file="./sections/''' + box_name + '/' + modified_file_name + '.tpl' + '''"}''')

        elif modified_file_name and count > 2:
            sub_tags = tag.find_all(recursive=False)
            for sub_tag in sub_tags:
                continues_tag_rplacment(sub_tag, patterns, folder_path, box_name, sub_folder_name)

        return tag
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def check_how_much_class_contains_soup(soup_element, detection_dict):
    try:
        final_dict = {}
        for region, dic in detection_dict.items():
            counter = 0
            for detector, file_name in dic.items():
                element = f'{soup_element}'
                if detector in element:
                    counter = counter + 1
            final_dict[region] = counter
        return final_dict
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def modulationSearchBoxTabs(search_box_path, tab):
    try:
        tab = BeautifulSoup(tab, 'html.parser')

        content = '''
                        {assign var='tab_counter' value=0}
                        {foreach $info_access_client_to_service as $key=>$client}
                            {if $obj_main_page->newClassTabsSearchBox($client['MainService'])}
                                {if ( $smarty.const.GDS_SWITCH eq 'mainPage' ) || ($active_tab eq 'internalFlight' && $client['MainService'] eq 'Flight' || $active_tab eq $client['MainService'])}
                                    {foreach $obj_main_page->newClassTabsSearchBox($client['MainService']) as $tab_id => $icon}
                                        <li class="nav-item">
                                            <a onclick="changeText(`{$obj_main_page->nameBoxSearchBox($tab_id)}` , 'null')"
                                               class="{$client['MainService']}-tab-pic nav-link {if $tab_counter eq 0 }active{/if}"
                                               id="{$tab_id}-tab" data-toggle="tab" href="#{$tab_id}">
                                                __put__tab__here__
                                            </a>
                                        </li>
                                        {$tab_counter = $tab_counter + 1}
                                    {/foreach}
                                {/if}
                            {/if}
                        {/foreach}

        '''
        tab = helper.remove_tag_from_soup_object(tab, 'li')
        tab = helper.remove_tag_from_soup_object(tab, 'a')
        helper.replace_attribute_by_tag(tab, 'h4', 'string','''{$obj_main_page->nameTabsSearchBox($tab_id)}''')
        check_i = tab.find('i')
        if check_i:
            check_i.replace_with('''{$icon}''')

        content = content.replace("__put__tab__here__", f'{tab}')

        content = helper.search_box_clean_serialize_string(f'{content}')

        return helper.create_file(content, search_box_path, 'tabs-search-box', 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, modulationSearchBoxTabs(): ' + str(e)  # Return the exception message for no


def modulationSearchBoxBoxes(search_box_path):
    try:
        content = '''{assign var="obj_main_page" value=$obj_main_page }
                        {foreach $info_access_client_to_service as $key=>$client}
                            {if $obj_main_page->newClassTabsSearchBox($client['MainService'])}
                                {if  $smarty.const.GDS_SWITCH eq 'mainPage'}
                                    {include file="./boxes/{$client['MainService']}.tpl" client=$client}
                                 {else}
                                    {if $active_tab eq 'internalFlight' && $client['MainService'] eq 'Flight' || $active_tab eq $client['MainService']}
                                        {include file="./boxes/{$client['MainService']}.tpl" client=$client active=true}
                                    {/if}
                                {/if}
                            {/if}
                        {/foreach}
                        
                        
                        '''
        content = helper.search_box_clean_serialize_string(f'{content}')
        return helper.create_file(content, search_box_path, 'boxs-search', 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, modulationSearchBoxBoxes(): ' + str(e)  # Return the exception message for no


def Tour(section=False, item_path=False, file_name=False, type=False):
    try:

        options_array = [
        '''
                                {assign var="cities" value=$obj_main_page->getOriginTourCities()}
                                 <option value="">##ChoseOption##...</option>
                                  {foreach $cities as $city}
                                        <option value="{$city['id']}">{$city['name']}</option>
                                    {/foreach}
        ''',
        '''<option value="">##ChoseOption##...</option>''',

        '''                         <option value="">##ChoseOption##...</option>
                                 {foreach $date_tour as $date}
                                        <option value='{$date['value']}'>{$date['text']}</option>
                                    {/foreach}
        ''',
        '''
                                {assign var="params" value=['type'=>'international']}
                        {assign var="cities_international" value=$obj_main_page->getOriginTourCities($params)}
                                 <option value="">##ChoseOption##...</option>
                                  {foreach $cities_international as $city}
                                        <option value="{$city['id']}">{$city['name']}</option>
                                    {/foreach}
        ''',
        '''<option value="">##ChoseOption##...</option>''',
        '''<option value="">##ChoseOption##...</option>''',
        '''
                                {assign var="date_tour" value=$obj_main_page->datesTour()}
                                {foreach $date_tour as $date}
                                    <option value='{$date['value']}'>{$date['text']}</option>
                                {/foreach}
        '''
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        if 'Tour_external' in type:
            i = 3
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section =  f'{section}'
        return helper.if_dosnt_exist_create_else_add(item_path, file_name, f'{final_section}')
    except Exception as e:
        traceback_str = traceback.format_exc()
        return str(e) + '\nTraceback:\n' + traceback_str


def Visa(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''
                        {assign var="continents" value=$obj_main_page->getListContinents()}
                    '''
        options_array = [
        '''
                            {foreach $continents as $continent}
                            <option value="">##ChoseOption##...</option>
                                <option value="{$continent['id']}">{$continent['titleFa']}</option>
                            {/foreach}
        ''',
        '''<option value="">##ChoseOption##...</option>''',
        '''<option selected="selected" value="">نوع ویزا</option>'''
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Visa(): ' + str(e)  # Return the exception message for now


def Train(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{assign var='cities' value=$obj_main_page->trainListCity()}
                        '''
        options_array = [
        '''
                        <option value="">##ChoseOption##...</option>
                        {foreach $cities as $city}
                            <option value="{$city['Code']}">{$city['Name']}</option>
                        {/foreach}
        ''',
        '''              <option value="">##ChoseOption##...</option>
                        {foreach $cities as $city}
                            <option value="{$city['Code']}">{$city['Name']}</option>
                        {/foreach}
        ''',
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Train(): ' + str(e)  # Return the exception message for now


def Insurance(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{assign var="countries" value=$obj_main_page->countryInsurance()}
                        '''
        options_array = [
        '''
                            <option value="">##ChoseOption##...</option>
                            {foreach $countries as $country}
                                <option value="{$country['abbr']}">{$country['persian_name']}({$country['abbr']})</option>
                            {/foreach}
        ''',
        '''                            <option value="">##ChoseOption##...</option>
                            {assign var="durations" value=['5','7','8','15','23','31','45','62','92','182','186','365']}
                            {foreach $durations as $days}
                            <option value="5">##untill## {$days} ##Day##</option>
                            {/foreach}
                            ''',

        '''                  <option value="">##ChoseOption##...</option>
                            {for $i=1 to 9}
                                <option value="{$i}">{$i} ##People##</option>
                            {/for}
        '''
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Insurance(): ' + str(e)  # Return the exception message for now


def Bus(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{assign var='cities' value=$obj_main_page->getBusRoutes()}'''
        options_array = [
        '''
                            <option value="">##ChoseOption##...</option>
                            {foreach $cities as $city}
                                <option value="{$city['id']}">{$city['text']}</option>
                            {/foreach}
        ''',
        '''                            <option value="">##ChoseOption##...</option>
                            {foreach $cities as $city}
                                <option value="{$city['id']}">{$city['text']}</option>
                            {/foreach}'''
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Bus(): ' + str(e)  # Return the exception message for now


def GashtTransfer(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{assign var="cities" value=$obj_main_page->getCitiesGashtTransfer()}'''
        options_array = [
        '''
                            <option value="">##ChoseOption##...</option>
                            {foreach $cities as $city}
                                <option value="{$city['city_code']}">{$city['city_name']}</option>
                            {/foreach}
        ''',
        '''                            <option value="">انتخاب کنید...</option>
                            <option selected="selected" value="1">گشت انفرادی</option>
                            <option value="2">گشت گروهی</option>''',

        '''                            <option value="">##ChoseOption##...</option>
                            {foreach $cities as $city}
                                <option value="{$city['city_code']}">{$city['city_name']}</option>
                            {/foreach}
        ''',
        '''
                            <option selected="selected" value="1">استقبال</option>
                            <option value="2">بدرقه</option>
                            <option value="3">استقبال و بدرقه</option>
        ''',
        '''                            <option selected="selected" value="1">سواری</option>
                            <option value="2">ون</option>
                            <option value="3">مینی بوس</option>
                            <option value="4">اتوبوس</option>
                            <option value="5">شناور</option>
        ''',
        '''<option value="">##ChoseOption##...</option>''',
        '''
                            <option selected="selected" value="1">فرودگاه</option>
                            <option value="2">ترمینال</option>
                            <option value="3">راه آهن</option>
                            <option value="4">بندر</option>
        '''
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, GashtTransfer(): ' + str(e)  # Return the exception message for now


def Entertainment(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{assign var="countries" value=$obj_main_page->getCountryEntertainment()}'''
        options_array = [
        '''
                            <option value="">##ChoseOption##...</option>
                            {foreach $countries as $country}
                                <option value='{$country['id']}'>{$country['name']}</option>
                            {/foreach}
        ''',
        '''<option value="">##ChoseOption##...</option>''',
        '''<option value="">##ChoseOption##...</option>''',
        '''<option value="">##ChoseOption##...</option>''',
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Entertainment(): ' + str(e)  # Return the exception message for now


def Europcar(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''{load_presentation_object filename="mainCity" assign="objCity"}
                        {assign var="type_data" value=['is_active'=>1 , 'limit' =>30]}
                        {assign var='listTypeCar' value=$obj_main_page->getTypeCar($type_data)}'''
        options_array = [
        '''
                            <option value="">##ChoseOption##...</option>
                            {foreach $listTypeCar as $car}
                                <option value="{$car['id']}">{$car['title']}</option>
                            {/foreach}
        ''',
        '''                            {foreach $objCity->getCityAll() as $key => $city}
                                <option value="{$city['id']}">
                                    استان {$city['name']}
                                </option>
                            {/foreach}''',
        '''                            <option value="">##ChoseOption##...</option>
                            {foreach $objCity->getCityAll() as $key => $city}
                                <option value="{$city['id']}">
                                    استان {$city['name']}
                                </option>
                            {/foreach}''',
        ]
        section = BeautifulSoup(section, "html.parser")
        helper.add_class_to_elements(section, 'tab-pane','  {if $active} active {/if} ')
        select_tags = section.find_all('select')

        i = 0
        for select_tag in select_tags:
            if i <= len(options_array):
                select_tag.string = options_array[i]
                i = i + 1
        section = helper.clean_serialize_string(f'{section}')
        final_section = befor_html + f'{section}'
        return helper.create_file(f'{final_section}', item_path, box_id, 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, Europcar(): ' + str(e)  # Return the exception message for now

