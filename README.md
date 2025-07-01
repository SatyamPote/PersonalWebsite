# 🌐 Dynamic Personal Portfolio & Dashboard

A fully dynamic personal portfolio website powered by a Django backend and a modern HTML/CSS/JS frontend. This project features a 3D interactive header and allows all content to be managed through a secure admin panel—no code editing required!

**🔗 Live Demo:** [https://satyampote.tech](https://satyampote.tech)

![Demo Screenshot](https://github.com/user-attachments/assets/6966b58d-bf83-4cb2-bd00-c29bdbaa433d)

---

## 🚀 Project Purpose & Features

- ⚙️ **Decoupled Architecture:** Django backend with a lightweight static frontend  
- 📝 **Dynamic Content:** All text and images served from backend, editable via Django Admin  
- 🧊 **Interactive 3D Header:** Built using [Spline](https://spline.design/) for immersive experience  
- 🔌 **API-Driven:** JSON endpoint for serving data to frontend  
- 📱 **Responsive Design:** Fully mobile/tablet/desktop friendly  
- 🖼️ **Memories Carousel:** Slider for achievements, certificates, and photos  
- 💸 **Zero-Cost Deployment:** Works on free tiers (Render + Netlify/Vercel)  

---

## 🛠️ Prerequisites & Dependencies

### Requirements

- Python 3.8+  
- pip  
- Git  
- Web Browser  
- (Optional) [VS Code](https://code.visualstudio.com/)

### Python Dependencies (`requirements.txt`)

- Django  
- djangorestframework  
- gunicorn  
- dj_database_url  
- (and others as needed)

---

## ⚡ Getting Started

### A. Run Locally

#### Set Up the Backend:

<pre><code class="language-sh">
python -m venv venv
source venv/bin/activate        # On macOS/Linux
# venv\Scripts\activate         # On Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
</code></pre>

Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the admin panel.

---

#### Set Up the Frontend:

In your `script.js`, set the API endpoint:

<pre><code class="language-js">
const API_URL = 'http://127.0.0.1:8000/api/data/';
</code></pre>

Open `index.html` in your browser (or use the Live Server extension in VS Code).

---

### B. Deploying

#### 1. Backend (Render)

Push your code to GitHub.  
Go to [Render](https://render.com), create a Web Service, and link your GitHub repo.

**Build Command:**

<pre><code class="language-sh">
pip install -r requirements.txt
</code></pre>

**Start Command:**

<pre><code class="language-sh">
gunicorn portfolio_project.wsgi
</code></pre>

**Set environment variables:**

- `SECRET_KEY`  
- `ALLOWED_HOSTS`  
- `DEBUG=False`  
- (and any other necessary values)

---

#### 2. Frontend (Netlify, Vercel, GitHub Pages)

In `script.js`, update the API URL:

<pre><code class="language-js">
const API_URL = 'https://your-backend-name.onrender.com/api/data/';
</code></pre>

Then deploy the frontend using your preferred service:

- Netlify  
- Vercel  
- GitHub Pages

---

#### 3. Keep Backend Awake (Optional)

Use a service like [UptimeRobot](https://uptimerobot.com) to ping your Render backend every 20 minutes to prevent it from sleeping (Render’s free tier idles after 15 minutes).

---

## 🙏 Acknowledgements

- **Hosting:** Render, Netlify, Vercel  
- **3D Modeling:** [Spline](https://spline.design)  
- **Icons:** [Devicon](https://devicon.dev)  
- **Fonts:** [Google Fonts](https://fonts.google.com)  

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more information.

---

## 👋 Contact

**Satyam Pote**  
- 💻 GitHub: [github.com/SatyamPote](https://github.com/SatyamPote)  
- 💼 LinkedIn: [linkedin.com/in/satyam-pote](https://www.linkedin.com/in/satyam-pote)  
- 📧 Email: [satyampote9999@gmail.com](mailto:satyampote9999@gmail.com)

Feel free to reach out if you have questions or want to connect!

---

## 📌 How to Update This README

1. [Click here to open the README.md editor in your repo.](https://github.com/SatyamPote/PersonalWebsite/new/main?filename=README.md)  
2. Paste this markdown into the editor.  
3. Commit the file to save your new `README.md`.
