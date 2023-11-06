document.getElementById("show-polls-button").addEventListener("click", function() {
      const polls = document.getElementById("polls-list")
      if (polls.style.display === "none" || polls.style.display === "") {
          this.textContent = "Hide Polls"
          polls.style.display = "block";
      } else {
          this.textContent = "Show all my polls"
          polls.style.display = "none";
      }
  });
  document.getElementById("update-profile-button").addEventListener("click", function() {
      const form = document.getElementById("update-profile-form");
      if (form.style.display === "none" || form.style.display === "") {
          form.style.display = "block";
      } else {
          form.style.display = "none";
      }
  });
  document.getElementById("profile-form").addEventListener("submit", function(event) {
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;

    if (!firstName) {
      event.preventDefault();
      document.getElementById("first_name_error").innerText = "Please, enter first name.";
    } else {
      document.getElementById("first_name_error").innerText = "";
    }

    if (!lastName) {
      event.preventDefault();
      document.getElementById("last_name_error").innerText = "Please, enter last name";
    } else {
      document.getElementById("last_name_error").innerText = "";
    }
  });