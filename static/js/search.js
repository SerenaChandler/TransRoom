const commentButtons = document.querySelectorAll(".comment-form");

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
          document.querySelector(`#rating${resj.restroom_id}`).innerHTML = `${resj.rating}/5`
        } else {
          document.querySelector("#comment-success").innerHTML = resj.status;
        }
      });
  } else {
    alert("please enter a comment before submitting rating");
  }
}

for (button of commentButtons) {
  button.addEventListener("submit", leave_comment);
}
