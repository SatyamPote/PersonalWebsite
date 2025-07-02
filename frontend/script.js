document.addEventListener('DOMContentLoaded', () => {
    const API_URL = "https://personal-dashboard-backend-dxrt.onrender.com/api/user-data/";

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

    fetch(API_URL)
        .then(res => {
            if (!res.ok) throw new Error(`Server responded with ${res.status}`);
            return res.json();
        })
        .then(data => {
            if (data.error) throw new Error(`API Error: ${data.error}`);
            renderAll(data);
        })
        .catch(error => {
            console.error("Failed to load data:", error);
            document.querySelector('.container').innerHTML = `
                <h1>Error</h1>
                <p>Sorry, the portfolio data could not be loaded. Please try again later.</p>
                <p><small>Error details: ${error.message}</small></p>
            `;
        });

    function renderAll(data) {
        if (data.personal_info) renderPersonalInfo(data.personal_info);
        if (data.social_links) renderSocialLinks(data.social_links);
        if (data.skills) renderSkills(data.skills);
        if (data.projects) renderProjects(data.projects);
        if (data.memories) renderMemoryCarousel(data.memories);
    }

    function renderPersonalInfo(info) {
        document.title = `${info.full_name} - Portfolio`;
        fullNameEl.textContent = info.full_name;
        subtitleEl.textContent = info.subtitle;
        aboutMeContentEl.textContent = info.about_me;
        locationEl.textContent = info.location;
        languagesEl.textContent = info.languages_spoken;
        myGoalsEl.textContent = info.my_goals;
        footerNameEl.textContent = info.full_name;

        if (info.profile_photo_url && info.profile_photo_url.startsWith('http')) {
            profilePhotoEl.src = info.profile_photo_url;
            profilePhotoEl.classList.remove('hidden');
        } else {
            profilePhotoEl.classList.add('hidden');
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
            if (skill.image_url && skill.image_url.startsWith('http')) {
                iconHtml = `<img src="${skill.image_url}" alt="${skill.name}">`;
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
                    if (photoUrl.startsWith('http')) {
                        allPhotos.push({
                            url: photoUrl,
                            title: memory.title,
                            date: memory.date_of_memory
                        });
                    }
                });
            }
        });

        if (allPhotos.length === 0) {
            memoriesContainer.innerHTML = '<p>No valid memory photos available.</p>';
            return;
        }

        allPhotos.forEach((photo, index) => {
            const slide = document.createElement('div');
            slide.className = 'memory-slide';
            if (index === 0) slide.classList.add('active');

            const memoryDate = new Date(photo.date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long'
            });

            slide.innerHTML = `
                <img src="${photo.url}" alt="${photo.title}">
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
            slides[currentIndex].classList.remove('active');
            currentIndex = (currentIndex + 1) % slides.length;
            slides[currentIndex].classList.add('active');
        }, 3000);
    }
});
