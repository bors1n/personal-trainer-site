    window.addEventListener('scroll', toggleBackToTopButton);

    // Smooth scroll to top on page load
    window.addEventListener('DOMContentLoaded', (event) => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Menu functionality
    document.addEventListener('DOMContentLoaded', () => {
        // Close dropdowns when clicking outside
        document.addEventListener('click', (event) => {
            // Close all dropdowns if clicking outside of any dropdown
            if (!event.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                    dropdown.classList.remove('dropdown-open');
                    dropdown.parentElement.querySelector('[tabindex="0"]').blur();
                });
            }
        });

        // Handle dropdown menu items clicks
        document.querySelectorAll('.dropdown-content a').forEach(link => {
            link.addEventListener('click', () => {
                // Close the dropdown when a menu item is clicked
                const dropdown = link.closest('.dropdown-content');
                dropdown.classList.remove('dropdown-open');
                dropdown.parentElement.querySelector('[tabindex="0"]').blur();
            });
        });
    });

    // Smooth scrolling for all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }); 