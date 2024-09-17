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

        function resetPassword(button) {
            const userId = button.getAttribute('data-user-id');
        
            if (confirm('Are you sure you want to reset the password for this user?')) {
                fetch(`/reset-password/${userId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': "{{ csrf_token() }}"
                    }
                })
                .then(response => response.text())
                .then(data => {
                    alert('Password reset successfully.');
                    location.reload();  
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while resetting the password.');
                });
            }
        }

        function redirectToSchedule() {
            window.location.href = "/schedule";
        }
