document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('popular-times-chart').getContext('2d');

  // static example data
  const labels = ['8 – 10 AM', '10 – 11 AM', '1 – 2 PM'];
  const dataPoints = [6, 8, 4];

  // create horizontal bar chart
  window.popularTimesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Users',
        data: dataPoints,
        backgroundColor: 'rgba(79, 133, 229, 1)',
        barPercentage: 0.6,
        categoryPercentage: 0.7
      }]
    },
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          beginAtZero: true,
          grid: { display: false },
          ticks: { stepSize: 1 }
        },
        y: {
          grid: { display: false }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true }
      }
    }
  });

  // handle week‐selector changes (hook if you add dynamic data later)
  document.getElementById('week-selector').addEventListener('change', (e) => {
    const week = e.target.value;
    // e.g. fetch new data based on `week` then:
    // renderPopularTimesChart(newLabels, newData);
  });
});

/**
 * If you later fetch new labels/data, call this to re-render:
 */
function renderPopularTimesChart(newLabels, newData) {
  popularTimesChart.data.labels = newLabels;
  popularTimesChart.data.datasets[0].data = newData;
  popularTimesChart.update();
}
