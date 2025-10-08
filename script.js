document.addEventListener('DOMContentLoaded', () => {
    // Element References
    const form = document.getElementById('calculator-form');
    const metricRadio = document.getElementById('metric');
    const imperialRadio = document.getElementById('imperial');
    const weightInput = document.getElementById('weight');
    const heightInput = document.getElementById('height');
    const ageInput = document.getElementById('age');
    const genderSelect = document.getElementById('gender');
    const activitySelect = document.getElementById('activity-level');
    const themeToggle = document.getElementById('theme-toggle');
    
    const resultArea = document.getElementById('result-area');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    
    const bmiValue = document.getElementById('bmi-value');
    const bmiCategory = document.getElementById('bmi-category');
    const bmrValue = document.getElementById('bmr-value');
    const tdeeValue = document.getElementById('tdee-value');
    const weightRecommendation = document.getElementById('weight-recommendation');
    
    const weightUnitSpan = document.getElementById('weight-unit');
    const heightUnitSpan = document.getElementById('height-unit');

    // =============================
    // UNIT SYSTEM SWITCHING
    // =============================
    function updateUnits() {
        const isMetric = metricRadio.checked;
        
        if (isMetric) {
            weightUnitSpan.textContent = 'kg';
            heightUnitSpan.textContent = 'm';
            weightInput.placeholder = '70';
            heightInput.placeholder = '1.75';
        } else {
            weightUnitSpan.textContent = 'lb';
            heightUnitSpan.textContent = 'in';
            weightInput.placeholder = '154';
            heightInput.placeholder = '69';
        }
        
        // Hide previous results/errors
        hideResults();
    }

    metricRadio.addEventListener('change', updateUnits);
    imperialRadio.addEventListener('change', updateUnits);
    updateUnits(); // Initial call

    // =============================
    // DARK MODE TOGGLE
    // =============================
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        updateThemeIcon(true);
    }

    themeToggle.addEventListener('click', () => {
        const isDark = document.body.classList.toggle('dark-mode');
        updateThemeIcon(isDark);
        
        // Save preference
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    function updateThemeIcon(isDark) {
        const icon = themeToggle.querySelector('i');
        if (isDark) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }

    // =============================
    // FORM SUBMISSION & AJAX
    // =============================
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Hide previous results/errors
        hideResults();

        const data = {
            weight: weightInput.value,
            height: heightInput.value,
            unit: metricRadio.checked ? 'metric' : 'imperial',
            age: ageInput.value,
            gender: genderSelect.value,
            activity_level: activitySelect.value
        };

        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayResults(result);
            } else {
                showError(result.error || 'An unknown error occurred.');
            }

        } catch (error) {
            console.error('Fetch error:', error);
            showError('Could not connect to the server. Please check your network connection.');
        }
    });

    // =============================
    // DISPLAY RESULTS
    // =============================
    function displayResults(result) {
        // BMI
        bmiValue.textContent = result.bmi;
        bmiCategory.textContent = result.category;
        
        // Apply BMI category styling
        const categoryClass = getBMICategoryClass(result.category);
        bmiCategory.className = metric-badge ${categoryClass};
        
        // BMR & TDEE
        bmrValue.textContent = result.bmr.toLocaleString();
        tdeeValue.textContent = result.tdee.toLocaleString();
        
        // Recommendation
        weightRecommendation.textContent = result.recommendation;
        
        // Show results with animation
        resultArea.classList.remove('d-none');
        
        // Smooth scroll to results
        setTimeout(() => {
            resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }

    function getBMICategoryClass(category) {
        const categoryLower = category.toLowerCase();
        if (categoryLower.includes('underweight')) return 'badge-underweight';
        if (categoryLower.includes('normal')) return 'badge-normal';
        if (categoryLower.includes('overweight')) return 'badge-overweight';
        if (categoryLower.includes('obesity')) return 'badge-obese';
        return 'badge-normal';
    }

    // =============================
    // ERROR HANDLING
    // =============================
    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('d-none');
        
        // Scroll to error
        setTimeout(() => {
            errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }

    function hideResults() {
        resultArea.classList.add('d-none');
        errorMessage.classList.add('d-none');
    }

    // =============================
    // INPUT VALIDATION
    // =============================
    [weightInput, heightInput, ageInput].forEach(input => {
        input.addEventListener('input', () => {
            hideResults();
        });
    });

    // =============================
    // ACCESSIBILITY
    // =============================
    // Add keyboard navigation support
    form.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
            e.preventDefault();
            form.requestSubmit();
        }
    });
});
