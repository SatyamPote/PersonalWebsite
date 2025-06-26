document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'https://personal-dashboard-backend-dxrt.onrender.com/api/data/';
    // We no longer need the BASE_URL since Cloudinary provides full URLs.

    // --- Element Selectors ---
    const headerContainer = document.getElementById('header-container');
    const profilePhotoEl = document.getElementById('profile-photo');
    const aboutMeContentEl = document.getElementById('about-me-content');
    const detailsContentEl = document.getElementById('details-content');
    const skillsContainer = document.getElementById('skills-container');
    const projectGrid = document.getElementById('project-grid');
    const memoriesContainer = document.getElementById('memories-slider-container');
    const footerNameEl = document.getElementById('footer-name');

    // --- Renderer Functions ---

    function renderPersonalInfo(info) {
        if (!info || Object.keys(info).length === 0) {
            headerContainer.innerHTML = '<h1>Portfolio</h1><p class="subtitle">Content coming soon.</p>';
            return;
        }
        document.title = `${info.full_name || 'Portfolio'}`;
        
        // SIMPLIFIED: Use the Cloudinary URL directly.
        if (info.profile_photo_url) {
            profilePhotoEl.src = info.profile_photo_url;
            profilePhotoEl.classList.remove('hidden');
        }
        headerContainer.querySelector('h1').textContent = info.full_name || 'Name not set';
        headerContainer.querySelector('p').textContent = info.subtitle || '';
        
        aboutMeContentEl.textContent = info.about_me || 'No about me information provided.';
        detailsContentEl.innerHTML = `<p><strong>Location:</strong> <span>${info.location || 'N/A'}</span></p><p><strong>Languages:</strong> <span>${info.languages_spoken || 'N/A'}</span></p><p><strong>My Goals:</strong> <span>${info.my_goals || 'N/A'}</span></p>`;
        footerNameEl.textContent = info.full_name || '';
    }
    
    function renderSocialLinks(links) { /* ... (This function is correct and unchanged) ... */ }

    function renderSkills(skills) {
        skillsContainer.innerHTML = '';
        if (!skills || skills.length === 0) {
            skillsContainer.innerHTML = '<p>No skills have been linked yet.</p>';
            return;
        }
        skills.forEach(skill => {
            const skillBadge = document.createElement('div');
            skillBadge.className = 'skill-badge';
            
            let iconHtml = '';
            // SIMPLIFIED: Use the Cloudinary URL for the skill image directly.
            if (skill.image_url) {
                iconHtml = `<img src="${skill.image_url}" alt="${skill.name}">`;
            } else if (skill.icon_class) {
                iconHtml = `<i class="${skill.icon_class}"></i>`;
            }
            skillBadge.innerHTML = `${iconHtml}<span>${skill.name}</span>`;
            skillsContainer.appendChild(skillBadge);
        });
    }

    function renderProjects(projects) { /* ... (This function is correct and unchanged) ... */ }
    
    function renderMemoryCarousel(memories) {
        memoriesContainer.innerHTML = '';
        if (!memories || memories.length === 0) {
            memoriesContainer.innerHTML = '<p>No memories added yet.</p>';
            return;
        }
        let allPhotos = [];
        memories.forEach(memory => {
            if (memory.photos && memory.photos.length > 0) {
                memory.photos.forEach(photoUrl => {
                    allPhotos.push({
                        // SIMPLIFIED: The photoUrl from the API is the full Cloudinary URL.
                        url: photoUrl,
                        title: memory.title,
                        date: memory.date_of_memory
                    });
                });
            }
        });
        if (allPhotos.length === 0) {
            memoriesContainer.innerHTML = '<p>No memory photos have been uploaded yet.</p>';
            return;
        }
        allPhotos.forEach((photo, index) => {
            const slide = document.createElement('div');
            slide.className = 'memory-slide';
            if (index === 0) slide.classList.add('active');
            
            const memoryDate = new Date(photo.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
            slide.innerHTML = `<img src="${photo.url}" alt="${photo.title}"><h3>${photo.title}</h3><p class="memory-date">${memoryDate}</p>`;
            memoriesContainer.appendChild(slide);
        });
        initializeCarousel();
    }
    
    function initializeCarousel() { /* ... (This function is correct and unchanged) ... */ }

    // --- Main Fetch Logic ---
    fetch(API_URL)
        .then(response => { if (!response.ok) throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`); return response.json(); })
        .then(data => {
            try {
                renderPersonalInfo(data.personal_info || {});
                renderSocialLinks(data.social_links || []);
                renderSkills(data.skills || []);
                renderProjects(data.projects || []);
                renderMemoryCarousel(data.memories || []);
            } catch (renderError) {
                console.error("Error rendering data:", renderError);
            }
        })
        .catch(error => {
            console.error('Failed to fetch portfolio data:', error);
            const header = document.getElementById('header-container');
            header.innerHTML = `<h1 class="glow-text">Error</h1><p class="subtitle">Could not load portfolio data. The backend server may be restarting.</p>`;
        });
});