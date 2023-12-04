
{assign var="countries" value=$obj_main_page->countryInsurance()}
<div class="tab-pane {if  $smarty.const.GDS_SWITCH eq 'page'} active {/if}" id="Insurance">
    <div class="col-md-12 col-12">
        <div class="row  ">
            <form data-action="https://s360online.iran-tech.com/" method="post" target="_blank"
                  name="gdsInsurance" id="gdsInsurance" class="d_contents">
                <div class="col-lg-3 col-md-4 col-sm-6 col-12 col_search">
                    <div class="form-group">
                            <select data-placeholder="##SelectDestinationCountry##"
                                    name="insurance_destination_country"
                                    id="insurance_destination_country"
                                    class="select2_in  select2-hidden-accessible insurance-destination-country-js"
                                    tabindex="-1" aria-hidden="true">
                            <option value="">##ChoseOption##...</option>
                                {foreach $countries as $country}
                                <option value="{$country['abbr']}">{$country['persian_name']}({$country['abbr']})</option>
                                    {/foreach}
                            </select>
                    </div>
                </div>
                <div class="col-lg-3 col-md-4 col-sm-6 col-12 col_search">
                    <div class="form-group">
                        <select data-placeholder="##travelDurationChoose##"
                                name="travel_time" id="travel_time"
                                class="select2_in travel-time-js select2-hidden-accessible"
                                tabindex="-1" aria-hidden="true">
                            <option value="">##ChoseOption##...</option>
                            <option value="5">##untill## 5 ##Day##</option>
                            <option value="7">##untill## 7 ##Day##</option>
                            <option value="8">##untill## 8 ##Day##</option>
                            <option value="15">##untill## 15 ##Day##</option>
                            <option value="23">##untill## 23 ##Day##</option>
                            <option value="31">##untill## 31 ##Day##</option>
                            <option value="45">##untill## 45 ##Day##</option>
                            <option value="62">##untill## 62 ##Day##</option>
                            <option value="92">##untill## 92 ##Day##</option>
                            <option value="182">##untill## 182 ##Day##</option>
                            <option value="186">##untill## 186 ##Day##</option>
                            <option value="365">##untill## 365 ##Day##</option>
                        </select></div>
                </div>
                <div class="col-lg-2 col-md-4 col-sm-6 col-12 col_search">
                    <div class="form-group">
                        <select name="number_of_passengers"
                                id="number_of_passengers"
                                data-placeholder="##ChoosePassangersNumber##"
                                class="select2_in passengers-count-js select2-hidden-accessible number-of-passengers-js"
                                tabindex="-1" aria-hidden="true">
                            <option value="">##ChoseOption##...</option>
                            {for $i=1 to 9}
                                <option value="{$i}">{$i} ##People##</option>
                            {/for}
                        </select>
                    </div>
                </div>
                <div class="count-passenger count-passengers-js">
                    <div class="col-lg-2 col-md-4 col-sm-6 col-12 col_search search_col nafarat-bime passenger-age-div-js">
                        <div class="form-group">
                            <input type="text"
			    readonly=""
                                   class="form-control passengers-age-js shamsiBirthdayCalendar"
                                   name="txt_birth_insurance1" autocomplete="off"
                                   id="txt_birth_insurance1"
                                   placeholder="##PassengerBirthDate## 1">
                            <i class="fal fa-calendar-alt"></i>
                        </div>
                    </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-6 col-12 col_search search_btn_insuranc">
                    <button type="button" onclick="searchInsurance()"
                            class="btn theme-btn seub-btn b-0"><span>##Search##</span></button>
                </div>
            </form>
        </div>
    </div>
</div>