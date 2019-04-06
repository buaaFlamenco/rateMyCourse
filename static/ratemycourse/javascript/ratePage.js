var score=[0,0,0,0];

function choose_term(text){
  //$(this).parent().prev().text($(this).text());
  var termList = $("#termList")
  termList.prev().text(text);
}

$(document).ready(function() {
  // Animation settings
  setAnimations()

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

  // Rate settings
  $(".star").click(function() {
    var parentId = parseInt($(this).parent().prop("id"))
    $(this).children().removeClass("fa fa-star-o text-dark").addClass("fa fa-star text-warning")
    $(this).prevAll().children().removeClass("fa fa-star-o text-dark").addClass("fa fa-star text-warning")
    $(this).nextAll().children().removeClass("fa fa-star text-warning").addClass("fa fa-star-o text-dark")
    score[parentId] = $(this).index() + 1
  })

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

  $.ajax('/getTeachers', {
    dataType:'json',
    data:{
      'course_number':window.location.pathname.split('/')[2]
    }
  }).done(function(data) {
    var teacherList = $("#teacherList")
    for (var i = 0; i < data.teachers.length; i++) {
      teacherList.append("<a class='dropdown-item btn btn-primary teacher' href='javascript:void(0)'>" + data.teachers[i] + "</a>")
    }
    $(".dropdown-item.teacher").click(function() {
      $(this).parent().prev().text($(this).text())
    })
  })
})

function Func_submit() {

  if($.cookie('username') == undefined){
    alert("提交评价前请先登录")
    return false
  }
  if($('#buttonSelectTerm').text() == '选择学期'){
    alert("请选择学期")
  	return false
  }
  if($('#buttonSelectTeacher').text() == '选择教师'){
    alert('请选择教师')
  	return false
  }
  if($('#writeCommentText').val().length < 30){
    alert('评价部分内容需要30字')
	return false
  }
  for(i = 0; i　< score.length; i++){
    if(score[i] == 0){
      alert('请填写所有选课部分')
      return false
    }
  }

  $.ajax("/submitComment/", {
    dataType: 'json',
    type: 'POST',
    traditional: true,
    data: {
      'username': $.cookie('username'),
      'anonymous': document.getElementById('anonymous').checked,
      'course_number':window.location.pathname.split('/')[2],
      'term': $('#buttonSelectTerm').text(),
      'teacher': $('#buttonSelectTeacher').text().split(','),
      'comment': $('#writeCommentText').val(),
      'rate':score
    }
  }).done(function (data) {
    if(data.statCode == 0){
      alert("your comment submited succesfully!")
      window.location.href = '../'
    }
    else {
      alert(data.errormessage)
    }
  })
}
