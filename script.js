const API_BASE_URL = 'https://ai-career-navigator-qhdu.onrender.com'; 

class ResumeAnalyzer {
    constructor() {
        this.selectedFile = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File input change event
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.handleFileSelect(e);
        });

        // Scroll to analyzer when CTA button is clicked
        document.querySelector('.cta-button').addEventListener('click', () => {
            this.showAnalyzer();
        });
    }

    showAnalyzer() {
        const analyzerSection = document.getElementById('analyzer');
        analyzerSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Validate file type
        const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
            this.showError('Unsupported file type. Please upload a .txt, .pdf, or .docx file');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('File size too large. Please upload a file smaller than 10MB');
            return;
        }

        this.selectedFile = file;
        this.displayFileInfo(file);
        this.hideError();
    }

    displayFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        fileInfo.style.display = 'flex';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    async analyzeResume() {
        if (!this.selectedFile) {
            this.showError('Please select a file first');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);

            const response = await fetch(`${API_BASE_URL}/analyze_resume`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const result = await response.json();
            this.displayResults(result);

        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(error.message || 'Failed to analyze resume. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(result) {
        // Display score
        this.displayScore(result.score, result.summary);
        
        // Display breakdown
        this.displayBreakdown(result.details);
        
        // Display skills
        this.displaySkills(result.skills);
        
        // Display suggestions
        this.displaySuggestions(result.suggestions);
        
        // Show results section
        this.showResults();
    }

    displayScore(score, summary) {
        const scoreNumber = document.getElementById('scoreNumber');
        const scoreIcon = document.getElementById('scoreIcon');
        const progressFill = document.getElementById('progressFill');
        const scoreSummary = document.getElementById('scoreSummary');

        // Animate score counting
        this.animateNumber(scoreNumber, 0, score, 1500);

        // Set score icon and color based on score
        scoreIcon.className = 'score-icon';
        if (score >= 80) {
            scoreIcon.classList.add('excellent');
            scoreIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        } else if (score >= 60) {
            scoreIcon.classList.add('good');
            scoreIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
        } else {
            scoreIcon.classList.add('needs-improvement');
            scoreIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        }

        // Animate progress bar
        setTimeout(() => {
            progressFill.style.width = `${score}%`;
        }, 500);

        // Set summary
        scoreSummary.textContent = summary;
    }

    displayBreakdown(details) {
        const breakdownGrid = document.getElementById('breakdownGrid');
        breakdownGrid.innerHTML = '';

        const categories = {
            'contact_info': { label: 'Contact Information', max: 20 },
            'experience_quality': { label: 'Experience Quality', max: 25 },
            'skills_relevance': { label: 'Skills Relevance', max: 20 },
            'achievements': { label: 'Achievements', max: 20 },
            'formatting': { label: 'Formatting', max: 10 },
            'keywords': { label: 'Industry Keywords', max: 5 }
        };

        Object.entries(categories).forEach(([key, category]) => {
            const score = details[key] || 0;
            const percentage = (score / category.max) * 100;

            const breakdownItem = document.createElement('div');
            breakdownItem.className = 'breakdown-item';
            breakdownItem.innerHTML = `
                <div class="breakdown-label">
                    <span>${category.label}</span>
                    <span class="breakdown-score">${score}/${category.max}</span>
                </div>
                <div class="breakdown-progress">
                    <div class="breakdown-progress-fill" style="width: 0%"></div>
                </div>
            `;

            breakdownGrid.appendChild(breakdownItem);

            // Animate progress bar
            setTimeout(() => {
                const progressFill = breakdownItem.querySelector('.breakdown-progress-fill');
                progressFill.style.width = `${percentage}%`;
            }, 700);
        });
    }

    displaySkills(skills) {
        const skillsGrid = document.getElementById('skillsGrid');
        skillsGrid.innerHTML = '';

        if (skills.length === 0) {
            skillsGrid.innerHTML = '<p style="color: var(--text-secondary); font-size: 0.9rem;">No technical skills detected. Consider adding more specific skills to your resume.</p>';
            return;
        }

        skills.forEach((skill, index) => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill;
            skillTag.style.animationDelay = `${index * 0.1}s`;
            skillsGrid.appendChild(skillTag);
        });
    }

    displaySuggestions(suggestions) {
        const suggestionsList = document.getElementById('suggestionsList');
        suggestionsList.innerHTML = '';

        suggestions.forEach((suggestion, index) => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.innerHTML = `
                <div class="suggestion-number">${index + 1}</div>
                <div class="suggestion-text">${suggestion}</div>
            `;
            suggestionsList.appendChild(suggestionItem);
        });
    }

    animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsedTime = currentTime - startTime;
            const progress = Math.min(elapsedTime / duration, 1);
            
            // Easing function for smoother animation
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(start + (end - start) * easeOut);
            
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        
        // Disable analyze button
        const analyzeButton = document.getElementById('analyzeButton');
        analyzeButton.disabled = true;
        analyzeButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Analyzing...</span>';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
        
        // Re-enable analyze button
        const analyzeButton = document.getElementById('analyzeButton');
        analyzeButton.disabled = false;
        analyzeButton.innerHTML = '<i class="fas fa-brain"></i><span>Analyze Resume</span>';
    }

    showResults() {
        const results = document.getElementById('results');
        results.style.display = 'block';
        
        // Smooth scroll to results
        setTimeout(() => {
            results.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }, 100);
    }

    hideResults() {
        document.getElementById('results').style.display = 'none';
    }

    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        
        errorText.textContent = message;
        errorMessage.style.display = 'flex';
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }
}

// Resume upload logic
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if(file) {
        document.getElementById('fileInfo').style.display = 'block';
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = (file.size/1024).toFixed(1) + ' KB';
        window.selectedResumeFile = file;
    }
});

function analyzeResume() {
    if(!window.selectedResumeFile) return;
    const formData = new FormData();
    formData.append('resume', window.selectedResumeFile);
    fetch('/upload_resume', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            alert('Resume uploaded and stored!');
            // Optionally trigger analysis here
        } else {
            alert('Upload failed: ' + data.error);
        }
    });
}

// Global functions for HTML onclick events
function showAnalyzer() {
    analyzer.showAnalyzer();
}

function analyzeResume() {
    analyzer.analyzeResume();
}

// Initialize the analyzer when the page loads
let analyzer;
document.addEventListener('DOMContentLoaded', () => {
    analyzer = new ResumeAnalyzer();
});

// Optional: Add smooth scrolling for better UX
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

// Add some visual feedback for file drag and drop (optional enhancement)
const uploadCard = document.querySelector('.upload-card');
if (uploadCard) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadCard.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadCard.style.borderColor = 'var(--primary)';
        uploadCard.style.backgroundColor = 'hsla(198, 100%, 60%, 0.05)';
    }

    function unhighlight(e) {
        uploadCard.style.borderColor = '';
        uploadCard.style.backgroundColor = '';
    }

    uploadCard.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const fileInput = document.getElementById('fileInput');
            fileInput.files = files;
            
            // Trigger the change event manually
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }

}



