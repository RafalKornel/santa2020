const anim = document.querySelector("#anim");
const current = document.querySelector(".current_person")

let names = anim.getElementsByClassName("name");
let height = 100 / names.length;
let speed = 1;
let RAF;
let interval;
let timeouts;

let ref_names = ["Janek", "Asia", "Daria", "Karolina"];

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
            current_person = e.textContent;
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
    if (current_person == person) {
        cancelAnimationFrame(RAF);
        clearInterval(interval);
    }
}

function draw() {
    cancelAnimationFrame(RAF);
    if (timeouts) timeouts.map( (tim) => clearTimeout(tim) );

    animate(0);

    let target = ref_names[Math.floor(Math.random() * ref_names.length)];
    speed = 10;
    timeouts = [
        setTimeout(() => speed = 5, 2000),
        setTimeout(() => speed = 2, 4000),
        setTimeout(() => speed = 1, 6000),
        setTimeout(() => {
            interval = setInterval(() => stopOn(target), 100);
        }, 8000),
    ]
}

animate(0);