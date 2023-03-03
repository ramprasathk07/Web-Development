const req=document.querySelectorAll(".req");
const hold=document.querySelectorAll(".hold");
let draggableT=null;


req.forEach((reqs) => {
    reqs.addEventListener("dragstart",dragStart);
    reqs.addEventListener("dragend",dragEnd);
});
function dragStart(){
    draggableT = this;
    console.log("dragstart");
}
function dragEnd(){
    draggableT = null;
    console.log("dragEnd");
}

hold.forEach(stats=>{
    stats.addEventListener("dragover",dragOver);
    stats.addEventListener("dragenter",dragEnter);
    stats.addEventListener("dragleave",dragLeave);
    stats.addEventListener("drop",dragDrop);

});
function dragOver(e){
    e.preventDefault();
    console.log("dragover");
}
function dragEnter(){
    console.log("dragenter");
}
function dragLeave(){
    console.log("dragleave");
}
function dragDrop(){
    this.appendChild(draggableT);
    console.log("dropped");
}