(function () {
  const toggle = document.querySelector('.nav-toggle');
  if (!toggle) return;

  const nav = toggle.closest('nav');

  toggle.addEventListener('click', function () {
    nav.classList.toggle('nav-open');
  });

  nav.querySelectorAll('.nav-links a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('nav-open');
    });
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
      nav.classList.remove('nav-open');
    }
  });
})();
