document.addEventListener('DOMContentLoaded', function() {
    var selects = document.querySelectorAll('#signup').forEach(button => {
        button.onclick = sendRequest;
    });
    
});

function sendRequest() {
    const request = new XMLHttpRequest();
    request.open('GET', '/signup');

    // Callback function for when request completes
    request.onload = () => {

        // Extract JSON data from request
        
        history.pushState(null, "signup", "signup");
    }

    // Add data to send with request
    // const data = new FormData();
    //data.append('currency', currency);

    // Send request
    request.send();
    return false;
}