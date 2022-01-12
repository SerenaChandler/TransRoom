

const commentButtons = document.querySelectorAll("#comment-form")
// const commentButton = document.querySelector(".comment-form")

function leave_comment(evt){
    evt.preventDefault()
    console.log(evt.target.children)
    const restroom_id = evt.target.children[0].value
    text = evt.target.children[1].value
    const formInputs = {
    rating: evt.target.children[3].value,
    text: evt.target.children[1].value }
    if(text != ""){
    fetch(`/comment/${restroom_id}`, {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
          },
    }).then(res => res.json())
    .then(resj => console.log("comment submitted"));
}else {
    alert("please enter a comment before submitting rating")
}

}

for (button of commentButtons){
button.addEventListener("submit", leave_comment)
}

// commentButton.addEventListener("submit", leave_comment)

