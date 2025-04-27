// ---- SETTINGS ---- //
const meetingDurationMinutes = 15; // <<<< Change this value manually if needed
// ------------------- //

const dates = generateDates(3); // today + 2 more
const formattedDates = dates.map(date => formatDate(date));

const timeSlots = [
  "09:00", "09:15", "09:30", "09:45",
  "10:00", "10:15", "10:30", "10:45",
  "11:00", "11:15", "11:30", "11:45",
  "12:00", "12:15", "12:30", "12:45",
  "13:00", "13:15", "13:30", "13:45",
  "14:00", "14:15", "14:30", "14:45",
  "15:00", "15:15", "15:30", "15:45",
  "16:00", "16:15", "16:30", "16:45"
];

let currentDayIndex = 0;
let selectedSlots = [];
const slotsNeeded = Math.ceil(meetingDurationMinutes / 15);

window.onload = () => {
  renderCalendar();
  updateSelectedSlotsDisplay();

  document.getElementById('prev-day').addEventListener('click', () => {
    if (currentDayIndex > 0) {
      currentDayIndex--;
      renderCalendar();
      updateSelectedSlotsDisplay();
    }
  });

  document.getElementById('next-day').addEventListener('click', () => {
    if (currentDayIndex < dates.length - 1) {
      currentDayIndex++;
      renderCalendar();
      updateSelectedSlotsDisplay();
    }
  });

  document.getElementById('slots-column').addEventListener('click', (event) => {
    if (event.target.classList.contains('time-slot') && !event.target.classList.contains('disabled')) {
      const clickedSlot = {
        date: dates[currentDayIndex],
        time: event.target.dataset.time
      };

      const index = selectedSlots.findIndex(slot =>
        slot.date === clickedSlot.date && slot.time === clickedSlot.time
      );

      if (index !== -1) {
        selectedSlots.splice(index, 1);
        event.target.classList.remove('selected');
      } else {
        selectedSlots.push(clickedSlot);
        event.target.classList.add('selected');
      }

      updateSelectedSlotsDisplay();
    }
  });
};

function generateDates(numDays) {
  const today = new Date();
  const generatedDates = [];
  for (let i = 0; i < numDays; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    generatedDates.push(date.toISOString().split('T')[0]);
  }
  return generatedDates;
}

function renderCalendar() {
  const timeCol = document.getElementById('time-column');
  const slotsCol = document.getElementById('slots-column');

  timeCol.innerHTML = "";
  slotsCol.innerHTML = "";

  const latestValidSlotIndex = timeSlots.length - slotsNeeded;

  timeSlots.forEach((time, index) => {
    const timeLabel = document.createElement('div');
    timeLabel.className = 'time-label';
    timeLabel.textContent = time;
    timeCol.appendChild(timeLabel);

    const slot = document.createElement('div');
    slot.className = 'time-slot';
    slot.dataset.time = time;

    if (index > latestValidSlotIndex) {
      slot.classList.add('disabled');
    }

    if (selectedSlots.some(s => s.date === dates[currentDayIndex] && s.time === time)) {
      slot.classList.add('selected');
    }

    slotsCol.appendChild(slot);
  });

  document.getElementById('current-date').textContent = formattedDates[currentDayIndex];
}

function updateSelectedSlotsDisplay() {
  const container = document.getElementById('selected-slots');
  if (selectedSlots.length === 0) {
    container.textContent = "No slots selected";
  } else {
    container.innerHTML = "<strong>Selected Slots:</strong><br>" +
      selectedSlots.map(slot => {
        const endTime = calculateEndTime(slot.time);
        return `- ${slot.time} → ${endTime} on ${formatDate(slot.date)}`;
      }).join("<br>");
  }
}

function calculateEndTime(startTime) {
  const [hours, minutes] = startTime.split(':').map(Number);
  const totalStartMinutes = hours * 60 + minutes;
  const totalEndMinutes = totalStartMinutes + meetingDurationMinutes;

  const endHours = Math.floor(totalEndMinutes / 60);
  const endMinutes = totalEndMinutes % 60;

  return `${String(endHours).padStart(2, '0')}:${String(endMinutes).padStart(2, '0')}`;
}

function formatDate(dateStr) {
  const dateObj = new Date(dateStr);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return dateObj.toLocaleDateString('en-GB', options).replace(/ /g, ' ');
}

document.querySelector('.submit-btn').addEventListener('click', () => {
    if (selectedSlots.length === 0) {
      alert("Please select at least one slot before submitting!");
    } else {
      alert("Availability Submitted!");
      window.location.href = "main-menu.html";
    }
  });
  
