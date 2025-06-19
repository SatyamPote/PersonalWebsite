// --- YOUR FIREBASE CONFIGURATION ---
const firebaseConfig = {
  apiKey: "AIzaSyA1VJDq-lrXvCt8Szhoifa1gORsonBKbR4",
  authDomain: "personalwebside-9999.firebaseapp.com",
  projectId: "personalwebside-9999",
  storageBucket: "personalwebside-9999.appspot.com",
  messagingSenderId: "691247567855",
  appId: "1:691247567855:web:5759757fdef1db9d8e9c1a",
  measurementId: "G-4NKKPYYXYH"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

document.addEventListener('DOMContentLoaded', function() {
    // Get all the elements from the HTML
    const authForm = document.getElementById('auth-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const formTitle = document.getElementById('form-title');
    const submitButton = document.getElementById('submit-button');
    const toggleModeLink = document.getElementById('toggle-mode-link');
    const errorMessageDiv = document.getElementById('error-message');

    // ==================================================================
    // === THIS IS THE IMPORTANT CHANGE FOR YOUR LIVE WEBSITE ===
    // ==================================================================
    const backendUrl = 'https://personal-dashboard-backend-dxrt.onrender.com';

    let isLoginMode = true; // By default, the form is in "Login" mode

    // --- Function to handle form submission ---
    authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = emailInput.value;
        const password = passwordInput.value;
        errorMessageDiv.innerText = '';

        if (isLoginMode) {
            auth.signInWithEmailAndPassword(email, password)
                .then(handleAuthSuccess)
                .catch(handleAuthError);
        } else {
            auth.createUserWithEmailAndPassword(email, password)
                .then(handleAuthSuccess)
                .catch(handleAuthError);
        }
    });

    // --- Function to toggle between Login and Sign Up modes ---
    toggleModeLink.addEventListener('click', (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;
        if (isLoginMode) {
            formTitle.innerText = 'Admin Panel Login';
            submitButton.innerText = 'Login';
            toggleModeLink.innerText = "Don't have an account? Sign Up";
        } else {
            formTitle.innerText = 'Create an Account';
            submitButton.innerText = 'Sign Up';
            toggleModeLink.innerText = 'Already have an account? Login';
        }
    });

    // --- Function to run after a successful login or sign up ---
    function handleAuthSuccess(authResult) {
        console.log("Authentication successful, calling backend...");
        authResult.user.getIdToken().then(idToken => {
            // We now use the live backendUrl variable
            fetch(`${backendUrl}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id_token: idToken }),
            })
            .then(response => {
                if (!response.ok) throw new Error('Backend validation failed.');
                return response.json();
            })
            .then(data => {
                localStorage.setItem('firebaseIdToken', idToken);
                localStorage.setItem('userInfo', JSON.stringify(data.user));
                window.location.href = 'dashboard.html';
            })
            .catch(error => errorMessageDiv.innerText = error.message);
        });
    }

    // --- Function to display errors to the user ---
    function handleAuthError(error) {
        console.error("Firebase Auth Error:", error);
        errorMessageDiv.innerText = error.message;
    }
});