// Dummy data for new users (replace with dynamic data in your backend)
const newUsers = [
    { name: "John Doe", email: "john.doe@example.com", resume: "john_doe_resume.pdf" },
    { name: "Jane Smith", email: "jane.smith@example.com", resume: "jane_smith_resume.pdf" },
];

// Function to update the count of new users
function updateNewUsersCount() {
    const newUsersCount = document.querySelector("#newUsersCount span");
    newUsersCount.textContent = newUsers.length;
}

// Function to view resume (simulate viewing a PDF)
function viewResume(resumeFile) {
    // Open the resume in a new window or show an alert
    // Replace this with your actual functionality for displaying the resume
    alert("Opening resume: " + resumeFile);
}

// Update the new users count
updateNewUsersCount();

// Dynamically render users list based on data
const usersList = document.querySelector(".users-list");
newUsers.forEach(user => {
    const userItem = document.createElement('div');
    userItem.classList.add('user-item');
    
    userItem.innerHTML = `
        <h3 class="user-name">${user.name}</h3>
        <p class="user-email">${user.email}</p>
        <button class="view-resume-btn" onclick="viewResume('${user.resume}')">View Resume</button>
    `;
    
    usersList.appendChild(userItem);
});
