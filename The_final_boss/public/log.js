document.addEventListener("DOMContentLoaded", () => {

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Define the 'request' function to handle interactions with the server
    function server_request(url) {
      return fetch(url, {
        credentials: 'same-origin',
        method: "POST",
       
      })
      .then(response => response.json())
      .then(response => {
        // console.log(response.session_id);
        if(response.session_id == 0 ){
          alert("Password invalid. Please try again");
        }
        else{
          location.replace('/home');

        }
        
      })
      .catch(error => console.error('Error:', error));
    }
  
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle Login POST Request
    let login_form = document.querySelector('#login_form');
    if (login_form) { // in case we are not on the login page
      login_form.addEventListener('submit', (event) => {
        // Stop the default form behavior
        event.preventDefault();
  
        // Grab the needed form fields
       
        const method = login_form.getAttribute('method');
        formdata = new FormData(login_form);
        console.log(formdata.get("username"));
        console.log(formdata.get("password"));

        const link = `${login_form.getAttribute('action')}/${formdata.get("username")}/${formdata.get("password")}`;
  
        // Submit the POST request
        server_request(link);
      });
    }
  
    // Handle logout POST request
    document.querySelector('.logout_button').addEventListener('click', (event) => {
        // Submit the POST request
        fetch("/logout", {
          credentials: 'same-origin',
          method: "POST",
         
        })
        .then(response => response.json())
      .then(response => {
        location.replace("/home");
      })
      .catch(error => console.error('Error:', error));
  
    });
  });