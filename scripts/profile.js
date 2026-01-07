// let user = { name: "Guest", email: "guest@example.com" };

const API_URL =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:8000'
        : 'https://annesana-1-dnv8.vercel.app/';

let user_id = localStorage.getItem("user");
document.addEventListener("DOMContentLoaded", async () => {
  
  let profile = document.getElementById("profile_details")
  const res = await fetch(`${API_URL}/users/${user_id}`);
    if (!res.ok) throw new Error("Failed to fetch foods");

    const user_details = await res.json();
    localStorage.setItem("user_details", JSON.stringify(user_details));

    console.log(user_details.image);
  profile.innerHTML = `
  
       <img src="../backend/uploads/${user_details.image || 'default.png'}" alt="${user_details.name}" class="profile-image" />
        <br />
        <h2>${user_details.name}</h2>
        <p class="about">${user_details.email}</p>
    `;
})
const editBtn = document.getElementById("editBtn");
const user_edit = document.getElementById("edit");

editBtn.addEventListener("click", async () => {
   let user_document = JSON.parse(localStorage.getItem("user_details"));

  let API_URL =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:8000'
        : 'https://annesana-1-dnv8.vercel.app/';
  user_edit.innerHTML = `
    <form id="editForm">
      <label>Name</label>
      <input 
        type="text" 
        id="name" 
        value="${user_document.name}" 
        required
      />

      <label>Profile Image</label>
      <input
        id="image"
        type="file"
        accept="image/*"
      />

      <img src="${API_URL}/${user_document.image}" width="80" />

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
   let user_document = JSON.parse(localStorage.getItem("user_details"));


  const email = user_document.email; // or however you store it
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
document.querySelector("a[href='#']").addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.clear();
  window.location.href = "./login.html";
});


