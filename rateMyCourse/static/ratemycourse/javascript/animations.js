function setAnimations() {
  // Navbar animation settings
  collapseNavbar()
  $(window).scroll(collapseNavbar)

  //Dropdown style settings
  slideDropdown()
}

function collapseNavbar() {
  if ($(".navbar").offset().top > 2) {
    $(".navbar").addClass("navbar-shrink")
  } else {
    $(".navbar").removeClass("navbar-shrink")
  }
}

function slideDropdown() {
  $('.dropdown').on('show.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
  });

  $('.dropdown').on('hide.bs.dropdown', function() {
    $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
  });
}
