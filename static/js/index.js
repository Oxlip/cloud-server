$(document).ready(function() {
  $("a.faq_question").each(function() {
    $(this).click(function(event) {
    ga('send', 'event', 'faq', 'click', $(this).text());
    });
  });

  $("a[href*=#]").click(function(e) {
   ga('send', 'event', 'hashtag', 'click', $(this).text());
  });

   $(".fancybox").fancybox({
      helpers : {
        overlay : {
          css : {
            'background' : 'rgba(124, 139, 143, 0.7)'
          }
        }
      }
    });

   $(".fancybox")
      .attr('rel', 'gallery')
      .fancybox({
        padding : 3

      });

    $('.tabs').tabslet();

});

function sendMessage(url) {
  var email, fullname, subject, message;
  email = $('#feedback_email').val();
  fullname = $('#feedback_fullname').val();
  subject = $('#feedback_subject').val();
  message = $('#feedback_message').val();

  $.get(url, {
        'email': email,
        'fullname': fullname,
        'subject': subject,
        'message': message
      },
    function(res) {
        var qtip_target = $('#feedback_message');
        qtip_target.qtip({
            id: 'messageTooltip',
            content: {
                text: res,
                title: 'Message posted'
            },
            position: {
                my: 'top left',
                at: 'center',
                target: qtip_target
            },
            events: {
                hide: function(event, api) {
                    api.destroy();
                }
            },
            style: {
               classes: 'qtip-youtube'
            }
        });
        var qtip2_api = qtip_target.qtip('api');
        qtip2_api.show();
    }
  );
}
