document.addEventListener('DOMContentLoaded', function() {
    // --- 1. SETUP AND AUTH CHECK ---
    const idToken = localStorage.getItem('firebaseIdToken');
    if (!idToken) {
        window.location.href = 'login.html';
        return;
    }
    const backendUrl = 'https://personal-dashboard-backend-dxrt.onrender.com';

    // --- 2. ELEMENT SELECTORS ---
    const logoutButton = document.getElementById('logout-button');
    const createNoteForm = document.getElementById('create-note-form');
    const notesList = document.getElementById('notes-list');
    const loadingNotesMessage = document.getElementById('loading-notes-message');
    const uploadMediaForm = document.getElementById('upload-media-form');
    const mediaList = document.getElementById('media-list');
    const loadingMediaMessage = document.getElementById('loading-media-message');
    const createLinkForm = document.getElementById('create-link-form');
    const linksList = document.getElementById('links-list');
    const loadingLinksMessage = document.getElementById('loading-links-message');
    
    // --- HELPER FUNCTION ---
    function escapeHTML(str) {
        if (typeof str !== 'string') return '';
        return str
            .replace(/&/g, '&')
            .replace(/</g, '<')
            .replace(/>/g, '>')
            .replace(/"/g, '"')
            .replace(/'/g, ',');
    }
    
    // --- GENERIC DELETE FUNCTION ---
    const handleDeleteItem = async (itemType, itemId) => {
        if (!confirm(`Are you sure you want to delete this ${itemType}? This action cannot be undone.`)) {
            return;
        }
        try {
            const endpoint = (itemType === 'media') ? 'media' : `${itemType}s`;
            const response = await fetch(`${backendUrl}/api/${endpoint}/${itemId}`, {
                method: 'DELETE', headers: { 'Authorization': `Bearer ${idToken}` }
            });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || `Failed to delete ${itemType}.`);
            }
            // Refresh the relevant list
            if (itemType === 'note') fetchNotes();
            if (itemType === 'media') fetchMediaFiles();
            if (itemType === 'link') fetchLinks();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    };

    // --- NOTES FUNCTIONS ---
    const fetchNotes = async () => {
        if (!notesList) return;
        loadingNotesMessage.style.display = 'block';
        notesList.innerHTML = '';
        try {
            const response = await fetch(`${backendUrl}/api/notes/`, { headers: { 'Authorization': `Bearer ${idToken}` } });
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            renderNotes(await response.json());
        } catch (error) { console.error('Notes Error:', error); notesList.innerHTML = `<p class="text-red-400">Error loading notes.</p>`; } 
        finally { loadingNotesMessage.style.display = 'none'; }
    };
    const renderNotes = (notes) => {
        if (notes.length === 0) { notesList.innerHTML = '<p class="text-gray-400">You have no notes yet.</p>'; return; }
        notes.forEach(note => {
            const el = document.createElement('div');
            el.className = 'bg-gray-700 p-4 rounded-lg shadow relative';
            el.innerHTML = `<button class="delete-button absolute top-2 right-2 text-gray-400 hover:text-red-500" data-id="${note.id}" data-type="note" title="Delete Note"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button><h3 class="font-bold text-lg pr-8">${escapeHTML(note.title)}</h3><p class="text-gray-300 mt-2 whitespace-pre-wrap">${escapeHTML(note.content)}</p><p class="text-xs text-gray-500 mt-4">Created: ${new Date(note.created_at).toLocaleString()}</p>`;
            notesList.appendChild(el);
        });
    };
    const handleCreateNote = async (event) => {
        event.preventDefault();
        const title = document.getElementById('note-title').value; const content = document.getElementById('note-content').value;
        try {
            await fetch(`${backendUrl}/api/notes/`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${idToken}` }, body: JSON.stringify({ title, content }) });
            createNoteForm.reset(); fetchNotes();
        } catch (error) { alert('Could not create the note.'); }
    };

    // --- MEDIA FUNCTIONS ---
    const fetchMediaFiles = async () => {
        if (!mediaList) return;
        loadingMediaMessage.style.display = 'block';
        mediaList.innerHTML = '';
        try {
            const response = await fetch(`${backendUrl}/api/media/`, { headers: { 'Authorization': `Bearer ${idToken}` } });
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            renderMediaFiles(await response.json());
        } catch (error) { console.error('Media Error:', error); mediaList.innerHTML = '<p class="col-span-full text-red-400">Error loading media.</p>'; } 
        finally { loadingMediaMessage.style.display = 'none'; }
    };
    const renderMediaFiles = (mediaFiles) => {
        if (mediaFiles.length === 0) { mediaList.innerHTML = '<p class="col-span-full text-gray-400">You have no media yet.</p>'; return; }
        mediaFiles.forEach(file => {
            const el = document.createElement('div');
            el.className = 'bg-gray-700 p-2 rounded-lg shadow text-center relative';
            let previewHtml;
            if (file.file_type === 'image') {
                previewHtml = `<a href="${file.file_url}" target="_blank" rel="noopener noreferrer"><img src="${file.file_url.replace('/upload/', '/upload/w_200,h_200,c_fill/')}" alt="${file.filename}" class="w-full h-32 object-cover rounded mb-2"></a>`;
            } else {
                previewHtml = `<a href="${file.file_url}" target="_blank" rel="noopener noreferrer"><div class="w-full h-32 bg-gray-600 flex items-center justify-center rounded mb-2"><svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg></div></a>`;
            }
            el.innerHTML = `<button class="delete-button absolute top-1 right-1 text-gray-300 bg-gray-900 bg-opacity-50 rounded-full p-1 hover:text-red-500" data-id="${file.id}" data-type="media" title="Delete Media"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>${previewHtml}<p class="text-xs text-white truncate" title="${escapeHTML(file.filename)}">${escapeHTML(file.filename)}</p>`;
            mediaList.appendChild(el);
        });
    };
    const handleUploadMedia = async (event) => {
        event.preventDefault();
        const file = document.getElementById('media-file').files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        const btn = document.getElementById('upload-button');
        const status = document.getElementById('upload-status');
        btn.disabled = true;
        btn.innerText = 'Uploading...';
        status.innerText = 'Uploading...';
        try {
            await fetch(`${backendUrl}/api/media/upload`, { method: 'POST', headers: { 'Authorization': `Bearer ${idToken}` }, body: formData });
            status.innerText = 'Upload successful!';
            document.getElementById('media-file').value = '';
            fetchMediaFiles();
        } catch (error) {
            status.innerText = 'Upload failed.';
        } finally {
            btn.disabled = false;
            btn.innerText = 'Upload File';
            setTimeout(() => {
                status.innerText = '';
            }, 5000);
        }
    };

    // --- LINKS FUNCTIONS ---
    const fetchLinks = async () => {
        if (!linksList) return;
        loadingLinksMessage.style.display = 'block';
        linksList.innerHTML = '';
        try {
            const response = await fetch(`${backendUrl}/api/links/`, { headers: { 'Authorization': `Bearer ${idToken}` } });
            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            renderLinks(await response.json());
        } catch (error) { console.error('Links Error:', error); linksList.innerHTML = '<p class="text-red-400">Error loading links.</p>'; } 
        finally { loadingLinksMessage.style.display = 'none'; }
    };
    const renderLinks = (links) => {
        if (links.length === 0) { linksList.innerHTML = '<p class="text-gray-400">You have no saved links yet.</p>'; return; }
        linksList.innerHTML = '';
        links.forEach(link => {
            const el = document.createElement('div');
            el.className = 'bg-gray-700 p-4 rounded-lg shadow relative';
            el.innerHTML = `<button class="delete-button absolute top-2 right-2 text-gray-400 hover:text-red-500" data-id="${link.id}" data-type="link" title="Delete Link"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button><div><a href="${link.url}" target="_blank" rel="noopener noreferrer"><h4 class="font-bold text-lg text-blue-400 hover:underline pr-8">${escapeHTML(link.title)}</h4></a><p class="text-sm text-gray-400 truncate">${escapeHTML(link.url)}</p><p class="text-gray-300 mt-2 text-sm">${escapeHTML(link.description)}</p></div><div class="mt-4 flex justify-between items-center">${link.category ? `<span class="text-xs bg-purple-600 text-white py-1 px-2 rounded-full">${escapeHTML(link.category)}</span>` : '<span></span>'}<span class="text-xs text-gray-500">${new Date(link.created_at).toLocaleDateString()}</span></div>`;
            linksList.appendChild(el);
        });
    };
    const handleCreateLink = async (event) => {
        event.preventDefault();
        const linkData = { url: document.getElementById('link-url').value, title: document.getElementById('link-title').value, description: document.getElementById('link-description').value, category: document.getElementById('link-category').value };
        try {
            const response = await fetch(`${backendUrl}/api/links/`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${idToken}` }, body: JSON.stringify(linkData) });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail[0].msg || 'Failed to save link.'); }
            createLinkForm.reset();
            fetchLinks();
        } catch (error) {
            alert('Could not save link: ' + error.message);
        }
    };
    
    // --- EVENT LISTENERS & INITIAL LOAD ---
    document.querySelector('main').addEventListener('click', function(e) {
        const deleteButton = e.target.closest('.delete-button');
        if (deleteButton) {
            handleDeleteItem(deleteButton.dataset.type, deleteButton.dataset.id);
        }
    });

    logoutButton.addEventListener('click', () => {
        localStorage.clear();
        window.location.href = 'index.html';
    });

    if (createNoteForm) createNoteForm.addEventListener('submit', handleCreateNote);
    if (uploadMediaForm) uploadMediaForm.addEventListener('submit', handleUploadMedia);
    if (createLinkForm) createLinkForm.addEventListener('submit', handleCreateLink);
    
    // Initial data fetch for all sections
    fetchNotes();
    fetchMediaFiles();
    fetchLinks();
});