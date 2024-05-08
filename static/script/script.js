var container = document.createElement('div');
container.setAttribute('id', 'container'); 
var train = document.createElement('div');
train.setAttribute('id', 'train'); 
var zones = document.createElement('div');
zones.setAttribute('id', 'zones'); 

container.appendChild(zones)
container.appendChild(train)

//affichage des zones
zones_names = "A,B,C,D,E"
zones_names = zones_names.split(",")

zones_names.forEach((zone)=>{
    div = document.createElement("div")
    div.setAttribute('class', 'zone')
    div.textContent = zone
    zones.appendChild(div)
})

var variablesElement = document.getElementById('variables');

//var carriages = variablesElement.dataset.flaskVariable;//.split(",");

var carriages2 = variablesElement.dataset.flaskVariable;

var expression = /,(?![^\[\]]*])/;

var carriages = carriages2.split(expression);

console.log(carriages)

nb_carriages = carriages.length
//var nb_carriages = composition_carriages
console.log(nb_carriages)

/*displayImages(div,carriage){
    if (condition) {
        
    }
}*/

carriages.forEach((carriage)=>{
    div = document.createElement("div")
    div.setAttribute('class', 'cb')
    div.setAttribute('style', 'width='+100/nb_carriages+"%")

    console.log(carriage)
    
    //Icons
    if (carriage.includes("(Accessible toilet)")) {
        div.innerHTML = "<div class='left-bottom'><i class='fa fa-wheelchair'></i></div>";
    }

    if (carriage.includes("(Toilet)")) {
        div.innerHTML += "<div class='left-top'><i class='fa fa-restroom'></i></div>";
    }
    
    if (carriage.includes("(Bike)")) {
        div.innerHTML += "<div class='right-top'><i class='fa fa-bicycle'></i></div>";
    }
    
   //Classes
   if (carriage.includes("[1]")) {
        div.innerHTML += "<div class='yellow'>1</div>";
    }else if (carriage.includes("[2]")) {
        div.innerHTML += "<div>2</div>";
    }else if (carriage.includes("[1, 2]")) {
        div.innerHTML += "<div><span class='yellow'>1</span>2</div>";
    }
    
    train.appendChild(div)
})


tchou = document.getElementById('tchoutchou');
tchou.appendChild(container)

/*
            <i class="fa fa-bicycle"></i><br>
            <i class="fa fa-wheelchair"></i><br>
            <i class="fa fa-arrow-right"></i>
            <i class="fa fa-arrow-left"></i><br>
            <i class="fa fa-arrow-circle-right"></i>
            <i class="fa fa-arrow-circle-left"></i><br>
            <i class="fa fa-volume-xmark"></i><br>
            <i class="fa fa-stairs"></i><br>
            <i class="fa fa-restroom"></i>
*/
