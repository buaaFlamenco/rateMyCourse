function Func_search() {
    url = '/search/?'
    if($("#buttonSelectSchool").text() != "选择学校"){
      url += "school=" + $("#buttonSelectSchool").text() + "&"
    }
    if($("#buttonSelectDepartment").text() != "选择专业"){
      url += "department=" + $("#buttonSelectDepartment").text() + "&"
    }
    url += "keywords=\"" + $("#searchboxCourse").val() + "\""
    window.location.href = url
}

function clickSearchButton() {
  //alert("!!!")
  $("#searchboxCourse").select()
}

$(document).ready(function() {
  //alert("!!!")

  // Set animations for common elements on page
  setAnimations()

  // Set scroll reveal
  window.sr = ScrollReveal({duration: 1500})
  sr.reveal('.selection', 100)

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
              xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
          }
      }
  });
  /////////////////////////////////

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
