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
  [nameError, emailError, passwordError, roleError, imageError].forEach(el => el && (el.textContent = ""));

  let isValid = true;

  if (name.length < 3) {
    nameError.textContent = "Name must be at least 3 letters";
    isValid = false;
  }

  if (!email.includes("@gmail.com")) {
    emailError.textContent = "Email must contain @gmail.com";
    isValid = false;
  } else if (email.length < 13) {
    emailError.textContent = "Email must be at least 13 characters";
    isValid = false;
  }

  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    isValid = false;
  }

  if (!role) {
    roleError.textContent = "Please select a role";
    isValid = false;
  }

  if (!imageFile) {
    imageError.textContent = "Please upload a profile image";
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

    console.log("Registering to:", `${API_URL}/users/`);

    const res = await fetch(`${API_URL}/users/`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      // Handle both FastAPI errors and our custom catch-all errors
      const errorMsg = data.detail || data.error || "Registration failed";
      alert(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg);
    } else {
      alert("Registration successful ✅ Please login now.");
      visible('loginForm', 'registerForm'); // Switch to login form
    }
  } catch (err) {
    console.error("Registration error:", err);
    alert("Connection error ❌ Check if backend is running.");
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

  if (!email.includes("@gmail.com") || email.length < 13) {
    emailError.textContent = "Invalid email format";
    return;
  }

  if (password.length < 6) {
    passwordError.textContent = "Password too short";
    return;
  }

  try {
    const res = await fetch(`${API_URL}/users/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      const errorMsg = data.detail || data.error || "Login failed";
      return alert(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg);
    }

    // ✅ Store all necessary info
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", data.user_id);
    localStorage.setItem("role", data.role);
    localStorage.setItem("user_details", JSON.stringify(data));

    // Navigate based on role
    if (data.role === "user") {
      location.href = "../index.html";
    } else if (data.role === "admin") {
      location.href = "./admin.html";
    } else if (data.role === "vendor") {
      try {
        const checkRes = await fetch(`${API_URL}/vendors/check/${data.user_id}/`);
        if (!checkRes.ok) throw new Error("Vendor check failed");
        const result = await checkRes.json();
        if (result.exists) {
          location.href = "./vendor-profile.html";
        } else {
          location.href = "./registration.html";
        }
      } catch (err) {
        console.error("Vendor check error:", err);
        location.href = "./registration.html";
      }
    }
  } catch (err) {
    console.error("Login error:", err);
    alert("Connection error ❌ Check if backend is running.");
  }
});
