{assign var="main_articles" value=$obj_main_page->getNewsArticles()}
                            {assign var="othe_itmes" value=$main_articles['data']}
                            {assign var="i" value="2"}
                            {assign var='counter' value=0}
                            {if $main_articles['count'] > 0 }
<section class="i_modular_news news my-5 py-5">
<div class="container">
<h2 class="news_title">آخرین اخبار و رویدادها</h2>
<div class="news-grid">
<div class="div1">
<h2>آخرین اخبار و رویدادها</h2>
<p class="mt-auto">
                        به روزترین و جذاب‌ترین اخبار از دنیای موارد مختلف در وب سایت ما!
                    </p>
<p>
                        به عنوان یک منبع اطلاعاتی جامع، با تیم ما در اینجا همراه شوید تا از آخرین اخبار و رویدادهای جذاب جهان مطلع شوید. از آخرین پیشرفت‌های علمی و تکنولوژی تا بهترین روش‌ها برای بهبود سلامتی، از جدیدترین موضوعات محیط‌زیستی تا هنر و فرهنگ هر کشور... همه چیز در اینجا وجود دارد!
                    </p>
</div>
{if $othe_itmes[0] }
<div class="__i_modular_c_item_class_0 div2">
<a href="{$othe_itmes[0]['link']}">
<img alt="{$othe_itmes[0]['alt']}" class="__image_class__" src="{$othe_itmes[0]['image']}"/>
<div>
<div>
<h4 class="__heading_class__">{$othe_itmes[0]['heading']}</h4>
<span>بیشتر بدانید
                                <svg viewbox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M447.1 256c0 13.25-10.76 24.01-24.01 24.01H83.9l132.7 126.6c9.625 9.156 9.969 24.41 .8125 33.94c-9.156 9.594-24.34 9.938-33.94 .8125l-176-168C2.695 268.9 .0078 262.6 .0078 256S2.695 243.2 7.445 238.6l176-168C193 61.51 208.2 61.85 217.4 71.45c9.156 9.5 8.812 24.75-.8125 33.94l-132.7 126.6h340.1C437.2 232 447.1 242.8 447.1 256z"></path></svg>
</span>
</div>
</div>
</a>
</div>
{/if}
{if $othe_itmes[1] }
<div class="__i_modular_c_item_class_1 div3">
<a class="news_box" href="{$othe_itmes[1]['link']}">
<div class="news_box_img">
<img alt="{$othe_itmes[1]['alt']}" class="__image_class__" src="{$othe_itmes[1]['image']}"/>
</div>
<div class="news_box_text">
<h4 class="__heading_class__">{$othe_itmes[1]['heading']}</h4>
<p class="__description__">همایش بیمارستان‌ها و مراکز درمانی با محوریت گردشگری سلامت با حضور نمایندگانی از ۳۰ کشور اسلامی و مدیران مراکز درمانی ایران و نمایندگان مجلس و وزیر میراث فرهنگی گردشگری و صنایع‌دستی، به مدت ۳ روز از ۲۵ تا ۲۷ تیرماه در سالن همایش‌های صدا و سیما برگزار می شود.</p>
<span>بیشتر بدانید
                            <svg viewbox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M447.1 256c0 13.25-10.76 24.01-24.01 24.01H83.9l132.7 126.6c9.625 9.156 9.969 24.41 .8125 33.94c-9.156 9.594-24.34 9.938-33.94 .8125l-176-168C2.695 268.9 .0078 262.6 .0078 256S2.695 243.2 7.445 238.6l176-168C193 61.51 208.2 61.85 217.4 71.45c9.156 9.5 8.812 24.75-.8125 33.94l-132.7 126.6h340.1C437.2 232 447.1 242.8 447.1 256z"></path></svg>
</span>
</div>
</a>
</div>
{/if}
{if $othe_itmes[2] }
<div class="__i_modular_c_item_class_2 div4">
<a class="news_box" href="{$othe_itmes[2]['link']}">
<div class="news_box_img">
<img alt="{$othe_itmes[2]['alt']}" class="__image_class__" src="{$othe_itmes[2]['image']}"/>
</div>
<div class="news_box_text">
<h4 class="__heading_class__">{$othe_itmes[2]['heading']}</h4>
<p class="__description__">یکی از شرکت‌های معروف و معتبر در صنعت ریلی کشور، شرکت ریل سیر کوثر است که با افزایش کیفیت خدمات و امکانات و با ارائه قطارهای متنوع در کلاس‌های مختلف، توانسته باعث رشد ناوگان حمل‌و‌نقل ریلی کشور شود. این شرکت ۱۰۰درصد به‌شکل خصوصی اداره می‌شود و با همکاری شرکت‌ واگن‌ پارس، به تازگی از قطار پنج ستاره خود پرده‌برداری کرده است. قطاری که امکانات آن دست‌ کمی از پروازهای بیزینس کلاس ندارد و با فراهم کردن آسایش مسافران، شکل جدیدی از خدمات رسانی در شبکه ریلی کشور را نشان می‌دهد.</p>
<span>بیشتر بدانید
                            <svg viewbox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M447.1 256c0 13.25-10.76 24.01-24.01 24.01H83.9l132.7 126.6c9.625 9.156 9.969 24.41 .8125 33.94c-9.156 9.594-24.34 9.938-33.94 .8125l-176-168C2.695 268.9 .0078 262.6 .0078 256S2.695 243.2 7.445 238.6l176-168C193 61.51 208.2 61.85 217.4 71.45c9.156 9.5 8.812 24.75-.8125 33.94l-132.7 126.6h340.1C437.2 232 447.1 242.8 447.1 256z"></path></svg>
</span>
</div>
</a>
</div>
{/if}
{if $othe_itmes[3] }
<div class="__i_modular_c_item_class_3 div5">
<a class="news_box" href="{$othe_itmes[3]['link']}">
<div class="news_box_img">
<img alt="{$othe_itmes[3]['alt']}" class="__image_class__" src="{$othe_itmes[3]['image']}"/>
</div>
<div class="news_box_text">
<h4 class="__heading_class__">{$othe_itmes[3]['heading']}</h4>
<p class="__description__">به نقل از خبرگزاری فرارو، در روزهای ۶ تا ۱۴ تیرماه برای نمایندگان صنعت گردشگری ایران، سفری با هدف آشنایی با مقاصد توریستی کشور روسیه برگزار شد. در این سفر که از طرف کمیته گردشگری شهر مسکو با همکاری کمیته دولتی گردشگری جمهوری تاتارستان برنامه‌ریزی شده بود، گفت‌وگوهای تجاری بین نمایندگان ایران، کازان و مسکو انجام شد و نمایندگان شهرهای مختلف گزارشی از زیرساخت‌ها و ظرفیت‌های توریستی خود برای گردشگران ایرانی، ارائه دادند. نمایندگان مسکو درباره نظیر جشن‌‌ها و فستیوال‌های فصلی، گردشگری غذایی و سرآشپزهای مشهور، پارک‌های متعدد،‌ تفریحات مختلف و سفرهای رودخانه‌ای و… صحبت کردند.</p>
<span>بیشتر بدانید
                            <svg viewbox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M447.1 256c0 13.25-10.76 24.01-24.01 24.01H83.9l132.7 126.6c9.625 9.156 9.969 24.41 .8125 33.94c-9.156 9.594-24.34 9.938-33.94 .8125l-176-168C2.695 268.9 .0078 262.6 .0078 256S2.695 243.2 7.445 238.6l176-168C193 61.51 208.2 61.85 217.4 71.45c9.156 9.5 8.812 24.75-.8125 33.94l-132.7 126.6h340.1C437.2 232 447.1 242.8 447.1 256z"></path></svg>
</span>
</div>
</a>
</div>
{/if}
</div>
</div>
</section>
{/if}