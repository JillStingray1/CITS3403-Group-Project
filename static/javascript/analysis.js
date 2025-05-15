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
    const daysOffset = Math.floor(order / 32);
    const slotOffset = order % 32;
    const dt = new Date(start);
    dt.setHours(9, 0, 0, 0);
    dt.setDate(dt.getDate() + daysOffset);
    dt.setMinutes(dt.getMinutes() + slotOffset * 15);
    return dt;
}

window.onload = () => {
    console.log(top_scores)
    console.log(start_date)
    let date_lables = [];
    let unavaliability_scores = [];
    for (let i = 0; i < top_scores.length; i++) {
        date_lables.push(getBestTimeFromSlot(top_scores[i][0], start_date).toLocaleString("en-GB"));
        unavaliability_scores.push(top_scores[i][1])
    }

    console.log(date_lables)
    const ctx = document.getElementById('popular-times-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar', // Change to 'line', 'pie', etc., for different chart types
        data: {
            labels: date_lables,
            datasets: [{
                label: 'Unavaliability score',
                data: unavaliability_scores,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

