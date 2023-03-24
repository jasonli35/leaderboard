document.addEventListener("DOMContentLoaded", () => {
    console.log("loading js");
    edit_form = document.querySelector("#edit_form");
    edit_form.addEventListener('submit', (event) => {
        event.preventDefault();
  
        // Grab the needed form fields
       
        formdata = new FormData(edit_form);
        id = document.querySelector("#user_id").innerHTML;
        console.log(formdata.get("uname"));
        console.log(JSON.stringify(Object.fromEntries(formdata.entries())));
        fetch(`/modify/${id}`, {method: "PUT", headers: {
            "Content-type": "application/json"
          },
           body: JSON.stringify(Object.fromEntries(formdata.entries()))})
        .then(data =>{
            console.log(data);
        })
        .catch(error => console.error('Error:', error));

    });

    logout_butt = document.querySelector(".logout_button");
    logout_butt.addEventListener('click', (event) =>{
        event.preventDefault();
        fetch('/logout', {method:"POST"})
        .catch(error => console.error('Error:', error));
        window.location.href="/";
    })

});