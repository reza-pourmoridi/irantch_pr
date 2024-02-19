{assign var=dateNow value=dateTimeSetting::jdate("Ymd", "", "", "", "en")}
{assign var="tour_params" value=['type'=>'','limit'=> '4','dateNow' => $dateNow, 'country' =>'','city' => null]}
                                {assign var='tour' value=$obj_main_page->getToursReservation($tour_params)}
                                {if $tour}
                                    {assign var='check_tour' value=true}
                                {/if}
                                {assign var="min" value=0}
                                {assign var="max" value=4}
                            
{if $check_tour}
<section class="i_modular_tours tour-paeiz-last">
<img alt="img-bg" class="tour-bg1" src="project_files/images/bg1.jpg"/>
<div class="__tour__ container">
<div class="title-paeize">
<div class="text-title-paeize">
<h2>تورهای لحظه آخری </h2>
<p>هیجان لحظه‌آخری، تورهای گردشگری با بهترین قیمت و تجربه‌ی بی‌نظیر</p>
</div>
<a class="more-title-paeize" href="{$smarty.const.ROOT_ADDRESS}/page/tour">
<span>تورهای بیشتر</span>
<svg viewbox="0 0 320 512" xmlns="http://www.w3.org/2000/svg"><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M234.8 36.25c3.438 3.141 5.156 7.438 5.156 11.75c0 3.891-1.406 7.781-4.25 10.86L53.77 256l181.1 197.1c6 6.5 5.625 16.64-.9062 22.61c-6.5 6-16.59 5.594-22.59-.8906l-192-208c-5.688-6.156-5.688-15.56 0-21.72l192-208C218.2 30.66 228.3 30.25 234.8 36.25z"></path></svg>
</a>
</div>
<div class="parent-last-tour">
<div class="owl-carousel owl-theme owl-last-tour">

                                {foreach $tour as $item}
                                    {if $min <= $max}
                                
<div class="__i_modular_nc_item_class_0 item">
<a class="item-last-tour" href="{$smarty.const.ROOT_ADDRESS}/detailTour/{$item['id']}/{$item['tour_slug']}">
<div class="parent-img">
<img alt="{$item['tour_name']}" class="__image_class__" src="{$smarty.const.ROOT_ADDRESS_WITHOUT_LANG}/pic/reservationTour/{$item['tour_pic']}"/>
</div>
<div class="parent-text">
<h2 class="__title_class__">{$item['tour_name']}</h2>
<h4><span class="__day_class__">{$item['night'] + 1}</span>روز <span class="__night_class__">{$item['night']}</span> شب</h4>
<h4>تاریخ برگزاری: <span class="__date_class__">{assign var="year" value=substr($item['start_date'], 0, 4)}
                                        {assign var="month" value=substr($item['start_date'], 4, 2)}
                                        {assign var="day" value=substr($item['start_date'], 6)}
                                        {$year}/{$month}/{$day}
                                        </span></h4>
<h4>ایرلاین: <span class="__airline_class__">{$item['airline_name']}</span></h4>
<button type="button">
<span>مشاهده بیشتر</span>
<i class="fa-light fa-arrow-left-long"></i>
</button>
</div>
</a>
</div>

                                    {$min = $min + 1}
                                    {/if}
                                {/foreach}
                                




</div>
</div>
</div>
</section>
{/if}