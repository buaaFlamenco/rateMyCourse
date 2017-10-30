$(document).ready(function(){
  // alert("!!!!!!!!!")
  $.ajax('/getSchool', {dataType: 'json'}).done(function(data){
    var schoolList = $("#schoolList")
    alert("!!!!!!!!!")
    for (var i = 0; i < data.school.length; i++) {
      schoolList.append("<a class='dropdown-item btn btn-primary'>" + data.school[i] + "</a>")
    }
  }).fail(function(xhr, status){
    alert(xhr.status + "   "+status)
  })
  $(".dropdown-item").click(function(){
    $(this).parent().prev().text($(this).text());
  })
})
