$(document).ready(function() {
  $("a.faq_question").each(function() {
    $(this).click(function(event) {
    ga('send', 'event', 'faq', 'click', $(this).text());
    });
  });

  $("a[href*=#]").click(function(e) {
   ga('send', 'event', 'hashtag', 'click', $(this).text());
  });

  $('.home-slider').bxSlider({
    auto: true,
    pause: 10000,
    speed: 1000,
    displaySlideQty: 4
  });

});
