function Func_search() {
    // $.ajax('/search',{
    //   dataType:'json',
    //   data:{
    //     'school':$("#buttonSelectSchool").val(),
    //     'department':$("#buttonSelectDepartment").val(),
    //     'keywords':$("#searchboxSearchCourse").val()
    //   }
    // }
    url = '/search/?'
    if($("#buttonSelectSchool").text() != "选择学校"){
      url += "school=" + $("#buttonSelectSchool").text() + "&"
    }
    if($("#buttonSelectDepartment").text() != "选择专业"){
      url += "department=" + $("#buttonSelectDepartment").text() + "&"
    }
    url += "keywords=" + $("#searchboxCourse").val()
    window.location.href = url
}

function clickSearchButton() {
  //alert("!!!")
  $("#searchboxCourse").select()
}

function validateSignUp() {
  $("#formRegister").validate({
    submitHandler: function() {
      Func_signUp();
    },
    rules: {
      inputEmail: {
        required: true,
	      email: true
      },
      inputUsername: {
        required: true,
	      minlength: 2
	    },
	    inputPassword: {
	      required: true,
	      minlength: 5
	    },
      inputVerify: {
        required: true,
	      minlength: 5,
	      equalTo: "#inputPassword"
      }
    },
    messages: {
      inputEmail: "请输入正确的邮箱地址",
      inputUsername: {
        required: "请输入用户名",
        minlength: "用户名长度不能小于2个字符"
      },
      inputPassword: {
        required: "请输入密码",
        minlength: "密码长度不能小于5个字符"
      },
      inputVerify: {
        required: "请再次输入密码",
        minlength: "密码长度不能小于5个字符",
        equalTo: "密码输入不一致"
      }
    }
  })
}

function validateSignIn() {
  $("#formLogin").validate({
    submitHandler: function() {
      Func_signIn();
    },
    rules: {
      username: {
        required: true,
	      minlength: 2
	    },
	    password: {
	      required: true,
	      minlength: 5
	    }
    },
    messages: {
      username: {
        required: "请输入用户名",
        minlength: "用户名必需由两个字符组成"
      },
      password: {
        required: "请输入密码",
        minlength: "密码长度不能小于 5 个字符"
      }
    }
  })
}

$(document).ready(function() {
  //alert("!!!")
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Login widget set according to cookie
  if($.cookie('username') == undefined) {
    $("#menuUser").hide()
    $("#menuLogin").show()
  }
  else{
    $("#menuLogin").hide()
    $("#menuUser").show()
    $("#navUser").text($.cookie('username'))
  }

  $.ajax('/getSchool', {dataType:'json'}).done(function(data) {
    var schoolList = $("#schoolList")
    for (var i = 0; i < data.school.length; i++) {
      schoolList.append("<a class='dropdown-item btn btn-primary school' href='javascript:void(0)'>" + data.school[i] + "</a>")
    }
    $(".dropdown-item.school").click(function() {
      $(this).parent().prev().text($(this).text())
      $("#buttonSelectDepartment").removeClass("disabled")
      $.ajax('/getDepartment',{
        dataType:'json',
        data:{'school':$(this).text()}
      }).done(function(data) {
        var departmentList = $("#departmentList")
        departmentList.children().remove()
        departmentList.prev().text("选择专业")
        for (var i = 0; i < data.department.length; i++) {
          departmentList.append("<a class='dropdown-item btn btn-primary department' href='javascript:void(0)'>" +
           data.department[i] + "</a>")
        }
        $(".dropdown-item.department").click(function() {
          $(this).parent().prev().text($(this).text())
        })
      })
    })
    $("#searchboxCourse").keyup(function(event) {
        if (event.keyCode == 13) {
            Func_search()
        }
      })
  })
})

function Func_signUp() {
  $.ajax("/signUp/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#inputUsername").val(),
      "mail": $("#inputEmail").val(),
      "password": $("#inputPassword").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.errormessage)
    } else {
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username)
    }
  })
  return false
}

function Func_signIn() {
  $.ajax("/signIn/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "password": $("#password").val()
    }
  }).done(function(data) {
    resetInputStyle()
    if(data.statCode != 0) {
      alert(data.errormessage)
    } else {
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username)
    }
  })
  return false
}

function Func_signOut() {
  $("#menuUser").hide()
  $("#menuLogin").show()
  $.removeCookie('username', {path: '/'})
  return false
}
