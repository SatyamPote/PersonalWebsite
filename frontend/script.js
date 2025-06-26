document.addEventListener('DOMContentLoaded', () => {

    // Change these two lines to your LIVE Render backend URL
const API_URL = 'https://satyam-portfolio-backend.onrender.com/api/data/';
const BASE_URL = 'https://satyam-portfolio-backend.onrender.com';

// ... (the rest of the script.js file remains exactly the same) ...

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
        document.title = `${info.full_name} - Portfolio`;
        fullNameEl.textContent = info.full_name;
        subtitleEl.textContent = info.subtitle;
        aboutMeContentEl.textContent = info.about_me;
        locationEl.textContent = info.location;
        languagesEl.textContent = info.languages_spoken;
        myGoalsEl.textContent = info.my_goals;
        footerNameEl.textContent = info.full_name;

        if (info.profile_photo_url) {
            profilePhotoEl.src = `${BASE_URL}${info.profile_photo_url}`;
            profilePhotoEl.classList.remove('hidden');
        }
    }

    function renderSocialLinks(links) {
        socialLinksContainer.innerHTML = '';
        links.forEach(link => {
            const linkEl = document.createElement('a');
            linkEl.href = link.url;
            linkEl.textContent = link.name;
            linkEl.target = '_blank';
            socialLinksContainer.appendChild(linkEl);
        });
    }

    // UPDATED AND MORE ROBUST RENDER SKILLS FUNCTION
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
            // New Logic: Prioritize image, but if it's empty, fall back to icon class.
            if (skill.image_url) {
                iconHtml = `<img src="${BASE_URL}${skill.image_url}" alt="${skill.name}">`;
            } else if (skill.icon_class) {
                iconHtml = `<i class="${skill.icon_class}"></i>`;
            }

            // This ensures the name is always displayed, even if there's no icon.
            skillBadge.innerHTML = `${iconHtml}<span>${skill.name}</span>`;
            skillsContainer.appendChild(skillBadge);
        });
    }

    function renderProjects(projects) {
        projectGrid.innerHTML = '';
        if (projects.length === 0) {
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

    // FIXED AND CORRECTED MEMORY CAROUSEL RENDERER
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
            if (index === 0) {
                slide.classList.add('active');
            }
            
            // This was the bug: The photo URL was wrong. It should be BASE_URL + the url from the API.
            const imageUrl = `${BASE_URL}${photo.url}`;
            const memoryDate = new Date(photo.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long'
            });

            slide.innerHTML = `
                <img src="${imageUrl}" alt="${photo.title}">
                <h3>${photo.title}</h3>
                <p class="memory-date">${memoryDate}</p>
            `;
            memoriesContainer.appendChild(slide);
        });

        initializeCarousel();
    }
    
    function initializeCarousel() {
        const slides = document.querySelectorAll('.memory-slide');
        if (slides.length <= 1) return;

        let currentIndex = 0;
        setInterval(() => {
            if (slides[currentIndex]) {
                slides[currentIndex].classList.remove('active');
            }
            currentIndex = (currentIndex + 1) % slides.length;
            if (slides[currentIndex]) {
                slides[currentIndex].classList.add('active');
            }
        }, 2000); // Cycle every 2 seconds
    }

    // --- Main Fetch Logic ---
    fetch(API_URL)
        .then(response => { if (!response.ok) throw new Error('Network response was not ok'); return response.json(); })
        .then(data => {
            renderPersonalInfo(data.personal_info || {});
            renderSocialLinks(data.social_links || []);
            renderSkills(data.skills || []);
            renderProjects(data.projects || []);
            renderMemoryCarousel(data.memories || []);
        })
        .catch(error => {
            console.error('Error fetching portfolio data:', error);
            fullNameEl.textContent = 'Error';
            subtitleEl.textContent = 'Could not load portfolio data. Is the backend server running?';
        });
});