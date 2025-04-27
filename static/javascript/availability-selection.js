// ---- SETTINGS ---- //
const meeting_duration_minutes = 15; // <<<< Change this value manually if needed
// ------------------- //

const dates = generate_dates(3); // today + 2 more
const formatted_dates = dates.map(date => format_date(date));

const time_slots = [
  "09:00", "09:15", "09:30", "09:45",
  "10:00", "10:15", "10:30", "10:45",
  "11:00", "11:15", "11:30", "11:45",
  "12:00", "12:15", "12:30", "12:45",
  "13:00", "13:15", "13:30", "13:45",
  "14:00", "14:15", "14:30", "14:45",
  "15:00", "15:15", "15:30", "15:45",
  "16:00", "16:15", "16:30", "16:45"
];

let current_day_index = 0;
let selected_slots = [];
const slots_needed = Math.ceil(meeting_duration_minutes / 15);

window.onload = () => {
  render_calendar();
  update_selected_slots_display();

  document.getElementById('prev-day').addEventListener('click', () => {
    if (current_day_index > 0) {
      current_day_index--;
      render_calendar();
      update_selected_slots_display();
    }
  });

  document.getElementById('next-day').addEventListener('click', () => {
    if (current_day_index < dates.length - 1) {
      current_day_index++;
      render_calendar();
      update_selected_slots_display();
    }
  });

  document.getElementById('slots-column').addEventListener('click', (event) => {
    if (event.target.classList.contains('time-slot') && !event.target.classList.contains('disabled')) {
      const clicked_slot = {
        date: dates[current_day_index],
        time: event.target.dataset.time
      };

      const index = selected_slots.findIndex(slot =>
        slot.date === clicked_slot.date && slot.time === clicked_slot.time
      );

      if (index !== -1) {
        selected_slots.splice(index, 1);
        event.target.classList.remove('selected');
      } else {
        selected_slots.push(clicked_slot);
        event.target.classList.add('selected');
      }

      update_selected_slots_display();
    }
  });
};

function generate_dates(num_days) {
  const today = new Date();
  const generated_dates = [];
  for (let i = 0; i < num_days; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    generated_dates.push(date.toISOString().split('T')[0]);
  }
  return generated_dates;
}

function render_calendar() {
  const time_col = document.getElementById('time-column');
  const slots_col = document.getElementById('slots-column');

  time_col.innerHTML = "";
  slots_col.innerHTML = "";

  const latest_valid_slot_index = time_slots.length - slots_needed;

  time_slots.forEach((time, index) => {
    const time_label = document.createElement('div');
    time_label.className = 'time-label';
    time_label.textContent = time;
    time_col.appendChild(time_label);

    const slot = document.createElement('div');
    slot.className = 'time-slot';
    slot.dataset.time = time;

    if (index > latest_valid_slot_index) {
      slot.classList.add('disabled');
    }

    if (selected_slots.some(s => s.date === dates[current_day_index] && s.time === time)) {
      slot.classList.add('selected');
    }

    slots_col.appendChild(slot);
  });

  document.getElementById('current-date').textContent = formatted_dates[current_day_index];
}

function update_selected_slots_display() {
  const container = document.getElementById('selected-slots');
  if (selected_slots.length === 0) {
    container.textContent = "No slots selected";
  } else {
    container.innerHTML = "<strong>Selected Slots:</strong><br>" +
      selected_slots.map(slot => {
        const end_time = calculate_end_time(slot.time);
        return `- ${slot.time} → ${end_time} on ${format_date(slot.date)}`;
      }).join("<br>");
  }
}

function calculate_end_time(start_time) {
  const [hours, minutes] = start_time.split(':').map(Number);
  const total_start_minutes = hours * 60 + minutes;
  const total_end_minutes = total_start_minutes + meeting_duration_minutes;

  const end_hours = Math.floor(total_end_minutes / 60);
  const end_minutes = total_end_minutes % 60;

  return `${String(end_hours).padStart(2, '0')}:${String(end_minutes).padStart(2, '0')}`;
}

function format_date(date_str) {
  const date_obj = new Date(date_str);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date_obj.toLocaleDateString('en-GB', options).replace(/ /g, ' ');
}

document.querySelector('.submit-btn').addEventListener('click', () => {
  if (selected_slots.length === 0) {
    alert("Please select at least one slot before submitting!");
  } else {
    alert("Availability Submitted!");
    window.location.href = "main-menu.html";
  }
});