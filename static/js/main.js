const toggle = document.getElementById('darkModeToggle');
        const body = document.getElementById('body');

        if (localStorage.getItem('darkMode') === 'enabled') {
            body.classList.add('dark-mode');
            toggle.checked = true;
        }

        toggle.addEventListener('change', () => {
            if (toggle.checked) {
                body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            } else {
                body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
            }
        });

 document.addEventListener("DOMContentLoaded", function() {
       let lastScrollTop = 0;
       const header = document.querySelector('.header-dashboard');
    
       window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            header.classList.add('header-hidden');
        } else {
            header.classList.remove('header-hidden');
        }
                
        lastScrollTop = scrollTop;
    });
});
