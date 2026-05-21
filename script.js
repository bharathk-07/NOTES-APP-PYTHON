// SEARCH NOTES

document
.getElementById("search")
.addEventListener("keyup", function(){

    let value =
    this.value.toLowerCase();

    let notes =
    document.querySelectorAll(".note");

    notes.forEach(note => {

        note.style.display =
        note.innerText
        .toLowerCase()
        .includes(value)

        ? "block"
        : "none";

    });

});


// OPEN EDIT MODAL

function openEdit(id, title, content){

    document
    .getElementById("modal")
    .style.display = "block";

    document
    .getElementById("editTitle")
    .value = title;

    document
    .getElementById("editContent")
    .value = content;

    document
    .getElementById("editForm")
    .action = "/edit/" + id;

}


// CLOSE MODAL

function closeModal(){

    document
    .getElementById("modal")
    .style.display = "none";

}


// CLOSE OUTSIDE CLICK

window.onclick = function(e){

    let modal =
    document.getElementById("modal");

    if(e.target == modal){

        closeModal();

    }

}