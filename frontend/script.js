document.addEventListener('DOMContentLoaded', () => {

    // --- We need both these URLs for the Render Disk method ---
    const API_URL = 'https://personal-dashboard-backend-dxrt.onrender.com/api/data/';
    const BASE_URL = 'https://personal-dashboard-backend-dxrt.onrender.com';

    // --- Element Selectors (No changes here) ---
    const profilePhotoEl = document.getElementById('profile-photo');
    // ... (rest of selectors) ...

    function renderPersonalInfo(info) {
        // ... (rest of function) ...
        if (info.profile_photo_url) {
            // --- REVERTED: Build the full URL ---
            profilePhotoEl.src = `${BASE_URL}${info.profile_photo_url}`;
            profilePhotoEl.classList.remove('hidden');
        }
    }

    function renderSkills(skills) {
        // ... (rest of function) ...
        skills.forEach(skill => {
            // ... (badge creation) ...
            if (skill.image_url) {
                // --- REVERTED: Build the full URL ---
                iconHtml = `<img src="${BASE_URL}${skill.image_url}" alt="${skill.name}">`;
            } else if (skill.icon_class) {
                iconHtml = `<i class="${skill.icon_class}"></i>`;
            }
            // ... (rest of badge logic) ...
        });
    }

    function renderMemoryCarousel(memories) {
        // ... (rest of function) ...
        allPhotos.forEach((photo, index) => {
            // ... (slide creation) ...
            // --- REVERTED: Build the full URL ---
            const imageUrl = `${BASE_URL}${photo.url}`;
            // ... (rest of slide logic) ...
        });
        initializeCarousel();
    }
    
    // The rest of the script.js file is identical to the one in my previous response.
    // The key is re-introducing BASE_URL and using it to construct the image src.
});