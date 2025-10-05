document.getElementById("roll-btn").addEventListener("click", async () => {
    const response = await fetch("/roll");
    const data = await response.json();
  
    // Update UI
    document.getElementById("dice-result").textContent = data.dice;
    document.getElementById("player-pos").textContent = data.position;
    document.getElementById("player-money").textContent = data.money;
    
    // Show event message
    showEventMessage(data.event);
    
    // Animate movement
    await animateMovement(data.position, data.dice);
    
    // Highlight final position
    highlightTile(data.position);
});

async function animateMovement(finalPos, steps) {
    // Animate player moving step by step
    let currentPos = parseInt(document.getElementById("player-pos").textContent);
    
    for (let i = 0; i < steps; i++) {
        await new Promise(resolve => setTimeout(resolve, 300));
        currentPos = (currentPos + 1) % 40;
        highlightTile(currentPos);
    }
}

function highlightTile(index) {
    document.querySelectorAll(".space").forEach(tile => {
        tile.classList.remove("player-on");
    });
    
    const targetTile = document.querySelector(`.space[data-index='${index}']`);
    if (targetTile) {
        targetTile.classList.add("player-on");
    }
}

function showEventMessage(message) {
    // Display event message to user
    const msgDiv = document.getElementById("event-message");
    msgDiv.textContent = message;
    msgDiv.style.display = "block";
    
    setTimeout(() => {
        msgDiv.style.display = "none";
    }, 3000);
}