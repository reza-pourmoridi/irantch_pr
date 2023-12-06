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
        has_tpl_services = {'Tour': Tour,'Visa': Visa,'Train': Train,'Insurance': Insurance,'Bus': Bus,'GashtTransfer': GashtTransfer,'Entertainment': Entertainment}

        # getting the tabs and put them in array adn tab.tpl file in searchbox directory
        hrefs_list = []
        if tabs_section:
            all_a_tags = tabs_section.find_all('a')
            for a in all_a_tags:
                if a.get('href'):
                    item = a.get('href').lstrip('#')
                    parent_li = a.find_parent('li')
                    item_path = helper.create_folder(item, project_path + '/include_files/search-box')
                    if parent_li:
                        tab_page = helper.create_file(f'{parent_li}', item_path, 'tab', 'tpl')
                    hrefs_list.append(item)

        # getting the ids of boxes and add them to href array. and put them in searchbox dierctory
        id_lists = hrefs_list
        boxs = boxes_section.find_all(class_='__box__')
        for b in boxs:
            box_id = b.get('id')
            if box_id:
                if box_id not in hrefs_list:
                    item_path = helper.create_folder(box_id, project_path + '/include_files/search-box')
                    id_lists.append(box_id)
                else:
                    item_path = project_path + '/include_files/search-box/' + box_id

                tab_page = helper.create_file(f'{b}', item_path, 'box', 'tpl')

        # creating relational services array
        services_array = {}
        for item in id_lists:
            modified_item = item.replace('_internal', '').replace('_external', '')
            if item in services_array:
                services_array[item].append(modified_item)
            else:
                services_array[item] = modified_item

        items_massages = []
        for key, val in services_array.items():
            if val in has_tpl_services:
               item_massage = has_tpl_services[val](key)
               items_massages.append(item_massage + '<br><br>')
            else:
                item_massage = key + ' box has been successfully modulation'
                items_massages.append(item_massage + '<br><br>')

        return [f'{items_massages}', services_array]
    except Exception as e:
        return str(e)  # Return the exception message for now


def Tour(id = False):
    if id:

        return id

def Visa(id = False):
    if id:
        return id

def Train(id = False):
    if id:
        return id

def Insurance(id = False):
    if id:
        return id

def Bus(id = False):
    if id:
        return id

def GashtTransfer(id = False):
    if id:
        return id

def Entertainment(id = False):
    if id:
        return id