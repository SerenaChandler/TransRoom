const commentButtons = document.querySelectorAll(".comment-form");

const showCommentButton = document.querySelectorAll('#comment-button-form')

const hideCommentsButton = document.querySelectorAll('#hide-comment-button-form')

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
  const restroom_id = evt.target.children[0].value;
  const commentList =document.querySelector(`#comment-list${restroom_id}`)
  console.log(Object.keys(commentList.children).length)
  if (Object.keys(commentList.children).length === 0) {
  fetch(`/restroom/${restroom_id}`)
  .then(res => res.json())
  .then(comments =>{ 
    
    for (let i = 0; i < Object.keys(comments).length; i++) {
      commentList.insertAdjacentHTML('beforeend', `<h2 class="comments">${comments[i]}</h2>`)
    }
    })
  }
}

function hideComments(evt) {
  evt.preventDefault()
  const restroom_id = evt.target.children[0].value;
  const commentList =document.querySelector(`#comment-list${restroom_id}`)
  commentList.innerHTML=""
}




for (button of commentButtons) {
  button.addEventListener("submit", leave_comment);
}


for (button of showCommentButton){
  button.addEventListener("submit", showComments);
}

for (button of hideCommentsButton){
  button.addEventListener("submit", hideComments);
}