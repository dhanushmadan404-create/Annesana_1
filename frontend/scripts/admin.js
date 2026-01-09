const API_URL =
  window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000/api'
    : 'https://annesana-1.onrender.com/api';
const token = localStorage.getItem("token");

function logout() {
  localStorage.clear();
  location.href = "./login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const role = localStorage.getItem("role");
  const userDetails = JSON.parse(localStorage.getItem("user_details") || "{}");

  if (!token || role !== "admin") {
    alert("Unauthorized. Admin access required.");
    location.href = "./login.html";
    return;
  }

  document.getElementById("adminName").textContent = userDetails.name || "Admin";

  const foodData = JSON.parse(localStorage.getItem("foodData")) || [];
  const tableBody = document.querySelector("#foodTable tbody");

  foodData.forEach((item, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input type="text" value="${item.food_name || ''}" placeholder="Food Name"></td>
      <td><input type="text" value="${item.category || ''}" placeholder="Category"></td>
      <td><input type="number" step="any" value="${item.latitude || ''}" placeholder="Lat"></td>
      <td><input type="number" step="any" value="${item.longitude || ''}" placeholder="Lng"></td>
      <td><input type="text" value="${item.vendor_id || ''}" placeholder="Vendor ID"></td>
      <td><input type="file" accept="image/*"></td>
      <td><button class="send-btn" onclick="sendData(${index},this)">Add Food</button></td>
    `;
    tableBody.appendChild(row);
  });
});

async function sendData(index, btn) {
  const row = btn.closest("tr");
  const inputs = row.querySelectorAll("input");
  const imageFile = inputs[5].files[0];

  if (!imageFile) return alert("Please select an image first");

  const food_name = inputs[0].value.trim();
  const category = inputs[1].value.trim();
  const latitude = inputs[2].value.trim();
  const longitude = inputs[3].value.trim();
  const vendor_id = inputs[4].value.trim();

  if (!food_name || !category || !latitude || !longitude || !vendor_id) {
    return alert("All fields are required");
  }

  try {
    const reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onload = async () => {
      const formData = new FormData();
      formData.append("food_name", food_name);
      formData.append("category", category);
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("vendor_id", vendor_id);
      formData.append("image_base64", reader.result);

      const res = await fetch(`${API_URL}/foods/`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to add food");
      }

      btn.disabled = true;
      btn.textContent = "Added ✅";
      alert("Food item added successfully!");
    };
  } catch (err) {
    console.error("Admin add food error:", err);
    alert(`Error: ${err.message}`);
  }
}

document.getElementById("clear").onclick = () => {
  localStorage.removeItem("foodData");
  location.reload();
};
