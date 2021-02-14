window.onload = toggle_theme;
function toggle_theme() {
  var navbar_theme = document.getElementsByTagName("nav")[0];
  if (document.querySelectorAll('[id=dark-dropdown]')) {
    var dark_dropdowns = document.querySelectorAll('[id=dark-dropdown]');
  }
  if (document.querySelectorAll('[id=list-item]')) {
    var dark_stats = document.querySelectorAll('[id=list-item]');
  }
  if (document.getElementById("profile-card")) {
    var profile_card = document.getElementById("profile-card");
  }
  if (document.body.style.background == "rgb(0, 0, 0)") {
    document.body.style.background = "#fff";
    document.body.style.color = "#000";
    navbar_theme.setAttribute("class", "navbar navbar-expand-lg navbar-light bg-light");
    if (document.getElementById("profile-card")) {
      profile_card.classList.remove("bg-dark", "text-white");
    }
    if (document.querySelectorAll('[id=dark-dropdown]')) {
      for (var i = 0; i < dark_dropdowns.length; i++) {
        dark_dropdowns[i].classList.remove("dropdown-menu-dark");
      }
    }
    if (document.querySelectorAll('[id=list-item]')) {
      for (var i = 0; i < dark_stats.length; i++) {
        dark_stats[i].classList.remove("list-group-item-dark");
      }
    }
  } else {
    document.body.style.background = "#000";
    document.body.style.color = "#fff";
    navbar_theme.setAttribute("class", "navbar navbar-expand-lg navbar-dark bg-dark");
    if (document.getElementById("profile-card")) {
      profile_card.classList.add("bg-dark", "text-white");
    }
    if (document.querySelectorAll('[id=dark-dropdown]')) {
      for (var i = 0; i < dark_dropdowns.length; i++) {
        dark_dropdowns[i].classList.add("dropdown-menu-dark");
      }
    }
    if (document.querySelectorAll('[id=list-item]')) {
      for (var i = 0; i < dark_stats.length; i++) {
        dark_stats[i].classList.add("list-group-item-dark");
      }
    }
  }
}