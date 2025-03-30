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
    document.querySelectorAll(".table-container table").forEach(table => {
        const rows = Array.from(table.querySelectorAll("tr")).filter(row => 
            !row.querySelector("th") || row.querySelector("td")
        );
    
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll(".stat"));
            // Skip rows with no stat cells or header rows
            if (cells.length === 0 || row.querySelector("th")) return;
    
            const values = cells.map(cell => {
                const text = cell.textContent.replace('%', '');
                return parseFloat(text) || 0;
            });
    
            // Find min and max values
            const minValue = Math.min(...values);
            const maxValue = Math.max(...values);
    
            cells.forEach((cell, index) => {
                const value = values[index];
                
                // Clear previous highlighting
                cell.classList.remove("green", "red");
                
                if (cell.classList.contains("positive")) {
                    if (value === maxValue) {
                        cell.classList.add("green");
                    } else if (value === minValue) {
                        cell.classList.add("red");
                    }
                } else if (cell.classList.contains("negative")) {
                    if (value === minValue) {
                        cell.classList.add("green");
                    } else if (value === maxValue) {
                        cell.classList.add("red");
                    }
                }
            });
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