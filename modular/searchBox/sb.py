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

    searchBox_path = helper.create_folder('search-box' , project_path + '/include_files')
    tabs_section = searchBox_section.find(class_='__search_box_tabs__')
    boxes_section = searchBox_section.find(class_='__search_boxes__')

    hrefs_list = []
    if tabs_section:
        all_a_tags = tabs_section.find_all('a')
        for a in all_a_tags:
            if a.get('href'):
                item = a.get('href').lstrip('#')
                
                parent_li = a.find_parent('li')

                return f'{parent_li}'
                item_path = helper.create_folder(item, project_path + '/include_files/search-box')
                hrefs_list.append(item)

    # main_page = helper.create_file(soup_str, project_path, 'mainPage', 'tpl')


    return f'{hrefs_list}'
