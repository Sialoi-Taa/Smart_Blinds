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
        
        function Write_Button() {
          const url = "/state";
          const verb = "get";
          server_get(url, verb, (response) => {
            let message = response["message"];
            State_Button.innerHTML = message;
          })
        }
        Write_Button();

        function State_Button() {
          const url = "/state";
          const verb = "put";
          const data = {"state": State_Button.innerHTML};
          server_request(url, data, verb, function() {
            let message = response["message"];
            State_Button.innerHTML = message;
          });
        }
    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
        var Title = document.getElementById("Title");
        var State_Button = document.getElementById("State");
        var Add_Button = document.getElementById("Add_Button");
        var Schedule_List = document.getElementById("Schedule_List");
        var Product_Name = document.cookie["Product_Name"];
    
    // EVENT LISTENERS ----------------------------------------------------------------->
        Title.innerHTML = `${Product_Name}`;

        State_Button.addEventListener("click", State_Button);
    })