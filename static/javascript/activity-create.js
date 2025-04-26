document.getElementById("activityForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    // Get field values
    const title = document.getElementById("meeting_name").value.trim();
    const description = document.getElementById("meeting_description").value.trim();
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;
    const duration = parseInt(document.getElementById("meeting_length").value);
  
    // Today's date in YYYY-MM-DD format
    const today = new Date().toISOString().split("T")[0];
  
    // Validation
    if (!title) {
      alert("Please enter an activity title.");
      return;
    }
  
    if (!startDate || startDate < today) {
      alert("Start date must be today or later.");
      return;
    }
  
    if (!endDate || endDate < today) {
      alert("End date must be today or later.");
      return;
    }
  
    if (endDate < startDate) {
      alert("End date cannot be before the start date.");
      return;
    }
  
    const allowedDurations = [15, 30, 45, 60, 90, 120, 300];
    if (!allowedDurations.includes(duration)) {
      alert("Invalid meeting duration selected.");
      return;
    }
  
    // Construct payload
    const meetingData = {
      meeting_name: title,
      meeting_description: description,
      start_date: startDate,
      end_date: endDate,
      meeting_length: duration
    };
  
    
    console.log("Submitting meeting:", meetingData);
  });
  
