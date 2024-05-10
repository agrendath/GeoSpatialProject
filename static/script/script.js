var container = document.createElement('div');
container.setAttribute('id', 'container'); 
var train = document.createElement('div');
train.setAttribute('id', 'train'); 
var zones = document.createElement('div');
zones.setAttribute('id', 'zones'); 

container.appendChild(zones)
container.appendChild(train)



//var variablesElement = document.getElementById('variables');

var carriagesElement = document.getElementById('carriages');
var zone_markersElement = document.getElementById('zone_markers');
var directionElement = document.getElementById('direction');

var carriagesText = carriagesElement.dataset.flaskVariable;
var zone_markersText = zone_markersElement.dataset.flaskVariable;
var directionText = directionElement.dataset.flaskVariable;


var carriages = carriagesText.split(/,(?![^\[\]]*])/);

zone_markersText =  zone_markersText.split("Decimal('")
zone_markersText =  zone_markersText.join("")
zone_markersText =  zone_markersText.split("')")
zone_markersText =  zone_markersText.join("")
zone_markersText =  zone_markersText.split("'")
zone_markersText =  zone_markersText.join('"')

var zone_markersJSON = JSON.parse(zone_markersText);

nb_carriages = carriages.length

/*const groupedZones = {};
zone_markersJSON.forEach(element => {
    if (!groupedZones[element.ref]) {
        groupedZones[element.ref] = [];
    }
    groupedZones[element.ref].push(element);
});

Object.keys(groupedZones).forEach(ref => {
    const elements = groupedZones[ref];
    let totalOccurences = elements.length;
    const div = document.createElement("div");
    div.setAttribute('class', 'zone');
    div.textContent = ref;

    if (totalOccurences > 1) {
        div.style.flexGrow = totalOccurences;
    }

    zones.appendChild(div);
});*/


//interverti
function isAntiAlphabetical(keys) {
    for (let i = 1; i < keys.length; i++) {
        if (keys[i] > keys[i - 1]) {
            return false;
        }
    }
    return true;
}

var invert = false;

const groupedZones = {};
zone_markersJSON.forEach(element => {
    if (!groupedZones[element.ref]) {
        groupedZones[element.ref] = [];
    }
    groupedZones[element.ref].push(element);
});

const keys = Object.keys(groupedZones);

if (isAntiAlphabetical(keys)) {
    invert = true;
}

if (invert) {
    keys.reverse();
}

keys.forEach(ref => {
    const elements = groupedZones[ref];
    let totalOccurences = elements.length;
    const div = document.createElement("div");
    div.setAttribute('class', 'zone');
    div.textContent = ref;

    if (totalOccurences > 1) {
        div.style.flexGrow = totalOccurences;
    }

    zones.appendChild(div);
});
//fin interverti

//interverti
if (invert) {
    carriages.reverse();
}
//fin interverti

carriages.forEach((carriage, index)=>{
    div = document.createElement("div")
    div.setAttribute('class', 'cb')
    div.setAttribute('style', 'width='+100/nb_carriages+"%")
    
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
    
    if (carriage.includes("(Luggage lockers)")) {
        div.innerHTML += "<div class='right-bottom'><i class='fa fa-lock'></i></div>";
    }
 
   //Classes
   if (carriage.includes("[1]")) {
        div.innerHTML += "<div class='middle'><span class='yellow'>1</span></div>";
    }else if (carriage.includes("[2]")) {
        div.innerHTML += "<div class='middle'>2</div>";
    }else if (carriage.includes("[1, 2]")) {
        div.innerHTML += "<div class='middle'><span class='yellow'>1</span>, 2</div>";
    }else  {
        if (index === 0) { 
            div.classList.add('locoL');
        } else {
            div.classList.add('locoR');     
        }   
    }
    
    train.appendChild(div)
})


var arr = document.createElement('div');
arr.setAttribute('class', 'arrow'); 

//interverti
if (invert) { //interverti
    if (directionText === "left") { 
        directionText = "right"
    } else if (directionText === "right") { 
        directionText = "left"
    } 
} 

//fin interverti

if (directionText === "left") { 
    arr.innerHTML = "<i class='fa fa-arrow-left'></i><i class='fa fa-arrow-left'></i><i class='fa fa-arrow-left'></i>";
} else if (directionText === "right") { 
    arr.innerHTML = "<i class='fa fa-arrow-right'></i><i class='fa fa-arrow-right'></i><i class='fa fa-arrow-right'></i>";
} 

container.appendChild(arr)

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
