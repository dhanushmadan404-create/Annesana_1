const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://127.0.0.1:8000/api' : '/api';
// ---------------------- Vendor Profile Script ----------------------
const profile_image = document.getElementById("DB");
const vendorName = document.getElementById("vendor_details");
const TimeStatus = document.getElementById("timeStatus");
const food_container = document.getElementById("food_container");



document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 1️⃣ Get vendor user_id from localStorage
    const vendorId = localStorage.getItem("vendor");
    if (!vendorId) return window.location.href = "./login.html"; // redirect if not logged in

    // 2️⃣ Get user info from "users" table
    const res = await fetch(`${API_URL}/users/${vendorId}`);
    if (!res.ok) throw new Error("Failed to fetch vendor data");
    const data = await res.json();



    // Render profile info
    profile_image.innerHTML = `<img src="${data.image || '../assets/default.png'}" class="card-image"/>`;
    vendorName.innerHTML = `
      <h2>${data.name}</h2>
      <p>${data.email}</p>
    `;

    // 3️⃣ Get vendor-specific info (opening & closing time)
    const vendorDetails = JSON.parse(localStorage.getItem("vendor_details"));

    TimeStatus.textContent = `${vendorDetails.opening_time} - ${vendorDetails.closing_time}`;

    // 4️⃣ Get foods added by this vendor
    const foodRes = await fetch(`${API_URL}/foods/vendor/${vendorDetails.vendor_id}`);
    if (!foodRes.ok) throw new Error("Failed to fetch foods");
    const foods = await foodRes.json();


    // Render food cards
    food_container.innerHTML = ""; // clear any existing
    foods.forEach(food => {
      const div = document.createElement("div");
      div.classList.add("review-card");
      div.id = `food-${food.food_id}`;
      div.innerHTML = `
        <img src="${food.food_image_url}" class="card-image"/>
        <div class="card-info">
          <p><strong>${food.food_name}</strong></p>
          <p>${food.category}</p>
          <button onclick="deleteFood(${food.food_id})" 
            style="background:red;color:white;border:none;padding:5px;cursor:pointer;">Remove</button>
        </div>
      `;
      food_container.appendChild(div);
    });

  } catch (error) {
    console.error(error);
    alert("Failed to load vendor profile ❌");
  }
});

// ---------------------- Logout ----------------------
function logout() {
  localStorage.removeItem("vendor");
  localStorage.removeItem("vendor_details");
  window.location.href = "./login.html"; // navigate to login page
}


async function deleteFood(foodId) {
  if (!foodId) return;

  // Optional: confirm before deleting
  const confirmDelete = confirm("Are you sure you want to delete this food?");
  if (!confirmDelete) return;

  try {
    const res = await fetch(`${API_URL}/foods/${foodId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) {
      throw new Error("Failed to delete food");
    }

    location.reload();
    alert("Food deleted successfully ✅");

  } catch (err) {
    console.error(err);
    alert("Error deleting food ❌");
  }
}

