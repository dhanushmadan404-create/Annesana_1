// ---------------- API URL ----------------
const API_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000/api"
    : "https://annesana-1.onrender.com/api";

// ---------------- SHOW / HIDE FORMS ----------------
function visible(showForm, hideForm) {
  const show = document.getElementById(showForm);
  const hide = document.getElementById(hideForm);

  if (!show || !hide) return;

  show.classList.add("visible");
  hide.classList.remove("visible");
}

// ---------------- IMAGE TO BASE64 ----------------
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
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

  [nameError, emailError, passwordError, roleError, imageError].forEach(
    (el) => (el.textContent = "")
  );

  let isValid = true;

  if (name.length < 3 || !/^[A-Za-z\s]+$/.test(name)) {
    nameError.textContent = "Name must be at least 3 letters";
    isValid = false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email) || !email.endsWith("@gmail.com")) {
    emailError.textContent = "Only valid @gmail.com emails allowed";
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

    await fetchAPI(`${API_URL}/users`, {
      method: "POST",
      body: formData,
    });

    alert("Registration successful ✅ Please login");

    // ✅ FIXED TOGGLE
    visible("loginForm", "registerForm");
  } catch (err) {
    alert(err.message);
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

  if (!email) {
    emailError.textContent = "Email required";
    return;
  }

  if (!password) {
    passwordError.textContent = "Password required";
    return;
  }

  try {
    const data = await fetchAPI(`${API_URL}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", data.user_id);
    localStorage.setItem("role", data.role);
    localStorage.setItem("user_details", JSON.stringify(data));

    if (data.role === "user") location.href = "../../index.html";
    else if (data.role === "admin") location.href = "./admin.html";
    else if (data.role === "vendor") {
      const checkData = await fetchAPI(
        `${API_URL}/vendors/check/${data.user_id}/`
      );
      location.href = checkData.exists
        ? "./vendor-profile.html"
        : "./registration.html";
    }
  } catch (err) {
    alert(err.message);
  }
});
