// Wait for the splash screen to fade out and show the buttons
setTimeout(function() {
    // Fade out the splash screen
    const splashScreen = document.getElementById('splash-screen');
    splashScreen.style.opacity = '0'; // Fade it out

    // After the fade-out is done, hide the splash screen and show the main content
    setTimeout(function() {
        splashScreen.style.display = 'none'; // Remove the splash screen from the view
        document.getElementById('main-container').style.display = 'block'; // Show the main content
    }, 1000); // 1000 ms delay to allow for fade-out animation to complete
}, 3000); // Wait 3 seconds before starting the fade-out
