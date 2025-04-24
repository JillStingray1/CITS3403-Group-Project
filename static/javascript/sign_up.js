
/**
 * Takes in the values in the sign-up form and sends it to /user,
 * which is the route that queries the database.
 * 
 * 
 */
function create_user() {
    let username = document.forms["signup"]["username"].value
    let password = document.forms["signup"]["password"].value
    let confirm_password = document.forms["signup"]["confirm_password"].value

    // Calls validation functions
    let username_validity = is_username_valid(username)
    let password_validity = is_password_valid(password)
    let matched_passwords = password_matching(password, confirm_password)
    alert(password_validity)
    alert(username_validity)
    alert(matched_passwords)
    if (!username_validity || !password_validity || !matched_passwords) {
        return false
    }
    post_user(password, username)
}

/**
 * Validates user inputed usernames, which can only contain alphanumeric 
 * characters and underscores
 * 
 * @param {string} username the username string from user input
 * @returns boolean that verifies user input
 */
function is_username_valid(username) {
    let santinized_username = username.match(new RegExp("[A-Za-z0-9_]+"));
    if (username.length < 3 && username.length > 25 ) {
        document.getElementById("username_warning").textContent 
            = "Username must be between 3 and 25 characters.";
        return false
    }
    if (santinized_username[0] != username){
        document.getElementById("username_warning").textContent 
            = "Username must only contain alphanumeric characters and underscores.";
        return false
    }
    return true;
}

/**
 * Validates user inputed passwords, Password must only contain alphanumeric 
 * characters and the following special characters !#+:=.?
 * 
 * @param {string} password the password string from user input
 * @returns boolean that verifies user input
 */
function is_password_valid(password) {
    let santinized_password = password.match(new RegExp("[A-Za-z0-9!#+:=.?]+"));
    if (password.length < 5 && password.length > 35 ) {
        document.getElementById("pasword_warning").textContent 
            = "Password must be between 5 and 35 characters.";
        return false
    }
    if (santinized_password[0] != password){
        document.getElementById("password_warning").textContent 
            = "Password must only contain alphanumeric characters and the following special characters !#+:=.?";
        return false
    }
    return true;

}


/**
 * Validates user inputed passwords, Password must only contain alphanumeric 
 * characters and the following special characters !#+:=.?
 * 
 * @param {string} password the password string from user input
 * @returns boolean that verifies user input
 */
function password_matching(password, confirm_password) {
    if (password != confirm_password) {
        document.getElementById("confirm_warning").textContent 
            = "Provided passwords must be identical."
        return 
    }
    return true
}


/**
 * Posts valid username and passwords to "/user/signup" where a new user is
 * created in the database. If it fails due to duplicate usernames, or
 * other reasons, then display the error in the warning box.
 *
 * @param {string} username 
 * @param {string} password 
 */
function post_user(username, password) {
    let sign_up_url ="/user/signup";
    
    fetch(sign_up_url, {
        "method": "POST",
        "body": JSON.stringify({
            username,
            password,
        })
    }).then()
}


// prevents the default behavior of submitting the form when all fields filed
window.onload = function ()  {
    let signup_form = document.getElementById("signup")
    signup_form.addEventListener('submit', event => {
        event.preventDefault();
        return create_user();
    })
}

