/**
 * Client side for share code related data.
 * 
 * 
 */

function confirm_share_code(e) {
    // Prevents the confirmation popup from disappearing when the dropdown disappears
    e.preventDefault()
    e.stopPropagation()
    let code = document.getElementById("code").value
    let base_url = window.location.origin
    let fetch_url = base_url + '/meeting/code/' + code
    try {
        let response = fetch(fetch_url).then(response => {
            if (response.ok) {
                response.json().then(response_json => {
                    console.log(response_json)
                    alert(response_json.meeting_name)
                    document.getElementById("meeting-name").textContent
                        = response_json.meeting_name;
                    document.getElementById("meeting-description").textContent
                        = response_json.meeting_description;
                    document.getElementById("start-date").textContent
                        = response_json.start_date;
                    document.getElementById("end-date").textContent
                        = response_json.end_date
                })
            }
        })
    } catch (error) {
        console.log(error.message);
    }

    document.getElementById("popup").style.display = "block"
}

window.onload = () => {
    const openBtn = document.getElementById("show-details");
    openBtn.addEventListener("click", confirm_share_code)
}