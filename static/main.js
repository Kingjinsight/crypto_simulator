document.getElementById("roll-btn").addEventListener("click", async () => {
    const response = await fetch("/roll");
    const data = await response.json();
  
    // Update UI
    document.getElementById("dice-result").textContent = data.dice;
    document.getElementById("player-pos").textContent = data.position;
  
    // highlight player tile visually
    highlightTile(data.position);
  });
  
  function highlightTile(index) {
    // remove existing highlights
    document.querySelectorAll(".space").forEach(tile => {
      tile.classList.remove("player-on");
    });
  
    // highlight the new position (assuming each .space has an index attribute)
    const targetTile = document.querySelector(`.space[data-index='${index}']`);
    if (targetTile) targetTile.classList.add("player-on");
  }
  