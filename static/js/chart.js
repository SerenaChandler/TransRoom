const chartButton = document.querySelectorAll("#show-chart-form");
const hideChartButton = document.querySelectorAll("#hide-chart-form");

function getChartData(evt) {
  evt.preventDefault();
  const restroom_id = evt.target.children[0].value;
  console.log(restroom_id);
  const chartContainer = document.querySelector(
    `#chart-container${restroom_id}`
  );
  chartContainer.innerHTML = "";
  chartContainer.insertAdjacentHTML(
    "afterbegin",
    `<canvas id="myChart${restroom_id}"></canvas>`
  );
  fetch(`/chart-data/${restroom_id}`)
    .then((res) => res.json())
    .then((chartData) => {
      console.log(chartData);

      const labels = [1, 2, 3, 4, 5];

      const data = {
        labels: labels,
        datasets: [
          {
            label: "Restroom Ratings",
            backgroundColor: [
              "rgb(179, 246, 255)",
              "rgb(255, 224, 251)",
              "rgb(179, 246, 255",
              "rgb(255, 224, 251)",
              "rgb(179, 246, 255)",
            ],
            data: chartData,
          },
        ],
      };

      const config = {
        type: "bar",
        data: data,
        options: {
          maintainAspectRatio: false,
        },
      };

      console.log(`#myChart${restroom_id}`);
      const myChart = new Chart(
        document.querySelector(`#myChart${restroom_id}`),
        config
      );
    });
}

function hideChart(evt) {
  evt.preventDefault();
  const restroom_id = evt.target.children[0].value;
  const chartContainer = document.querySelector(
    `#chart-container${restroom_id}`
  );
  chartContainer.innerHTML = "";
}

for (let button of hideChartButton) {
  button.addEventListener("submit", hideChart);
}

for (let button of chartButton) {
  button.addEventListener("submit", getChartData);
}
