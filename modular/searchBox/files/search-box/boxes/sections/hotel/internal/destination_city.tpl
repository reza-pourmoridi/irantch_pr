<div class="col-lg-3 col-md-6 col-sm-6 col-12 col_search search_col">
    <div class="form-group destination_start">
        <div class="s-u-in-out-wrapper raft raft-change change-bor w-100">
            <input id="autoComplateSearchIN" name="autoComplateSearchIN"
                   class="inputSearchForeign w-100" type="text" value=""
                   placeholder='##Selection## ##City##'
                   autocomplete="off"
                   onkeyup="searchCity('hotel')"
                   onclick="openBoxPopular('hotel')">
            <input type='hidden' id='autoComplateSearchIN_hidden' value='' placeholder='##Selection## ##City##'>
            <input type='hidden' id='autoComplateSearchIN_hidden_en' value='' placeholder='##Selection## ##City##'>
            <ul id="listSearchCity" class="ul-inputSearch-externalHotel displayiN"></ul>
        </div>

    </div>
</div>