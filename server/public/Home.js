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
    
    // Function for opening form
    function create_form() {
      // Create a form element
      const form = document.createElement("form");
      form.id = "Product-Registration";

      // Creates the form elements with labels and input tags
      const break_line = document.createElement("br");
      
      const serial_number_label = document.createElement("label");
      serial_number_label.htmlFor = "Serial_Number";
      serial_number_label.innerHTML = "<br> Serial Number: ";
      const serial_number_input = document.createElement("input");
      serial_number_input.required = true;
      serial_number_input.type = "text";
      serial_number_input.id = "Serial_Number";
      serial_number_input.name = "Serial_Number";
      serial_number_input.pattern = "{,12}";
      serial_number_input.title = "Serial number should be a 12 characters that are a mixture of letters and numbers"
      form.appendChild(serial_number_label);
      form.appendChild(serial_number_input);

      const product_name_label = document.createElement("label");
      product_name_label.htmlFor = "Product_Name";
      product_name_label.innerHTML = "<br> Product Name: ";
      const product_name_input = document.createElement("input");
      product_name_input.required = true;
      product_name_input.type = "text";
      product_name_input.id = "Product_Name";
      product_name_input.name = "Product_Name";
      product_name_input.pattern = "{,12}";
      product_name_input.title = "Serial number should be a 12 characters that are a mixture of letters and numbers"
      form.appendChild(product_name_label);
      form.appendChild(product_name_input);
      form.appendChild(break_line);

      const submit_button = document.createElement("input");
      submit_button.type = "submit";
      form.appendChild(submit_button);

      // Appends the newly formed node
      document.body.appendChild(form)
      form1 = document.getElementById("Product-Registration");
      form1.addEventListener("submit", add_product, true);
    }

    // Function for loading in product buttons
    function load_buttons() {
      Products.innerHTML = "";
      const url = "/home/products";
      const verb = "get";
      server_get(url, verb, (response) => {
        // [[Serial, Product_Name], [Serial, Product_Name]]
        length = response.length;
        if(response.length > 0) {
          Products.hidden = false;
        }
        // First FOR loop iterates through the rows
        for(var i = 0; i < response.length; i++) {
          let break_line = document.createElement("br");
          let child = document.createElement("button");
          child.id = response[i][0];
          child.innerHTML = response[i][1];
          child.name = response[i][1];
          Products.appendChild(child);
          Products.append(break_line);
          child.addEventListener("click", function() {
            document.cookie = `Product_Name=${child.name}`;
            location.replace("/product");
          })
        }
      })
    }

    // Function for adding a product to the list
    var add_product = function(event) {
      event.preventDefault()
      const data = Object.fromEntries(new FormData(event.target).entries());
      // data = {"Serial_Number": input, "Product_Name": input}
      const url = "/home";
      const verb = "post";
      server_request(url, data, verb, (response) => {
        if(response["message"] == "Serial number was not added to the owner") {
          alert(`Serial number was not added to ${Username}'s account. Please enter a valid serial number.`);
        } else if(response["message"] == "Serial number doesn't exist or is already owned") {
          alert(`Serial number was not added to ${Username}'s account. Please enter a valid serial number.`);
        } else {
          alert("Product was successfully added!");
        }
        add_button.hidden = false;
        delete_button.hidden = false;
        document.body.removeChild(reg_form);
        location.reload();
      })
    }

    function delete_form() {
      if (length === 0) {
        alert("There's no products to delete.")
        return
      }
      // Create a form element
      const form = document.createElement("form");
      form.id = "Product-Deletion";

      // Creates the form elements with labels and input tags
      const break_line = document.createElement("br");

      const product_name_label = document.createElement("label");
      product_name_label.htmlFor = "Product_Name";
      product_name_label.innerHTML = "<br> Product Name: ";
      const product_name_input = document.createElement("input");
      product_name_input.required = true;
      product_name_input.type = "text";
      product_name_input.id = "Product_Name";
      product_name_input.name = "Product_Name";
      product_name_input.pattern = "[a-zA-Z\d]{,12}";
      product_name_input.title = "Serial number should be a 12 characters that are a mixture of letters and numbers"
      form.appendChild(product_name_label);
      form.appendChild(product_name_input);
      form.appendChild(break_line);

      const submit_button = document.createElement("input");
      submit_button.type = "submit";
      form.appendChild(submit_button);

      // Appends the newly formed node
      document.body.appendChild(form)
      form1 = document.getElementById("Product-Deletion");
      form1.addEventListener("submit", delete_product, true);
    }

    // A function to delete a product
    var delete_product = function(event)  {
      add_button.hidden = false;
      delete_button.hidden = false;
      event.preventDefault();
      prod_name = event.target.Product_Name.value;
      prod_button = document.querySelector(`[name=${prod_name}]`);
      const URL = "/home";
      const VERB = "delete";
      const DATA = {"Serial_Number": prod_button.id};
      server_request(URL, DATA, VERB, (response) => {
        if(response["message"] == "Failure") {
          alert("Product wasn't deleted, something went wrong.");
        } else {
          alert("Product was successfully removed from your account!");
        }
        location.reload();
      });
    }

    // A function to check the session ID
    function check_session() {
      const url = "/sessions";
      const verb = "get";
      server_get(url, verb, (response) => {
        message = response["message"];
        if(message === "Session doesn't exist") {
          alert("Session doesn't exist, please log back in with valid credentials!");
          location.replace("/login");
        } else if(message === "Session Expired") {
          alert("Your session has expired! Please log back in with valid credentials.");
          location.replace("/login");
        }
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

    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
    var Greetings = document.getElementById("Intro");
    var Username = getCookieValue("Username");
    var Products = document.getElementById("Product-Container");
    var add_button = document.getElementById("Add-Product");
    var delete_button = document.getElementById("Delete-Product");
    var reg_form;
    var length;

    // EVENT LISTENERS ----------------------------------------------------------------->
    check_session();
    load_buttons();

    Greetings.innerHTML = `Greetings, ${Username}!`;
    add_button.addEventListener("click", function() {
      delete_button.hidden = true;
      create_form();
      add_button.hidden = true;
      reg_form = document.getElementById("Product-Registration");
    })
    
    delete_button.addEventListener("click", function() {
      add_button.hidden = true;
      delete_button.hidden = true;
      delete_form();
    })
    // INTERVAL FUNCTIONS ----------------------------------------------------------------->
    // Runs every minute to check for session ID expiration
    setInterval(function() {
      check_session();
    }, 15000);
    })