


const searchButton = document.querySelector("#search-form")



function search_restrooms(evt){
    evt.preventDefault();
    const APIURL = "www.refugerestrooms.org/api/v1/restrooms/search?page=1&per_page=10&offset=0&query=";
    const value = document.querySelector("#search-text").value;
    let query = APIURL + value
    console.log(query)
    fetch(`/${query}`)
    .then(res => res.json())
    .then(data => {
        console.log(data)
    })
}

searchButton.addEventListener("submit", search_restrooms)
