$(document).ready(function() {
  // alert("!!!")
  // Navbar style settings
  collapseNavbar()
  $(window).scroll(collapseNavbar)
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  setCookie()

  ////////// csrf set up //////////
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
          }
      }
  });
  /////////////////////////////////
})

function Func_submit() {
  if($("#additionalRate").val().length < 30){
    alert("please write more for your course!(more than 30 characters)")
	   return false
  }
  for(i = 0; i　< score.length; i++){
    if(score[i] == 0){
      alert("please rate for all aspect!")
      return false
    }
  }

  $.ajax("/changeComment/", {
    dataType: "json",
    type: "POST",
    traditional: true,
    data: {
      "comment_id": location.pathname.split("/")[2],
      "comment_add": $("#additionalRate").val(),
      "password": $.cookie("password")
      // rates
    }
  }).done(function (data) {
    if(data.statCode == 0){
      alert("your comment submited succesfully!")
      location.href = "../"
    }
    else {
      alert(data.errormessage)
    }
  })
}
