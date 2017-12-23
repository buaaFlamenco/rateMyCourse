$(document).ready(function() {
  // alert("!!!")
  // Animation settings
  setAnimations()

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
  if($.cookie('username') == undefined){
    alert("提交评价前请先登录")
    return false
  }
  
  if($("#additionalRate").val().length < 30){
    alert("评价内容至少需要30字")
	   return false
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
      alert("评论追加成功")
      location.href = "../"
    }
    else {
      alert(data.errormessage)
    }
  })
}
