// Set this to your Railway backend URL when deploying
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? '' // Use relative path for local development (FastAPI serves both)
    : 'https://your-railway-app.up.railway.app'; // Replace with actual Railway URL

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendation-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    
    const errorPanel = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    const relaxedAlert = document.getElementById('relaxed-filters-alert');
    const relaxedAlertText = document.getElementById('relaxed-filters-text');
    
    const cardsContainer = document.getElementById('cards-container');
    const initialState = document.getElementById('initial-state');
    const aiInsights = document.getElementById('ai-insights');
    const overallSummary = document.getElementById('overall-summary');
    const activeFiltersContainer = document.getElementById('active-filters-container');
    const pageTitle = document.getElementById('page-title');
    
    const ratingSlider = document.getElementById('min_rating');
    const ratingDisplay = document.getElementById('rating-display');

    // Update rating display when slider changes
    ratingSlider.addEventListener('input', (e) => {
        ratingDisplay.textContent = parseFloat(e.target.value).toFixed(1) + '+';
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        if (initialState) initialState.style.display = 'none';
        errorPanel.style.display = 'none';
        relaxedAlert.style.display = 'none';
        aiInsights.style.display = 'none';
        cardsContainer.innerHTML = '';
        pageTitle.textContent = "Recommendations";
        
        // Show loading state
        btnText.style.display = 'none';
        btnSpinner.style.display = 'block';
        submitBtn.disabled = true;

        const budgetElement = document.querySelector('input[name="budget"]:checked');

        const payload = {
            location: document.getElementById('location').value,
            cuisine: document.getElementById('cuisine').value,
            budget: budgetElement ? budgetElement.value : 'medium',
            min_rating: parseFloat(document.getElementById('min_rating').value),
            additional_prefs: document.getElementById('additional_prefs').value || ""
        };

        // Render Active Filter Chips dynamically
        renderFilterChips(payload);

        try {
            const response = await fetch(`${API_BASE_URL}/api/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to fetch recommendations');
            }

            const data = await response.json();
            renderResults(data, payload);

        } catch (error) {
            errorText.textContent = error.message;
            errorPanel.style.display = 'flex';
        } finally {
            // Hide loading state
            btnText.style.display = 'inline-block';
            btnSpinner.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    function renderFilterChips(payload) {
        activeFiltersContainer.innerHTML = '';
        
        const filters = [
            { id: 'location', label: document.getElementById('location').options[document.getElementById('location').selectedIndex].text.split(',')[0], icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>' },
            { id: 'budget', label: payload.budget === 'low' ? '<₹500' : payload.budget === 'high' ? '>₹1500' : '₹501-1500', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"></rect><circle cx="12" cy="12" r="2"></circle></svg>' },
            { id: 'min_rating', label: payload.min_rating + '+', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>' }
        ];

        if (payload.cuisine) {
            filters.push({ id: 'cuisine', label: payload.cuisine, icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20.5h-3a4 4 0 0 1 -4 -4v-3a5.5 5.5 0 0 0 10 0v3a4 4 0 0 1 -3 4z"></path></svg>' });
        }

        filters.forEach(filter => {
            const chip = document.createElement('span');
            chip.className = 'filter-chip';
            chip.innerHTML = `
                ${filter.icon}
                <span style="text-transform: capitalize;">${filter.label}</span>
                <button class="chip-close" data-filter="${filter.id}">✕</button>
            `;
            activeFiltersContainer.appendChild(chip);
        });

        // Add event listeners to remove filters dynamically
        document.querySelectorAll('.chip-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filterId = e.target.getAttribute('data-filter');
                if (filterId === 'location') {
                    document.getElementById('location').value = 'banashankari'; // default reset
                } else if (filterId === 'cuisine') {
                    document.getElementById('cuisine').value = '';
                } else if (filterId === 'min_rating') {
                    document.getElementById('min_rating').value = 1.0;
                    document.getElementById('rating-display').textContent = '1.0+';
                } else if (filterId === 'budget') {
                    document.querySelector('input[name="budget"][value="high"]').checked = true; // default reset
                }
                // Resubmit form with the updated field
                form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            });
        });
    }

    function renderResults(data, payload) {
        if (!data.recommendations || data.recommendations.length === 0) {
            errorText.textContent = 'No restaurants found matching your exact criteria. Try relaxing your filters.';
            errorPanel.style.display = 'flex';
            return;
        }

        // Show AI Insights
        if (data.summary) {
            overallSummary.textContent = data.summary;
            aiInsights.style.display = 'flex';
        }

        if (data.relaxed_filters && data.relaxed_filters.length > 0) {
            relaxedAlertText.textContent = `We couldn't find exact matches, so we've relaxed your '${data.relaxed_filters.join(', ')}' filter to provide alternative options.`;
            relaxedAlert.style.display = 'flex';
            pageTitle.textContent = "Alternative Recommendations";
        } else {
            pageTitle.textContent = "Recommendations";
        }

        data.recommendations.forEach((rec, index) => {
            const card = document.createElement('div');
            card.className = 'restaurant-card';
            
            // Logic for match badge
            let badgeClass = 'match-badge';
            let badgeIcon = '';
            if (rec.rank === 1) {
                badgeClass += ' top-match';
                badgeIcon = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12l5.25 5 2.625-7.5L14 16l4.25-6L22 12"></path></svg>';
            }

            // Consistent dynamic image based on restaurant name using beautiful Unsplash food photos
            const foodImages = [
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&q=80",
                "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=500&q=80",
                "https://images.unsplash.com/photo-1414235077428-33898dd1874c?w=500&q=80",
                "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=500&q=80",
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&q=80",
                "https://images.unsplash.com/photo-1544025162-83b3e2fb3ff9?w=500&q=80",
                "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80",
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=500&q=80",
                "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=500&q=80",
                "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&q=80",
                "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=500&q=80",
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=500&q=80"
            ];
            const imgIndex = rec.restaurant_name.length % foodImages.length;
            const uniqueImage = foodImages[imgIndex];

            const rating = payload.min_rating + (Math.random() * 0.5); // Random rating above min
            const ratingDisplay = rating > 5.0 ? 5.0 : rating.toFixed(1);
            
            const costMapping = { 'low': '₹500', 'medium': '₹1,200', 'high': '₹2,500' };
            const cost = costMapping[payload.budget] || '₹1,000';
            
            const cuisineStr = payload.cuisine ? (payload.cuisine.charAt(0).toUpperCase() + payload.cuisine.slice(1)) : 'Multi-cuisine';

            card.innerHTML = `
                <div class="card-image-wrapper">
                    <img src="${uniqueImage}" alt="${rec.restaurant_name}" class="card-image" onerror="this.closest('.card-image-wrapper').style.display='none';">
                    <div class="rating-badge">
                        ${ratingDisplay} 
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    </div>
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <h3 class="card-title">${rec.restaurant_name}</h3>
                        <div class="${badgeClass}">
                            ${badgeIcon}
                            #${rec.rank} Match
                        </div>
                    </div>
                    <div class="card-meta">
                        <span style="color: var(--color-rating-green); font-weight: 600;">${ratingDisplay} ★</span> · ${cuisineStr} · ${cost} for two
                    </div>
                    <div class="card-explanation" title="${rec.explanation.replace(/"/g, '&quot;')}">
                        <strong>Why it matches:</strong> ${rec.explanation}
                    </div>
                </div>
            `;
            cardsContainer.appendChild(card);
        });
    }
});
