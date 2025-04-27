// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the love button and message elements
    const loveButton = document.getElementById('showLove');
    const loveSentMessage = document.querySelector('.love-sent-message');
    
    // Add click event to the love button
    loveButton.addEventListener('click', function() {
        // Display the love sent message
        loveSentMessage.style.display = 'block';
        
        // Create floating hearts effect
        createFloatingHearts();
        
        // Vibrate the device if supported (mobile feature)
        if (navigator.vibrate) {
            navigator.vibrate(200);
        }
    });
    
    // Function to create floating hearts animation
    function createFloatingHearts() {
        for (let i = 0; i < 12; i++) {
            const heart = document.createElement('div');
            heart.classList.add('floating-heart');
            heart.innerHTML = '❤️';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = (Math.random() * 3) + 2 + 's';
            document.body.appendChild(heart);
            
            // Remove the heart element after animation completes
            setTimeout(() => {
                heart.remove();
            }, 5000);
        }
    }
    
    // Add floating heart style
    const style = document.createElement('style');
    style.textContent = `
        .floating-heart {
            position: fixed;
            font-size: 1.5rem;
            bottom: -20px;
            animation: float linear forwards;
            z-index: 9999;
            pointer-events: none;
        }
        
        @keyframes float {
            0% {
                bottom: -20px;
                opacity: 1;
                transform: translateX(0) scale(1);
            }
            100% {
                bottom: 100vh;
                opacity: 0;
                transform: translateX(calc(Math.random() * 100 - 50px)) scale(0.5);
            }
        }
    `;
    document.head.appendChild(style);
    
    // Add touch feedback to list items
    const listItems = document.querySelectorAll('.reasons li');
    listItems.forEach(item => {
        item.addEventListener('touchstart', function() {
            this.style.backgroundColor = '#f0c4d0';
        });
        
        item.addEventListener('touchend', function() {
            this.style.backgroundColor = '#f8e1e8';
        });
    });
});
