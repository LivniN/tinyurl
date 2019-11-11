function draw_stats(stats_data) {
    var data = JSON.parse(stats_data)
    draw_number(data.url_redirection_registrations_count)
    draw_bar(data.time_stats, 'time_stats')
}

function draw_bar(data, element_id) {
    var ctx = document.getElementById(element_id);
    var myPieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: data.data_objects,
        },
        options: {
            title: {
                display: true,
                text: 'Time based stats'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        },
    });
}

function draw_number(data) {
    element = document.getElementById('url_registrations_count')
    element.innerHTML = `<strong>${data}</strong>   Redirections in the DB`

}