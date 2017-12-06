var optionLocation = "0px";
var optionWidth;
var optionWidthStr;
$(document).ready(function() {
  // Set optionBar width
  optionWidth = $(optionColumn).width()
  $("#optionBar").width(optionWidth)
  optionWidthStr = optionWidth.toString() + "px"
  // Form validation for Sign in / Sign up forms
  validateSignUp()
  validateSignIn()

  // Evaluations section is open on default
  viewEvaluations()

  // Option bar settings
  $("#choiceEvaluations").hover(
    optionMoveLeft, optionMoveBack
  ).click(
    function(){
    $("#choiceEvaluations").unbind("mouseleave")
    $("#choiceDiscussions").on("mouseleave", optionMoveLeft)
    optionLocation = "0px"
    optionMoveLeft()
    viewEvaluations()
    }
  )
  $("#choiceDiscussions").hover(
    optionMoveRight, optionMoveBack
  ).click(
    function(){
    $("#choiceDiscussions").unbind("mouseleave")
    $("#choiceEvaluations").on("mouseleave", optionMoveRight)
    optionLocation = "70px"
    optionMoveRight()
    viewDiscussions()
    }
  )

})

function optionMoveLeft() {
  $("#optionBar").stop().animate({
    marginLeft:"0px"
  })
}

function optionMoveRight() {
  $("#optionBar").stop().animate({
    marginLeft:optionWidthStr
  })
}

function optionMoveBack() {
  $("#optionBar").stop().animate({
    marginLeft:optionLocation
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
