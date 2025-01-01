// Function to open the modal and display application details
function openModal(jobTitle, company, date, status, details) {
    const modal = document.getElementById('applicationModal');
    const modalBody = document.getElementById('modalBody');

    // Set the content inside the modal
    modalBody.innerHTML = `
        <p><strong>Job Title:</strong> ${jobTitle}</p>
        <p><strong>Company:</strong> ${company}</p>
        <p><strong>Application Date:</strong> ${date}</p>
        <p><strong>Status:</strong> <span class="status ${status.toLowerCase()}">${status}</span></p>
        <p><strong>Application Details:</strong> ${details}</p>
    `;
    modal.style.display = 'flex'; // Show the modal
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('applicationModal');
    modal.style.display = 'none';
}

// Close the modal if clicked outside
window.onclick = function(event) {
    const modal = document.getElementById('applicationModal');
    if (event.target === modal) {
        closeModal();
    }
}
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

 