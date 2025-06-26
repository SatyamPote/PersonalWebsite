document.addEventListener('DOMContentLoaded', () => {

    // The API URL for your live backend.
    const API_URL = 'https://personal-dashboard-backend-dxrt.onrender.com/api/data/';

    // --- Element Selectors ---
    const profilePhotoEl = document.getElementById('profile-photo');
    const fullNameEl = document.getElementById('full-name');
    const subtitleEl = document.getElementById('subtitle');
    const socialLinksContainer = document.getElementById('social-links-container');
    const aboutMeContentEl = document.getElementById('about-me-content');
    const locationEl = document.getElementById('location');
    const languagesEl = document.getElementById('languages');
    const myGoalsEl = document.getElementById('my-goals');
    const skillsContainer = document.getElementById('skills-container');
    const projectGrid = document.getElementById('project-grid');
    const memoriesContainer = document.getElementById('memories-slider-container');
    const footerNameEl = document.getElementById('footer-name');
    
    // --- Renderer Functions ---

    function renderPersonalInfo(info) {
        if (!info) return;
        document.title = info.full_name ? `${info.full_name} - Portfolio` : 'Portfolio';
        fullNameEl.textContent = info.full_name || 'Your Name';
        subtitleEl.textContent = info.subtitle || 'A Developer';
        
        // Use the image URL from the API directly.
        if (info.profile_photo_url) {
            profilePhotoEl.src = info.profile_photo_url;
            profilePhotoEl.classList.remove('hidden');
        }
        
        aboutMeContentEl.textContent = info.about_me || 'Information coming soon.';
        locationEl.textContent = info.location || 'N/A';
        languagesEl.textContent = info.languages_spoken || 'N/A';
        myGoalsEl.textContent = info.my_goals || 'N/A';
        footerNameEl.textContent = info.full_name || '';
    }

    function renderSocialLinks(links) {
        socialLinksContainer.innerHTML = '';
        if (!links || links.length === 0) return;
        links.forEach(link => {
            const linkEl = document.createElement('a');
            linkEl.href = link.url;
            linkEl.textContent = link.name;
            linkEl.target = '_blank';
            socialLinksContainer.appendChild(linkEl);
        });
    }

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
            
            // Use the image URL from the API directly.
            if (skill.image_url) {
                iconHtml = `<img src="${skill.image_url}" alt="${skill.name}">`;
            }
            // Note: The icon_class logic is removed as we are simplifying to only use image URLs.
            
            skillBadge.innerHTML = `${iconHtml}<span>${skill.name}</span>`;
            skillsContainer.appendChild(skillBadge);
        });
    }

    function renderProjects(projects) {
        projectGrid.innerHTML = '';
        if (!projects || projects.length === 0) {
            projectGrid.innerHTML = '<p>No projects added yet.</p>';
            return;
        }
        projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                ${project.project_url ? `<a href="${project.project_url}" class="visit-button" target="_blank">Visit</a>` : ''}
            `;
            projectGrid.appendChild(card);
        });
    }
    
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
                        url: photoUrl, // The URL is already a full, direct link.
                        title: memory.title,
                        date: memory.date_of_memory
                    });
                });
            }
        });

        if (allPhotos.length === 0) {
            memoriesContainer.innerHTML = '<p>No memory photos have been added yet.</p>';
            return;
        }

        allPhotos.forEach((photo, index) => {
            const slide = document.createElement('div');
            slide.className = 'memory-slide';
            if (index === 0) slide.classList.add('active');
            
            const memoryDate = new Date(photo.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long'
            });

            slide.innerHTML = `<img src="${photo.url}" alt="${photo.title}"><h3>${photo.title}</h3><p class="memory-date">${memoryDate}</p>`;
            memoriesContainer.appendChild(slide);
        });
        
        initializeCarousel();
    }
    
    function initializeCarousel() {
        const slides = document.querySelectorAll('.memory-slide');
        if (slides.length <= 1) return;
        let currentIndex = 0;
        setInterval(() => {
            if (slides[currentIndex]) slides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % slides.length;
            if (slides[currentIndex]) slides[currentIndex].classList.add('active');
        }, 3000); // Cycle every 3 seconds
    }

    // --- Main Fetch Logic ---
    fetch(API_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Render each section with the data received, or an empty object/array if null
            renderPersonalInfo(data.personal_info || {});
            renderSocialLinks(data.social_links || []);
            renderSkills(data.skills || []);
            renderProjects(data.projects || []);
            renderMemoryCarousel(data.memories || []);
        })
        .catch(error => {
            console.error('Failed to fetch portfolio data:', error);
            const header = document.getElementById('header-container');
            header.innerHTML = `<h1 class="glow-text">Error</h1><p class="subtitle">Could not load portfolio data. The backend may be spinning up.</p>`;
        });
});