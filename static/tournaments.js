document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.getElementById('luck-index-tooltip-trigger');
    const content = document.getElementById('luck-index-tooltip-content');

    if (trigger && content) {
        // Show on hover
        trigger.addEventListener('mouseover', function() {
            const rect = trigger.getBoundingClientRect();
            // Position below the trigger icon
            content.style.left = (rect.left + window.scrollX) + 'px'; 
            content.style.top = (rect.bottom + window.scrollY + 5) + 'px'; 
            content.style.display = 'block';
        });

        // Hide when mouse leaves trigger OR tooltip content
        trigger.addEventListener('mouseout', function() {
            setTimeout(() => {
                if (!content.matches(':hover')) {
                    content.style.display = 'none';
                }
            }, 100); 
        });
        content.addEventListener('mouseleave', function() {
            content.style.display = 'none';
        });
    }
});