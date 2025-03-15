/**
 * Results Display Component
 * Manages the display and navigation of processed text chunks
 */

// Component state
const resultsState = {
    chunks: [],
    currentChunkIndex: 0,
    showOriginalText: false,
    isLoading: false
};

// DOM Elements
const resultsContainer = document.getElementById('results-container');
const resultChunksContainer = document.getElementById('result-chunks');
const prevChunkButton = document.getElementById('prev-chunk');
const nextChunkButton = document.getElementById('next-chunk');
const toggleViewButton = document.getElementById('toggle-view');
const toggleViewText = toggleViewButton.querySelector('.toggle-text');
const currentChunkSpan = document.getElementById('current-chunk');
const totalChunksSpan = document.getElementById('total-chunks');
const loadingIndicator = document.getElementById('loading-indicator');

/**
 * Initialize event listeners for the results display component
 */
function initResultsDisplay() {
    // Navigate to previous chunk
    prevChunkButton.addEventListener('click', () => {
        if (resultsState.currentChunkIndex > 0) {
            resultsState.currentChunkIndex--;
            renderCurrentChunk();
            updateNavigationControls();
        }
    });

    // Navigate to next chunk
    nextChunkButton.addEventListener('click', () => {
        if (resultsState.currentChunkIndex < resultsState.chunks.length - 1) {
            resultsState.currentChunkIndex++;
            renderCurrentChunk();
            updateNavigationControls();
        }
    });

    // Toggle between summary and original text
    toggleViewButton.addEventListener('click', () => {
        resultsState.showOriginalText = !resultsState.showOriginalText;
        toggleViewText.textContent = resultsState.showOriginalText ? 'Show Summary' : 'Show Original Text';
        renderCurrentChunk();
    });
}

/**
 * Set the response data and render the first chunk
 * @param {Object} response - The API response data
 */
function setResponseData(response) {
    if (!response || !response.chunks || response.chunks.length === 0) {
        showError('No data received from the server');
        return;
    }

    resultsState.chunks = response.chunks;
    resultsState.currentChunkIndex = 0;
    resultsState.showOriginalText = false;
    
    // Update the UI
    totalChunksSpan.textContent = resultsState.chunks.length;
    currentChunkSpan.textContent = resultsState.currentChunkIndex + 1;
    toggleViewText.textContent = 'Show Original Text';
    
    // Render the chunks
    renderCurrentChunk();
    updateNavigationControls();
    
    // Show the results container
    resultsContainer.style.display = 'block';
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Render the current chunk
 */
function renderCurrentChunk() {
    // Clear the container
    resultChunksContainer.innerHTML = '';
    
    if (resultsState.chunks.length === 0) {
        return;
    }
    
    const chunk = resultsState.chunks[resultsState.currentChunkIndex];
    const chunkElement = createChunkElement(chunk);
    resultChunksContainer.appendChild(chunkElement);
}

/**
 * Create a DOM element for a chunk
 * @param {Object} chunk - The chunk data
 * @returns {HTMLElement} The chunk element
 */
function createChunkElement(chunk) {
    const chunkElement = document.createElement('div');
    chunkElement.classList.add('chunk');
    chunkElement.dataset.chunkId = chunk.id;
    
    // Create header with title and TTS button
    const header = document.createElement('div');
    header.classList.add('chunk-header');
    
    const title = document.createElement('div');
    title.classList.add('chunk-title');
    title.textContent = `Chunk ${resultsState.currentChunkIndex + 1}`;
    
    const ttsButton = document.createElement('button');
    ttsButton.classList.add('tts-button');
    ttsButton.innerHTML = '<i class="fas fa-volume-up"></i>';
    ttsButton.title = 'Listen to this chunk';
    ttsButton.addEventListener('click', () => {
        // This will be handled by the TTS Player component
        if (window.ttsPlayer) {
            const text = resultsState.showOriginalText ? chunk.original_text : chunk.summary;
            window.ttsPlayer.playText(text, chunk.id);
        }
    });
    
    header.appendChild(title);
    header.appendChild(ttsButton);
    
    // Create content
    const content = document.createElement('div');
    content.classList.add('chunk-content');
    
    // Display either summary or original text based on state
    const textToDisplay = resultsState.showOriginalText ? chunk.original_text : chunk.summary;
    content.textContent = textToDisplay;
    
    // Assemble the chunk element
    chunkElement.appendChild(header);
    chunkElement.appendChild(content);
    
    return chunkElement;
}

/**
 * Update the navigation buttons state based on current position
 */
function updateNavigationControls() {
    prevChunkButton.disabled = resultsState.currentChunkIndex === 0;
    nextChunkButton.disabled = resultsState.currentChunkIndex === resultsState.chunks.length - 1;
    
    currentChunkSpan.textContent = resultsState.currentChunkIndex + 1;
}

/**
 * Show error message in the results container
 * @param {string} message - The error message to display
 */
function showError(message) {
    resultChunksContainer.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            <p>${message}</p>
        </div>
    `;
    resultsContainer.style.display = 'block';
}

/**
 * Show loading indicator
 * @param {boolean} isLoading - Whether loading is in progress
 */
function setLoading(isLoading) {
    resultsState.isLoading = isLoading;
    loadingIndicator.style.display = isLoading ? 'flex' : 'none';
}

// Initialize the component
document.addEventListener('DOMContentLoaded', initResultsDisplay);

// Export functions for use by other components
window.resultsDisplay = {
    setResponseData,
    setLoading,
    showError
};
