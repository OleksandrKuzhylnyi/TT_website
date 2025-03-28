function addPlayer() {
    const playerInput = document.getElementById('player_name');
    const player = playerInput.value.trim();
    if (!player) return;

    addPlayerElement(player);
    playerInput.value = '';
    updatePlayersArea();
}

function addPlayerElement(player) {
    const playerContainer = document.getElementById('players-container');
    const playerItem = document.createElement('div');
    playerItem.className = 'player-item';
    playerItem.innerHTML = `<span>${player}</span><button class="remove-player">×</button>`;
    playerContainer.appendChild(playerItem);
}

function updatePlayersArea() {
    const playerItems = document.querySelectorAll('#players-container .player-item span');
    const players = Array.from(playerItems).map(span => span.textContent);
    document.getElementById('players_area').value = players.join('\n');
}

document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector(".table-container table");
    const rows = Array.from(table.querySelectorAll("tbody tr"));

    // Iterate over each row (excluding the header row)
    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll(".stat"));
        const values = cells.map(cell => parseFloat(cell.textContent));

        // Find the min and max values in the row
        const minValue = Math.min(...values);
        const maxValue = Math.max(...values);

        // Apply colors to each cell in the row
        cells.forEach((cell, index) => {
        const value = values[index];

        if (cell.classList.contains("positive")) {
            // Positive metrics: green for max, red for min
            if (value === maxValue) {
            cell.classList.add("green");
            } else if (value === minValue) {
            cell.classList.add("red");
            }
        } else if (cell.classList.contains("negative")) {
            // Negative metrics: green for min, red for max
            if (value === minValue) {
            cell.classList.add("green");
            } else if (value === maxValue) {
            cell.classList.add("red");
            }
        }
        });
    });

    const inputField = document.getElementById('player_name');
    const suggestionsBox = document.getElementById('autocomplete-suggestions');

    let debounceTimer;
    let abortController = null;

    inputField.addEventListener('input', function () {
        const query = inputField.value.trim();

        // Clear previous operations
        clearTimeout(debounceTimer);
        if (abortController) abortController.abort();
        suggestionsBox.classList.remove('show'); // Hide immediately

        if (query.length === 0) {
            suggestionsBox.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            abortController = new AbortController(); // Create a new abort controller

            fetch(`/autocomplete?query=${encodeURIComponent(query)}`, {
                signal: abortController.signal // Link to abort controller
            })
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = ''; // Clear previous suggestions

                if (data.length > 0) {
                    data.forEach(suggestion => {
                        const div = document.createElement('div');
                        div.textContent = suggestion;
                        div.style.cursor = 'pointer';
                        div.style.padding = '5px';
                        div.style.backgroundColor = '#f0f0f0';
                        div.style.margin = '2px 0';

                        // Handle suggestion selection
                        div.addEventListener('click', () => {
                            inputField.value = suggestion; // Fill input with selected suggestion
                            suggestionsBox.innerHTML = ''; // Clear suggestions
                            suggestionsBox.classList.remove('show'); // Hide suggestions box
                        });

                        suggestionsBox.appendChild(div);
                    });
                } else {
                    suggestionsBox.innerHTML = '<div style="padding: 5px;">No matches found</div>';
                }

                // Show the suggestions box after content is ready
                suggestionsBox.classList.add('show');
            })
            .catch(error => {
                if (error.name !== 'AbortError') { // Ignore abort errors
                    console.error('Error fetching suggestions:', error);
                }
            });
        }, 300);
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function (event) {
        if (!suggestionsBox.contains(event.target) && event.target !== inputField) {
            suggestionsBox.innerHTML = '';
            suggestionsBox.classList.remove('show'); // Properly hide with transition
        }
    });

    const playersArea = document.getElementById('players_area');
    const players = playersArea.value.split('\n').filter(p => p.trim() !== '');
    players.forEach(addPlayerElement);

    document.getElementById('players-container').addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-player')) {
            const playerItem = e.target.closest('.player-item');
            playerItem.remove();
            updatePlayersArea();
        }
    });
});