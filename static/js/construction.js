/*global $, jQuery, document, window, navigator*/
/* ==========================================================================
Document Ready Function
========================================================================== */
jQuery(document).ready(function () {

    'use strict';

    var WindowsHeight, HomeSectionContainer, CalcMarginTop, formInput, sformInput, onMobile;

    /* ==========================================================================
    Modify Copied Text
    ========================================================================== */
    function addLink() {
        var body_element, selection, pagelink, copytext, newdiv;
        body_element = document.getElementsByTagName('body')[0];
        selection = window.getSelection();
        pagelink = " Read more at: <a href='" + document.location.href + "'>" + document.location.href + "</a>";
        copytext = selection + pagelink;
        newdiv = document.createElement('div');
        newdiv.style.position = 'absolute';
        newdiv.style.left = '-99999px';
        body_element.appendChild(newdiv);
        newdiv.innerHTML = copytext;
        selection.selectAllChildren(newdiv);
        window.setTimeout(function () {
            body_element.removeChild(newdiv);
        }, 0);
    }
    document.oncopy = addLink;


    /* ==========================================================================
    Home Section Height
    ========================================================================== */
    WindowsHeight = $(window).height();
    HomeSectionContainer = $('#home-section-container').height();
    CalcMarginTop = (WindowsHeight - HomeSectionContainer) / 2;

    $('#home-section').css({height: WindowsHeight});
    $('#home-section-container').css({top: CalcMarginTop });


    /* ==========================================================================
    CountDown Timer
    ========================================================================== */
    $('#countdown_dashboard').countDown({
        targetDate: {
            'day': 1,
            'month': 11,
            'year': 2014,
            'hour': 0,
            'min': 0,
            'sec': 0
        },
        omitWeeks: true
    });

    $("a[data-rel=tooltip]").tooltip({container: 'body'});


    /* ==========================================================================
    on mobile?
    ========================================================================== */
	onMobile = false;
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) { onMobile = true; }

	if (onMobile === true) {
        $("a[data-rel=tooltip]").tooltip('destroy');
        jQuery('#team-section').css("background-attachment", "scroll");
    }
}); // JavaScript Document


/* ==========================================================================
Window Resize
========================================================================== */
$(window).resize(function () {

    'use strict';

    var WindowsHeight, HomeSectionContainer, CalcMarginTop;

    /* ==========================================================================
    Home Section Height
    ========================================================================== */
    WindowsHeight = $(window).height();
    HomeSectionContainer = $('#home-section-container').height();
    CalcMarginTop = (WindowsHeight - HomeSectionContainer) / 2;

    $('#home-section').css({height: WindowsHeight});
    $('#home-section-container').css({top: CalcMarginTop });

});




/* ==========================================================================
Window Load
========================================================================== */
jQuery(window).load(function () {

    'use strict';

    /* ==============================================
    Loader
    =============================================== */
    var LoaderDelay = 350,
        LoaderFadeOutTime = 800;

    function hideLoader() {
        var loadingLoader = $('#Loader');
        loadingLoader.fadeOut();
    }
    hideLoader();

    /* ==========================================================================
    Funny Text
    ========================================================================== */
    $('#welcome-msg').funnyText({
        speed: 500,
        fontSize: '2em',
        color: '#ffffff',
        activeColor: '#f1c40f',
        borderColor: 'none'
    });

});

/**
 * funnyText.js 0.3 Beta
 * https://github.com/alvarotrigo/funnyText.js
 * MIT licensed
 *
 * Copyright (C) 2013 alvarotrigo.com - A project by Alvaro Trigo
 */

(function($){
    $.fn.funnyText = function(options){
        
        // Create some defaults, extending them with any options that were provided
        options = $.extend({
            'speed': 700,
            'borderColor': 'black',
            'activeColor': 'white',
            'color': 'black',
            'fontSize': '7em',
            'direction': 'both'
        }, options);

        var that = $(this);
        
        that.addClass('funnyText');
        
        var original = $(this);
        var characters = $.trim(original.text()).split('');
        
        
        var positionsY = ['top', 'bottom'];
        var positionsX = ['left', 'right'];

        var activePositionX, activePositionY, normalPositionX, normalPositionY;
        var previousPosition;

        //removing the original text
        original.html('');

        //append the CSS styles
        var style = $('<style>'+that.selector +'.funnyText span.active { color: ' + options.activeColor + '; text-shadow: -1px 0 '+options.borderColor+', 0 1px '+options.borderColor+', 1px 0 '+options.borderColor+', 0 -1px '+options.borderColor+';} '+that.selector +'.funnyText span{color: ' + options.color +'; font-size:' + options.fontSize + ';}</style>')
        $('html > head').append(style);


        //for each character
        for (var i = 0; i < characters.length; i++){
            normalPositionY = positionsY[getRandom(0, 100) % 2];
            normalPositionX = positionsX[getRandom(0, 100) % 2];

            if(characters[i]  == ' '){
                characters[i] = '&nbsp;';
            }
            
            var visibleChar = '<span class="normal  ' + normalPositionY + ' ' + normalPositionX + '">' + characters[i] + '</span>';

            //avoid repeating the same values two consecutive letters 
            do{
                activePositionXY = getNewPosition(normalPositionX, normalPositionY);
            }while(activePositionXY == previousPosition && options.direction == 'both');

            previousPosition = activePositionXY;

            var activeChar = '<span class="active ' + activePositionXY + '">' + characters[i] + '</span>';

            var newChar = '<div class="charWrap">' + visibleChar + activeChar + '</div>';
            original.append(newChar);
        };

        
        //setting the width and height of each character to its wrapper
        that.find('.charWrap').each(function (){
            var sizeX = $(this).find('span').width();
            var sizeY = $(this).find('span').height();
        
            $(this).css({
                'width': sizeX * 2 + 'px',
                'height': sizeY * 2 + 'px'
            });

            //adjusting the wrappers positions
            setMargin($(this));

            //creating the "viewport" for each character. 
            $(this).wrap('<div class="character" style="width:' + sizeX + 'px; height: ' + sizeY + 'px"></div>');
        });


        /**
        * Returnsn a random number between two values.
        */
        function getRandom(from, to){
            return from + Math.floor(Math.random() * (to +1));
        }

        
        /**
        * Gets a new position for the active character in a way it can be scrolled 
        * vertically or horizontally from the position of the original character.
        * (from top left to botom right wouldn't work, for example)
        */
        function getNewPosition(x, y){
            var result;
            
            if((getRandom(0, 100) % 2 && options.direction == 'both') || options.direction == 'horizontal') {
                if(x == "right" && y == "top"){
                    result = "left top moveLeft";
                } else if(x == "right" && y == "bottom"){
                    result = "left bottom moveLeft";
                } else if(x == "left" && y == "top"){
                    result = "right top moveRight";
                } else if(x == "left" && y == "bottom"){
                    result = "right bottom moveRight";
                }
            }else{
                if(x == "right" && y == "top"){
                    result = "right bottom moveDown";
                } else if(x == "right" && y == "bottom"){
                    result = "right top moveUp";
                } else if(x == "left" && y == "top"){
                    result = "left bottom moveDown";
                } else if(x == "left" && y == "bottom"){
                    result = "left top moveUp";
                }
            }

            return result;
        }

        
        /**
        * Sets the margin for the characters container depending on the position 
        * of the characters to show.
        */
        function setMargin(obj){
            if(obj.find('.normal').hasClass('bottom')){
                obj.css('top', '-' + obj.find('.normal').height() + 'px');
            }

            if(obj.find('.normal').hasClass('right')){
                obj.css('left', '-' + obj.find('.normal').width() + 'px');
            }
        }



        //random movement for the characters of the title
        setInterval(function (){
            var randomTime = getRandom(2, 6);
            var previousNum = '';
            do{
                var num = getRandom(0, characters.length - 1);
            }while(num === previousNum);

            previousNum = num;

            setTimer(that.find('.charWrap').eq(num), randomTime);
        }, 1 * options.speed);

        
        /**
        * Sets a timer for a given character for a given time.
        */
        function setTimer(character, time){
            setTimeout(function (){
                moveCharacter(character);
            }, time * options.speed);
        }

        $('.charWrap').hover(function (){
            if(!$(this).hasClass('moved')){
                moveCharacter($(this));
            }
        });

        
        /**
        * Moves a character to the destination position.
        * Once reached, it will add a class "moved" as an  status indicator.
        */
        function moveCharacter(characterWrap){
            var sizeY = characterWrap.height() / 2;
            var sizeX = characterWrap.width() / 2;
            var character = characterWrap.find('.active');

            if(supportTransitions()){
                if(character.hasClass('moveRight')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.css('left', '-' + sizeX + 'px');
                    }else{
                        characterWrap.css('left', '0px');
                    }
                } else if(character.hasClass('moveLeft')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.css('left', '0px');
                    }else{
                        characterWrap.css('left', '-' + sizeX + 'px');
                    }
                } else if(character.hasClass('moveUp')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.css('top', '0px');
                    }else{
                        characterWrap.css('top', '-' + sizeY + 'px');
                    }
                } else if(character.hasClass('moveDown')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.css('bottom', sizeY + 'px');
                    }else{
                        characterWrap.css('bottom', '0px');
                    }
                }
            }
            
            //jquery fallback 
            else{
                if(character.hasClass('moveRight')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.animate({
                            'left': '-' + sizeX + 'px'
                        }, 400);
                    }else{
                        characterWrap.animate({
                            'left': '0px'
                        },400);
                    }
                } else if(character.hasClass('moveLeft')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.animate({
                            'left': '0px'
                        },400);
                    }else{
                        characterWrap.animate({
                            'left' :  '-' + sizeX + 'px'
                        },400);
                    }
                } else if(character.hasClass('moveUp')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.animate({
                            'top': '0px'
                        }, 400);
                    }else{
                        characterWrap.animate({
                            'top': '-' + sizeY + 'px'
                        }, 400);
                    }
                } else if(character.hasClass('moveDown')){
                    if(!characterWrap.hasClass('moved')){
                        characterWrap.animate({
                            'bottom' : sizeY + 'px'
                        }, 400);
                    }else{
                        characterWrap.animate({
                            'bottom':'0px'
                        },400);
                    }
                }
            }

            characterWrap.toggleClass('moved');
        }
    };
    
    
        
    /**
     * jQuery.support.cssProperty
     * To verify that a CSS property is supported (or any of its browser-specific implementations)
     *
     *
     * @Author: Axel Jack Fuchs (Cologne, Germany)
     * @Date: 08-29-2010 18:43
     *
     * Example: $.support.cssProperty('boxShadow');
     * Returns: true
     *
     * Example: $.support.cssProperty('boxShadow', true);
     * Returns: 'MozBoxShadow' (On Firefox4 beta4)
     * Returns: 'WebkitBoxShadow' (On Safari 5)
     */
    function supportTransitions() {
        var b = document.body || document.documentElement;
        var s = b.style;
        var p = 'transition';
        if(typeof s[p] == 'string') {return true; }

        // Tests for vendor specific prop
        v = ['Moz', 'Webkit', 'Khtml', 'O', 'ms', 'Icab'],
        p = p.charAt(0).toUpperCase() + p.substr(1);
        for(var i=0; i<v.length; i++) {
          if(typeof s[v[i] + p] == 'string') { return true; }
        }
        return false;
    }

})(jQuery);


/*!
 * jQuery Countdown plugin v1.0
 * http://www.littlewebthings.com/projects/countdown/
 *
 * Copyright 2010, Vassilis Dourdounis
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
(function($){

    $.fn.countDown = function (options) {

        config = {};

        $.extend(config, options);

        diffSecs = this.setCountDown(config);
    
        if (config.onComplete)
        {
            $.data($(this)[0], 'callback', config.onComplete);
        }
        if (config.omitWeeks)
        {
            $.data($(this)[0], 'omitWeeks', config.omitWeeks);
        }

        $('#' + $(this).attr('id') + ' .digit').html('<div class="top"></div><div class="bottom"></div>');
        $(this).doCountDown($(this).attr('id'), diffSecs, 500);

        return this;

    };

    $.fn.stopCountDown = function () {
        clearTimeout($.data(this[0], 'timer'));
    };

    $.fn.startCountDown = function () {
        this.doCountDown($(this).attr('id'),$.data(this[0], 'diffSecs'), 500);
    };

    $.fn.setCountDown = function (options) {
        var targetTime = new Date();

        if (options.targetDate)
        {
            targetTime = new Date(options.targetDate.month + '/' + options.targetDate.day + '/' + options.targetDate.year + ' ' + options.targetDate.hour + ':' + options.targetDate.min + ':' + options.targetDate.sec + (options.targetDate.utc ? ' UTC' : ''));
        }
        else if (options.targetOffset)
        {
            targetTime.setFullYear(options.targetOffset.year + targetTime.getFullYear());
            targetTime.setMonth(options.targetOffset.month + targetTime.getMonth());
            targetTime.setDate(options.targetOffset.day + targetTime.getDate());
            targetTime.setHours(options.targetOffset.hour + targetTime.getHours());
            targetTime.setMinutes(options.targetOffset.min + targetTime.getMinutes());
            targetTime.setSeconds(options.targetOffset.sec + targetTime.getSeconds());
        }

        var nowTime = new Date();

        diffSecs = Math.floor((targetTime.valueOf()-nowTime.valueOf())/1000);

        $.data(this[0], 'diffSecs', diffSecs);

        return diffSecs;
    };

    $.fn.doCountDown = function (id, diffSecs, duration) {
        $this = $('#' + id);
        if (diffSecs <= 0)
        {
            diffSecs = 0;
            if ($.data($this[0], 'timer'))
            {
                clearTimeout($.data($this[0], 'timer'));
            }
        }

        secs = diffSecs % 60;
        mins = Math.floor(diffSecs/60)%60;
        hours = Math.floor(diffSecs/60/60)%24;
        if ($.data($this[0], 'omitWeeks') == true)
        {
            days = Math.floor(diffSecs/60/60/24);
            weeks = Math.floor(diffSecs/60/60/24/7);
        }
        else 
        {
            days = Math.floor(diffSecs/60/60/24)%7;
            weeks = Math.floor(diffSecs/60/60/24/7);
        }

        $this.dashChangeTo(id, 'seconds_dash', secs, duration ? duration : 800);
        $this.dashChangeTo(id, 'minutes_dash', mins, duration ? duration : 1200);
        $this.dashChangeTo(id, 'hours_dash', hours, duration ? duration : 1200);
        $this.dashChangeTo(id, 'days_dash', days, duration ? duration : 1200);
        $this.dashChangeTo(id, 'weeks_dash', weeks, duration ? duration : 1200);

        $.data($this[0], 'diffSecs', diffSecs);
        if (diffSecs > 0)
        {
            e = $this;
            t = setTimeout(function() { e.doCountDown(id, diffSecs-1) } , 1000);
            $.data(e[0], 'timer', t);
        } 
        else if (cb = $.data($this[0], 'callback')) 
        {
            $.data($this[0], 'callback')();
        }

    };

    $.fn.dashChangeTo = function(id, dash, n, duration) {
          $this = $('#' + id);
         
          for (var i=($this.find('.' + dash + ' .digit').length-1); i>=0; i--)
          {
                var d = n%10;
                n = (n - d) / 10;
                $this.digitChangeTo('#' + $this.attr('id') + ' .' + dash + ' .digit:eq('+i+')', d, duration);
          }
    };

    $.fn.digitChangeTo = function (digit, n, duration) {
        if (!duration)
        {
            duration = 800;
        }
        if ($(digit + ' div.top').html() != n + '')
        {

            $(digit + ' div.top').css({'display': 'none'});
            $(digit + ' div.top').html((n ? n : '0')).slideDown(duration);

            $(digit + ' div.bottom').animate({'height': ''}, duration, function() {
                $(digit + ' div.bottom').html($(digit + ' div.top').html());
                $(digit + ' div.bottom').css({'display': 'block', 'height': ''});
                $(digit + ' div.top').hide().slideUp(10);

            
            });
        }
    };

})(jQuery);


