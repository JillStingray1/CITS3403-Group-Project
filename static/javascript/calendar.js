// static/javascript/calendar.js

/**
 * Retries a list of meetings from the database, currently unimplemented 
 * 
 * @returns list of JSON objects which contains meeting details
 */
function load_tasks() {
    //! TODO: currently returns a demo task, should implement some 
    //! get request and data validation
    const now = new Date();
    return [{
        name: "Demo Meeting",
        due: local_ISO(now),
        time: "10:00 AM"
    },
    {
        name: "Demo Meeting 3",
        due: "2025-04-30",
        time: "10:00 AM"
    },
    {
        name: "Demo Meeting 2",
        due: "2024-04-27",
        time: "10:00 AM"
    },
    ];
}

/**
 * Converts a Date object into a string literal with date padding
 * 
 * 
 * @param {Date} d 
 * @returns 
 */
function local_ISO(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
}

/**
 * Compares the eqality of 2 Date objects
 * 
 * @param {Date} a 
 * @param {Date} b 
 * @returns Boolean value that represents equality
 */
function is_same_day(a, b) {
    return a.getFullYear() === b.getFullYear()
        && a.getMonth() === b.getMonth()
        && a.getDate() === b.getDate();
}


/**
 * Checks if a date object is either today, tomorrow, within the next week, 
 * or beyond, and returns a string accordingly.
 * 
 * @param {*} iso_date A date in ISO format
 * @returns "Today", "Tomorrow", "This [Weekday]", or the full date string
 */
function format_when(iso_date) {
    const d = new Date(iso_date);
    const today = new Date(); today.setHours(0, 0, 0, 0);
    if (is_same_day(d, today)) return 'Today';

    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    if (is_same_day(d, tomorrow)) return 'Tomorrow';

    const nextWeek = new Date(today);
    nextWeek.setDate(today.getDate() + 7);
    if (today < d && d < nextWeek) return `This ${d.toLocaleString('default', { weekday: 'long' })}`;

    return d.toLocaleDateString('default', { year: 'numeric', month: 'long', day: 'numeric' });
}


/**
 * Renders 2 lists of activities, depending on if the retrived activity is
 * before or after the current date
 */
function render_activities() {
    const all = load_tasks();
    const midpoint = new Date(), current_body = document.getElementById('current-activities'),
        pastTbody = document.getElementById('past-activities');
    midpoint.setHours(0, 0, 0, 0);
    current_body.innerHTML = ''; pastTbody.innerHTML = '';
    all.forEach(t => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${t.name}</td>
                      <td>${format_when(t.due)}</td>
                      <td>${t.time}</td>`;
        const dueDate = new Date(t.due);
        if (dueDate < midpoint) pastTbody.appendChild(tr);
        else current_body.appendChild(tr);
    });
}

/** Renders the calender on the main menu of the year and month passed to 
 *  the function
 * 
 * @param {number} year the year to display
 * @param {number} month the default month to display 
 */
function render_calendar(year, month) {
    const days_el = document.getElementById('calendar-days');
    days_el.innerHTML = '';
    // header title
    const title = document.getElementById('calendar-title');
    const month_name = new Date(year, month).toLocaleString('default', { month: 'long' });
    title.textContent = `${month_name} ${year}`;

    const first_weekday = new Date(year, month, 1).getDay();
    const num_days = new Date(year, month + 1, 0).getDate();
    const today = new Date(); today.setHours(0, 0, 0, 0);
    // blanks
    for (let i = 0; i < first_weekday; i++) {
        const b = document.createElement('div'); b.className = 'blank';
        days_el.appendChild(b);
    }
    // days
    const all = load_tasks();
    for (let d = 1; d <= num_days; d++) {
        const cell = document.createElement('div');
        const dt = new Date(year, month, d);
        cell.textContent = d;
        if (is_same_day(dt, today)) cell.classList.add('today');
        // attach tasks
        const iso = local_ISO(dt);
        const dayTasks = all.filter(t => t.due === iso);
        if (dayTasks.length) {
            cell.classList.add('has-task');
            cell.dataset.tasks = JSON.stringify(dayTasks);
            cell.addEventListener('mouseenter', e => {
                const tip = document.createElement('div');
                tip.className = 'tooltip';
                JSON.parse(e.target.dataset.tasks).forEach(t => {
                    const row = document.createElement('div');
                    row.className = 'item';
                    row.innerHTML = `<span class="icon">🕒</span> ${t.time} — ${t.name}`;
                    tip.appendChild(row);
                });
                document.body.appendChild(tip);
                const r = e.target.getBoundingClientRect();
                tip.style.top = `${r.top - tip.offsetHeight - 8}px`;
                tip.style.left = `${r.left + r.width / 2 - tip.offsetWidth / 2}px`;
                e.target._tooltip = tip;
            });
            cell.addEventListener('mouseleave', e => {
                e.target._tooltip?.remove();
            });
        }
        days_el.appendChild(cell);
    }
}


// Displays calendar and activities
let view = new Date(), view_year = view.getFullYear(), view_month = view.getMonth();
render_activities();
render_calendar(view_year, view_month);
document.getElementById('prev-month').addEventListener('click', () => {
    view_month--; if (view_month < 0) { view_month = 11; view_year--; }
    render_calendar(view_year, view_month);
});
document.getElementById('next-month').addEventListener('click', () => {
    view_month++; if (view_month > 11) { view_month = 0; view_year++; }
    render_calendar(view_year, view_month);
});
