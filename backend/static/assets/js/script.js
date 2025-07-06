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
        .then(res => res.ok ? res.json() : Promise.reject(`Status: ${res.status}`))
        .then(data => {
            if (data.error) throw new Error(data.error);
            renderAll(data);
        })
        .catch(error => {
            console.error("Failed to load data:", error);
            document.querySelector('.container').innerHTML = `
                <h1>Error</h1>
                <p>Sorry, portfolio data could not be loaded.</p>
                <p><small>${error}</small></p>`;
        });

    function renderAll(data) {
        if (data.personal_info) renderPersonalInfo(data.personal_info);
        if (data.social_links) renderSocialLinks(data.social_links);
        if (data.skills) renderSkills(data.skills);
        if (data.projects) renderProjectCarousel(data.projects);
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

        if (info.profile_photo_url) {
            profilePhotoEl.src = info.profile_photo_url;
            profilePhotoEl.classList.remove('hidden');
        } else {
            profilePhotoEl.classList.add('hidden');
        }
    }

    function renderSocialLinks(links) {
        socialLinksContainer.innerHTML = '';
        links.forEach(link => {
            const a = document.createElement('a');
            a.href = link.url;
            a.textContent = link.name;
            a.target = "_blank";
            socialLinksContainer.appendChild(a);
        });
    }

    function renderSkills(skills) {
        skillsContainer.innerHTML = '';
        if (!skills.length) return skillsContainer.innerHTML = `<p>No skills found.</p>`;
        skills.forEach(skill => {
            const badge = document.createElement('div');
            badge.className = 'skill-badge';
            const icon = skill.image_url
                ? `<img src="${skill.image_url}" alt="${skill.name}">`
                : skill.icon_class
                    ? `<i class="${skill.icon_class}"></i>` : '';
            badge.innerHTML = `${icon}<span>${skill.name}</span>`;
            skillsContainer.appendChild(badge);
        });
    }

    function renderMemoryCarousel(memories) {
        memoriesContainer.innerHTML = '';
        const slides = [];

        memories.forEach(memory => {
            (memory.photos || []).forEach(url => {
                if (url.startsWith("http")) {
                    slides.push({
                        title: memory.title,
                        date: memory.date_of_memory,
                        url
                    });
                }
            });
        });

        if (slides.length === 0) {
            memoriesContainer.innerHTML = '<p>No memory photos added yet.</p>';
            return;
        }

        slides.forEach((photo, idx) => {
            const slide = document.createElement('div');
            slide.className = 'memory-slide';
            if (idx === 0) slide.classList.add('active');

            const date = new Date(photo.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long'
            });

            slide.innerHTML = `
                <img src="${photo.url}" alt="${photo.title}" />
                <h3>${photo.title}</h3>
                <p class="memory-date">${date}</p>
            `;
            memoriesContainer.appendChild(slide);
        });

        const allSlides = document.querySelectorAll('.memory-slide');
        let current = 0;
        setInterval(() => {
            allSlides[current].classList.remove('active');
            current = (current + 1) % allSlides.length;
            allSlides[current].classList.add('active');
        }, 4000);
    }

    function renderProjectCarousel(projects) {
        projectGrid.innerHTML = '';
        if (!projects.length) {
            projectGrid.innerHTML = `<p>No projects available.</p>`;
            return;
        }

        const carousel = document.createElement('div');
        carousel.className = 'carousel-wrapper';

        projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'carousel-card';
            card.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                ${project.project_url ? `<a href="${project.project_url}" target="_blank" class="visit-button">Visit</a>` : ''}
            `;
            carousel.appendChild(card);
        });

        projectGrid.appendChild(carousel);
    }
});
