const anim = document.querySelector("#anim");
const names = anim.getElementsByClassName("name");

let name_values = [...names].map((e) => e.textContent);
let height = 100 / names.length;
let speed = 1;
let RAF;
let current_person;
let stopOn = "";
let slowDown = false;
let stop = false;
let slowDownRate = 0.05;

for (let i = 0; i < names.length; i++) {
  let e = names[i];
  let y = (i * height) % 100;
  e.style.top = `${y}%`;
  e.style.opacity = `${Math.sin((y * Math.PI) / 100) * 100}%`;
}

function animate(n) {
  anim.style.minHeight = `${anim.parentElement.offsetHeight}px`;

  if (slowDown) {
    if (speed > 1) {
      speed -= slowDownRate;
    } else {
      slowDown = false;
      setTimeout(() => {
        stop = true;
      }, 2000);
    }
  }

  for (let i = 0; i < names.length; i++) {
    let e = names[i];
    let y = (i * height + n) % 100;

    e.style.top = `${y}%`;
    e.style.opacity = `${Math.sin((y * Math.PI) / 100) * 100}%`;

    if (Math.abs(y - 50) < 1) {
      if (stopOn == e.textContent && stop) {
        current_person = e;
        stopAnimation();
        showWylosowana();
        return;
      }
    }
  }

  n += speed;

  RAF = requestAnimationFrame(() => animate(n));
}

function stopAnimation() {
  cancelAnimationFrame(RAF);
  current_person.style.color = "red";
  stopOn = undefined;
  slowDown = false;
  stop = false;
}

function showWylosowana() {
  const w = document.querySelector("#wylosowana");
  const d = document.querySelector("#do-wylosowania");

  w.style.display = "block";
  d.style.display = "none";
}

async function draw() {
  if (slowDown || stop) return;

  if (current_person) current_person.style.color = "black";

  speed = 10;

  cancelAnimationFrame(RAF);
  animate(0);

  const divisor = document.querySelector("#divisor");
  if (divisor) {
    divisor.style.display = "none";
  }

  const btncontainer = document.querySelector("#btn-container");
  if (btncontainer) {
    btncontainer.style.display = "none";
  }

  let splicedScheme = window.location.href.split("/");
  let group = splicedScheme[splicedScheme.length - 1];

  let draftName = await fetch(`/draw/${group}`)
    .then((res) => res.text())
    .catch((err) => console.error(err));

  stopOn = draftName;
  slowDown = true;

  document.querySelector("#osoba-name").textContent = draftName;
}

animate(0);
