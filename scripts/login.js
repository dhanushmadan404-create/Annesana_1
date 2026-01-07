const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://127.0.0.1:8000/api' : '/api';
// ---------------- SHOW / HIDE FORMS ----------------
function visible(showForm, hideForm) {

  document.getElementById(showForm).classList.add("visible");
  document.getElementById(hideForm).classList.remove("visible");
}

// Utility to convert file to Base64
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

// ---------------- REGISTER ----------------
document.getElementById("append").addEventListener("click", async (e) => {
  e.preventDefault();
  // get values
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("registrationEmail").value.trim();
  const password = document.getElementById("registrationPassword").value.trim();
  const role = document.getElementById("role").value;
  const imageFile = document.getElementById("image").files[0];

  // error labels
  const nameError = document.getElementById("nameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");
  const roleError = document.getElementById("roleError");
  const imageError = document.getElementById("imageError");

  // clear old errors
  nameError.textContent = "";
  emailError.textContent = "";
  passwordError.textContent = "";
  roleError.textContent = "";
  imageError.textContent = "";

  let isValid = true;

  // NAME VALIDATION (only letters & min 3)
  const nameRegex = /^[A-Za-z ]+$/;
  if (name.length < 3) {
    nameError.textContent = "Name must be at least 3 letters";
    isValid = false;
  } else if (!nameRegex.test(name)) {
    nameError.textContent = "Name should contain only letters";
    isValid = false;
  }

  // EMAIL VALIDATION
  if (!email.includes("@gmail.com")) {
    emailError.textContent = "Email must contain @gmail.com";
    isValid = false;
  } else if (email.length < 13) {
    emailError.textContent = "Email must be at least 13 characters";
    isValid = false;
  }

  // PASSWORD VALIDATION
  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    isValid = false;
  } else if (password.toLowerCase() === "password") {
    passwordError.textContent = "Password cannot be 'password'";
    isValid = false;
  }

  // ROLE VALIDATION
  if (!role) {
    roleError.textContent = "Please select a role";
    isValid = false;
  }

  // IMAGE VALIDATION
  if (!imageFile) {
    imageError.textContent = "Please upload a profile image";
    isValid = false;
  }

  if (!isValid) return;

  const image_base64 = await getBase64(imageFile);

  const formData = new FormData();
  formData.append("name", name);
  formData.append("email", email);
  formData.append("password", password);
  formData.append("role", role);
  formData.append("image_base64", image_base64);

  const res = await fetch(`${API_URL}/users/`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  if (!res.ok) {
    alert(data.detail);
  } else {
    alert("Registration successful ✅");
    setTimeout(() => location.reload(), 500);
  }
});

// ---------------- LOGIN ----------------
document.getElementById("check").addEventListener("click", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  const emailError = document.getElementById("loginEmail");
  const passwordError = document.getElementById("loginPassword");

  // clear previous errors
  emailError.textContent = "";
  passwordError.textContent = "";



  // EMAIL VALIDATION
  if (!email.includes("@gmail.com")) {
    emailError.textContent = "Email must contain @gmail.com";

  } else if (email.length < 13) {
    emailError.textContent = "Email must be at least 13 characters";

  }

  // PASSWORD VALIDATION
  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";

  }

  ///
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  if (!res.ok) return alert(`please check you email and password if you not register please register you account ${data.detail}`);

  // store ONLY ONE item
  localStorage.setItem(data.role, data.user_id);

  // role based navigation
  if (data.role === "user") {
    location.href = "../index.html";
  }

  else if (data.role === "admin") {
    location.href = "./admin.html";
  }

  else if (data.role === "vendor") {
    try {
      const res = await fetch(
        `${API_URL}/vendors/check/${data.user_id}`
      );

      if (!res.ok) throw new Error("Vendor check failed");

      const result = await res.json();

      if (result.exists) {
        location.href = "./vendor-profile.html";
      } else {
        location.href = "./registration.html";
      }

    } catch (err) {
      console.error(err);
      location.href = "./registration.html";
    }
  }
});



