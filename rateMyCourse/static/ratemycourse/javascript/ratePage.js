
function chooseScore(id){
        		var c0="B";
        		var c1=id.charAt(1);
        		var c2=id.charAt(2);
        		var i=2;
        		for(i=1;i<=parseInt(c2);i++)
            {
              var s=c0.concat(c1.concat(i.toString()));
              $(s).removeClass("fa fa-star-o text-dark");
              $(s).addClass("fa fa-star text-warning");

            }
        		for(i=5;i>parseInt(c2);i--)
            {
              var s=c0.concat(c1.concat(i.toString()));
  						$(s).removeClass("fa fa-star text-warning");
             	$(s).addClass("fa fa-star-o text-dark");
            }
}

function choose_term(text){
              //$(this).parent().prev().text($(this).text());
            	var termList = $("#termList")
            	termList.prev().text(text);
}



$(document).ready(function() {
  alert('!!!')
  if($.cookie('username') == undefined) {
    $("#menuUser").hide()
    $("#menuLogin").show()
  }
  else{
    $("#menuLogin").hide()
    $("#menuUser").show()
    $("#navUser").text($.cookie('username'))
  }
  $.ajax('/getTeachers', {dataType:'json'}).done(function(data) {
    var teacherList = $("#teacherList")
    for (var i = 0; i < data.teachers.length; i++) {
      teacherList.append("<a class='dropdown-item btn btn-primary ' href='#/'>" + data.teachers[i] + "</a>")
    }
    $(".dropdown-item.teacher").click(function() {
      $(this).parent().prev().text($(this).text())

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
  return false
}
