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
      url += "department=" + $("buttonSelectDepartment").text() + "&"
    }
    url += "keywords=" + $("#searchboxCourse").val()
    window.location.href = url
}

$(document).ready(function() {
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
      schoolList.append("<a class='dropdown-item btn btn-primary school' href='#/'>" + data.school[i] + "</a>")
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
          departmentList.append("<a class='dropdown-item btn btn-primary department' href='#/'>" +
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
  $.removeCookie('username')
  return false
}
