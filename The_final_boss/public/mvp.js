document.addEventListener("DOMContentLoaded", () => {
    console.log("loading js");
    
    logout_butt = document.querySelector(".logout_button");
    logout_butt.addEventListener('click', (event) =>{
        event.preventDefault();
        fetch('/logout', {method:"POST"})
        .catch(error => console.error('Error:', error));
        window.location.href="/";
    })

});