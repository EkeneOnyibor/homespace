const productId = window.PRODUCT_ID;

window.addEventListener('pageshow', function() {
    fetch(`/get-cart-quantity/${productId}/`)
        .then(res => res.json())
        .then(data => {
            if (data.quantity > 0) {
                showQuantityControls(data.quantity);
            }
        });
});

function handleAddToCart(productId) {
    fetch(`/add-to-cart/${productId}/`)
        .then(res => res.json())
        .then(data => {
            updateCartCount(data.cart_count);
            showQuantityControls(1);
        });
}

function showQuantityControls(quantity) {
    document.getElementById('add-to-cart-btn').style.display = 'none';
    document.getElementById('quantity-controls').style.display = 'flex';
    document.getElementById('quantity-display').innerText = quantity;
}

function changeQuantity(productId, change) {
    const display = document.getElementById('quantity-display');
    let currentQty = parseInt(display.innerText);
    let newQty = currentQty + change;

    fetch(`/update-cart/${productId}/?quantity=${newQty}`)
        .then(res => res.json())
        .then(data => {
            updateCartCount(data.cart_count);
            if (newQty <= 0) {
                document.getElementById('add-to-cart-btn').style.display = 'block';
                document.getElementById('quantity-controls').style.display = 'none';
            } else {
                display.innerText = newQty;
            }
        });
}