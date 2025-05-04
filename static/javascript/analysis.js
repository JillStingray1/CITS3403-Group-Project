// static/javascript/analysis.js

/**
 * Populate the “Week of” dropdown with this week + next 3 weeks.
 * Weeks start on Monday.
 */
function populate_week_options() {
  const selector = document.getElementById('week-select');
  if (!selector) return;

  const today = new Date();
  const dayOfWeek = today.getDay();           // 0=Sun…6=Sat
  const offsetToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  const monday = new Date(today);
  monday.setDate(today.getDate() + offsetToMonday);

  // Clear any placeholder options
  selector.innerHTML = '';

  for (let i = 0; i < 4; i++) {
    const wk = new Date(monday);
    wk.setDate(monday.getDate() + 7 * i);
    const display = wk.toLocaleDateString('default', {
      month: 'long',
      day:   'numeric',
      year:  'numeric'
    });
    const value = wk.toISOString().slice(0, 10);
    const opt = document.createElement('option');
    opt.value = value;
    opt.textContent = display;
    selector.appendChild(opt);
  }
}

/**
 * Render the “Most Popular Free Times” stats table.
 * Uses demo data.
 */
function render_stats_table() {
  const tbody = document.getElementById('stats-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  // — DEMO DATA —
  const demoStats = [
    { slot: '8 – 10 AM',  users:  6 },
    { slot: '10 – 11 AM', users:  8 },
    { slot: '1 – 2 PM',   users:  4 }
  ];

  demoStats.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${item.slot}</td><td>${item.users}</td>`;
    tbody.appendChild(tr);
  });
}

/**
 * Render the heat-map grid; draws a blank corner, weekday headers,
 * time-labels down the left, and lightly coloured demo cells.
 */
function render_heatmap() {
  const grid = document.getElementById('heatmap-grid');
  if (!grid) return;
  grid.innerHTML = '';

  // — DEMO CONFIG —
  const days  = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const slots = ['9 AM','10 AM','11 AM','1 PM','4 PM'];
  const demoHeat = [
    [0, 2, 1, 3, 2, 0, 1],
    [1, 0, 4, 2, 3, 1, 0],
    [0, 1, 3, 5, 4, 2, 1],
    [2, 3, 0, 1, 2, 0, 0],
    [1, 0, 2, 3, 1, 0, 1]
  ];

  // 1) blank top-left
  grid.appendChild(document.createElement('div'));

  // 2) weekday headers
  days.forEach(d => {
    const h = document.createElement('div');
    h.className = 'heatmap-header';
    h.textContent = d;
    grid.appendChild(h);
  });

  // 3) find max (for colour scaling)
  const maxVal = demoHeat.flat().reduce((m, v) => Math.max(m, v), 1);

  // 4) for each time slot: label + cells
  slots.forEach((slot, i) => {
    // time label
    const lbl = document.createElement('div');
    lbl.className = 'heatmap-row-label';
    lbl.textContent = slot;
    grid.appendChild(lbl);

    // cells
    days.forEach((_, j) => {
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      const val = demoHeat[i][j] || 0;
      if (val > 0) {
        const t = val / maxVal;
        // interpolate between pale yellow (#FFECB3) and deep orange (#FF9800)
        const [r0,g0,b0] = [255,236,179];
        const [r1,g1,b1] = [255,152,0];
        const r = Math.round(r0 + (r1-r0)*t);
        const g = Math.round(g0 + (g1-g0)*t);
        const b = Math.round(b0 + (b1-b0)*t);
        cell.style.background = `rgb(${r},${g},${b})`;
      }
      grid.appendChild(cell);
    });
  });
}

/**
 * Render a demo pie-chart of “Availability by Day” using Chart.js,
 * and build a matching legend to its left.
 */
function render_pie_chart() {
  const legendHolder = document.getElementById('pie-legend');
  const canvasHolder = document.getElementById('pie-chart-large');
  legendHolder.innerHTML = '';
  canvasHolder.innerHTML = '<canvas id="pieCanvas"></canvas>';

  const ctx = document.getElementById('pieCanvas').getContext('2d');
  ctx.canvas.width  = 300;
  ctx.canvas.height = 300;

  // — DEMO DATA —
  const demoPie = [
    { day: 'Monday', pct: 20, color: '#4f6cff' },
    { day: 'Tuesday', pct: 15, color: '#42b983' },
    { day: 'Wednesday', pct: 25, color: '#ffcc00' },
    { day: 'Thursday', pct: 10, color: '#ff5733' },
    { day: 'Friday', pct: 20, color: '#33c3ff' },
    { day: 'Saturday/Sunday', pct: 10, color: '#FFB74D' }
  ];

  // build legend
  const ul = document.createElement('ul');
  demoPie.forEach(item => {
    const li = document.createElement('li');
    const sw = document.createElement('span');
    sw.className = 'swatch';
    sw.style.background = item.color;
    li.appendChild(sw);
    li.append(`${item.day}: ${item.pct}%`);
    ul.appendChild(li);
  });
  legendHolder.appendChild(ul);

  // draw the pie
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: demoPie.map(d=>d.day),
      datasets: [{
        data:  demoPie.map(d=>d.pct),
        backgroundColor: demoPie.map(d=>d.color),
        borderWidth: 0
      }]
    },
    options: {
      responsive:      true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    }
  });
}

/**
 * On any week change (or initial load) we re-render everything.
 */
function on_week_change() {
  render_stats_table();
  render_heatmap();
  render_pie_chart();
}

// — Initialize on page load —
document.addEventListener('DOMContentLoaded', () => {
  populate_week_options();
  const sel = document.getElementById('week-select');
  if (sel) sel.addEventListener('change', on_week_change);
  on_week_change();
});
