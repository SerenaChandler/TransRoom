const commentButtons = document.querySelectorAll(".comment-form");

const showCommentButton = document.querySelectorAll('#comment-button-form')

function leave_comment(evt) {
  evt.preventDefault();
  console.log(evt.target);
  const restroom_id = evt.target.children[0].value;
  const current_rating = evt.target.children;
  text = evt.target.children[1].value;
  const formInputs = {
    rating: evt.target.children[3].value,
    text: evt.target.children[1].value,
  };
  if (text != "") {
    fetch(`/comment/${restroom_id}`, {
      method: "POST",
      body: JSON.stringify(formInputs),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((resj) => {
        if (resj.success == true) {
          document.querySelector("#comment-success").innerHTML = resj.status;
          document.querySelector(`#rating${resj.restroom_id}`).innerHTML = `${resj.rating}/5`;
          alert("comment submitted")
        } else {
          document.querySelector("#comment-success").innerHTML = resj.status;
        }
      });
  } else {
    alert("please enter a comment before submitting rating");
  }
}

function showComments(evt) {
  evt.preventDefault()
  const commentList =document.querySelector('#comment-list')
  console.log(Object.keys(commentList.children).length)
  const restroom_id = evt.target.children[0].value;
  if (Object.keys(commentList.children).length === 0) {
  fetch(`/restroom/${restroom_id}`)
  .then(res => res.json())
  .then(comments =>{ 
    
    for (let i = 0; i < Object.keys(comments).length; i++) {
      commentList.insertAdjacentHTML('beforeend', `<li>${comments[i]}</li>`)
    }
    })
  }
}






for (button of commentButtons) {
  button.addEventListener("submit", leave_comment);
}


for (button of showCommentButton){
  button.addEventListener("submit", showComments);
}