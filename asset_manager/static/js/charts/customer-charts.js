document.addEventListener("DOMContentLoaded", function() {
    // Customer Chart
    const customerChartCtx = document.getElementById('customerChart').getContext('2d');
    new Chart(customerChartCtx, {
        type: 'doughnut',
        data: {
            labels: assignmentStatusLabels,
            datasets: [{
                data: [assignedAssets, unassignedAssets ],
                backgroundColor: ['#28a745', '#dc3545'],
            }]
        }
    });
});

