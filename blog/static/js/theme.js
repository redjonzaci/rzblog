window.onload = toggle_theme;
function toggle_theme() {
  var navbar_theme = document.getElementsByTagName("nav")[0];
  if (document.getElementById("profile-card")) {
    var profile_card = document.getElementById("profile-card");
  }
  
  if (document.body.style.background == "rgb(0, 0, 0)") {
    document.body.style.background = "#fff";
    document.body.style.color = "#000";
    navbar_theme.setAttribute("class", "navbar navbar-expand-lg navbar-light bg-light");
    if (document.getElementById("profile-card")) {
      profile_card.classList.remove("bg-dark", "text-white")
    }
  } else {
    document.body.style.background = "#000";
    document.body.style.color = "#fff";
    navbar_theme.setAttribute("class", "navbar navbar-expand-lg navbar-dark bg-dark");
    if (document.getElementById("profile-card")) {
      profile_card.classList.add("bg-dark", "text-white")
    }
  }
}