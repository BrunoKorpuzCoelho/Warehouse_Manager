document.addEventListener('DOMContentLoaded', function() {
    const brandSelect = document.getElementById('brand-select');
    function loadBrands() {
        fetch('/get_brands')
            .then(response => response.json())
            .then(data => {
                data.sort((a, b) => a.name.localeCompare(b.name));
                data.forEach(brand => {
                    const option = document.createElement('option');
                    option.value = brand.id; 
                    option.text = brand.name;  
                    brandSelect.appendChild(option);
                });
                $('#brand-select').select2({
                    placeholder: 'Select a brand',
                    allowClear: true
                });
            })
            .catch(error => {
                console.error('Error loading brands:', error);
            });
    }
    loadBrands();
});


document.addEventListener('DOMContentLoaded', function() {
    const productTypeSelect = document.getElementById('product_type-select');
    function loadProductTypes() {
        fetch('/get-product-type')
            .then(response => response.json())
            .then(data => {
                data.sort((a, b) => a.name.localeCompare(b.name));
                                data.forEach(t => {
                    const option = document.createElement('option');
                    option.value = t.id; 
                    option.text = t.name;  
                    productTypeSelect.appendChild(option);
                });
                if (typeof $ !== 'undefined' && $.fn.select2) {
                    $('#product_type-select').select2({
                        placeholder: 'Select a product type',
                        allowClear: true
                    });
                }
            })
            .catch(error => {
                console.error('Error loading product types:', error);
            });
    }
    loadProductTypes();
});
