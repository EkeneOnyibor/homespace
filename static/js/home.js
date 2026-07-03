document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('carouselTrack');
   
    if (!track) return;
   
    const cards = track.querySelectorAll('.carousel-card');
    const cardWidth = 220 + 20; // card width + gap
    let currentIndex = 0;
    const totalCards = cards.length;

    if (totalCards === 0) return;

    // Clone all cards and append to end for seamless loop
    cards.forEach(card => {
        const clone = card.cloneNode(true);
        track.appendChild(clone);
    });

    setInterval(() => {
        currentIndex++;

        track.style.transition = 'transform 0.8s ease-in-out';
        track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;

        // When we reach the cloned set, jump back silently
        if (currentIndex >= totalCards) {
            setTimeout(() => {
                track.style.transition = 'none';
                track.style.transform = `translateX(0)`;
                currentIndex = 0;
            }, 800);
        }
    }, 3000);
});