$(document).ready(function(){
  $.ajax('/getSchool', {dataType: 'json'}).done(function(data){
    var schoolList = $("#schoolList")
    for (var i = 0; i < data.school.length; i++) {
      schoolList.append("<a class='dropdown-item btn btn-primary'>" + data.school[i] + "</a>")
    }
  $(".dropdown-item").click(function(){
    $(this).parent().prev().text($(this).text());
  })
  })
})
