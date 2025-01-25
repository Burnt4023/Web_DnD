document.addEventListener("DOMContentLoaded", function() {
    const tooltips = document.querySelectorAll('.tooltip');
    
    tooltips.forEach(function(tooltip) {
        const tooltipContent = tooltip.querySelector('.tooltip-content');

        tooltip.addEventListener('mouseenter', function() {
            const rect = tooltipContent.getBoundingClientRect();
            const windowWidth = window.innerWidth;

            // Ajustar la posición horizontal
            if (rect.left < 0) {
                tooltipContent.style.left = '125%';
            } else if (rect.right > windowWidth) {
                tooltipContent.style.left = 'auto';
                tooltipContent.style.right = '125%';
            }
        });
    });
});