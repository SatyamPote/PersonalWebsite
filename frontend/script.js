// script.js

document.addEventListener('DOMContentLoaded', () => {
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

    const data = {
        personal_info: {
            full_name: "Satyam Pote",
            subtitle: "A DEVELOPER",
            profile_photo_url: "profile_photos/team-1.jpg.jpg",
            about_me: "Hello my-self Satyam ,I have successfully completed a diploma in Mechatronic engineering...",
            location: "bengaluru karnataka",
            languages_spoken: "English * Hindi * Kannada * Marathi",
            my_goals: "To become a successful person"
        },
        social_links: [],
        skills: [
            {
                name: "Css",
                icon_class: "devicon-css3-plain-wordmark colored",
                image_url: "skill_icons/62b2220b038aad4d3ed7ca2f.png"
            },
            {
                name: "html",
                icon_class: null,
                image_url: null
            }
        ],
        projects: [
            {
                title: "Movies-Series---Rating",
                description: "This project is a Django-based web application...",
                project_url: "https://satyampote.pythonanywhere.com/"
            }
        ],
        memories: [
            {
                title: "TIE-GLOBAL-SIMIT",
                description: "The event was an incredible opportunity...",
                link: "https://www.linkedin.com/posts/...",
                date_of_memory: "2024-12-04",
                photos: [
                    "memories/IMG-20241213-WA0063_qqAYuhB.jpg",
                    "memories/IMG-20241213-WA0065_4ChOwze.jpg",
                    "memories/IMG-20241213-WA0081_D7aSlXL.jpg"
                ]
            },
            {
                title: "Aventus DSCE.",
                description: "Stepping into our first 24-hour hackathon...",
                link: "https://www.linkedin.com/posts/...",
                date_of_memory: "2024-06-05",
                photos: ["memories/IMG-20240519-WA0022.jpg"]
            }
        ]
    };

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
            if (skill.image_url) {
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
            memoriesContainer.innerHTML = '<p>No memory photos have been added yet.</p>';
            return;
        }

        allPhotos.forEach((photo, index) => {
            const slide = document.createElement('div');
            slide.className = 'memory-slide';
            if (index === 0) {
                slide.classList.add('active');
            }

            const memoryDate = new Date(photo.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long'
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

    // Render all sections using the dummy data
    renderPersonalInfo(data.personal_info);
    renderSocialLinks(data.social_links);
    renderSkills(data.skills);
    renderProjects(data.projects);
    renderMemoryCarousel(data.memories);
});
