$(document).ready(function() {
  // Common animation settings
  setAnimations()

  // Set scroll reveal
  window.sr = ScrollReveal()
  sr.reveal('.course-item', {duration:1500, reset:true}, 100)

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
