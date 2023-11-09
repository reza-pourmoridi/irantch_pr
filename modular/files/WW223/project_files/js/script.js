$(document).ready(function () {
    $('.OWL_slider_banner').owlCarousel({
        rtl: true,
        loop:true,
        margin:1,
        nav:false,
        dots:false,
        animateOut: 'fadeOut',
        autoplay:true,
        autoplayTimeout:6000,
        items:1,
    })
    // search
    $('#hotel_local_room ul').click(function () {
        $('.hotel_local-rooms').toggleClass('active_p');
    });
    $('#hotel_local_room').click(function (event) {
        $('html').one('click', function () {
            $('.myhotels-rooms').removeClass('active_p');
        });
        event.stopPropagation();
    });
    $('.hotel_local-rooms').on('click', '.btn_add_room_hotel_local', function (e) {
        $('.hotel_local-rooms .close').show();
        $('.hotel_local-rooms .close').addClass("d-flexs");
        $(this).parents(".hotel_local-rooms").find(".close").removeClass("d-none");
        let roomCount = parseInt($('.myroom-hotel_local-item').length);
        let numberAdult = parseInt($('.number_adult_hotel_local').text());
        let number_room = parseInt($('.number_room_hotel_local').text());
        $('.number_adult_hotel_local').text(numberAdult + 1);
        $('.number_room_hotel_local').text(number_room + 1);
        let code = createRoomHotelLocal(roomCount);
        $(".hotel_local_select_room").append(code);
        if (roomCount == 3) {
            $(this).hide();
        }
    });
    $('.hotel_local-rooms').on('click', '.myroom-hotel_local-item .close', function () {
        let babyCountThis = $(this).parents('.myroom-hotel_local-item').find('.countChild_hotel_local').val();
        let number_baby = $('.number_baby_hotel_local').text();
        $('.number_baby_hotel_local').text(number_baby - babyCountThis);
        let AdultCountThis = $(this).parents('.myroom-hotel_local-item').find('.countParent_hotel_local').val();
        let number_adult = $('.number_adult_hotel_local').text();
        $('.number_adult_hotel_local').text(number_adult - AdultCountThis);
        $('.btn_add_room_hotel_local').show();
        let roomNumber = $(this).parents(".myroom-hotel_local-item").data("roomnumber");
        let roomCount = $(".myroom-hotel_local-item").length;
        let number_room = parseInt($('.number_room_hotel_local').text());
        $('.number_room_hotel_local').text(number_room - 1);
        $(this).parents(".myroom-hotel_local-item").remove();
        let countRoom = parseInt($('#countRoom').val()) - 1;
        $("#countRoom option:selected").prop("selected", false);
        $("#countRoom option[value=" + countRoom + "]").prop("selected", true);
        let numberRoom = 1;
        let numberText = "اول";
        $('.myroom-hotel_local-item').each(function () {
            $(this).data("roomnumber", numberRoom);
            if (numberRoom == 1) {
                numberText = "اول";
            } else if (numberRoom == 2) {
                numberText = "دوم";
            } else if (numberRoom == 3) {
                numberText = "سوم";
            } else if (numberRoom == 4) {
                numberText = "چهارم";
            }
            $(this).find('.myroom-hotel_local-item-title').html('<span class="close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg></span>' + ' اتاق ' + numberText);
            $(this).find(".myroom-hotel_local-item-info").find("input[name^='adult_hotel_local']").attr("name", "adult_hotel_local" + numberRoom);
            $(this).find(".myroom-hotel_local-item-info").find("input[name^='adult_hotel_local']").attr("id", "adult_hotel_local" + numberRoom);
            $(this).find(".myroom-hotel_local-item-info").find("input[name^='child_hotel_local']").attr("name", "child_hotel_local" + numberRoom);
            $(this).find(".myroom-hotel_local-item-info").find("input[name^='child_hotel_local']").attr("id", "child_hotel_local" + numberRoom);
            let numberChild = 1;
            let inputNameSelectChildAge = $(this).find(".tarikh-tavalods .tarikh-tavalod-item");
            inputNameSelectChildAge.each(function () {
                $(this).find("select[name^='childAge']").attr("name", "childAge" + numberRoom + numberChild);
                $(this).find("select[name^='childAge']").attr("id", "childAge" + numberRoom + numberChild);
                numberChild++;
            });
            numberRoom++;
        });
        if (roomCount == 2) {
            $('.myroom-hotel_local-item-title .close').hide();
        }
    });
    $('.hotel_local-rooms').on('click', 'i.addParent_hotel_local', function () {
        var inputNum = $(this).siblings(".countParent_hotel_local").val();
        if (inputNum < 7) {
            inputNum++;
            let numberAdult = parseInt($('.number_adult_hotel_local').text());
            let resultNumber = numberAdult + 1;
            $(this).siblings(".countParent_hotel_local").val(inputNum);
            $('.number_adult_hotel_local').html('');
            $('.number_adult_hotel_local').append(resultNumber);
        }
    });
    $('.hotel_local-rooms').on('click', 'i.minusParent_hotel_local', function () {
        let data_roomnumber = $(this).parents('.myroom-hotel_local-item').attr('data-roomnumber');
        let ThiscountParent = $(this).parents('.myroom-hotel_local-item').find('.countParent_hotel_local').val();
        var inputNum = $(this).siblings(".countParent_hotel_local").val();
        if (inputNum > 1) {
            inputNum--;
            let numberAdult = parseInt($('.number_adult_hotel_local').text());
            let resultNumber = numberAdult - 1;
            $(this).siblings(".countParent_hotel_local").val(inputNum);
            $('.number_adult_hotel_local').html('');
            $('.number_adult_hotel_local').append(resultNumber);
        }
    });
    $('.hotel_local-rooms').on('click', 'i.addChild_hotel_local', function () {
        var inputNum = $(this).siblings(".countChild_hotel_local").val();
        inputNum++;
        if (inputNum < 5) {
            let numberBaby = parseInt($('.number_baby_hotel_local').text());
            let numberBabyThis = parseInt($(this).parents().find('.countChild_hotel_local').val()) + 1;
            let resultNumber = numberBaby + 1;
            $(this).siblings(".countChild_hotel_local").val(inputNum);
            $('.number_baby_hotel_local').html('');
            $('.number_baby_hotel_local').append(resultNumber);
            $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();
            let roomNumber = $(this).parents(".myroom-hotel_local-item").data("roomnumber");
            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);
            $(this).parents(".myroom-hotel_local-item-info").find(".tarikh-tavalods").html(htmlBox);
        }
    });
    $('.hotel_local-rooms').on('click', 'i.minusChild_hotel_local', function () {
        var inputNum = $(this).siblings(".countChild_hotel_local").val();
        $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();
        if (inputNum != 0) {
            let numberBaby = parseInt($('.number_baby_hotel_local').text());
            let numberBabyThis = parseInt($(this).parents().find('.countChild_hotel_local').val()) + 1;
            let resultNumber = numberBaby - 1;
            inputNum--;
            $(this).siblings(".countChild_hotel_local").val(inputNum);
            $('.number_baby_hotel_local').html('');
            $('.number_baby_hotel_local').append(resultNumber);
            let roomNumber = $(this).parents(".myroom-hotel_local-item").data("roomnumber");
            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);
            $(this).parents(".myroom-hotel_local-item-info").find(".tarikh-tavalods").html(htmlBox);
        } else {
            $(this).siblings(".countChild_hotel_local").val('0');
        }
    });
    $('.hotel_local-rooms').on('click', '.close_room', function () {
        $(this).parent().parent().removeClass('active_p');
    });
    function createRoomHotelLocal(roomCount) {
        var HtmlCode = "";
        let i = $('.myroom-hotel_local-item').length + 1;
        let numberText = "اول";
        let valuefirst;
        if (i == 1) {
            numberText = "اول";
            valuefirst = "2"
        } else if (i == 2) {
            numberText = "دوم";
            valuefirst = "1";
        } else if (i == 3) {
            numberText = "سوم";
            valuefirst = "1";
        } else if (i == 4) {
            numberText = "چهارم";
            valuefirst = "1";
        }
        if (i < 5) {
            HtmlCode += `<div class="myroom-hotel_local-item" data-roomNumber="${i}"> <div class="myroom-hotel_local-item-title"> <span class="close"> <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg> </span> اتاق  ${numberText} </div><div class="myroom-hotel_local-item-info"> <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal"> <h6>بزرگسال</h6> (بزرگتر از ۱۲ سال) <div><i class="addParent_hotel_local plus-nafar hotelroom-minus plus-hotelroom-bozorgsal"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 256C432 269.3 421.3 280 408 280h-160v160c0 13.25-10.75 24.01-24 24.01S200 453.3 200 440v-160h-160c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h160v-160c0-13.25 10.75-23.99 24-23.99S248 58.75 248 72v160h160C421.3 232 432 242.8 432 256z"></path></svg></i> <input readonly class="countParent_hotel_local"  min="0" value="${valuefirst}" max="5" type="number" name="adultHotelLocal${i}" id="adultHotelLocal${i}"> <i class="minusParent_hotel_local minus-nafar hotelroom-minus minus-hotelroom-bozorgsal"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 256C432 269.3 421.3 280 408 280H40c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h368C421.3 232 432 242.8 432 256z"></path></svg></i> </div> </div> <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal"> <h6>کودک</h6> (کوچکتر از ۱۲ سال) <div> <i class="addChild_hotel_local plus-nafar hotelroom-minus plus-hotelroom-koodak"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 256C432 269.3 421.3 280 408 280h-160v160c0 13.25-10.75 24.01-24 24.01S200 453.3 200 440v-160h-160c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h160v-160c0-13.25 10.75-23.99 24-23.99S248 58.75 248 72v160h160C421.3 232 432 242.8 432 256z"></path></svg></i><input readonly class="countChild_hotel_local" min="0" value="0" max="5" type="number" name="childHotelLocal${i}" id="childHotelLocal${i}"> <i class="minusChild_hotel_local minus-nafar hotelroom-minus minus-hotelroom-koodak"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 256C432 269.3 421.3 280 408 280H40c-13.25 0-24-10.74-24-23.99C16 242.8 26.75 232 40 232h368C421.3 232 432 242.8 432 256z"></path></svg></i> </div> </div><div class="tarikh-tavalods"></div> </div> </div>`;
        }
        return HtmlCode;
    }
    $('.switch-label-off').click();
    $('#number_of_passengers').on('change', function (e) {
        var itemInsu = $(this).val();
        itemInsu++;
        var HtmlCode = "";
        $(".nafaratbime").html('');
        var i = 1;
        while (i < itemInsu) {
            HtmlCode += "<div class='col-lg-2 col-md-6 col-6 col_search search_col nafarat-bime '>" +
                "<div class='form-group'>"+
                "<input placeholder='تاریخ تولد مسافر " + i + "' autocomplete='off' type='text' name='txt_birth_insurance" + i + "' id='txt_birth_insurance" + i + "' class='shamsiBirthdayCalendar form-control' />" +
                "</div>"+
                "</div>";
            i++;
        }
        $(".nafaratbime ").append(HtmlCode);
    });
    $(".plus-nafar").click(function () {
        var nafar = $(this).siblings(".number-count").attr('data-number');
        if (nafar < 9) {
            var newnafar = ++nafar;
            $(this).siblings(".number-count").html(newnafar);
            $(this).siblings(".number-count").attr('data-number', newnafar);
            var whathidden = $(this).siblings(".number-count").attr('data-value');
            $("." + whathidden).val(newnafar);

        }
        var nafarbozorg = Number($(this).parents(".box-of-count-nafar").find(".bozorg-num .number-count").attr('data-number'));
        var nafarkoodak = Number($(this).parents(".box-of-count-nafar").find(".koodak-num .number-count").attr('data-number'));
        var nafarnozad = Number($(this).parents(".box-of-count-nafar").find(".nozad-num .number-count").attr('data-number'));
        var tedad = nafarbozorg + nafarkoodak + nafarnozad;
        if(nafarnozad == 0 && nafarkoodak == 0){
            $(this).parents(".box-of-count-nafar").find(".text-count-nafar").text(tedad + ' مسافر ');
        }else{
            $(this).parents(".box-of-count-nafar").find(".text-count-nafar").text(tedad + ' مسافر ');

        }
    });
    $(".minus-nafar").click(function () {
        var nafar = $(this).siblings(".number-count").attr('data-number');

        var nmin = $(this).siblings(".number-count").attr('data-min');
        if (nafar > nmin) {
            var newnafar = --nafar;
            $(this).siblings(".number-count").html(newnafar);
            $(this).siblings(".number-count").attr('data-number', newnafar);
            var whathidden = $(this).siblings(".number-count").attr('data-value');
            $("." + whathidden).val(newnafar);
        }
        var nafarbozorg2 = Number($(this).parents(".box-of-count-nafar").find(".bozorg-num .number-count").attr('data-number'));
        var nafarkoodak2 = Number($(this).parents(".box-of-count-nafar").find(".koodak-num .number-count").attr('data-number'));
        var nafarnozad2 = Number($(this).parents(".box-of-count-nafar").find(".nozad-num .number-count").attr('data-number'));
        var tedad2 = nafarbozorg2 + nafarkoodak2 + nafarnozad2;
        if(nafarnozad2 == 0 && nafarkoodak2 == 0){
            $(this).parents(".box-of-count-nafar").find(".text-count-nafar").text(tedad2 + ' مسافر ');
        }else{
            $(this).parents(".box-of-count-nafar").find(".text-count-nafar").text(tedad2 + ' مسافر ');
        }
    });
    $('.box-of-count-nafar-boxes').click(function () {

        $('.cbox-count-nafar').toggle();
        $(this).parents().find('.down-count-nafar').toggleClass('fa-caret-up');
    });
    $('body').on('click', '.more_close_matn', function () {
        $(this).parents('.card_matn_').removeClass('show_more');
        $(this).parents('.card_matn_').find('.more_read_matn').show();
        $(this).remove();
    });
    $('.more_read_matn').click(function () {
        $(this).parents('.card_matn_').addClass('show_more');
        $(this).hide();
        $(this).parent('.content_card_matn').append('<a class="more_close_matn">بستن</a>');
    });
    $('.more_read').click(function () {
        $(this).parents('.card_').addClass('show_more');
        $(this).hide();
        $(this).parent('.content_card').append('<a class="more_close">بستن</a>');
    });
    $('body').on('click', '.more_close', function () {
        $(this).parents('.card_').removeClass('show_more');
        $(this).parents('.content_card').find('.more_read').show();
        $(this).remove();
    });
    $('.more_matn').click(function () {
        $(this).parent('.c-card-content').toggleClass('selected');
        $(this).toggleClass('select_btn');

        if ($(this).parent('.c-card-content').hasClass('selected')) {
            $(this).text('بستن')
        } else {
            $(this).text('بیشتر بخوانید')
        }
    });
    setTimeout(function () {

        if ($('.more_matn').parent().find('.typo__context').height() < 210) {
            $('.more_matn').hide();

            $('.c-card-content .typo__context').addClass('hide_before');
        } else {
            $('.more_matn').show();
        }

    }, 2000);
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    $(document).ready(function () {
        $('#package_room ul').click(function () {
            $('.mypackege-rooms').toggleClass('active_p');
        });
        $('.hotel_passenger_picker ul').click(function () {
            $('.myhotels-rooms').toggleClass('active_p');
        });
        $('#package_room').click(function(event) {
            $('html').one('click',function() {
                $('.myhotels-rooms').removeClass('active_p');
            });

            event.stopPropagation();
        });


        var wwidth = $(window).width();
        if (wwidth < 575) {
            var wheight = $(window).height();
            var sheight = $('.search').height();
            var height11 = sheight + 200;
            $(".js-height-full").height(height11);
        } else {
            var wheight = $(window).height();
            var sheight = $('.search').height();
            var height1 = wheight - sheight;
            var height = height1 + sheight;
            $(".js-height-full").height(height);
        }
    });
    $('#countRoomPackage').on('change', function (e) {

        var roomCount = $("#countRoomPackage").val();
        createRoomHotelPackage(roomCount);
        $(".mypackage-rooms").find(".myroom-hotel-item").remove();
        var code = createRoomHotelPackage(roomCount);
        $(".mypackage-rooms").append(code);


        var wwidth = $(window).width();
        if (wwidth < 575) {
            var wheight = $(window).height();
            var sheight = $('.search').height();
            var height11 = sheight + 200;
            $(".js-height-full").height(height11);
        } else {
            var wheight = $(window).height();
            var sheight = $('.search').height();
            var height1 = wheight - sheight;
            var height = height1 + sheight;
            $(".js-height-full").height(height);
        }
    });
    $('input:radio[name="DOM_TripMode"]').change(function(){
        if (this.checked && this.value == '1') {
            $('.return_input').removeAttr('disabled', '');


        }
        else {
            $('.return_input').attr('disabled', '');
        }
    });
    $('input:radio[name="DOM_TripMode2"]').change(function(){
        if (this.checked && this.value == '1') {
            $('.return_input2').removeAttr('disabled', '');

        }
        else {
            $('.return_input2').attr('disabled', '');
        }
    });
    $('input:radio[name="DOM_TripMode6"]').change(function(){
        if (this.checked && this.value == '1') {
            $('.return_input_train').removeAttr('disabled', '');

        }
        else {
            $('.return_input_train').attr('disabled', '');
        }
    });
    $('input:radio[name="DOM_TripMode4"]').change(function(){
        if (this.checked && this.value == '1') {


            $('#hotel_khareji').css('display','flex');
            $('#hotel_dakheli').hide();


        }
        else {
            $('#hotel_khareji').hide();
            $('#hotel_dakheli').css('display','flex');
        }
    });
    $('input:radio[name="DOM_TripMode8"]').change(function(){
        if (this.checked && this.value == '1') {
            $('#flight_khareji').css('display','flex');
            $('#flight_dakheli').hide();
        }
        else {
            $('#flight_khareji').hide();
            $('#flight_dakheli').css('display','flex');
        }
    });
    $('input:radio[name="DOM_TripMode7"]').change(function(){
        if (this.checked && this.value == '1') {


            $('#transfer_div').css('display','flex');
            $('#gasht_div').hide();


        }
        else {
            $('#transfer_div').hide();
            $('#gasht_div').css('display','flex');
        }
    });
    $('input:radio[name="DOM_TripMode5"]').change(function(){
        if (this.checked && this.value == '1') {


            $('#tour_khareji').css('display','flex');
            $('#tour_dakheli').hide();


        }
        else {
            $('#tour_khareji').hide();
            $('#tour_dakheli').css('display','flex');
        }
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });
    $('.top__user_menu').bind('click', function(e){
        //as when we click inside the menu it bubbles up and closes the menu when it hits html we have to stop the propagation while its open
        e.stopPropagation();

    });
    $('.main-navigation__button').click(function () {

        $('.main-navigation__sub-menu').toggle();
        $('.button-chevron').toggleClass('rotate');

    });
    $('body').click(function () {

        $('.main-navigation__sub-menu').hide();
        $('.button-chevron').removeClass('rotate');

        $('.cbox-count-nafar').hide();
        $(this).parents().find('.down-count-nafar').removeClass('fa-caret-up');
    });
    $('.btn-close').click(function () {
        $('.cbox-count-nafar').hide();
        $(this).parents().find('.down-count-nafar').removeClass('fa-caret-up');

    })
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });
    $('.lang ').bind('click', function(e){
        //as when we click inside the menu it bubbles up and closes the menu when it hits html we have to stop the propagation while its open
        e.stopPropagation();
    });
    $('body').click(function () {
        $('.lang_ul').removeClass('active_lang');
    });
    $('.lang span').click(function () {
        $('.lang_ul').toggleClass('active_lang');
    });
    $('.top__user_menu').bind('click', function(e){
        e.stopPropagation();
    });
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });
    $('.box-of-count-nafar').bind('click', function(e){
        //as when we click inside the menu it bubbles up and closes the menu when it hits html we have to stop the propagation while its open
        e.stopPropagation();

    });
    $('.main-navigation__button').click(function () {

        $('.main-navigation__sub-menu').toggle();
        $('.button-chevron').toggleClass('rotate');

    });
    $('body').click(function () {

        $('.main-navigation__sub-menu').hide();
        $('.button-chevron').removeClass('rotate');

        $('.cbox-count-nafar').hide();
        $(this).parents().find('.down-count-nafar').removeClass('fa-caret-up');
    });
    $('.top__user_menu').bind('click', function(e){
        //as when we click inside the menu it bubbles up and closes the menu when it hits html we have to stop the propagation while its open
        e.stopPropagation();

    });
    $('body').click(function () {
        $('.main-navigation__sub-menu2').hide();
    });
    $('.main-navigation__button2').click(function (e) {
        e.stopPropagation()
    });
    function formatState (state) {
        if (!state.id) {
            return state.text;
        }
        var baseUrl = "/user/pages/images/flags";
        var $state = $(
            '<span class="city_start"><i class="fa fa-map-marker-alt"></i>' + state.text + '</span>'
        );
        return $state;
    };
    $(".select2_in , .select2").select2({
        templateResult: formatState
    });
    $('.multiselectportal').click(function () {
        if ($("input[name='select-rb']:checked").val() == '1') {
            $('.returnCalendar').prop("disabled", "disabled");
        } else {
            $('.returnCalendar').removeAttr("disabled");
        }
    });
    $('.select_multiway').click(function () {
        if ($("input[name='select-rb2']:checked").val() == '1') {
            $('.checktest').prop("disabled", "disabled");
        } else {
            $('.checktest').removeAttr("disabled");
        }
    });
    $('.myroom-hotel-item-title .close').hide();
    $('body').on('click','.btn_add_room', function (e) {
        $('.myroom-hotel-item-title .close').show();


        let roomCount = parseInt($('.myroom-hotel-item').length) ;

        let numberAdult = parseInt($('.number_adult').text() );
        let number_room = parseInt($('.number_room').text() );
        $('.number_adult').text(numberAdult + 1)
        $('.number_room').text(number_room + 1)


        let code = createRoomHotel(roomCount);
        $(".hotel_select_room").append(code);
        if(roomCount ==3){
            $(this).hide();
        }



    });
    $('body').on('click', '.myroom-hotel-item .close', function () {

        let babyCountThis =$(this).parents('.myroom-hotel-item').find('.countChild').val();
        let number_baby = $('.number_baby').text();
        $('.number_baby').text(number_baby - babyCountThis );

        let AdultCountThis =$(this).parents('.myroom-hotel-item').find('.countParent').val();
        let number_adult = $('.number_adult').text();
        $('.number_adult').text(number_adult - AdultCountThis );

        $('.btn_add_room').show();

        let roomNumber = $(this).parents(".myroom-hotel-item").data("roomnumber");
        let roomCount = $(".myroom-hotel-item").length;

        let number_room = parseInt($('.number_room').text());
        $('.number_room').text(number_room - 1)


        $(this).parents(".myroom-hotel-item").remove();
        let countRoom = parseInt($('#countRoom').val()) - 1;
        $("#countRoom option:selected").prop("selected", false);
        $("#countRoom option[value=" + countRoom + "]").prop("selected", true);
        let numberRoom = 1;
        let numberText = "اول";
        $('.myroom-hotel-item').each(function () {
            $(this).data("roomnumber", numberRoom);
            if (numberRoom == 1) {
                numberText = "اول";
            } else if (numberRoom == 2) {
                numberText = "دوم";
            } else if (numberRoom == 3) {
                numberText = "سوم";
            } else if (numberRoom == 4) {
                numberText = "چهارم";
            }
            $(this).find('.myroom-hotel-item-title').html(' اتاق ' + numberText + '<span class="close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg></span>');
            $(this).find(".myroom-hotel-item-info").find("input[name^='adult']").attr("name", "adult" + numberRoom);
            $(this).find(".myroom-hotel-item-info").find("input[name^='adult']").attr("id", "adult" + numberRoom);
            $(this).find(".myroom-hotel-item-info").find("input[name^='child']").attr("name", "child" + numberRoom);
            $(this).find(".myroom-hotel-item-info").find("input[name^='child']").attr("id", "child" + numberRoom);
            let numberChild = 1;
            let inputNameSelectChildAge = $(this).find(".tarikh-tavalods .tarikh-tavalod-item");
            inputNameSelectChildAge.each(function () {
                $(this).find("select[name^='childAge']").attr("name", "childAge" + numberRoom + numberChild);
                $(this).find("select[name^='childAge']").attr("id", "childAge" + numberRoom + numberChild);
                numberChild++;
            });
            numberRoom++;
        });
        if(roomCount == 2){
            $('.close').hide();
        }


    });
    $('body').on('click', 'i.addParent', function () {


        var inputNum = $(this).siblings(".countParent").val();

        if (inputNum < 7) {
            inputNum++;
            let numberAdult =parseInt( $('.number_adult').text());
            let resultNumber = numberAdult + 1
            $(this).siblings(".countParent").val(inputNum);
            $('.number_adult').html('');
            $('.number_adult').append(resultNumber);
        }
    });
    $('body').on('click', 'i.minusParent', function () {

        let data_roomnumber = $(this).parents('.myroom-hotel-item').attr('data-roomnumber');
        let ThiscountParent =  $(this).parents('.myroom-hotel-item').find('.countParent').val();


        var inputNum = $(this).siblings(".countParent").val();

        if (inputNum > 1) {
            inputNum--;
            let numberAdult =parseInt( $('.number_adult').text());
            let resultNumber = numberAdult - 1
            $(this).siblings(".countParent").val(inputNum);
            $('.number_adult').html('');
            $('.number_adult').append(resultNumber);
        }



    });
    $('body').on('click', 'i.addChild', function () {
        var inputNum = $(this).siblings(".countChild").val();
        inputNum++;
        if (inputNum < 5) {
            let numberBaby =parseInt( $('.number_baby').text());
            let numberBabyThis =parseInt($(this).parents().find('.countChild').val()) + 1;

            let resultNumber = numberBaby + 1

            $(this).siblings(".countChild").val(inputNum);
            $('.number_baby').html('');
            $('.number_baby').append(resultNumber);

            $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();

            let roomNumber = $(this).parents(".myroom-hotel-item").data("roomnumber");

            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);

            $(this).parents(".myroom-hotel-item-info").find(".tarikh-tavalods").html(htmlBox);
        }
    });
    $('body').on('click', 'i.minusChild', function () {

        var inputNum = $(this).siblings(".countChild").val();
        $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();

        if (inputNum != 0) {
            let numberBaby =parseInt( $('.number_baby').text());
            let numberBabyThis =parseInt($(this).parents().find('.countChild').val()) + 1;

            let resultNumber = numberBaby - 1

            inputNum--;
            $(this).siblings(".countChild").val(inputNum);
            $('.number_baby').html('');
            $('.number_baby').append(resultNumber);

            let roomNumber = $(this).parents(".myroom-hotel-item").data("roomnumber");

            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);

            $(this).parents(".myroom-hotel-item-info").find(".tarikh-tavalods").html(htmlBox);

        } else {
            $(this).siblings(".countChild").val('0');

        }
    });
    $('.mypackege-rooms').on('click','.btn_add_room_p', function (e) {
        $('.mypackege-rooms .close').show();


        let roomCount = parseInt($('.myroom-package-item').length) ;

        let numberAdult = parseInt($('.number_adult_p').text() );
        let number_room = parseInt($('.number_room_p').text() );
        $('.number_adult_p').text(numberAdult + 1)
        $('.number_room_p').text(number_room + 1)

        let code = createRoomHotelPackage(roomCount);
        $(".package_select_room").append(code);
        if(roomCount ==3){
            $(this).hide();
        }



    });
    $('.mypackege-rooms').on('click', '.myroom-package-item .close', function () {

        let babyCountThis =$(this).parents('.myroom-package-item').find('.countChild_p').val();
        let number_baby = $('.number_baby_p').text();
        $('.number_baby_p').text(number_baby - babyCountThis );

        let AdultCountThis =$(this).parents('.myroom-package-item').find('.countParent_p').val();
        let number_adult = $('.number_adult_p').text();
        $('.number_adult_p').text(number_adult - AdultCountThis );

        $('.btn_add_room_p').show();

        let roomNumber = $(this).parents(".myroom-package-item").data("roomnumber");
        let roomCount = $(".myroom-package-item").length;

        let number_room = parseInt($('.number_room_p').text());
        $('.number_room_p').text(number_room - 1)


        $(this).parents(".myroom-package-item").remove();
        let countRoom = parseInt($('#countRoom').val()) - 1;
        $("#countRoom option:selected").prop("selected", false);
        $("#countRoom option[value=" + countRoom + "]").prop("selected", true);
        let numberRoom = 1;
        let numberText = "اول";
        $('.myroom-package-item').each(function () {
            $(this).data("roomnumber", numberRoom);
            if (numberRoom == 1) {
                numberText = "اول";
            } else if (numberRoom == 2) {
                numberText = "دوم";
            } else if (numberRoom == 3) {
                numberText = "سوم";
            } else if (numberRoom == 4) {
                numberText = "چهارم";
            }
            $(this).find('.myroom-package-item-title').html(' اتاق ' + numberText + '<span class="close"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg></span>');
            $(this).find(".myroom-package-item-info").find("input[name^='adult_p']").attr("name", "adult_p" + numberRoom);
            $(this).find(".myroom-package-item-info").find("input[name^='adult_p']").attr("id", "adult_p" + numberRoom);
            $(this).find(".myroom-package-item-info").find("input[name^='child_p']").attr("name", "child_p" + numberRoom);
            $(this).find(".myroom-package-item-info").find("input[name^='child_p']").attr("id", "child_p" + numberRoom);
            let numberChild = 1;
            let inputNameSelectChildAge = $(this).find(".tarikh-tavalods .tarikh-tavalod-item");
            inputNameSelectChildAge.each(function () {
                $(this).find("select[name^='childAge']").attr("name", "childAge" + numberRoom + numberChild);
                $(this).find("select[name^='childAge']").attr("id", "childAge" + numberRoom + numberChild);
                numberChild++;
            });
            numberRoom++;
        });
        if(roomCount == 2){
            $('.myroom-package-item-title .close').hide();
        }


    });
    $('.mypackege-rooms').on('click', 'i.addParent_p', function () {


        var inputNum = $(this).siblings(".countParent_p").val();

        if (inputNum < 7) {
            inputNum++;
            let numberAdult =parseInt( $('.number_adult_p').text());
            let resultNumber = numberAdult + 1
            $(this).siblings(".countParent_p").val(inputNum);
            $('.number_adult_p').html('');
            $('.number_adult_p').append(resultNumber);
        }
    });
    $('.mypackege-rooms').on('click', 'i.minusParent_p', function () {

        let data_roomnumber = $(this).parents('.myroom-package-item').attr('data-roomnumber');
        let ThiscountParent =  $(this).parents('.myroom-package-item').find('.countParent_p').val();


        var inputNum = $(this).siblings(".countParent_p").val();

        if (inputNum > 1) {
            inputNum--;
            let numberAdult =parseInt( $('.number_adult_p').text());
            let resultNumber = numberAdult - 1
            $(this).siblings(".countParent_p").val(inputNum);
            $('.number_adult_p').html('');
            $('.number_adult_p').append(resultNumber);
        }



    });
    $('.mypackege-rooms').on('click', 'i.addChild_p', function () {

        var inputNum = $(this).siblings(".countChild_p").val();
        inputNum++;
        if (inputNum < 5) {
            let numberBaby =parseInt( $('.number_baby_p').text());
            let numberBabyThis =parseInt($(this).parents().find('.countChild_p').val()) + 1;

            let resultNumber = numberBaby + 1

            $(this).siblings(".countChild_p").val(inputNum);
            $('.number_baby_p').html('');
            $('.number_baby_p').append(resultNumber);

            $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();

            let roomNumber = $(this).parents(".myroom-package-item").data("roomnumber");

            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);

            $(this).parents(".myroom-package-item-info").find(".tarikh-tavalods").html(htmlBox);
        }
    });
    $('.mypackege-rooms').on('click', 'i.minusChild_p', function () {

        var inputNum = $(this).siblings(".countChild_p").val();
        $(this).parents(".child-number").siblings(".child-birthday-box").find(".childAge-button").remove();

        if (inputNum != 0) {
            let numberBaby =parseInt( $('.number_baby_p').text());
            let numberBabyThis =parseInt($(this).parents().find('.countChild_p').val()) + 1;

            let resultNumber = numberBaby - 1

            inputNum--;
            $(this).siblings(".countChild_p").val(inputNum);
            $('.number_baby_p').html('');
            $('.number_baby_p').append(resultNumber);

            let roomNumber = $(this).parents(".myroom-packege-item").data("roomnumber");

            var htmlBox = createBirthdayCalendar(inputNum, roomNumber);

            $(this).parents(".myroom-package-item-info").find(".tarikh-tavalods").html(htmlBox);

        } else {
            $(this).siblings(".countChild_p").val('0');

        }
    });
    $('.mypackege-rooms').on('click', '.close_room', function () {

        $(this).parent().removeClass('active_p');


    });
    $('.myhotels-rooms').on('click', '.close_room', function () {

        $(this).parent().removeClass('active_p');

    });
    function createRoomHotel(roomCount) {

        var HtmlCode = "";
        let i = $('.myroom-hotel-item').length +1;
        let numberText = "اول";
        let valuefirst;


        if (i == 1) {
            numberText = "اول";
            valuefirst = "2"
        } else if (i == 2) {
            numberText = "دوم";
            valuefirst = "1";

        } else if (i == 3) {
            numberText = "سوم";
            valuefirst = "1";

        } else if (i == 4) {
            numberText = "چهارم";
            valuefirst = "1";

        }


        if(i < 5){
            HtmlCode +=
                `<div class="myroom-hotel-item" data-roomNumber="${i}">
             <div class="myroom-hotel-item-title">
            اتاق  ${numberText}
            <span class="close">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg>
            </span>
            </div><div class="myroom-hotel-item-info">
        <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal">
       <h6>بزرگسال</h6>
           (بزرگتر از ۱۲ سال)
        <div><i class="addParent plus-nafar hotelroom-minus plus-hotelroom-bozorgsal fas fa-plus"></i>
        <input readonly class="countParent"  min="0" value="${valuefirst}" max="5" type="number" name="adult${i}" id="adult${i}">
        <i class="minusParent minus-nafar hotelroom-minus minus-hotelroom-bozorgsal fas fa-minus"></i>
        </div>
        </div>
        <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal">
       <h6>کودک</h6>
                                                    (کوچکتر از ۱۲ سال)
        <div>
        <i class="addChild plus-nafar hotelroom-minus plus-hotelroom-koodak fas fa-plus">
        
        </i><input readonly class="countChild" min="0" value="0" max="5" type="number" name="child${i}" id="child${i}">
        <i class="minusChild minus-nafar hotelroom-minus minus-hotelroom-koodak fas fa-minus"></i>
        </div>
        </div><div class="tarikh-tavalods"></div>
        </div>
        </div>`;
        }

        return HtmlCode;
    }
    function createRoomHotelPackage(roomCount) {

        var HtmlCode = "";
        let i = $('.myroom-package-item').length +1;
        let numberText = "اول";
        let valuefirst;


        if (i == 1) {
            numberText = "اول";
            valuefirst = "2"
        } else if (i == 2) {
            numberText = "دوم";
            valuefirst = "1";

        } else if (i == 3) {
            numberText = "سوم";
            valuefirst = "1";

        } else if (i == 4) {
            numberText = "چهارم";
            valuefirst = "1";

        }


        if(i < 5){
            HtmlCode +=
                `<div class="myroom-package-item" data-roomNumber="${i}">
             <div class="myroom-package-item-title">اتاق  ${numberText}
             <span class="close">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M432 64C440.8 64 448 71.16 448 80C448 88.84 440.8 96 432 96H413.7L388.2 452.6C385.9 486.1 357.1 512 324.4 512H123.6C90.01 512 62.15 486.1 59.75 452.6L34.29 96H16C7.164 96 0 88.84 0 80C0 71.16 7.164 64 16 64H111.1L137 22.56C145.8 8.526 161.2 0 177.7 0H270.3C286.8 0 302.2 8.526 310.1 22.56L336.9 64H432zM177.7 32C172.2 32 167.1 34.84 164.2 39.52L148.9 64H299.1L283.8 39.52C280.9 34.84 275.8 32 270.3 32H177.7zM381.6 96H66.37L91.67 450.3C92.87 467 106.8 480 123.6 480H324.4C341.2 480 355.1 467 356.3 450.3L381.6 96z"/></svg>
            </span>
            </div><div class="myroom-package-item-info">
        <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal">
       <h6>بزرگسال</h6>
           (بزرگتر از ۱۲ سال)
        <div><i class="addParent_p plus-nafar hotelroom-minus plus-hotelroom-bozorgsal fas fa-plus"></i>
        <input readonly class="countParent_p"  min="0" value="${valuefirst}" max="5" type="number" name="adultpackage${i}" id="adultpackage${i}">
        <i class="minusParent_p minus-nafar hotelroom-minus minus-hotelroom-bozorgsal fas fa-minus"></i>
        </div>
        </div>
        <div class="myroom-hotel-item-tedad my-room-hotel-bozorgsal">
       <h6>کودک</h6>
                                                    (کوچکتر از ۱۲ سال)
        <div>
        <i class="addChild_p plus-nafar hotelroom-minus plus-hotelroom-koodak fas fa-plus">
        
        </i><input readonly class="countChild_p" min="0" value="0" max="5" type="number" name="childpackage${i}" id="childpackage${i}">
        <i class="minusChild_p minus-nafar hotelroom-minus minus-hotelroom-koodak fas fa-minus"></i>
        </div>
        </div><div class="tarikh-tavalods"></div>
        </div>
        </div>`;
        }

        return HtmlCode;
    }
    function createBirthdayCalendar(inputNum, roomNumber) {
        var i = 1;
        var HtmlCode = "";
        let numberTextChild = "سلام";
        while (i <= inputNum) {
            if (i == 1) {
                numberTextChild = "اول";
            } else if (i == 2) {
                numberTextChild = "دوم";
            } else if (i == 3) {
                numberTextChild = "سوم";
            } else if (i == 4) {
                numberTextChild = "چهارم";
            }
            HtmlCode += '<div class="tarikh-tavalod-item">'
                + '<span>سن کودک <i>' + numberTextChild + '</i></span>'
                + '<select id="childAge' + roomNumber + i + '" name="childAge' + roomNumber + i + '">'
                + '<option value="1">0 تا 1 سال</option>'
                + '<option value="2">1 تا 2 سال</option>'
                + '<option value="3">2 تا 3 سال</option>'
                + '<option value="4">3 تا 4 سال</option>'
                + '<option value="5">4 تا 5 سال</option>'
                + '<option value="6">5 تا 6 سال</option>'
                + '<option value="7">6 تا 7 سال</option>'
                + '<option value="8">7 تا 8 سال</option>'
                + '<option value="9">8 تا 9 سال</option>'
                + '<option value="10">9 تا 10 سال</option>'
                + '<option value="11">10 تا 11 سال</option>'
                + '<option value="12">11 تا 12 سال</option>'
                + '</select>'
                + '</div>';
            i++;
        }
        return HtmlCode;
    };
    // search
});