



//   // initialize chart on page load
//   window.addEventListener('load', function(e) {
//     if (window.location.pathname.match(/\/population-projection\/.*/)) {
//         initializeChart()
//     }
//     else if (window.location.pathname.match(/\/dashboard\/.*/)) {
//         dashboardChart()
//     }
//   })
 
  
//   // reinitialize chart after htmx settle
//   document.body.addEventListener('htmx:afterSettle', function(evt) {
//         // if id == main and url == /population-projection/[regex]
//         if (evt.detail.elt.id == 'main' && evt.detail.xhr.responseURL.match(/\/population-projection\/.*/)) {
//             console.log('reinitializing chart')
//             initializeChart()
//         }
//         else if (evt.detail.elt.id == 'main' && evt.detail.xhr.responseURL.match(/\/dashboard\/.*/)) {
//             console.log('reinitializing dashboard chart')
//             dashboardChart()
//         }
            
// })


//take screenshot of chart automatically
// function takeScreenshot() {
//     var canvas = document.getElementById('populationChart');
//     var dataURL = canvas.toDataURL('image/png');
//     var link = document.createElement('a');
//     link.download = 'population-projection.png';
//     link.href = dataURL;
//     link.click();
// }
//


  
    

