<div class="col-lg-4 col-md-6 col-sm-6 col-12 col_search">
    <div class="form-group">
        <select data-placeholder="##cityrTrain##"
                name="origin_bus"
                id="origin_bus"
                class="select2_in select2-hidden-accessible select-origin-route-bus-js"
                tabindex="-1" aria-hidden="true">
            <option value="">##ChoseOption##...</option>
            {foreach $cities as $city}
                <option value="{$city['id']}">{$city['text']}</option>
            {/foreach}
        </select>
    </div>
</div>