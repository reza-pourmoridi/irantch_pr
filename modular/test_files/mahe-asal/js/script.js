$('.owl-banner-kanoun').owlCarousel({
    rtl:true,
    loop:true,
    margin:0,
    nav:true,
    navText: ["<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\"><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d=\"M7 239c-9.4 9.4-9.4 24.6 0 33.9L143 409c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-95-95L488 280c13.3 0 24-10.7 24-24s-10.7-24-24-24L81.9 232l95-95c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0L7 239z\"/></svg>","<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\"><!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d=\"M505 273c9.4-9.4 9.4-24.6 0-33.9L369 103c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l95 95L24 232c-13.3 0-24 10.7-24 24s10.7 24 24 24l406.1 0-95 95c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0L505 273z\"/></svg>"],
    autoplay: true,
    autoplayTimeout:5000,
    autoplayHoverPause:true,
    dots:false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});
$('.owl-tablighat').owlCarousel({
    rtl:true,
    loop:true,
    margin:10,
    nav:false,
    autoplay: false,
    autoplayTimeout: 7000,
    autoplaySpeed:3000,
    dots:false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});


particlesJS("particles-js", {
    particles: {
        number: {
            value: 200,
            density: {
                enable: true,
                value_area: 800,
            },
        },
        color: {
            value: "#f0c394",
        },
        opacity: {
            value: 0.4,
            random: false,
            anim: {
                enable: false,
                speed: 1,
                opacity_min: 0.1,
                sync: false,
            },
        },
        size: {
            value: 3,
            random: true,
            anim: {
                enable: false,
                speed: 40,
                size_min: 0.1,
                sync: false,
            },
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: "#eee",
            opacity: 0.3,
            width: 1,
        },
        move: {
            enable: true,
            speed: 0.5,
            direction: "none",
            random: false,
            straight: false,
            out_mode: "out",
            bounce: false,
            attract: {
                enable: false,
                rotateX: 600,
                rotateY: 1200,
            },
        },
    },
    retina_detect: true,
});



$('.tour-owl').owlCarousel({
    rtl:true,
    loop:true,
    margin:20,
    nav:false,
    navText: ["<span class=\"fa-sharp fa-regular fa-arrow-right\"></span>","<span class=\"fa-regular fa-arrow-left\"></span>"],
    autoplay: true,
    autoplayTimeout: 8000,
    autoplaySpeed:5000,
    dots:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:4
        }
    }
});
function clickScroll(e){
    $("html").animate({
        scrollTop: $(`#${e}`).offset().top - 30
    }, 1000);
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$(".select2").select2();


// hide #back-top first
$("#scroll-top").addClass('d-none');
// fade in #back-top
$(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#scroll-top').addClass('d-flex');
            $('#scroll-top').removeClass('d-none');
        } else {
            $('#scroll-top').removeClass('d-flex');
            $('#scroll-top').addClass('d-none');
        }
    });
    // scroll body to 0px on click
    $('#scroll-top').click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 800);
    });
});


$(document).ready(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.bottom-header').addClass('scrolled');
        } else {
            $('.bottom-header').removeClass('scrolled');
        }
    });
});
