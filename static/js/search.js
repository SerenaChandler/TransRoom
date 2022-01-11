


// const searchButton = document.querySelector("#search-form")



// function search_restrooms(evt){
//     evt.preventDefault();
//     const APIURL = "http://www.refugerestrooms.org/api/v1/restrooms/search?page=1&per_page=10&offset=0&query=";
//     const value = document.querySelector("#search-text").value;
//     let query = APIURL + value
//     console.log(query)
//     fetch(`/${query}`)
//     .then(res => console.log(res))
//     .then(data => {
//         console.log(data)
//     })
// }

// searchButton.addEventListener("submit", search_restrooms)

const commentButton = document.querySelector("#comment-form")

function leave_comment(evt){
    evt.preventDefault()
    const restroom_id = document.querySelector("#hidden-restroom-id").value
    const formInputs = {
    rating: document.querySelector('input[name="rating"]:checked').value,
    text: document.querySelector("#comment_text").value }

    fetch(`/comment/${restroom_id}`, {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
          },
    }).then(res => res.json())
    .then(resj => alert(resj.status));
}

commentButton.addEventListener("submit", leave_comment)



