// ---------------- API URL ----------------
const API_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000/api"
    : "https://annesana-1.onrender.com/api";

// ---------------- TOGGLE FORMS ----------------
function visible(showForm, hideForm) {
  const show = document.getElementById(showForm);
  const hide = document.getElementById(hideForm);

  if (!show || !hide) return;

  show.classList.add("visible");
  hide.classList.remove("visible");
}

// ---------------- BASE64 IMAGE ----------------
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });
}

// ---------------- REGISTER ----------------
document.getElementById("append").addEventListener("click", async () => {
  const name = nameInput("name", "nameError", 3);
  const email = emailInput("registrationEmail", "emailError");
  const password = minInput("registrationPassword", "passwordError", 6);
  const role = selectInput("role", "roleError");
  const imageFile = document.getElementById("image").files[0];
  const imageError = document.getElementById("imageError");

  imageError.textContent = imageFile ? "" : "Image required";
  if (!name || !email || !password || !role || !imageFile) return;

  try {
    const image_base64 = await getBase64(imageFile);

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("role", role);
    formData.append("image_base64", image_base64);

    await fetchAPI(`${API_URL}/users`, {
      method: "POST",
      body: formData,
    });

    alert("Registration successful ✅");
    visible("loginForm", "registerForm");
  } catch (err) {
    alert(err.message);
  }
});

// ---------------- LOGIN ----------------
document.getElementById("check").addEventListener("click", async () => {
  const email = emailInput("email", "loginEmail");
  const password = minInput("password", "loginPassword", 1);
  if (!email || !password) return;

  try {
    const data = await fetchAPI(`${API_URL}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", data.user_id);
    localStorage.setItem("role", data.role);

    location.href = "../../index.html";
  } catch (err) {
    alert(err.message);
  }
});

// ---------------- HELPERS ----------------
function nameInput(id, err, min) {
  const el = document.getElementById(id);
  const er = document.getElementById(err);
  er.textContent = el.value.length >= min ? "" : `Min ${min} chars`;
  return el.value.length >= min ? el.value.trim() : null;
}

function emailInput(id, err) {
  const el = document.getElementById(id);
  const er = document.getElementById(err);
  const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value);
  er.textContent = ok ? "" : "Invalid email";
  return ok ? el.value.trim() : null;
}

function minInput(id, err, min) {
  const el = document.getElementById(id);
  const er = document.getElementById(err);
  er.textContent = el.value.length >= min ? "" : `Required`;
  return el.value.length >= min ? el.value.trim() : null;
}

function selectInput(id, err) {
  const el = document.getElementById(id);
  const er = document.getElementById(err);
  er.textContent = el.value ? "" : "Select role";
  return el.value || null;
}
