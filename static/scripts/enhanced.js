// Enhanced interactivity for portfolio website

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.navbar a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add ripple effect
            addRippleEffect(this);
        });
    });
    
    // Add loading animation
    document.body.classList.add('loaded');
    
    // Portfolio cards hover effects
    const cards = document.querySelectorAll('.cards');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Form validation enhancement
    const contactForm = document.getElementById('contact-input');
    if (contactForm) {
        const inputs = contactForm.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
        });
    }
});

// Ripple effect function
function addRippleEffect(element) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Scroll reveal animation
window.addEventListener('scroll', reveal);

function reveal() {
    const reveals = document.querySelectorAll('.cards, .about-text h3');
    
    reveals.forEach(element => {
        const windowHeight = window.innerHeight;
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            element.classList.add('active');
        }
    });
}

// Add loading class
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.body.classList.add('page-loaded');
    }, 100);
});
