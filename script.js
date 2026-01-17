document.getElementById("talk-btn").addEventListener("click", () => {
    const chatBox = document.getElementById("chat-box");

    // Example chatbot response
    const botMessage = document.createElement("div");
    botMessage.classList.add("message");
    botMessage.textContent = "Hello! How can I help you prepare today?";

    chatBox.appendChild(botMessage);
    chatBox.scrollTop = chatBox.scrollHeight;
    
    const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");

// Click to open file browser
dropZone.addEventListener("click", () => fileInput.click());

// Handle file selection
fileInput.addEventListener("change", (e) => {
    handleFile(e.target.files[0]);
});

// Drag over styling
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

// Remove styling when leaving
dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

// Handle drop
dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

// What happens when a file is uploaded
function handleFile(file) {
    if (!file) return;

    const chatBox = document.getElementById("chat-box");
    const message = document.createElement("div");
    message.classList.add("message");
    message.textContent = `Uploaded: ${file.name}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

});
