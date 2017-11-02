$(document).ready(function(){
  $.ajax('/getSchool', {dataType:'json'}).done(function(data){
    var schoolList = $("#schoolList")
    for (var i = 0; i < data.school.length; i++) {
      schoolList.append("<a class='dropdown-item btn btn-primary school' href='#'>" + data.school[i] + "</a>")
    }
    $(".dropdown-item.school").click(function(){
      $(this).parent().prev().text($(this).text())
      $("#selectDepartment").removeClass("disabled")
      $.ajax('/getDepartment',{
        dataType:'json',
        data:{'school':$(this).text()}
      }).done(function(data){
        var departmentList = $("#departmentList")
        departmentList.children().remove()
        departmentList.prev().text("选择专业")
        for (var i = 0; i < data.department.length; i++) {
          departmentList.append("<a class='dropdown-item btn btn-primary department' href='#'>" +
           data.department[i] + "</a>")
        }
        $(".dropdown-item.department").click(function(){
          $(this).parent().prev().text($(this).text())
        })
      })
    })
  })
})

function Func_signUp(){
  $.ajax("/signUp/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#inputUsername").val(),
      "mail": $("#inputEmail").val(),
      "password": $("#inputPassword").val(),
    }
  }).done(function(data){
    if (data.statCode != 0) {
      alert(data.errormessage)
    } else {
      $("#navLogin").text("你好！" + data.username)
    }
  })
  return false
}

function Func_signIn(){
  $.ajax("/signIn/", {
    dataType: 'json',
    type: 'POST', 
    data: {
      "username": $("#username").val(),
      "password": $("#password").val()
    }
  }).done(function(data){
    if(data.statCode != 0) {
      alert(data.errormessage)
    } else {
      $("#navLogin").text("你好！" + data.username)
    }
  })
  return false
}