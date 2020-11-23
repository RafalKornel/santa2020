const namesSubform = document.querySelector("#names-subform");
const node = namesSubform.querySelector(".form-group");
const input = node.getElementsByTagName("input")[0];


let i = namesSubform.childElementCount - 1;

function inpOnEnter(event) {
    console.log(event.key);

    if (event.key === "Enter") {
    event.preventDefault();
    copyNameNode();
  }
}

input.addEventListener("keydown", (e) => inpOnEnter(e));


function copyNameNode() {
    console.log("adding ", i);
    let idStr = `names-${i}-name`;
    let copy = node.cloneNode(true);
    copy.id = `name-field-${i}`;
    copy.querySelector("label").htmlFor = idStr;
    copy.querySelector("input").value = "";
    copy.querySelector("input").id = idStr;
    copy.querySelector("input").name = idStr;
    copy.querySelector("input").addEventListener("keydown", (e) => inpOnEnter(e));

    namesSubform.appendChild(copy);

    copy.querySelector("input").focus();
    
    i += 1;
}