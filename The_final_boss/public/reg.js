document.addEventListener("DOMContentLoaded", () => {

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Define the 'request' function to handle interactions with the server
    function server_request(url, verb) {
      fetch(url, {
        credentials: 'same-origin',
        method: verb,
      })
      .then(respnse => {
        return respnse.json();
      })
      .then((data) => {
        console.log(data);
        if(data == 0){
            alert("this email or pid have been register");
        }
        else{
          location.replace('/log');
        }
        
      })
      .catch(error => console.error('Error:', error));
    }
  
    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle Login POST Request
    let reg_form = document.querySelector('form[name=reg_form]');
    if (reg_form) { // in case we are not on the reg page
        reg_form.addEventListener('submit', (event) => {
        // Stop the default form behavior
        event.preventDefault();
  
        // Grab the needed form fields
        formdata = new FormData(reg_form);
        if(formdata.get("psw") != formdata.get("psw-repeat")){
            alert("password doesn't match! please re-enter");
        }
        else{
            const method = reg_form.getAttribute('method');
            const link = `${reg_form.getAttribute('action')}/${formdata.get("fname")}/${formdata.get("lname")}/${formdata.get("sid")}/${formdata.get("email")}/${formdata.get("uname")}/${formdata.get("psw")}`;
             // Submit the POST request
            server_request(link, method);

        }
      
      
    
  
       
      });
    }
  
  });