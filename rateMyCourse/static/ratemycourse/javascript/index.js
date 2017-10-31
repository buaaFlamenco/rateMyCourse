$(document).ready(function(){
  $.ajax('/getSchool', {dataType:'json'}).done(function(data){
    var schoolList = $("#schoolList")
    for (var i = 0; i < data.school.length; i++) {
      schoolList.append("<a class='dropdown-item btn btn-primary school'>" + data.school[i] + "</a>")
    }
    $(".dropdown-item.school").click(function(){
      $(this).parent().prev().text($(this).text())
      $(".dropdown-toggle.selectDepartment").removeClass("btn-lg")
      $(".dropdown-toggle.selectDepartment").addClass("btn-sm")
      $.ajax('/getDepartment',{
        dataType:'json',
        data:{'school':$(this).text()}
      }).done(function(data){
        var departmentList = $("#departmentList")
        departmentList.children().remove()
        departmentList.prev().text("选择专业")
        for (var i = 0; i < data.department.length; i++) {
          departmentList.append("<a class='dropdown-item btn btn-primary department'>" +
           data.department[i] + "</a>")
        }
        $(".dropdown-item.department").click(function(){
          $(this).parent().prev().text($(this).text())
        })
      })
    })
  })
})
