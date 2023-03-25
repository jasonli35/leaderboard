document.addEventListener("DOMContentLoaded", () => {

    head = document.getElementById("head");

    function addComent(groupid, newcomment) {
        console.log("adding comment");
        comment_cotainer = document.createElement("div");
        let parent = document.querySelector(`#group-${groupid}`);
        let newCommentEntry = document.createElement("p");
        delete_but = document.createElement("button");
        
        delete_but.style.color = "white";
        delete_but.innerHTML = "Delete";
        newCommentEntry.innerHTML = newcomment;
        
        comment_cotainer.appendChild(newCommentEntry);
        comment_cotainer.appendChild(delete_but);
        parent.appendChild(comment_cotainer);
    }
    
    for(let i = 1; i < 26; i++){
        
        const desnode = document.createElement("h2");
        desnode.setAttribute('id',`group-${i}`)
        fetch(`https://slidespace.icu/api/teams/${i}`)
        .then(respnse => {
            //console.log(respnse.json());
            return  respnse.json();
            
        })
        .then((data) => {

            info = JSON.parse(data.team);
            let descrip = info.name; 
            let id = info.id;
           
            desnode.innerHTML = id + ". " + descrip;
           
        })
        .catch(error => console.error('Error: ', error));
        head.appendChild(desnode);


     }
     

     comment_form = document.querySelector("#comment_form");
        comment_form.addEventListener('submit' , (event)=>{
            event.preventDefault();
  
            // Grab the needed form fields
            
            let formdata = new FormData(comment_form);
            let newcomment = formdata.get("new_comment");
            let groupid = formdata.get('group_no');
            addComent(groupid,newcomment);
            var dict = {
                id: groupid,
                content: newcomment
            };
            fetch(`/addcomment`, {method: "PUT", headers: {
                "Content-type": "application/json"
              },
               body: JSON.stringify(dict)})
            .then((response) =>  response.json())
            .then((result) => {
                console.log("below is comment id");
                console.log(result);
                delete_but.addEventListener('click' , (event) =>{
                    event.preventDefault();
                    comment_cotainer.remove();
    
                    fetch(`/delete_comment/${result}`,{method:"DELETE"})
                    .catch(error => console.error('Error: ', error));
                });
            })
            .catch(error => console.error('Error: ', error));


           
            


        });

    fetch("/all-comments")
     .then(response => {
        return response.json();
     })
     .then((data) => {
        // console.log("printing all comments data");
        // console.log(data);
        for (const [key,value] of Object.entries(data)) {
            // console.log(value["team_id"]);
            // console.log(value["content"]);
            console.log(value["team_id"]);
            console.log(value["content"]);
            addComent(value["team_id"], value["content"]);
        }

     })
     .catch(error => console.error('Error: ', error));

       



})