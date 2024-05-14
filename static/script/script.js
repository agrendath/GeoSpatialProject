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
var zone_distancesElement = document.getElementById('zone_distances');


var carriagesText = carriagesElement.dataset.flaskVariable;
var zone_markersText = zone_markersElement.dataset.flaskVariable;
var directionText = directionElement.dataset.flaskVariable;
var zone_distancesText = zone_distancesElement.dataset.flaskVariable;

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




var zone_distances = JSON.parse(zone_distancesText);

var lastDistance = zone_distances[zone_distances.length - 1]; /**/
zone_distances.push(lastDistance); /**/
var totalDistance = zone_distances.reduce((sum, distance) => sum + distance, 0);/**/
console.log(zone_distances);
console.log(totalDistance);


const groupedZones = {};
zone_markersJSON.forEach(element => {
    if (!groupedZones[element.ref]) {
        groupedZones[element.ref] = [];
    }
    groupedZones[element.ref].push(element);
});

console.log(groupedZones);

/*// Si vous voulez une liste de références et de distances à partir de groupedZones
const result = Object.values(groupedZones);

console.log(result);*/

const keys = Object.keys(groupedZones);

if (isAntiAlphabetical(keys)) {
    invert = true;
}

if (invert) {
    keys.reverse();
}


keys.forEach((ref, index) => {
    const elements = groupedZones[ref];
    let totalOccurences = elements.length;
    console.log(totalOccurences);
    const div = document.createElement("div");
    div.setAttribute('class', 'zone');
    div.textContent = ref;
    
    distance = zone_distances[index];

    if (totalOccurences > 1) {
        div.style.flexGrow = totalOccurences;
    }
    
    console.log(distance);

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
if (invert) {
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

setInterval(function(){
    window.location.reload();
}, 30000); // Rafraîchit la page toutes les 5 secondes (5000 millisecondes)
