const namesSubform = document.querySelector("#names-subform");

let i = namesSubform.childElementCount - 1;

function copyNameNode() {
    let node = namesSubform.querySelector(".form-group");
    let idStr = `names-${i}-name`;
    let copy = node.cloneNode(true);
    copy.querySelector("label").htmlFor = idStr;
    copy.querySelector("input").value = "";
    copy.querySelector("input").id = idStr;
    copy.querySelector("input").name = idStr;
    namesSubform.appendChild(copy);
    
    i += 1;
}