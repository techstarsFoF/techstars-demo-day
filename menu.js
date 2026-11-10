// Hamburger menu: open/close the side panel
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.menu-btn');
  var close = document.querySelector('.menu .close');
  var scrim = document.querySelector('.menu-scrim');
  function set(open) {
    root.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open);
    if (open) close.focus(); else btn.focus();
  }
  btn.addEventListener('click', function () { set(true); });
  close.addEventListener('click', function () { set(false); });
  scrim.addEventListener('click', function () { set(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && root.classList.contains('menu-open')) set(false);
  });
})();
