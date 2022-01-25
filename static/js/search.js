const commentButtons = document.querySelectorAll(".comment-form");

const showCommentButton = document.querySelectorAll("#comment-button-form");

const hideCommentsButton = document.querySelectorAll(
  "#hide-comment-button-form"
);

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
        if (
          document.querySelector(`#comment-list${restroom_id}`).innerHTML !== ""
        ) {
          showComments(evt);
        }
        document.querySelector("#comment-success").innerHTML = resj.status;
        document.querySelector(
          `#rating${resj.restroom_id}`
        ).innerHTML = `${resj.rating}/5`;
      });
  } else {
    alert("please enter a comment before submitting rating");
  }
}

function showComments(evt) {
  evt.preventDefault();

  const restroom_id = evt.target.children[0].value;
  const commentList = document.querySelector(`#comment-list${restroom_id}`);
  commentList.innerHTML = "";

  fetch(`/restroom/${restroom_id}`)
    .then((res) => res.json())
    .then((comments) => {
      if (Object.keys(comments["comments"]).length < 1) {
        commentList.insertAdjacentHTML(
          "beforeend",
          `<h4 class="comments">No Comments Yet</h4>`
        );
      }
      for (let i = 0; i < Object.keys(comments["comments"]).length; i++) {
        commentList.insertAdjacentHTML(
          "afterbegin",
          `<h2 class="comments">${comments["comments"][i]}: ${comments["rating"][i]}/5</h2>`
        );
      }
    });
}

function hideComments(evt) {
  evt.preventDefault();
  const restroom_id = evt.target.children[0].value;
  const commentList = document.querySelector(`#comment-list${restroom_id}`);
  commentList.innerHTML = "";
}

for (button of commentButtons) {
  button.addEventListener("submit", leave_comment);
}

for (button of showCommentButton) {
  button.addEventListener("submit", showComments);
}

for (button of hideCommentsButton) {
  button.addEventListener("submit", hideComments);
}

document.addEventListener("DOMContentLoaded", () => {

  const socket = io.connect(
    "https://" + document.domain + ":" + location.port,
    { secure: true },
    { transports: ["websocket"] }
  );



})

// $(document).ready(function () {
//   const socket = io.connect(
//     "https://" + document.domain + ":" + location.port,
//     { secure: true },
//     { transports: ["websocket"] }
//   );

  // var socket = io.connect('http://' + document.domain + ":" + location.port);

  // socket.on('connect', function() {
  // 	socket.send('User has connected!');
  // });

  // socket.on('message', function(msg) {
  // 	$("#messages").append('<li>'+msg+'</li>');
  // 	console.log('Received message');
  // });

  // $('#sendbutton').on('click', function() {
  // 	socket.send($('#myMessage').val());
  // 	$('#myMessage').val('');
  // });
// });
