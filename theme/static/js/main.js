//function for onload to load theme from localstorage
function loadTheme(){
    const theme = localStorage.getItem('theme');
    if(theme){
        document.getElementsByTagName('html')[0].dataset.theme = theme
        console.log(theme);
    }
}


//call loadTheme function on load
loadTheme();

window.onload = function() {
    loadTheme();
};

