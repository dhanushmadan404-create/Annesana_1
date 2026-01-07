const API_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://annesana-1-dnv8.vercel.app";

// ---------------- MENU LIST ----------------
const ul = document.getElementById("list_container");
const input = document.getElementById("menuName");
const imageInput = document.getElementById("menuImage");
const menuError = document.getElementById("menuError");

// Utility to convert file to Base64
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

async function addMenuItem() {
  const name = input?.value.trim();
  const file = imageInput?.files?.[0];

  menuError.textContent = "";

  if (!name) {
    menuError.textContent = "Please enter a menu item name.";
    return;
  }
  if (!file) {
    menuError.textContent = "Please select an image.";
    return;
  }

  const base64 = await getBase64(file); // ✅ convert to Base64

  const list = document.createElement("li");
  list.dataset.imageFile = base64; // store Base64 string

  const imgTag = `<img src="${base64}" class="menu_image" width="50" style="margin-left:10px; object-fit: cover;">`;
  list.innerHTML = `*${name} ${imgTag} <button type="button" onclick="removeItem(event)">Delete</button>`;
  ul.appendChild(list);

  input.value = "";
  imageInput.value = "";
}

function removeItem(e) {
  e.target.parentElement.remove();
}

// ---------------- MAP OPEN / CLOSE ----------------
const mapCon = document.getElementById("mapContainer");

document.querySelector(".location-group")?.addEventListener("click", () => {
  mapCon.style.display = "block";
});
document.getElementById("back")?.addEventListener("click", () => {
  mapCon.style.display = "none";
});
document.getElementById("save")?.addEventListener("click", () => {
  mapCon.style.display = "none";
});

// ---------------- MAP INIT ----------------
const map = L.map("map").setView([13.0827, 80.2707], 11);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 20 }).addTo(map);

const foodIcon = L.icon({ iconUrl: "/assets/3448609.png", iconSize: [40, 40], iconAnchor: [20, 40] });
let marker = null;
let latitude = null;
let longitude = null;

map.on("click", (e) => {
  if (marker) map.removeLayer(marker);
  marker = L.marker([e.latlng.lat, e.latlng.lng], { icon: foodIcon }).addTo(map);
  latitude = e.latlng.lat;
  longitude = e.latlng.lng;
});

// ---------------- CURRENT LOCATION ----------------
document.getElementById("location")?.addEventListener("click", () => {
  navigator.geolocation.getCurrentPosition((pos) => {
    map.setView([pos.coords.latitude, pos.coords.longitude], 15);
  });
});

// ---------------- VENDOR REGISTRATION ----------------
document.getElementById("vendorRegistration")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  let hasError = false;
  document.querySelectorAll(".error-message").forEach(span => (span.textContent = ""));

  // --- Food Type ---
  const foodType = document.getElementById("foodType");
  const foodTypeError = document.getElementById("foodTypeError");
  if (!foodType?.value) { foodTypeError.textContent = "Select food type"; hasError = true; }

  // --- Phone Number ---
  const phone = document.getElementById("number");
  const numberError = document.getElementById("numberError");
  if (!phone?.value || !/^\d{10}$/.test(phone.value)) { numberError.textContent = "Enter a valid 10-digit phone number"; hasError = true; }

  // --- Vendor Image ---
  const image = document.getElementById("image");
  const imageError = document.getElementById("imageError");
  if (!image?.files?.length) { imageError.textContent = "Upload an image"; hasError = true; }

  // --- Menu List ---
  menuError.textContent = "";
  if (!ul || ul.children.length === 0) { menuError.textContent = "Add at least one menu item"; hasError = true; }

  // --- Location ---
  const locationError = document.getElementById("locationError");
  if (latitude === null || longitude === null) { locationError.textContent = "Select shop location"; hasError = true; }

  // --- Operating Hours ---
  const openingTime = document.getElementById("openingTime");
  const closingTime = document.getElementById("closingTime");
  const openingTimeError = document.getElementById("openingTimeError");
  const closingTimeError = document.getElementById("closingTimeError");

  if (!openingTime?.value) { openingTimeError.textContent = "Select opening time"; hasError = true; }
  if (!closingTime?.value) { closingTimeError.textContent = "Select closing time"; hasError = true; }

  if (openingTime?.value && closingTime?.value) {
    const [oh, om] = openingTime.value.split(":").map(Number);
    const [ch, cm] = closingTime.value.split(":").map(Number);
    const openMinutes = oh * 60 + om;
    const closeMinutes = ch * 60 + cm;
    if (closeMinutes <= openMinutes) { closingTimeError.textContent = "Closing must be after opening"; hasError = true; }
    if (closeMinutes - openMinutes < 60) { closingTimeError.textContent = "Minimum 1 hour required"; hasError = true; }
  }

  if (hasError) return;

  // ---------------- SEND VENDOR DATA ----------------
  // Get the ID from localStorage - check for 'vendor', 'user', or 'admin'
  const userId = localStorage.getItem("vendor") || localStorage.getItem("user") || localStorage.getItem("admin");

  if (!userId) {
    alert("You must be logged in to register a vendor");
    return;
  }

  const vendorForm = new FormData();
  vendorForm.append("phone_number", phone.value);
  vendorForm.append("cart_image_url", await getBase64(image.files[0])); // vendor main image Base64
  vendorForm.append("opening_time", openingTime.value);
  vendorForm.append("closing_time", closingTime.value);
  vendorForm.append("user_id", userId);

  try {
    const res = await fetch(`${API_URL}/vendors`, { method: "POST", body: vendorForm });
    if (!res.ok) {
      const err = await res.json();
      return alert(err.detail || "Registration failed");
    }
    const data = await res.json();
    localStorage.setItem("vendor_details", JSON.stringify(data));

    // --- Menu Items ---
    for (let li of ul.children) {
      const base64Image = li.dataset.imageFile;
      if (!base64Image) continue; // skip if missing

      const foodForm = new FormData();
      foodForm.append("food_name", li.textContent.replace("Delete", "").trim());
      foodForm.append("category", foodType.value.toLowerCase());
      foodForm.append("latitude", latitude);
      foodForm.append("longitude", longitude);
      foodForm.append("vendor_id", data.vendor_id);
      foodForm.append("image_base64", base64Image);

      await fetch(`${API_URL}/foods`, { method: "POST", body: foodForm });
    }

    alert("Vendor registration successful ✅");
    location.href = "../pages/vendor-profile.html";
  } catch (err) {
    alert("Upload failed ❌");
    console.error(err);
  }
});
