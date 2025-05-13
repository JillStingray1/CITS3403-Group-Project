document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('popular-times-chart').getContext('2d');

  // create the empty horizontal bar chart
  window.popularTimesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],        // will be populated dynamically
      datasets: [{
        label: 'Users',
        data: [],
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

  // load data once on startup
  loadPopularTimes();

  // if you have a week‐selector dropdown later:
  const sel = document.getElementById('week-selector');
  if (sel) {
    sel.addEventListener('change', e => loadPopularTimes(e.target.value));
  }
});

/**
 * Fetches raw stats from the server, picks the Top-3 free slots,
 * and calls renderPopularTimesChart().
 *
 * @param {string=} weekFilter  unused for now—if you add per-week data
 */
async function loadPopularTimes(weekFilter = null) {
  try {
    const resp = await fetch(`/meeting/${MEETING_ID}/stats`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const { total_users, timeslots, start_date } = await resp.json();

    // compute availability = total_users – unavailable.length per slot
    const availBySlot = timeslots.map(ts => ({
      order:       ts.order,
      available:   total_users - ts.unavailable.length
    }));

    // sort descending and pick top 3
    availBySlot.sort((a, b) => b.available - a.available);
    const top3 = availBySlot.slice(0, 3);

    // build labels like “8 – 10 AM” from ts.order if you know your mapping:
    // here’s a simple example assuming slot 0 = “8 – 9 AM”, slot 1 = “9 – 10 AM”, etc.
    const slotLabels = top3.map(s => {
      const startHour = 8 + s.order;
      const endHour   = startHour + 1;
      return `${startHour} – ${endHour} AM`;
    });
    const dataPoints = top3.map(s => s.available);

    renderPopularTimesChart(slotLabels, dataPoints);
  } catch (e) {
    console.error("Failed to load popular times:", e);
  }
}

/**
 * Updates the chart’s labels & data and re-draws it.
 */
function renderPopularTimesChart(newLabels, newData) {
  popularTimesChart.data.labels            = newLabels;
  popularTimesChart.data.datasets[0].data  = newData;
  popularTimesChart.update();
}
