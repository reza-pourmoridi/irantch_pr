$(".nimcal").select2({
});
/****************/
$('#owl1').owlCarousel({
    loop:true,
    center:true,
    rtl:true,
    margin:10,
    nav:false,
    dots: true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:5
        }
    }
});
/****************/
$('#owl2').owlCarousel({
    loop:true,
    center:true,
    rtl:true,
    margin:10,
    nav:false,
    dots: true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:5
        }
    }
});
/*******************/
$('#owl3').owlCarousel({
    loop:true,
    center:false,
    rtl:true,
    margin:10,
    nav:false,
    dots: true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:3
        }
    }
});
/***********************/
$('#owl4').owlCarousel({
    loop:true,
    center:false,
    rtl:true,
    margin:15,
    nav:false,
    dots: true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:4
        }
    }
});
/***************************************/
$('#owl5').owlCarousel({
    loop:true,
    center:true,
    rtl:true,
    margin:10,
    nav:false,
    dots: false,
    responsive:{
        0:{
            items:3
        },
        600:{
            items:5
        },
        1000:{
            items:9
        }
    }
});
/************filter toor***************/
$('#toordakheli').click(function () {
    $('#toordakheli').addClass('nimspstylebanafsh');
    $('#toorkhareji').removeClass('nimspstylebanafsh');
    $('#owl2').css('display','none');
    $('#owl1').css('display','block');
});
$('#toorkhareji').click(function () {
    $('#toorkhareji').addClass('nimspstylebanafsh');
    $('#toordakheli').removeClass('nimspstylebanafsh');
    $('#owl2').css('display','block');
    $('#owl1').css('display','none');
});
/*******************menu hamberger***********************/
$("#nimbar").click(function(){
    $(".nimitemhamb").slideToggle();
});
$('#parvaz').click(function () {
    $('.pacc .pavazdakheli').slideToggle();
    $('.pacc .radio').slideToggle();
});
$('#hotel').click(function () {
    $('.pacc .hotel').slideToggle();
});
$('#toor').click(function () {
    $('.pacc .toordakheli').slideToggle();
    $('.pacc .btntoor').slideToggle();
});
$('#bime').click(function () {
    $('.pacc .bime').slideToggle();
});
$('#gasht').click(function () {
    $('.pacc .gasht').slideToggle();
    $('.pacc .btngasht').slideToggle();
});
function myFunction2(x) {
    x.classList.toggle("change");
}
/***********search box******************/
$('#hotelha').click(function () {
    $('.hotel').css('display','flex');
    $('#hotel').addClass('nimsearchitemclick');
    $(".radio,.pavazdakheli,.pavazkhareji,.toordakheli,.toorkhareji,.btntoor,.bime,.btngasht,.gasht,.trans").css('display','none');
    $('.btngasht').css('display','none');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#toor').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');

})
$('.nimdakhel').click(function () {
    $('.nimdakhel>div').addClass('abi');
    $('.nimkharej>div').removeClass('abi');
    $('.pavazdakheli').css('display','flex');
    $('.pavazkhareji').css('display','none');
});
$('.nimkharej').click(function () {
    $('.nimkharej>div').addClass('abi');
    $('.nimdakhel>div').removeClass('abi');
    $('.pavazkhareji').css('display','flex');
    $('.pavazdakheli').css('display','none');
});
$('.nimdakhel2').click(function () {
    $('.nimdakhel2>div').addClass('abi');
    $('.nimkharej2>div').removeClass('abi');
    $('.toordakheli').css('display','flex');
    $('.toorkhareji').css('display','none');
});
$('.nimkharej2').click(function () {
    $('.nimkharej2>div').addClass('abi');
    $('.nimdakhel2>div').removeClass('abi');
    $('.toorkhareji').css('display','flex');
    $('.toordakheli').css('display','none');
});
$('.nimdakhel3').click(function () {
    $('.nimdakhel3>div').addClass('abi');
    $('.nimkharej3>div').removeClass('abi');
    $('.gasht').css('display','flex');
    $('.trans').css('display','none');
});
$('.nimkharej3').click(function () {
    $('.nimkharej3>div').addClass('abi');
    $('.nimdakhel3>div').removeClass('abi');
    $('.trans').css('display','flex');
    $('.gasht').css('display','none');
});
$("#yek").click(function(){
    $('.bargasht2').css('display','none');
    $(".bargasht").css('display','block');
});
$("#do").click(function(){
    $('.bargasht').css('display','none');
    $(".bargasht2").css('display','block');
});
$("#yek2").click(function(){
    $('.bargasht2').css('display','none');
    $(".bargasht").css('display','block');
});
$("#do2").click(function(){
    $('.bargasht').css('display','none');
    $(".bargasht2").css('display','block');
});
$('#parvaz').click(function () {
    $('#parvaz').addClass('nimsearchitemclick');
    $('#toor').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.radio').css('display', 'flex');
    $('.pavazdakheli').css('display','flex');
    $('.btngasht').css('display','none');
    $('.nimdakhel>div').addClass('abi');
    $('.nimkharej>div').removeClass('abi');
    $(".pavazkhareji,.hotel,.toordakheli,.toorkhareji,.btntoor,.bime,.btngasht,.gasht,.trans").css('display','none');

});

$('#toor').click(function () {
    $('#toor').addClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.radio').css('display', 'none');
    $('.toordakheli').css('display','flex');
    $('.nimdakhel2>div').addClass('abi');
    $('.nimkharej2>div').removeClass('abi');
    $('.btntoor').css('display','flex');
    $(".pavazkhareji,.hotel,.pavazdakheli,.toorkhareji,.bime,.btngasht,.gasht,.trans").css('display','none');
});
$('#bime').click(function () {
    $('#bime').addClass('nimsearchitemclick');
    $('#toor').removeClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.bime').css('display','flex');
    $('.btntoor').css('display','none');
    $('.radio').css('display', 'none');
    $(".pavazkhareji,.hotel,.pavazdakheli,.toorkhareji,.toordakheli,.btngasht,.gasht,.trans").css('display','none');
});
$('#gasht').click(function () {
    $('#gasht').addClass('nimsearchitemclick');
    $('#toor').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.btngasht').css('display','flex');
    $('.btntoor').css('display','none');
    $('.radio').css('display', 'none');
    $('.gasht').css('display','flex');
    $('.nimdakhel3>div').addClass('abi');
    $('.nimkharej3>div').removeClass('abi');
    $(".pavazkhareji,.hotel,.pavazdakheli,.toorkhareji,.toordakheli,.bime,.trans").css('display','none');
});
$('#hotel').click(function () {
    $('#hotel').addClass('nimsearchitemclick');
    $('#toor').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('.radio').css('display', 'none');
    $('.hotel').css('display','flex');
    $(".pavazdakheli,.pavazkhareji,.toordakheli,.toorkhareji,.btntoor,.bime,.btngasht,.gasht,.trans").css('display','none');
});
$('.number_of_passengers').on('change', function (e) {
    var itemInsu = $(this).val();
    itemInsu++;
    var HtmlCode = "";
    $(".nafaratbime").html('');
    var i = 1;
    while (i < itemInsu) {

        HtmlCode += "<div class='d-flex justify-content-center nafarat-bime flex-lg-nowrap flex-wrap' style=' margin-top: 25px'>" +
            "<input placeholder='تولد مسافر" +i+ "' type='text' name='txt_birth_insurance" + i + "' id='txt_birth_insurance" + i + "' class=' niminput2 niminput3 nimbtnnafarat' style='padding: 5px' />" +
            "</div>";
        i++;

    }
    $(".nafaratbime ").append(HtmlCode);
});
$('.dakhelitordrop').click(function () {
    $('#toor').addClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.toordakheli').css('display','flex');
    $('.nimdakhel2>div').addClass('abi');
    $('.nimkharej2>div').removeClass('abi');
    $('.btntoor').css('display','flex');
    $('.radio').css('display', 'none');
    $(".pavazkhareji,.hotel,.pavazdakheli,.toorkhareji,.bime,.btngasht,.gasht,.trans").css('display','none');

});
$('.kharejitordrop').click(function () {
    $('#toor').addClass('nimsearchitemclick');
    $('#parvaz').removeClass('nimsearchitemclick');
    $('#bime').removeClass('nimsearchitemclick');
    $('#gasht').removeClass('nimsearchitemclick');
    $('#hotel').removeClass('nimsearchitemclick');
    $('.toorkhareji').css('display','flex');
    $('.nimdakhel2>div').removeClass('abi');
    $('.nimkharej2>div').addClass('abi');
    $('.btntoor').css('display','flex');
    $('.radio').css('display', 'none');
    $(".pavazkhareji,.hotel,.pavazdakheli,.toordakheli,.bime,.btngasht,.gasht,.trans").css('display','none');
});


/***************fiterslider5**************************/
$('#nimfilter0').click(function () {
    $('#nimfilter0').addClass('activfilter');
    $('#nimfilter1,#nimfilter2,#nimfilter3,#nimfilter4,#nimfilter5').removeClass('activfilter');
    $('.iran').css('display','flex');
    $('.moarefi').css('display','flex');
    $('.etelaat').css('display','flex');
    $('.akhbar').css('display','flex');
    $('.sayer').css('display','flex');
});
$('#nimfilter1').click(function () {
      $('#nimfilter1').addClass('activfilter');
      $('#nimfilter0,#nimfilter2,#nimfilter3,#nimfilter4,#nimfilter5').removeClass('activfilter');
      $('.iran').css('display','flex');
      $('.moarefi').css('display','none');
      $('.etelaat').css('display','none');
      $('.akhbar').css('display','none');
      $('.sayer').css('display','none');
});
$('#nimfilter2').click(function () {
    $('#nimfilter2').addClass('activfilter');
    $('#nimfilter0,#nimfilter1,#nimfilter3,#nimfilter4,#nimfilter5').removeClass('activfilter');
    $('.moarefi').css('display','flex');
    $('.iran').css('display','none');
    $('.etelaat').css('display','none');
    $('.akhbar').css('display','none');
    $('.sayer').css('display','none');
});
$('#nimfilter3').click(function () {
    $('#nimfilter3').addClass('activfilter');
    $('#nimfilter0,#nimfilter2,#nimfilter1,#nimfilter4,#nimfilter5').removeClass('activfilter');
    $('.etelaat').css('display','flex');
    $('.iran').css('display','none');
    $('.moarefi').css('display','none');
    $('.akhbar').css('display','none');
    $('.sayer').css('display','none');

});
$('#nimfilter4').click(function () {
    $('#nimfilter4').addClass('activfilter');
    $('#nimfilter0,#nimfilter2,#nimfilter3,#nimfilter1,#nimfilter5').removeClass('activfilter');
    $('.akhbar').css('display','flex');
    $('.iran').css('display','none');
    $('.etelaat').css('display','none');
    $('.moarefi').css('display','none');
    $('.sayer').css('display','none');
});
$('#nimfilter5').click(function () {
    $('#nimfilter5').addClass('activfilter');
    $('#nimfilter0,#nimfilter2,#nimfilter3,#nimfilter1,#nimfilter4').removeClass('activfilter');
    $('.sayer').css('display','flex');
    $('.akhbar').css('display','none');
    $('.iran').css('display','none');
    $('.etelaat').css('display','none');
    $('.moarefi').css('display','none');
});
/****************menu langari*************/
$(document).ready(function(){
    // Add smooth scrolling to all links
    $(".langar").on('click', function(event) {

        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){

                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });
        } // End if
    });
});



