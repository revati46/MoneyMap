const switchers = [...document.querySelectorAll('.switcher')];

switchers.forEach(item => {
    item.addEventListener('click', function() {
        switchers.forEach(item => item.parentElement.classList.remove('is-active'));
        this.parentElement.classList.add('is-active');
    });
});

// Assuming your login form has an ID of "loginForm"
document.getElementById("loginForm").addEventListener("Login", function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Get Gmail and Password input values
    const gmail = document.getElementById("E-mail").value;
    const password = document.getElementById("Password").value;

    // Simulate authentication (replace this with actual validation)
    if (gmail === "test@gmail.com" && password === "1234") { 
        window.location.href = "/transactions"; // Redirect to Transactions page
    } else {
        alert("Invalid Gmail or Password. Please try again.");
    }
});
