{assign var="type_data" value=['is_active'=>1 , 'limit' =>10]}
                        {assign var='banners' value=$obj_main_page->galleryBannerMain($type_data)}
<div class="i_modular_banner_gallery OWL_slider_banner owl-carousel owl-theme">
{foreach $banners as $key => $banner}
<div class="__i_modular_nc_item_class_0 item">
<img alt='{$banner["title"]}' class="__image_class__" src='{$banner["pic"]}'/>
</div>
{/foreach}


</div>
