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
let stopOn = "";


for (let i = 0; i < names.length; i++) {
    let e = names[i];
    let y = (i * height) % 100;
    e.style.top = `${y}%`;
    e.style.opacity = `${Math.sin(y * Math.PI / 100) * 100}%`;
}

function animate(n) {

    for (let i = 0; i < names.length; i++) {
        let e = names[i];
        let y = (i * height + n * speed) % 100;

        e.style.top = `${y}%`;
        e.style.opacity = `${Math.sin(y * Math.PI / 100) * 100}%`;

        if (Math.abs(y  - 50) < 1) {
            if (stopOn == e.textContent) 
            {
                current_person = e;
                stopAnimation();
                return; 
            }
        }
    }

    n += 1;

    RAF = requestAnimationFrame(() => animate(n))
}


function stopAnimation() {
    cancelAnimationFrame(RAF);
    clearInterval(interval);
    current_person.style.color = "red";
    stopOn = undefined;
    timeouts = undefined;
}

async function draw() {
    if (timeouts) return;

    if (current_person) current_person.style.color = "black";

    cancelAnimationFrame(RAF);
    animate(0);

    let splicedScheme = window.location.href.split("/");
    let group = splicedScheme[ splicedScheme.length - 1];

    let draftName = await fetch(`/draw/${group}`)
                      .then(res => res.text())
                      .catch(err => console.error(err));

    speed = 10;
    timeouts = [
        setTimeout(() => speed = 7, 2000),
        setTimeout(() => speed = 5, 4000),
        setTimeout(() => speed = 3, 5000),
        setTimeout(() => speed = 1.5, 6000),
        setTimeout(() => speed = 1, 7000),
        setTimeout(() => stopOn = draftName, 8000),
    ]
}

animate(0);