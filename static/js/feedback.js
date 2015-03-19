(function () { var hu = document.createElement("script"); hu.type = "text/javascript"; hu.async = true; hu.src = "//www.heeduser.com/supfiles/Script/widget.js"; var s = document.getElementsByTagName("script")[0]; s.parentNode.insertBefore(hu, s); })()
var _heeduser = {
type: "button",
community: "nuton",
placement: "middle-right",
color: "#202021"
}
var heeduser_url = "https://www.heeduser.com/FeedbackWidget/Widget.aspx?community=" + _heeduser.community + "&sso=" + encodeURIComponent(_heeduser.sso_token);
document.write('<a id="heeduser_wb" href="JavaScript:heeduser_openwidget(heeduser_url)" class="' + _heeduser.placement + '" style="background:' + _heeduser.color + '"><img src="https://www.heeduser.com/supfiles/Images/feedback_button_en_rm.png"></a>');
