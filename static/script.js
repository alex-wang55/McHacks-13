let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Elements
const recordBtn = document.getElementById('recordBtn');
const statusText = document.getElementById('statusText');
const visualizer = document.getElementById('visualizer');
const chatHistory = document.getElementById('chatHistory');
const resumeUpload = document.getElementById('resumeUpload');
const resumeStatus = document.getElementById('resumeStatus');
const uploadText = document.getElementById('uploadText');

// 1. Resume Upload Logic
resumeUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    uploadText.textContent = "Uploading...";
    const formData = new FormData();
    formData.append('resume', file);

    try {
        const response = await fetch('/api/upload-resume', { method: 'POST', body: formData });
        if (response.ok) {
            resumeStatus.classList.remove('hidden');
            uploadText.textContent = "📄 Resume Updated";
        }
    } catch (err) {
        alert("Upload failed.");
    }
});

// 2. Setup Speech Recognition (Browser Built-in)
// This gives us the text of what YOU said immediately.
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let finalUserText = "";

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        finalUserText += transcript + " ";
    };
} else {
    console.log("Browser does not support Speech Recognition");
}

// 3. Recording Logic
recordBtn.addEventListener('click', async () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        finalUserText = ""; // Reset text

        mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        
        mediaRecorder.onstop = async () => {
            // 1. Prepare Audio Blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // 2. Add USER Message to Chat (using the browser transcript)
            // Fallback to "(Audio)" if recognition failed
            const displayText = finalUserText.trim() || "(Audio Message)";
            addMessage(displayText, 'user-message');

            // 3. Show "Thinking" bubble
            const loadingId = addMessage("Thinking...", 'ai-message');

            // 4. Send to Backend
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');

            try {
                const response = await fetch('/api/process-audio', { method: 'POST', body: formData });
                const data = await response.json();
                
                // Remove loading bubble
                document.getElementById(loadingId).remove();

                if (data.error) {
                    addMessage("Error: " + data.error, 'ai-message');
                } else {
                    // Add AI Message
                    addMessage(data.ai_text, 'ai-message');
                    
                    // Play Audio
                    const audio = new Audio("data:audio/mp3;base64," + data.audio_data);
                    audio.play();
                }
            } catch (err) {
                console.error(err);
                document.getElementById(loadingId).innerText = "Error connecting to server.";
            }
        };

        mediaRecorder.start();
        if (recognition) recognition.start(); // Start listening for text
        
        isRecording = true;
        recordBtn.classList.add('recording');
        visualizer.classList.remove('hidden');
        statusText.textContent = "Listening...";

    } catch (err) {
        alert("Microphone access denied.");
    }
}

function stopRecording() {
    mediaRecorder.stop();
    if (recognition) recognition.stop();
    
    isRecording = false;
    recordBtn.classList.remove('recording');
    visualizer.classList.add('hidden');
    statusText.textContent = "Processing...";
}

// Helper: Add Chat Bubble
function addMessage(text, className) {
    const div = document.createElement('div');
    div.classList.add('message', className);
    div.innerText = text;
    div.id = 'msg-' + Date.now();
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Auto scroll
    return div.id;
}