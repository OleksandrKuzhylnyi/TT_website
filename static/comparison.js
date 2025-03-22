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
});
});