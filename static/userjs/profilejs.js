let isEditing = false;

function toggleEdit() {
    const aboutMeText = document.getElementById("about-me-text");
    const aboutMeEdit = document.getElementById("about-me-edit");
    const button = document.getElementById("edit-save-button");

    if (isEditing) {
        // Save changes
        const newAboutMe = aboutMeEdit.value;
        aboutMeText.textContent = newAboutMe || "Not provided";
        aboutMeText.style.display = "block";
        aboutMeEdit.style.display = "none";
        button.textContent = "Edit";

        // Optionally, send updated data to the server using fetch or AJAX
        // fetch('/save-about-me', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ about_me: newAboutMe })
        // }).then(response => console.log('Saved successfully.'));
    } else {
        // Enable editing
        aboutMeEdit.value = aboutMeText.textContent.trim() !== "Not provided" ? aboutMeText.textContent : "";
        aboutMeText.style.display = "none";
        aboutMeEdit.style.display = "block";
        button.textContent = "Save Changes";
    }

    isEditing = !isEditing;
}
