let formToSubmit;
const message_timeout = document.getElementById("message-timer");

setTimeout(function(){
    message_timeout.style.display = "none";
}, 8000);

document.addEventListener("DOMContentLoaded", function () {
    flatpickr('.datepicker', {
        dateFormat: "Y-m-d",  // Matches Django's default date format
        theme: "bootstrap5", // Flatpickr for Bootstrap 5 theme
    });
});


// Function to show the confirmation modal
function showConfirmation(event) {
    event.preventDefault();  // Prevent form submission
    
    // Store the form to submit later
    formToSubmit = event.target;

    // Show the modal
    var confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
}

// Function to submit the form after confirmation
function submitForm() {
    formToSubmit.submit();  // Submit the form
}