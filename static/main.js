const anim = document.querySelector("#anim");
//const current = document.querySelector(".current_person")
const names = anim.getElementsByClassName("name");

let name_values = [ ...names ].map( (e) => e.textContent );
let height = 100 / names.length;
let speed = 1;
let RAF;
let interval;
let timeouts;
let current_person;


for (let i = 0; i < names.length; i++) {
    let e = names[i];
    let value = (i / names.length * 100) % 100;
    let y = value - height / 2
    e.style.top = `${y}%`;
    e.style.opacity = `${Math.sin(value * Math.PI / 100) * 100}%`;
}

function animate(n) {
    for (let i = 0; i < names.length; i++) {
        let e = names[i];
        let value = (i / names.length * 100 + n * speed) % 100;
        let y = value - height / 2
        if (Math.abs(y - 50) < height / 2 - 1) {
            current_person = e;
        }
        else {
            e.style.background = "";
        }
        e.style.top = `${y}%`;
        e.style.opacity = `${Math.sin(value * Math.PI / 100) * 100}%`;
    }

    n += 1;

    RAF = requestAnimationFrame(() => animate(n))
}

function stopOn(person) {
    if (current_person.textContent == person) {
        cancelAnimationFrame(RAF);
        clearInterval(interval);
        current_person.style.color = "red";
        timeouts = undefined;
    }
}

async function draw() {
    if (timeouts) return;

    current_person.style.color = "black";

    cancelAnimationFrame(RAF);
    animate(0);

    let splicedScheme = window.location.href.split("/");
    let group = splicedScheme[ splicedScheme.length - 1];

    let draft = await fetch(`/draw/${group}`)
                      .then(res => res.json())
                      .catch(err => console.error(err));

    let draftName = draft["name"];

    //let target = name_values[Math.floor(Math.random() * name_values.length)];
    
    speed = 10;
    timeouts = [
        setTimeout(() => speed = 5, 2000),
        setTimeout(() => speed = 2, 4000),
        setTimeout(() => speed = 1, 6000),
        setTimeout(() => {
            interval = setInterval(() => stopOn(draftName), 100);
        }, 8000),
    ]
}

animate(0);