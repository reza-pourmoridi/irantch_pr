let percentage = 20;
let NumberOfInstallments = 4;
function plus_box_percentage(e){
    if (percentage < 100 ){
    e.currentTarget.parentNode.querySelector('span').innerText = percentage + 10 + '%';
    percentage = percentage + 10;
    }
}
function minus_box_percentage(e){
    if (percentage > 20 ){
        e.currentTarget.parentNode.querySelector('span').innerText = percentage - 10 + '%';
        percentage = percentage - 10;
    }
}
function plus_box_NumberOfInstallments(e){
    if (NumberOfInstallments < 12 ) {
        e.currentTarget.parentNode.querySelector('span').innerText = NumberOfInstallments + 1;
        NumberOfInstallments = NumberOfInstallments + 1;
    }
}
function minus_box_NumberOfInstallments(e){
    if (NumberOfInstallments > 4 ) {
        e.currentTarget.parentNode.querySelector('span').innerText = NumberOfInstallments - 1;
        NumberOfInstallments = NumberOfInstallments - 1;
    }
}
function AdvancedInstallmentCalculatorBtn(){
    $(".AdvancedInstallmentCalculatorBox").toggle();
    $(".AdvancedInstallmentCalculatorBtn__open").toggle();
    $(".AdvancedInstallmentCalculatorBtn__close").toggle();
    $(".AdvancedInstallmentCalculatorBox_response_hide").hide();
}
function Main_AdvancedInstallmentCalculatorBtn(){
    $(".AdvancedInstallmentCalculatorBox_response_hide").show();
}
function formatPrice() {
    let priceInput = document.getElementById('priceInput');
    let price = priceInput.value.replace(/\D/g, '');
    if (!isNaN(price)) {
        let formattedPrice = price.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        priceInput.value = formattedPrice;
    }
}
$(document).ready(function () {
    $(".anAmount_btn").click(() => {
        $(".percentage").hide()
        $(".anAmount").show()
        $(".anAmount_btn").addClass("active")
        $(".percentage_btn").removeClass("active")
    })
    $(".percentage_btn").click(() => {
        $(".percentage").show()
        $(".anAmount").hide()
        $(".percentage_btn").addClass("active")
        $(".anAmount_btn").removeClass("active")
    })


    $('[data-rangeslider]').rangeslider({
        polyfill:false,
        rangeClass:'rangeslider',
        disabledClass:'rangeslider--disabled',
        activeClass:'rangeslider--active',
        horizontalClass:'rangeslider--horizontal',
        verticalClass:'rangeslider--vertical',
        fillClass:'rangeslider__fill',
        handleClass:'rangeslider__handle',
        onSlide:function(position, value) {
            console.log("onSlide" , position , value);
            $(".div-rangeslider > h6").text(value)
        }
    });
    $('[data-rangeslider2]').rangeslider({
        polyfill:false,
        rangeClass:'rangeslider',
        disabledClass:'rangeslider--disabled',
        activeClass:'rangeslider--active',
        horizontalClass:'rangeslider--horizontal',
        verticalClass:'rangeslider--vertical',
        fillClass:'rangeslider__fill',
        handleClass:'rangeslider__handle',
        onSlide:function(position, value) {
            console.log("onSlide" , position , value)
            $(".div-rangeslider2 > h6").text(value)
        }
    });

    $('.owl-tour').owlCarousel({
        loop:true,
        rtl:true,
        margin:30,
        navText: ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M166.5 424.5l-143.1-152c-4.375-4.625-6.562-10.56-6.562-16.5c0-5.938 2.188-11.88 6.562-16.5l143.1-152c9.125-9.625 24.31-10.03 33.93-.9375c9.688 9.125 10.03 24.38 .9375 33.94l-128.4 135.5l128.4 135.5c9.094 9.562 8.75 24.75-.9375 33.94C190.9 434.5 175.7 434.1 166.5 424.5z"/></svg>','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M89.45 87.5l143.1 152c4.375 4.625 6.562 10.56 6.562 16.5c0 5.937-2.188 11.87-6.562 16.5l-143.1 152C80.33 434.1 65.14 434.5 55.52 425.4c-9.688-9.125-10.03-24.38-.9375-33.94l128.4-135.5l-128.4-135.5C45.49 110.9 45.83 95.75 55.52 86.56C65.14 77.47 80.33 77.87 89.45 87.5z"/></svg>'],
        nav:true,
        dots:true,
        autoplay:true,
        autoplayTimeout:3500,
        autoplayHoverPause:true,
        responsive:{
            0:{
                items:1
            },
            992:{
                items:2
            },
            1000:{
                items:2
            },
            1200:{
                items:3
            }
        },
    });
    $('.owl-custom').owlCarousel({
        loop:false,
        rtl:true,
        margin:30,
        navText: ["<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 512\"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d=\"M166.5 424.5l-143.1-152c-4.375-4.625-6.562-10.56-6.562-16.5c0-5.938 2.188-11.88 6.562-16.5l143.1-152c9.125-9.625 24.31-10.03 33.93-.9375c9.688 9.125 10.03 24.38 .9375 33.94l-128.4 135.5l128.4 135.5c9.094 9.562 8.75 24.75-.9375 33.94C190.9 434.5 175.7 434.1 166.5 424.5z\"/></svg>","<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 512\"><!--! Font Awesome Pro 6.1.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d=\"M89.45 87.5l143.1 152c4.375 4.625 6.562 10.56 6.562 16.5c0 5.937-2.188 11.87-6.562 16.5l-143.1 152C80.33 434.1 65.14 434.5 55.52 425.4c-9.688-9.125-10.03-24.38-.9375-33.94l128.4-135.5l-128.4-135.5C45.49 110.9 45.83 95.75 55.52 86.56C65.14 77.47 80.33 77.87 89.45 87.5z\"/></svg>"],
        nav:false,
        dots:true,
        autoplay:true,
        autoplayTimeout:3500,
        autoplayHoverPause:true,
        responsive:{
            0:{
                items:1
            },
            992:{
                items:2
            },
            1000:{
                items:2
            },
            1200:{
                items:4
            }
        },
    });
});