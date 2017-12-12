function collapseNavbar() {
  if ($("#mainNav").offset().top > 100) {
    $("#mainNav").addClass("navbar-shrink")
  } else {
    $("#mainNav").removeClass("navbar-shrink")
  }
}
