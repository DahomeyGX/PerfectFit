document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('barcode-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const barcode = document.getElementById('barcode').value;
            
            fetch('/check-barcode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ barcode: barcode })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result-message').textContent = data.message;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

document.getElementById('add-item').addEventListener('click', function() {
    const container = document.getElementById('items-container');
    const index = container.children.length + 1;
    
    const itemDiv = document.createElement('div');
    itemDiv.classList.add('item');
    
    itemDiv.innerHTML = `
        <label for="item_${index}">Item:</label>
        <input type="text" id="item_${index}" name="items[]" required>
        <label for="price_${index}">Price:</label>
        <input type="text" id="price_${index}" name="prices[]" required>
    `;
    
    container.appendChild(itemDiv);
});
