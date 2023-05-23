document.addEventListener("DOMContentLoaded", function() {

    // FUNCTION DEFINITIONS ------------------------------------------------------>
    // Function for PUTs, POSTs, and DELETEs
    function server_request(url, data={}, Verb, callback) {
        return fetch(url, {
          credentials: 'same-origin',
          method: Verb,
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        .then(response => response.json())
        .then(function(response) {
          if(callback)
            callback(response);
        })
        .catch(error => console.error('Error:', error));
      }
    
    // Function for GETs
    function server_get(url, Verb, callback) {
      return fetch(url, {
        credentials: 'same-origin',
        method: Verb
      })
      .then(response => response.json())
      .then(function(response) {
        if(callback)
          callback(response);
      })
      .catch(error => console.error('Error:', error));
    }
        
    // Function for submitting the form data
    function submission(theForm) {
      const data = Object.fromEntries(new FormData(theForm).entries());
      // {"Email": input, "Username": input, "Password": input}
      const url = "/register";
      const verb = "post";
      let message
      // Will attempt to create a new user
      server_request(url, data, verb, (response) => {
        message = response["message"]
        if(message == "Username not unique") {
          alert("Username is already in use! Please choose a different one.");
          the_message = false;
        } else if(message == "Email already in use") {
          alert("Email is in use with another account. Please choose a different one.");
          the_message = false;
        }
        the_message = true;
      })
      return the_message
    }
    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
    var Form = document.getElementById("Register-Form");
    var the_message;
    
    // EVENT LISTENERS ----------------------------------------------------------------->
    Form.addEventListener("submit", function(event) {
      // Prevents the page form reloading
      event.preventDefault();
      success = submission(Form);
      // If user was successfully created, then relocate them to the login page
      if(success) {
        alert("Welcome to the Smart Blinds family! >:D");
        location.replace("/login");
      } else {
        location.reload();
      }
    });
    })