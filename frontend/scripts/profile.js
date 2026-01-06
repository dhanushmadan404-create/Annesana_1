const API_URL = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost" ? "http://127.0.0.1:8000" : "";
let user = { name: "Guest", email: "guest@example.com" };
try {
  user = JSON.parse(localStorage.getItem("user"));
} catch (e) {
  console.error("Invalid user data");
}

if (!user || !user.user_id) {
  // If no user context, maybe redirect or show guest
  // window.location.href = "/pages/login.html";
}
document.addEventListener("DOMContentLoaded", () => {
  let profile = document.getElementById("profile_details")

  profile.innerHTML = `
       <img src="${API_URL}/uploads/${user.image || 'default.png'}" class="profile-image" />
        <br />
        <h2>${user.name}</h2>
        <p class="about">${user.email}</p>
    `;
})
const editBtn = document.getElementById("editBtn");
const user_edit = document.getElementById("edit");

editBtn.addEventListener("click", () => {
  user_edit.innerHTML = `
    <form id="editForm">
      <label>Name</label>
      <input 
        type="text" 
        id="name" 
        value="${user.name}" 
        required
      />

      <label>Profile Image</label>
      <input
        id="image"
        type="file"
        accept="image/*"
      />

      <img src="${API_URL}/${user.image}" width="80" />

      <button type="submit">Update</button>
    </form>
    `;


  // attach submit handler
  document
    .getElementById("editForm")
    .addEventListener("submit", submitEditForm);
});
async function submitEditForm(e) {
  e.preventDefault();

  const email = JSON.parse(localStorage.getItem("user")).email; // or however you store it
  const name = document.getElementById("name").value;
  const image = document.getElementById("image").files[0];

  const formData = new FormData();
  formData.append("email", email);
  formData.append("name", name);

  // image is optional
  if (image) {
    formData.append("image", image);
  }

  try {
    const res = await fetch(
      `${API_URL}/users/profile`,
      {
        method: "PUT",
        body: formData
      }
    );

    if (!res.ok) {
      alert("Update failed ❌");
      return;
    }

    const updatedUser = await res.json();
    console.log(updatedUser);

    // Update local storage
    localStorage.setItem("user", JSON.stringify(updatedUser));
    user = updatedUser; // update global var
    location.reload(); // Reload to show changes

    alert("Profile updated ✅");
    // ✅ HIDE EDIT FORM AFTER SUCCESS
    user_edit.innerHTML = ""


  } catch (err) {
    console.error(err);

    alert("Server error ❌");
  }
}

// Log out
document.querySelector("a[href='./registration.html']").addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.clear();
  window.location.href = "./login.html";
});
