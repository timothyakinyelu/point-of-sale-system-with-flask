(function() {
    // get period data from database
    selectPeriod = (text) => { 
        $.ajax(
            {
                type: "GET",
                url: '/chart',
                data: { "period": text },
                success: function (response) { 
                    openCharts(response);
                }
            }
        )
        $('#products').removeClass("show");
    }

    selectMonth = (e, text) => {
        e.preventDefault();

        if(!$('#month').hasClass('active')) {
            $('#month').addClass('active')
            $('#week').removeClass('active')

            selectPeriod(text)
        }
    }

    selectWeek = (e, text) => {
        e.preventDefault();

        if(!$('#week').hasClass('active')) {
            $('#week').addClass('active')
            $('#month').removeClass('active')
            
            selectPeriod(text)
        }
    }

    // on page load fetch period
    $(document).ready(function() {
        var text = $('.nav-tabs li a.active').data('role')
        selectPeriod(text)
    });

    // create new chart on page load or button click
    openCharts = (data) => {
        var labels = data.labels
        var legend = data.legend
        var values = data.values
        var ctx = document.getElementById('myChart').getContext('2d');

        if(window.chart && window.chart !== null){
            window.chart.destroy();
        }

        window.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: legend,
                    data: values,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(55, 129, 64, 0.2)',
                        'rgba(255, 59, 64, 0.2)',
                        'rgba(235, 139, 64, 0.2)',
                        'rgba(225, 129, 64, 0.2)',
                        'rgba(205, 59, 64, 0.2)',
                        'rgba(215, 149, 64, 0.2)',
                        'rgba(25, 169, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 109, 63, 1)',
                        'rgba(255, 129, 234, 1)',
                        'rgba(255, 119, 214, 1)',
                        'rgba(255, 139, 124, 1)',
                        'rgba(255, 149, 124, 1)',
                        'rgba(255, 159, 134, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                responsive: true,
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 0,
                        bottom: 0
                    }
                },
                legend: {
                    display: false,
                    labels: {
                        fontColor: 'grey',
                        boxWidth: 0,
                    }
                }
            }
        });
    }

    // function getLabels(data) {
    //     var labels = [];

    //     for(var i = 0; i < data.length; i++) {
    //         labels.push(data[i])
    //     }

    //     return labels;
    // }
})();