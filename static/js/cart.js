function addToCart(productId) {
    fetch(`/add-to-cart/${productId}/`)
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
            showCardQuantityControls(productId, 1);
        })
        .catch(error => {
            console.log("Error:", error);
        });
}

function showCardQuantityControls(productId, quantity) {
    const btn = document.getElementById(`add-btn-${productId}`);
    const controls = document.getElementById(`qty-controls-${productId}`);
    const display = document.getElementById(`qty-display-${productId}`);

    if (btn) btn.style.display = 'none';
    if (controls) controls.style.display = 'flex';
    if (display) display.innerText = quantity;
}

function changeCardQuantity(productId, change) {
    const display = document.getElementById(`qty-display-${productId}`);
    let currentQty = parseInt(display.innerText);
    let newQty = currentQty + change;

    fetch(`/update-cart/${productId}/?quantity=${newQty}`)
        .then(res => res.json())
        .then(data => {
            updateCartCount(data.cart_count);
            if (newQty <= 0) {
                const btn = document.getElementById(`add-btn-${productId}`);
                const controls = document.getElementById(`qty-controls-${productId}`);
                if (btn) btn.style.display = 'block';
                if (controls) controls.style.display = 'none';
            } else {
                display.innerText = newQty;
            }
        });
}

function updateCartCount(count) {
    const cartCount = document.getElementById("cart-count");
    if (cartCount) {
        cartCount.innerText = count;
    }
}

window.addEventListener('pageshow', function(event) {
    fetch('/get-cart-count/')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.cart_count);
        });
});

function changeCartQuantity(productId, change) {
    const qtyDisplay = document.getElementById(`qty-${productId}`);
    let currentQty = parseInt(qtyDisplay.innerText);
    let newQty = currentQty + change;

    fetch(`/update-cart/${productId}/?quantity=${newQty}`)
        .then(res => res.json())
        .then(data => {
            updateCartCount(data.cart_count);
            if (newQty <= 0) {
                document.getElementById(`cart-item-${productId}`).remove();
            } else {
                qtyDisplay.innerText = newQty;
            }
            location.reload();
        });
}

document.addEventListener("DOMContentLoaded", function() {
    const alertBox = document.querySelector(".cart-alert");
    if (alertBox) {
        setTimeout(function() {
            alertBox.style.opacity = "0";
            setTimeout(function() {
                alertBox.style.display = "none";
            }, 500);
        }, 5000);
    }

    // Check existing cart quantities on page load
    document.querySelectorAll('[data-product-id]').forEach(function(el) {
        const productId = el.getAttribute('data-product-id');
        fetch(`/get-cart-quantity/${productId}/`)
            .then(res => res.json())
            .then(data => {
                if (data.quantity > 0) {
                    showCardQuantityControls(productId, data.quantity);
                }
            });
    });
});