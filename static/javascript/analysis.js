// static/javascript/analysis.js

/**
 * Converts a timeslot order (15-min ticks from 9am Day 0) into a JS Date.
 * Mirrors tool.py get_best_time_from_slot.
 *
 * @param {number} order  the timeslot index (0 = Day 0 @ 9:00, 1 = 9:15, …)
 * @param {Date}   start the meeting’s start_date as a JS Date
 * @returns {Date} the absolute date/time
 */
function getBestTimeFromSlot(order, start) {
  // floor(order / 32) days after start
  const daysOffset = Math.floor(order / 32);
  // remainder * 15 minutes after 9am
  const slotOffset = order % 32;
  const dt = new Date(start);
  dt.setHours(9, 0, 0, 0);
  dt.setDate(dt.getDate() + daysOffset);
  dt.setMinutes(dt.getMinutes() + slotOffset * 15);
  return dt;
}

/**
 * Fetches all timeslot data + meeting meta, computes the top-3
 * “most-available” windows, and re-renders your horizontal bar chart.
 */
async function loadAndRenderStats(meetingId) {
  // 1) Fetch timeslots and meta
  const [tsResp, metaResp] = await Promise.all([
    fetch(`/meeting/${meetingId}/all`),
    fetch(`/meeting/${meetingId}`)
  ]);
  const timeslots = await tsResp.json();       // [{ order, unavailable_users: [...] }, …]
  const { start_date, meeting_length, participants_count } = await metaResp.json();

  // 2) Prep
  const slotsNeeded = meeting_length / 15;
  const sorted      = [...timeslots].sort((a, b) => a.order - b.order);

  // 3) Slide a window of size slotsNeeded, summing unavailable counts
  const windowScores = [];
  for (let i = 0; i + slotsNeeded <= sorted.length; i++) {
    let sumUnavailable = 0;
    for (let j = 0; j < slotsNeeded; j++) {
      sumUnavailable += sorted[i + j].unavailable_users.length;
    }
    windowScores.push({ startOrder: sorted[i].order, totalUnavailable: sumUnavailable });
  }

  // 4) Find the top-10 windows with the fewest unavailable users
  windowScores.sort((a, b) => a.totalUnavailable - b.totalUnavailable);
  const top10 = windowScores.slice(0, 10);

  // 5) Turn them into human-readable labels & data points
  const labels = top10.map(w => {
    const startDT = getBestTimeFromSlot(w.startOrder, new Date(start_date));
    const endDT   = getBestTimeFromSlot(w.startOrder + slotsNeeded, new Date(start_date));
    const fmt = d => d.toLocaleDateString('default',{ day:'numeric', month:'short' });
    return `${fmt(startDT)} – ${fmt(endDT)}`;
  });
  const data = top10.map(w => participants_count - w.totalUnavailable);

  // 6) Re-render your Chart.js bar chart
  renderPopularTimesChart(labels, data);
}


// ─── initialize on page load ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // first render with static example (optional), then load real data
  // renderPopularTimesChart(['13 May – 17 May','…','…'], [6,8,4]);
  loadAndRenderStats(meetingId);
});
