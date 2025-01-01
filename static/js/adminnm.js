// Function to toggle the display of the form
function toggleForm() {
    const formContainer = document.getElementById("jobFormContainer");
    formContainer.style.display = formContainer.style.display === "block" ? "none" : "block";
}

// Function to add a job
function addJob() {
    const jobTitle = document.getElementById("jobTitle").value;
    const jobDescription = document.getElementById("jobDescription").value;
    const jobType = document.getElementById("jobType").value;
    const location = document.getElementById("location").value;
    const salary = document.getElementById("salary").value;
    const deadline = document.getElementById("deadline").value;

    if (!jobTitle || !jobDescription || !location || !salary || !deadline) {
        alert("Please fill in all fields.");
        return;
    }

    const jobList = document.getElementById("jobList");
    const jobItem = document.createElement("li");

    jobItem.innerHTML = `
        <h3>${jobTitle}</h3>
        <p><strong>Type:</strong> ${jobType}</p>
        <p><strong>Location:</strong> ${location}</p>
        <p><strong>Salary:</strong> ${salary}</p>
        <p><strong>Deadline:</strong> ${deadline}</p>
        <p><strong>Description:</strong> ${jobDescription}</p>
    `;

    jobList.appendChild(jobItem);
    document.getElementById("jobForm").reset(); // Reset the form
    toggleForm(); // Hide the form after submission
}
