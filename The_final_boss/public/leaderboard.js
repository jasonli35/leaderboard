document.addEventListener("DOMContentLoaded", () => {
 
    parent = document.querySelector("#parent");
     for(let i = 1; i < 27; i++){
        const newTr = document.createElement("tr");

       
        fetch(`https://slidespace.icu/api/teams/${i}`)
        .then(respnse => {
            //console.log(respnse.json());
            return  respnse.json();
            
        })
        .then((data) => {

            info = JSON.parse(data.team);
            let descrip = info.name;
            let member = info.members
          

            
            const desnode = document.createElement("td");
            desnode.innerHTML = descrip;
            const membernode = document.createElement("td");
            membernode.innerHTML = member;
            newTr.appendChild(desnode);
            newTr.appendChild(membernode);
   
        })
        .catch(error => console.error('Error: ', error));

        fetch(`https://slidespace.icu/api/teams/${i}/scores`)
        .then(respnse => {
            //console.log(respnse.json());
            return  respnse.json();
            
        })
        .then((data) => {

            scoredata = data.scores;
            jsonScore =  JSON.parse(scoredata);
            scoreone = jsonScore.topic_1;
            scoretwo = jsonScore.topic_2;
            scorethree = jsonScore.topic_3;
            const scoreNode = document.createElement("td");
            scoreNode.innerHTML = scoreone + " , " + scoretwo + " , " +  scorethree;
            newTr.appendChild(scoreNode);


   
        })
        .catch(error => console.error('Error: ', error));

        parent.appendChild(newTr);





     }


});