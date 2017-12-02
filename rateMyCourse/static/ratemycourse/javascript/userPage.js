$(document).ready(function() {
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Evaluations section is open on default
  viewEvaluations();

  // Option bar settings
  $("#choiceDiscussions").hover(
    optionMoveRight, optionMoveLeft
  ).click(function(){
    $("#choiceDiscussions").unbind("mouseleave")
    $("#choiceEvaluations").on("mouseleave", optionMoveRight)
    optionMoveRight()
    viewDiscussions()
  })

  $("#choiceEvaluations").hover(
    optionMoveLeft, optionMoveRight
  ).click(function(){
    $("#choiceEvaluations").unbind("mouseleave")
    $("#choiceDiscussions").on("mouseleave", optionMoveLeft)
    optionMoveLeft()
    viewEvaluations()
  })
})

function optionMoveLeft(){
  $("#optionBar").stop().animate({
    marginLeft:"0px"
  })
}

function optionMoveRight(){
  $("#optionBar").stop().animate({
    marginLeft:"70px"
  })
}

function viewEvaluations(){
  $("#choiceEvaluations").addClass("active");
  $("#choiceDiscussions").removeClass("active");

  $("#evaluations").show()
  $("#discussions").hide()
}

function viewDiscussions(){
  $("#choiceDiscussions").addClass("active");
  $("#choiceEvaluations").removeClass("active");

  $("#discussions").show()
  $("#evaluations").hide()
}
