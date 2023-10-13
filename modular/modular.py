from flask import Flask, jsonify, request, send_file, jsonify
from bs4 import BeautifulSoup
import os
import shutil
import re
import requests
import json
import codecs
from modular import helper_functions as helper


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

    # blog module
    blog_section = soup.find(class_="i_modular_blog")
    if blog_section:
        blog_module_massage = blog_module(blog_section,project_path)
        # soup = BeautifulSoup(html_content, 'html.parser')
        # blog_section = soup.find(class_="i_modular_blog")
        # intial_blog_test_massage = initial_blog_test(blog_section)

    # tour module

    return jsonify({"message":  " building blog section result =" + blog_module_massage + "- - - - <br><br>- - - - blog test result =" })


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

        before_html = '''{assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>i_modular__max_limit0]}
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
                for tag in blog_section.find_all():
                    if tag.decode() == simple_element.decode():
                        new_tag = BeautifulSoup(f'{before_foreach}\n{simple_element}\n{after_foreach}')
                        simple_element.replace_with(new_tag)
                simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
                simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)
                simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
                for tag in simple_element.find_all():
                    if "__image__" in tag.get('class', []):
                        # Replace the src attribute for tags with class __image__
                        tag['src'] = '{$article["image"]}'  # Replace with desired code
                    if "__title__" in tag.get('class', []):
                        # Replace the text content for tags with class __title__
                        tag.string = '{$article["title"]}'  # Replace with desired code
                helper.replace_attribute(simple_element, '__image__', 'src','{$article["image"]}')
                helper.replace_attribute(simple_element, '__title__', 'string','{$article["title"]}')

            else:
                simple_element.decompose()
        for num in complex_items_numbers:
            blog_complex_replacement_data = {
                "__link__": '''{{$articles[{0}]['link']}}'''.format(num),
                "__alt_article__": '''{{$articles[{0}]['title']}}'''.format(num),
                'images/5497750661271-6.jpg': '''{{$articles[{0}]['image']}}'''.format(num),
                '<span class="__date__">5 بهمن 1402</span>': '''{{$articles[{0}]['created_at']}}'''.format(num),
                '<span class="__comments_number__">450</span>': '''{{$articles[{0}]['comments_count']['comments_count']}}'''.format(num)
            }
            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)
            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            helper.replace_attribute(complex_element, '__image__', 'src', '''{{$articles[{0}]['image']}}'''.format(num))
            helper.replace_attribute(complex_element, '__title__', 'string', '''{{$articles[{0}]['title']}}'''.format(num))




        blog_final_content = f'{before_html}\n{blog_section}\n{after_html}'
        include_files_directory = os.path.join(project_path, 'include_files')  # Create a 'files' subdirectory
        helper.write_text_in_path(project_path, "{inclued 'include_files/blog.tpl'}")
        blog_final_content = blog_final_content.replace("&gt;", ">")
        blog_final_content = blog_final_content.replace("&lt;", "<")

        return helper.create_file(blog_final_content, include_files_directory, 'blog', 'tpl')
    except Exception as e:
        return str(e)  # Return the exception message for now


def initial_blog_test(blog_section):
    # Replace the URL with your local machine's URL
    url = "http://192.168.1.100/"

    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            html_content = response.text

            # Check if "i_modular_blog" is present in the HTML content
            if "i_modular_blog" in html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                blog_section_online = soup.find(class_="i_modular_blog")
                blog_unit_test_massage = blog_unit_test(blog_section, blog_section_online)
                return blog_unit_test_massage
            else:
                return "ماژول وبلاگ موجود نیست."



        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def blog_unit_test(blog_section, blog_section_online):
    try:
        script_directory = os.path.dirname(__file__)  # Get the directory of the script
        unit_test_files_directory = os.path.join(script_directory, 'unit_test_fles')
        json_file_path = os.path.join(unit_test_files_directory, 'blog_test_data.json')

        # Initialize an empty list to store the data
        blog_data = []
        json_string = codecs.open(json_file_path, 'r', encoding='utf-8').read()

        blog_data = json.loads(json_string)

        # for item in blog_data:
        #     testt = (item["title"])

        complex_items_pattern = re.compile(r'__i_modular_c_item_(\d+)')
        simple_items_pattern = re.compile(r'__i_modular_nc_item_(\d+)')
        complex_items_numbers = []
        simple_items_numbers = []

        elements = blog_section.find_all(class_=complex_items_pattern)
        for element in elements:
            match = complex_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                complex_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")
        elements = blog_section.find_all(class_=simple_items_pattern)
        for element in elements:
            match = simple_items_pattern.search(element.get('class')[0])
            if match:
                number = match.group(1)
                simple_items_numbers.append(number)
            else:
                raise ValueError(f"No number found in class attribute: {element.get('class')[0]}")


        for num in simple_items_numbers:
            blog_replacement_data = {
                "__i_modular_nc_item_" + num: "__i_modular_nc_item_" + simple_items_numbers[0],
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__title__": blog_data[int(num)]['title'],
                "__alt_article__": blog_data[int(num)]['title'],
                '<span class="__date__">5 بهمن 1402</span>': blog_data[int(num)]['created_at'],
                '<span class="__comments_number__">450</span>': blog_data[int(num)]['comments_count']['comments_count'],
                'images/5497750661271-6.jpg': blog_data[int(num)]['image'],
                '<span class="__title__">تایتل</span>': blog_data[int(num)]['title']
            }
            simple_element = blog_section.find(class_="__i_modular_nc_item_" + num)
            simple_element = helper.replace_placeholders(simple_element, blog_replacement_data)



        for num in complex_items_numbers:
            blog_complex_replacement_data = {
                "__airline__": blog_data[int(num)]['link'],
                "__link__": blog_data[int(num)]['link'],
                "__image__": blog_data[int(num)]['image'],
                "__title__": blog_data[int(num)]['title'],
                "__alt_article__": blog_data[int(num)]['title'],
                '<span class="__date__">5 بهمن 1402</span>': blog_data[int(num)]['created_at'],
                '<span class="__comments_number__">450</span>': blog_data[int(num)]['comments_count']['comments_count'],
                'images/5497750661271-6.jpg': blog_data[int(num)]['image'],
                'images/images/article1.jpg': blog_data[int(num)]['image'],
                '<span class="__title__">تایتل</span>': blog_data[int(num)]['title'],
                '<h2>جاهای دیدنی مازندران</h2>': '<h2>' +blog_data[int(num)]['title'] + '</h2>',
                '<h2>جاهای دیدنی چالوس</h2>': '<h2>' +blog_data[int(num)]['title'] + '</h2>',
                '<h2>جاهای دیدنی چابکسر</h2>': '<h2>' +blog_data[int(num)]['title'] + '</h2>',
                '<h2>بهترین جاهای دیدنی دبی</h2>': '<h2>' +blog_data[int(num)]['title'] + '</h2>',
                '<h2>جاهای دیدنی اسپانیا</h2>': '<h2>' +blog_data[int(num)]['title'] + '</h2>',
                '<p>در میان تنوع آب‌وهوایی موجود در ایران، این خطه سرسبز شمال است که همیشه اولین مقصد برای سفرهای گاه‌و‌بی‌گاه ما محسوب می‌شود. در این میان، چالوس را باید با شگفتی‌های بی‌نظیری که دارد، بهشت گمشده ایران دانست. جاهای دیدنی چالوس از طبیعت بکر تا آبشارهای حیرت‌انگیز آن، همگی مسافران خوش‌ذوق را به سمت خود فرامی‌خوانند. ما در این مطلب از مجله گردشگری فلای‌ تودی، قصد داریم نگاهی تخصصی به جاهای دیدنی چالوس داشته باشیم تا راز محبوبیت این شهر شمالی را بیشتر دریابیم. به شما نیز برای داشتن سفری رویایی، پیشنهاد می‌کنیم تا پایان این مطلب همراه ما باشید.</p>': '<p>' + blog_data[int(num)]['description'] + '</p>',
                '<p>همه شما از زیبایی‌های شهرهای شمالی ایران باخبر هستید. این مطلب را هم به معرفی جاهای دیدنی یکی از همین شهرها، یعنی شهر زیبای چابکسر، اختصاص داده‌ایم. با خواندن این مطلب، قطعا نمی‌توانید از بازدید از جاهای دیدنی چابکسر صرف‌نظر کنید. دلیل معروف‌بودن چابکسر، این جواهر در مرز استان‌های گیلان و مازندران، فاصله کم میان کوهستان‌های جنگلی سرسبز و دریای زیبای خزر است. مسیرهای میان شهرهای شمالی، طولانی نیستند و این مسئله، شما را برای گردش در میان زیبایی‌های شگفت‌انگیز طبیعت تشویق خواهد کرد. جاذبه‌ های گردشگری چابکسر از طبیعت مسحورکننده گرفته تا سایر مکان‌های دیدنی و تفریحی، این شهر را به یکی از بهترین مقاصد گردشگری کشور تبدیل کرده‌اند. برای آشنایی با جاهای دیدنی چابکسر در این مطلب از مجله گردشگری فلای تودی، با ما همراه باشید.   </p>': '<p>' + blog_data[int(num)]['description'] + '</p>',
                '<p>جاذبه های گردشگری دبی را می‌شناسید؟ حتما بعد از دیدن این سوال خیلی زود به یاد آسمانخراش‌های دبی افتاده‌اید. اما به جز برج های سر از آسمان برآورده، دبی جاهای دیدنی دیگری نیز دارد که شاید خیلی از گردشگران از وجود آنها خبر هم نداشته باشند. در این مطلب از مجله گردشگری فلای تودی با مکان های دیدنی دبی آشنا شوید.</p>': '<p>' + blog_data[int(num)]['description'] + '</p>',
                '<p>اگر قطب گردشگری در اروپا را جاهای دیدنی اسپانیا بدانیم، بیراه نگفته‌ایم؛ کشوری زنده و پرانرژی که گوشه‌گوشه آن، زندگی را به‌ معنای واقعی کلمه به‌ تصویر می‌کشد. عظمت قصر خلیفه، شادی یک روز آفتابی در سواحل مدیترانه و سکوت حیرت‌انگیز زائران در کلیسای سانتیاگو، همگی از تجربه‌های نابی است که از سفر به اسپانیا به‌ دست می‌آیند. اسپانیا پر است از جاذبه‌های گردشگری که هر کدام از آن‌ها، حکایت‌هایی شیرین از تاریخ غنی، فرهنگ جذاب و طبیعت مسحورکننده این کشور را روایت می‌کنند. اگر به این کشور رویایی سفر کردید، بدانید با برنامه‌ای شلوغ، نفس‌گیر اما هیجان‌انگیز مواجه خواهید شد. ما نیز در این مطلب از مجله گردشگری فلای‌ تودی با معرفی بهترین جاهای دیدنی اسپانیا، چاشنی شور و هیجان سفرتان را بیشتر می‌کنیم.</p>': '<p>' + blog_data[int(num)]['description'] + '</p>',
                '<p>بدون شک، یکی از بهترین مقاصد سفر برای ما ایرانی‌ها، مناطق شمالی ایران است. در این میان، جاهای دیدنی مازندران چهره‌ای دیگر از زیبایی‌های این منطقه دوست‌داشتنی را به تصویر می‌کشند. حدس می‌زنیم شهرت محبوبیت مازندران از لحاظ دارا بودن جاذبه‌های گردشگری به گوش شما هم رسیده باشد. در عین‌ حال، اگر زیبایی‌های طبیعت بکر و تماشایی این استان زیبا را از نزدیک لمس نکرده‌اید، با ما در این مطلب از مجله گردشگری فلای‌ تودی، همراه شوید تا با معرفی بهترین جاهای دیدنی مازندران در فصول مختلف سال، اسباب سفری خوش و خاطره‌انگیز را برای شما در آینده فراهم کنیم. آماده سفر به بهترین قطب گردشگری شمال ایران هستید؟</p>': '<p>' + blog_data[int(num)]['description'] + '</p>',
            }

            complex_element = blog_section.find(class_="__i_modular_c_item_" + num)
            complex_element_final = helper.replace_placeholders(complex_element, blog_complex_replacement_data)

        blog_section_online = blog_section_online.prettify()
        # blog_section = blog_section.prettify()

        blog_section = f'{blog_section}'
        for num in simple_items_numbers:
            blog_section = blog_section.replace("__i_modular_nc_item_" + num, "__i_modular_nc_item_" + simple_items_numbers[0])

        for num in complex_items_numbers:
            blog_section = blog_section.replace("__i_modular_c_item_" + num, "__i_modular_c_item_" + complex_items_numbers[0])

        blog_section_online = blog_section_online.replace("</img>", "")
        blog_section = blog_section.replace("/>", ">")

        html_code_1 = re.sub(r'\s+', '', blog_section_online)
        html_code_2 = re.sub(r'\s+', '', blog_section)

        # Compare the two HTML code strings.
        if html_code_1 == html_code_2:
            return "تست سکشن بلاگ موفقیت آمیز بود."

        return blog_section_online + '   ' + blog_section
        return 'طرح و سکشن بلاگ ماژول گذاری شده هماهنگ نیستند.'
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"




