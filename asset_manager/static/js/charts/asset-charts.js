document.addEventListener("DOMContentLoaded", function() {
    // Warranty Chart
    const ctx = document.getElementById('warrantyChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: warrantyStatusLabels,
            datasets: [{
                data: [assetsUnderWarranty, assetsOutOfWarranty],
                backgroundColor: ['#28a745', '#dc3545'],
            }]
        }
    });
});