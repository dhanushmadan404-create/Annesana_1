let API_URL =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:8000'
        : 'https://annesana-1-dnv8.vercel.app/';
// ---------------- MENU LIST ----------------
 var ul=document.getElementById("list_container")
        var input=document.getElementById("get")
        function add(){
            // let value=input.value 
            var list=document.createElement("li")
            list.innerHTML=input.value+"<button onclick='remove(event)' >Delete</button>"
            ul.append(list)
        }
        function remove(e){
           e.target.parentElement.remove()
        }

// ---------------- MAP OPEN / CLOSE ----------------
let mapCon = document.getElementById("mapContainer");

document.querySelector(".location-group").addEventListener("click", () => {
  mapCon.style.display = "block"; // show map
});

document.getElementById("back").addEventListener("click", () => {
  mapCon.style.display = "none"; // hide map
});

document.getElementById("save").addEventListener("click", () => {
  mapCon.style.display = "none"; // hide map
});

// ---------------- MAP INIT ----------------
const map = L.map("map").setView([13.0827, 80.2707], 11);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 20,
}).addTo(map);

// ---------------- CURRENT LOCATION ----------------
document.getElementById("location").addEventListener("click", () => {
  navigator.geolocation.getCurrentPosition((position) => {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    map.setView([lat, lon], 15); // center map
  });
});

// ---------------- MAP ICON ----------------
const foodIcon = L.icon({
  iconUrl: "/assets/3448609.png",
  iconSize: [40, 40],
  iconAnchor: [20, 40],
});

// ---------------- LOCATION SELECT ----------------
let marker = null;
let latitude = null;   // ❗ was const (fixed)
let longitude = null;  // ❗ was const (fixed)

map.on("click", (e) => {
  if (marker) map.removeLayer(marker); // remove old marker

  marker = L.marker([e.latlng.lat, e.latlng.lng], { icon: foodIcon }).addTo(map);

  latitude = e.latlng.lat;   // save lat
  longitude = e.latlng.lng;  // save lng
});
// ---------------- VENDOR REGISTRATION ----------------
document.getElementById("vendorRegistration").addEventListener("submit", async (e) => {
  e.preventDefault(); // stop page refresh
  let API_URL =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:8000'
        : 'https://annesana-1-dnv8.vercel.app/';
  // Clear all previous error messages
  document.querySelectorAll(".error-message").forEach(span => span.textContent = "");

  let hasError = false;

  // --- Food Type ---
  const foodType = document.getElementById("foodType");
  const foodTypeError = document.getElementById("foodTypeError");
  if (!foodType.value) {
    foodTypeError.textContent = "Select food type";
    hasError = true;
  } else {
    foodType.value = foodType.value.toLowerCase(); // lowercase transform
  }

  // --- Phone Number ---
  const phone = document.getElementById("number");
  const numberError = document.getElementById("numberError");
  if (!/^\d{10}$/.test(phone.value)) {
    numberError.textContent = "Enter a valid 10-digit phone number";
    hasError = true;
  }

  // --- Image ---
  const image = document.getElementById("image");
  const imageError = document.getElementById("imageError");
  if (!image.files.length) {
    imageError.textContent = "Upload an image";
    hasError = true;
  }

  // --- Menu List ---
  const menuContainer = document.getElementById("list_container");
  const menuError = document.getElementById("menuError");
  if (menuContainer.children.length === 0) {
    menuError.textContent = "Add at least one menu item";
    hasError = true;
  } else {
    // Check that every menu item has an image (assuming each <li> has data-image)
    [...menuContainer.children].forEach((item, idx) => {
      if (!item.dataset.image) {
        menuError.textContent = `Menu item #${idx + 1} must have an image`;
        hasError = true;
      }
    });
  }

  // --- Location ---
  const locationError = document.getElementById("locationError");
  if (typeof latitude === "undefined" || typeof longitude === "undefined" || latitude === null || longitude === null) {
    locationError.textContent = "Select shop location";
    hasError = true;
  }

  // --- Operating Hours ---
  const openingTime = document.getElementById("openingTime");
  const closingTime = document.getElementById("closingTime");
  const openingTimeError = document.getElementById("openingTimeError");
  const closingTimeError = document.getElementById("closingTimeError");

  if (!openingTime.value) {
    openingTimeError.textContent = "Select opening time";
    hasError = true;
  }
  if (!closingTime.value) {
    closingTimeError.textContent = "Select closing time";
    hasError = true;
  }

  if (openingTime.value && closingTime.value) {
    const [openH, openM] = openingTime.value.split(":").map(Number);
    const [closeH, closeM] = closingTime.value.split(":").map(Number);
    const openMinutes = openH * 60 + openM;
    const closeMinutes = closeH * 60 + closeM;

    if (closeMinutes <= openMinutes) {
      closingTimeError.textContent = "Closing must be after opening";
      hasError = true;
    }
    if (closeMinutes - openMinutes < 60) {
      closingTimeError.textContent = "Minimum 1 hour required";
      hasError = true;
    }
  }

  if (hasError) return; // Stop submission if any validation fails

  // ---------------- SEND VENDOR DATA ----------------
  const user = localStorage.getItem("user")
   // actually user_id, backend maps it

  const formData = new FormData();
  formData.append("phone_number", phone.value);
  formData.append("cart_image_url", image.files[0]);
  formData.append("opening_time", openTime);
  formData.append("closing_time", closeTime);
  formData.append("user_id", user);

  try {
    const res = await fetch(`${API_URL}/vendors`, {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      return alert(err.detail || "Registration failed");
    }

    const data = await res.json();
    localStorage.setItem("vendor_details", data);
// / --- Collect menu items ---
const menuContainer = document.getElementById("list_container");

// Transform <li> items to array of {name, image}
const menuList = [...menuContainer.children].map(item => ({
  name: item.textContent.trim(),
  image: item.dataset.image || null // make sure image exists
}));

// --- Map to backend format ---
const foodDataList = menuList.map(food => ({
  food_name: food.name,
  category: foodType.value.toLowerCase(), // lowercase
  latitude,
  longitude,
  vendor_id: data.vendor_id, // correct
  image: food.image
}));

console.log(foodDataList);


// --- Send each item to backend ---
foodDataList.forEach(async (foodItem) => {

    const formData = new FormData();
    formData.append("food_name", foodItem.food_name);
    formData.append("category", foodItem.category);
    formData.append("latitude", foodItem.latitude);
    formData.append("longitude", foodItem.longitude);
    formData.append("vendor_id", foodItem.vendor_id);
    
    // Convert base64 back to Blob if needed for backend file upload
    if (foodItem.image) {
      const res = await fetch(foodItem.image);
      const blob = await res.blob();
      formData.append("image", blob, `${foodItem.food_name}.png`);
    }

    // Send POST request
    const response = await fetch(`${API_URL}/api/addFood`, {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    console.log("Item added:", result);

  });

    alert("Vendor registration successful ✅");
    location.href = "../pages/vendor-profile.html";
  } catch (err) {
    alert("Upload failed ❌");
  }
});



