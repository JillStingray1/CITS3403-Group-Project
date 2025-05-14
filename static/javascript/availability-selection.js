const selected_slots = [];
const dateRange = generateDateRange(startDate, endDate);
let currentDateIndex = 0;

function generateDateRange(start, end) {
  const result = [];
  let current = new Date(start);
  const endDate = new Date(end);

  while (current <= endDate) {
    result.push(new Date(current).toISOString().split('T')[0]);
    current.setDate(current.getDate() + 1);
  }

  return result;
}


function render_calendar() {
  const time_column = document.getElementById("time-column");
  const slots_column = document.getElementById("slots-column");

  time_column.innerHTML = "";
  slots_column.innerHTML = "";

  const dateStr = dateRange[currentDateIndex];
  const dateDisplay = document.getElementById("current-date");
  if (dateDisplay) {
    dateDisplay.textContent = new Date(dateStr).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }
  document.getElementById("current-date").textContent = dateStr;

  for (let hour = 9; hour < 17; hour++) {
    for (let quarter = 0; quarter < 60; quarter += 15) {
      const timeStr = `${String(hour).padStart(2, "0")}:${String(quarter).padStart(2, "0")}`;

      const timeDiv = document.createElement("div");
      timeDiv.className = "time-label";
      timeDiv.textContent = timeStr;

      const slotDiv = document.createElement("div");
      slotDiv.className = "time-slot";
      
      const isSelected = selected_slots.some(
        s => s.date === dateStr && s.time === timeStr
      );
      if (isSelected) {
        slotDiv.classList.add("selected");
      }


      if (hour === 16 && quarter > 45) {
        slotDiv.classList.add("disabled");
        slotDiv.style.pointerEvents = "none";
      }

      slotDiv.addEventListener("click", () => {
        if (slotDiv.classList.contains("disabled")) return;

        slotDiv.classList.toggle("selected");

        const index = selected_slots.findIndex(
          s => s.date === dateStr && s.time === timeStr
        );

        if (index !== -1) {
          selected_slots.splice(index, 1);
        } else {
          selected_slots.push({ date: dateStr, time: timeStr });
        }
      });

      time_column.appendChild(timeDiv);
      slots_column.appendChild(slotDiv);
    }
  }
}

document.getElementById("prev-day").addEventListener("click", () => {
  if (currentDateIndex > 0) {
    currentDateIndex--;
    render_calendar();
  }
});

document.getElementById("next-day").addEventListener("click", () => {
  if (currentDateIndex < dateRange.length - 1) {
    currentDateIndex++;
    render_calendar();
  }
});



document.addEventListener("DOMContentLoaded", render_calendar);

document.querySelector("#submit-button").addEventListener("click", () => {
  if (selected_slots.length === 0) {
    alert("Please select at least one slot before submitting!");
    return;
  }

  fetch(`/submit-availability?meeting_id=${meetingId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slots: selected_slots })
  }).then(response => {
    if (response.ok) {
      window.location.href = "/main-menu";
    } else {
      alert("Error submitting availability.");
    }
  }).catch(err => {
    console.error(err);
    alert("Something went wrong.");
  });
});
