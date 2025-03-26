function addPlayer() {
    const playerInput = document.getElementById('new_player');
    const playersArea = document.getElementById('players_area');
    const player = playerInput.value.trim();
    
    if (player) {
        if (playersArea.value) {
            playersArea.value += '\n' + player;
        } else {
            playersArea.value = player;
        }
        playerInput.value = '';
    }
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


        const inputField = document.getElementById('player_name');
        const suggestionsBox = document.getElementById('autocomplete-suggestions');

        inputField.addEventListener('input', function () {
            const query = inputField.value.trim();
            if (query.length === 0) {
                suggestionsBox.innerHTML = ''; // Clear suggestions if input is empty
                return;
            }

            // Fetch suggestions from the server
            fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
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
                            div.addEventListener('click', function () {
                                inputField.value = suggestion; // Fill input with selected suggestion
                                suggestionsBox.innerHTML = ''; // Clear suggestions
                            });

                            suggestionsBox.appendChild(div);
                            suggestionsBox.classList.add('show');
                        });
                    } else {
                        suggestionsBox.innerHTML = '<div style="padding: 5px;">No matches found</div>';
                        suggestionsBox.classList.add('show');
                    }
                })
                .catch(error => console.error('Error fetching suggestions:', error));
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function (event) {
            if (!suggestionsBox.contains(event.target) && event.target !== inputField) {
                suggestionsBox.innerHTML = '';
            }
        });
    });
});