function category(food_name) {
    // 1. Save the name to memory
    localStorage.setItem("selectedFood", food_name);
    // 2. Move to the map page
    window.location.href = "../map.html"; 
}