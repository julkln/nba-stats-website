

function getJoueur() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const joueur = urlParams.get('joueur')
    return joueur
  }

function getDateChoisie() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const date = urlParams.get('date_choisie')
    if (date === null){
      let d = new Date()
      d.setDate(d.getDate() -1);
      d = d.toISOString().split('T')[0]
      return d
    } else {
      return date
    }
  }

document.getElementById("input-search").value = getJoueur();

document.getElementById("input-date").value = getDateChoisie();



var today = getDateChoisie();
var parts = today.split('-');
var mydate = new Date(parts[0], parts[1] - 1, parts[2]); 

var options = { month: 'long'};
today_month = new Intl.DateTimeFormat('en-US', options).format(mydate);
today_year = mydate.getFullYear()
today_day = mydate.getDate()


phrase = today_day + ' '+ today_month

document.getElementById('div-classement').style.display = 'none';
document.getElementById('div-player').style.display = 'none';
document.getElementById('div-resultats').style.display = '';

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const date_choisie = urlParams.get('date_choisie')
const player = urlParams.get('joueur')

if (date_choisie != null) {
  document.getElementById('div-classement').style.display = 'none';
  document.getElementById('div-player').style.display = 'none';
  document.getElementById('div-resultats').style.display = '';
  document.getElementById('btn-results').className += " chosen";
  document.getElementById('btn-search').classList.remove("chosen");
  document.getElementById('btn-rankings').classList.remove("chosen");
}
if (player != null) {
  document.getElementById('div-classement').style.display = 'none';
  document.getElementById('div-player').style.display = '';
  document.getElementById('btn-search').className += " chosen";
  document.getElementById('btn-results').classList.remove("chosen");
  document.getElementById('btn-rankings').classList.remove("chosen");
  document.getElementById('div-resultats').style.display = 'none';
}

const clickableRows = document.querySelectorAll(".clickable-row");
const hiddenTables = document.querySelectorAll(".hiddenTable");

clickableRows.forEach((row, index) => {
    row.addEventListener("click", function() {
        // Toggle the display of the corresponding hidden table
        if (hiddenTables[index].classList.contains("hidden")) {
            hiddenTables[index].classList.remove("hidden");
        } else {
            hiddenTables[index].classList.add("hidden");
        }
    });
});