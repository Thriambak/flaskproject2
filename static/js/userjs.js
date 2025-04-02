// Initialize the chart
document.addEventListener('DOMContentLoaded', () => {
    // Success Rate Chart
    const successRateCtx = document.getElementById('successRateChart').getContext('2d');
    new Chart(successRateCtx, {
        type: 'pie',
        data: {
            labels: ['Successful', 'Unsuccessful'],
            datasets: [{
                data: [60, 40], // Replace with dynamic data if needed
                backgroundColor: ['#4caf50', '#f44336'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
            }
        }
    });

    // Applications Overview Chart
    const applicationsCtx = document.getElementById('applicationsChart').getContext('2d');
    new Chart(applicationsCtx, {
        type: 'bar',
        data: {
            labels: ['Job A', 'Job B', 'Job C'], // Replace with dynamic data if needed
            datasets: [
                {
                    label: 'Applications',
                    data: [30, 50, 20],
                    backgroundColor: '#2196f3',
                },
                {
                    label: 'Shortlisted',
                    data: [10, 25, 5],
                    backgroundColor: '#4caf50',
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { beginAtZero: true },
                y: { beginAtZero: true },
            }
        }
    });
});



    setTimeout(() => {
        const messages = document.querySelectorAll('.flash-message');
        messages.forEach(message => message.style.display = 'none');
    }, 5000); // Adjust timing if needed

    window.addEventListener('click', function(event) {
        const dropdown = document.querySelector('.profile-dropdown');
        const dropdownBtn = document.querySelector('.profile-icon-btn');
        
        if (!dropdown.contains(event.target)) {
            const dropdownContent = document.querySelector('.dropdown-content');
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            }
        }
    });
    
    // Toggle dropdown on click (alternative to hover)
    document.querySelector('.profile-icon-btn').addEventListener('click', function(event) {
        event.stopPropagation();
        const dropdownContent = document.querySelector('.dropdown-content');
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });