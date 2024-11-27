const backendUrl = 'https://8c07-77-240-35-7.ngrok-free.app'; // No trailing slash

document.getElementById('recommendButton').addEventListener('click', async () => {
  const movieTitle = document.getElementById('movieInput').value;

  const response = await fetch(`${backendUrl}/recommend?title=${encodeURIComponent(movieTitle)}`);
  const data = await response.json();

  const recommendationsList = document.getElementById('recommendations');
  recommendationsList.innerHTML = ''; // Clear previous recommendations

  if (data.recommendations) {
    data.recommendations.forEach(async (movie) => {
      // Fetch movie details for poster and description
      const movieDetails = await fetch(`${backendUrl}/movie-details?title=${encodeURIComponent(movie)}`);
      const details = await movieDetails.json();

      // Create a movie card
      const card = document.createElement('div');
      card.classList.add('movie-card');

      card.innerHTML = `
        <img src="${details.poster_url}" alt="${details.title}" class="movie-poster">
        <h3>${details.title}</h3>
        <p>${details.description}</p>
      `;
      recommendationsList.appendChild(card);
    });
  } else {
    recommendationsList.innerHTML = `<p>${data.error}</p>`;
  }
});






const inputField = document.getElementById('movieInput');

inputField.addEventListener('input', async () => {
  const query = inputField.value;

  if (query.length > 1) { // Trigger only for queries longer than 1 character
    const response = await fetch(`${backendUrl}/suggest?query=${encodeURIComponent(query)}`);
    const suggestions = await response.json();

    showSuggestions(suggestions);
  } else {
    clearSuggestions();
  }
});

function showSuggestions(suggestions) {
  const suggestionBox = document.getElementById('suggestionBox') || createSuggestionBox();

  suggestionBox.innerHTML = '';
  suggestions.forEach((suggestion) => {
    const suggestionItem = document.createElement('div');
    suggestionItem.className = 'suggestion-item';
    suggestionItem.textContent = suggestion;

    suggestionItem.addEventListener('click', () => {
      inputField.value = suggestion;
      clearSuggestions();
    });

    suggestionBox.appendChild(suggestionItem);
  });
}

function clearSuggestions() {
  const suggestionBox = document.getElementById('suggestionBox');
  if (suggestionBox) suggestionBox.innerHTML = '';
}

function createSuggestionBox() {
  const box = document.createElement('div');
  box.id = 'suggestionBox';
  box.className = 'suggestion-box';
  inputField.parentNode.appendChild(box);
  return box;
}
