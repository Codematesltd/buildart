document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.carousel-container img');
    const indicators = document.querySelectorAll('.bottom-5 button');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    let currentIndex = 0;
    let isTransitioning = false;

    function showImage(index) {
        if (isTransitioning) return;
        isTransitioning = true;

        images.forEach(img => {
            img.style.transition = 'opacity 1000ms ease';
            img.classList.add('opacity-0');
        });
        indicators.forEach(ind => ind.classList.remove('opacity-100'));
        
        setTimeout(() => {
            images[index].classList.remove('opacity-0');
            indicators[index].classList.add('opacity-100');
            isTransitioning = false;
        }, 50);
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage(currentIndex);
    }

    // Event listeners
    nextBtn?.addEventListener('click', nextImage);
    prevBtn?.addEventListener('click', prevImage);
    
    // Auto advance every 5 seconds if not hovering
    let interval = setInterval(nextImage, 5000);
    
    const carousel = document.querySelector('.carousel-container');
    if (carousel) {
        carousel.addEventListener('mouseenter', () => clearInterval(interval));
        carousel.addEventListener('mouseleave', () => {
            clearInterval(interval);
            interval = setInterval(nextImage, 5000);
        });

        // Touch support
        let touchstartX = 0;
        let touchendX = 0;
        
        carousel.addEventListener('touchstart', e => {
            touchstartX = e.changedTouches[0].screenX;
            clearInterval(interval);
        }, {passive: true});

        carousel.addEventListener('touchend', e => {
            touchendX = e.changedTouches[0].screenX;
            handleSwipe();
            interval = setInterval(nextImage, 5000);
        }, {passive: true});

        function handleSwipe() {
            const SWIPE_THRESHOLD = 50;
            const diff = touchendX - touchstartX;
            
            if (Math.abs(diff) > SWIPE_THRESHOLD) {
                if (diff > 0) prevImage();
                else nextImage();
            }
        }
    }

    // Initialize first image
    showImage(0);
});