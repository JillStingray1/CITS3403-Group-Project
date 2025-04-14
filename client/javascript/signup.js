document.getElementById("signupForm").addEventListener("submit", function (e) {
  const password = document.getElementById("password").value;
  const confirm = document.getElementById("confirmPassword").value;
  if (password !== confirm) {
    e.preventDefault();
    alert("Passwords do not match!");
  }
});
