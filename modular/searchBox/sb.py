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


def search_box(searchBox_section, project_path, lang = 'fa',  file_name = ''):
    try:
        tabs_section = searchBox_section.find(class_='__search_box_tabs__')
        boxes_section = searchBox_section.find(class_='__search_boxes__')
        has_tpl_services = {'Tour': Tour,
                            'Visa': Visa,'Train': Train,'Insurance': Insurance,'Bus': Bus,'GashtTransfer': GashtTransfer,'Entertainment': Entertainment,'Europcar': Europcar
                            }

        # getting the tabs and put them in array adn tab.tpl file in searchbox directory
        hrefs_list = []
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
                    item = item.replace('_internal', '').replace('_external', '')
                    item_path = helper.create_folder(item, sections_path)



            testt = modulationSearchBoxTabs(project_path + '/include_files/search-box', parent_li)
            modulationSearchBoxBoxes(project_path + '/include_files/search-box')

        # getting the ids of boxes and add them to href array. and put them in searchbox dierctory
        id_lists = hrefs_list
        boxs = boxes_section.find_all(class_='__box__')
        items_massages = []
        for b in boxs:
            box_id = b.get('id')
            modified_id = box_id.replace('_internal', '').replace('_external', '')
            if box_id:
                if box_id not in hrefs_list:
                    item_path = helper.create_folder(box_id, sections_path)
                    id_lists.append(box_id)
                if modified_id in has_tpl_services:
                    item_massage = has_tpl_services[modified_id](f'{b}' ,boxes_path, modified_id, box_id)
                    items_massages.append(item_massage + '<br><br>')
                else:
                    helper.if_dosnt_exist_create_else_add(boxes_path, modified_id, f'{b}')
                    item_massage = box_id + ' box has been successfully modulation'
                    items_massages.append(item_massage + '<br><br>')

        # creating relational services array
        services_array = {}
        for item in id_lists:
            modified_item = item.replace('_internal', '').replace('_external', '')
            if item in services_array:
                return f'{services_array}'
                services_array[item].append(modified_item)
            else:
                services_array[item] = modified_item


        return [f'{items_massages}', services_array]
    except Exception as e:
        return 'search_box()' + str(e)  # Return the exception message for now


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
        return 'searchBox/sb.py, Tour(): ' + str(e)  # Return the exception message for now


def Visa(section=False, item_path=False, box_id=False, type=False):
    try:

        befor_html = '''
                        {assign var="continents" value=$obj_main_page->getListContinents()}
                    '''
        options_array = [
        '''
                            {foreach $continents as $continent}
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


def modulationSearchBoxTabs(search_box_path, tab):
    try:
        tab = BeautifulSoup(tab, 'html.parser')

        content = '''
                    <ul class="nav" id="searchBoxTabs">
                        {foreach $info_access_client_to_service as $key=>$client}
                            {if  $smarty.const.GDS_SWITCH eq 'mainPage'}
                    
                                {if ($smarty.const.SOFTWARE_LANG eq 'fa') || $client['MainService'] neq 'Train' && $client['MainService'] neq 'Bus' &&
                                $client['MainService'] neq 'Europcar' && $client['MainService'] neq 'GashtTransfer' && $client['MainService'] neq 'Package'}
                                    <li class="nav-item">
                                        <a onclick="changeText(`{$obj_main_page->nameBoxSearchBox($client['MainService'])}` , 'null')" class="nav-link
                                            {if $client['MainService'] eq 'Flight' }active{/if}"
                                             id="{$client['MainService']}-tab" data-toggle="tab" href="#{$client['MainService']}">
                                            __put__tab__here__
                                        </a>
                                    </li>
                                {/if}
                            {else}
                                {if $active_tab eq 'internalFlight' && $client['MainService'] eq 'Flight' || $active_tab eq $client['MainService']}
                                    <li class="nav-item">
                                        <a onclick="changeText(`{$obj_main_page->nameBoxSearchBox($client['MainService'])}` , 'null')" class="nav-link active"
                                           id="{$client['MainService']}-tab" data-toggle="tab" href="#{$client['MainService']}">
                                            __put__tab__here__
                                        </a>
                                    </li>
                                {/if}
                            {/if}
                        {/foreach}
                    </ul>
        '''
        tab = helper.remove_tag_from_soup_object(tab, 'li')
        tab = helper.remove_tag_from_soup_object(tab, 'a')
        helper.replace_attribute_by_tag(tab, 'h4', 'string','''{$obj_main_page->nameTabsSearchBox($client['MainService'])}''')
        check_svg =  tab.find_all('svg')
        check_i =  tab.find_all('i')
        if check_svg:
            helper.replace_attribute_by_tag(tab, 'i', 'string','''{$obj_main_page->classTabsSearchBox($client['MainService'])}''')
        elif check_i:
            helper.replace_attribute_by_tag(tab, 'i', 'class','''{$obj_main_page->classTabsSearchBox($client['MainService'])}''')

        content = content.replace("__put__tab__here__", f'{tab}')

        return helper.create_file(f'{content}', search_box_path, 'tabs-search-box', 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, modulationSearchBoxTabs(): ' + str(e)  # Return the exception message for no


def modulationSearchBoxBoxes(search_box_path):
    try:
        content = '''{assign var="obj_main_page" value=$obj_main_page }
                        <div class="tab-content" id="searchBoxContent">
                            {foreach $info_access_client_to_service as $key=>$client}
                                {if  $smarty.const.GDS_SWITCH eq 'mainPage'}
                                    {include file="./boxes/{$client['MainService']}.tpl" client=$client}
                                {else}
                                    {if $active_tab eq 'internalFlight' && $client['MainService'] eq 'Flight' || $active_tab eq $client['MainService']}
                                        {include file="./boxes/{$client['MainService']}.tpl" client=$client}
                                    {/if}
                                {/if}
                            {/foreach}
                        </div>
                        '''
        return helper.create_file(f'{content}', search_box_path, 'tabs-search-box', 'tpl')
    except Exception as e:
        return 'searchBox/sb.py, modulationSearchBoxBoxes(): ' + str(e)  # Return the exception message for no