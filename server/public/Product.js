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
        
        // Loads all of the schedules assigned to that product
        function load_schedules() {
          // Goes to the server and returns the list of all schedules
          // for that specific serial number. Then loads all of them
          // onto the page for the product.

          const url = "/schedule";
          const verb = "get";
          server_get(url, verb, (response) => {
            if(response.length > 0) {
              Schedule_List.hidden = false;
              Schedule_List.innerHTML = "";
            }
            // First FOR loop iterates through the rows
            for(var i = 0; i < response.length; i++) {
              //console.log(response);
              start = response[i][0];
              end = response[i][1];
              state = response[i][2];
              if (state == 1) {
                state = "ON";
              } else if( state == 0) {
                state = "OFF";
              }
              let child = document.createElement("div");
              child.class
              child.innerHTML = `From ${start} to ${end}, Smart Blinds product named: ${Product_Name} will be turned ${state}. <br>`;
              Schedule_List.appendChild(child);
            }
          })
        }

        // Writes the current state of the button as the user enters the page
        function Write_Button() {
          const url = "/state";
          const verb = "get";
          server_get(url, verb, (response) => {
            let message = response["message"];
            State_Button.innerHTML = message;
          })
        }
        Write_Button();

        // Writes the state of the button on the HTML page
        function Change_State_Button() {
          // Will take the current state of the button, send it to the server,
          // store the switched state in a table, change the state in the hardware 
          // and return the new current state to be written for the user.

          const url = "/state";
          const verb = "put";
          const data = {"state": State_Button.innerHTML};
          server_request(url, data, verb, (response) => {
            let message = response["message"];
            console.log("Change_State_Button " + message);
            Write_Button();
          });
        }

        // Checks the validity of the user's session
        function check_session() {
          const url = "/sessions";
          const verb = "get";
          server_get(url, verb, (response) => {
            message = response["message"];
            if(message == "Session doesn't exist") {
              alert("Session doesn't exist, please log back in with valid credentials!");
              location.replace("/login");
            } else if(message == "Session Expired") {
              alert("Your session has expired! Please log back in with valid credentials.");
              location.replace("/login");
            }
          })
        }

        // Function for adding interactivity for the add button
        function add_button_functionality() {
          // Hides the add button, creates a form to add a new schedule
          // and when submitted will go to the add_schedule function

          Add_Button.hidden = true;
          // Create a form element
          const form = document.createElement("form");
          form.id = "Time_Input";

          // Creates the form elements with labels and input tags
          const break_line = document.createElement("br");
          
          const start_time_label = document.createElement("label");
          start_time_label.htmlFor = "Start_Time";
          start_time_label.innerHTML = "<br> Start Time: ";
          const start_time_input = document.createElement("input");
          start_time_input.required = true;
          start_time_input.type = "text";
          start_time_input.id = "Start_Time";
          start_time_input.name = "Start_Time";
          start_time_input.pattern = "[0-9]{2}:[0-9]{2}";
          start_time_input.title = "Time should only be in the format HH:MM"
          form.appendChild(start_time_label);
          form.appendChild(start_time_input);

          const end_time_label = document.createElement("label");
          end_time_label.htmlFor = "End_Time";
          end_time_label.innerHTML = "<br> End Time: ";
          const end_time_input = document.createElement("input");
          end_time_input.required = true;
          end_time_input.type = "text";
          end_time_input.id = "End_Time";
          end_time_input.name = "End_Time";
          end_time_input.pattern = "[0-9]{2}:[0-9]{2}";
          end_time_input.title = "Time should only be in the format HH:MM"
          form.appendChild(end_time_label);
          form.appendChild(end_time_input);

          const state_label = document.createElement("label");
          state_label.htmlFor = "State";
          state_label.innerHTML = "<br> State: ";
          const state_input = document.createElement("input");
          state_input.required = true;
          state_input.type = "text";
          state_input.id = "State";
          state_input.name = "State";
          state_input.pattern = "(?=.*[A-Z]){2,3}[A-Z]*$";
          state_input.title = "Input should be either ON or OFF"
          form.appendChild(state_label);
          form.appendChild(state_input);
          form.appendChild(break_line);

          const submit_button = document.createElement("input");
          submit_button.type = "submit";
          form.appendChild(submit_button);

          // Appends the newly formed node
          document.body.appendChild(form)
          form1 = document.getElementById("Time_Input");
          form1.addEventListener("submit", add_schedule, true);

        }

        // Function for the adding a schedule
        function add_schedule(event) {
          // Tells the server the new schedule information and goes
          // to the load_schedules function to add the new schedule
          // to the list of schedules on the page currently.

          event.preventDefault();
          const url = "/schedule";
          const verb = "post";
          const data = Object.fromEntries(new FormData(event.target).entries());
          //console.log(data);
          server_request(url, data, verb, function(response) {
            message = response["message"];
            //console.log(response);
            alert(message);
            document.body.removeChild(document.getElementById("Time_Input"));
            Add_Button.hidden = false
            load_schedules();
          })
        }

        // A function to get a cookie's value
        function getCookieValue(cookieName) {
          // Because when looking at the cookies its in the form: cookie_name=cookie_value;cookie_name=cookie_value...
          const cookies = document.cookie.split(';');
          // Now we iterate over set of key value pairs of cookies
          for (let i = 0; i < cookies.length; i++) {
            // Removes the leading and trailing white space
            const cookie = cookies[i].trim();
            // Check if the cookie starts with the provided name
            if (cookie.startsWith(cookieName + '=')) {
              // Extract and return the cookie value by looking at the length 
              // of the key value pair and start at the index of the length of 
              // the key plus 1 which would be the equal sign
              return cookie.substring(cookieName.length + 1);
            }
          }
          // If the cookie is not found
          return null;
        }

        function schedule_change_state() {
          const url = "/schedule/product";
          const verb = "get";
          console.log("here");
          server_get(url, verb, (response) => {
            console.log("in");
            message = response["message"];
            Write_Button();
          })
        }

    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
        var Title = document.getElementById("Title");
        var State_Button = document.getElementById("State");
        var Add_Button = document.getElementById("Add_Button");
        var Schedule_List = document.getElementById("Schedule_List");
        var Product_Name = getCookieValue("Product_Name");
        //var Username = getCookieValue("Username");
    
    // EVENT LISTENERS ----------------------------------------------------------------->
        Title.innerHTML = `${Product_Name}`;
        load_schedules();
        State_Button.addEventListener("click", Change_State_Button);
        Add_Button.addEventListener("click", add_button_functionality);


    // INTERVAL FUNCTIONS -------------------------------------------------------------->
    // Runs every minute to check for session ID expiration
    setInterval(function() {
      check_session();
      schedule_change_state();
    }, 5000);
    })