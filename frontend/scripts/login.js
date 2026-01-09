const API_URL =
  window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000/api'
    : 'https://annesana-1.onrender.com/api';
// ---------------- SHOW / HIDE FORMS ----------------
function visible(showForm, hideForm) {
  document.getElementById(showForm).classList.add("visible");
  document.getElementById(hideForm).classList.remove("visible");
}

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

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("registrationEmail").value.trim();
  const password = document.getElementById("registrationPassword").value.trim();
  const role = document.getElementById("role").value;
  const imageFile = document.getElementById("image").files[0];

  const nameError = document.getElementById("nameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");
  const roleError = document.getElementById("roleError");
  const imageError = document.getElementById("imageError");

  [nameError, emailError, passwordError, roleError, imageError].forEach(el => el && (el.textContent = ""));

  let isValid = true;

  // Advanced Name Validation
  if (name.length < 3) {
    nameError.textContent = "Name must be at least 3 characters";
    isValid = false;
  } else if (!/^[A-Za-z\s]+$/.test(name)) {
    nameError.textContent = "Name should contain only letters";
    isValid = false;
  }

  // Strict Email Validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    emailError.textContent = "Please enter a valid email address";
    isValid = false;
  } else if (!email.endsWith("@gmail.com")) {
    emailError.textContent = "Only @gmail.com accounts are allowed";
    isValid = false;
  }

  // Strong Password Validation
  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    isValid = false;
  }

  if (!role) {
    roleError.textContent = "Please select a user role";
    isValid = false;
  }

  if (!imageFile) {
    imageError.textContent = "Profile image is required";
    isValid = false;
  }

  if (!isValid) return;

  try {
    const image_base64 = await getBase64(imageFile);
    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("role", role);
    formData.append("image_base64", image_base64);

    // Use the robust fetchAPI helper
    const data = await fetchAPI(`${API_URL}/users`, {
      method: "POST",
      body: formData
    });

    alert("Registration successful ✅ Welcome! Please login now.");
    visible('loginForm', 'registerForm');
  } catch (err) {
    console.error("Registration error:", err);
    alert(`Error: ${err.message}`);
  }
});

// ---------------- LOGIN ----------------
document.getElementById("check").addEventListener("click", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  const emailError = document.getElementById("loginEmail");
  const passwordError = document.getElementById("loginPassword");

  emailError.textContent = "";
  passwordError.textContent = "";

  if (!email) { emailError.textContent = "Email is required"; return; }
  if (!password) { passwordError.textContent = "Password is required"; return; }

  try {
    const data = await fetchAPI(`${API_URL}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    // ✅ Secure Full Stack Session Management
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", data.user_id);
    localStorage.setItem("role", data.role);
    localStorage.setItem("user_details", JSON.stringify(data));

    // Role-based redirection
    if (data.role === "user") location.href = "../../index.html";
    else if (data.role === "admin") location.href = "./admin.html";
    else if (data.role === "vendor") {
      const checkData = await fetchAPI(`${API_URL}/vendors/check/${data.user_id}/`);
      location.href = checkData.exists ? "./vendor-profile.html" : "./registration.html";
    }
  } catch (err) {
    console.error("Login error:", err);
    alert(`Error: ${err.message}`);
  }
});
