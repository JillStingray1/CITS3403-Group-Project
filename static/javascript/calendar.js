// static/javascript/calendar.js

// — helpers —
function loadTasks() {
    return JSON.parse(localStorage.getItem('tasks') || '[]');
  }
  function saveTasks(tasks) {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }
  function localISO(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth()+1).padStart(2,'0');
    const day = String(d.getDate()).padStart(2,'0');
    return `${y}-${m}-${day}`;
  }
  function isSameDay(a,b) {
    return a.getFullYear()===b.getFullYear()
        && a.getMonth()   ===b.getMonth()
        && a.getDate()    ===b.getDate();
  }
  function formatWhen(isoDate) {
    const d = new Date(isoDate);
    const today = new Date(); today.setHours(0,0,0,0);
    if (isSameDay(d,today)) return 'Today';
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate()+1);
    if (isSameDay(d,tomorrow)) return 'Tomorrow';
    return d.toLocaleString('default',{ weekday: 'long' });
  }
  
  // –– DEMO SEED – only seed if there are absolutely no tasks yet
  const existing = loadTasks();
  if (existing.length === 0) {
    const now = new Date();
    const demo = {
        name: "Demo Meeting",
        due:   localISO(now),
        time:  "10:00 AM"
    };
    saveTasks([ demo ]);
  }


  
  // — RENDER ACTIVITIES —
  function renderActivities() {
    const all = loadTasks();
    const midpoint = new Date(), curTbody = document.getElementById('current-activities'),
          pastTbody = document.getElementById('past-activities');
    midpoint.setHours(0,0,0,0);
    curTbody.innerHTML = ''; pastTbody.innerHTML = '';
    all.forEach(t=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${t.name}</td>
                      <td>${formatWhen(t.due)}</td>
                      <td>${t.time}</td>`;
      const dueDate = new Date(t.due);
      if (dueDate < midpoint) pastTbody.appendChild(tr);
      else curTbody.appendChild(tr);
    });
  }
  
  // — RENDER CALENDAR —
  function renderCalendar(year,month) {
    const daysEl = document.getElementById('calendar-days');
    daysEl.innerHTML = '';
    // header title
    const title = document.getElementById('calendar-title');
    const monthName = new Date(year,month).toLocaleString('default',{month:'long'});
    title.textContent = `${monthName} ${year}`;
  
    const firstWeekday = new Date(year,month,1).getDay();
    const numDays      = new Date(year,month+1,0).getDate();
    const today        = new Date(); today.setHours(0,0,0,0);
    // blanks
    for (let i=0; i<firstWeekday; i++) {
      const b = document.createElement('div'); b.className='blank';
      daysEl.appendChild(b);
    }
    // days
    const all = loadTasks();
    for (let d=1; d<=numDays; d++) {
      const cell = document.createElement('div');
      const dt   = new Date(year,month,d);
      cell.textContent = d;
      if (isSameDay(dt,today)) cell.classList.add('today');
      // attach tasks
      const iso = localISO(dt);
      const dayTasks = all.filter(t=>t.due===iso);
      if (dayTasks.length) {
        cell.classList.add('has-task');
        cell.dataset.tasks = JSON.stringify(dayTasks);
        cell.addEventListener('mouseenter', e=>{
          const tip = document.createElement('div');
          tip.className = 'tooltip';
          JSON.parse(e.target.dataset.tasks).forEach(t=>{
            const row = document.createElement('div');
            row.className = 'item';
            row.innerHTML = `<span class="icon">🕒</span> ${t.time} — ${t.name}`;
            tip.appendChild(row);
          });
          document.body.appendChild(tip);
          const r = e.target.getBoundingClientRect();
          tip.style.top  = `${r.top - tip.offsetHeight - 8}px`;
          tip.style.left = `${r.left + r.width/2 - tip.offsetWidth/2}px`;
          e.target._tooltip = tip;
        });
        cell.addEventListener('mouseleave', e=>{
          e.target._tooltip?.remove();
        });
      }
      daysEl.appendChild(cell);
    }
  }
  
  // initialize & wire controls
  let view = new Date(), viewYear = view.getFullYear(), viewMonth = view.getMonth();
  renderActivities();
  renderCalendar(viewYear,viewMonth);
  document.getElementById('prev-month').addEventListener('click', ()=>{
    viewMonth--; if (viewMonth<0) {viewMonth=11; viewYear--;}
    renderCalendar(viewYear,viewMonth);
  });
  document.getElementById('next-month').addEventListener('click', ()=>{
    viewMonth++; if (viewMonth>11) {viewMonth=0; viewYear++;}
    renderCalendar(viewYear,viewMonth);
  });
  