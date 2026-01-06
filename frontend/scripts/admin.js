function logout() {
  localStorage.removeItem("admin");
  location.href = "./login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const admin = JSON.parse(localStorage.getItem("admin"));
  if (!admin || admin.role !== "admin") {
    alert("Access denied");
    location.href = "./login.html";
    return;
  }

  document.getElementById("adminName").textContent = admin.name;

  const foodData = JSON.parse(localStorage.getItem("foodData")) || [];
  const tableBody = document.querySelector("#foodTable tbody");

  foodData.forEach((item, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><input value="${item.food_name}"></td>
      <td><input value="${item.category}"></td>
      <td><input value="${item.latitude}"></td>
      <td><input value="${item.longitude}"></td>
      <td><input value="${item.vendor_id}"></td>
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
  if (image) formData.append("image", image);

  const res = await fetch("http://localhost:8000/foods", {
    method: "POST",
    body: formData
  });

  if (!res.ok) return alert("Failed ❌");

  btn.style.pointerEvents = "none";
  btn.style.opacity = "0.5";
  alert("Food added ✅");
}

document.getElementById("clear").onclick = () => {
  localStorage.removeItem("foodData");
  location.reload();
};
