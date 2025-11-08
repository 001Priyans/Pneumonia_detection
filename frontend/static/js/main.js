// Main JavaScript for Pneumonia Detection App

// Global variables
let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const changeImageBtn = document.getElementById('changeImage');
const analyzeAnotherBtn = document.getElementById('analyzeAnother');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkServerHealth();
});

function initializeEventListeners() {
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeImage);
    
    // Change image button
    changeImageBtn.addEventListener('click', resetUpload);
    
    // Analyze another button
    analyzeAnotherBtn.addEventListener('click', resetUpload);
}

// Drag and drop handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File selection handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Handle file
function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        showAlert('Please upload a valid image file (JPG, JPEG, or PNG)', 'error');
        return;
    }
    
    // Validate file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        showAlert('File size should not exceed 16MB', 'error');
        return;
    }
    
    selectedFile = file;
    displayImagePreview(file);
}

// Display image preview
function displayImagePreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadArea.style.display = 'none';
        imagePreview.style.display = 'block';
        analyzeBtn.disabled = false;
        results.style.display = 'none';
    };
    
    reader.readAsDataURL(file);
}

// Analyze image
async function analyzeImage() {
    if (!selectedFile) {
        showAlert('Please select an image first', 'error');
        return;
    }
    
    // Show loading
    analyzeBtn.disabled = true;
    loading.style.display = 'block';
    results.style.display = 'none';
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showAlert(data.error || 'Error analyzing image', 'error');
            analyzeBtn.disabled = false;
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Failed to connect to server. Please try again.', 'error');
        analyzeBtn.disabled = false;
    } finally {
        loading.style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    // Show results section
    results.style.display = 'block';
    
    // Set prediction text
    const predictionText = document.getElementById('predictionText');
    const prediction = data.prediction;
    predictionText.textContent = `Prediction: ${prediction}`;
    
    // Add color class
    if (prediction === 'NORMAL') {
        predictionText.className = 'prediction-normal';
    } else {
        predictionText.className = 'prediction-pneumonia';
    }
    
    // Set confidence badge
    const confidenceBadge = document.getElementById('confidenceBadge');
    const confidence = data.confidence;
    confidenceBadge.textContent = `${confidence}%`;
    
    // Set confidence class
    if (confidence >= 90) {
        confidenceBadge.className = 'confidence-badge confidence-high';
    } else if (confidence >= 70) {
        confidenceBadge.className = 'confidence-badge confidence-medium';
    } else {
        confidenceBadge.className = 'confidence-badge confidence-low';
    }
    
    // Set probability bars
    const normalProb = data.probabilities.NORMAL;
    const pneumoniaProb = data.probabilities.PNEUMONIA;
    
    document.getElementById('normalProb').textContent = `${normalProb}%`;
    document.getElementById('pneumoniaProb').textContent = `${pneumoniaProb}%`;
    
    // Animate bars
    setTimeout(() => {
        document.getElementById('normalBar').style.width = `${normalProb}%`;
        document.getElementById('pneumoniaBar').style.width = `${pneumoniaProb}%`;
    }, 100);
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Reset upload
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    imagePreview.style.display = 'none';
    results.style.display = 'none';
    analyzeBtn.disabled = true;
    
    // Reset progress bars
    document.getElementById('normalBar').style.width = '0%';
    document.getElementById('pneumoniaBar').style.width = '0%';
    
    // Scroll to upload section
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Show alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'info'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of upload card
    const uploadCard = document.querySelector('.upload-card');
    uploadCard.insertBefore(alertDiv, uploadCard.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Check server health
async function checkServerHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (data.status === 'running' && !data.model_loaded) {
            console.warn('Warning: Model not loaded on server');
        }
    } catch (error) {
        console.error('Server health check failed:', error);
    }
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
