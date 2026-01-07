const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://127.0.0.1:8000/api' : '/api';

const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", async () => {
  if (!token) {
    location.href = "./login.html";
    return;
  }

  const profile = document.getElementById("profile_details");
  try {
    // We now use /users/me which is protected by the token
    const res = await fetch(`${API_URL}/users/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) {
      localStorage.clear();
      location.href = "./login.html";
      return;
    }

    const user_details = await res.json();
    localStorage.setItem("user_details", JSON.stringify(user_details));

    profile.innerHTML = `
         <img src="${user_details.image || '../assets/default.png'}" alt="${user_details.name}" class="profile-image" />
          <br />
          <h2>${user_details.name}</h2>
          <p class="about">${user_details.email}</p>
          <p><strong>Role:</strong> ${user_details.role}</p>
      `;
  } catch (err) {
    console.error("Profile load error:", err);
    alert("Connection error ❌");
  }
});

const editBtn = document.getElementById("editBtn");
const user_edit = document.getElementById("edit");

editBtn.addEventListener("click", () => {
  const user_document = JSON.parse(localStorage.getItem("user_details") || "{}");

  user_edit.innerHTML = `
    <form id="editForm">
      <label>Name</label>
      <input 
        type="text" 
        id="name" 
        value="${user_document.name || ''}" 
        minlength="3"
        required
      />

      <label>Profile Image</label>
      <input
        id="image"
        type="file"
        accept="image/*"
      />

      <img src="${user_document.image || ''}" width="80" id="preview" style="display: block; margin-top: 10px;"/>

      <button type="submit">Update Profile</button>
    </form>
    `;

  document.getElementById("editForm").addEventListener("submit", submitEditForm);
});

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

async function submitEditForm(e) {
  e.preventDefault();
  const name = document.getElementById("name").value.trim();
  const imageFile = document.getElementById("image").files[0];

  const formData = new FormData();
  if (name) formData.append("name", name);

  if (imageFile) {
    const image_base64 = await getBase64(imageFile);
    formData.append("image_base64", image_base64);
  }

  try {
    const res = await fetch(`${API_URL}/users/profile`, {
      method: "PUT",
      headers: { "Authorization": `Bearer ${token}` },
      body: formData
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Update failed");
    }

    const updatedUser = await res.json();
    localStorage.setItem("user_details", JSON.stringify(updatedUser));
    alert("Profile updated ✅");
    location.reload();
  } catch (err) {
    console.error("Update error:", err);
    alert(`Update failed ❌: ${err.message}`);
  }
}

// Log out
const logoutBtn = document.querySelector("a[href='#']");
if (logoutBtn) {
  logoutBtn.addEventListener("click", (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "./login.html";
  });
}
