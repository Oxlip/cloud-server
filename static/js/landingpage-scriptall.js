var pmc = 0;
var val = 0;
var clearTime = 0;
var code_val = "";
var code = "";
$(document).ready(function() {

  $(".overlay").click(function() {
    $(".c-text1").removeClass("c-text-exp");
    $(".errow_messate_box").fadeOut();
    $(".errow_messate_box_text").fadeOut();
    $(".promocode_accept_worng").fadeOut();
  });

  $(".p_code_list").click(function() {
    $(".c-text1").addClass("blink_1");
  });
  $(".c-text1").click(function() {
    $(".c-text1").removeClass("blink_no");
  });

  $(".simplemodal-close").click(function() {
    $(".over_lay").css("opacity", 0).css("left", "-3000px");
  });
  var af = new Array();
  af = [false, false, false, false]
  var c_status = false;
  $(".p_code_list").click(function() {
    var id = $(this).attr("data-i");
    //af[id-1] = id;
    //alert(af[id-1]);
    var t = $(this);
    if (!af[id - 1]) {
      $(this).next().animate({
        width: 130
      }, "slow");
      $(this).next().find(".c-text1").animate({
        width: 130,
        marginLeft: 30
      }, "slow");
      $(this).parent().parent().parent().prev().find('.promocode_accept').fadeOut();
      $(this).parent().parent().parent().prev().find('.promocode_accept_worng').fadeOut();
      af[id - 1] = true;
      clearTimeout(clearTime);
      clearTime = setTimeout(function() {
        t.next().animate({
          width: 0
        }, "slow");
        t.next().find(".c-text1").animate({
          width: 0,
          marginLeft: 0
        }, "slow");
        af[id - 1] = false;
      }, 6000);
    } else {
      $(this).next().animate({
        width: 0
      }, "slow");
      $(this).next().find(".c-text1").animate({
        width: 0,
        marginLeft: 0
      }, "slow");
      af[id - 1] = false;
    }
  });
  $(".c-text1").keyup(function(e) {
    var id = $(this).attr("data-i");
    //alert(id);
    var t = $(this);
    val = $(this).val();
    clearTimeout(clearTime);
    if (val) {
      $.ajax({
        type: 'POST',
        url: "nw_page.php?vari=" + val + "&mode=check",
        cache: false,
        success: function(res) {
          //alert(res);
          if (res === '1') {
            //alert('yes');
            t.parent().next().fadeIn();
            t.parent().next().next().fadeOut();
            t.focus();
            clearTimeout(clearTime);
            clearTime = setTimeout(function() {
              t.parent().animate({
                width: 0
              }, "slow");
              t.animate({
                width: 0,
                marginLeft: 0
              }, "fast");
              t.parent().parent().parent().prev().find('.promocode_accept_worng').fadeOut();
              t.parent().parent().parent().prev().find('.promocode_accept').fadeIn();
              t.parent().parent().parent().prev().find('.errow_messate_box').fadeOut();
              af[id - 1] = false;
              //$(".ddreew").animate({width:30},"slow");
              $(".c-text1").animate({
                width: 0,
                marginLeft: 0
              }, "fast");
            }, 2000);
          } else if (res === '0') {
            t.parent().next().fadeOut();
            t.parent().next().next().fadeIn();
            t.focus();
            clearTimeout(clearTime);
            clearTime = setTimeout(function() {
              t.parent().animate({
                width: 0
              }, "slow");
              t.animate({
                width: 0,
                marginLeft: 0
              }, "fast");
              t.parent().parent().parent().prev().find('.promocode_accept_worng').fadeIn();
              t.parent().parent().parent().prev().find('.promocode_accept').fadeOut();
              t.parent().parent().parent().prev().find('.errow_messate_box').fadeOut();
              af[id - 1] = false;
              //$(".ddreew").animate({width:30},"slow");
              $(".c-text1").animate({
                width: 0,
                marginLeft: 0
              }, "fast");
            }, 2000);
          }
        }
      });
    } else {
      t.parent().next().hide();
      t.parent().next().next().hide();
      clearTimeout(clearTime);
      clearTime = setTimeout(function() {
        t.parent().animate({
          width: 0
        }, "slow");
        t.animate({
          width: 0,
          marginLeft: 0
        }, "fast");
        t.parent().parent().parent().prev().find('.promocode_accept_worng').fadeIn();
        t.parent().parent().parent().prev().find('.promocode_accept').fadeOut();
        t.parent().parent().parent().prev().find('.errow_messate_box').fadeOut();
        af[id - 1] = false;
        //$(".ddreew").animate({width:30},"slow");
        $(".c-text1").animate({
          width: 0,
          marginLeft: 0
        }, "fast");
      }, 2000);
    }
  });
});
