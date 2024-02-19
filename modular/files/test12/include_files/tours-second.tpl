{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}
{assign var="tour_params" value=['type'=>'special','limit'=> '3','dateNow' => $dateNow, 'country' =>'','city' => null]}
                                {assign var='__tour_var__' value=$obj_main_page->getToursReservation($tour_params)}
                                {if $__tour_var__}
                                    {assign var='check_tour' value=true}
                                {/if}
                                {assign var="min_" value=0}
                                {assign var="max_" value=0}
                            
{if $check_general}
<section class="i_modular_tours special-tours-paeiz">
<div class="__tour__special__ container">
<div class="title-paeize">
<div class="text-title-paeize">
<h2>تورهای ویژه </h2>
<p>سفرهای ویژه با تجربیات بی‌نظیر در دنیای گردشگری</p>
</div>
<a class="more-title-paeize" href="{$smarty.const.ROOT_ADDRESS}/page/tour">
<span>تورهای بیشتر</span>
<svg viewbox="0 0 320 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M234.8 36.25c3.438 3.141 5.156 7.438 5.156 11.75c0 3.891-1.406 7.781-4.25 10.86L53.77 256l181.1 197.1c6 6.5 5.625 16.64-.9062 22.61c-6.5 6-16.59 5.594-22.59-.8906l-192-208c-5.688-6.156-5.688-15.56 0-21.72l192-208C218.2 30.66 228.3 30.25 234.8 36.25z"></path></svg>
</a>
</div>
<div class="parent-special-tours-paeiz">
{if $tour_special[0]}
<a class="__i_modular_c_item_class_0 items-special-tours-paeiz" href="{$smarty.const.ROOT_ADDRESS}/detailTour/{$__tour_var__[0]['id']}/{$__tour_var__[0]['tour_slug']}">
<img alt="{$__tour_var__[0]['tour_name']}" class="__image_class__" src="{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__tour_var__[0]['tour_pic']}"/>
<div class="parent-text">
<h2 class="__title_class__">{$__tour_var__[0]['tour_name']}</h2>
<h4><span class="__day_class__">{$__tour_var__[0]['night'] + 1}</span>روز <span class="__night_class__">{$__tour_var__[0]['night']}</span> شب</h4>
<h4>تاریخ برگزاری: <span class="__date_class__">{assign var="year" value=substr($__tour_var__[0]['start_date'], 0, 4)}
                                        {assign var="month" value=substr($__tour_var__[0]['start_date'], 4, 2)}
                                        {assign var="day" value=substr($__tour_var__[0]['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        </span></h4>
<h4>ایرلاین: <span class="__airline_class__">{$__tour_var__[0]['airline_name']}</span></h4>
</div>
</a>
{/if}
<div class="parent-special-tours2">
{if $tour_special[0]}
<a class="__i_modular_c_item_class_1 items-special-tours2" href="{$smarty.const.ROOT_ADDRESS}/detailTour/{$__tour_var__[0]['id']}/{$__tour_var__[0]['tour_slug']}">
<img alt="{$__tour_var__[1]['tour_name']}" class="__image_class__" src="{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__tour_var__[1]['tour_pic']}"/>
<div class="parent-text">
<h2 class="__title_class__">{$__tour_var__[1]['tour_name']}</h2>
<h4><span class="__day_class__">{$__tour_var__[1]['night'] + 1}</span>روز <span class="__night_class__">{$__tour_var__[1]['night']}</span> شب</h4>
<h4>تاریخ برگزاری: <span class="__date_class__">{assign var="year" value=substr($__tour_var__[1]['start_date'], 0, 4)}
                                        {assign var="month" value=substr($__tour_var__[1]['start_date'], 4, 2)}
                                        {assign var="day" value=substr($__tour_var__[1]['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        </span></h4>
<h4>ایرلاین: <span class="__airline_class__">{$__tour_var__[1]['airline_name']}</span></h4>
</div>
</a>
{/if}
{if $tour_special[0]}
<a class="__i_modular_c_item_class_2 items-special-tours2" href="{$smarty.const.ROOT_ADDRESS}/detailTour/{$__tour_var__[0]['id']}/{$__tour_var__[0]['tour_slug']}">
<img alt="{$__tour_var__[2]['tour_name']}" class="__image_class__" src="{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__tour_var__[2]['tour_pic']}"/>
<div class="parent-text">
<h2 class="__title_class__">{$__tour_var__[2]['tour_name']}</h2>
<h4><span class="__day_class__">{$__tour_var__[2]['night'] + 1}</span>روز <span class="__night_class__">{$__tour_var__[2]['night']}</span> شب</h4>
<h4>تاریخ برگزاری: <span class="__date_class__">{assign var="year" value=substr($__tour_var__[2]['start_date'], 0, 4)}
                                        {assign var="month" value=substr($__tour_var__[2]['start_date'], 4, 2)}
                                        {assign var="day" value=substr($__tour_var__[2]['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        </span></h4>
<h4>ایرلاین: <span class="__airline_class__">{$__tour_var__[2]['airline_name']}</span></h4>
</div>
</a>
{/if}
</div>
{if $tour_special[0]}
<a class="__i_modular_c_item_class_3 items-special-tours-paeiz items-special-tours-paeiz2" href="{$smarty.const.ROOT_ADDRESS}/detailTour/{$__tour_var__[0]['id']}/{$__tour_var__[0]['tour_slug']}">
<img alt="{$__tour_var__[3]['tour_name']}" class="__image_class__" src="{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$__tour_var__[3]['tour_pic']}"/>
<div class="parent-text">
<h2 class="__title_class__">{$__tour_var__[3]['tour_name']}</h2>
<h4><span class="__day_class__">{$__tour_var__[3]['night'] + 1}</span>روز <span class="__night_class__">{$__tour_var__[3]['night']}</span> شب</h4>
<h4>تاریخ برگزاری: <span class="__date_class__">{assign var="year" value=substr($__tour_var__[3]['start_date'], 0, 4)}
                                        {assign var="month" value=substr($__tour_var__[3]['start_date'], 4, 2)}
                                        {assign var="day" value=substr($__tour_var__[3]['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        </span></h4>
<h4>ایرلاین: <span class="__airline_class__">{$__tour_var__[3]['airline_name']}</span></h4>
</div>
</a>
{/if}
</div>
</div>
</section>
{/if}