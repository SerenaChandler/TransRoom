const charts = document.querySelectorAll("#myChart");

for (let chart of charts) {
  const labels = [1, 2, 3, 4, 5];

  const data = {
    labels: labels,
    datasets: [
      {
        label: "My First dataset",
        backgroundColor: [
          "rgb(255, 255, 255)",
          "rgb(255, 224, 251)",
          "rgb(179, 246, 255",
          "rgb(255, 224, 251)",
          "rgb(179, 246, 255)",
        ],
        data: [0, 0, 2, 20, 30],
      },
    ],
  };

  const config = {
    type: "pie",
    data: data,
    options: {
      maintainAspectRatio: false,
    },
  };

  newChart = new Chart(chart, config);
}
