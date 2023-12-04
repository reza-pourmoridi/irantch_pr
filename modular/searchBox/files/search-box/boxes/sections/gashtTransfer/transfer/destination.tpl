
{assign var="cities" value=$obj_main_page->getCitiesGashtTransfer()}
<div class="col-lg-2 col-md-6 col-sm-6 col-12 col_search">
    <div class="form-group"><select data-placeholder="##DesOrTrain##"
                                    name="transfer_destination" id="transfer_destination"
                                    class="select2_in transfer-destination-js select2-hidden-accessible" tabindex="-1"
                                    aria-hidden="true">
            <option value="">##ChoseOption##...</option>
            {foreach $cities as $city}
                <option value="{$city['city_code']}">{$city['city_name']}</option>
            {/foreach}

        </select></div>
</div>