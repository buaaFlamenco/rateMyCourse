$(document).ready(function() {
  // alert("!!!")
  // Navbar style settings
  collapseNavbar()
  $(window).scroll(collapseNavbar)
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  if ($.cookie('username') == undefined) {
      $("#menuUser").hide()
      $("#menuLogin").show()
  }
  else {
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text($.cookie('username'))
  }

  ////////// csrf set up //////////
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
          }
      }
  });
  /////////////////////////////////


})
