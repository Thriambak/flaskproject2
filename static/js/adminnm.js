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
function editJob(id, title, description, jobType, location, salary, deadline) {
    console.log("Editing Job:", { id, title, description, jobType, location, salary, deadline });

    // Display the form container
    const formContainer = document.getElementById("jobFormContainer");
    formContainer.style.display = "block"; // Ensure the form is visible

    // Update form title
    document.getElementById("formTitle").innerText = "Update Job";

    // Pre-fill the form fields with job details
    document.getElementById("jobId").value = id; // Hidden field for job ID
    document.getElementById("jobTitle").value = title;
    document.getElementById("jobDescription").value = description;

    // Handle the dropdown for job type
    const jobTypeDropdown = document.getElementById("jobType");
    for (let i = 0; i < jobTypeDropdown.options.length; i++) {
        if (jobTypeDropdown.options[i].value === jobType) {
            jobTypeDropdown.selectedIndex = i;
            break;
        }
    }

    document.getElementById("location").value = location;
    document.getElementById("salary").value = salary;
    document.getElementById("deadline").value = deadline;

    // Change the form submit button text to "Update Job"
    document.getElementById("formSubmitButton").innerText = "Update Job";

    // Scroll to the form for better UX
    formContainer.scrollIntoView({ behavior: 'smooth' });
}

