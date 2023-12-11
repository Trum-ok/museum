// keep track of previous scroll position
let prevScrollPos = window.pageYOffset;

window.addEventListener('scroll', function() {
  // current scroll position
  const currentScrollPos = window.pageYOffset;

  if (prevScrollPos > currentScrollPos) {
    // user has scrolled up
    // document.querySelector('.main-nav').classList.add('show');
    //  document.getElementById("navbar").style.top = "-50px";
  }

  // update previous scroll position
  prevScrollPos = currentScrollPos;
});