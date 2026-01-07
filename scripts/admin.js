const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'http://127.0.0.1:8000/api' : 'https://annesana-1-dnv8.vercel.app/api';

function logout() {
  localStorage.clear();
  location.href = "./login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const role = localStorage.getItem("role");
  const userDetails = JSON.parse(localStorage.getItem("user_details") || "{}");

  if (role !== "admin") {
    alert("Access denied. Admin role required.");
    location.href = "./login.html";
    return;
  }

  document.getElementById("adminName").textContent = userDetails.name || "Admin";

  const foodData = JSON.parse(localStorage.getItem("foodData")) || [];
  const tableBody = document.querySelector("#foodTable tbody");

  foodData.forEach((item, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input value="${item.food_name || ''}"></td>
      <td><input value="${item.category || ''}"></td>
      <td><input value="${item.latitude || ''}"></td>
      <td><input value="${item.longitude || ''}"></td>
      <td><input value="${item.vendor_id || ''}"></td>
      <td><input type="file"></td>
      <td><a href="#" onclick="sendData(${index},this)">Send</a></td>
    `;
    tableBody.appendChild(row);
  });
});

async function sendData(index, btn) {
  const row = btn.closest("tr");
  const inputs = row.querySelectorAll("input");
  const image = inputs[5].files[0];

  const formData = new FormData();
  formData.append("food_name", inputs[0].value.trim());
  formData.append("category", inputs[1].value.trim());
  formData.append("latitude", inputs[2].value.trim());
  formData.append("longitude", inputs[3].value.trim());
  formData.append("vendor_id", inputs[4].value.trim());

  if (image) {
    // For admin, we still use the old "image" field or "image_base64"
    // To match our new backend, let's use getBase64 if we want consistency
    // But backend router/food.py expects image_base64 now.
    const reader = new FileReader();
    reader.readAsDataURL(image);
    reader.onload = async () => {
      formData.append("image_base64", reader.result);
      const res = await fetch(`${API_URL}/foods`, {
        method: "POST",
        body: formData
      });
      if (!res.ok) return alert("Failed ❌");
      btn.style.pointerEvents = "none";
      btn.style.opacity = "0.5";
      alert("Food added ✅");
    };
  } else {
    alert("Please select an image");
  }
}

document.getElementById("clear").onclick = () => {
  localStorage.removeItem("foodData");
  location.reload();
};
