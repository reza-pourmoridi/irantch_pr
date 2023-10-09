{assign var="data_search_blog" value=['service'=>'Public','section'=>'article', 'limit' =>4]}
{assign var='articles' value=$obj_main_page->articlesPosition($data_search_blog)}
{assign var='counter' value=0}
{assign var="article_count" value=$articles|count}
{if $articles}
<div class="my-blog">
    <div class="container">
        <div class="my-titr">
            <h2>وبلاگ</h2>
            <svg xmlns="http://www.w3.org/2000/svg" version="1.0" width="2358.000000pt" height="218.000000pt" viewBox="0 0 2358.000000 218.000000" preserveAspectRatio="xMidYMid meet">
                <g transform="translate(0.000000,218.000000) scale(0.100000,-0.100000)"  stroke="none">
                    <path d="M18199 2040 c-450 -9 -1198 -29 -2029 -55 -1986 -63 -4578 -200 -7435 -396 -435 -29 -4150 -315 -4410 -339 -1332 -122 -2603 -298 -3955 -546 -195 -36 -356 -66 -357 -68 -2 -1 95 -8 215 -14 1329 -73 2436 -81 3567 -27 594 29 512 22 3440 300 874 83 2850 249 3800 320 2517 186 4696 292 6660 324 325 6 865 13 1200 16 1060 10 2141 46 3275 110 711 40 876 56 1075 101 61 14 147 33 192 43 45 9 85 19 88 23 3 3 -117 8 -267 11 -210 4 -385 16 -758 51 -789 73 -1343 111 -2025 136 -376 15 -1735 20 -2276 10z"/>
                </g>
            </svg>
        </div>
        <div class="parent-blog">
            <div  class="blog-item">
                <a href="{{$articles[0]['link']}}" class="parent-link-blog">
                    <img src="project_files/images/5497750661271-6.jpg" alt="blog-img">
                    <div class="text-blog">
                        <h3>{{$articles[0]['title']}}</h3>
                        <div class="parent-comment-star">
                            <div class="data-blog">
                                <i class="fa-light fa-calendar-days"></i>
                                <span>{{$articles[0]['created_at']}}</span>
                            </div>
                            <div class="comment-blog">
                                <i class="fa-light fa-comment"></i>
                                {{$articles[0]['comments_count']['comments_count']}}
                            </div>
                        </div>
                    </div>
                </a>
            </div>
            <div  class="blog-item blog-grid">
                {foreach $articles as $key => $article}
                    {if $counter > 0 and $counter < 5}

                        <a href="{$article['link']}" class="child-item-blog gradient{{$counter}}">
                            <img src="{$article['image']}" alt="{$article['title']}">
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
                    {/if}
                    {$counter = $counter + 1}

                {/foreach}

            </div>
        </div>
    </div>
</div>
{/if}