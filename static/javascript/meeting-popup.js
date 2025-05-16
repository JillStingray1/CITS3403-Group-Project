/**
 * 
 */
function hide_popup() {
    document.getElementById("popup").style.display = "none";
}

/**
 * Shows a popup of the meeting's details from the share code to allow 
 * users to confirm whether they have imported the correct meeting
 * 
 * @param {*} e the confirm event
 */
function confirm_share_code(e) {
    // Prevents the confirmation popup from disappearing when the dropdown disappears
    e.preventDefault()
    e.stopPropagation()
    let code = document.getElementById("code").value
    let base_url = window.location.origin
    let fetch_url = base_url + '/meeting/code/' + code
    try {
        fetch(fetch_url).then(response => {
            if (response.ok) {
                response.json().then(response_json => {
                    document.getElementById("meeting-name").textContent
                        = response_json.meeting_name;
                    document.getElementById("meeting-description").textContent
                        = response_json.meeting_description;
                    document.getElementById("start-date").textContent
                        = response_json.start_date;
                    document.getElementById("end-date").textContent
                        = response_json.end_date
                    document.getElementById("popup").style.display = "block"
                })
            } else if (response.status == 403) {
                response.json().then(response_json => {
                    document.getElementById("error").textContent = response_json.error
                })
            }
        })
    } catch (error) {
        document.getElementById("error").textContent = "There's been an error with geting your meeting";
    }
}



window.onload = () => {
    const open_btn = document.getElementById("show-details");
    open_btn.addEventListener("click", confirm_share_code)
    const close_btn = document.getElementById("close-button");
    close_btn.addEventListener("click", hide_popup)
}