var container = document.createElement('div');
container.setAttribute('id', 'container');
var train = document.createElement('div');
train.setAttribute('id', 'train');
var zones = document.createElement('div');
zones.setAttribute('id', 'zones');

container.appendChild(zones)
container.appendChild(train)

var carriagesElement = document.getElementById('carriages');
var zone_markersElement = document.getElementById('zone_markers');
var directionElement = document.getElementById('direction');
var zone_distancesElement = document.getElementById('zone_distances');
var stop_distanceElement = document.getElementById('stop_distance');


var carriagesText = carriagesElement.dataset.flaskVariable;
var zone_markersText = zone_markersElement.dataset.flaskVariable;
var directionText = directionElement.dataset.flaskVariable;
var zone_distancesText = zone_distancesElement.dataset.flaskVariable;
var stop_distanceText = stop_distanceElement.dataset.flaskVariable;

var carriages = carriagesText.split(/,(?![^\[\]]*])/);

zone_markersText =  zone_markersText.split("Decimal('")
zone_markersText =  zone_markersText.join("")
zone_markersText =  zone_markersText.split("')")
zone_markersText =  zone_markersText.join("")
zone_markersText =  zone_markersText.split("'")
zone_markersText =  zone_markersText.join('"')

var zone_markersJSON = JSON.parse(zone_markersText);

nb_carriages = carriages.length

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

var lastDistance = zone_distances[zone_distances.length - 1]; 
zone_distances.push(lastDistance); 
var totalDistance = zone_distances.reduce((sum, distance) => sum + distance, 0);

const groupedZones = {};
zone_markersJSON.forEach(element => {
    if (!groupedZones[element.ref]) {
        groupedZones[element.ref] = [];
    }
    groupedZones[element.ref].push(element);
});



const keys = Object.keys(groupedZones);

//interverti
if (isAntiAlphabetical(keys)) {
    invert = true;
}

if (invert) {
    if (directionText === "left") {
        directionText = "right"
    } else if (directionText === "right") {
        directionText = "left"
    }
}

if (invert) {
    keys.reverse();
}

if (invert) {
    carriages.reverse();
}
//fin interverti

var index = 0;
keys.forEach(ref => {
    const elements = groupedZones[ref];
    let totalOccurences = elements.length;
    
    distance = zone_distances[index];
    
    if (totalOccurences > 1) {
        for (let i = 1; i < totalOccurences; i++) {
            distance += zone_distances[index + i];
        }
        index = index + (totalOccurences-1);
    } else {
        distance = zone_distances[index];
    }
    index = index + 1;
   
    const zoneWidth = (100/ totalDistance) * distance;

    const div = document.createElement("div");
    div.setAttribute('class', 'zone');
    div.textContent = ref;
    div.style.width = zoneWidth + '%';
  


    zones.appendChild(div);
});

carriages.forEach((carriage, index)=>{
    div = document.createElement("div")
    div.setAttribute('class', 'cb')
    
    const carrWidth = (100/ totalDistance) * 18.4;
    div.style.width = carrWidth + '%';
    
    if (directionText === "left") {
        const decalWidth = (100/ totalDistance) * stop_distanceText;
        div.style.left = decalWidth + '%';
    } else if (directionText === "right") {
        const decalWidth = (100/ totalDistance) * stop_distanceText;
        var e = 100 - decalWidth ;
        div.style.left = e - (carrWidth*(nb_carriages+1)) + '%';
        console.log(carrWidth);
    }
    
   
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
            if  (directionText === "right" && nb_carriages == 1) {
                div.classList.add('locoR');
            } else {
                div.classList.add('locoL');
            }
        } else {
            div.classList.add('locoR');
        }
    }

    train.appendChild(div)
})


var arr = document.createElement('div');
arr.setAttribute('class', 'arrow');

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
}, 60000); // Rafraîchit la page toutes les 5 secondes (5000 millisecondes)
