{include file="include_files/header.tpl" }
{include file="include_files/menu.tpl"}

<main>

    {assign var="type_data" value=['is_active'=>1 , 'limit' =>5]}
    {assign var='banners' value=$obj_main_page->galleryBannerMain($type_data)}


    <section class="banner">
        <div class="OWL_slider_banner owl-carousel owl-theme">
            {foreach $banners as $key => $banner}
                <div class="item">
                    <img class='search_box' src="{$banner['pic']}" alt="{$banner['title']}">
                </div>
            {/foreach}
        </div>
        <div class="context_banner">
            <div class="textBox_banner">
                <div class="container">
                    <span>آوا پرواز ایرانیان</span>
                    <h2>بلیط هواپیمای داخلی و خارجی</h2>
                </div>
            </div>
            <div class="searchBox_banner">
                <div class="container">
                    <div class="searchs_box">
                        <ul style="display: none" class="nav nav-tabs" id="myTab" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active"
                                   id="flight-internal-tab"
                                   data-toggle="tab"
                                   href="#flight-internal"
                                   role="tab"
                                   aria-controls="flight-internal"
                                   aria-selected="true">
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M576 256C576 305 502.1 336 464.2 336H382.2L282.4 496C276.4 506 266.4 512 254.4 512H189.5C179.5 512 169.5 508 163.5 500C157.6 492 155.6 480.1 158.6 471L201.5 336H152.5L113.6 388C107.6 396 98.61 400 88.62 400H31.7C22.72 400 12.73 396 6.74 388C.7485 380-1.248 370 1.747 360L31.7 256L.7488 152C-1.248 143 .7488 133 6.74 125C12.73 117 22.72 112 31.7 112H88.62C98.61 112 107.6 117 113.6 125L152.5 176H201.5L158.6 41C155.6 32 157.6 21 163.5 13C169.5 5 179.5 0 189.5 0H254.4C265.4 0 277.4 7 281.4 16L381.2 176H463.2C502.1 176 576 208 576 256H576zM527.1 256C525.1 246 489.1 224 463.2 224H355.3L245.4 48H211.5L266.4 224H128.6L80.63 160H53.67L81.63 256L53.67 352H80.63L128.6 288H266.4L211.5 464H245.4L355.3 288H463.2C490.1 288 526.1 267 527.1 256V256z"/></svg>
                                        <h4>پرواز داخلی</h4>
                                    </div>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link"
                                   id="flight-international-tab"
                                   data-toggle="tab"
                                   href="#flight-international"
                                   role="tab"
                                   aria-controls="flight-international"
                                   aria-selected="false">
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M576 256C576 305 502.1 336 464.2 336H382.2L282.4 496C276.4 506 266.4 512 254.4 512H189.5C179.5 512 169.5 508 163.5 500C157.6 492 155.6 480.1 158.6 471L201.5 336H152.5L113.6 388C107.6 396 98.61 400 88.62 400H31.7C22.72 400 12.73 396 6.74 388C.7485 380-1.248 370 1.747 360L31.7 256L.7488 152C-1.248 143 .7488 133 6.74 125C12.73 117 22.72 112 31.7 112H88.62C98.61 112 107.6 117 113.6 125L152.5 176H201.5L158.6 41C155.6 32 157.6 21 163.5 13C169.5 5 179.5 0 189.5 0H254.4C265.4 0 277.4 7 281.4 16L381.2 176H463.2C502.1 176 576 208 576 256H576zM527.1 256C525.1 246 489.1 224 463.2 224H355.3L245.4 48H211.5L266.4 224H128.6L80.63 160H53.67L81.63 256L53.67 352H80.63L128.6 288H266.4L211.5 464H245.4L355.3 288H463.2C490.1 288 526.1 267 527.1 256V256z"/></svg>
                                        <h4>پرواز خارجی</h4>
                                    </div>
                                </a>
                            </li>
                        </ul>
                        <div class="tab-content" id="myTabContent">
                            <div class="tab-pane active show"
                                 id="flight-international"
                                 role="tabpanel"
                                 aria-labelledby="flight-international-tab">
                                <div>
                                    <form method="post"
                                          target="_blank" class="d_contents"
                                          id="gds_portal"
                                          name="gds_portal">
                                        <div class="col-md-12 col-xs-12 col-sm-12 d-ceckboxs">
                                            <div class="cntr">
                                                <label for="rdo-3" class="btn-radio">
                                                    <input checked="" class="multiselectportal" type="radio" id="rdo-3" name="select-rb" value="1">
                                                    <span>یک طرفه </span>
                                                </label>
                                                <label for="rdo-4" class="btn-radio">
                                                    <input type="radio" class="multiselectportal" id="rdo-4" name="select-rb" value="2">
                                                    <span>دو طرفه </span>
                                                </label>
                                            </div>
                                        </div>
                                        <div class="col-lg-2 col-md-6 col-sm-12 col-12 col_search search_col col_with_route">
                                            <div class="form-group origin_start"><input type="text"
                                                                                        name="OriginPortal"
                                                                                        id="OriginPortal"
                                                                                        class="form-control  inputSearchForeign"
                                                                                        placeholder="مبدأ ( نام شهر یا فرودگاه )"><img
                                                        src="project_files/images/loader.gif" class="loaderSearch" id="loaderSearch"
                                                        name="loaderSearch" style="display: none" alt="loader"><input
                                                        id="OriginAirportPortal" class="" type="hidden" value=""
                                                        name="OriginAirportPortal">
                                                <div id="ListAirPort" class="resultUlInputSearch"
                                                     style="display: none"></div>
                                                <div class="ListAirPort" id="ListAirPort_2">
                                                    <div class="first">
                                                        <h4 class="m-0"><span class="c-text"><div
                                                                        class="c-text2"></div><div
                                                                        class="yata_gdemo"><i></i><em></em></div></span>
                                                        </h4>
                                                    </div>
                                                </div>
                                            </div>
                                            <button onclick="reversDestination('internationalFlights')"
                                                    class="switch_routs" type="button" name="button">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                                    <path d="M488 344H79.24l74.29-79.63C162.6 254.7 162.1 239.5 152.4 230.5C142.7 221.4 127.5 221.9 118.5 231.6l-112 120c-8.625 9.219-8.625 23.53 0 32.75l112 120C123.2 509.4 129.6 512 136 512c5.875 0 11.75-2.125 16.38-6.469c9.688-9.031 10.22-24.22 1.156-33.91L79.24 392H488c13.25 0 24-10.75 24-24S501.3 344 488 344zM24 168h408.8l-74.29 79.63c-9.062 9.688-8.531 24.88 1.156 33.91c9.656 9.094 24.88 8.562 33.91-1.156l112-120c8.625-9.219 8.625-23.53 0-32.75l-112-120C388.8 2.562 382.4 0 376 0c-5.875 0-11.75 2.125-16.38 6.469c-9.688 9.031-10.22 24.22-1.156 33.91L432.8 120H24C10.75 120 0 130.8 0 144S10.75 168 24 168z"/>
                                                </svg>
                                            </button>
                                        </div>
                                        <div class="col-lg-2 col-md-6 col-sm-12 col-12 col_search search_col">
                                            <div class="form-group"><span class="destnition_start"><input
                                                            type="text" id="DestinationPortal" name="DestinationPortal"
                                                            class="inputSearchForeign form-control "
                                                            placeholder="مقصد ( نام شهر یا فرودگاه )"></span><input
                                                        id="DestinationAirportPortal" class="" type="hidden" value=""
                                                        name="DestinationAirportPortal">
                                                <div id="ListAirPortDestination" class="resultUlInputSearch"
                                                     style="display: none"></div>
                                                <div class="ListAirPort" id="ListAirPortDestination_2">
                                                    <div class="first">
                                                        <h4 class="m-0"><span class="c-text"><div
                                                                        class="c-text2"></div><div
                                                                        class="yata_gdemo"><i></i><em></em></div></span>
                                                        </h4>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-lg-4 col-md-12 col-sm-12 col-12 col_search date_search">
                                            <div class="form-group"><input readonly type="text"
                                                                           class=" deptCalendar form-control went "
                                                                           name="gds_dept_date_portal"
                                                                           id="gds_dept_date_Portal"
                                                                           placeholder="تاریخ رفت"></div>
                                            <div class="form-group"><input readonly disabled type="text"
                                                                           name="regds_dept_date_Portal"
                                                                           id="regds_dept_date_Portal"
                                                                           class="form-control return_input2 checktest1 returnCalendar"
                                                                           placeholder="تاریخ برگشت"></div>
                                        </div>
                                        <div class="col-lg-2 col-md-6 col-sm-12 col-12 col_search">
                                            <div class="select inp-s-num adt box-of-count-nafar"><input
                                                        type="hidden" class="l-bozorgsal-2" name="gds_infants_no_portal"
                                                        id="qtyadt" value="1"><input type="hidden" class="l-kodak-2"
                                                                                     name="gds_childs_no_portal"
                                                                                     id="qtychd"><input type="hidden"
                                                                                                        class="l-nozad-2"
                                                                                                        name="gds_infants_no_portal"
                                                                                                        id="qtyinf">
                                                <div class="box-of-count-nafar-boxes"><span
                                                            class="text-count-nafar">1 مسافر</span><span
                                                            class="fas fa-caret-down down-count-nafar"></span></div>
                                                <div class="cbox-count-nafar">
                                                    <div class="col-xs-12 cbox-count-nafar-ch bozorg-num">
                                                        <div class="row">
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="type-of-count-nafar"><h6> بزرگسال </h6>
                                                                    (بزرگتر از ۱۲ سال)
                                                                </div>
                                                            </div>
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="num-of-count-nafar"><i
                                                                            class="counting-of-count-nafar plus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280h-160v160c0 13.25-10.75 24.01-24 24.01S200 453.3 200 440v-160h-160c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h160v-160c0-13.25 10.75-23.99 24-23.99S248 58.75 248 72v160h160C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i><i class="number-count counting-of-count-nafar"
                                                                           data-number="1" data-min="1"
                                                                           data-value="l-bozorgsal"
                                                                           id="bozorgsal_prtal">1</i><i
                                                                            class="counting-of-count-nafar minus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280H40c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h368C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i></div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="col-xs-12 cbox-count-nafar-ch koodak-num">
                                                        <div class="row">
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="type-of-count-nafar"><h6> کودک </h6>(بین
                                                                    2 الی 12 سال)
                                                                </div>
                                                            </div>
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="num-of-count-nafar"><i
                                                                            class="counting-of-count-nafar plus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280h-160v160c0 13.25-10.75 24.01-24 24.01S200 453.3 200 440v-160h-160c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h160v-160c0-13.25 10.75-23.99 24-23.99S248 58.75 248 72v160h160C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i><i class="number-count counting-of-count-nafar"
                                                                           id="kodak_prtal" data-number="0" data-min="0"
                                                                           data-value="l-kodak">0</i><i
                                                                            class="counting-of-count-nafar minus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280H40c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h368C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i></div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="col-xs-12 cbox-count-nafar-ch nozad-num">
                                                        <div class="row">
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="type-of-count-nafar"><h6> نوزاد </h6>
                                                                    (کوچکتر از 2 سال)
                                                                </div>
                                                            </div>
                                                            <div class="col-xs-12 col-sm-6 col-6">
                                                                <div class="num-of-count-nafar"><i
                                                                            class="counting-of-count-nafar plus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280h-160v160c0 13.25-10.75 24.01-24 24.01S200 453.3 200 440v-160h-160c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h160v-160c0-13.25 10.75-23.99 24-23.99S248 58.75 248 72v160h160C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i><i class="number-count counting-of-count-nafar"
                                                                           data-number="0" data-min="0" id="nozad_prtal"
                                                                           data-value="l-nozad">0</i><i
                                                                            class="counting-of-count-nafar minus-nafar">
                                                                        <svg xmlns="http://www.w3.org/2000/svg"
                                                                             viewBox="0 0 448 512">
                                                                            <!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
                                                                            <path d="M432 256C432 269.3 421.3 280 408 280H40c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h368C421.3 232 432 242.8 432 256z"/>
                                                                        </svg>
                                                                    </i></div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-lg-2 col-md-6 col-sm-12 col-12 btn_s col_search">
                                            <button type="button" onclick="gds_ticket_portal_check()" class="button_searchBox w-100"><span>جستجو</span></button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    </section>


    {include file="include_files/blog.tpl"}
    {include file="include_files/news.tpl"}
    {include file="include_files/newsletter.tpl"}

</main>
{include file="include_files/footer.tpl"}
</body>
{include file="include_files/script-footer.tpl"}