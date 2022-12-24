document.getElementById('dark-mode-button').addEventListener('click', function() {
  document.body.classList.toggle('dark-mode');
  var navbar = document.getElementById('navbar-header');
  navbar.classList.toggle('navbar navbar-expand-lg bg-dark');
});

