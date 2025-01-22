function showDetails(jobTitle, company, status) {
    document.getElementById('modalJobTitle').textContent = jobTitle;
    document.getElementById('modalCompany').textContent = company;
    document.getElementById('modalStatus').textContent = status;

    // Show the modal
    var detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
    detailsModal.show();
}
