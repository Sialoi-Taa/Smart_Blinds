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
      const break_line = document.createElement("inline");
      break_line.innerHTML = "<br>";

      const serial_number_label = document.createElement("label");
      serial_number_label.htmlFor = "Serial_Number";
      serial_number_label.innerHTML = "<br> Serial Number: ";
      const serial_number_input = document.createElement("input");
      serial_number_input.type = "text";
      serial_number_input.id = "Serial_Number";
      serial_number_input.name = "Serial_Number";
      serial_number_input.pattern = "[a-zA-Z\d]{,12}";
      serial_number_input.title = "Serial number should be a 12 characters that are a mixture of letters and numbers"
      form.appendChild(serial_number_label);
      form.appendChild(serial_number_input);
      form.appendChild(break_line);

      const product_name_label = document.createElement("label");
      product_name_label.htmlFor = "Product_Name";
      product_name_label.innerHTML = "<br> Product Name: ";
      const product_name_input = document.createElement("input");
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
      form1 = document.getElementById("Product-Registration");
      form1.addEventListener("submit", add_product, true);
      console.log(form1);
    }

    // Function for adding a product to the list
    var add_product = function(event) {
      event.preventDefault()
      const data = Object.fromEntries(new FormData(reg_form).entries());
      // data = {"Serial_Number": input, "Product_Name": input}
      const url = "/home";
      const verb = "post";
      server_request(url, data, verb, function() {

      })
      add_button.hidden = false;
      document.body.removeChild(reg_form);
    }

    // DOCUMENT ELEMENT VARIABLES ------------------------------------------------------>
    var Greetings = document.getElementById("Intro");
    var Username = document.cookie["Username"];
    var Products = document.getElementById("Product-Container");
    var Form_Container = document.getElementById("Form-Container");
    var add_button = document.getElementById("Add-Product");

    // EVENT LISTENERS ----------------------------------------------------------------->
    Greetings.innerHTML = `Greetings, ${Username}!`;
    add_button.addEventListener("click", function() {
      create_form();
      add_button.hidden = true;
      var reg_form
      reg_form = document.getElementById("Product-Registration");
    })

    // INTERVALE FUNCTIONS ----------------------------------------------------------------->
    //setInterval(,10000)

    })