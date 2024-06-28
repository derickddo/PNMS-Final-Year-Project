// export chart js
export const initializeChart = () => {
    var ctx = document.getElementById('populationChart').getContext('2d');
    var ctx2 = document.getElementById('populationChart2').getContext('2d');
    var ctx3 = document.getElementById('populationChart3').getContext('2d');
   
    let backgroundColors = JSON.parse(ctx.canvas.dataset.values).map((value, index) => {
        return index % 2 === 0 ? 'rgba(255, 99, 132, 1)' : 'rgba(54, 162, 235, 1)';
    })
    var populationChart = new Chart(ctx, {
        type: 'line', // or 'bar', 'pie', etc.
        data: {
          labels: JSON.parse(ctx.canvas.dataset.labels), // Example labels
            datasets: [{
                label: 'Population Projection',
                data: JSON.parse(ctx.canvas.dataset.values), // Example data
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Population'
                    }
                }
            }
        }
    });
    
    var populationChart2 = new Chart(ctx2, {
        type: 'bar', // or 'bar', 'pie', etc.
        data: {
            labels: JSON.parse(ctx.canvas.dataset.labels), // Example labels
            datasets: [{
                label: 'Population Projection',
                data: JSON.parse(ctx.canvas.dataset.values), // Example data
                borderColor: backgroundColors,
                backgroundColor: backgroundColors,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Population'
                    }
                }
            }
        }
    });
   
    var populationChart3 = new Chart(ctx3, {
        type: 'doughnut', // or 'bar', 'pie', etc.
        data: {
            labels: JSON.parse(ctx.canvas.dataset.labels), // Example labels
            datasets: [{
                label: 'Population Projection',
                data: JSON.parse(ctx.canvas.dataset.values), // Example data
                borderColor: backgroundColors,
                backgroundColor: backgroundColors,
                
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Year'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Population'
                    }
                }
            }
        }
    });
   
}

export const dashboardChart = () => {
    // Select all elements with the class 'populationProjectionChart'
    var chartElements = document.querySelectorAll('.populationProjectionChart');

    // Iterate over each chart element
    chartElements.forEach(ctx => {
        let backgroundColors = JSON.parse(ctx.dataset.values).map((value, index) => {
            return index % 2 === 0 ? 'rgba(255, 99, 132, 0.8)' : 'rgba(54, 162, 235, 0.8)';
        });
        let data = JSON.parse(ctx.dataset.values).map(value => Math.round(value/ 100));

        let labels = JSON.parse(ctx.dataset.labels);

        // get 5 data points if more than 5
        data= data.length > 5 ? data.slice(0, 5) : data 
        labels = labels.length > 5 ? labels.slice(0, 5) : labels;
        
        //convert to zeros
        let base_number = ctx.dataset.values.split(',')[0].length;
        base_number = Math.pow(10, base_number - 1);
        // Initialize Chart.js for the current element
        new Chart(ctx, {
            type: 'bar', // or 'bar', 'pie', etc.
            data: {
                labels: labels, // Example labels
                datasets: [{
                    label: `Population Projection (in ${base_number}s)`,
                    // remove plenty of zeros
                    data: data, // Example data
                    
                    borderColor: backgroundColors,
                    backgroundColor: backgroundColors,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: false,
                            text: 'Year'
                        }
                    },
                    y: {
                        title: {
                            display: false,
                            text: 'Projected Population' 
                        }
                    }
                }
            }
        });
    });
};

