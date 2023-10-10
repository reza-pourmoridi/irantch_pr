{assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>40]}
                        {assign var='articles' value=$obj_main_page->articlesPosition($data_search_blog)}
                        {assign var='counter' value=0}
                        {assign var="article_count" value=$articles|count}
                        {if $articles}
<div class="i_modular_blog my-blog">
<div class="container">
<div class="my-titr">
<h2>وبلاگ</h2>
<svg height="218.000000pt" preserveaspectratio="xMidYMid meet" version="1.0" viewbox="0 0 2358.000000 218.000000" width="2358.000000pt" xmlns="http://www.w3.org/2000/svg">
<g stroke="none" transform="translate(0.000000,218.000000) scale(0.100000,-0.100000)">
<path d="M18199 2040 c-450 -9 -1198 -29 -2029 -55 -1986 -63 -4578 -200 -7435 -396 -435 -29 -4150 -315 -4410 -339 -1332 -122 -2603 -298 -3955 -546 -195 -36 -356 -66 -357 -68 -2 -1 95 -8 215 -14 1329 -73 2436 -81 3567 -27 594 29 512 22 3440 300 874 83 2850 249 3800 320 2517 186 4696 292 6660 324 325 6 865 13 1200 16 1060 10 2141 46 3275 110 711 40 876 56 1075 101 61 14 147 33 192 43 45 9 85 19 88 23 3 3 -117 8 -267 11 -210 4 -385 16 -758 51 -789 73 -1343 111 -2025 136 -376 15 -1735 20 -2276 10z"></path>
</g>
</svg>
</div>
<div class="parent-blog">
<div class="blog-item">
<a class="__i_modular_c_item_0 parent-link-blog" href="{$articles[0]['link']}">
<img alt="{$articles[0]['title']}" src="{$articles[0]['image']}"/>
<div class="text-blog">
<h3>{$articles[0]['title']}</h3>
<div class="parent-comment-star">
<div class="data-blog">
<i class="fa-light fa-calendar-days"></i>
<span>{$articles[0]['created_at']}</span>
</div>
<div class="comment-blog">
<i class="fa-light fa-comment"></i>
{$articles[0]['comments_count']['comments_count']}
</div>
</div>
</div>
</a>
</div>
<div class="blog-item blog-grid">
{foreach $articles as $key => $article} {if $counter >= 1 and $counter <= 4}
<a class="__i_modular_nc_item_1 child-item-blog gradient1" href="{$article['link']}">
<img alt="{$article['title']}" src="{$article['image']}"/>
<div class="text-blog">
<h3>{$article['title']}</h3>
<div class="parent-comment-star">
<div class="data-blog">
<i class="fa-light fa-calendar-days"></i>
<span>{$article['created_at']}</span>
</div>
<div class="comment-blog">
<i class="fa-light fa-comment"></i>
{$article['comments_count']['comments_count']}
</div>
</div>
</div>
</a>
{/if}{$counter = $counter + 1}{/foreach}



</div>
</div>
</div>
</div>
{/if}