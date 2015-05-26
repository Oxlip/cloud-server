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
        $('#preload').delay(250).fadeOut(1500);
        $('.borders').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('#intro-wrapper').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('.menu').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('.menu-mobile').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('#countdown-wrapper').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('#subscribe-form').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
        $('.social-icons-wrapper').delay(2000).css({
            display: 'none'
        }).fadeIn(3000);
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


// fire
$(document).ready(function() {
    "use strict";
    // fire home
    $("#fire-home").click(function(e) {
        e.preventDefault();
		$(".current").fadeOut( 900, function() {
			$( ".upper-page" ).fadeIn( 900 );
            $(".current").removeClass("current");
            $(".upper-page").addClass("current");
        });
    });
    // fire about
    $("#fire-about").click(function(e) {
        e.preventDefault();
		$(".current").fadeOut( 900, function() {
			$( "#about" ).fadeIn( 900 );
            $(".current").removeClass("current");
            $("#about").addClass("current");
        });
    });
    // fire services
    $("#fire-services").click(function(e) {
        e.preventDefault();
		$(".current").fadeOut( 900, function() {
			$( "#services" ).fadeIn( 900 );
            $(".current").removeClass("current");
            $("#services").addClass("current");
        });
    });
    // fire contact
    $("#fire-contact").click(function(e) {
        e.preventDefault();
		$(".current").fadeOut( 900, function() {
			$( "#contact" ).fadeIn( 900 );
            $(".current").removeClass("current");
            $("#contact").addClass("current");
        });
    });
    // fire home mobile
    $("#fire-home-mobile").click(function(e) {
        e.preventDefault();
        $(".current").fadeOut( 900, function() {
            $(".upper-page").fadeIn( 900 );
            $(".current").removeClass("current");
            $(".upper-page").addClass("current");
        });
    });
    // fire about mobile
    $("#fire-about-mobile").click(function(e) {
        e.preventDefault();
        $(".current").fadeOut( 900, function() {
            $("#about").fadeIn( 900 );
            $(".current").removeClass("current");
            $("#about").addClass("current");
        });
    });
    // fire services mobile
    $("#fire-services-mobile").click(function(e) {
        e.preventDefault();
        $(".current").fadeOut( 900, function() {
            $("#services").fadeIn( 900 );
            $(".current").removeClass("current");
            $("#services").addClass("current");
        });
    });
    // fire contact mobile
    $("#fire-contact-mobile").click(function(e) {
        e.preventDefault();
        $(".current").fadeOut( 900, function() {
            $("#contact").fadeIn( 900 );
            $(".current").removeClass("current");
            $("#contact").addClass("current");
        });
    });
    // fire closer
    $("#fire-about-closer, #fire-services-closer, #fire-contact-closer").click(function(e) {
        e.preventDefault();
		$(".current").fadeOut( 900, function() {
			$( ".upper-page" ).fadeIn( 900 );
            $(".current").removeClass("current");
            $(".upper-page").addClass("current");
        });
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