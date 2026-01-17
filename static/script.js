<<<<<<< HEAD
// ... existing code ...

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#3b82f6";
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "rgba(255, 255, 255, 0.3)";
    const file = e.dataTransfer.files[0];
    handleResumeUpload(file);
});

fileInput.addEventListener("change", (e) => {
    handleResumeUpload(e.target.files[0]);
});

async function handleResumeUpload(file) {
    if (!file) return;

    // Visual Feedback
    dropZone.innerHTML = `<p>⏳ Analyzing ${file.name}...</p>`;
    
    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("/api/upload-resume", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            dropZone.innerHTML = `<p>✅ Resume Loaded!</p>`;
            addMessage("System: I have read your resume. I'm ready to begin.", "system");
        } else {
            dropZone.innerHTML = `<p>❌ Error</p>`;
        }
    } catch (error) {
        console.error(error);
        dropZone.innerHTML = `<p>❌ Upload Failed</p>`;
    }
}
=======
// ... existing code ...

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#3b82f6";
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "rgba(255, 255, 255, 0.3)";
    const file = e.dataTransfer.files[0];
    handleResumeUpload(file);
});

fileInput.addEventListener("change", (e) => {
    handleResumeUpload(e.target.files[0]);
});

async function handleResumeUpload(file) {
    if (!file) return;

    // Visual Feedback
    dropZone.innerHTML = `<p>⏳ Analyzing ${file.name}...</p>`;
    
    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("/api/upload-resume", {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            dropZone.innerHTML = `<p>✅ Resume Loaded!</p>`;
            addMessage("System: I have read your resume. I'm ready to begin.", "system");
        } else {
            dropZone.innerHTML = `<p>❌ Error</p>`;
        }
    } catch (error) {
        console.error(error);
        dropZone.innerHTML = `<p>❌ Upload Failed</p>`;
    }
}
>>>>>>> c9a6c9f69360d2ff917f3cc8192fa84ac13fdf7c
