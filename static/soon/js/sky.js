// JavaScript Document


// screen loader
$(window).load(function() {
    "use strict";
    $('.screen-loader').fadeOut('slow');
});


// preload
$(document).ready(function() {
    "use strict";
    $('#preload').css({
        display: 'table'
    });
});


// preload function
$(window).load(preLoader);
"use strict";

function preLoader() {
    setTimeout(function() {
        $('#preload').delay(250).fadeOut(250);
        $('.borders').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('#intro-wrapper').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('.menu').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('.menu-mobile').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('#countdown-wrapper').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('#subscribe-form').delay(250).css({
            display: 'none'
        }).fadeIn(250);
        $('.social-icons-wrapper').delay(250).css({
            display: 'none'
        }).fadeIn(250);
    });
};


// snow
var $ = jQuery.noConflict();
jQuery(function($) {
    "use strict";
    $("#snow").each(function() {
        snowBind();
    });
});


function fire_delayed_load(e, name) {
    $(name).removeClass("current");
    e.preventDefault();
    $(".current").fadeOut(250, function() {
        $(name).fadeIn(250);
        $(".current").removeClass("current");
        $(name).addClass("current");
    });
}

// fire
$(document).ready(function() {
    "use strict";
    // fire home
    $("#fire-home").click(function(e) {
        fire_delayed_load(e, ".upper-page");
    });
    // fire about
    $("#fire-about").click(function(e) {
        fire_delayed_load(e, "#about");
    });
    // fire services
    $("#fire-services").click(function(e) {
        fire_delayed_load(e, "#services");
    });
    // fire contact
    $("#fire-contact").click(function(e) {
        fire_delayed_load(e, "#contact");
    });
    // fire home mobile
    $("#fire-home-mobile").click(function(e) {
        fire_delayed_load(e, ".upper-page");
    });
    // fire about mobile
    $("#fire-about-mobile").click(function(e) {
        fire_delayed_load(e, "#about");
    });
    // fire services mobile
    $("#fire-services-mobile").click(function(e) {
        fire_delayed_load(e, "#services");
    });
    // fire contact mobile
    $("#fire-contact-mobile").click(function(e) {
        fire_delayed_load(e, "#contact");
    });
    // fire closer
    $("#fire-about-closer, #fire-services-closer, #fire-contact-closer").click(function(e) {
        fire_delayed_load(e, ".upper-page");
    });
});


// menu active state
$('a.menu-state').click(function() {
    "use strict";
    $('a.menu-state').removeClass("active");
    $(this).addClass("active");
});


// niceScroll
$(document).ready(function() {
    "use strict";
    $("body").niceScroll({
        cursorcolor: "#fff",
        cursorwidth: "5px",
        cursorborder: "1px solid #fff",
        cursorborderradius: "0px",
        zindex: "9999",
        scrollspeed: "60",
        mousescrollstep: "40"
    });
});


// niceScroll || scrollbars resize
$("body").getNiceScroll().resize();


// teaser
$(window).load(function() {
    "use strict";
    var tid = setInterval(animateTeaser, 4000);
    var animCount = 0;

    function animateTeaser() {
        animCount++;
        if (animCount > 3) {
            animCount = 0;
            $('.teaser-text-animation.active').fadeTo(300, 0, function() {
                $('.teaser-text-animation').removeClass('active');
                $('.teaser-text-animation').removeClass('first');
                $('.teaser-normal').css({
                    marginTop: '100px'
                });
                $('.teaser-highlight').css({
                    marginTop: '-100px'
                });
                $('.teaser-text-animation:first').addClass('active').fadeTo(300, 1, function() {
                    $('.teaser-normal, .teaser-highlight, .teaser-text-animation:first').each(function(wordCount) {
                        $(this).animate({
                            marginTop: 0
                        }, {
                            duration: 400,
                            queue: false
                        });
                    });
                });
            });
        } else {
            var nextAnim = $('.teaser-text-animation').get(animCount);
            $('.teaser-text-animation.active').fadeTo(300, 0, function() {
                $('.teaser-text-animation').removeClass('active');
                $('.teaser-normal').css({
                    marginTop: '100px'
                });
                $('.teaser-highlight').css({
                    marginTop: '-100px'
                });
                $(nextAnim).addClass('active').fadeTo(300, 1, function() {
                    $('.teaser-normal, .teaser-highlight', nextAnim).each(function(wordCount) {
                        $(this).animate({
                            marginTop: 0
                        }, {
                            duration: 400,
                            queue: false
                        });
                    });
                });
            });
        }
    }
});


// mobile-detect
var isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};