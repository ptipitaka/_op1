dragElement(document.getElementById("mydiv"));

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        /* if present, the header is where you move the DIV from:*/
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        /* otherwise, move the DIV from anywhere inside the DIV:*/
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
    }
}


// // auto height textarea
// const txHeight = 16;
// const tx = document.getElementsByTagName("textarea")        // 
// for (let i = 0; i < tx.length; i++) {
//     if (tx[i].value == '') {
//         tx[i].setAttribute("style", "height:" + txHeight + "px;overflow-y:hidden;");
//     } else {
//         tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight + 40) + "px;overflow-y:hidden;");
//     }
//     tx[i].addEventListener("input", OnInput, false);
// 
// function OnInput(e) {
//     this.style.height = 0;
//     this.style.height = (this.scrollHeight + 40) + "px";
// }

// make the DIV element draggagle //