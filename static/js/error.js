<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function() {
    // Código para exibir alertas
    var alerts = document.querySelectorAll('.alert');
    var currentAlertIndex = 0;

    function showNextAlert() {
        if (currentAlertIndex < alerts.length) {
            var alert = alerts[currentAlertIndex];
            alert.style.display = "block"; 
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = 1;

            setTimeout(function() {
                hideCurrentAlert(alert);
            }, 2000); 
        }
    }

    function hideCurrentAlert(alert) {
        alert.style.opacity = 0;
        setTimeout(function() {
            alert.style.display = "none";
            currentAlertIndex++; 
            showNextAlert(); 
        }, 500); 
    }

    showNextAlert();
=======
document.addEventListener("DOMContentLoaded", function() {
    // Código para exibir alertas
    var alerts = document.querySelectorAll('.alert');
    var currentAlertIndex = 0;

    function showNextAlert() {
        if (currentAlertIndex < alerts.length) {
            var alert = alerts[currentAlertIndex];
            alert.style.display = "block"; 
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = 1;

            setTimeout(function() {
                hideCurrentAlert(alert);
            }, 2000); 
        }
    }

    function hideCurrentAlert(alert) {
        alert.style.opacity = 0;
        setTimeout(function() {
            alert.style.display = "none";
            currentAlertIndex++; 
            showNextAlert(); 
        }, 500); 
    }

    showNextAlert();
>>>>>>> origin/main
});