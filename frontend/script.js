// --- script.js ---
document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'https://personal-dashboard-backend-dxrt.onrender.com/api/data/';
    const BASE_URL = 'https://personal-dashboard-backend-dxrt.onrender.com';

    function getFullImageUrl(url) {
        if (!url) return '';
        return url.startsWith('http') ? url : `${BASE_URL}${url}`;
    }

    const headerContainer = document.getElementById('header-container');
    const profilePhotoEl = document.getElementById('profile-photo');
    const aboutMeContentEl = document.getElementById('about-me-content');
    const detailsContentEl = document.getElementById('details-content');
    const skillsContainer = document.getElementById('skills-container');
    const projectGrid = document.getElementById('project-grid');
    const memoriesContainer = document.getElementById('memories-slider-container');
    const footerNameEl = document.getElementById('footer-name');

    function renderPersonalInfo(info) {
        if (!info || Object.keys(info).length === 0) {
            headerContainer.innerHTML = '<h1>Portfolio</h1><p class="subtitle">Content coming soon.</p>';
            return;
        }
        document.title = info.full_name || 'Portfolio';

        const photoUrl = getFullImageUrl(info.profile_photo_url);
        if (photoUrl) {
            profilePhotoEl.src = photoUrl;
            profilePhotoEl.classList.remove('hidden');
        }
        headerContainer.querySelector('h1').textContent = info.full_name || 'Name not set';
        headerContainer.querySelector('p').textContent = info.subtitle || '';

        aboutMeContentEl.textContent = info.about_me || 'No about me information provided.';
        detailsContentEl.innerHTML = `<p><strong>Location:</strong> <span>${info.location || 'N/A'}</span></p>
                                      <p><strong>Languages:</strong> <span>${info.languages_spoken || 'N/A'}</span></p>
                                      <p><strong>My Goals:</strong> <span>${info.my_goals || 'N/A'}</span></p>`;
        footerNameEl.textContent = info.full_name || '';
    }

    function renderSocialLinks(links) {
        const container = document.getElementById('social-links-container');
        container.innerHTML = '';
        if (!links || links.length === 0) return;
        links.forEach(link => {
            const linkEl = document.createElement('a');
            linkEl.href = link.url;
            linkEl.textContent = link.name;
            linkEl.target = '_blank';
            container.appendChild(linkEl);
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
            const imageUrl = getFullImageUrl(skill.image_url);
            if (imageUrl) {
                iconHtml = `<img src="${imageUrl}" alt="${skill.name}">`;
            } else if (skill.icon_class) {
                iconHtml = `<i class="${skill.icon_class}"></i>`;
            }
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
            card.innerHTML = `<h3>${project.title}</h3><p>${project.description}</p>
                              ${project.project_url ? `<a href="${project.project_url}" class="visit-button" target="_blank">Visit</a>` : ''}`;
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
                memory.photos.forEach(photo => {
                    allPhotos.push({ url: getFullImageUrl(photo.image_url), title: memory.title, date: memory.date_of_memory });
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

    function initializeCarousel() {
        const slides = document.querySelectorAll('.memory-slide');
        if (slides.length <= 1) return;
        let currentIndex = 0;
        setInterval(() => {
            if (slides[currentIndex]) slides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % slides.length;
            if (slides[currentIndex]) slides[currentIndex].classList.add('active');
        }, 3000);
    }

    fetch(API_URL)
        .then(response => {
            if (!response.ok) throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            return response.json();
        })
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
