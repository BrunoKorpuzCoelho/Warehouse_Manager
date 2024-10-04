document.addEventListener('DOMContentLoaded', function() {
    function applyFilters() {
        const recordType = document.getElementById('filter-record-type').value.toLowerCase();
        const status = document.getElementById('filter-status').value.toLowerCase();
        const logType = document.getElementById('filter-log-type').value.toLowerCase();

        const rows = document.querySelectorAll('#schedule-records tr');

        rows.forEach(row => {
            const recordTypeValue = row.querySelector('.record-type').textContent.toLowerCase();
            const statusValue = row.querySelector('.status').textContent.toLowerCase();
            const logTypeValue = row.querySelector('.log-type').textContent.toLowerCase();

            let showRow = true;

            if (recordType !== 'all' && recordType !== recordTypeValue) {
                showRow = false;
            }

            if (status !== 'all' && status !== statusValue) {
                showRow = false;
            }

            if (logType !== 'all' && logType !== logTypeValue) {
                showRow = false;
            }

            if (showRow) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    document.querySelector('.schedule-manager-search-btn').addEventListener('click', applyFilters);
});