$(document).ready(function() {
    // Add event listener to the button
    $("#submit_button").on("click", function(e) {
        e.preventDefault(); // Prevent form submission if needed
        // Get the element by ID
        const element = $("#id01");
        // Change the inner HTML
        element.html("New information");
    });
});