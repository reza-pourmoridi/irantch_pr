{if $obj_main_page->isLogin() }
    <span class="logined-name">##Welcomeing##</span>
    {else}
    <a class="logined-name" href="{$smarty.const.ROOT_ADDRESS}/authenticate">##OsafarLogin## / ##OsafarSetAccount##</a>
{/if}
