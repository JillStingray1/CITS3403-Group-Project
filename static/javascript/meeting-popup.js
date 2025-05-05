/**
 * Client side for share code related data.
 * 
 * 
 */

function confirm_share_code(e) {
    e.preventDefault()
    e.stopPropagation()
    document.getElementById("popup").style.display = "block"
}

window.onload = () => {
    const openBtn = document.getElementById("show-details");
    openBtn.addEventListener("click", confirm_share_code)
}