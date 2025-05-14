let page = 1

let timeslots = [];

const nextpage = document.getElementById("next-day");
const prevpage = document.getElementById("prev-day");
const grid = document.getElementById("calendar-grid");
const dateEl = document.getElementById("current-date");

/**
 * Convert a 15-minute slot index into a time string, cycling every
 * 32 slots (09:00–17:00).
 * 
 * @param {number} order
 *   Non-negative integer slot index (0 → day 0 @ 09:00, 32 → day 1 @ 09:00).
 * @returns {{ dayOffset: number, time: string }}
 *   dayOffset:  0 for the first day, 1 for the next, etc.
 *   time:       "HH:MM" between "09:00" and "16:45".
 * @throws {Error}
 *   If `order` isn’t a non-negative integer.
 */
function getTimeFromOrder(order) {
  // how many 15-min slots in a 9→17 day?
  const SLOTS_PER_DAY = (17 - 9) * 4; // 8h × 4 = 32

  // which day (0-based) and which slot within that day
  const dayOffset  = Math.floor(order / SLOTS_PER_DAY);
  const slotInDay  = order % SLOTS_PER_DAY;

  // minutes past midnight for 09:00 plus slotInDay × 15
  const totalMins  = 9 * 60 + slotInDay * 15;
  const hours      = Math.floor(totalMins / 60);
  const mins       = totalMins % 60;

  // format to "HH:MM"
  const hh = String(hours).padStart(2, "0");
  const mm = String(mins ).padStart(2, "0");

  return {time: `${hh}:${mm}` };
}


function setDate(date, dateEl){
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        dateEl.textContent = `${days[date.getDay()]}, ${date.getDate()}-${date.getMonth()}-${date.getFullYear()}`;
}


function renderTimeslots(timeslots, username){

    timeslots.forEach(timeslot => {
        const timeDiv = document.createElement("p");
        timeDiv.display = "inline-block";
        if (timeslot.unavailable_users.includes(username)){
            timeDiv.className = "time-slot unavailable";
        } else {
            timeDiv.className = "time-slot available";
        }
        timeDiv.textContent = timeslot.time;
        grid.appendChild(timeDiv);
        timeDiv.addEventListener("click", () => {
               fetch(`/meeting/timeslot`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf
        },
        body: JSON.stringify({timeslots: [{timeslot_id:timeslot.id}]}) 
    }).then(response => {
        if (response.ok) {
            let clickedSlot = timeslots.find(slot => slot.id === timeslot.id);
            clickedSlot.unavailable_users.push(username);
            timeDiv.classList.toggle("available");
            timeDiv.classList.toggle("unavailable");
        }
    }).catch(err => {
        console.error(err);
        alert("Something went wrong.");
    });
        });
    });
}


    fetch(`/meeting`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        };
        return response.json();
    }).then(data => {
        let date = new Date(data.start_date);
        timeslots = data.timeslots;
        username = data.username;
        timeslots.forEach((timeslot) => {
            timeslot.time = getTimeFromOrder(timeslot.order).time;
        })
        maxpages = timeslots.length/32
        console.log(timeslots)
        firstpage = timeslots.slice(0, 31);
        setDate(date, dateEl);
        renderTimeslots(firstpage, username);

        prevpage.disabled = true;
        nextpage.addEventListener("click", () => {

            page++;
            if (page > 1){
                prevpage.disabled = false;
            }
            if (page >= maxpages){
                nextpage.disabled = true;
            }
            date.setDate(date.getDate() + 1);
            setDate(date, dateEl);
            grid.innerHTML = '';
            renderTimeslots(timeslots.slice((page-1)*32, page*32), username);
        
        })

        prevpage.addEventListener("click", () => {
            page--;
            if (page < maxpages){
                nextpage.disabled = false;
            }
            if (page <= 1){
                prevpage.disabled = true;
            }
            date.setDate(date.getDate() - 1);
            setDate(date, dateEl);
            grid.innerHTML = '';
            renderTimeslots(timeslots.slice((page-1)*32, page*32), username);
        })

    })
