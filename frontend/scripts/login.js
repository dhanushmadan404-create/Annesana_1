const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
  ? 'http://127.0.0.1:8000'
  : 'https://annesana-1.onrender.com/api';

// ---------------- FETCH HELPER ----------------
async function fetchAPI(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Something went wrong");
  return data;
}

// ---------------- TOGGLE FORMS ----------------
function toggleForm(targetFormId) {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (targetFormId === "loginForm") {
    loginForm.classList.add("visible");
    registerForm.classList.remove("visible");
  } else if (targetFormId === "registerForm") {
    registerForm.classList.add("visible");
    loginForm.classList.remove("visible");
  }
}

// ---------------- REGISTER ----------------
document.addEventListener("DOMContentLoaded", () => {
  const registerBtn = document.getElementById("registerBtn");
  const loginBtn = document.getElementById("loginBtn");

  // Register
  registerBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value.trim();
    const role = document.getElementById("role").value;
    const imageFile = document.getElementById("img").files[0];

    const nameError = document.getElementById("nameError");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const roleError = document.getElementById("roleError");
    const imageError = document.querySelector("label[for='img'].error");

    [nameError,emailError,passwordError,roleError,imageError].forEach(el => el.textContent = "");

    let valid = true;
    if(name.length < 3){ nameError.textContent = "Name min 3 chars"; valid = false; }
    if(!/\S+@\S+\.\S+/.test(email)){ emailError.textContent = "Invalid email"; valid = false; }
    if(password.length < 6){ passwordError.textContent = "Password min 6 chars"; valid = false; }
    if(!role){ roleError.textContent = "Select role"; valid = false; }
    if(!imageFile){ imageError.textContent = "Profile image required"; valid = false; }
    if(!valid) return;

    try {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("email", email);
      formData.append("password", password);
      formData.append("role", role);
      formData.append("image", imageFile); // Method 1 file upload

      await fetchAPI("/users", { method: "POST", body: formData });

      alert("Registration successful ✅");
      toggleForm("loginForm");
    } catch (err) {
      alert(err.message);
    }
  });

  // Login
  loginBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    const emailError = document.getElementById("loginEmailError");
    const passwordError = document.getElementById("loginPasswordError");

    emailError.textContent = "";
    passwordError.textContent = "";


    if(!email){ emailError.textContent = "Email required"; return; }
    if(!password){ passwordError.textContent = "Password required"; return; }

    try {
      const data = await fetchAPI(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      localStorage.setItem("token", data.access_token);
      localStorage.setItem(`${data.role}`, JSON.stringify(data));

      // Role-based navigation
      if(data.role === "user") location.href = "../../index.html";
      else if(data.role === "admin") location.href = "./admin.html";
      else if(data.role === "vendor") {
        const checkData = await fetchAPI(`/vendors/user/${data.user_id}`);
        location.href = checkData.exists ? "./vendor-profile.html" : "./vendor-register.html";
      }

    } catch (err) {
      passwordError.textContent = err.message;
    }
  });
});
