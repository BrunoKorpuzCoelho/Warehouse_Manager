document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("qrCodeModal");
    const qrCodeImage = document.getElementById("qrCodeImage");
    const modalTitle = document.getElementById("modalTitle");
    const span = document.getElementsByClassName("close")[0];

    document.querySelectorAll('.generate-qr-code').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            modalTitle.innerText = `QR Code for ${productName}`;
            modalTitle.innerHTML = `QR Code for <span style="color: var(--color-danger);">${productName}</span>`;
            qrCodeImage.src = `/generate_qr_code/${productId}`;
            modal.style.display = "block";
        });
    });
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

