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
    
    // Function for checking login information is correct
    function verification() {
      const data = Object.fromEntries(new FormData(form).entries());
      // {"Email": input, "Password": input}
      const url = "/login";
      const verb = "put";
      let message;
      // Will attempt to create a new user
      server_request(url, data, verb, (response) => {
        message = response["message"];
        if(message == "Success") {
          the_message = true;
          alert("Welcome!");
          location.replace("/home");
        } else {
          the_message = false;
          alert("Wrong login information!");
          location.reload();
        }
      })
      return the_message;
    }
    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
    var form = document.getElementById("Login-Form");
    var the_message;

    // EVENT LISTENERS ----------------------------------------------------------------->
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      verification();
    })
    })