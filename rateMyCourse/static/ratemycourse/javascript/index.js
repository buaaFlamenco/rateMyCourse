$(document).ready(function(){
  $(".dropdown-item").click(function(){
    $(this).parent().prev().text($(this).text());
  })
})
