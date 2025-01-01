// Initialize the chart
const ctx = document.getElementById('chart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Successful Applications', 'Unsuccessful Applications'],
        datasets: [{
            label: 'Success Rate',
            data: [70, 30], // Adjust these values as necessary
            backgroundColor: ['#0a9396', '#f4a261'],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});
document.getElementById('application-history-btn').addEventListener('click', function() {
    fetch('/load_application_history') // Request to load application history page
        .then(response => response.text()) // Parse the response as text (HTML)
        .then(data => {
            document.getElementById('content').innerHTML = data; // Inject the page content
        })
        .catch(error => {
            console.error('Error loading application history:', error);
        });
});
